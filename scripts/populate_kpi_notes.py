#!/usr/bin/env python3
"""Populate KPI cells with hover notes showing offender/task details.

Reads DB_Data, matches tasks to each KPI cell, and writes Google Sheets notes
so that hovering a cell reveals WHY a number is what it is.
"""
import os, sys
sys.stdout.reconfigure(line_buffering=True, encoding='utf-8', errors='replace')
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

KPI_SPREADSHEET_ID = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w'

# DB column indices (0-based)
TSA, WEEK, FOCUS, STATUS, DEMAND_TYPE, CATEGORY, CUSTOMER, DATE_ADD, ETA, DD, PERF = range(11)

# Sheet name → DB name
NAME_TO_DB = {
    'Thiago': 'THIAGO', 'Diego': 'DIEGO', 'Gabrielle': 'GABI',
    'Carlos': 'CARLOS', 'Alexandra': 'ALEXANDRA',
    'Thais': 'THAIS', 'Yasmim': 'YASMIM',
}

# Section types and their DB filters + note logic
# 'delivery' → On Time vs Late (offenders), percentage
# 'throughput' → Done tasks, count
# 'overdue' → Overdue tasks, count
# 'count' → All tasks in category, count
# 'wip' → In Progress tasks, count

TABS = {
    'Thiago Calculations': {
        'num_people': 5,
        'name_col': 4,        # column D (1-indexed)
        'week_row': 3,        # 1-indexed sheet row with week range strings
        'first_data_col': 5,  # 1-indexed (column E)
        'sections': [
            {'name': 'Internal Delivery', 'start_row': 6,  'type': 'delivery', 'category': 'Internal'},
            {'name': 'External Delivery', 'start_row': 13, 'type': 'delivery', 'category': 'External'},
            {'name': 'Throughput',        'start_row': 20, 'type': 'throughput'},
            {'name': 'Overdue',           'start_row': 27, 'type': 'overdue'},
            {'name': 'WIP',               'start_row': 34, 'type': 'wip'},
            {'name': 'Internal Tasks',    'start_row': 41, 'type': 'count', 'category': 'Internal'},
            {'name': 'External Tasks',    'start_row': 48, 'type': 'count', 'category': 'External'},
        ]
    },
    'Thais Calculations': {
        'num_people': 2,
        'name_col': 4,
        'week_row': 3,
        'first_data_col': 5,
        'sections': [
            {'name': 'Internal Delivery', 'start_row': 6,  'type': 'delivery', 'category': 'Internal'},
            {'name': 'External Delivery', 'start_row': 10, 'type': 'delivery', 'category': 'External'},
            {'name': 'Throughput',        'start_row': 14, 'type': 'throughput'},
            {'name': 'Overdue',           'start_row': 18, 'type': 'overdue'},
            {'name': 'WIP',               'start_row': 22, 'type': 'wip'},
            {'name': 'Internal Tasks',    'start_row': 26, 'type': 'count', 'category': 'Internal'},
            {'name': 'External Tasks',    'start_row': 30, 'type': 'count', 'category': 'External'},
        ]
    }
}

MAX_TASKS_IN_NOTE = 12  # truncate after this many


# ── Note builders ───────────────────────────────────────────────────────

def _trunc(s, n=35):
    s = str(s or '')
    return (s[:n-1] + '…') if len(s) > n else s


def _task_line(task, show_status=False, show_eta=False):
    """Format a single task line for a note."""
    parts = [f"• {_trunc(task[FOCUS])}"]
    if task[CUSTOMER]:
        parts.append(f"[{_trunc(task[CUSTOMER], 15)}]")
    if show_status and task[STATUS]:
        parts.append(f"({task[STATUS]})")
    if show_eta and task[ETA]:
        parts.append(f"ETA: {task[ETA]}")
    return ' '.join(parts)


