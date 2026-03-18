"""
Migrate Thiago's 115 tasks from spreadsheet to Linear.
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
THIAGO_ID = 'a6063009-d822-49f1-a638-6cebfe59e89e'

# Projects
PROJECT_QBO        = 'ee2eabec-8466-4163-a38f-8c22324477ae'
PROJECT_GEM        = 'e7e478a1-2fe3-4a03-84a6-73719a6ffd59'
PROJECT_GONG       = 'ab0dde3c-09c4-4b53-8bf2-c78579240730'
PROJECT_MAILCHIMP  = 'bd241897-7518-4963-a9a9-ec99fc36936f'
PROJECT_SITEIMPROVE = '30ddab6f-eaed-42ac-9ecd-b2d03b668012'
PROJECT_CALLRAIL   = '2e8d65ef-6892-4300-83ce-1b48c5eb5e17'
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
LABEL_QBO         = '75d960f0-ebcb-4b42-9c83-c80cc7c3fade'
LABEL_GEM         = '9e0dd48f-90bb-42fa-9376-5a28ca0d08ad'
LABEL_GONG        = '63aad579-bb8c-4f71-93d5-9be5f2bd4c1c'
LABEL_MAILCHIMP   = '0f7cdc0e-b4d1-4c1b-844a-0c0751014055'
LABEL_SITEIMPROVE = 'e27a6fd9-811d-48de-ace3-5d45a07b2f59'
LABEL_CALLRAIL    = '50e0d66d-addc-4a83-90c2-862a5775afeb'
LABEL_APOLLO      = '0852f0d5-b582-49dd-9ab0-7006c45210ab'
LABEL_TROPIC      = '7c646e26-c927-47a0-9f8d-5e770a256b63'
LABEL_PEOPLE_AI   = '890f30a7-2f47-46d6-8cf2-c38509fc73ff'
LABEL_HOCKEYSTACK = '954a563d-1c24-4fcd-bf61-ba5c07accd78'

# Scope Labels
LABEL_EXTERNAL = '97bef858-f435-43e4-9c24-6325dca9a1d3'
LABEL_INTERNAL = 'd0706bf9-db94-4079-a4e1-7541515864de'

DEMAND_MAP = {
    'Improvement': LABEL_IMPROVEMENT,
    'Maintenance': LABEL_MAINTENANCE,
    'Strategic':   LABEL_STRATEGIC,
    'Routine':     LABEL_ROUTINE,
    'Incident':    LABEL_INCIDENT,
    'Data Gen.':   LABEL_DATAGEN,
    'External(Customer)': LABEL_STRATEGIC,
}

# Customer to label mapping
CUSTOMER_LABEL_MAP = {
    'QBO':         LABEL_QBO,
    'GEM':         LABEL_GEM,
    'GONG':        LABEL_GONG,
    'MailChimp':   LABEL_MAILCHIMP,
    'MAILCHIMP':   LABEL_MAILCHIMP,
    'SITEIMPROVE': LABEL_SITEIMPROVE,
    'CALLRAIL':    LABEL_CALLRAIL,
    'APOLLO':      LABEL_APOLLO,
    'TROPIC':      LABEL_TROPIC,
    'PEOPLE.AI':   LABEL_PEOPLE_AI,
    'HockeyStack': LABEL_HOCKEYSTACK,
    'HOCKEYSTACK': LABEL_HOCKEYSTACK,
}

# Internal customers (no customer label, Internal scope)
INTERNAL_CUSTOMERS = {'Waki', 'CODA', 'GENERAL', 'Routine'}


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
    input_data = {'title': title, 'teamId': TEAM_RAC, 'assigneeId': THIAGO_ID}
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


def get_scope(task):
    """Internal for CODA/GENERAL/Waki/Routine, External for all others."""
    cust = task.get('customer', '').strip()
    if cust in INTERNAL_CUSTOMERS:
        return 'Internal'
    return 'External'


def get_parent_status(sub_statuses):
    if all(s == STATUS['Done'] for s in sub_statuses):
        return STATUS['Done']
    if any(s == STATUS['In Progress'] for s in sub_statuses):
        return STATUS['In Progress']
    if any(s == STATUS['Todo'] for s in sub_statuses):
        return STATUS['In Progress']
    return STATUS['In Progress']


def build_labels(task):
    """Build label list: demand type + customer + scope."""
    labels = []

    # Demand type
    dt = task.get('demand_type', '').strip()
    if dt in DEMAND_MAP:
        labels.append(DEMAND_MAP[dt])

    # Customer label (only for external customers)
    cust = task.get('customer', '').strip()
    if cust in CUSTOMER_LABEL_MAP:
        labels.append(CUSTOMER_LABEL_MAP[cust])

    # Scope
    scope = get_scope(task)
    labels.append(LABEL_EXTERNAL if scope == 'External' else LABEL_INTERNAL)

    return labels


def build_description(task):
    parts = []
    if task.get('focus'):
        parts.append(f"**Focus:** {task['focus']}")
    if task.get('date_add'):
        parts.append(f"**Date Added:** {task['date_add']}")
    if task.get('eta'):
        parts.append(f"**ETA:** {task['eta']}")
    if task.get('delivery_date'):
        parts.append(f"**Delivery Date:** {task['delivery_date']}")
    if task.get('priority') and not task['priority'].startswith('http'):
        parts.append(f"**Priority:** {task['priority']}")
    if task.get('last_update') and len(task['last_update']) < 500:
        parts.append(f"\n**Last Update:** {task['last_update']}")
    elif task.get('last_update'):
        parts.append(f"\n**Last Update:** {task['last_update'][:500]}...")
    parts.append(f"\n*Migrated from TSA_Tasks_Consolidate (THIAGO tab) on 2026-03-18*")
    return '\n'.join(parts)


# === TASK GROUPINGS ===
# (parent_title, primary_customer_label, scope, project_id, row_numbers)
GROUPS = [
    # === CODA (Internal documentation) ===
    ('CODA - TSA Process Documentation', None, 'Internal', PROJECT_INTERNAL,
     [4, 5, 6, 7, 8, 32, 35]),

    ('CODA - Customer Overview Pages', None, 'Internal', PROJECT_INTERNAL,
     [9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20]),

    ('CODA - Flowchart & Knowledge Base', None, 'Internal', PROJECT_INTERNAL,
     [21, 113]),

    # === QBO (External) ===
    ('QBO - Winter Release Validation', LABEL_QBO, 'External', PROJECT_QBO,
     [39, 40, 42, 49, 50, 51, 52, 53]),

    ('QBO - Environment Health & Sweeps', LABEL_QBO, 'External', PROJECT_QBO,
     [47, 57, 58, 59, 60, 61, 62, 63, 64]),

    ('QBO - Financial Investigations', LABEL_QBO, 'External', PROJECT_QBO,
     [41, 43, 44, 45, 46, 54, 55, 56, 66, 67]),

    ('QBO - Deliverables & Handover', LABEL_QBO, 'External', PROJECT_QBO,
     [2, 22, 38, 48, 65, 111, 112]),

    # === GEM (External) ===
    ('GEM - Strategy & Due Diligence', LABEL_GEM, 'External', PROJECT_GEM,
     [3, 68, 69, 70]),

    ('GEM - Implementation & Delivery', LABEL_GEM, 'External', PROJECT_GEM,
     [71, 72, 73, 74, 75]),

    # === GONG (External) ===
    ('Gong - Investigations & Support', LABEL_GONG, 'External', PROJECT_GONG,
     [76, 77, 78, 79]),

    # === MAILCHIMP (External) ===
    ('Mailchimp - Support & Audits', LABEL_MAILCHIMP, 'External', PROJECT_MAILCHIMP,
     [33, 34, 80, 81, 82, 83, 84]),

    # === CALLRAIL (External) ===
    ('CallRail - Investigation & Response', LABEL_CALLRAIL, 'External', PROJECT_CALLRAIL,
     [87, 88, 89]),

    # === SITEIMPROVE (External) ===
    ('Siteimprove - Deep Learning & Validation', LABEL_SITEIMPROVE, 'External', PROJECT_SITEIMPROVE,
     [85, 86]),

    # === HOCKEYSTACK (External, no project per Q6) ===
    ('HockeyStack - Analysis & Onboarding', LABEL_HOCKEYSTACK, 'External', None,
     [17, 90, 91]),

    # === OTHER CUSTOMERS (External, no project) ===
    ('Other Customers - Research & Analysis', None, 'External', None,
     [92, 93, 94]),

    # === INTERNAL ===
    ('Internal - Waki Alignment', None, 'Internal', PROJECT_INTERNAL,
     [1, 27, 28, 37]),

    ('Internal - TSA Process & KPIs', None, 'Internal', PROJECT_INTERNAL,
     [23, 24, 25, 26, 29, 30, 31, 36]),

    ('Internal - Tool Development', None, 'Internal', PROJECT_INTERNAL,
     [95, 96, 97, 98, 99, 100, 101, 102, 103, 106, 107]),

    ('Internal - Leadership & Coaching', None, 'Internal', PROJECT_INTERNAL,
     [104, 108, 109, 110, 114, 115, 116]),
]


def main():
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '_migration_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    tasks = {t['row']: t for t in all_data['thiago']}

    # Verify coverage
    all_rows = set()
    for _, _, _, _, rows in GROUPS:
        all_rows.update(rows)
    missing = set(tasks.keys()) - all_rows
    extra = all_rows - set(tasks.keys())
    if missing:
        print(f"WARNING: {len(missing)} rows not in any group: {sorted(missing)}")
    if extra:
        print(f"WARNING: {len(extra)} rows in groups but not in data: {sorted(extra)}")

    print('=' * 60)
    print('MIGRATING THIAGO TO LINEAR')
    print(f'Total tasks: {len(tasks)}')
    print(f'Groups: {len(GROUPS)}')
    print(f'Rows covered: {len(all_rows)}')
    print('=' * 60)

    created = {'parents': 0, 'subs': 0, 'errors': 0}
    issue_map = {}

    # Phase 1: Create parent issues
    print('\n[Phase 1] Creating parent issues...')
    parent_ids = {}

    for title, cust_label, scope, project_id, rows in GROUPS:
        sub_statuses = [map_status(tasks[r]['status']) for r in rows if r in tasks]
        parent_status = get_parent_status(sub_statuses)

        # Parent labels: scope + customer (if applicable)
        parent_labels = []
        if cust_label:
            parent_labels.append(cust_label)
        parent_labels.append(LABEL_EXTERNAL if scope == 'External' else LABEL_INTERNAL)

        desc = f"Parent issue grouping {len(rows)} related tasks.\n\n*Migrated from TSA_Tasks_Consolidate (THIAGO tab) on 2026-03-18*"

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
    total_subs = sum(len(r) for _, _, _, _, r in GROUPS)
    print(f'\n[Phase 2] Creating sub-issues ({total_subs} tasks)...')

    for title, cust_label, scope, project_id, rows in GROUPS:
        parent_id = parent_ids.get(title)
        if not parent_id:
            print(f"  SKIP group {title} - no parent")
            continue

        for row_num in rows:
            task = tasks.get(row_num)
            if not task:
                print(f"  SKIP row {row_num} - not found")
                continue

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
    print(f'THIAGO MIGRATION COMPLETE')
    print(f'  Parents: {created["parents"]}')
    print(f'  Subs:    {created["subs"]}')
    print(f'  Errors:  {created["errors"]}')
    print(f'  Total:   {created["parents"] + created["subs"]}')
    print(f'{"=" * 60}')

    # Save mapping
    mapping_path = os.path.join(os.path.dirname(__file__), '_thiago_issue_map.json')
    save_map = {str(k): v for k, v in issue_map.items()}
    save_map['_parents'] = {k: v for k, v in parent_ids.items()}
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(save_map, f, indent=2, ensure_ascii=False)
    print(f'  Mapping saved to: {mapping_path}')


if __name__ == '__main__':
    main()
