"""Merge Opossum + Raccoons Linear data for Thais & Yasmim into _dashboard_data.json.

Sources:
  - _opossum_raw.json: Cached Opossum team issues (Thais 44 + Yasmim 31)
  - _raccoons_thais.json: Cached Raccoons team issues assigned to Thais (3)
  - Spreadsheet data for other 5 TSA members stays untouched

Data quality notes:
  - Thais: 80% of issues have NO dueDate → excluded from KPI1/KPI3
  - Yasmim: 26% without dueDate → moderate sample
  - Both parents and sub-issues counted (matches spreadsheet methodology)
  - Week assigned from createdAt (spreadsheet uses manually assigned week)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, re
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, '..', '_dashboard_data.json')
OPOSSUM_CACHE = os.path.join(SCRIPT_DIR, '..', '_opossum_raw.json')
RACCOONS_THAIS_CACHE = os.path.join(SCRIPT_DIR, '..', '_raccoons_thais.json')
OUTPUT_PATH = DATA_PATH  # overwrite

# ── Load existing dashboard data ──
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    existing = json.load(f)

# Remove old THAIS/YASMIM records (will be rebuilt from Linear)
existing = [r for r in existing if r['tsa'] not in ('THAIS', 'YASMIM')]
print(f"Existing records (without THAIS/YASMIM): {len(existing)}")

# ── Load Opossum issues from local cache ──
with open(OPOSSUM_CACHE, 'r', encoding='utf-8') as f:
    issues = json.load(f)
print(f"Opossum issues loaded: {len(issues)}")

# ── Load Raccoons issues for Thais (if cache exists) ──
raccoons_thais = []
if os.path.exists(RACCOONS_THAIS_CACHE):
    with open(RACCOONS_THAIS_CACHE, 'r', encoding='utf-8') as f:
        raccoons_thais = json.load(f)
    print(f"Raccoons/Thais issues loaded: {len(raccoons_thais)}")
    # Deduplicate by id (in case any issue appears in both teams)
    seen_ids = {i.get('id') for i in issues}
    for ri in raccoons_thais:
        if ri.get('id') not in seen_ids:
            issues.append(ri)
            seen_ids.add(ri.get('id'))
    print(f"Combined issues after dedup: {len(issues)}")


# ── Helper: compute week string from date ──
def date_to_week(date_str):
    """Convert YYYY-MM-DD to 'YY-MM W.N' format."""
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
    except ValueError:
        return None
    y = dt.year % 100
    m = dt.month
    # Week number within month (1-based, starting from day 1)
    day = dt.day
    wn = (day - 1) // 7 + 1
    return f"{y:02d}-{m:02d} W.{wn}"


def week_range(date_str):
    """Compute week range string like '01/05 - 01/09/2026'."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
    except ValueError:
        return ""
    # Find Monday of that week
    monday = dt - timedelta(days=dt.weekday())
    friday = monday + timedelta(days=4)
    return f"{monday.strftime('%m/%d')} - {friday.strftime('%m/%d/%Y')}"


def extract_customer(title):
    """Extract customer from [brackets] in title."""
    m = re.match(r'\[([^\]]+)\]', title)
    if m:
        cust = m.group(1).strip()
        # Normalize known customers
        cust_map = {
            'Archer': 'Archer', 'GONG': 'Gong', 'Gem': 'Gem',
            'People AI': 'People.ai', 'People.ai': 'People.ai',
            'Gainsight': 'Gainsight', 'Mailchimp': 'Mailchimp',
            'QuickBooks': 'QuickBooks', 'DE Team': 'Internal',
            'SPIKE': None,
        }
        for key, val in cust_map.items():
            if key.lower() in cust.lower():
                return val or ''
        return cust
    return ''


def map_status(linear_status):
    """Map Linear status to spreadsheet status."""
    mapping = {
        'Done': 'Done',
        'In Progress': 'In Progress',
        'In Review': 'In Progress',
        'Todo': 'To do',
        'Backlog': 'To do',
        'Canceled': 'Canceled',
        'Triage': 'To do',
    }
    return mapping.get(linear_status, linear_status)


def calc_perf(status, eta, delivery, date_add):
    """Calculate performance label."""
    if status == 'Canceled':
        return 'N/A'
    if not eta:
        return 'No ETA'
    if status == 'Done':
        if not delivery:
            return 'No Delivery Date'
        try:
            d_eta = datetime.strptime(eta, '%Y-%m-%d')
            d_del = datetime.strptime(delivery[:10], '%Y-%m-%d')
            diff = (d_del - d_eta).days
            if diff <= 7:  # within 1 week tolerance
                return 'On Time'
            else:
                return 'Late'
        except ValueError:
            return 'N/A'
    else:
        # Not done yet — check if overdue
        try:
            d_eta = datetime.strptime(eta, '%Y-%m-%d')
            if d_eta < datetime.now():
                return 'Overdue'
            else:
                return 'On Track'
        except ValueError:
            return 'N/A'


def determine_category(customer, title):
    """Determine Internal vs External."""
    if customer in ('Internal', ''):
        # Check if it's a DE Team or internal task
        if 'DE Team' in title or 'Internal' in title or 'Spike' in title.lower():
            return 'Internal'
        # If has a customer bracket, it's external work
        if re.match(r'\[', title):
            return 'External'
        return 'Internal'
    return 'External'


# ── Convert Opossum issues to dashboard records ──
PERSON_MAP = {
    'Tha\u00eds Linzmaier': 'THAIS',
    'Yasmim Arsego': 'YASMIM',
}

new_records = []
for iss in issues:
    assignee = iss.get('assignee', '')
    tsa = PERSON_MAP.get(assignee)
    if not tsa:
        continue  # skip unassigned or Diego's single issue

    title = iss.get('title', '')
    created = iss.get('createdAt', '')[:10] if iss.get('createdAt') else ''
    due = iss.get('dueDate') or ''
    completed = iss.get('completedAt', '')[:10] if iss.get('completedAt') else ''
    status = map_status(iss.get('status', ''))
    customer = extract_customer(title)
    category = determine_category(customer, title)

    # Use createdAt for week assignment
    week = date_to_week(created)
    wrange = week_range(created)

    perf = calc_perf(status, due, completed, created)

    # Demand type
    if category == 'External' and customer:
        demand = f"External(Customer)"
    else:
        demand = "Internal"

    ticket_id = iss.get('id', '')
    ticket_url = iss.get('url', '')
    # Construct URL from ID if missing
    if ticket_id and not ticket_url:
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
        ticket_url = f"https://linear.app/testbox/issue/{ticket_id}/{slug}"

    record = {
        'tsa': tsa,
        'week': week or '',
        'weekRange': wrange,
        'focus': title,
        'status': status,
        'demandType': demand,
        'category': category,
        'customer': customer if customer != 'Internal' else '',
        'dateAdd': created,
        'eta': due,
        'delivery': completed,
        'perf': perf,
        'ticketId': ticket_id,
        'ticketUrl': ticket_url,
        'source': 'linear',
    }
    new_records.append(record)

print(f"\nNew Opossum records: {len(new_records)}")

# Stats
from collections import Counter
for tsa in ['THAIS', 'YASMIM']:
    recs = [r for r in new_records if r['tsa'] == tsa]
    perfs = Counter(r['perf'] for r in recs)
    print(f"  {tsa}: {len(recs)} records — {dict(perfs)}")

# ── Merge ──
merged = existing + new_records
print(f"\nMerged total: {len(merged)}")

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
print(f"Saved: {OUTPUT_PATH}")