def build_delivery_note(tasks, category):
    """Delivery section: only show note when there are Late offenders (< 100%)."""
    matching = [t for t in tasks
                if t[CATEGORY] == category and t[PERF] in ('On Time', 'Late')]
    if not matching:
        return None

    late = [t for t in matching if t[PERF] == 'Late']
    if not late:
        return None  # 100% On Time → no note needed

    on_time_count = len(matching) - len(late)
    total = len(matching)

    lines = [f"⚠ {len(late)} Late ({on_time_count}/{total} On Time)"]
    for t in late[:MAX_TASKS_IN_NOTE]:
        detail = f"• {_trunc(t[FOCUS])}"
        if t[CUSTOMER]:
            detail += f" [{_trunc(t[CUSTOMER], 15)}]"
        if t[ETA] or t[DD]:
            detail += f"\n  ETA: {t[ETA] or '?'} → Del: {t[DD] or '?'}"
        lines.append(detail)

    return '\n'.join(lines)


def build_throughput_note(tasks):
    """Throughput: show note when below target (<5 Done tasks)."""
    done = [t for t in tasks if t[STATUS] == 'Done']
    total_tasks = len(tasks)
    done_count = len(done)

    if done_count >= 5:
        return None  # On target → no note needed

    if done_count == 0:
        # Check if there were tasks at all
        if total_tasks == 0:
            return None  # No tasks assigned → no note
        in_progress = [t for t in tasks if t[STATUS] == 'In Progress']
        lines = [f"⚠ 0 deliveries ({total_tasks} tasks assigned)"]
        if in_progress:
            lines.append(f"  {len(in_progress)} still In Progress:")
            for t in in_progress[:MAX_TASKS_IN_NOTE]:
                lines.append(_task_line(t, show_eta=True))
        return '\n'.join(lines)

    # 1-4 deliveries: show what was done
    lines = [f"⚠ {done_count} deliveries (target: 5)"]
    for t in done[:MAX_TASKS_IN_NOTE]:
        lines.append(_task_line(t))
    if len(done) > MAX_TASKS_IN_NOTE:
        lines.append(f"  … +{len(done) - MAX_TASKS_IN_NOTE} more")
    return '\n'.join(lines)


def build_overdue_note(tasks):
    """Overdue: all tasks are offenders."""
    overdue = [t for t in tasks if t[PERF] == 'Overdue']
    if not overdue:
        return None
    lines = [f"⚠ Overdue: {len(overdue)} tasks"]
    for t in overdue[:MAX_TASKS_IN_NOTE]:
        lines.append(_task_line(t, show_eta=True))
    if len(overdue) > MAX_TASKS_IN_NOTE:
        lines.append(f"  … +{len(overdue) - MAX_TASKS_IN_NOTE} more")
    return '\n'.join(lines)


def build_count_note(tasks, category):
    """Count section: no note needed — not a deviation metric."""
    return None


def build_wip_note(tasks):
    """WIP: show which tasks are In Progress."""
    wip = [t for t in tasks if t[STATUS] == 'In Progress']
    if not wip:
        return None
    lines = [f"📋 {len(wip)} In Progress:"]
    for t in wip[:MAX_TASKS_IN_NOTE]:
        lines.append(_task_line(t, show_eta=True))
    if len(wip) > MAX_TASKS_IN_NOTE:
        lines.append(f"  … +{len(wip) - MAX_TASKS_IN_NOTE} more")
    return '\n'.join(lines)


def build_note(section, tasks):
    """Dispatch to the right builder based on section type."""
    sec_type = section['type']
    if sec_type == 'delivery':
        return build_delivery_note(tasks, section['category'])
    elif sec_type == 'throughput':
        return build_throughput_note(tasks)
    elif sec_type == 'overdue':
        return build_overdue_note(tasks)
    elif sec_type == 'count':
        return build_count_note(tasks, section['category'])
    elif sec_type == 'wip':
        return build_wip_note(tasks)
    return None


# ── Main ────────────────────────────────────────────────────────────────

