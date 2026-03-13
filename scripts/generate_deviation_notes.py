"""
Generate deviation warning notes for S8 (Avg Exec), S9 (Timeline), S10 (Effective Rate).
Matches the style of existing S1-S5 notes: task name, customer, ETA, delivery date.
"""
import requests
from kpi_auth import get_access_token, KPI_SHEET as KPI, THIAGO_SID, THAIS_SID

access_token = get_access_token()
h = {'Authorization': 'Bearer ' + access_token}
headers_auth = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}

# ============================================================
# 1. Read all DB_Data + week headers
# ============================================================
r = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchGet'.format(KPI),
    headers=h,
    params={
        'ranges': [
            'DB_Data!A2:K1000',
            'Thiago Calculations!E3:BI3',
            'Thiago Calculations!D55:D59',  # Avg Exec names
            'Thiago Calculations!D62:D66',  # Timeline names
            'Thiago Calculations!D69:D73',  # Effective names
            # Current values to check deviations
            'Thiago Calculations!E55:BI59',  # Avg Exec values
            'Thiago Calculations!E62:BI66',  # Timeline values
            'Thiago Calculations!E69:BI73',  # Effective values
            # Thais
            'Thais Calculations!D34:D35',    # Avg Exec names
            'Thais Calculations!D38:D39',    # Timeline names
            'Thais Calculations!D42:D43',    # Effective names
            'Thais Calculations!E34:BI35',   # Avg Exec values
            'Thais Calculations!E38:BI39',   # Timeline values
            'Thais Calculations!E42:BI43',   # Effective values
        ],
        'valueRenderOption': 'FORMATTED_VALUE'
    }
).json()

db_rows = r['valueRanges'][0].get('values', [])
weeks = r['valueRanges'][1].get('values', [[]])[0]

# Thiago names
t_avg_names = [row[0] for row in r['valueRanges'][2].get('values', [])]
t_tl_names = [row[0] for row in r['valueRanges'][3].get('values', [])]
t_eff_names = [row[0] for row in r['valueRanges'][4].get('values', [])]

t_avg_vals = r['valueRanges'][5].get('values', [])
t_tl_vals = r['valueRanges'][6].get('values', [])
t_eff_vals = r['valueRanges'][7].get('values', [])

# Thais names
th_avg_names = [row[0] for row in r['valueRanges'][8].get('values', [])]
th_tl_names = [row[0] for row in r['valueRanges'][9].get('values', [])]
th_eff_names = [row[0] for row in r['valueRanges'][10].get('values', [])]

th_avg_vals = r['valueRanges'][11].get('values', [])
th_tl_vals = r['valueRanges'][12].get('values', [])
th_eff_vals = r['valueRanges'][13].get('values', [])

# ============================================================
# 2. Build lookup: (NAME_UPPER, week) -> list of tasks
# ============================================================
# DB columns: A=TSA, B=Week, C=Focus, D=Status, E=DemandType, F=Category, G=Customer, H=DateAdd, I=ETA, J=DelivDate, K=Perf
tasks = {}
for row in db_rows:
    if len(row) < 4:
        continue
    name = row[0]  # already UPPER
    week = row[1]
    focus = row[2] if len(row) > 2 else ''
    status = row[3] if len(row) > 3 else ''
    customer = row[6] if len(row) > 6 else ''
    date_add = row[7] if len(row) > 7 else ''
    eta = row[8] if len(row) > 8 else ''
    deliv = row[9] if len(row) > 9 else ''
    perf = row[10] if len(row) > 10 else ''

    key = (name, week)
    if key not in tasks:
        tasks[key] = []
    tasks[key].append({
        'focus': focus, 'status': status, 'customer': customer,
        'date_add': date_add, 'eta': eta, 'deliv': deliv, 'perf': perf
    })

# Name mapping: sheet name -> DB name
def to_db_name(sheet_name):
    if sheet_name == 'Gabrielle':
        return 'GABI'
    return sheet_name.upper()


# ============================================================
# 3. Generate notes
# ============================================================
batch_requests = []
note_count = 0


def add_note(sheet_id, row1, col1, note_text):
    global note_count
    batch_requests.append({
        'updateCells': {
            'rows': [{'values': [{'note': note_text}]}],
            'fields': 'note',
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row1 - 1,
                'endRowIndex': row1,
                'startColumnIndex': col1 - 1,
                'endColumnIndex': col1
            }
        }
    })
    note_count += 1


def truncate(s, max_len=45):
    return s[:max_len] + '...' if len(s) > max_len else s


