"""Rewrite MAP tab - simple table: Indicator | Formula | What it shows | Target."""
import requests
from kpi_auth import get_access_token, KPI_SHEET as KPI, MAP_SID

access_token = get_access_token()
headers_auth = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}

# ============================================================
# Content
# ============================================================
rows = [
    ['Indicator', 'Formula', 'What It Shows', 'Target'],
    [
        'S1 - Internal Accuracy',
        'On Time / (On Time + Late)\nDemand Category = "Internal"',
        'Whether internal tasks (process, automation, docs) are delivered on time. Shows "-" if no internal tasks that week.',
        '> 90%'
    ],
    [
        'S2 - External Accuracy',
        'On Time / (On Time + Late)\nDemand Category = "External"',
        'Whether customer-facing tasks are delivered on time. Separating from Internal helps spot if client work is being deprioritized.',
        '> 90%'
    ],
    [
        'S3 - Throughput',
        'COUNT(Status = "Done")',
        'How many tasks each person finishes per week. Low numbers may mean blockers, oversized tasks, or untracked work.',
        '>= 5/week'
    ],
    [
        'S4 - Overdue Snapshot',
        'COUNT(Performance = "Overdue")',
        'Tasks that are STILL OPEN past their deadline. Unlike Late (already delivered), Overdue = active risk needing immediate action.',
        '0'
    ],
    [
        'S5 - WIP',
        'COUNT(Status = "In Progress")',
        'How many tasks are open at the same time. High WIP = multitasking overload, slower delivery across the board.',
        '<= 3'
    ],
    [
        'S6 - Internal Count',
        'COUNT(Demand Category = "Internal")',
        'Volume of internal tasks. Helps balance internal vs external workload. No quality judgment, just volume.',
        'Monitor only'
    ],
    [
        'S7 - External Count',
        'COUNT(Demand Category = "External")',
        'Volume of customer tasks. Together with S6, shows where effort is going. Ideally most work is external (client value).',
        'Monitor only'
    ],
    [
        'S8 - Avg Execution Time',
        'AVERAGE(Delivery Date - Date Add)\nStatus = "Done", 0-60 day range',
        'Average days from task creation to delivery. Lower is better. Excludes outliers >60 days. Decimal format (3.5 = 3.5 days).',
        'Trend (lower = better)'
    ],
    [
        'S9 - Timeline Accuracy',
        'On Time / (On Time + Late)\nAll tasks combined (no type filter)',
        'Overall on-time rate for finished work. Does NOT count open Overdue tasks. Answers: "when we deliver, are we on time?"',
        '> 90%'
    ],
    [
        'S10 - Effective Delivery Rate',
        'On Time / (On Time + Late + Overdue)',
        'Stricter than S9. Includes open Overdue in denominator, penalizing backlogs. If S9 is high but S10 is low, overdue tasks are piling up.',
        '> 85%'
    ],
]

# ============================================================
# Clear + Write
# ============================================================
print('Clearing MAP tab...')
clear_url = 'https://sheets.googleapis.com/v4/spreadsheets/{}/values/MAP!A1:Z200:clear'.format(KPI)
requests.post(clear_url, headers=headers_auth)

# Also clear all formatting
requests.post(
    'https://sheets.googleapis.com/v4/spreadsheets/{}:batchUpdate'.format(KPI),
    headers=headers_auth,
    json={'requests': [{
        'repeatCell': {
            'range': {'sheetId': MAP_SID, 'startRowIndex': 0, 'endRowIndex': 200,
                      'startColumnIndex': 0, 'endColumnIndex': 10},
            'cell': {'userEnteredFormat': {}},
            'fields': 'userEnteredFormat'
        }
    }]}
)

print('Writing {} rows...'.format(len(rows)))
body = {
    'valueInputOption': 'RAW',
    'data': [{
        'range': 'MAP!A1:D{}'.format(len(rows)),
        'values': rows
    }]
}
resp = requests.post(
    'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchUpdate'.format(KPI),
    headers=headers_auth, json=body
)
print('Status: {}'.format(resp.status_code))

# ============================================================
# Simple formatting
# ============================================================
fmt_requests = []

