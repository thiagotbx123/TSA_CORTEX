"""
Migrate Gabrielle's 43 tasks from spreadsheet to Linear.
Parent issues for grouped tasks, sub-issues for individual items.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

LINEAR_API_KEY = os.getenv('LINEAR_API_KEY')
LINEAR_URL = 'https://api.linear.app/graphql'
HEADERS = {
    'Authorization': LINEAR_API_KEY,
    'Content-Type': 'application/json',
}

# === IDs ===
TEAM_RAC = '5a021b9f-bb1a-49fa-ad3b-83422c46c357'
GABI_ID = 'd9745bdb-7138-4345-9303-516aa6e4ec39'

# Projects
PROJECT_ARCHER    = 'f6dade9a-05b6-482b-a2ee-16f3d04ae711'
PROJECT_MAILCHIMP = 'bd241897-7518-4963-a9a9-ec99fc36936f'
PROJECT_STAIRCASE = 'dcd11ea1-d883-4f36-8f21-c6d84027bdd5'

# Status IDs
STATUS = {
    'Backlog':     '0a00ef8b-f3e2-4b1b-8413-1961c91fe495',
    'Todo':        'ab5844ed-4edd-4d84-99fc-34ab37859486',
    'In Progress': '8fd63b1a-1ec5-460f-b0c9-605ac0d6e04b',
    'Paused':      'c7a6728a-dee7-4e2b-a60f-476e699d4b54',
    'Done':        '6e10418c-81fe-467d-aed3-d4c75577d16e',
    'Canceled':    '97ef043e-ccb7-4e2a-b75b-7542ef198abc',
}

# Demand Type Labels
LABEL_IMPROVEMENT = '989f1692-9c59-4379-9895-dd46d324e10b'
LABEL_MAINTENANCE = 'ea1b2051-0e6b-4f1e-84be-8595ff41415e'
LABEL_STRATEGIC   = '26587b0c-1e0a-4186-a8e1-a8e0dabf353d'
LABEL_ROUTINE     = '5645598f-5d57-4232-b43a-df549d8bad1d'
LABEL_INCIDENT    = '091ca07b-d2d8-4b28-a6b3-4031ec4ffea0'
LABEL_DATAGEN     = '7b7288ef-77a8-49ff-b5d6-7d9e922ff483'

# Customer Labels
LABEL_ARCHER    = '20f03684-1ef1-4194-8eeb-67c0ec7f89c1'
LABEL_MAILCHIMP = '0f7cdc0e-b4d1-4c1b-844a-0c0751014055'
LABEL_STAIRCASE = 'b48ab084-e6b6-46c7-9a99-e9022d3057e2'

# Scope Labels
LABEL_EXTERNAL = '97bef858-f435-43e4-9c24-6325dca9a1d3'
LABEL_INTERNAL = 'd0706bf9-db94-4079-a4e1-7541515864de'

DEMAND_MAP = {
    'External(Customer)': None,  # Infer from context -> usually External(Customer) = maintenance/strategic
    'Improvement': LABEL_IMPROVEMENT,
    'Maintenance': LABEL_MAINTENANCE,
    'Strategic': LABEL_STRATEGIC,
    'Routine': LABEL_ROUTINE,
    'Incident': LABEL_INCIDENT,
    'Data Gen.': LABEL_DATAGEN,
}


def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    r = requests.post(LINEAR_URL, headers=HEADERS, json=payload)
    data = r.json()
    if 'errors' in data:
        print(f"  ERROR: {data['errors']}")
        return None
    return data.get('data')


def create_issue(title, description='', state_id=None, label_ids=None,
                 project_id=None, priority=None, parent_id=None):
    mutation = '''
    mutation CreateIssue($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue { id identifier url }
        }
    }
    '''
    input_data = {'title': title, 'teamId': TEAM_RAC, 'assigneeId': GABI_ID}
    if description:
        input_data['description'] = description
    if state_id:
        input_data['stateId'] = state_id
    if label_ids:
        input_data['labelIds'] = label_ids
    if project_id:
        input_data['projectId'] = project_id
    if priority is not None:
        input_data['priority'] = priority
    if parent_id:
        input_data['parentId'] = parent_id

    result = gql(mutation, {'input': input_data})
    if result and result.get('issueCreate', {}).get('success'):
        return result['issueCreate']['issue']
    return None


def map_status(raw):
    s = raw.strip().lower()
    if 'done' in s: return STATUS['Done']
    if 'in progress' in s: return STATUS['In Progress']
    if 'canceled' in s: return STATUS['Canceled']
    if 'b.b.c' in s or 'on hold' in s: return STATUS['Paused']
    if 'to do' in s: return STATUS['Todo']
    return STATUS['Backlog']


def map_demand_label(demand_type):
    dt = demand_type.strip()
    if dt in DEMAND_MAP and DEMAND_MAP[dt]:
        return DEMAND_MAP[dt]
    # External(Customer) -> map to Strategic (closest for customer-facing work)
    if 'external' in dt.lower():
        return LABEL_STRATEGIC
    return None


def get_customer(task):
    """Determine customer from priority or customer field."""
    cust = task.get('customer', '').strip()
    prio = task.get('priority', '').strip()

    # Check explicit customer field first
    if cust.lower() in ('mailchimp',):
        return 'Mailchimp'
    if cust.lower() in ('staircase',):
        return 'Staircase'

    # Check priority field (Gabi uses this for customer)
    if prio.lower() in ('mailchimp', 'mailchimp'):
        return 'Mailchimp'
    if prio.lower() in ('archer',):
        return 'Archer'
    if prio.lower() in ('staircase',):
        return 'Staircase'

    # Row 33 has no priority but is about abandoned carts (Mailchimp context)
    if 'abandon' in task.get('focus', '').lower() or 'mailchimp' in task.get('last_update', '').lower():
        return 'Mailchimp'

    return 'Unknown'


def get_scope(task):
    """Determine External/Internal scope."""
    dt = task.get('demand_type', '').strip().lower()
    if 'external' in dt:
        return 'External'
    # Most of Gabi's work is customer-facing
    return 'External'


def get_parent_status(sub_statuses):
    """Determine parent status from children."""
    if all(s == STATUS['Done'] for s in sub_statuses):
        return STATUS['Done']
    if any(s == STATUS['In Progress'] for s in sub_statuses):
        return STATUS['In Progress']
    return STATUS['In Progress']


def build_labels(task):
    """Build label list: demand type + customer + scope."""
    labels = []

    # Demand type
    dl = map_demand_label(task.get('demand_type', ''))
    if dl:
        labels.append(dl)

    # Customer
    cust = get_customer(task)
    cust_map = {
        'Archer': LABEL_ARCHER,
        'Mailchimp': LABEL_MAILCHIMP,
        'Staircase': LABEL_STAIRCASE,
    }
    if cust in cust_map:
        labels.append(cust_map[cust])

    # Scope
    scope = get_scope(task)
    labels.append(LABEL_EXTERNAL if scope == 'External' else LABEL_INTERNAL)

    return labels


def build_description(task):
    """Build issue description from task data."""
    parts = []
    if task.get('focus'):
        parts.append(f"**Focus:** {task['focus']}")
    if task.get('date_add'):
        parts.append(f"**Date Added:** {task['date_add']}")
    if task.get('eta'):
        parts.append(f"**ETA:** {task['eta']}")
    if task.get('delivery_date'):
        parts.append(f"**Delivery Date:** {task['delivery_date']}")
    if task.get('last_update') and len(task['last_update']) < 500:
        parts.append(f"\n**Last Update:** {task['last_update']}")
    elif task.get('last_update'):
        parts.append(f"\n**Last Update:** {task['last_update'][:500]}...")
    parts.append(f"\n*Migrated from TSA_Tasks_Consolidate (GABI tab) on 2026-03-18*")
    return '\n'.join(parts)


# === TASK GROUPINGS ===
# Each group: (parent_title, customer, project_id, row_numbers)
GROUPS = [
    # Archer
    ('Archer - BIA Campaign & Data Generation', 'Archer', PROJECT_ARCHER,
     [1, 2, 3, 21, 24, 34, 41, 42, 43]),

    # Mailchimp
    ('Mailchimp - Website & Shopify Integration', 'Mailchimp', PROJECT_MAILCHIMP,
     [4, 5, 6, 16, 27, 28, 29]),
    ('Mailchimp - Email Automation & Campaigns', 'Mailchimp', PROJECT_MAILCHIMP,
     [12, 13, 17, 18, 19, 20, 26, 39, 40]),
    ('Mailchimp - Dataset & Activity Plans', 'Mailchimp', PROJECT_MAILCHIMP,
     [30, 31, 32, 33, 14]),
    ('Mailchimp - UAT & Design', 'Mailchimp', PROJECT_MAILCHIMP,
     [10, 11, 35, 36]),

    # Staircase
    ('Staircase - Data & Japanese Version', 'Staircase', PROJECT_STAIRCASE,
     [7, 22, 23, 25, 37, 38]),
    ('Staircase - Adjustments & Bug Fixes', 'Staircase', PROJECT_STAIRCASE,
     [8, 9, 15]),
]


def main():
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '_migration_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    tasks = {t['row']: t for t in all_data['gabi']}

    print('=' * 60)
    print('MIGRATING GABRIELLE TO LINEAR')
    print(f'Total tasks: {len(tasks)}')
    print('=' * 60)

    created = {'parents': 0, 'subs': 0, 'errors': 0}
    issue_map = {}  # row -> issue info

    # Phase 1: Create parent issues
    print('\n[Phase 1] Creating parent issues...')
    parent_ids = {}  # group_title -> issue_id

    for title, customer, project_id, rows in GROUPS:
        # Determine parent status from children
        sub_statuses = [map_status(tasks[r]['status']) for r in rows if r in tasks]
        parent_status = get_parent_status(sub_statuses)

        # Build parent labels
        cust_map = {
            'Archer': LABEL_ARCHER,
            'Mailchimp': LABEL_MAILCHIMP,
            'Staircase': LABEL_STAIRCASE,
        }
        parent_labels = [LABEL_EXTERNAL]
        if customer in cust_map:
            parent_labels.append(cust_map[customer])

        desc = f"Parent issue grouping {len(rows)} related tasks.\n\n*Migrated from TSA_Tasks_Consolidate (GABI tab) on 2026-03-18*"

        issue = create_issue(
            title=title,
            description=desc,
            state_id=parent_status,
            label_ids=parent_labels,
            project_id=project_id,
        )
        if issue:
            parent_ids[title] = issue['id']
            print(f"  {issue['identifier']}: {title}")
            created['parents'] += 1
        else:
            print(f"  FAILED: {title}")
            created['errors'] += 1
        time.sleep(0.12)

    # Phase 2: Create sub-issues
    print(f'\n[Phase 2] Creating sub-issues ({sum(len(r) for _, _, _, r in GROUPS)} tasks)...')

    for title, customer, project_id, rows in GROUPS:
        parent_id = parent_ids.get(title)
        if not parent_id:
            print(f"  SKIP group {title} - no parent")
            continue

        for row_num in rows:
            task = tasks.get(row_num)
            if not task:
                print(f"  SKIP row {row_num} - not found")
                continue

            # Build title: clean up focus field
            focus = task.get('focus', '').strip()
            if len(focus) > 100:
                focus = focus[:97] + '...'
            sub_title = focus if focus else f"Task #{row_num}"

            issue = create_issue(
                title=sub_title,
                description=build_description(task),
                state_id=map_status(task['status']),
                label_ids=build_labels(task),
                project_id=project_id,
                parent_id=parent_id,
            )
            if issue:
                issue_map[row_num] = issue
                print(f"  {issue['identifier']}: {sub_title[:60]}")
                created['subs'] += 1
            else:
                print(f"  FAILED row {row_num}: {sub_title[:60]}")
                created['errors'] += 1
            time.sleep(0.12)

    # Summary
    print(f'\n{"=" * 60}')
    print(f'GABRIELLE MIGRATION COMPLETE')
    print(f'  Parents: {created["parents"]}')
    print(f'  Subs:    {created["subs"]}')
    print(f'  Errors:  {created["errors"]}')
    print(f'  Total:   {created["parents"] + created["subs"]}')
    print(f'{"=" * 60}')

    # Save mapping
    mapping_path = os.path.join(os.path.dirname(__file__), '_gabi_issue_map.json')
    save_map = {str(k): v for k, v in issue_map.items()}
    save_map['_parents'] = {k: v for k, v in parent_ids.items()}
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(save_map, f, indent=2, ensure_ascii=False)
    print(f'  Mapping saved to: {mapping_path}')


if __name__ == '__main__':
    main()
