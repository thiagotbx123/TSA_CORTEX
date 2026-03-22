"""Refresh Linear cache files with LIVE data from Linear API.

Replaces _opossum_raw.json and _raccoons_thais.json with fresh data.
Must be run before merge_opossum_data.py to ensure KPI data is current.

Usage: python kpi/refresh_linear_cache.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, requests, shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(__file__)
ROOT = os.path.join(SCRIPT_DIR, '..')
ENV_PATH = os.path.join(ROOT, '..', '.env')

# Load API key
api_key = None
for env_file in [ENV_PATH, os.path.join(ROOT, '.env')]:
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip().startswith('LINEAR_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    break
    if api_key:
        break

if not api_key:
    print("ERROR: LINEAR_API_KEY not found in .env")
    sys.exit(1)

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': api_key,
}
API_URL = 'https://api.linear.app/graphql'
HTTP_TIMEOUT = 30  # H11: timeout to prevent hanging

# Team IDs
OPOSSUM_TEAM_ID = 'b3fb1317-885c-47a0-b87d-85a77252d994'
RACCOONS_TEAM_ID = '5a021b9f-bb1a-49fa-ad3b-83422c46c357'

# Person IDs (Thais and Yasmim)
THAIS_ID = '0879df15-56d6-477f-944d-df033121641a'
YASMIM_ID = 'df4a6bcf-c519-469d-bb40-b1a0e93d0041'

QUERY = """
query($teamId: ID!, $cursor: String) {
  issues(
    filter: { team: { id: { eq: $teamId } } }
    first: 100
    after: $cursor
    orderBy: createdAt
  ) {
    pageInfo { hasNextPage endCursor }
    nodes {
      identifier
      title
      description
      url
      branchName
      createdAt
      updatedAt
      archivedAt
      completedAt
      dueDate
      startedAt
      slaStartedAt
      slaMediumRiskAt
      slaHighRiskAt
      slaBreachesAt
      slaType
      state { name }
      labels { nodes { name } }
      creator { name id }
      assignee { name id }
      project { name id }
      projectMilestone { name id }
      parent { identifier }
      team { name id key }
      estimate
    }
  }
}
"""


def atomic_write_json(path, data):
    """C3: Write JSON atomically — write to .tmp then os.replace."""
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)


def fetch_team_issues(team_id, team_name):
    """Fetch all issues for a team with pagination.
    C2: Returns (issues, complete) tuple — complete=False if pagination broke mid-way."""
    all_issues = []
    cursor = None
    page = 0
    pagination_complete = False

    while True:
        page += 1
        variables = {'teamId': team_id}
        if cursor:
            variables['cursor'] = cursor

        try:
            resp = requests.post(API_URL, headers=HEADERS,
                                 json={'query': QUERY, 'variables': variables},
                                 timeout=HTTP_TIMEOUT)
        except requests.exceptions.Timeout:
            print(f"  ERROR: Request timed out on page {page}")
            break
        except requests.exceptions.ConnectionError as e:
            print(f"  ERROR: Connection failed on page {page}: {e}")
            break

        if resp.status_code != 200:
            print(f"  ERROR: API returned {resp.status_code}: {resp.text[:200]}")
            break

        data = resp.json()
        if 'errors' in data:
            print(f"  ERROR: {data['errors'][0].get('message', '')}")
            break

        issues_data = data['data']['issues']
        nodes = issues_data['nodes']
        print(f"  Page {page}: {len(nodes)} issues")

        for node in nodes:
            estimate = node.get('estimate')
            pm = node.get('projectMilestone')
            project = node.get('project')
            parent = node.get('parent')
            labels_raw = node.get('labels', {}).get('nodes', [])
            desc_raw = (node.get('description') or '')
            desc = desc_raw[:500] + ('...' if len(desc_raw) > 500 else '')  # L1: truncation indicator

            issue = {
                'id': node['identifier'],
                'title': node.get('title', ''),
                'description': desc,
                'projectMilestone': {'id': pm['id'], 'name': pm['name']} if pm else None,
                'estimate': {'value': estimate, 'name': f"{estimate} Points"} if estimate else None,
                'url': node.get('url', ''),
                'gitBranchName': node.get('branchName', ''),
                'createdAt': node.get('createdAt', ''),
                'updatedAt': node.get('updatedAt', ''),
                'archivedAt': node.get('archivedAt'),
                'completedAt': node.get('completedAt'),
                'dueDate': node.get('dueDate'),
                'startedAt': node.get('startedAt'),
                'slaStartedAt': node.get('slaStartedAt'),
                'slaMediumRiskAt': node.get('slaMediumRiskAt'),
                'slaHighRiskAt': node.get('slaHighRiskAt'),
                'slaBreachesAt': node.get('slaBreachesAt'),
                'slaType': node.get('slaType', ''),
                'status': node.get('state', {}).get('name', ''),
                'labels': [l['name'] for l in labels_raw],
                'createdBy': node.get('creator', {}).get('name', '') if node.get('creator') else '',
                'createdById': node.get('creator', {}).get('id', '') if node.get('creator') else '',
                'assignee': node.get('assignee', {}).get('name', '') if node.get('assignee') else '',
                'assigneeId': node.get('assignee', {}).get('id', '') if node.get('assignee') else '',
                'project': project['name'] if project else '',
                'projectId': project['id'] if project else '',
                'parentId': parent['identifier'] if parent else None,
                'team': node.get('team', {}).get('name', '') if node.get('team') else '',
                'teamId': node.get('team', {}).get('id', '') if node.get('team') else '',
            }
            all_issues.append(issue)

        if not issues_data['pageInfo']['hasNextPage']:
            pagination_complete = True  # C2: only mark complete if we reached the end
            break
        cursor = issues_data['pageInfo']['endCursor']

    return all_issues, pagination_complete


def fetch_raccoons_thais(raccoons_issues):
    """Filter Raccoons issues assigned to Thais."""
    return [i for i in raccoons_issues if i.get('assigneeId') == THAIS_ID]


print(f"=== Linear Cache Refresh — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

# Fetch Opossum team
print("Fetching Opossum team...")
opossum_issues, opossum_complete = fetch_team_issues(OPOSSUM_TEAM_ID, 'Opossum')
print(f"  Total Opossum issues: {len(opossum_issues)} (complete: {opossum_complete})")

# Filter by Thais/Yasmim
thais_opo = [i for i in opossum_issues if i.get('assigneeId') == THAIS_ID]
yasmim_opo = [i for i in opossum_issues if i.get('assigneeId') == YASMIM_ID]
print(f"  Thais: {len(thais_opo)} | Yasmim: {len(yasmim_opo)}")

# Check dueDate coverage
thais_with_due = sum(1 for i in thais_opo if i.get('dueDate'))
yasmim_with_due = sum(1 for i in yasmim_opo if i.get('dueDate'))
print(f"  Thais dueDate: {thais_with_due}/{len(thais_opo)} ({100*thais_with_due//max(len(thais_opo),1)}%)")
print(f"  Yasmim dueDate: {yasmim_with_due}/{len(yasmim_opo)} ({100*yasmim_with_due//max(len(yasmim_opo),1)}%)")

# Save Opossum cache — C2: only save if pagination completed fully
opossum_path = os.path.join(ROOT, '_opossum_raw.json')
if len(opossum_issues) == 0:
    print(f"  SKIPPED save — 0 issues fetched, keeping existing cache")
elif not opossum_complete:
    print(f"  SKIPPED save — pagination incomplete ({len(opossum_issues)} partial issues), keeping existing cache")
else:
    atomic_write_json(opossum_path, opossum_issues)
    print(f"  Saved: {opossum_path}")

# Fetch Raccoons team
print("\nFetching Raccoons team...")
raccoons_issues, raccoons_complete = fetch_team_issues(RACCOONS_TEAM_ID, 'Raccoons')
print(f"  Total Raccoons issues: {len(raccoons_issues)} (complete: {raccoons_complete})")

# Filter Thais from Raccoons
raccoons_thais = fetch_raccoons_thais(raccoons_issues)
print(f"  Raccoons/Thais: {len(raccoons_thais)}")

# Save Raccoons/Thais cache — H8: check raccoons_thais count (not raccoons_issues)
raccoons_path = os.path.join(ROOT, '_raccoons_thais.json')
if len(raccoons_thais) == 0:
    print(f"  SKIPPED save — 0 Thais issues found, keeping existing cache")
elif not raccoons_complete:
    print(f"  SKIPPED save — pagination incomplete, keeping existing cache")
else:
    atomic_write_json(raccoons_path, raccoons_thais)
    print(f"  Saved: {raccoons_path}")

# Summary
print(f"\n=== Refresh complete ===")
print(f"  Opossum: {len(opossum_issues)} issues ({len(thais_opo)} Thais + {len(yasmim_opo)} Yasmim) — {'COMPLETE' if opossum_complete else 'PARTIAL'}")
print(f"  Raccoons/Thais: {len(raccoons_thais)} issues — {'COMPLETE' if raccoons_complete else 'PARTIAL'}")
print(f"  Thais ETA coverage: {thais_with_due}/{len(thais_opo)}")
print(f"  Yasmim ETA coverage: {yasmim_with_due}/{len(yasmim_opo)}")
print(f"\nNext: run 'python kpi/merge_opossum_data.py' then 'python kpi/build_html_dashboard.py'")