# Header row: bold, dark bg, white text
fmt_requests.append({
    'repeatCell': {
        'range': {'sheetId': MAP_SID, 'startRowIndex': 0, 'endRowIndex': 1,
                  'startColumnIndex': 0, 'endColumnIndex': 4},
        'cell': {'userEnteredFormat': {
            'textFormat': {'bold': True, 'fontSize': 11,
                           'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
            'backgroundColor': {'red': 0.2, 'green': 0.25, 'blue': 0.35},
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'wrapStrategy': 'WRAP'
        }},
        'fields': 'userEnteredFormat'
    }
})

# Data rows: wrap, vertical top
fmt_requests.append({
    'repeatCell': {
        'range': {'sheetId': MAP_SID, 'startRowIndex': 1, 'endRowIndex': len(rows),
                  'startColumnIndex': 0, 'endColumnIndex': 4},
        'cell': {'userEnteredFormat': {
            'wrapStrategy': 'WRAP',
            'verticalAlignment': 'TOP',
            'textFormat': {'fontSize': 10}
        }},
        'fields': 'userEnteredFormat(wrapStrategy,verticalAlignment,textFormat.fontSize)'
    }
})

# Column A (Indicator): bold
fmt_requests.append({
    'repeatCell': {
        'range': {'sheetId': MAP_SID, 'startRowIndex': 1, 'endRowIndex': len(rows),
                  'startColumnIndex': 0, 'endColumnIndex': 1},
        'cell': {'userEnteredFormat': {
            'textFormat': {'bold': True}
        }},
        'fields': 'userEnteredFormat(textFormat.bold)'
    }
})

# Column widths
widths = [(0, 220), (1, 280), (2, 420), (3, 120)]
for col, px in widths:
    fmt_requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': MAP_SID, 'dimension': 'COLUMNS',
                      'startIndex': col, 'endIndex': col + 1},
            'properties': {'pixelSize': px},
            'fields': 'pixelSize'
        }
    })

# Light alternating row colors
for i in range(1, len(rows)):
    if i % 2 == 0:
        bg = {'red': 0.95, 'green': 0.96, 'blue': 0.98}
    else:
        bg = {'red': 1, 'green': 1, 'blue': 1}
    fmt_requests.append({
        'repeatCell': {
            'range': {'sheetId': MAP_SID, 'startRowIndex': i, 'endRowIndex': i + 1,
                      'startColumnIndex': 0, 'endColumnIndex': 4},
            'cell': {'userEnteredFormat': {'backgroundColor': bg}},
            'fields': 'userEnteredFormat(backgroundColor)'
        }
    })

# Freeze header
fmt_requests.append({
    'updateSheetProperties': {
        'properties': {'sheetId': MAP_SID,
                       'gridProperties': {'frozenRowCount': 1}},
        'fields': 'gridProperties.frozenRowCount'
    }
})

# Borders: thin border around all
fmt_requests.append({
    'updateBorders': {
        'range': {'sheetId': MAP_SID, 'startRowIndex': 0, 'endRowIndex': len(rows),
                  'startColumnIndex': 0, 'endColumnIndex': 4},
        'top': {'style': 'SOLID', 'color': {'red': 0.7, 'green': 0.7, 'blue': 0.7}},
        'bottom': {'style': 'SOLID', 'color': {'red': 0.7, 'green': 0.7, 'blue': 0.7}},
        'left': {'style': 'SOLID', 'color': {'red': 0.7, 'green': 0.7, 'blue': 0.7}},
        'right': {'style': 'SOLID', 'color': {'red': 0.7, 'green': 0.7, 'blue': 0.7}},
        'innerHorizontal': {'style': 'SOLID', 'color': {'red': 0.85, 'green': 0.85, 'blue': 0.85}},
        'innerVertical': {'style': 'SOLID', 'color': {'red': 0.85, 'green': 0.85, 'blue': 0.85}},
    }
})

resp2 = requests.post(
    'https://sheets.googleapis.com/v4/spreadsheets/{}:batchUpdate'.format(KPI),
    headers=headers_auth, json={'requests': fmt_requests}
)
print('Formatting: {}'.format(resp2.status_code))
print('Done!')
