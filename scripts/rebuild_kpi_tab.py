#!/usr/bin/env python3
"""
Rebuild 'Thiago Calculations' tab with English labels + improved formatting.
Row 1: English month names merged
Row 2: Friendly labels (JAN W.1, FEB W.2, etc.)
Row 3: Hidden - DB week range strings for formula matching
Row 4: blank separator
Row 5: Internal group header
Rows 6-10: Internal TSA data
Row 11: blank separator
Row 12: External group header
Rows 13-17: External TSA data
"""
import os
from datetime import date, timedelta
from collections import OrderedDict
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

KPI_ID = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w'
DB_ID  = '1XaJgJCExt_dQ-RBY0eINP-0UCnCH7hYjGC3ibPlluzw'
FIRST_DATA_COL = 4  # Column E (0-indexed)

TSA_DISPLAY = ['Alexandra', 'Carlos', 'Diego', 'Gabrielle', 'Thiago']

MONTH_EN = {12: 'DECEMBER', 1: 'JANUARY', 2: 'FEBRUARY', 3: 'MARCH', 4: 'APRIL'}
MONTH_ABBR = {12: 'DEC', 1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR'}

# --- Auth ---
creds = Credentials(
    token=None,
    refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)
sh = service.spreadsheets()

# --- Helpers ---
def col_letter(idx):
    r = ''
    while True:
        r = chr(65 + idx % 26) + r
        idx = idx // 26 - 1
        if idx < 0: break
    return r

def gen_weeks():
    weeks = []
    d = date(2025, 12, 1)  # First Monday Dec 2025
    while d < date(2026, 4, 18):
        fri = d + timedelta(days=4)
        weeks.append({
            'db_str': f"{d.month:02d}/{d.day:02d} - {fri.month:02d}/{fri.day:02d}/{fri.year}",
            'month': d.month,
            'year': d.year
        })
        d += timedelta(days=7)
    return weeks

def make_formula(row, col_idx, category):
    """On Time / (On Time + Late) — only Done tasks count. In Progress ignored."""
    cl = col_letter(col_idx)
    tsa = f'IF($D{row}="Gabrielle","GABI",UPPER($D{row}))'
    base = (f'DB_Data!$A:$A,{tsa},'
            f'DB_Data!$B:$B,{cl}$3,'
            f'DB_Data!$F:$F,"{category}"')
    on_time = f'COUNTIFS({base},DB_Data!$K:$K,"On Time")'
    late = f'COUNTIFS({base},DB_Data!$K:$K,"Late")'
    return f'=IFERROR({on_time}/({on_time}+{late}),1)'

# --- Generate weeks ---
weeks = gen_weeks()
TOTAL_COLS = FIRST_DATA_COL + len(weeks)
LAST_COL = col_letter(TOTAL_COLS - 1)

months = OrderedDict()
for w in weeks:
    base = MONTH_EN.get(w['month'], str(w['month']))
    # Add year suffix if not 2026 to distinguish Dec 2025
    name = f"{base} '{str(w['year'])[-2:]}" if w['year'] != 2026 else base
    months.setdefault(name, []).append(w)

print(f"Weeks: {len(weeks)}, Months: {len(months)}, Cols: {TOTAL_COLS} (A-{LAST_COL})")
for m, ws in months.items():
    print(f"  {m}: {len(ws)} weeks")

# --- Build friendly labels ---
week_labels = []
month_counters = {}
for w in weeks:
    abbr = MONTH_ABBR[w['month']]
    month_counters.setdefault(w['month'], 0)
    month_counters[w['month']] += 1
    yr = str(w['year'])[-2:]
    week_labels.append(f"{yr}-{w['month']:02d} W.{month_counters[w['month']]}")

print("Labels:", week_labels)

# --- Get sheet ID ---
sp = sh.get(spreadsheetId=KPI_ID).execute()
ids = {s['properties']['title']: s['properties']['sheetId'] for s in sp['sheets']}
test_id = ids.get('Thiago Calculations')
if not test_id:
    print("ERROR: 'Thiago Calculations' not found")
    exit(1)

# --- Clear existing content ---
sh.values().clear(spreadsheetId=KPI_ID, range="'Thiago Calculations'!A:AZ").execute()
reqs = [
    {'unmergeCells': {'range': {'sheetId': test_id,
        'startRowIndex': 0, 'endRowIndex': 50, 'startColumnIndex': 0, 'endColumnIndex': 30}}},
    {'repeatCell': {
        'range': {'sheetId': test_id,
            'startRowIndex': 0, 'endRowIndex': 50, 'startColumnIndex': 0, 'endColumnIndex': 30},
        'cell': {'userEnteredFormat': {}}, 'fields': 'userEnteredFormat'}}
]
# Remove existing conditional format rules
existing = sh.get(spreadsheetId=KPI_ID, fields='sheets.conditionalFormats,sheets.properties').execute()
for sheet in existing['sheets']:
    if sheet['properties']['sheetId'] == test_id:
        rules = sheet.get('conditionalFormats', [])
        for i in range(len(rules) - 1, -1, -1):
            reqs.append({'deleteConditionalFormatRule': {'sheetId': test_id, 'index': i}})
        break

sh.batchUpdate(spreadsheetId=KPI_ID, body={'requests': reqs}).execute()
print("Cleared old content and formats")

# --- Build values ---
vals = []

# Row 1: Month names (English)
vals.append([''] * TOTAL_COLS)

# Row 2: Friendly labels (JAN W.1, etc.)
r2 = ['Metrics', 'Group', 'Category', 'TSA']
for label in week_labels:
    r2.append(label)
vals.append(r2)

# Row 3: Hidden - DB format week ranges
r3 = ['', '', '', '']
for w in weeks:
    r3.append(w['db_str'])
vals.append(r3)

# Row 4: blank separator
vals.append([])

# Row 5: Internal header
vals.append([
    'TSA Internal Demands', 'Delivery',
    'Are estimations met effectively? (internal timelines)',
    '>90% target'
])

# Rows 6-10: Internal TSA data
for tsa in TSA_DISPLAY:
    row = ['', '', '', tsa]
    rn = len(vals) + 1  # 1-based sheet row
    for i in range(len(weeks)):
        row.append(make_formula(rn, FIRST_DATA_COL + i, 'Internal'))
    vals.append(row)

# Row 11: blank separator
vals.append([])

# Row 12: External header
vals.append([
    'TSA External Demands', 'Delivery',
    'Are estimations met effectively? (external timelines)',
    '>90% target'
])

# Rows 13-17: External TSA data
for tsa in TSA_DISPLAY:
    row = ['', '', '', tsa]
    rn = len(vals) + 1
    for i in range(len(weeks)):
        row.append(make_formula(rn, FIRST_DATA_COL + i, 'External'))
    vals.append(row)

TOTAL_ROWS = len(vals)
print(f"Built {TOTAL_ROWS} rows x {TOTAL_COLS} cols")

# Write all values
sh.values().update(
    spreadsheetId=KPI_ID,
    range=f"'Thiago Calculations'!A1:{LAST_COL}{TOTAL_ROWS}",
    valueInputOption='USER_ENTERED',
    body={'values': vals}
).execute()
print("Written values + formulas")

# Write month names to row 1
mrow = ['', '', '', '']
for name, mweeks in months.items():
    mrow.append(name)
    mrow.extend([''] * (len(mweeks) - 1))
sh.values().update(
    spreadsheetId=KPI_ID, range=f"'Thiago Calculations'!A1:{LAST_COL}1",
    valueInputOption='USER_ENTERED', body={'values': [mrow]}
).execute()
print("Written month names (English)")

# ============================
# FORMATTING
# ============================
reqs = []

# --- Merges ---
# Merge A1:D1
reqs.append({'mergeCells': {'range': {
    'sheetId': test_id, 'startRowIndex': 0, 'endRowIndex': 1,
    'startColumnIndex': 0, 'endColumnIndex': 4
}, 'mergeType': 'MERGE_ALL'}})

# Merge months in row 1
cs = FIRST_DATA_COL
for name, mweeks in months.items():
    ce = cs + len(mweeks)
    if len(mweeks) > 1:
        reqs.append({'mergeCells': {'range': {
            'sheetId': test_id, 'startRowIndex': 0, 'endRowIndex': 1,
            'startColumnIndex': cs, 'endColumnIndex': ce
        }, 'mergeType': 'MERGE_ALL'}})
    cs = ce

# --- Row 1: Month headers with alternating dark shades ---
MONTH_COLORS = [
    {'red': 0.13, 'green': 0.13, 'blue': 0.13},
    {'red': 0.22, 'green': 0.22, 'blue': 0.22},
    {'red': 0.13, 'green': 0.13, 'blue': 0.13},
    {'red': 0.22, 'green': 0.22, 'blue': 0.22},
]
reqs.append({'repeatCell': {
    'range': {'sheetId': test_id, 'startRowIndex': 0, 'endRowIndex': 1,
              'startColumnIndex': 0, 'endColumnIndex': FIRST_DATA_COL},
    'cell': {'userEnteredFormat': {
        'backgroundColor': {'red': 0.10, 'green': 0.10, 'blue': 0.10},
        'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True, 'fontSize': 12},
        'horizontalAlignment': 'CENTER', 'verticalAlignment': 'MIDDLE'
    }}, 'fields': 'userEnteredFormat'
}})

col_start = FIRST_DATA_COL
for i, (name, mweeks) in enumerate(months.items()):
    ce = col_start + len(mweeks)
    reqs.append({'repeatCell': {
        'range': {'sheetId': test_id, 'startRowIndex': 0, 'endRowIndex': 1,
                  'startColumnIndex': col_start, 'endColumnIndex': ce},
        'cell': {'userEnteredFormat': {
            'backgroundColor': MONTH_COLORS[i % 4],
            'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True, 'fontSize': 12},
            'horizontalAlignment': 'CENTER', 'verticalAlignment': 'MIDDLE'
        }}, 'fields': 'userEnteredFormat'
    }})
    col_start = ce

# --- Row 2: Sub-headers (friendly labels) ---
reqs.append({'repeatCell': {
    'range': {'sheetId': test_id, 'startRowIndex': 1, 'endRowIndex': 2,
              'startColumnIndex': 0, 'endColumnIndex': TOTAL_COLS},
    'cell': {'userEnteredFormat': {
        'backgroundColor': {'red': 0.90, 'green': 0.92, 'blue': 0.94},
        'textFormat': {'bold': True, 'fontSize': 9, 'foregroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2}},
        'horizontalAlignment': 'CENTER', 'verticalAlignment': 'MIDDLE',
        'borders': {'bottom': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}}}}
    }}, 'fields': 'userEnteredFormat'
}})