def main():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    sheets = build('sheets', 'v4', credentials=creds)

    # 1. Get sheet IDs
    meta = sheets.spreadsheets().get(spreadsheetId=KPI_SPREADSHEET_ID).execute()
    sheet_ids = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

    # 2. Read DB_Data
    print("Reading DB_Data...")
    db_raw = sheets.spreadsheets().values().get(
        spreadsheetId=KPI_SPREADSHEET_ID,
        range='DB_Data!A2:K'
    ).execute().get('values', [])

    # Pad short rows and index by (tsa_upper, week)
    db_index = {}
    for row in db_raw:
        while len(row) < 11:
            row.append('')
        key = (row[TSA].upper().strip(), row[WEEK].strip())
        if key[0] and key[1]:  # skip rows with empty TSA or week
            db_index.setdefault(key, []).append(row)
    print(f"  {len(db_raw)} rows, {len(db_index)} unique (TSA, week) combos")

    total_notes = 0

    for tab_name, tab_cfg in TABS.items():
        if tab_name not in sheet_ids:
            print(f"  SKIP: '{tab_name}' not found")
            continue

        sid = sheet_ids[tab_name]
        num_people = tab_cfg['num_people']
        first_col = tab_cfg['first_data_col']  # 1-indexed
        name_col_letter = chr(64 + tab_cfg['name_col'])  # D

        # 3. Read actual names from column D of first section
        first_row = tab_cfg['sections'][0]['start_row']
        name_range = f"'{tab_name}'!{name_col_letter}{first_row}:{name_col_letter}{first_row + num_people - 1}"
        name_data = sheets.spreadsheets().values().get(
            spreadsheetId=KPI_SPREADSHEET_ID, range=name_range
        ).execute().get('values', [])
        names = [r[0] for r in name_data if r]
        print(f"  Names from sheet: {names}")

        # 4. Read week ranges from row 3 (E3:BI3 covers up to 57 weeks)
        week_range_str = f"'{tab_name}'!E3:BI3"
        week_data = sheets.spreadsheets().values().get(
            spreadsheetId=KPI_SPREADSHEET_ID,
            range=week_range_str
        ).execute().get('values', [[]])
        weeks = week_data[0] if week_data else []
        num_weeks = len(weeks)
        print(f"\n{tab_name}: {len(names)} people, {num_weeks} weeks")

        if not weeks:
            continue

        # 5. Build note requests
        requests = []
        tab_notes = 0

        for section in tab_cfg['sections']:
            for person_idx, person_name in enumerate(names):
                db_name = NAME_TO_DB.get(person_name, person_name.upper())
                row_1idx = section['start_row'] + person_idx  # 1-indexed sheet row
                row_0idx = row_1idx - 1  # 0-indexed for API

                # Build notes for each week column
                note_values = []
                for week_idx, week_str in enumerate(weeks):
                    week_str = week_str.strip()
                    key = (db_name, week_str)
                    tasks = db_index.get(key, [])

                    note = build_note(section, tasks) if tasks else None
                    note_values.append({'note': note or ''})

                    if note:
                        tab_notes += 1

                # One updateCells per person-row covering all week columns
                requests.append({
                    'updateCells': {
                        'rows': [{'values': note_values}],
                        'range': {
                            'sheetId': sid,
                            'startRowIndex': row_0idx,
                            'endRowIndex': row_0idx + 1,
                            'startColumnIndex': first_col - 1,  # 0-indexed
                            'endColumnIndex': first_col - 1 + num_weeks,
                        },
                        'fields': 'note'
                    }
                })

        # 5. Execute
        if requests:
            print(f"  Writing {len(requests)} row-updates ({tab_notes} notes)...")
            # Batch in chunks of 100 to stay within API limits
            for i in range(0, len(requests), 100):
                chunk = requests[i:i+100]
                sheets.spreadsheets().batchUpdate(
                    spreadsheetId=KPI_SPREADSHEET_ID,
                    body={'requests': chunk}
                ).execute()
            total_notes += tab_notes

    print(f"\n✓ {total_notes} notes written across all tabs.")
    print("  Hover any KPI data cell to see task details.")


if __name__ == '__main__':
    main()