def generate_notes_for_section(sheet_id, names, values, start_row, section_type):
    """
    section_type: 'avg_exec', 'timeline', 'effective'
    start_row: first data row (1-indexed)
    """
    for pi, name in enumerate(names):
        db_name = to_db_name(name)
        row_vals = values[pi] if pi < len(values) else []

        for wi, week in enumerate(weeks):
            col = wi + 5  # E=5
            val_str = row_vals[wi] if wi < len(row_vals) else '-'

            if val_str == '-' or val_str == '':
                continue

            key = (db_name, week)
            task_list = tasks.get(key, [])

            if section_type == 'avg_exec':
                # Flag if avg > 7 days
                try:
                    val = float(val_str)
                except ValueError:
                    continue
                if val <= 7:
                    continue

                # Find the slow tasks (Done with dates)
                slow = []
                for t in task_list:
                    if t['status'] == 'Done' and t['date_add'] and t['deliv']:
                        try:
                            # Approx duration from string dates
                            slow.append(t)
                        except:
                            pass

                if slow:
                    lines = ['\u26a0 Avg {:.1f} days (target: <7)'.format(val)]
                    for t in slow[:5]:
                        cust = ' [{}]'.format(t['customer']) if t['customer'] else ''
                        lines.append('\u2022 {}{}'.format(truncate(t['focus']), cust))
                        lines.append('  Add: {} \u2192 Del: {}'.format(t['date_add'], t['deliv']))
                    note_text = '\n'.join(lines)
                    add_note(sheet_id, start_row + pi, col, note_text)

            elif section_type == 'timeline':
                # Flag if < 90%
                try:
                    val_str_clean = val_str.replace('%', '')
                    val = float(val_str_clean) / 100
                except ValueError:
                    continue
                if val >= 0.9:
                    continue

                # Find Late tasks
                late_tasks = [t for t in task_list if t['perf'] == 'Late']
                on_time = sum(1 for t in task_list if t['perf'] == 'On Time')

                if late_tasks:
                    lines = ['\u26a0 {} Late ({}/{} On Time)'.format(
                        len(late_tasks), on_time, on_time + len(late_tasks))]
                    for t in late_tasks[:5]:
                        cust = ' [{}]'.format(t['customer']) if t['customer'] else ''
                        lines.append('\u2022 {}{}'.format(truncate(t['focus']), cust))
                        lines.append('  ETA: {} \u2192 Del: {}'.format(t['eta'], t['deliv']))
                    note_text = '\n'.join(lines)
                    add_note(sheet_id, start_row + pi, col, note_text)

            elif section_type == 'effective':
                # Flag if < 85%
                try:
                    val_str_clean = val_str.replace('%', '')
                    val = float(val_str_clean) / 100
                except ValueError:
                    continue
                if val >= 0.85:
                    continue

                late_tasks = [t for t in task_list if t['perf'] == 'Late']
                overdue_tasks = [t for t in task_list if t['perf'] == 'Overdue']
                on_time = sum(1 for t in task_list if t['perf'] == 'On Time')
                total = on_time + len(late_tasks) + len(overdue_tasks)

                if late_tasks or overdue_tasks:
                    lines = ['\u26a0 {}/{} On Time ({} Late, {} Overdue)'.format(
                        on_time, total, len(late_tasks), len(overdue_tasks))]
                    if late_tasks:
                        lines.append('Late:')
                        for t in late_tasks[:3]:
                            cust = ' [{}]'.format(t['customer']) if t['customer'] else ''
                            lines.append('\u2022 {}{}'.format(truncate(t['focus']), cust))
                            lines.append('  ETA: {} \u2192 Del: {}'.format(t['eta'], t['deliv']))
                    if overdue_tasks:
                        lines.append('Overdue:')
                        for t in overdue_tasks[:4]:
                            cust = ' [{}]'.format(t['customer']) if t['customer'] else ''
                            lines.append('\u2022 {}{} ETA: {}'.format(
                                truncate(t['focus']), cust, t['eta']))
                    note_text = '\n'.join(lines)
                    add_note(sheet_id, start_row + pi, col, note_text)


# ============================================================
# 4. Generate for Thiago
# ============================================================
print('Generating notes for Thiago Calculations...')
generate_notes_for_section(THIAGO_SID, t_avg_names, t_avg_vals, 55, 'avg_exec')
generate_notes_for_section(THIAGO_SID, t_tl_names, t_tl_vals, 62, 'timeline')
generate_notes_for_section(THIAGO_SID, t_eff_names, t_eff_vals, 69, 'effective')
print('  Thiago: {} notes'.format(note_count))

thiago_count = note_count

# ============================================================
# 5. Generate for Thais
# ============================================================
print('Generating notes for Thais Calculations...')
generate_notes_for_section(THAIS_SID, th_avg_names, th_avg_vals, 34, 'avg_exec')
generate_notes_for_section(THAIS_SID, th_tl_names, th_tl_vals, 38, 'timeline')
generate_notes_for_section(THAIS_SID, th_eff_names, th_eff_vals, 42, 'effective')
print('  Thais: {} notes'.format(note_count - thiago_count))

# ============================================================
# 6. Push
# ============================================================
if batch_requests:
    print('\nPushing {} notes...'.format(len(batch_requests)))
    # Split into chunks of 100 (API limit)
    for i in range(0, len(batch_requests), 100):
        chunk = batch_requests[i:i+100]
        url = 'https://sheets.googleapis.com/v4/spreadsheets/{}:batchUpdate'.format(KPI)
        resp = requests.post(url, headers=headers_auth, json={'requests': chunk})
        print('  Chunk {}-{}: {}'.format(i, i+len(chunk), resp.status_code))
        if resp.status_code != 200:
            print('  Error: {}'.format(resp.json().get('error', {}).get('message', '')))
else:
    print('No deviation notes needed.')

print('\nDone! {} total notes generated.'.format(note_count))
