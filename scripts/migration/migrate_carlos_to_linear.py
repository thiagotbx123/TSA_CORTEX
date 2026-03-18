"""
Migrate Carlos's 132 tasks from spreadsheet to Linear.
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
CARLOS_ID = 'b13ca864-e0f4-4ff6-b020-ec3f4491643e'

# Projects
PROJECT_GONG       = 'ab0dde3c-09c4-4b53-8bf2-c78579240730'
PROJECT_SITEIMPROVE = '30ddab6f-eaed-42ac-9ecd-b2d03b668012'
PROJECT_APOLLO     = '6ec07cae-a9b7-4996-b207-6d8ca3634e82'
PROJECT_INTERNAL   = '26760852-ba0d-4012-adf5-d5d1dcc07671'

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
LABEL_GONG        = '63aad579-bb8c-4f71-93d5-9be5f2bd4c1c'
LABEL_SITEIMPROVE = 'e27a6fd9-811d-48de-ace3-5d45a07b2f59'
LABEL_APOLLO      = '0852f0d5-b582-49dd-9ab0-7006c45210ab'

# Scope Labels
LABEL_EXTERNAL = '97bef858-f435-43e4-9c24-6325dca9a1d3'
LABEL_INTERNAL = 'd0706bf9-db94-4079-a4e1-7541515864de'

# Product Labels (Carlos-specific)
LABEL_DEMO    = '340d1426-ad4a-4a1a-bf01-bb4d4a6d1335'
LABEL_SANDBOX = '3f6e0ccb-6f27-4c95-97a3-8e1b24fedbba'

DEMAND_MAP = {
    'Improvement': LABEL_IMPROVEMENT,
    'Maintenance': LABEL_MAINTENANCE,
    'Strategic':   LABEL_STRATEGIC,
    'Routine':     LABEL_ROUTINE,
    'Incident':    LABEL_INCIDENT,
    'Data Gen.':   LABEL_DATAGEN,
    'External(Customer)': LABEL_STRATEGIC,  # Customer-facing = strategic
}

PRIORITY_MAP = {
    'P0': 1,  # Urgent
    'P1': 2,  # High
    'P2': 3,  # Medium
    'P3': 4,  # Low
}

CUSTOMER_LABEL_MAP = {
    'Gong':        LABEL_GONG,
    'Siteimprove': LABEL_SITEIMPROVE,
    'Apollo':      LABEL_APOLLO,
}

CUSTOMER_PROJECT_MAP = {
    'Gong':        PROJECT_GONG,
    'Siteimprove': PROJECT_SITEIMPROVE,
    'Apollo':      PROJECT_APOLLO,
    'TBX':         PROJECT_INTERNAL,
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
    input_data = {'title': title, 'teamId': TEAM_RAC, 'assigneeId': CARLOS_ID}
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


def map_priority(raw):
    p = raw.strip().upper()
    if p in ('P0', 'P1', 'P2', 'P3'):
        return PRIORITY_MAP[p]
    return None


def get_scope(task):
    """Determine External/Internal scope. TBX product = Internal."""
    product = task.get('product', '').strip()
    customer = task.get('customer', '').strip()
    if product == 'TBX' or customer == 'TBX':
        return 'Internal'
    return 'External'


def get_product_labels(task):
    """Get product labels (Demo/Sandbox) based on product field."""
    product = task.get('product', '').strip()
    labels = []
    if 'Demo' in product:
        labels.append(LABEL_DEMO)
    if 'Sandbox' in product:
        labels.append(LABEL_SANDBOX)
    return labels


def get_parent_status(sub_statuses):
    """Determine parent status from children."""
    if all(s == STATUS['Done'] for s in sub_statuses):
        return STATUS['Done']
    if any(s == STATUS['In Progress'] for s in sub_statuses):
        return STATUS['In Progress']
    if any(s == STATUS['Todo'] for s in sub_statuses):
        return STATUS['In Progress']
    return STATUS['In Progress']


def build_labels(task):
    """Build label list: demand type + customer + scope + product."""
    labels = []

    # Demand type
    dt = task.get('demand_type', '').strip()
    if dt in DEMAND_MAP:
        labels.append(DEMAND_MAP[dt])

    # Customer
    cust = task.get('customer', '').strip()
    if cust in CUSTOMER_LABEL_MAP:
        labels.append(CUSTOMER_LABEL_MAP[cust])

    # Scope
    scope = get_scope(task)
    labels.append(LABEL_EXTERNAL if scope == 'External' else LABEL_INTERNAL)

    # Product
    labels.extend(get_product_labels(task))

    return labels


def build_description(task):
    """Build issue description from task data."""
    parts = []
    if task.get('focus'):
        parts.append(f"**Focus:** {task['focus']}")
    if task.get('product'):
        parts.append(f"**Product:** {task['product']}")
    if task.get('priority'):
        parts.append(f"**Priority:** {task['priority']}")
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
    parts.append(f"\n*Migrated from TSA_Tasks_Consolidate (CARLOS tab) on 2026-03-18*")
    return '\n'.join(parts)


# === TASK GROUPINGS ===
# (parent_title, customer, project_id, row_numbers)
GROUPS = [
    # === GONG ===
    ('Gong - Sandbox Development & Provisioning', 'Gong', PROJECT_GONG,
     [1, 3, 4, 14, 29, 30, 31, 33, 34, 56, 65, 115]),

    ('Gong - Demo Account Refresh & Ingestion', 'Gong', PROJECT_GONG,
     [15, 26, 28, 35, 64, 66, 67, 68, 80, 91]),

    ('Gong - Deals & Forecast', 'Gong', PROJECT_GONG,
     [10, 12, 38, 41, 42, 43, 45, 51, 57, 59, 61, 63]),

    ('Gong - Engage & AI Features', 'Gong', PROJECT_GONG,
     [46, 48, 50, 52, 53, 54, 93]),

    ('Gong - Maintenance & Bug Fixes', 'Gong', PROJECT_GONG,
     [6, 11, 16, 20, 32, 49]),

    ('Gong - Customer Calls & Alignment', 'Gong', PROJECT_GONG,
     [24, 27, 37, 55, 58, 90, 130]),

    ('Gong - Story Framework & New Initiatives', 'Gong', PROJECT_GONG,
     [116, 121, 122]),

    ('Gong - Internal & Documentation', 'Gong', PROJECT_GONG,
     [13, 117, 118, 126]),

    # === SITEIMPROVE ===
    ('Siteimprove - Setup & Configuration', 'Siteimprove', PROJECT_SITEIMPROVE,
     [2, 5, 8, 9, 17, 18, 19, 22, 25]),

    ('Siteimprove - Dataset & Table Design', 'Siteimprove', PROJECT_SITEIMPROVE,
     [21, 36, 39, 40, 44, 47, 60, 62, 78, 81]),

    ('Siteimprove - Gov Website Data Gen (v2-v3)', 'Siteimprove', PROJECT_SITEIMPROVE,
     [72, 73, 74, 75, 76, 77, 84, 85, 86, 87, 88, 89, 92]),

    ('Siteimprove - Gov Website Data Gen (v4-v6)', 'Siteimprove', PROJECT_SITEIMPROVE,
     [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]),

    ('Siteimprove - Userflows & Validation', 'Siteimprove', PROJECT_SITEIMPROVE,
     [23, 69, 70, 79, 114, 131]),

    ('Siteimprove - Financial Website', 'Siteimprove', PROJECT_SITEIMPROVE,
     [82, 94, 120]),

    ('Siteimprove - Customer Calls & Documentation', 'Siteimprove', PROJECT_SITEIMPROVE,
     [83, 119, 123, 124, 125, 127, 132]),

    # === APOLLO ===
    ('Apollo - Implementation', 'Apollo', PROJECT_APOLLO,
     [113, 128, 129]),

    # === INTERNAL ===
    ('Internal - TSA Operations (Carlos)', 'TBX', PROJECT_INTERNAL,
     [7, 71]),
]


def main():
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '_migration_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    tasks = {t['row']: t for t in all_data['carlos']}

    # Verify all rows are covered
    all_rows = set()
    for _, _, _, rows in GROUPS:
        all_rows.update(rows)
    missing = set(tasks.keys()) - all_rows
    extra = all_rows - set(tasks.keys())
    if missing:
        print(f"WARNING: {len(missing)} rows not in any group: {sorted(missing)}")
    if extra:
        print(f"WARNING: {len(extra)} rows in groups but not in data: {sorted(extra)}")

    print('=' * 60)
    print('MIGRATING CARLOS TO LINEAR')
    print(f'Total tasks: {len(tasks)}')
    print(f'Groups: {len(GROUPS)}')
    print(f'Rows covered: {len(all_rows)}')
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
        parent_labels = []
        if customer in CUSTOMER_LABEL_MAP:
            parent_labels.append(CUSTOMER_LABEL_MAP[customer])

        # Scope: Internal groups get Internal label
        if customer == 'TBX':
            parent_labels.append(LABEL_INTERNAL)
        else:
            parent_labels.append(LABEL_EXTERNAL)

        desc = f"Parent issue grouping {len(rows)} related tasks.\n\n*Migrated from TSA_Tasks_Consolidate (CARLOS tab) on 2026-03-18*"

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

            # Map priority
            priority = map_priority(task.get('priority', ''))

            issue = create_issue(
                title=sub_title,
                description=build_description(task),
                state_id=map_status(task['status']),
                label_ids=build_labels(task),
                project_id=project_id,
                priority=priority,
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
    print(f'CARLOS MIGRATION COMPLETE')
    print(f'  Parents: {created["parents"]}')
    print(f'  Subs:    {created["subs"]}')
    print(f'  Errors:  {created["errors"]}')
    print(f'  Total:   {created["parents"] + created["subs"]}')
    print(f'{"=" * 60}')

    # Save mapping
    mapping_path = os.path.join(os.path.dirname(__file__), '_carlos_issue_map.json')
    save_map = {str(k): v for k, v in issue_map.items()}
    save_map['_parents'] = {k: v for k, v in parent_ids.items()}
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(save_map, f, indent=2, ensure_ascii=False)
    print(f'  Mapping saved to: {mapping_path}')


if __name__ == '__main__':
    main()
