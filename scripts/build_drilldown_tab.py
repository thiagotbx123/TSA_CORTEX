#!/usr/bin/env python3
"""Build interactive '🔍 Drill Down' tab in the KPI spreadsheet.

Dropdowns for TSA, Week, Section → FILTER formula shows matching DB_Data rows.
No Apps Script required — pure Sheets API.
"""
import os, json, sys
sys.stdout.reconfigure(line_buffering=True, encoding='utf-8', errors='replace')
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

KPI_SPREADSHEET_ID = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w'
TAB_NAME = '🔍 Drill Down'

TSA_NAMES = ['THIAGO', 'DIEGO', 'GABI', 'CARLOS', 'ALEXANDRA', 'THAIS', 'YASMIM']
SECTIONS = ['All', 'Internal Delivery', 'External Delivery', 'Throughput',
            'Overdue', 'Internal Tasks', 'External Tasks', 'WIP']

RESULT_HEADERS = ['Focus', 'Status', 'Demand Type', 'Category', 'Customer', 'ETA', 'Delivery Date', 'Performance']
COL_WIDTHS = [280, 110, 130, 110, 160, 100, 110, 120]  # pixels per column A-H

# ── Colours ─────────────────────────────────────────────────────────────
DARK_HEADER = {'red': 0.17, 'green': 0.24, 'blue': 0.31}   # #2c3e50
WHITE       = {'red': 1, 'green': 1, 'blue': 1}
LIGHT_GRAY  = {'red': 0.95, 'green': 0.96, 'blue': 0.96}
LABEL_BG    = {'red': 0.93, 'green': 0.94, 'blue': 0.95}
DROP_BORDER = {'red': 0.20, 'green': 0.51, 'blue': 0.80}   # blue accent

# Conditional formatting colours
GREEN_BG  = {'red': 0.71, 'green': 0.84, 'blue': 0.66}   # #b6d7a8
BLUE_BG   = {'red': 0.79, 'green': 0.85, 'blue': 0.97}   # #c9daf8
YELLOW_BG = {'red': 1.0,  'green': 0.95, 'blue': 0.80}   # #fff2cc
RED_BG    = {'red': 0.96, 'green': 0.80, 'blue': 0.80}   # #f4cccc
ORANGE_BG = {'red': 0.99, 'green': 0.90, 'blue': 0.80}   # #fce5cd
GRAY_BG   = {'red': 0.88, 'green': 0.88, 'blue': 0.88}   # #e0e0e0

