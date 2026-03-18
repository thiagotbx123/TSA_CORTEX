"""
Step 1: Create new labels and projects for the Gabi/Carlos/Thiago migration.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

LINEAR_API_KEY = os.getenv('LINEAR_API_KEY')
LINEAR_URL = 'https://api.linear.app/graphql'
HEADERS = {
    'Authorization': LINEAR_API_KEY,
    'Content-Type': 'application/json',
}

TEAM_RAC = '5a021b9f-bb1a-49fa-ad3b-83422c46c357'


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


def create_label(name, team_id, color=None, description=None):
    """Create a label and return its ID."""
    mutation = '''
    mutation($input: IssueLabelCreateInput!) {
        issueLabelCreate(input: $input) {
            success
            issueLabel { id name }
        }
    }
    '''
    input_data = {'name': name, 'teamId': team_id}
    if color:
        input_data['color'] = color
    if description:
        input_data['description'] = description

    result = gql(mutation, {'input': input_data})
    if result and result.get('issueLabelCreate', {}).get('success'):
        label = result['issueLabelCreate']['issueLabel']
        print(f"  CREATED label: {label['name']} -> {label['id']}")
        return label['id']
    print(f"  FAILED to create label: {name}")
    return None


def create_project(name, team_ids, description=None, color=None):
    """Create a project and return its ID."""
    mutation = '''
    mutation($input: ProjectCreateInput!) {
        projectCreate(input: $input) {
            success
            project { id name }
        }
    }
    '''
    input_data = {'name': name, 'teamIds': team_ids}
    if description:
        input_data['description'] = description
    if color:
        input_data['color'] = color

    result = gql(mutation, {'input': input_data})
    if result and result.get('projectCreate', {}).get('success'):
        proj = result['projectCreate']['project']
        print(f"  CREATED project: {proj['name']} -> {proj['id']}")
        return proj['id']
    print(f"  FAILED to create project: {name}")
    return None


def main():
    print('=' * 60)
    print('CREATING LABELS AND PROJECTS FOR MIGRATION')
    print('=' * 60)

    results = {'labels': {}, 'projects': {}}

    # ── PHASE 1: Create Labels ──
    print('\n[Phase 1] Creating Labels...')

    # Demand Type label
    print('\n  --- Demand Type ---')
    label_configs = [
        ('Data Gen.', '#8B5CF6', 'Data generation tasks'),
    ]
    for name, color, desc in label_configs:
        lid = create_label(name, TEAM_RAC, color, desc)
        if lid:
            results['labels'][name] = lid
        time.sleep(0.15)

    # Customer labels
    print('\n  --- Customer Labels ---')
    customer_labels = [
        ('Archer',     '#F59E0B'),
        ('Mailchimp',  '#FFE01B'),
        ('Staircase',  '#10B981'),
        ('Gong',       '#8B5CF6'),
        ('Siteimprove','#3B82F6'),
        ('Apollo',     '#EC4899'),
        ('GEM',        '#14B8A6'),
        ('CallRail',   '#F97316'),
        ('Tropic',     '#06B6D4'),
        ('People.ai',  '#6366F1'),
    ]
    for name, color in customer_labels:
        lid = create_label(name, TEAM_RAC, color)
        if lid:
            results['labels'][name] = lid
        time.sleep(0.15)

    # Product labels (Carlos)
    print('\n  --- Product Labels ---')
    product_labels = [
        ('Demo',    '#22C55E'),
        ('Sandbox', '#EAB308'),
    ]
    for name, color in product_labels:
        lid = create_label(name, TEAM_RAC, color)
        if lid:
            results['labels'][name] = lid
        time.sleep(0.15)

    # ── PHASE 2: Create Projects ──
    print('\n[Phase 2] Creating Projects...')

    project_configs = [
        ('[Archer] Implementation',      '#F59E0B'),
        ('[Mailchimp] Implementation',   '#FFE01B'),
        ('[Staircase] Implementation',   '#10B981'),
        ('[Gong] Implementation',        '#8B5CF6'),
        ('[Siteimprove] Implementation', '#3B82F6'),
        ('[Apollo] Implementation',      '#EC4899'),
        ('[GEM] Implementation',         '#14B8A6'),
        ('[Internal] TSA Operations',    '#6B7280'),
        ('[CallRail] Operations',        '#F97316'),
    ]
    for name, color in project_configs:
        pid = create_project(name, [TEAM_RAC], color=color)
        if pid:
            results['projects'][name] = pid
        time.sleep(0.15)

    # ── Save results ──
    output_path = os.path.join(os.path.dirname(__file__), '_infrastructure_ids.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f'\n{"=" * 60}')
    print(f'INFRASTRUCTURE CREATED:')
    print(f'  Labels:   {len(results["labels"])}')
    print(f'  Projects: {len(results["projects"])}')
    print(f'  Saved to: {output_path}')
    print(f'{"=" * 60}')

    # Print for quick reference
    print('\n--- LABEL IDS ---')
    for name, lid in results['labels'].items():
        print(f"  '{name}': '{lid}',")

    print('\n--- PROJECT IDS ---')
    for name, pid in results['projects'].items():
        print(f"  '{name}': '{pid}',")


if __name__ == '__main__':
    main()