# --- Row 3: Hidden DB format row ---
reqs.append({'updateDimensionProperties': {
    'properties': {'pixelSize': 1, 'hiddenByUser': True},
    'range': {'sheetId': test_id, 'dimension': 'ROWS', 'startIndex': 2, 'endIndex': 3},
    'fields': 'pixelSize,hiddenByUser'
}})

# --- Row 4 & 11: Thin separators ---
for idx in [3, 10]:
    reqs.append({'updateDimensionProperties': {
        'properties': {'pixelSize': 8},
        'range': {'sheetId': test_id, 'dimension': 'ROWS', 'startIndex': idx, 'endIndex': idx + 1},
        'fields': 'pixelSize'
    }})
    reqs.append({'repeatCell': {
        'range': {'sheetId': test_id, 'startRowIndex': idx, 'endRowIndex': idx + 1,
                  'startColumnIndex': 0, 'endColumnIndex': TOTAL_COLS},
        'cell': {'userEnteredFormat': {
            'backgroundColor': {'red': 0.85, 'green': 0.85, 'blue': 0.85}
        }}, 'fields': 'userEnteredFormat'
    }})

# --- Group headers (rows 5 and 12, idx 4 and 11) ---
GROUP_COLORS = [
    {'red': 0.22, 'green': 0.46, 'blue': 0.69},  # Steel blue (internal)
    {'red': 0.36, 'green': 0.54, 'blue': 0.66},  # Muted teal (external)
]
for i, idx in enumerate([4, 11]):
    reqs.append({'repeatCell': {
        'range': {'sheetId': test_id, 'startRowIndex': idx, 'endRowIndex': idx + 1,
                  'startColumnIndex': 0, 'endColumnIndex': TOTAL_COLS},
        'cell': {'userEnteredFormat': {
            'backgroundColor': GROUP_COLORS[i],
            'textFormat': {'bold': True, 'fontSize': 10,
                           'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
            'verticalAlignment': 'MIDDLE',
            'borders': {
                'top': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': {'red': 0.3, 'green': 0.3, 'blue': 0.3}}},
                'bottom': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': {'red': 0.3, 'green': 0.3, 'blue': 0.3}}}
            }
        }}, 'fields': 'userEnteredFormat'
    }})

# --- TSA name column (D) ---
for s, e in [(5, 10), (12, 17)]:
    reqs.append({'repeatCell': {
        'range': {'sheetId': test_id, 'startRowIndex': s, 'endRowIndex': e,
                  'startColumnIndex': 3, 'endColumnIndex': 4},
        'cell': {'userEnteredFormat': {
            'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.97},
            'textFormat': {'bold': True, 'fontSize': 10},
            'verticalAlignment': 'MIDDLE',
            'borders': {'right': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': {'red': 0.5, 'green': 0.5, 'blue': 0.5}}}}
        }}, 'fields': 'userEnteredFormat'
    }})

# --- Alternating week column tints + borders ---
TINT_A = {'red': 1.0,  'green': 1.0,  'blue': 1.0}
TINT_B = {'red': 0.94, 'green': 0.96, 'blue': 0.98}
THIN = {'style': 'SOLID', 'colorStyle': {'rgbColor': {'red': 0.75, 'green': 0.75, 'blue': 0.75}}}

for s, e in [(5, 10), (12, 17)]:
    for i in range(len(weeks)):
        col = FIRST_DATA_COL + i
        tint = TINT_A if i % 2 == 0 else TINT_B
        reqs.append({'repeatCell': {
            'range': {'sheetId': test_id, 'startRowIndex': s, 'endRowIndex': e,
                      'startColumnIndex': col, 'endColumnIndex': col + 1},
            'cell': {'userEnteredFormat': {
                'backgroundColor': tint,
                'numberFormat': {'type': 'PERCENT', 'pattern': '0%'},
                'horizontalAlignment': 'CENTER', 'verticalAlignment': 'MIDDLE',
                'borders': {'left': THIN, 'right': THIN, 'top': THIN, 'bottom': THIN}
            }}, 'fields': 'userEnteredFormat'
        }})

# --- Left columns A-C: light bg for data rows ---
for s, e in [(5, 10), (12, 17)]:
    reqs.append({'repeatCell': {
        'range': {'sheetId': test_id, 'startRowIndex': s, 'endRowIndex': e,
                  'startColumnIndex': 0, 'endColumnIndex': 3},
        'cell': {'userEnteredFormat': {
            'backgroundColor': {'red': 0.97, 'green': 0.97, 'blue': 0.97},
            'verticalAlignment': 'MIDDLE'
        }}, 'fields': 'userEnteredFormat'
    }})

# --- Thick month separator borders ---
MONTH_BORDER = {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2}}}
for name, mweeks in months.items():
    first_col = FIRST_DATA_COL + weeks.index(mweeks[0])
    reqs.append({'updateBorders': {
        'range': {'sheetId': test_id, 'startRowIndex': 0, 'endRowIndex': 17,
                  'startColumnIndex': first_col, 'endColumnIndex': first_col + 1},
        'left': MONTH_BORDER
    }})
