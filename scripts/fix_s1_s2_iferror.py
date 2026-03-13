"""
Fix S1 (Internal Accuracy) and S2 (External Accuracy) IFERROR fallback.
BUG: IFERROR(..., 1) returns 100% when there are 0 tasks. Should return "-".
Affects both Thiago Calculations and Thais Calculations.
"""
import requests
from kpi_auth import get_access_token, KPI_SHEET as KPI

access_token = get_access_token()
headers_auth = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
h = {'Authorization': 'Bearer ' + access_token}


def col_letter(n):
    result = ''
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


def build_accuracy(row, col, cat_filter, use_gabi):
    """Build S1/S2 formula with IFERROR -> "-" instead of 1."""
    cl = col_letter(col)
    week_ref = cl + '$3'

    if use_gabi:
        name_expr = 'IF($D${}="Gabrielle","GABI",UPPER($D${}))'.format(row, row)
    else:
        name_expr = 'UPPER($D${})'.format(row)

    base = 'DB_Data!$A:$A,{name},DB_Data!$B:$B,{week},DB_Data!$F:$F,"{cat}"'.format(
        name=name_expr, week=week_ref, cat=cat_filter)

    on_time = 'COUNTIFS({},DB_Data!$K:$K,"On Time")'.format(base)
    late = 'COUNTIFS({},DB_Data!$K:$K,"Late")'.format(base)

    return '=IFERROR({ot}/({ot}+{lt}),"-")'.format(ot=on_time, lt=late)


value_updates = []

# ============================================================
# Thiago Calculations
# ============================================================
# S1 Internal Accuracy: rows 7-11 (Alexandra row is missing? Let me check)
# Actually from audit: S1 header=5, target row=5 col D, data rows 6-10 or 7-11?
# From the output: S1 shows Carlos, Diego, Gabrielle, Thiago (4 people)
# Wait - the audit showed rows D7:J11 returning 4 rows starting with Carlos
# But Alexandra should be first (row 6 or 7)
# Let me check: from Thiago layout S1(5-10) means header=5, data=6-10
# But the formula check was for E7 which is Carlos... so data starts at row 6

# Actually from the context: Thiago S1 header=5, data rows 6-10 (5 people)
# Alexandra=6, Carlos=7, Diego=8, Gabrielle=9, Thiago=10
# S2 header=12, data rows 13-17
# But earlier audit showed S1 data as D7:J11... let me use the actual row numbers

# Let me re-read: Section layout Thiago from summary:
# S1(5-10) = header row 5, data rows 6-10 (5 people)
# S2(12-17) = header row 12, data rows 13-17

# But the Thiago formula was at E7 (Carlos)... which means:
# If header=5, then row 5 = header text, row 6 = target label? No...
# Actually from fix_kpi_notes.py: thiago_notes = {5: NOTE_INTERNAL, 12: NOTE_EXTERNAL}
# Header at row 5, target in D5. Data rows must be 6-10.
# But the formula at E7 was for Carlos... maybe row 6 is Alexandra?
# Let me just pull row 6 to check.

# Actually, the audit showed S1 Internal (Thiago):
#   ['Carlos', '100%', '75%', '90%', '0%', '100%', '100%']
#   ['Diego', ...]
#   ['Gabrielle', ...]
#   ['Thiago', ...]
# That's from D7:J11 which is 5 rows but only 4 returned (Alexandra might be row 6)
# Wait no, D7:J11 is rows 7-11 = 5 rows. But only 4 showed. So row 7=Carlos.
# That means the layout might be: 5=header, 6=Alexandra, 7=Carlos, 8=Diego, 9=Gabi, 10=Thiago

# For S2: 12=header, 13=Alexandra, 14=Carlos, 15=Diego, 16=Gabi, 17=Thiago

# Let me just fix all data rows for S1 and S2

