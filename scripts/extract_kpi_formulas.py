"""Extract actual formulas and conditional formatting for KPI Playbook."""
import requests
from kpi_auth import get_access_token, KPI_SHEET as KPI

access_token = get_access_token()
h = {'Authorization': 'Bearer ' + access_token}

# Pull one formula per section (Carlos row in Thiago, Thais row in Thais)
cells = [
    ("S1 Internal Accuracy", "Thiago Calculations", "E7"),
    ("S2 External Accuracy", "Thiago Calculations", "E14"),
    ("S3 Throughput", "Thiago Calculations", "E21"),
    ("S4 Overdue", "Thiago Calculations", "E28"),
    ("S5 WIP", "Thiago Calculations", "E35"),
    ("S6 Internal Count", "Thiago Calculations", "E42"),
    ("S7 External Count", "Thiago Calculations", "E49"),
    ("S8 Avg Exec Time", "Thiago Calculations", "E56"),
    ("S9 Timeline Combined", "Thiago Calculations", "E63"),
    ("S10 ETA Compliance", "Thiago Calculations", "E70"),
    ("Team Avg Exec", "Thiago Calculations", "E60"),
    ("Team Avg Timeline", "Thiago Calculations", "E67"),
    ("Team Avg ETA", "Thiago Calculations", "E74"),
    ("Thais Avg Exec", "Thais Calculations", "E34"),
    ("Thais Timeline", "Thais Calculations", "E38"),
    ("Thais ETA", "Thais Calculations", "E42"),
]

ranges = ["'{}'!{}".format(s, c) for _, s, c in cells]

r = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchGet'.format(KPI),
    headers=h,
    params={'ranges': ranges, 'valueRenderOption': 'FORMULA'}
).json()

for i, vr in enumerate(r.get('valueRanges', [])):
    vals = vr.get('values', [['(empty)']])
    formula = vals[0][0] if vals and vals[0] else '(empty)'
    print('=== {} ==='.format(cells[i][0]))
    print(formula)
    print()

# Conditional formatting
print('=== CONDITIONAL FORMATTING ===')
cf_url = 'https://sheets.googleapis.com/v4/spreadsheets/{}?fields=sheets(properties(sheetId,title),conditionalFormats)'.format(KPI)
cf_data = requests.get(cf_url, headers=h).json()
for sheet in cf_data['sheets']:
    title = sheet['properties']['title']
    if title in ('Thiago Calculations', 'Thais Calculations'):
        cfs = sheet.get('conditionalFormats', [])
        print('\n{}: {} rules total'.format(title, len(cfs)))
        for cf in cfs[:6]:
            ranges_str = ', '.join('rows {}-{}'.format(
                rng.get('startRowIndex', '?'), rng.get('endRowIndex', '?'))
                for rng in cf.get('ranges', []))
            rule = cf.get('booleanRule', {})
            cond = rule.get('condition', {})
            fmt = rule.get('format', {})
            bg = fmt.get('backgroundColor', {})
            vals = [v.get('userEnteredValue', '') for v in cond.get('values', [])]
            print('  {} | {} {} | bg: r={:.2f} g={:.2f} b={:.2f}'.format(
                ranges_str,
                cond.get('type', '?'),
                vals,
                bg.get('red', 0), bg.get('green', 0), bg.get('blue', 0)))