# Right border on last column
reqs.append({'updateBorders': {
    'range': {'sheetId': test_id, 'startRowIndex': 0, 'endRowIndex': 17,
              'startColumnIndex': TOTAL_COLS - 1, 'endColumnIndex': TOTAL_COLS},
    'right': MONTH_BORDER
}})

# --- Bottom borders after last data rows ---
for row_idx in [9, 16]:
    reqs.append({'updateBorders': {
        'range': {'sheetId': test_id, 'startRowIndex': row_idx, 'endRowIndex': row_idx + 1,
                  'startColumnIndex': 0, 'endColumnIndex': TOTAL_COLS},
        'bottom': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}}}
    }})

# --- Row heights ---
reqs.append({'updateDimensionProperties': {
    'properties': {'pixelSize': 32},
    'range': {'sheetId': test_id, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
    'fields': 'pixelSize'
}})
reqs.append({'updateDimensionProperties': {
    'properties': {'pixelSize': 28},
    'range': {'sheetId': test_id, 'dimension': 'ROWS', 'startIndex': 1, 'endIndex': 2},
    'fields': 'pixelSize'
}})
for s, e in [(4, 5), (11, 12)]:
    reqs.append({'updateDimensionProperties': {
        'properties': {'pixelSize': 30},
        'range': {'sheetId': test_id, 'dimension': 'ROWS', 'startIndex': s, 'endIndex': e},
        'fields': 'pixelSize'
    }})
for s, e in [(5, 10), (12, 17)]:
    reqs.append({'updateDimensionProperties': {
        'properties': {'pixelSize': 26},
        'range': {'sheetId': test_id, 'dimension': 'ROWS', 'startIndex': s, 'endIndex': e},
        'fields': 'pixelSize'
    }})

# --- Column widths ---
reqs.append({'updateDimensionProperties': {
    'properties': {'pixelSize': 200},
    'range': {'sheetId': test_id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
    'fields': 'pixelSize'}})
for ci in [1, 2]:
    reqs.append({'updateDimensionProperties': {
        'properties': {'pixelSize': 120},
        'range': {'sheetId': test_id, 'dimension': 'COLUMNS', 'startIndex': ci, 'endIndex': ci+1},
        'fields': 'pixelSize'}})
reqs.append({'updateDimensionProperties': {
    'properties': {'pixelSize': 90},
    'range': {'sheetId': test_id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4},
    'fields': 'pixelSize'}})
reqs.append({'updateDimensionProperties': {
    'properties': {'pixelSize': 85},
    'range': {'sheetId': test_id, 'dimension': 'COLUMNS',
              'startIndex': FIRST_DATA_COL, 'endIndex': TOTAL_COLS},
    'fields': 'pixelSize'}})

# --- Freeze rows 2 + cols 4 ---
reqs.append({'updateSheetProperties': {
    'properties': {'sheetId': test_id,
        'gridProperties': {'frozenRowCount': 2, 'frozenColumnCount': 4}},
    'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
}})

# --- Conditional formatting ---
data_ranges = [
    {'sheetId': test_id, 'startRowIndex': 5, 'endRowIndex': 10,
     'startColumnIndex': FIRST_DATA_COL, 'endColumnIndex': TOTAL_COLS},
    {'sheetId': test_id, 'startRowIndex': 12, 'endRowIndex': 17,
     'startColumnIndex': FIRST_DATA_COL, 'endColumnIndex': TOTAL_COLS}
]

reqs.append({'addConditionalFormatRule': {'rule': {
    'ranges': data_ranges,
    'booleanRule': {
        'condition': {'type': 'NUMBER_GREATER_THAN_EQ', 'values': [{'userEnteredValue': '0.9'}]},
        'format': {'backgroundColor': {'red': 0.56, 'green': 0.77, 'blue': 0.49}}
    }}, 'index': 0}})

reqs.append({'addConditionalFormatRule': {'rule': {
    'ranges': data_ranges,
    'booleanRule': {
        'condition': {'type': 'NUMBER_BETWEEN',
                      'values': [{'userEnteredValue': '0.5'}, {'userEnteredValue': '0.8999'}]},
        'format': {'backgroundColor': {'red': 1.0, 'green': 0.85, 'blue': 0.4}}
    }}, 'index': 1}})

reqs.append({'addConditionalFormatRule': {'rule': {
    'ranges': data_ranges,
    'booleanRule': {
        'condition': {'type': 'NUMBER_LESS', 'values': [{'userEnteredValue': '0.5'}]},
        'format': {'backgroundColor': {'red': 0.91, 'green': 0.49, 'blue': 0.45}}
    }}, 'index': 2}})

# --- Execute ---
print(f"Sending {len(reqs)} formatting requests...")
sh.batchUpdate(spreadsheetId=KPI_ID, body={'requests': reqs}).execute()
print("Done!")
print(f"\nTab rebuilt: {TOTAL_ROWS} rows x {TOTAL_COLS} cols")
print(f"Row 1: {', '.join(months.keys())}")
print(f"Row 2: {', '.join(week_labels)}")
print("Row 3: Hidden (DB week ranges for formula matching)")