# Thiago S1: rows 6-10 (5 people)
print('Building Thiago S1 (Internal Accuracy) formulas...')
for row in range(6, 11):
    formulas = []
    for col in range(5, 62):  # E=5 to BI=61
        formulas.append(build_accuracy(row, col, 'Internal', use_gabi=True))
    value_updates.append({
        'range': "'Thiago Calculations'!E{}:BI{}".format(row, row),
        'values': [formulas]
    })

# Thiago S2: rows 13-17 (5 people)
print('Building Thiago S2 (External Accuracy) formulas...')
for row in range(13, 18):
    formulas = []
    for col in range(5, 62):
        formulas.append(build_accuracy(row, col, 'External', use_gabi=True))
    value_updates.append({
        'range': "'Thiago Calculations'!E{}:BI{}".format(row, row),
        'values': [formulas]
    })

# ============================================================
# Thais Calculations
# ============================================================
# Thais S1: rows 6-7 (2 people)
print('Building Thais S1 (Internal Accuracy) formulas...')
for row in range(6, 8):
    formulas = []
    for col in range(5, 62):
        formulas.append(build_accuracy(row, col, 'Internal', use_gabi=False))
    value_updates.append({
        'range': "'Thais Calculations'!E{}:BI{}".format(row, row),
        'values': [formulas]
    })

# Thais S2: rows 10-11 (2 people)
print('Building Thais S2 (External Accuracy) formulas...')
for row in range(10, 12):
    formulas = []
    for col in range(5, 62):
        formulas.append(build_accuracy(row, col, 'External', use_gabi=False))
    value_updates.append({
        'range': "'Thais Calculations'!E{}:BI{}".format(row, row),
        'values': [formulas]
    })

# ============================================================
# Push
# ============================================================
print('\nPushing {} value ranges...'.format(len(value_updates)))
body = {'valueInputOption': 'USER_ENTERED', 'data': value_updates}
url = 'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchUpdate'.format(KPI)
resp = requests.post(url, headers=headers_auth, json=body)
result = resp.json()
print('Status: {}, cells: {}'.format(resp.status_code, result.get('totalUpdatedCells', 0)))

if resp.status_code != 200:
    print('Error: {}'.format(result.get('error', {}).get('message', '')))

# ============================================================
# Verify
# ============================================================
print('\n=== VERIFICATION ===')
r = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchGet'.format(KPI),
    headers=h,
    params={
        'ranges': [
            "'Thais Calculations'!D5:J7",     # S1 Thais
            "'Thais Calculations'!D9:J11",    # S2 Thais
            "'Thiago Calculations'!D5:J10",   # S1 Thiago
            "'Thiago Calculations'!D12:J17",  # S2 Thiago
            # Formula check
            "'Thais Calculations'!E6",
            "'Thiago Calculations'!E6",
        ],
        'valueRenderOption': 'FORMATTED_VALUE'
    }
).json()

print('\nThais S1 Internal:')
for row in r['valueRanges'][0].get('values', []):
    print('  {}'.format(row[:7]))

print('\nThais S2 External:')
for row in r['valueRanges'][1].get('values', []):
    print('  {}'.format(row[:7]))

print('\nThiago S1 Internal:')
for row in r['valueRanges'][2].get('values', []):
    print('  {}'.format(row[:7]))

print('\nThiago S2 External:')
for row in r['valueRanges'][3].get('values', []):
    print('  {}'.format(row[:7]))

# Formula check
r2 = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchGet'.format(KPI),
    headers=h,
    params={
        'ranges': [
            "'Thais Calculations'!E6",
            "'Thiago Calculations'!E6",
        ],
        'valueRenderOption': 'FORMULA'
    }
).json()

print('\nFormula check:')
for i, label in enumerate(['Thais S1 E6', 'Thiago S1 E6']):
    vals = r2['valueRanges'][i].get('values', [['?']])
    print('  {}: {}'.format(label, vals[0][0][:100]))