# ── Auth ────────────────────────────────────────────────────────────────
creds = Credentials(
    token=None,
    refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets = build('sheets', 'v4', credentials=creds)

# ── 1. Get or create tab ───────────────────────────────────────────────
meta = sheets.spreadsheets().get(spreadsheetId=KPI_SPREADSHEET_ID).execute()
existing = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

# Delete if exists, then recreate fresh (avoids banding/conditional format cleanup)
requests = []
if TAB_NAME in existing:
    requests.append({'deleteSheet': {'sheetId': existing[TAB_NAME]}})
    print(f"Deleting existing '{TAB_NAME}'")

requests.append({'addSheet': {
    'properties': {
        'title': TAB_NAME,
        'gridProperties': {'rowCount': 300, 'columnCount': 12}
    }
}})

resp = sheets.spreadsheets().batchUpdate(
    spreadsheetId=KPI_SPREADSHEET_ID,
    body={'requests': requests}
).execute()

for reply in resp.get('replies', []):
    if 'addSheet' in reply:
        sheet_id = reply['addSheet']['properties']['sheetId']
        break
print(f"Created '{TAB_NAME}' (id={sheet_id})")

# ── 2. Build FILTER formula ────────────────────────────────────────────
# Columns: C=Focus, D=Status, E=DemandType, F=Category, G=Customer, I=ETA, J=DD, K=Perf
# Use arithmetic (+ for OR, * for AND) to always produce arrays — scalar TRUE breaks FILTER.
FILTER_FORMULA = (
    '=IFERROR(FILTER('
    '{DB_Data!C$2:C,DB_Data!D$2:D,DB_Data!E$2:E,DB_Data!F$2:F,DB_Data!G$2:G,DB_Data!I$2:I,DB_Data!J$2:J,DB_Data!K$2:K},'
    'DB_Data!A$2:A=B$2,'
    '(D$2="")+(DB_Data!B$2:B=D$2),'
    '(F$2="All")'
    '+((F$2="Internal Delivery")*(DB_Data!F$2:F="Internal")*((DB_Data!K$2:K="On Time")+(DB_Data!K$2:K="Late")))'
    '+((F$2="External Delivery")*(DB_Data!F$2:F="External")*((DB_Data!K$2:K="On Time")+(DB_Data!K$2:K="Late")))'
    '+((F$2="Throughput")*(DB_Data!D$2:D="Done"))'
    '+((F$2="Overdue")*(DB_Data!K$2:K="Overdue"))'
    '+((F$2="Internal Tasks")*(DB_Data!F$2:F="Internal"))'
    '+((F$2="External Tasks")*(DB_Data!F$2:F="External"))'
    '+((F$2="WIP")*(DB_Data!D$2:D="In Progress"))'
    '),'
    '"")'
)

COUNT_FORMULA = '=IF(B2="","← Select filters",IF(A5="","0 tasks found",COUNTA(A5:A300)&IF(COUNTA(A5:A300)=1," task"," tasks")&" found"))'
WEEK_HELPER = '=SORT(UNIQUE(FILTER(DB_Data!B$2:B,DB_Data!B$2:B<>"")))'

# ── 3. Write values ────────────────────────────────────────────────────
values = [
    # Row 1: Title
    ['🔍 KPI Drill Down', '', '', '', '', '', '', ''],
    # Row 2: Labels + dropdown placeholders
    ['TSA/DE:', '', 'Week:', '', 'Section:', '', '', COUNT_FORMULA],
    # Row 3: separator
    [''] * 8,
    # Row 4: Column headers
    RESULT_HEADERS,
    # Row 5: FILTER formula
    [FILTER_FORMULA] + [''] * 7,
]

# Helper columns (J-K) for dropdown sources — TSA names in J, weeks formula in K
helper_values = []
for i in range(max(len(TSA_NAMES), 1)):
    row = [''] * 2
    if i < len(TSA_NAMES):
        row[0] = TSA_NAMES[i]
    helper_values.append(row)

# Set default dropdown values
values[1][1] = 'THIAGO'   # B2 default
values[1][5] = 'All'      # F2 default

print("Writing values...")
sheets.spreadsheets().values().update(
    spreadsheetId=KPI_SPREADSHEET_ID,
    range=f"'{TAB_NAME}'!A1:H5",
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()

# Write helper TSA list
sheets.spreadsheets().values().update(
    spreadsheetId=KPI_SPREADSHEET_ID,
    range=f"'{TAB_NAME}'!J2:K2",
    valueInputOption='USER_ENTERED',
    body={'values': [[''] * 2]}  # placeholder
).execute()
sheets.spreadsheets().values().update(
    spreadsheetId=KPI_SPREADSHEET_ID,
    range=f"'{TAB_NAME}'!J2:J{2 + len(TSA_NAMES) - 1}",
    valueInputOption='USER_ENTERED',
    body={'values': [[n] for n in TSA_NAMES]}
).execute()
# Week helper formula in K2
sheets.spreadsheets().values().update(
    spreadsheetId=KPI_SPREADSHEET_ID,
    range=f"'{TAB_NAME}'!K2",
    valueInputOption='USER_ENTERED',
    body={'values': [[WEEK_HELPER]]}
).execute()

print("Values written.")

# ── 4. Formatting ──────────────────────────────────────────────────────
fmt_requests = []

# Title row merge + format
fmt_requests.append({'mergeCells': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 8},
    'mergeType': 'MERGE_ALL'
}})
fmt_requests.append({'repeatCell': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 8},
    'cell': {'userEnteredFormat': {
        'backgroundColor': DARK_HEADER,
        'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 14, 'fontFamily': 'Segoe UI'},
        'horizontalAlignment': 'CENTER',
        'verticalAlignment': 'MIDDLE',
        'padding': {'top': 8, 'bottom': 8}
    }},
    'fields': 'userEnteredFormat'
}})

# Row 2: Label cells (A2, C2, E2)
for col_idx in [0, 2, 4]:
    fmt_requests.append({'repeatCell': {
        'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': col_idx, 'endColumnIndex': col_idx + 1},
        'cell': {'userEnteredFormat': {
            'backgroundColor': LABEL_BG,
            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Segoe UI'},
            'horizontalAlignment': 'RIGHT',
            'verticalAlignment': 'MIDDLE',
            'padding': {'right': 6}
        }},
        'fields': 'userEnteredFormat'
    }})

