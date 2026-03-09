#!/usr/bin/env python3
"""
Add 'Week Ref' column (e.g., JAN W.1, FEB W.2) to:
1. DB tab in TSA_Tasks_Consolidate (column L)
2. Update IMPORTRANGE in KPIS Raccoons to include new column (A:K → A:L)
"""
import os, re
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

DB_ID  = '1XaJgJCExt_dQ-RBY0eINP-0UCnCH7hYjGC3ibPlluzw'
KPI_ID = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w'

MONTH_ABBR = {
    1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
    7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'
}

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


def week_ref_from_range(week_range):
    """Convert '01/05 - 01/09/2026' → 'JAN W.1'"""
    if not week_range or not week_range.strip():
        return ''
    # Parse Monday date (first part: MM/DD)
    m = re.match(r'(\d{1,2})/(\d{1,2})\s*-\s*(\d{1,2})/(\d{1,2})/(\d{4})', week_range.strip())
    if not m:
        return ''
    month = int(m.group(1))
    day = int(m.group(2))
    abbr = MONTH_ABBR.get(month, f'M{month}')
    week_num = (day - 1) // 7 + 1
    return f'{abbr} W.{week_num}'


# --- Step 1: Read Week Range column from DB ---
print("Reading DB tab from TSA_Tasks_Consolidate...")
result = sh.values().get(spreadsheetId=DB_ID, range='DB!B:B').execute()
rows = result.get('values', [])
total = len(rows)
print(f"  {total} rows (including header)")

# Compute Week Ref for each row
week_refs = [['Week Ref']]  # Header
for i, row in enumerate(rows[1:], start=2):
    wr = row[0] if row else ''
    ref = week_ref_from_range(wr)
    week_refs.append([ref])

print(f"  Computed {len(week_refs)-1} Week Ref values")
# Show sample
samples = {}
for wr in week_refs[1:]:
    if wr[0]:
        samples[wr[0]] = samples.get(wr[0], 0) + 1
print(f"  Distribution: {dict(sorted(samples.items()))}")

# --- Step 2: Write Week Ref to column L in DB ---
print("\nWriting Week Ref to DB!L column...")
sh.values().update(
    spreadsheetId=DB_ID,
    range=f'DB!L1:L{total}',
    valueInputOption='RAW',
    body={'values': week_refs}
).execute()
print("  Done")

# --- Step 3: Update DB filter to include column L ---
print("\nUpdating DB filter to include column L...")
sp = sh.get(spreadsheetId=DB_ID).execute()
db_sheet_id = None
for s in sp['sheets']:
    if s['properties']['title'] == 'DB':
        db_sheet_id = s['properties']['sheetId']
        break

if db_sheet_id is not None:
    # Remove existing filter and re-create with expanded range
    reqs = []
    # Try to remove existing filter first
    reqs.append({'clearBasicFilter': {'sheetId': db_sheet_id}})
    try:
        sh.batchUpdate(spreadsheetId=DB_ID, body={'requests': reqs}).execute()
    except Exception:
        pass  # No filter to clear

    # Create new filter including column L (12 columns: A-L, indices 0-11)
    reqs = [{'setBasicFilter': {'filter': {
        'range': {
            'sheetId': db_sheet_id,
            'startRowIndex': 0,
            'endRowIndex': total,
            'startColumnIndex': 0,
            'endColumnIndex': 12  # A through L
        }
    }}}]
    sh.batchUpdate(spreadsheetId=DB_ID, body={'requests': reqs}).execute()
    print("  Filter updated (A:L)")

    # Format header L1
    reqs = [{'repeatCell': {
        'range': {'sheetId': db_sheet_id,
                  'startRowIndex': 0, 'endRowIndex': 1,
                  'startColumnIndex': 11, 'endColumnIndex': 12},
        'cell': {'userEnteredFormat': {
            'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
            'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1},
                           'bold': True},
            'horizontalAlignment': 'CENTER'
        }},
        'fields': 'userEnteredFormat'
    }}]
    sh.batchUpdate(spreadsheetId=DB_ID, body={'requests': reqs}).execute()
    print("  Header L1 formatted")
else:
    print("  WARNING: DB sheet not found")

# --- Step 4: Update IMPORTRANGE in KPIS Raccoons DB_Data ---
print("\nUpdating IMPORTRANGE in KPIS Raccoons (A:K to A:L)...")
sh.values().update(
    spreadsheetId=KPI_ID,
    range='DB_Data!A1',
    valueInputOption='USER_ENTERED',
    body={'values': [[f'=IMPORTRANGE("{DB_ID}","DB!A:L")']]
}).execute()
print("  IMPORTRANGE updated to DB!A:L")

print("\n=== DONE ===")
print("Column L 'Week Ref' added to DB tab in TSA_Tasks_Consolidate")
print("IMPORTRANGE updated in KPIS Raccoons to include new column")
print("Both spreadsheets now have filterable Week Ref (JAN W.1, FEB W.2, etc.)")
