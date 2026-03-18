"""
Migrate Alexandra's tasks from Google Sheets to Linear.
Creates parent issues for grouped tasks, sub-issues for individual items.
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

# === IDs from Linear ===
TEAM_RAC = '5a021b9f-bb1a-49fa-ad3b-83422c46c357'
PROJECT_QBO = 'ee2eabec-8466-4163-a38f-8c22324477ae'
PROJECT_WFS = '1ccf280f-066b-46ae-bd31-8331ac94e064'
ALEXANDRA_ID = '19b6975e-3026-450b-bc01-f468ad543028'

# Status IDs (Raccoons)
STATUS = {
    'Backlog':     '0a00ef8b-f3e2-4b1b-8413-1961c91fe495',
    'Todo':        'ab5844ed-4edd-4d84-99fc-34ab37859486',
    'In Progress': '8fd63b1a-1ec5-460f-b0c9-605ac0d6e04b',
    'Paused':      'c7a6728a-dee7-4e2b-a60f-476e699d4b54',
    'In Review':   '89e4c72d-57aa-4774-8cf0-b00ee103d17c',
    'Done':        '6e10418c-81fe-467d-aed3-d4c75577d16e',
    'Canceled':    '97ef043e-ccb7-4e2a-b75b-7542ef198abc',
}

# Label IDs (Demand Type)
LABELS = {
    'Improvement': '989f1692-9c59-4379-9895-dd46d324e10b',
    'Maintenance': 'ea1b2051-0e6b-4f1e-84be-8595ff41415e',
    'Strategic':   '26587b0c-1e0a-4186-a8e1-a8e0dabf353d',
    'Routine':     '5645598f-5d57-4232-b43a-df549d8bad1d',
    'Incident':    '091ca07b-d2d8-4b28-a6b3-4031ec4ffea0',
}


def gql(query, variables=None):
    """Execute a GraphQL query against Linear API."""
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    r = requests.post(LINEAR_URL, headers=HEADERS, json=payload)
    data = r.json()
    if 'errors' in data:
        print(f"  ERROR: {data['errors']}")
        return None
    return data.get('data')


def create_issue(title, team_id, description='', state_id=None, assignee_id=None,
                 label_ids=None, project_id=None, priority=None, due_date=None,
                 parent_id=None):
    """Create a Linear issue and return its ID."""
    mutation = '''
    mutation CreateIssue($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue {
                id
                identifier
                url
            }
        }
    }
    '''
    input_data = {
        'title': title,
        'teamId': team_id,
    }
    if description:
        input_data['description'] = description
    if state_id:
        input_data['stateId'] = state_id
    if assignee_id:
        input_data['assigneeId'] = assignee_id
    if label_ids:
        input_data['labelIds'] = label_ids
    if project_id:
        input_data['projectId'] = project_id
    if priority is not None:
        input_data['priority'] = priority
    if due_date and due_date not in ('TBD', '', 'None'):
        input_data['dueDate'] = due_date
    if parent_id:
        input_data['parentId'] = parent_id

    result = gql(mutation, {'input': input_data})
    if result and result.get('issueCreate', {}).get('success'):
        issue = result['issueCreate']['issue']
        return issue
    return None


def map_status(raw_status):
    """Map spreadsheet status to Linear status ID."""
    s = raw_status.strip().lower()
    if 'done' in s:
        return STATUS['Done']
    if 'in progress' in s:
        return STATUS['In Progress']
    if 'canceled' in s:
        return STATUS['Canceled']
    if 'b.b.c' in s or 'bbc' in s:
        return STATUS['Paused']
    return STATUS['Backlog']


def map_demand_label(demand_type, focus):
    """Map demand type + focus to our 5 label categories."""
    dt = demand_type.strip().lower()
    f = focus.strip().lower()

    # Explicit labels from sheet
    if 'improvement' in dt:
        return LABELS['Improvement']
    if 'maintenance' in dt:
        return LABELS['Maintenance']
    if 'routine' in dt:
        return LABELS['Routine']
    if 'incident' in dt:
        return LABELS['Incident']
    if 'strategic' in dt:
        return LABELS['Strategic']

    # Infer from focus for External(Customer) / Data Gen
    if any(kw in f for kw in ['winter release', 'environment prep', 'improvements on']):
        return LABELS['Improvement']
    if any(kw in f for kw in ['sow', 'playbook', 'pre scoping', 'pro and cons']):
        return LABELS['Strategic']
    if any(kw in f for kw in ['ticket analysis', 'features review', 'uat']):
        return LABELS['Maintenance']
    if any(kw in f for kw in ['documentation', 'handover', 'onboarding', 'handoff']):
        return LABELS['Routine']

    # Default
    return LABELS['Maintenance']


def get_parent_status(tasks):
    """Determine parent status based on subtask statuses."""
    statuses = [t['status'].strip().lower() for t in tasks]
    if any('in progress' in s for s in statuses):
        return STATUS['In Progress']
    if any('b.b.c' in s for s in statuses):
        return STATUS['Paused']
    if all('done' in s for s in statuses):
        return STATUS['Done']
    if all('canceled' in s for s in statuses):
        return STATUS['Canceled']
    return STATUS['Done']  # mix of done + canceled


def get_latest_date(tasks, field='eta'):
    """Get the latest valid date from tasks."""
    dates = []
    for t in tasks:
        d = t.get(field, '').strip().split('\n')[0].split(' ')[0].strip()
        if d and d != 'TBD' and len(d) >= 10:
            dates.append(d[:10])
    return max(dates) if dates else None


def get_project(customer):
    """Get project ID based on customer."""
    c = customer.strip().upper()
    if c == 'QBO':
        return PROJECT_QBO
    if c == 'WFS':
        return PROJECT_WFS
    return None  # standalone


# ============================================================
# TASK DATA (from spreadsheet)
# ============================================================
TASKS = [
    {"row":1,"status":"🟢 Done","demand_type":"External(Customer)","customer":"WFS","focus":"SOW improvement","date_add":"2026-01-07","eta":"2026-01-22","last_update":"Intuit need to define if the demo capabilities will be built into an existing environment (TCO or Keystone Construction) or a new standalone environment.( entrega feita, monitorando ....)","delivery_date":"2026-01-22"},
    {"row":2,"status":"🟢 Done","demand_type":"External(Customer)","customer":"WFS","focus":"List of Pro and Cons for environment decision","date_add":"2026-01-12","eta":"2026-01-16","last_update":"First draft of the final document completed, improvements needed. Kat is reviewing the first version.","delivery_date":"2026-01-16"},
    {"row":3,"status":"🟢 Done","demand_type":"Data Gen.","customer":"HockeyStack","focus":"Handover","date_add":"2026-01-12","eta":"2026-01-16","last_update":"Handover HockeyStack for Thiago during this week.","delivery_date":"2026-01-16"},
    {"row":4,"status":"🟢 Done","demand_type":"Routine","customer":"QBO","focus":"Onboarding and handover activities","date_add":"2026-01-07","eta":"2026-01-08","last_update":"The first handover meeting happened yesterday. It's necessary to summarize all learning, and perform the handover of upcoming activities together with Thiago.","delivery_date":"2026-01-08"},
    {"row":5,"status":"🟡 In Progress","demand_type":"Routine","customer":"QBO","focus":"Onboarding and handover activities","date_add":"2026-07-01","eta":"2026-03-31","last_update":"Keeping the hypercare routine with Thiago","delivery_date":""},
    {"row":6,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Documentation review","date_add":"2026-01-12","eta":"2026-01-16","last_update":"Stay aligned with Kat's comments on the first version of the features and efforts.","delivery_date":"2026-01-16"},
    {"row":7,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Documentation review","date_add":"2026-01-12","eta":"2026-01-19","last_update":"Review, study and improve the first version of the document with features and efforts for Winter release (FY26).","delivery_date":"2026-01-19"},
    {"row":8,"status":"🟢 Done","demand_type":"External(Customer)","customer":"WFS","focus":"List of Pro and Cons for environment decision","date_add":"2026-01-07","eta":"2026-01-09","last_update":"Prepare a first draft of the document to support Intuit's decision","delivery_date":"2026-01-09"},
    {"row":9,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Features review","date_add":"2026-01-12","eta":"2026-02-02","last_update":"Capture evidence on the TCO environment to confirm which features are enabled or not, to support the tracker and effort document.","delivery_date":"2026-02-02"},
    {"row":10,"status":"🔴 Canceled","demand_type":"External(Customer)","customer":"QBO","focus":"Features review","date_add":"2026-01-12","eta":"2026-02-09","last_update":"Capture evidence on the Construction Sales environment to confirm which features are enabled or not.","delivery_date":""},
    {"row":11,"status":"🔴 Canceled","demand_type":"External(Customer)","customer":"QBO","focus":"Features review","date_add":"2026-01-12","eta":"2026-02-16","last_update":"Capture evidence on the Construction Events environment to confirm which features are enabled or not.","delivery_date":""},
    {"row":12,"status":"🟢 Done","demand_type":"External(Customer)","customer":"WFS","focus":"SOW - draft","date_add":"2026-01-19","eta":"2026-01-22","last_update":"Prepare draft version of the SOW.","delivery_date":"2026-01-22"},
    {"row":13,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"documentation preparation","date_add":"2026-01-19","eta":"2026-01-21","last_update":"Prepare a documentation with the updated list of the features to Intuit fulfill with the missing dates of the IES.","delivery_date":"2026-01-21"},
    {"row":14,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"documentation preparation","date_add":"2026-01-28","eta":"2026-01-28","last_update":"Rerun the IES Write it Straight validation to confirm scope changes and green status updates","delivery_date":"2026-01-28"},
    {"row":15,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Support on UAT Environment","date_add":"2026-01-27","eta":"2026-01-27","last_update":"Follow up on the child company access issue and support to unblock the creation of test users for the UAT environments.","delivery_date":"2026-01-27"},
    {"row":16,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"ticket analysis","date_add":"2026-01-22","eta":"2026-01-22","last_update":"Support the analysis and refinement of the ticket PLA-3201","delivery_date":"2026-01-22"},
    {"row":17,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"ticket analysis","date_add":"2026-01-23","eta":"2026-01-23","last_update":"Support the analysis and refinement of the ticket PLA-3202","delivery_date":"2026-01-23"},
    {"row":18,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"ticket analysis","date_add":"2026-01-26","eta":"2026-01-26","last_update":"Support the analysis and refinement of the ticket PLA-3224","delivery_date":"2026-01-26"},
    {"row":19,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"ticket analysis","date_add":"2026-01-27","eta":"2026-01-28","last_update":"Support the analysis and refinement of the ticket PLA-3227","delivery_date":"2026-01-28"},
    {"row":20,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Documentation","date_add":"2026-01-28","eta":"2026-01-30","last_update":"Review the new 3 documents sent by Intuit for the Winter Release","delivery_date":"2026-01-30"},
    {"row":21,"status":"🔴 B.B.C.","demand_type":"External(Customer)","customer":"WFS","focus":"SOW improvement","date_add":"2026-01-28","eta":"TBD","last_update":"Improve the SOW with Intuit, lock the scope, and incorporate comments and revisions.","delivery_date":""},
    {"row":22,"status":"🔴 B.B.C.","demand_type":"External(Customer)","customer":"WFS","focus":"SOW improvement","date_add":"2026-02-04","eta":"TBD","last_update":"Prepare a draft for the SOW Milestones chapter to validate internally.","delivery_date":""},
    {"row":23,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"documentation preparation","date_add":"2026-02-04","eta":"2026-02-13","last_update":"Organize and update the FY26 tracker based on the latest Winter Release docs from Intuit and the updates on IES February Release FY26.","delivery_date":"2026-02-13"},
    {"row":24,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Environment preparation","date_add":"2026-02-02","eta":"2026-02-10","last_update":"Accompany delivery of the UAT environment for the winter release, supporting Engineering team as needed.","delivery_date":"2026-02-10"},
    {"row":25,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Environment preparation","date_add":"2026-02-02","eta":"2026-02-04","last_update":"Prepare the TestBook for the UAT environment.","delivery_date":"2026-02-04"},
    {"row":26,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Environment preparation","date_add":"2026-02-02","eta":"2026-02-05","last_update":"Run TestBook on the UAT environment and capture evidences.","delivery_date":"2026-02-05"},
    {"row":27,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"ticket analysis","date_add":"2026-01-27","eta":"2026-01-28","last_update":"Support the analysis and refinement of the ticket KLA-2399","delivery_date":"2026-01-28"},
    {"row":28,"status":"🟢 Done","demand_type":"External(Customer)","customer":"WFS","focus":"SOW improvement","date_add":"2026-01-30","eta":"2026-02-03","last_update":"Improve the SOW according to internal review.","delivery_date":"2026-02-03"},
    {"row":29,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Environment preparation","date_add":"2026-02-05","eta":"2026-02-10","last_update":"Support data ingestion for equalization of Intuit's UAT and Sales environments for FY26 and update the tickets with the progress.","delivery_date":"2026-02-10"},
    {"row":30,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Environment preparation","date_add":"2026-02-10","eta":"2026-02-12","last_update":"Run again TestBook on the UAT environment.","delivery_date":"2026-02-12"},
    {"row":31,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-10","eta":"2026-02-12","last_update":"Review created tickets for data ingestion related to FY26","delivery_date":"2026-02-12"},
    {"row":32,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-10","eta":"2026-02-11","last_update":"Prepare action plan for Winter Release to share internally","delivery_date":"2026-02-11"},
    {"row":33,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-12","eta":"2026-02-19","last_update":"Validate evidences collected for IES Construction logging and correcting gaps that may appear, update the tickets accordingly","delivery_date":"2026-02-19"},
    {"row":34,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-12","eta":"2026-02-19","last_update":"Finish the Collection of evidences for IES Construction UAT.","delivery_date":"2026-02-19"},
    {"row":35,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-12","eta":"2026-02-19","last_update":"Finish the Collection of evidences for IES Construction Events.","delivery_date":"2026-02-19"},
    {"row":36,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-12","eta":"2026-02-19","last_update":"Finish the Collection of evidences for IES Construction Sales","delivery_date":"2026-02-19"},
    {"row":37,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-10","eta":"2026-02-23","last_update":"Validate IES Construction and UAT after ingestion. Share daily internal progress updates.","delivery_date":"2026-02-23"},
    {"row":38,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-17","eta":"2026-02-19","last_update":"Check and answer Intuit's comments on tracker.","delivery_date":"2026-02-19"},
    {"row":39,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-17","eta":"2026-02-19","last_update":"Check, answer and work on the Intuit's comments on slack channel","delivery_date":"2026-02-23"},
    {"row":40,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-17","eta":"2026-02-23","last_update":"Close remaining gaps and proceed with the remaining features across all environments, after Intuit's validation.","delivery_date":"2026-02-24"},
    {"row":41,"status":"🟡 In Progress","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-09","eta":"2026-03-31","last_update":"Review and prepare backlog tickets after Winter Release","delivery_date":""},
    {"row":42,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-09","last_update":"Collect and organize evidences from the TCO environment for the Winter release","delivery_date":"2026-03-09"},
    {"row":43,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-09","last_update":"Collect and organize evidences from the Professional Services environment for the Winter release","delivery_date":"2026-03-09"},
    {"row":44,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-13","last_update":"Collect and organize evidences from the QBOA environment for the Winter release","delivery_date":""},
    {"row":45,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-09","last_update":"Collect and organize evidences from the Events environment for the Winter release","delivery_date":"2026-03-09"},
    {"row":46,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-13","last_update":"Collect and organize evidences from the Non Profit environment for the Winter release","delivery_date":""},
    {"row":47,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-09","last_update":"Validate the evidences from TCO for the Winter release","delivery_date":"2026-03-09"},
    {"row":48,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-13","last_update":"Validate the evidences from Professional services for the Winter release","delivery_date":""},
    {"row":49,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-13","last_update":"Validate the evidences from QBOA for the Winter release","delivery_date":""},
    {"row":50,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-09","last_update":"Validate the evidences from Events for the Winter release","delivery_date":"2026-03-09"},
    {"row":51,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-13","last_update":"Collect and organize evidences from the Manufacturing environment for the Winter release","delivery_date":""},
    {"row":52,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-13","last_update":"Validate the evidences from Manufacturing for the Winter release","delivery_date":""},
    {"row":53,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-02","eta":"2026-03-09","last_update":"Validate the evidences from Non Profit for the Winter release","delivery_date":""},
    {"row":54,"status":"🟡 In Progress","demand_type":"Improvement","customer":"QBO","focus":"Playbook","date_add":"2026-03-04","eta":"2026-03-20","last_update":"Prepare a plan for the QBO Playbook","delivery_date":""},
    {"row":55,"status":"🟢 Done","demand_type":"External(Customer)","customer":"WFS","focus":"Pre scoping","date_add":"2026-03-03","eta":"2026-03-04","last_update":"Prepare WFS pre-scoping questions for Intuit to anticipate potential blockers before story scoping.","delivery_date":"2026-03-04"},
    {"row":56,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-03","eta":"2026-03-04","last_update":"Define an action plan to validate the remaining Intuit environments.","delivery_date":"2026-03-04"},
    {"row":57,"status":"🟢 Done","demand_type":"Maintenance","customer":"QBO","focus":"Ticket analysis","date_add":"2026-02-25","eta":"2026-02-26","last_update":"Support the analysis and refinement of the ticket PLA-3308","delivery_date":"2026-02-26"},
    {"row":58,"status":"🟢 Done","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-02-01","eta":"2026-03-11","last_update":"Support the Winter Release work end to end, from setting up the new UAT environment to completing feature checks and evidence across all Intuit environments","delivery_date":""},
    {"row":59,"status":"🟡 In Progress","demand_type":"External(Customer)","customer":"QBO","focus":"improvements on the environment","date_add":"2026-03-11","eta":"TBD","last_update":"Support improvements on the environment management together with CE team to prevent incidents and reduce risk across all the environments.","delivery_date":""},
    {"row":60,"status":"🟡 In Progress","demand_type":"External(Customer)","customer":"QBO","focus":"Winter Release","date_add":"2026-03-11","eta":"2026-03-27","last_update":"Document lessons learned from this Winter Release to improve the next release execution","delivery_date":""},
    {"row":61,"status":"🟡 In Progress","demand_type":"External(Customer)","customer":"WFS","focus":"Pre scoping","date_add":"2026-03-11","eta":"2026-03-17","last_update":"Prepare and align next steps to support Pre scoping phase.","delivery_date":""},
]


# ============================================================
# GROUP DEFINITIONS — parent issues with their subtask rows
# ============================================================
GROUPS = [
    {
        'title': '[QBO] Winter Release FY26',
        'customer': 'QBO',
        'label': 'Improvement',
        'priority': 2,
        'description': (
            'End-to-end Winter Release execution across all Intuit environments '
            '(TCO, Construction, Events, Non Profit, Manufacturing, QBOA, Professional Services).\n\n'
            'Covers evidence collection, validation, UAT setup, feature checks, '
            'tracker updates, and stakeholder communication.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,56,58,60],
    },
    {
        'title': '[QBO] Environment Preparation',
        'customer': 'QBO',
        'label': 'Improvement',
        'priority': 3,
        'description': (
            'UAT environment setup, data ingestion, TestBook execution and '
            'evidence collection for FY26 environments.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [24,25,26,29,30],
    },
    {
        'title': '[QBO] Ticket Analysis',
        'customer': 'QBO',
        'label': 'Maintenance',
        'priority': 3,
        'description': (
            'Analysis and refinement of engineering tickets (PLA, KLA series) '
            'supporting QBO implementation.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [16,17,18,19,27,57],
    },
    {
        'title': '[WFS] Statement of Work',
        'customer': 'WFS',
        'label': 'Strategic',
        'priority': 2,
        'description': (
            'WFS SOW drafting, improvement, internal review and Intuit alignment. '
            'Includes scope locking and milestones definition.\n\n'
            '**Note:** Some items blocked by client (B.B.C.).\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [1,12,21,22,28],
    },
    {
        'title': '[QBO] Features Review',
        'customer': 'QBO',
        'label': 'Maintenance',
        'priority': 3,
        'description': (
            'Evidence capture across environments (TCO, Construction Sales, Construction Events) '
            'to confirm enabled features for the tracker and effort document.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [9,10,11],
    },
    {
        'title': '[QBO] Documentation Preparation',
        'customer': 'QBO',
        'label': 'Routine',
        'priority': 3,
        'description': (
            'Preparation and update of feature lists, IES trackers, and '
            'release documentation for Intuit.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [13,14,23],
    },
    {
        'title': '[QBO] Documentation Review',
        'customer': 'QBO',
        'label': 'Routine',
        'priority': 3,
        'description': (
            'Review and improvement of feature documentation and effort '
            'estimations for Winter Release.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [6,7],
    },
    {
        'title': '[QBO] Onboarding & Handover',
        'customer': 'QBO',
        'label': 'Routine',
        'priority': 3,
        'description': (
            'Onboarding activities and ongoing hypercare routine with Thiago '
            'for QBO implementation.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [4,5],
    },
    {
        'title': '[WFS] Environment Decision Analysis',
        'customer': 'WFS',
        'label': 'Strategic',
        'priority': 3,
        'description': (
            'Analysis of pros and cons for WFS environment decision — '
            'whether to build into existing environment or standalone.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [2,8],
    },
    {
        'title': '[WFS] Pre Scoping',
        'customer': 'WFS',
        'label': 'Strategic',
        'priority': 3,
        'description': (
            'Pre-scoping questions and preparation for WFS story scoping with Intuit. '
            'Anticipate potential blockers before formal scoping phase.\n\n'
            '**Migrated from TSA Tasks Consolidate spreadsheet — Alexandra Lacerda**'
        ),
        'rows': [55,61],
    },
]

# Standalone issues (not part of any group)
STANDALONE = [
    {
        'title': '[HockeyStack] Handover to Thiago',
        'customer': 'HockeyStack',
        'label': 'Routine',
        'priority': 4,
        'row': 3,
    },
    {
        'title': '[QBO] Intuit Winter Release Documentation Review',
        'customer': 'QBO',
        'label': 'Routine',
        'priority': 3,
        'row': 20,
    },
    {
        'title': '[QBO] Playbook Preparation',
        'customer': 'QBO',
        'label': 'Strategic',
        'priority': 2,
        'row': 54,
    },
    {
        'title': '[QBO] UAT Environment Support',
        'customer': 'QBO',
        'label': 'Maintenance',
        'priority': 3,
        'row': 15,
    },
    {
        'title': '[QBO] Environment Improvements & Risk Reduction',
        'customer': 'QBO',
        'label': 'Improvement',
        'priority': 2,
        'row': 59,
    },
]


def build_subtask_title(task):
    """Build a clean subtask title from the task data."""
    update = task['last_update']
    # Truncate at 120 chars
    if len(update) > 120:
        update = update[:117] + '...'
    return update


def build_subtask_description(task):
    """Build description for a subtask."""
    parts = []
    parts.append(f"**Date Added:** {task['date_add']}")
    parts.append(f"**ETA:** {task['eta']}")
    if task.get('delivery_date'):
        parts.append(f"**Delivery Date:** {task['delivery_date']}")
    parts.append(f"**Demand Type (original):** {task['demand_type']}")
    parts.append(f"**Customer:** {task['customer']}")
    parts.append(f"**Focus Area:** {task['focus']}")
    parts.append('')
    parts.append(f"> {task['last_update']}")
    parts.append('')
    parts.append(f'*Migrated from spreadsheet row {task["row"]}*')
    return '\n'.join(parts)


# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    print('=' * 60)
    print('ALEXANDRA → LINEAR MIGRATION')
    print('=' * 60)

    # Build row lookup
    task_by_row = {t['row']: t for t in TASKS}

    created_issues = []
    created_subs = []

    # --- Phase 1: Create parent issues ---
    print(f'\n[Phase 1] Creating {len(GROUPS)} parent issues...')
    for g in GROUPS:
        subtasks = [task_by_row[r] for r in g['rows'] if r in task_by_row]
        parent_status = get_parent_status(subtasks)
        due = get_latest_date(subtasks)
        project = get_project(g['customer'])

        print(f"  Creating: {g['title']} ({len(subtasks)} subtasks)...", end=' ')
        issue = create_issue(
            title=g['title'],
            team_id=TEAM_RAC,
            description=g['description'],
            state_id=parent_status,
            assignee_id=ALEXANDRA_ID,
            label_ids=[LABELS[g['label']]],
            project_id=project,
            priority=g['priority'],
            due_date=due,
        )
        if issue:
            print(f"OK → {issue['identifier']}")
            g['issue_id'] = issue['id']
            g['identifier'] = issue['identifier']
            created_issues.append(issue)
        else:
            print('FAILED')
            g['issue_id'] = None

        time.sleep(0.15)  # rate limit safety

    # --- Phase 2: Create subtask issues ---
    print(f'\n[Phase 2] Creating subtask issues...')
    for g in GROUPS:
        if not g.get('issue_id'):
            continue
        subtasks = [task_by_row[r] for r in g['rows'] if r in task_by_row]
        for i, task in enumerate(subtasks, 1):
            title = build_subtask_title(task)
            desc = build_subtask_description(task)
            status = map_status(task['status'])
            label_id = map_demand_label(task['demand_type'], task['focus'])
            eta = task['eta'].split(' ')[0].strip() if task['eta'] and task['eta'] != 'TBD' else None
            project = get_project(task['customer'])

            print(f"  [{g['identifier']}] Sub {i}/{len(subtasks)}: {title[:60]}...", end=' ')
            sub = create_issue(
                title=title,
                team_id=TEAM_RAC,
                description=desc,
                state_id=status,
                assignee_id=ALEXANDRA_ID,
                label_ids=[label_id],
                project_id=project,
                priority=g['priority'],
                due_date=eta,
                parent_id=g['issue_id'],
            )
            if sub:
                print(f"OK → {sub['identifier']}")
                created_subs.append(sub)
            else:
                print('FAILED')

            time.sleep(0.12)

    # --- Phase 3: Create standalone issues ---
    print(f'\n[Phase 3] Creating {len(STANDALONE)} standalone issues...')
    for s in STANDALONE:
        task = task_by_row[s['row']]
        desc = build_subtask_description(task)
        status = map_status(task['status'])
        label_id = LABELS[s['label']]
        eta = task['eta'].split(' ')[0].strip() if task['eta'] and task['eta'] != 'TBD' else None
        project = get_project(s['customer'])

        print(f"  Creating: {s['title']}...", end=' ')
        issue = create_issue(
            title=s['title'],
            team_id=TEAM_RAC,
            description=desc,
            state_id=status,
            assignee_id=ALEXANDRA_ID,
            label_ids=[label_id],
            project_id=project,
            priority=s['priority'],
            due_date=eta,
        )
        if issue:
            print(f"OK → {issue['identifier']}")
            created_issues.append(issue)
        else:
            print('FAILED')

        time.sleep(0.15)

    # --- Summary ---
    print('\n' + '=' * 60)
    print(f'MIGRATION COMPLETE')
    print(f'  Parent issues created:     {len([g for g in GROUPS if g.get("issue_id")])}')
    print(f'  Sub-issues created:        {len(created_subs)}')
    print(f'  Standalone issues created: {len([s for s in STANDALONE])}')
    print(f'  TOTAL:                     {len(created_subs) + len(created_issues)}')
    print('=' * 60)

    # Print all created issues for reference
    print('\n--- Parent Issues ---')
    for g in GROUPS:
        if g.get('identifier'):
            print(f"  {g['identifier']}: {g['title']}")

    print('\n--- Standalone Issues ---')
    for issue in created_issues[len(GROUPS):]:
        print(f"  {issue['identifier']}: {issue.get('url', '')}")


if __name__ == '__main__':
    main()