# Row 2: Dropdown cells (B2, D2, F2) — blue border accent
for col_idx in [1, 3, 5]:
    fmt_requests.append({'repeatCell': {
        'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': col_idx, 'endColumnIndex': col_idx + 1},
        'cell': {'userEnteredFormat': {
            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Segoe UI'},
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'borders': {
                'top':    {'style': 'SOLID', 'width': 2, 'color': DROP_BORDER},
                'bottom': {'style': 'SOLID', 'width': 2, 'color': DROP_BORDER},
                'left':   {'style': 'SOLID', 'width': 2, 'color': DROP_BORDER},
                'right':  {'style': 'SOLID', 'width': 2, 'color': DROP_BORDER},
            }
        }},
        'fields': 'userEnteredFormat'
    }})

# H2: Count cell
fmt_requests.append({'repeatCell': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 7, 'endColumnIndex': 8},
    'cell': {'userEnteredFormat': {
        'textFormat': {'bold': False, 'fontSize': 11, 'fontFamily': 'Segoe UI',
                       'foregroundColor': {'red': 0.5, 'green': 0.5, 'blue': 0.5}},
        'horizontalAlignment': 'RIGHT',
        'verticalAlignment': 'MIDDLE',
    }},
    'fields': 'userEnteredFormat'
}})

# Row 4: Column headers
fmt_requests.append({'repeatCell': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 3, 'endRowIndex': 4, 'startColumnIndex': 0, 'endColumnIndex': 8},
    'cell': {'userEnteredFormat': {
        'backgroundColor': DARK_HEADER,
        'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 10, 'fontFamily': 'Segoe UI'},
        'horizontalAlignment': 'CENTER',
        'verticalAlignment': 'MIDDLE',
        'padding': {'top': 4, 'bottom': 4}
    }},
    'fields': 'userEnteredFormat'
}})

# Results area (rows 5-300): light font, alternating would be nice but complex
fmt_requests.append({'repeatCell': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 4, 'endRowIndex': 300, 'startColumnIndex': 0, 'endColumnIndex': 8},
    'cell': {'userEnteredFormat': {
        'textFormat': {'fontSize': 10, 'fontFamily': 'Segoe UI'},
        'verticalAlignment': 'MIDDLE',
        'wrapStrategy': 'WRAP',
    }},
    'fields': 'userEnteredFormat'
}})

# Column widths
for i, w in enumerate(COL_WIDTHS):
    fmt_requests.append({'updateDimensionProperties': {
        'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i + 1},
        'properties': {'pixelSize': w},
        'fields': 'pixelSize'
    }})

# Row heights
fmt_requests.append({'updateDimensionProperties': {
    'range': {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
    'properties': {'pixelSize': 42},
    'fields': 'pixelSize'
}})
fmt_requests.append({'updateDimensionProperties': {
    'range': {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': 1, 'endIndex': 2},
    'properties': {'pixelSize': 36},
    'fields': 'pixelSize'
}})
fmt_requests.append({'updateDimensionProperties': {
    'range': {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': 2, 'endIndex': 3},
    'properties': {'pixelSize': 6},
    'fields': 'pixelSize'
}})

# Hide helper columns J-K
fmt_requests.append({'updateDimensionProperties': {
    'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 9, 'endIndex': 11},
    'properties': {'hiddenByUser': True},
    'fields': 'hiddenByUser'
}})

# Freeze rows 1-4
fmt_requests.append({'updateSheetProperties': {
    'properties': {'sheetId': sheet_id, 'gridProperties': {'frozenRowCount': 4}},
    'fields': 'gridProperties.frozenRowCount'
}})

# Separator row 3: thin bottom border
fmt_requests.append({'updateBorders': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 2, 'endRowIndex': 3, 'startColumnIndex': 0, 'endColumnIndex': 8},
    'bottom': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.85, 'green': 0.85, 'blue': 0.85}}
}})

# ── 5. Data Validation (dropdowns) ─────────────────────────────────────

