"""Normalize _dashboard_data.json — ensure all records have consistent fields.

Adds missing fields (ticketId, ticketUrl, source) to spreadsheet-sourced records.
Constructs Linear URLs from ticket IDs when URL is missing.
Fixes data quality issues (empty weeks, malformed dates).

Usage: python kpi/normalize_data.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, re

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, '..', '_dashboard_data.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded: {len(data)} records")

# Required fields with defaults
REQUIRED = {
    'tsa': '', 'week': '', 'weekRange': '', 'focus': '',
    'status': '', 'demandType': '', 'category': '',
    'customer': '', 'dateAdd': '', 'eta': '', 'delivery': '',
    'perf': '', 'ticketId': '', 'ticketUrl': '', 'source': '',
}

fixes = {'fields_added': 0, 'urls_constructed': 0, 'source_tagged': 0, 'weeks_fixed': 0}

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
        # Try to parse malformed dates like "26-Jab"
        m = re.match(r'^(\d{2})-([A-Za-z]+)$', r['dateAdd'])
        if m:
            day = int(m.group(1))
            mon_map = {'jan': 1, 'jab': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5,
                       'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
            mon_str = m.group(2).lower()
            if mon_str in mon_map:
                mon = mon_map[mon_str]
                yr = 25 if mon == 12 else 26
                wn = (day - 1) // 7 + 1
                r['week'] = f"{yr:02d}-{mon:02d} W.{wn}"
                r['dateAdd'] = f"20{yr}-{mon:02d}-{day:02d}"
                fixes['weeks_fixed'] += 1

    # 5. Fix 2019 dates → 2025 (Gabi data entry error)
    if r.get('dateAdd', '').startswith('2019-'):
        r['dateAdd'] = '2025-' + r['dateAdd'][5:]
        if r['week'].startswith('19-'):
            r['week'] = '25-' + r['week'][3:]
        fixes.setdefault('year_fixed', 0)
        fixes['year_fixed'] += 1
    if r.get('eta', '').startswith('2019-'):
        r['eta'] = '2025-' + r['eta'][5:]
    if r.get('delivery', '').startswith('2019-'):
        r['delivery'] = '2025-' + r['delivery'][5:]

    # 6. Clean corrupted ETA/delivery fields (sentences instead of dates)
    for field in ('eta', 'delivery'):
        val = r.get(field, '')
        if val and len(val) > 12 and not re.match(r'^\d{4}-\d{2}-\d{2}', val):
            r[field] = ''
            r['perf'] = 'No ETA' if field == 'eta' else r['perf']
            fixes.setdefault('corrupted_cleaned', 0)
            fixes['corrupted_cleaned'] += 1

print(f"\nFixes applied:")
for k, v in fixes.items():
    print(f"  {k}: {v}")

# Validation
print(f"\nValidation:")
no_week = [r for r in data if not r['week']]
no_focus = [r for r in data if not r['focus']]
no_ticket = [r for r in data if not r['ticketUrl']]
by_source = {}
for r in data:
    by_source.setdefault(r['source'], 0)
    by_source[r['source']] += 1

print(f"  Records without week: {len(no_week)}")
print(f"  Records without focus: {len(no_focus)}")
print(f"  Records without ticket URL: {len(no_ticket)}")
print(f"  By source: {by_source}")

if no_week:
    print(f"\n  Still missing week:")
    for r in no_week:
        print(f"    {r['tsa']} | {r['focus'][:50]} | dateAdd={r['dateAdd']}")

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"\nSaved: {DATA_PATH}")
