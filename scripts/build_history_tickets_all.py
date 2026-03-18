"""
Create historical reference tickets for Gabrielle, Carlos, and Thiago.
Preserves original dates and KPI data since Linear migration dates ≠ original dates.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import json
import time
import re
import requests
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

LINEAR_API_KEY = os.getenv('LINEAR_API_KEY')
LINEAR_URL = 'https://api.linear.app/graphql'
HEADERS = {
    'Authorization': LINEAR_API_KEY,
    'Content-Type': 'application/json',
}

TEAM_RAC = '5a021b9f-bb1a-49fa-ad3b-83422c46c357'
STATUS_DONE = '6e10418c-81fe-467d-aed3-d4c75577d16e'
LABEL_INTERNAL = 'd0706bf9-db94-4079-a4e1-7541515864de'

PERSON_IDS = {
    'gabi':   'd9745bdb-7138-4345-9303-516aa6e4ec39',
    'carlos': 'b13ca864-e0f4-4ff6-b020-ec3f4491643e',
    'thiago': 'a6063009-d822-49f1-a638-6cebfe59e89e',
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


def create_issue(title, description, assignee_id):
    mutation = '''
    mutation CreateIssue($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue { id identifier url }
        }
    }
    '''
    input_data = {
        'title': title,
        'teamId': TEAM_RAC,
        'assigneeId': assignee_id,
        'stateId': STATUS_DONE,
        'labelIds': [LABEL_INTERNAL],
        'description': description,
    }
    result = gql(mutation, {'input': input_data})
    if result and result.get('issueCreate', {}).get('success'):
        return result['issueCreate']['issue']
    return None


def parse_date(raw):
    """Try to parse various date formats into YYYY-MM-DD string."""
    if not raw or raw.strip() in ('', '-', 'TBD', 'N/A'):
        return None
    raw = raw.strip()

    # Already ISO format: 2026-01-15 or 2025-12-08
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', raw)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # MM/DD/YYYY format: 01/12/2026 or 12/17/2025
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})', raw)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"

    # D-Mon format: 5-Dec, 12-Dec, 10-12
    m = re.match(r'^(\d{1,2})-(\w+)$', raw)
    if m:
        day = int(m.group(1))
        mon_str = m.group(2)
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
            'jab': 1,  # typo in data (26-Jab)
        }
        if mon_str.lower() in month_map:
            month = month_map[mon_str.lower()]
            year = 2026 if month >= 1 else 2025
            if month == 12:
                year = 2025
            return f"{year}-{month:02d}-{day:02d}"
        # Could be DD-MM format like 10-12
        try:
            day_num = int(m.group(1))
            mon_num = int(m.group(2))
            if 1 <= mon_num <= 12:
                year = 2025 if mon_num == 12 else 2026
                return f"{year}-{mon_num:02d}-{day_num:02d}"
        except ValueError:
            pass

    # D-Mon with year hint in context
    m = re.match(r'^(\d{1,2})-(\w{3})', raw)
    if m:
        day = int(m.group(1))
        mon_str = m.group(2).lower()
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        }
        if mon_str in month_map:
            month = month_map[mon_str]
            year = 2025 if month == 12 else 2026
            return f"{year}-{month:02d}-{day:02d}"

    return None


def map_status_str(raw):
    s = raw.strip().lower()
    if 'done' in s: return 'Done'
    if 'in progress' in s: return 'In Progress'
    if 'canceled' in s: return 'Canceled'
    if 'b.b.c' in s or 'on hold' in s: return 'Paused'
    if 'to do' in s: return 'Todo'
    return 'Backlog'


def get_customer_display(task, person):
    """Get the display customer name."""
    if person == 'gabi':
        # Gabi's customer is in priority field
        cust = task.get('customer', '').strip()
        prio = task.get('priority', '').strip()
        if cust.lower() in ('mailchimp',): return 'Mailchimp'
        if cust.lower() in ('staircase',): return 'Staircase'
        if prio.lower() in ('mailchimp',): return 'Mailchimp'
        if prio.lower() in ('archer',): return 'Archer'
        if prio.lower() in ('staircase',): return 'Staircase'
        if 'abandon' in task.get('focus', '').lower(): return 'Mailchimp'
        return 'Unknown'
    else:
        return task.get('customer', '').strip() or 'Unknown'


def build_history_body(person_name, person_key, tasks, issue_map):
    """Build the markdown body for a historical reference ticket."""
    lines = []

    # Header
    lines.append(f'# TSA Historical Data — {person_name}')
    lines.append('')
    lines.append(f'> **Purpose:** This ticket preserves the original dates and KPI-critical fields from the TSA Tasks Consolidate spreadsheet (Dec 2025 - Mar 2026). Linear migration happened on 2026-03-18, so `createdAt` and `completedAt` on migrated issues reflect the migration date, NOT original dates. Use THIS ticket as the authoritative source for historical KPI calculations.')
    lines.append('')
    lines.append('---')
    lines.append('')

    # Calculate KPIs
    status_counts = Counter(map_status_str(t['status']) for t in tasks)
    total = len(tasks)

    # Date-based KPIs
    on_time = 0
    late = 0
    total_deliverable = 0
    total_delta = 0
    within_1_week = 0
    durations = []

    for t in tasks:
        eta_str = parse_date(t.get('eta', ''))
        del_str = parse_date(t.get('delivery_date', ''))
        add_str = parse_date(t.get('date_add', ''))

        if eta_str and del_str:
            try:
                eta_d = datetime.strptime(eta_str, '%Y-%m-%d')
                del_d = datetime.strptime(del_str, '%Y-%m-%d')
                d = (del_d - eta_d).days
                total_deliverable += 1
                total_delta += abs(d)
                if d <= 0:
                    on_time += 1
                else:
                    late += 1
                if abs(d) <= 7:
                    within_1_week += 1
            except:
                pass

        if add_str and del_str:
            try:
                add_d = datetime.strptime(add_str, '%Y-%m-%d')
                del_d = datetime.strptime(del_str, '%Y-%m-%d')
                dur = (del_d - add_d).days
                if dur >= 0:
                    durations.append(dur)
            except:
                pass

    # Find date range
    all_dates = []
    for t in tasks:
        d = parse_date(t.get('date_add', ''))
        if d:
            all_dates.append(d)
    date_range = f"{min(all_dates)} — 2026-03-18" if all_dates else "Dec 2025 — Mar 2026"

    lines.append(f'## KPI Snapshot ({date_range})')
    lines.append('')
    lines.append('| Metric | Value |')
    lines.append('|--------|-------|')
    lines.append(f'| Total tasks | {total} |')
    lines.append(f'| Done | {status_counts.get("Done", 0)} |')
    lines.append(f'| In Progress | {status_counts.get("In Progress", 0)} |')
    lines.append(f'| Todo | {status_counts.get("Todo", 0)} |')
    lines.append(f'| Canceled | {status_counts.get("Canceled", 0)} |')
    lines.append(f'| Paused (BBC/On Hold) | {status_counts.get("Paused", 0)} |')
    lines.append(f'| Backlog | {status_counts.get("Backlog", 0)} |')
    lines.append(f'| Tasks with ETA+Delivery | {total_deliverable} |')

    if total_deliverable > 0:
        lines.append(f'| **On-time rate** | **{100*on_time/total_deliverable:.1f}%** ({on_time}/{total_deliverable}) |')
        lines.append(f'| Late deliveries | {late} |')
        lines.append(f'| Avg absolute delta | {total_delta/total_deliverable:.1f} days |')
        lines.append(f'| **Within 1 week (Waki target >90%)** | **{100*within_1_week/total_deliverable:.1f}%** ({within_1_week}/{total_deliverable}) |')

    if durations:
        lines.append(f'| Avg duration (Date Add → Delivery) | {sum(durations)/len(durations):.1f} days |')
        lines.append(f'| Median duration | {sorted(durations)[len(durations)//2]} days |')
        lines.append(f'| Max duration | {max(durations)} days |')

    if total_deliverable > 0:
        lines.append('')
        lines.append('### Waki KPI Assessment')
        lines.append('')
        lines.append(f'1. **ETA Accuracy (<1 week, >90%):** {100*within_1_week/total_deliverable:.1f}% of delivered tasks within 1 week of ETA')
        if durations:
            lines.append(f'2. **Faster Implementations (4-week target):** Avg {sum(durations)/len(durations):.1f} days, median {sorted(durations)[len(durations)//2]} days')
        lines.append(f'3. **Implementation Reliability (90%):** {100*on_time/total_deliverable:.1f}% on-time delivery rate')

    lines.append('')
    lines.append('---')
    lines.append('')

    # Customer breakdown
    lines.append('## Customer Breakdown')
    lines.append('')
    cust_counter = Counter(get_customer_display(t, person_key) for t in tasks)
    for c, n in cust_counter.most_common():
        done = sum(1 for t in tasks if get_customer_display(t, person_key) == c and map_status_str(t['status']) == 'Done')
        lines.append(f'- **{c}**: {n} tasks ({done} done)')

    lines.append('')
    lines.append('## Demand Type Breakdown')
    lines.append('')
    dt_counter = Counter(t.get('demand_type', 'Unknown').strip() for t in tasks)
    for d, n in dt_counter.most_common():
        lines.append(f'- **{d}**: {n}')

    lines.append('')
    lines.append('---')
    lines.append('')

    # Full historical record
    lines.append('## Full Historical Record')
    lines.append('')
    lines.append('| # | Linear | Customer | Focus | Status | Date Add | ETA | Delivery | Delta |')
    lines.append('|---|--------|----------|-------|--------|----------|-----|----------|-------|')

    for t in tasks:
        row = t['row']
        linear_id = ''
        if issue_map and str(row) in issue_map:
            linear_id = issue_map[str(row)].get('identifier', '')

        customer = get_customer_display(t, person_key)
        focus = t.get('focus', '')[:40]
        status = map_status_str(t['status'])
        date_add = parse_date(t.get('date_add', '')) or t.get('date_add', '')
        eta = parse_date(t.get('eta', '')) or t.get('eta', '')
        delivery = parse_date(t.get('delivery_date', '')) or '-'

        delta = ''
        eta_parsed = parse_date(t.get('eta', ''))
        del_parsed = parse_date(t.get('delivery_date', ''))
        if eta_parsed and del_parsed:
            try:
                eta_d = datetime.strptime(eta_parsed, '%Y-%m-%d')
                del_d = datetime.strptime(del_parsed, '%Y-%m-%d')
                delta = str((del_d - eta_d).days)
            except:
                pass

        lines.append(f'| {row} | {linear_id} | {customer} | {focus} | {status} | {date_add} | {eta} | {delivery} | {delta} |')

    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append(f'*Generated by TSA_CORTEX migration script on 2026-03-18. Source: TSA_Tasks_Consolidate spreadsheet, {person_key.upper()} tab.*')

    return '\n'.join(lines)


def main():
    # Load migration data
    data_path = os.path.join(os.path.dirname(__file__), '_migration_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    # Load issue maps
    maps = {}
    for key in ('gabi', 'carlos', 'thiago'):
        map_path = os.path.join(os.path.dirname(__file__), f'_{key}_issue_map.json')
        if os.path.exists(map_path):
            with open(map_path, 'r', encoding='utf-8') as f:
                maps[key] = json.load(f)
        else:
            maps[key] = {}

    persons = [
        ('Gabrielle Caputo', 'gabi', all_data['gabi']),
        ('Carlos Pereira', 'carlos', all_data['carlos']),
        ('Thiago Brito', 'thiago', all_data['thiago']),
    ]

    print('=' * 60)
    print('CREATING HISTORICAL REFERENCE TICKETS')
    print('=' * 60)

    for person_name, person_key, tasks in persons:
        print(f'\n--- {person_name} ({len(tasks)} tasks) ---')

        body = build_history_body(person_name, person_key, tasks, maps.get(person_key, {}))

        # Check size
        print(f'  Body length: {len(body)} chars')
        if len(body) > 100000:
            print(f'  WARNING: Body exceeds 100K chars, truncating historical record')
            # Truncate the full record table if too large
            body = body[:99000] + '\n\n*[Truncated due to size limits]*'

        title = f'[HISTORY] TSA Historical Data — {person_name} (Dec 2025 - Mar 2026)'
        issue = create_issue(title, body, PERSON_IDS[person_key])

        if issue:
            print(f'  CREATED: {issue["identifier"]} - {title}')
            print(f'  URL: {issue["url"]}')
        else:
            print(f'  FAILED: {title}')

        # Save body to file for reference
        body_path = os.path.join(os.path.dirname(__file__), f'_history_ticket_{person_key}.md')
        with open(body_path, 'w', encoding='utf-8') as f:
            f.write(body)
        print(f'  Body saved to: {body_path}')

        time.sleep(0.15)

    print(f'\n{"=" * 60}')
    print('HISTORICAL TICKETS COMPLETE')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