# B2: TSA dropdown
fmt_requests.append({'setDataValidation': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 1, 'endColumnIndex': 2},
    'rule': {
        'condition': {'type': 'ONE_OF_LIST', 'values': [{'userEnteredValue': n} for n in TSA_NAMES]},
        'showCustomUi': True,
        'strict': False
    }
}})

# D2: Week dropdown (from helper column K)
fmt_requests.append({'setDataValidation': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 3, 'endColumnIndex': 4},
    'rule': {
        'condition': {'type': 'ONE_OF_RANGE', 'values': [{'userEnteredValue': f"='{TAB_NAME}'!$K$2:$K$70"}]},
        'showCustomUi': True,
        'strict': False
    }
}})

# F2: Section dropdown
fmt_requests.append({'setDataValidation': {
    'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 5, 'endColumnIndex': 6},
    'rule': {
        'condition': {'type': 'ONE_OF_LIST', 'values': [{'userEnteredValue': s} for s in SECTIONS]},
        'showCustomUi': True,
        'strict': False
    }
}})

# ── 6. Conditional Formatting ──────────────────────────────────────────

# Status column (B5:B300)
status_rules = [
    ('Done',        GREEN_BG),
    ('In Progress', BLUE_BG),
    ('To Do',       YELLOW_BG),
]
for text, color in status_rules:
    fmt_requests.append({'addConditionalFormatRule': {
        'rule': {
            'ranges': [{'sheetId': sheet_id, 'startRowIndex': 4, 'endRowIndex': 300, 'startColumnIndex': 1, 'endColumnIndex': 2}],
            'booleanRule': {
                'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': text}]},
                'format': {'backgroundColor': color}
            }
        },
        'index': 0
    }})

# Performance column (H5:H300)
perf_rules = [
    ('On Time',  GREEN_BG),
    ('Late',     RED_BG),
    ('Overdue',  ORANGE_BG),
    ('On Track', BLUE_BG),
    ('No ETA',   GRAY_BG),
    ('N/A',      GRAY_BG),
]
for text, color in perf_rules:
    fmt_requests.append({'addConditionalFormatRule': {
        'rule': {
            'ranges': [{'sheetId': sheet_id, 'startRowIndex': 4, 'endRowIndex': 300, 'startColumnIndex': 7, 'endColumnIndex': 8}],
            'booleanRule': {
                'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': text}]},
                'format': {'backgroundColor': color}
            }
        },
        'index': 0
    }})

# Category column (D5:D300): Internal=indigo tint, External=terracotta tint
cat_rules = [
    ('Internal', {'red': 0.87, 'green': 0.84, 'blue': 0.93}),
    ('External', {'red': 0.93, 'green': 0.87, 'blue': 0.84}),
]
for text, color in cat_rules:
    fmt_requests.append({'addConditionalFormatRule': {
        'rule': {
            'ranges': [{'sheetId': sheet_id, 'startRowIndex': 4, 'endRowIndex': 300, 'startColumnIndex': 3, 'endColumnIndex': 4}],
            'booleanRule': {
                'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': text}]},
                'format': {'backgroundColor': color}
            }
        },
        'index': 0
    }})

# Alternating row colors for results
fmt_requests.append({'addBanding': {
    'bandedRange': {
        'range': {'sheetId': sheet_id, 'startRowIndex': 3, 'endRowIndex': 300, 'startColumnIndex': 0, 'endColumnIndex': 8},
        'rowProperties': {
            'headerColor': DARK_HEADER,
            'firstBandColor': WHITE,
            'secondBandColor': {'red': 0.97, 'green': 0.97, 'blue': 0.98},
        }
    }
}})

# ── 7. Execute formatting ──────────────────────────────────────────────
print(f"Applying {len(fmt_requests)} formatting requests...")
sheets.spreadsheets().batchUpdate(
    spreadsheetId=KPI_SPREADSHEET_ID,
    body={'requests': fmt_requests}
).execute()

print(f"\n✓ '{TAB_NAME}' built successfully!")
print(f"  • Dropdowns: TSA ({len(TSA_NAMES)}), Week (dynamic from DB_Data), Section ({len(SECTIONS)})")
print(f"  • Default: THIAGO / All sections")
print(f"  • FILTER formula auto-updates when dropdowns change")
print(f"  • Conditional formatting: Status (3), Performance (6), Category (2)")
print(f"\n  Open the KPI spreadsheet and go to the '{TAB_NAME}' tab.")
