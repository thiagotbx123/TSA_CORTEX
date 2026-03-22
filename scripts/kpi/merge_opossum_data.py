"""Merge Opossum + Raccoons Linear data for Thais & Yasmim into _dashboard_data.json.

Sources:
  - _opossum_raw.json: Cached Opossum team issues (Thais + Yasmim)
  - _raccoons_thais.json: Cached Raccoons team issues assigned to Thais
  - Spreadsheet data for other TSA members stays untouched (frozen backlog)

Usage: python kpi/merge_opossum_data.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, re
from datetime import datetime, timedelta
from collections import Counter

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, '..', '_dashboard_data.json')
OPOSSUM_CACHE = os.path.join(SCRIPT_DIR, '..', '_opossum_raw.json')
RACCOONS_THAIS_CACHE = os.path.join(SCRIPT_DIR, '..', '_raccoons_thais.json')
OUTPUT_PATH = DATA_PATH


# ── Load existing dashboard data ──
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    existing = json.load(f)

# H6: Count existing records before deleting
old_thais = len([r for r in existing if r.get('tsa') == 'THAIS'])
old_yasmim = len([r for r in existing if r.get('tsa') == 'YASMIM'])

# Remove old THAIS/YASMIM records (will be rebuilt from Linear)
existing = [r for r in existing if r.get('tsa') not in ('THAIS', 'YASMIM')]
print(f"Existing records (without THAIS/YASMIM): {len(existing)}")
print(f"  Removed: THAIS={old_thais}, YASMIM={old_yasmim}")

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
    monday = dt - timedelta(days=dt.weekday())
    friday = monday + timedelta(days=4)
    return f"{monday.strftime('%m/%d')} - {friday.strftime('%m/%d/%Y')}"


def extract_customer(title):
    """Extract customer from [brackets] in title."""
    m = re.match(r'\[([^\]]+)\]', title)
    if m:
        cust = m.group(1).strip()
        # L3: Use exact match (==) instead of substring (in) to avoid false positives
        cust_map = {
            'archer': 'Archer', 'gong': 'Gong', 'gem': 'Gem',
            'people ai': 'People.ai', 'people.ai': 'People.ai',
            'gainsight': 'Staircase',  # M6: unified to Staircase
            'staircase': 'Staircase',
            'mailchimp': 'Mailchimp',
            'quickbooks': 'QuickBooks', 'qbo': 'QuickBooks',
            'de team': 'Internal',
            'spike': None,
        }
        cust_lower = cust.lower().strip()
        if cust_lower in cust_map:
            return cust_map[cust_lower] or ''
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


def calc_perf(status, eta, delivery):
    """Calculate performance label.
    L5: Removed unused date_add parameter."""
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
            if diff <= 0:
                return 'On Time'
            else:
                return 'Late'
        except ValueError:
            return 'N/A'
    else:
        try:
            d_eta = datetime.strptime(eta, '%Y-%m-%d').date()
            if d_eta < datetime.now().date():
                return 'Overdue'
            else:
                return 'On Track'
        except ValueError:
            return 'N/A'


def determine_category(customer, title):
    """Determine Internal vs External.
    M4/M5: If it has a real customer name, it's External.
    Internal = improvements, standardizations, internal stuff."""
    if customer in ('Internal', ''):
        if 'DE Team' in title or 'Internal' in title or 'Spike' in title.lower():
            return 'Internal'
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
        continue

    title = iss.get('title', '')
    created = iss.get('createdAt', '')[:10] if iss.get('createdAt') else ''
    due = iss.get('dueDate') or ''
    completed = iss.get('completedAt', '')[:10] if iss.get('completedAt') else ''
    started_at = iss.get('startedAt', '')[:10] if iss.get('startedAt') else ''
    status = map_status(iss.get('status', ''))
    customer = extract_customer(title)
    category = determine_category(customer, title)

    # D.LIE6: Use startedAt for week assignment when available (more accurate)
    # Falls back to createdAt if startedAt is not set
    week_date = started_at if started_at else created
    week = date_to_week(week_date)
    wrange = week_range(week_date)

    perf = calc_perf(status, due, completed)

    # M5: Customer work = External regardless of type
    if category == 'External' and customer:
        demand = "External(Customer)"
    else:
        demand = "Internal"

    ticket_id = iss.get('id', '')
    ticket_url = iss.get('url', '')
    parent_id = iss.get('parentId', '') or ''
    pm = iss.get('projectMilestone')
    milestone = pm.get('name', '') if pm else ''

    # Detect rework label
    raw_labels = iss.get('labels', [])
    label_names = [l.lower() if isinstance(l, str) else (l.get('name', '').lower() if isinstance(l, dict) else '') for l in raw_labels]
    has_rework = 'yes' if 'rework:implementation' in label_names else ''

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
        'milestone': milestone,
        'parentId': parent_id,
        'rework': has_rework,
        'startedAt': started_at,
    }
    new_records.append(record)

print(f"\nNew Linear records: {len(new_records)}")

# H6: Validate count before merging — warn if replacement set is significantly smaller
new_thais = len([r for r in new_records if r['tsa'] == 'THAIS'])
new_yasmim = len([r for r in new_records if r['tsa'] == 'YASMIM'])
print(f"  THAIS: {old_thais} → {new_thais}")
print(f"  YASMIM: {old_yasmim} → {new_yasmim}")

if old_thais > 0 and new_thais < old_thais * 0.5:
    print(f"  WARNING: THAIS record count dropped >50% ({old_thais}→{new_thais}). Check data source.")
if old_yasmim > 0 and new_yasmim < old_yasmim * 0.5:
    print(f"  WARNING: YASMIM record count dropped >50% ({old_yasmim}→{new_yasmim}). Check data source.")

# Stats
for tsa in ['THAIS', 'YASMIM']:
    recs = [r for r in new_records if r['tsa'] == tsa]
    perfs = Counter(r['perf'] for r in recs)
    print(f"  {tsa}: {len(recs)} records — {dict(perfs)}")

# ── Merge ──
merged = existing + new_records
print(f"\nMerged total: {len(merged)}")

# C3: Atomic write
tmp_path = OUTPUT_PATH + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
os.replace(tmp_path, OUTPUT_PATH)
print(f"Saved: {OUTPUT_PATH}")
