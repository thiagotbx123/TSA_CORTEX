"""Normalize _dashboard_data.json — ensure all records have consistent fields.

Adds missing fields, fixes data quality issues, recalculates performance labels.
Linear is the standard going forward; spreadsheet data is frozen backlog.

Usage: python kpi/normalize_data.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, re
from datetime import datetime
from collections import Counter

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, '..', '_dashboard_data.json')

# L2: Validate JSON before processing
try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"ERROR: Malformed JSON in {DATA_PATH}: {e}")
    sys.exit(1)

print(f"Loaded: {len(data)} records")

# Required fields with defaults
REQUIRED = {
    'tsa': '', 'week': '', 'weekRange': '', 'focus': '',
    'status': '', 'demandType': '', 'category': '',
    'customer': '', 'dateAdd': '', 'eta': '', 'delivery': '',
    'perf': '', 'ticketId': '', 'ticketUrl': '', 'source': '',
    'milestone': '', 'parentId': '', 'rework': '', 'startedAt': '',
    'deliveryDate': '', 'originalEta': '', 'finalEta': '',
    'reviewerDelay': None, 'etaChanges': 0, 'inReviewDate': '',
}

# M6: Unified customer mapping — Staircase is the correct name (Gabi's reference)
CUSTOMER_MAP = {
    'qbo': 'QuickBooks', 'quickbooks': 'QuickBooks',
    'intuit quickbooks': 'QuickBooks', 'intuit': 'QuickBooks',
    'intuit ies tco/keystone construction': 'QuickBooks',
    'qbo-wfs': 'WFS',
    'gong': 'Gong',
    'gem': 'Gem',
    'mailchimp': 'Mailchimp',
    'people.ai': 'People.ai',
    'siteimprove': 'Siteimprove',
    'brevo': 'Brevo',
    'archer': 'Archer',
    'tropic': 'Tropic',
    'apollo': 'Apollo',
    'callrail': 'CallRail',
    'hockeystack': 'HockeyStack',
    'wfs': 'WFS',
    'staircase': 'Staircase',
    'coda': 'Coda',
    'general': 'General',
    'outreach': 'Outreach',
    'gainsight': 'Staircase',  # M6: Gainsight IS Staircase
    'tbx': 'TBX',
}

# Month maps (Portuguese + English + typos)
MONTH_MAP = {
    'jan': 1, 'jab': 1, 'fev': 2, 'feb': 2, 'mar': 3, 'abr': 4, 'apr': 4,
    'mai': 5, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'aug': 8,
    'set': 9, 'sep': 9, 'out': 10, 'oct': 10, 'nov': 11, 'dez': 12, 'dec': 12,
}

# H15: Unparseable date values to clean
INVALID_DATES = {'tbd', 'n/a', '-', 'na', 'none', ''}

# M8: Blocked By Customer status normalization
BBC_VARIANTS = {'B.B.C.', 'B.B.C', 'BBC', 'bbc', 'b.b.c.', 'b.b.c'}

# Not real clients — Internal contexts
NOT_REAL_CLIENTS = {'Waki', 'TBX', 'Routine', 'General', 'Coda', 'All',
                    'Internal', "Internal \u2013 Sam's Board Meeting"}

# Real clients that must be External
FORCE_EXTERNAL = {'Tabs'}

fixes = {'fields_added': 0, 'urls_constructed': 0, 'source_tagged': 0, 'weeks_fixed': 0}


def infer_year(month, context_date=None):
    """M1: Infer year from month using context date or current date."""
    ref = context_date or datetime.now()
    if month <= ref.month:
        return ref.year
    return ref.year - 1


def calc_perf(status, eta, delivery):
    """D.LIE7: Calculate performance label from current data (legacy fallback)."""
    if status == 'Canceled':
        return 'N/A'
    # D.LIE10: B.B.C. (Blocked By Customer) should not be penalized
    if status == 'B.B.C':
        return 'Blocked'
    if not eta:
        # D.LIE17: Not-started tickets without ETA = N/A (not actionable yet)
        # Only flag "No ETA" for active/completed work
        if status in ('Backlog', 'Todo', 'Triage'):
            return 'Not Started'
        return 'No ETA'
    if status == 'Done':
        if not delivery:
            return 'No Delivery Date'
        try:
            d_eta = datetime.strptime(eta[:10], '%Y-%m-%d')
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
            d_eta = datetime.strptime(eta[:10], '%Y-%m-%d').date()
            if d_eta < datetime.now().date():
                return 'Late'
            else:
                return 'On Track'
        except ValueError:
            return 'N/A'


def calc_perf_with_history(record):
    """Activity-based perf calculation using Linear issue history.

    Uses deliveryDate (first In Review/Done) instead of completedAt,
    and finalEta (current dueDate) for comparison. Falls back to
    legacy calc_perf when history fields are missing.
    """
    status = record.get('status', '')
    final_eta = record.get('originalEta', '') or record.get('finalEta', '') or record.get('eta', '')
    delivery_date = record.get('deliveryDate', '')
    in_review_date = record.get('inReviewDate', '')

    # Preserve special statuses
    if status == 'Canceled':
        return 'N/A'
    if status == 'B.B.C':
        return 'Blocked'
    if not final_eta:
        if status in ('Backlog', 'Todo', 'Triage'):
            return 'Not Started'
        return 'No ETA'

    today = datetime.now().date()

    try:
        d_eta = datetime.strptime(final_eta[:10], '%Y-%m-%d').date()
    except ValueError:
        return 'N/A'

    # Case 1: Has a deliveryDate (first In Review or Done transition)
    if delivery_date:
        try:
            d_del = datetime.strptime(delivery_date[:10], '%Y-%m-%d').date()
            if d_del <= d_eta:
                return 'On Time'
            else:
                return 'Late'
        except ValueError:
            pass

    # Case 2: No deliveryDate, but is In Review — check when it moved there
    if not delivery_date and status == 'In Progress' and in_review_date:
        # status mapped to In Progress but actually In Review in Linear
        pass
    if not delivery_date and in_review_date:
        try:
            d_review = datetime.strptime(in_review_date[:10], '%Y-%m-%d').date()
            if today > d_eta:
                # Past ETA — was the In Review move on time?
                if d_review <= d_eta:
                    return 'On Time'
                else:
                    return 'Late'
            else:
                return 'On Track'
        except ValueError:
            pass

    # Case 3: No deliveryDate AND no In Review — open ticket
    if not delivery_date and not in_review_date:
        if d_eta < today:
            return 'Late'
        else:
            return 'On Track'

    # Fallback to legacy
    return calc_perf(status, final_eta, record.get('delivery', ''))


for r in data:
    # 1. Ensure all required fields exist
    for k, default in REQUIRED.items():
        if k not in r:
            r[k] = default
            fixes['fields_added'] += 1

    # 2. Tag source
    if not r['source']:
        if r.get('ticketId') or r.get('ticketUrl'):
            r['source'] = 'linear'
        else:
            r['source'] = 'spreadsheet'
        fixes['source_tagged'] += 1

    # 3. Construct Linear URL from ticket ID if missing
    if r['ticketId'] and not r['ticketUrl']:
        tid = r['ticketId']
        slug = re.sub(r'[^a-z0-9]+', '-', r.get('focus', '').lower()).strip('-')[:60]
        r['ticketUrl'] = f"https://linear.app/testbox/issue/{tid}/{slug}"
        fixes['urls_constructed'] += 1

    # 4. Fix empty weeks from bad dateAdd
    if not r['week'] and r['dateAdd']:
        m = re.match(r'^(\d{2})-([A-Za-z]+)$', r['dateAdd'])
        if m:
            day = int(m.group(1))
            mon_str = m.group(2).lower()
            if mon_str in MONTH_MAP:
                mon = MONTH_MAP[mon_str]
                yr_full = infer_year(mon)
                yr = yr_full % 100
                wn = (day - 1) // 7 + 1
                r['week'] = f"{yr:02d}-{mon:02d} W.{wn}"
                r['dateAdd'] = f"{yr_full}-{mon:02d}-{day:02d}"
                fixes['weeks_fixed'] += 1

    # 5. Fix 2019 dates → 2025 (Gabi data entry error)
    if r.get('dateAdd', '').startswith('2019-'):
        r['dateAdd'] = '2025-' + r['dateAdd'][5:]
        if r['week'].startswith('19-'):
            r['week'] = '25-' + r['week'][3:]
        fixes.setdefault('year_fixed', 0)
        fixes['year_fixed'] += 1
    for df in ('eta', 'delivery', 'startedAt', 'deliveryDate', 'inReviewDate', 'originalEta', 'finalEta'):
        if r.get(df, '').startswith('2019-'):
            r[df] = '2025-' + r[df][5:]

    # M10: Fix weekRange year 2019→2025
    wr = r.get('weekRange', '')
    if wr and '/2019' in wr:
        r['weekRange'] = wr.replace('/2019', '/2025')
        fixes.setdefault('weekrange_year_fixed', 0)
        fixes['weekrange_year_fixed'] += 1

    # 6. Normalize customer names
    cust = r.get('customer', '').strip()
    if cust:
        cust_lower = cust.lower()
        if cust_lower in CUSTOMER_MAP:
            if r['customer'] != CUSTOMER_MAP[cust_lower]:
                r['customer'] = CUSTOMER_MAP[cust_lower]
                fixes.setdefault('customers_normalized', 0)
                fixes['customers_normalized'] += 1

    # 7. Fix category/demandType misclassifications
    # M5: Customer work = External (incidents, implementation, common work)
    #     Internal = improvements, standardizations, internal stuff
    cust2 = r.get('customer', '')

    # Internal contexts wrongly tagged as External → fix to Internal
    if cust2 in NOT_REAL_CLIENTS and r.get('category') == 'External':
        r['category'] = 'Internal'
        r['demandType'] = 'Internal'
        fixes.setdefault('category_fixed', 0)
        fixes['category_fixed'] += 1

    # Real clients must be External
    if cust2 in FORCE_EXTERNAL and r.get('category') == 'Internal':
        r['category'] = 'External'
        r['demandType'] = 'External(Customer)'
        fixes.setdefault('category_fixed_to_ext', 0)
        fixes['category_fixed_to_ext'] += 1

    # M4: If customer is a real client name but category=Internal, fix to External
    # (Must run BEFORE H13 so the category is correct when demandType is checked)
    if cust2 and cust2 not in NOT_REAL_CLIENTS and r.get('category') == 'Internal':
        r['category'] = 'External'
        fixes.setdefault('client_reclassified_ext', 0)
        fixes['client_reclassified_ext'] += 1

    # H13/H18: External records with a real customer must have proper demandType
    if cust2 and cust2 not in NOT_REAL_CLIENTS and r.get('category') == 'External':
        if r.get('demandType', '') not in ('External(Customer)', 'External(Incident)'):
            r['demandType'] = 'External(Customer)'
            fixes.setdefault('demandtype_fixed', 0)
            fixes['demandtype_fixed'] += 1

    # 8. Clean corrupted ETA/delivery fields (sentences instead of dates)
    for field in ('eta', 'delivery'):
        val = r.get(field, '')
        if val and len(val) > 12 and not re.match(r'^\d{4}-\d{2}-\d{2}', val):
            r[field] = ''
            fixes.setdefault('corrupted_cleaned', 0)
            fixes['corrupted_cleaned'] += 1

    # H15: Clean unparseable date strings (skip already-empty fields)
    for field in ('eta', 'delivery'):
        val = r.get(field, '').strip()
        if val and val.lower() in INVALID_DATES:
            r[field] = ''
            fixes.setdefault('invalid_dates_cleaned', 0)
            fixes['invalid_dates_cleaned'] += 1

    # 9. Fix short date formats like "11-Fev" → "2026-02-11"
    for field in ('eta', 'delivery'):
        val = r.get(field, '').strip()
        if val:
            m2 = re.match(r'^(\d{1,2})-([A-Za-z]{3})$', val)
            if m2:
                day = int(m2.group(1))
                mon_str = m2.group(2).lower()
                if mon_str in MONTH_MAP:
                    mon = MONTH_MAP[mon_str]
                    # M1: Use dateAdd as context for year inference
                    ctx = None
                    da = r.get('dateAdd', '')
                    if da and len(da) >= 10:
                        try:
                            ctx = datetime.strptime(da[:10], '%Y-%m-%d')
                        except ValueError:
                            pass
                    yr = infer_year(mon, ctx)
                    r[field] = f"{yr}-{mon:02d}-{day:02d}"
                    fixes.setdefault('short_dates_fixed', 0)
                    fixes['short_dates_fixed'] += 1

    # 10. Fix delivery < dateAdd when clearly wrong year (2024/2025 typos)
    da = r.get('dateAdd', '')
    dl = r.get('delivery', '')
    if da and dl and len(da) == 10 and len(dl) == 10:
        try:
            d1 = datetime.strptime(da, '%Y-%m-%d')
            d2 = datetime.strptime(dl, '%Y-%m-%d')
            diff_days = (d1 - d2).days
            if 360 <= diff_days <= 370:
                r['delivery'] = f"{d1.year}-{dl[5:]}"
                fixes.setdefault('year_in_delivery_fixed', 0)
                fixes['year_in_delivery_fixed'] += 1
        except ValueError:
            pass

    # M8: Normalize B.B.C. status variants
    if r.get('status', '') in BBC_VARIANTS:
        r['status'] = 'B.B.C'
        fixes.setdefault('bbc_normalized', 0)
        fixes['bbc_normalized'] += 1

    # M3: Canceled tasks should have perf=N/A regardless of previous value
    if r.get('status') == 'Canceled' and r.get('perf') not in ('N/A', ''):
        old_perf = r['perf']
        r['perf'] = 'N/A'
        fixes.setdefault('canceled_perf_fixed', 0)
        fixes['canceled_perf_fixed'] += 1

    # D.LIE14: Update delivery field with activity-based deliveryDate for velocity accuracy
    if r.get('source') == 'linear' and r.get('deliveryDate') and not r.get('delivery'):
        r['delivery'] = r['deliveryDate']
        fixes.setdefault('delivery_from_history', 0)
        fixes['delivery_from_history'] += 1
    # Also update delivery if deliveryDate is earlier (person moved to In Review before Done)
    if r.get('source') == 'linear' and r.get('deliveryDate') and r.get('delivery'):
        if r['deliveryDate'] < r['delivery']:
            r['delivery'] = r['deliveryDate']
            fixes.setdefault('delivery_corrected_to_review', 0)
            fixes['delivery_corrected_to_review'] += 1

    # D.LIE7: Recalculate perf for ALL records to ensure consistency after date fixes
    # Use activity-based history for Linear records; legacy for spreadsheet
    old_perf = r.get('perf', '')

    # D.LIE15: Detect bulk-closed / admin-closed / migrated tickets
    # Pattern 1: No startedAt, no deliveryDate, no inReviewDate → pure admin close
    # Pattern 2: Migrated from spreadsheet (createdAt ≈ dueDate, only 1 status transition)
    #            These tickets were already delivered in the spreadsheet and just closed in Linear
    is_admin_close = False
    if r.get('source') == 'linear' and r.get('status') == 'Done':
        # Pattern 1: never started
        if not r.get('startedAt') and not r.get('deliveryDate') and not r.get('inReviewDate'):
            is_admin_close = True
        # Pattern 2: migrated ticket — createdAt == dueDate (same day) and no In Review step
        # Guard: also require no startedAt to avoid misclassifying tickets that were actually worked on.
        elif (r.get('eta') and r.get('dateAdd')
              and r['eta'][:10] == r['dateAdd'][:10]
              and not r.get('inReviewDate')
              and not r.get('startedAt')
              and r.get('etaChanges', 0) <= 1):
            is_admin_close = True

    if is_admin_close:
        if r.get('eta'):
            new_perf = 'On Time'
        else:
            new_perf = 'N/A'
        fixes.setdefault('admin_close_fixed', 0)
        fixes['admin_close_fixed'] += 1
    elif r.get('source') == 'linear' and (r.get('deliveryDate') or r.get('inReviewDate')):
        new_perf = calc_perf_with_history(r)
    else:
        new_perf = calc_perf(r.get('status', ''), r.get('eta', ''), r.get('delivery', ''))
    if new_perf != old_perf:
        fixes.setdefault('perf_recalculated', 0)
        fixes['perf_recalculated'] += 1
        # Track history-based improvements separately
        if r.get('source') == 'linear' and (r.get('deliveryDate') or r.get('inReviewDate')):
            fixes.setdefault('perf_improved_by_history', 0)
            fixes['perf_improved_by_history'] += 1
        r['perf'] = new_perf

    # A35c: D.LIE20 — If history signals rework but rework label is absent, flag it.
    # reassignedInReview is stored in the record; reworkDetected is not persisted but
    # merge already sets rework='yes' from it. This is a safety net for stale/partial records.
    if r.get('source') == 'linear' and r.get('status') == 'Done':
        if r.get('reassignedInReview') and not r.get('rework'):
            r['rework'] = 'yes'
            fixes.setdefault('rework_flagged_from_history', 0)
            fixes['rework_flagged_from_history'] += 1

# D.LIE22: Remove spreadsheet records that have a Linear equivalent
# Linear is the source of truth — if a ticket exists in Linear for the same task, drop the spreadsheet version
linear_focuses = set()
for r in data:
    if r.get('source') == 'linear' and r.get('focus'):
        # Normalize: lowercase, strip brackets, first 60 chars
        norm = re.sub(r'^\[.*?\]\s*', '', r['focus']).strip().lower()[:60]
        linear_focuses.add((r.get('tsa', ''), norm))

before_dedup = len(data)
deduped = []
sheet_replaced = 0
for r in data:
    if r.get('source') == 'spreadsheet' and r.get('focus'):
        norm = r['focus'].strip().lower()[:60]
        if (r.get('tsa', ''), norm) in linear_focuses:
            sheet_replaced += 1
            continue  # Linear has this — drop the spreadsheet version
    deduped.append(r)
data = deduped
if sheet_replaced:
    fixes['sheet_replaced_by_linear'] = sheet_replaced
    print(f"  D.LIE22: {sheet_replaced} spreadsheet records replaced by Linear equivalents")

# M9: Detect duplicates (alert, don't auto-remove)
seen = {}
dup_groups = []
for i, r in enumerate(data):
    key = (r.get('tsa', ''), r.get('focus', ''), r.get('dateAdd', ''))
    if key in seen and key[1]:  # skip empty focus
        dup_groups.append((i, seen[key], key))
    else:
        seen[key] = i

print(f"\nFixes applied:")
for k, v in fixes.items():
    print(f"  {k}: {v}")

# Validation
print(f"\nValidation:")
no_week = [r for r in data if not r['week']]
no_focus = [r for r in data if not r['focus']]
no_ticket = [r for r in data if not r['ticketUrl']]
ext_no_cust = [r for r in data if r.get('category') == 'External' and not r.get('customer')]
by_source = Counter(r['source'] for r in data)
by_perf = Counter(r['perf'] for r in data)

print(f"  Records without week: {len(no_week)}")
print(f"  Records without focus: {len(no_focus)}")
print(f"  Records without ticket URL: {len(no_ticket)}")
print(f"  External without customer: {len(ext_no_cust)}")  # H13
print(f"  By source: {dict(by_source)}")
print(f"  By perf: {dict(by_perf)}")

if no_week:
    print(f"\n  Still missing week:")
    for r in no_week:
        print(f"    {r['tsa']} | {r['focus'][:50]} | dateAdd={r['dateAdd']}")

if ext_no_cust:
    print(f"\n  External without customer (H13):")
    for r in ext_no_cust[:10]:
        print(f"    {r['tsa']} | {r['focus'][:50]} | status={r['status']}")

if dup_groups:
    print(f"\n  Potential duplicates detected: {len(dup_groups)} pairs")
    for idx, orig_idx, key in dup_groups[:5]:
        print(f"    [{idx}] = [{orig_idx}] | {key[0]} | {key[1][:40]} | {key[2]}")

# History impact summary
history_improved = fixes.get('perf_improved_by_history', 0)
linear_with_history = [r for r in data if r.get('source') == 'linear' and (r.get('deliveryDate') or r.get('inReviewDate'))]
print(f"\n  Activity-based history analysis:")
print(f"    Linear records with history data: {len(linear_with_history)}")
print(f"    {history_improved} issues improved by history analysis")

# C3: Atomic write
tmp_path = DATA_PATH + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
os.replace(tmp_path, DATA_PATH)
print(f"\nSaved: {DATA_PATH}")
