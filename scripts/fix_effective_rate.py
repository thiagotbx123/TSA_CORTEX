"""
Rewrite S10 as Effective Delivery Rate:
= On Time / (On Time + Late + Overdue)
Includes open overdue tasks in denominator, making it stricter than Timeline.
"""
import requests
from kpi_auth import get_access_token, KPI_SHEET as KPI, THIAGO_SID, THAIS_SID

access_token = get_access_token()
headers_auth = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
h = {'Authorization': 'Bearer ' + access_token}


def col_letter(n):
    result = ''
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


def build_effective_rate(row, col, use_gabi):
    cl = col_letter(col)
    week_ref = cl + '$3'

    if use_gabi:
        name_expr = 'IF($D${}="Gabrielle","GABI",UPPER($D${}))'.format(row, row)
    else:
        name_expr = 'UPPER($D${})'.format(row)

    base = 'DB_Data!$A:$A,{name},DB_Data!$B:$B,{week}'.format(
        name=name_expr, week=week_ref)

    on_time = 'COUNTIFS({},DB_Data!$K:$K,"On Time")'.format(base)
    late = 'COUNTIFS({},DB_Data!$K:$K,"Late")'.format(base)
    overdue = 'COUNTIFS({},DB_Data!$K:$K,"Overdue")'.format(base)

    return '=IFERROR({ot}/({ot}+{lt}+{od}),"-")'.format(
        ot=on_time, lt=late, od=overdue)


# ============================================================
# PART 1: Push formulas
# ============================================================
value_updates = []

# Thiago: rows 69-73
for row in range(69, 74):
    formulas = []
    for col in range(5, 62):
        formulas.append(build_effective_rate(row, col, use_gabi=True))
    value_updates.append({
        'range': "'Thiago Calculations'!E{}:BI{}".format(row, row),
        'values': [formulas]
    })

# Thais: rows 42-43
for row in range(42, 44):
    formulas = []
    for col in range(5, 62):
        formulas.append(build_effective_rate(row, col, use_gabi=False))
    value_updates.append({
        'range': "'Thais Calculations'!E{}:BI{}".format(row, row),
        'values': [formulas]
    })

# Headers
value_updates.append({
    'range': "'Thiago Calculations'!A68",
    'values': [['Effective Delivery Rate\nOn Time vs total workload (including overdue)']]
})
value_updates.append({
    'range': "'Thiago Calculations'!D68",
    'values': [['>85% target']]
})
value_updates.append({
    'range': "'Thais Calculations'!A41",
    'values': [['Effective Delivery Rate\nOn Time vs total workload (including overdue)']]
})
value_updates.append({
    'range': "'Thais Calculations'!D41",
    'values': [['>85% target']]
})

# OBS rows
value_updates.append({
    'range': "'Thiago Calculations'!A75",
    'values': [['OBS: On Time / (On Time + Late + Overdue). Stricter than Timeline \u2014 penalizes open overdue tasks, not just late deliveries. Lower target (85%) because denominator includes unfinished work.']]
})
value_updates.append({
    'range': "'Thais Calculations'!A45",
    'values': [['OBS: On Time / (On Time + Late + Overdue). Stricter than Timeline \u2014 includes open overdue tasks in denominator.']]
})

print('Pushing {} value ranges...'.format(len(value_updates)))
body = {'valueInputOption': 'USER_ENTERED', 'data': value_updates}
url = 'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchUpdate'.format(KPI)
resp = requests.post(url, headers=headers_auth, json=body)
print('Status: {}, cells: {}'.format(resp.status_code, resp.json().get('totalUpdatedCells', 0)))

# ============================================================
# PART 2: Update notes
# ============================================================
NOTE_EFFECTIVE = (
    'FORMULA: On Time / (On Time + Late + Overdue)\n'
    'SOURCE: DB_Data col K (Delivery Performance)\n'
    'FILTER: All tasks for that person + week (no status filter)\n'
    'TARGET: >85% \u2014 stricter than Timeline\n'
    'KEY DIFFERENCE: Includes Overdue (open past-due tasks) in denominator.\n'
    'Timeline only counts finished work (On Time vs Late).\n'
    'This penalizes having unfinished overdue tasks.\n'
    'Example: 17 OnTime, 1 Late, 3 Overdue \u2192 Timeline=94%, EffectiveRate=81%\n'
    'COLOR: Green >=90% | Yellow 50-89% | Red <50%'
)

batch_requests = []
for sid, row in [(THIAGO_SID, 68), (THAIS_SID, 41)]:
    batch_requests.append({
        'updateCells': {
            'rows': [{'values': [{'note': NOTE_EFFECTIVE}]}],
            'fields': 'note',
            'range': {
                'sheetId': sid,
                'startRowIndex': row - 1,
                'endRowIndex': row,
                'startColumnIndex': 3,
                'endColumnIndex': 4
            }
        }
    })

url2 = 'https://sheets.googleapis.com/v4/spreadsheets/{}:batchUpdate'.format(KPI)
resp2 = requests.post(url2, headers=headers_auth, json={'requests': batch_requests})
print('Notes: {}'.format(resp2.status_code))

# ============================================================
# PART 3: Verify
# ============================================================
print('\n=== VERIFICATION ===')
r = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchGet'.format(KPI),
    headers=h,
    params={
        'ranges': [
            'Thiago Calculations!E3:BI3',
            'Thiago Calculations!D62:BI66',
            'Thiago Calculations!D69:BI73',
        ],
        'valueRenderOption': 'FORMATTED_VALUE'
    }
).json()

weeks = r['valueRanges'][0].get('values', [[]])[0]
timeline = r['valueRanges'][1].get('values', [])
effective = r['valueRanges'][2].get('values', [])

identical = 0
different = 0

for pi in range(5):
    name = timeline[pi][0]
    diffs = []
    same = 0
    for w in range(min(len(timeline[pi]) - 1, len(effective[pi]) - 1)):
        tv = timeline[pi][w + 1] if w + 1 < len(timeline[pi]) else '-'
        ev = effective[pi][w + 1] if w + 1 < len(effective[pi]) else '-'
        if tv == '-' and ev == '-':
            continue
        if tv == ev:
            identical += 1
            same += 1
        else:
            different += 1
            diffs.append((weeks[w] if w < len(weeks) else '?', tv, ev))

    print('{}: {} same, {} DIFFERENT'.format(name, same, len(diffs)))
    for wk, tv, ev in diffs:
        print('  {} : Timeline={} Effective={}'.format(wk, tv, ev))

print('\nTOTAL: {} identical, {} DIFFERENT'.format(identical, different))
if different > 0:
    print('SUCCESS! Indicators now show different values.')
else:
    print('STILL IDENTICAL - need investigation')
