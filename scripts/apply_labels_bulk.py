"""Apply Customer + External/Internal labels to all migrated Alexandra issues."""
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

# Label IDs
LABEL_QBO = '75d960f0-ebcb-4b42-9c83-c80cc7c3fade'
LABEL_WFS = 'f390bd54-fce5-4422-82ce-df320de5d507'
LABEL_HOCKEYSTACK = '954a563d-1c24-4fcd-bf61-ba5c07accd78'
LABEL_EXTERNAL = '97bef858-f435-43e4-9c24-6325dca9a1d3'
LABEL_INTERNAL = 'd0706bf9-db94-4079-a4e1-7541515864de'

CUSTOMER_LABELS = {
    'QBO': LABEL_QBO,
    'WFS': LABEL_WFS,
    'HockeyStack': LABEL_HOCKEYSTACK,
}

# Issue → Customer mapping (from migration)
ISSUE_MAP = {
    # Parents
    'RAC-228': ('QBO', 'External'),
    'RAC-229': ('QBO', 'External'),
    'RAC-230': ('QBO', 'External'),
    'RAC-231': ('WFS', 'External'),
    'RAC-232': ('QBO', 'External'),
    'RAC-233': ('QBO', 'External'),
    'RAC-234': ('QBO', 'External'),
    'RAC-235': ('QBO', 'External'),
    'RAC-236': ('WFS', 'External'),
    'RAC-237': ('WFS', 'External'),
    # QBO Winter Release subs
    'RAC-238': ('QBO', 'External'),
    'RAC-239': ('QBO', 'External'),
    'RAC-240': ('QBO', 'External'),
    'RAC-241': ('QBO', 'External'),
    'RAC-242': ('QBO', 'External'),
    'RAC-243': ('QBO', 'External'),
    'RAC-244': ('QBO', 'External'),
    'RAC-245': ('QBO', 'External'),
    'RAC-246': ('QBO', 'External'),
    'RAC-247': ('QBO', 'External'),
    'RAC-248': ('QBO', 'External'),
    'RAC-249': ('QBO', 'External'),
    'RAC-250': ('QBO', 'External'),
    'RAC-251': ('QBO', 'External'),
    'RAC-252': ('QBO', 'External'),
    'RAC-253': ('QBO', 'External'),
    'RAC-254': ('QBO', 'External'),
    'RAC-255': ('QBO', 'External'),
    'RAC-256': ('QBO', 'External'),
    'RAC-257': ('QBO', 'External'),
    'RAC-258': ('QBO', 'External'),
    'RAC-259': ('QBO', 'External'),
    'RAC-260': ('QBO', 'External'),
    'RAC-261': ('QBO', 'External'),
    'RAC-262': ('QBO', 'External'),
    'RAC-263': ('QBO', 'External'),
    # QBO Env Prep subs
    'RAC-264': ('QBO', 'External'),
    'RAC-265': ('QBO', 'External'),
    'RAC-266': ('QBO', 'External'),
    'RAC-267': ('QBO', 'External'),
    'RAC-268': ('QBO', 'External'),
    # QBO Ticket Analysis subs
    'RAC-269': ('QBO', 'External'),
    'RAC-270': ('QBO', 'External'),
    'RAC-271': ('QBO', 'External'),
    'RAC-272': ('QBO', 'External'),
    'RAC-273': ('QBO', 'External'),
    'RAC-274': ('QBO', 'External'),
    # WFS SOW subs
    'RAC-275': ('WFS', 'External'),
    'RAC-276': ('WFS', 'External'),
    'RAC-277': ('WFS', 'External'),
    'RAC-278': ('WFS', 'External'),
    'RAC-279': ('WFS', 'External'),
    # QBO Features Review subs
    'RAC-280': ('QBO', 'External'),
    'RAC-281': ('QBO', 'External'),
    'RAC-282': ('QBO', 'External'),
    # QBO Doc Prep subs
    'RAC-283': ('QBO', 'External'),
    'RAC-284': ('QBO', 'External'),
    'RAC-285': ('QBO', 'External'),
    # QBO Doc Review subs
    'RAC-286': ('QBO', 'External'),
    'RAC-287': ('QBO', 'External'),
    # QBO Onboarding subs
    'RAC-288': ('QBO', 'Internal'),  # Routine/onboarding = internal
    'RAC-289': ('QBO', 'Internal'),  # Hypercare routine = internal
    # WFS Env Decision subs
    'RAC-290': ('WFS', 'External'),
    'RAC-291': ('WFS', 'External'),
    # WFS Pre Scoping subs
    'RAC-292': ('WFS', 'External'),
    'RAC-293': ('WFS', 'External'),
    # Standalone
    'RAC-294': ('HockeyStack', 'Internal'),  # Handover = internal
    'RAC-295': ('QBO', 'External'),
    'RAC-296': ('QBO', 'Internal'),  # Playbook = internal improvement
    'RAC-297': ('QBO', 'External'),
    'RAC-298': ('QBO', 'External'),
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


def get_issue_id(identifier):
    """Get issue UUID from identifier like RAC-228."""
    query = '''
    query($filter: IssueFilter!) {
        issues(filter: $filter, first: 1) {
            nodes { id identifier }
        }
    }
    '''
    # Use number filter
    team_key = identifier.split('-')[0]
    number = int(identifier.split('-')[1])
    result = gql(query, {
        'filter': {
            'team': {'key': {'eq': team_key}},
            'number': {'eq': number}
        }
    })
    if result and result['issues']['nodes']:
        return result['issues']['nodes'][0]['id']
    return None


def add_labels(issue_id, label_ids):
    """Add labels to an issue (append, don't replace)."""
    mutation = '''
    mutation($id: String!, $input: IssueUpdateInput!) {
        issueUpdate(id: $id, input: $input) {
            success
        }
    }
    '''
    result = gql(mutation, {
        'id': issue_id,
        'input': {'labelIds': label_ids}
    })
    return result and result.get('issueUpdate', {}).get('success')


def main():
    print('=' * 60)
    print('APPLYING CUSTOMER + EXTERNAL/INTERNAL LABELS')
    print('=' * 60)

    # First, get all issue UUIDs
    print('\n[Phase 1] Resolving issue IDs...')
    id_cache = {}
    for ident in sorted(ISSUE_MAP.keys(), key=lambda x: int(x.split('-')[1])):
        issue_id = get_issue_id(ident)
        if issue_id:
            id_cache[ident] = issue_id
        else:
            print(f'  WARNING: Could not find {ident}')
        time.sleep(0.08)

    print(f'  Resolved {len(id_cache)}/{len(ISSUE_MAP)} issues')

    # Phase 2: For each issue, get existing labels, then add new ones
    print('\n[Phase 2] Applying labels...')

    # First get all current labels for all issues
    query = '''
    query($filter: IssueFilter!) {
        issues(filter: $filter, first: 250) {
            nodes {
                id
                identifier
                labels { nodes { id name } }
            }
        }
    }
    '''
    result = gql(query, {
        'filter': {
            'team': {'key': {'eq': 'RAC'}},
            'number': {'gte': 228, 'lte': 299},
            'assignee': {'email': {'eq': 'alexandra@testbox.com'}}
        }
    })

    if not result:
        # Fallback: query without assignee filter
        result = gql(query, {
            'filter': {
                'team': {'key': {'eq': 'RAC'}},
                'number': {'gte': 228, 'lte': 298}
            }
        })

    current_labels = {}
    if result:
        for node in result['issues']['nodes']:
            ident = node['identifier']
            existing_ids = [l['id'] for l in node['labels']['nodes']]
            current_labels[ident] = existing_ids

    print(f'  Fetched current labels for {len(current_labels)} issues')

    success = 0
    failed = 0
    for ident, (customer, scope) in sorted(ISSUE_MAP.items(), key=lambda x: int(x[0].split('-')[1])):
        if ident not in id_cache:
            continue

        issue_id = id_cache[ident]
        existing = current_labels.get(ident, [])

        # Build new label set: existing + customer + scope
        new_labels = list(existing)
        cust_label = CUSTOMER_LABELS.get(customer)
        scope_label = LABEL_EXTERNAL if scope == 'External' else LABEL_INTERNAL

        if cust_label and cust_label not in new_labels:
            new_labels.append(cust_label)
        if scope_label not in new_labels:
            new_labels.append(scope_label)

        if set(new_labels) == set(existing):
            print(f'  {ident}: already has all labels, skip')
            continue

        print(f'  {ident}: adding {customer} + {scope}...', end=' ')
        ok = add_labels(issue_id, new_labels)
        if ok:
            print('OK')
            success += 1
        else:
            print('FAILED')
            failed += 1
        time.sleep(0.1)

    print(f'\n{"="*60}')
    print(f'LABELS APPLIED: {success} updated, {failed} failed')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
