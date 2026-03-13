"""
Fix KPI Notes:
1. Add detailed formula explanation notes to each KPI header target cell (col D)
2. Clear stale warning notes (cells that meet target but still have warning)
"""
import requests
import json
from kpi_auth import get_access_token, KPI_SHEET as KPI, THIAGO_SID, THAIS_SID

access_token = get_access_token()

batch_requests = []


def add_note(sheet_id, row1, col1, note_text):
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


def clear_note(sheet_id, row0, col0):
    batch_requests.append({
        'updateCells': {
            'rows': [{'values': [{'note': ''}]}],
            'fields': 'note',
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row0,
                'endRowIndex': row0 + 1,
                'startColumnIndex': col0,
                'endColumnIndex': col0 + 1
            }
        }
    })


# ============================================================
# PART 1: Find and clear stale notes
# ============================================================
print("=== CHECKING STALE NOTES ===")

url = ('https://sheets.googleapis.com/v4/spreadsheets/{}?'
       'ranges=%27Thiago%20Calculations%27&ranges=%27Thais%20Calculations%27&'
       'fields=sheets(properties(sheetId,title),'
       'data(rowData(values(note,formattedValue,effectiveValue))))').format(KPI)
resp = requests.get(url, headers={'Authorization': 'Bearer ' + access_token})
sheets_data = resp.json()

stale_count = 0

for sheet in sheets_data['sheets']:
    sid = sheet['properties']['sheetId']
    title = sheet['properties']['title']

    if sid == THIAGO_SID:
        sections = [
            (5, 10, 'pct', 0.90),
            (12, 16, 'pct', 0.90),
            (19, 23, 'count_min', 5),
            (26, 30, 'count_max', 0),
            (32, 37, 'count_max', 3),
            (61, 66, 'pct', 0.90),
            (68, 73, 'pct', 0.90),
        ]
    else:
        sections = [
            (5, 6, 'pct', 0.90),
            (9, 10, 'pct', 0.90),
            (13, 14, 'count_min', 5),
            (17, 18, 'count_max', 0),
            (21, 22, 'count_max', 3),
            (37, 39, 'pct', 0.90),
            (41, 43, 'pct', 0.90),
        ]

    row_data = sheet.get('data', [{}])[0].get('rowData', [])

    for rd_idx, rd in enumerate(row_data):
        for c_idx, cell in enumerate(rd.get('values', [])):
            note = cell.get('note', '')
            if not note or not note.startswith('\u26a0'):
                continue

            ev = cell.get('effectiveValue', {})
            num_val = ev.get('numberValue', None)
            fv = cell.get('formattedValue', '')

            for ds_0, de_0, stype, target in sections:
                ds = ds_0 - 1  # convert to 0-indexed
                de = de_0 - 1
                if ds <= rd_idx <= de and c_idx >= 4:
                    should_clear = False
                    reason = ''

                    if stype == 'pct' and num_val is not None:
                        if num_val >= target:
                            should_clear = True
                            reason = 'val={} >= target {}'.format(fv, int(target*100))
                    elif stype == 'count_min' and num_val is not None:
                        if num_val >= target:
                            should_clear = True
                            reason = 'val={} >= target {}'.format(fv, target)
                    elif stype == 'count_max' and num_val is not None:
                        if num_val <= target:
                            should_clear = True
                            reason = 'val={} <= target {}'.format(fv, target)

                    if should_clear:
                        col_l = chr(65 + c_idx) if c_idx < 26 else chr(64 + c_idx // 26) + chr(65 + c_idx % 26)
                        print("  STALE: {} Row {} Col {}: {} | {}".format(
                            title[:7], rd_idx + 1, col_l, reason, note[:60]))
                        clear_note(sid, rd_idx, c_idx)
                        stale_count += 1
                    break

print("Found and clearing {} stale notes".format(stale_count))

# ============================================================
# PART 2: Add KPI formula explanation notes
# ============================================================
print("\n=== ADDING KPI FORMULA NOTES ===")

NOTE_INTERNAL = (
    "FORMULA: On Time / (On Time + Late)\n"
    "FILTRO: Demand Type = \"Internal\", Week Range match\n"
    "FONTE: DB_Data col E (Demand Type) + col K (Delivery Performance)\n"
    "TARGET: >90% \u2014 9 em cada 10 internas entregues no prazo\n"
    "COR: Verde >=90% | Amarelo 50-89% | Vermelho <50%"
)

NOTE_EXTERNAL = (
    "FORMULA: On Time / (On Time + Late)\n"
    "FILTRO: Demand Type = \"External\", Week Range match\n"
    "FONTE: DB_Data col E (Demand Type) + col K (Delivery Performance)\n"
    "TARGET: >90% \u2014 9 em cada 10 externas (cliente) no prazo\n"
    "COR: Verde >=90% | Amarelo 50-89% | Vermelho <50%"
)

NOTE_THROUGHPUT = (
    "FORMULA: COUNTIFS(Name, Week, Status=\"Done\")\n"
    "FONTE: DB_Data col D (Status)\n"
    "TARGET: >=5 entregas/semana por pessoa\n"
    "INTERPRETACAO: Mede vazao. <5 indica semana lenta ou tarefas complexas.\n"
    "COR: Verde >=5 | Amarelo 3-4 | Vermelho <3"
)

NOTE_OVERDUE = (
    "FORMULA: COUNTIFS(Name, Week, Delivery Performance=\"Overdue\")\n"
    "FONTE: DB_Data col K (Delivery Performance)\n"
    "TARGET: 0 \u2014 nenhuma tarefa atrasada aberta\n"
    "INTERPRETACAO: Tarefas abertas que passaram do ETA. Cada overdue = risco ativo.\n"
    "COR: Verde =0 | Vermelho >0"
)

NOTE_WIP = (
    "FORMULA: COUNTIFS(Name, Week, Status=\"In Progress\")\n"
    "FONTE: DB_Data col D (Status)\n"
    "TARGET: <=3 tarefas simultaneas\n"
    "INTERPRETACAO: WIP alto = sobrecarga ou falta de foco. Ideal: 2-3.\n"
    "NOTA: Inclui tarefas de qualquer tipo em andamento."
)

NOTE_INT_COUNT = (
    "FORMULA: COUNTIFS(Name, Week, Demand Type=\"Internal\")\n"
    "FONTE: DB_Data col E (Demand Type)\n"
    "TARGET: Monitoramento \u2014 sem meta fixa\n"
    "USO: Volume de demandas internas. Balancear carga interno vs externo."
)

NOTE_EXT_COUNT = (
    "FORMULA: COUNTIFS(Name, Week, Demand Type=\"External\")\n"
    "FONTE: DB_Data col E (Demand Type)\n"
    "TARGET: Monitoramento \u2014 sem meta fixa\n"
    "USO: Volume de demandas de cliente. Comparar com Internal Count."
)

NOTE_AVG_EXEC = (
    "FORMULA: AVERAGE(FILTER(Delivery Date - Date Add))\n"
    "FILTRO: Status=\"Done\", datas validas, duracao 0-60 dias\n"
    "FONTE: DB_Data col H (Date Add) + col J (Delivery Date)\n"
    "TARGET: Tendencia \u2014 menor e melhor\n"
    "INTERPRETACAO: Media de dias para completar. Exclui <0 (erro) e >60 (outlier).\n"
    "FORMATO: Decimal (3.5 = 3 dias e meio)"
)

NOTE_TIMELINE = (
    "FORMULA: COUNTIFS(\"On Time\") / COUNTIFS(\"On Time\" + \"Late\")\n"
    "FILTRO: Todas as tarefas (Internal + External combinado)\n"
    "FONTE: DB_Data col K (Delivery Performance) \u2014 usa labels\n"
    "TARGET: >90% \u2014 taxa geral de pontualidade\n"
    "NOTA: Nao filtra por Demand Type. Baseia-se nos labels da coluna K.\n"
    "COR: Verde >=90% | Amarelo 50-89% | Vermelho <50%"
)

NOTE_ETA_COMPLIANCE = (
    "FORMULA: COUNT(Done onde Delivery Date <= ETA) / COUNT(Done com ambas datas)\n"
    "FILTRO: Status=\"Done\", ETA e Delivery Date preenchidos\n"
    "FONTE: DB_Data col I (ETA) vs col J (Delivery Date) \u2014 compara datas reais\n"
    "TARGET: >90% \u2014 entrega dentro do prazo estimado\n"
    "DIFERENCIAL: Independe dos labels. Compara datas diretamente.\n"
    "COR: Verde >=90% | Amarelo 50-89% | Vermelho <50%"
)

# Thiago: header rows with target in D column
thiago_notes = {
    5: NOTE_INTERNAL,
    12: NOTE_EXTERNAL,
    19: NOTE_THROUGHPUT,
    26: NOTE_OVERDUE,
    33: NOTE_WIP,
    40: NOTE_INT_COUNT,
    47: NOTE_EXT_COUNT,
    54: NOTE_AVG_EXEC,
    61: NOTE_TIMELINE,
    68: NOTE_ETA_COMPLIANCE,
}

for row, note in thiago_notes.items():
    add_note(THIAGO_SID, row, 4, note)
print("  {} KPI notes -> Thiago Calculations (col D headers)".format(len(thiago_notes)))

# Thais: header rows
thais_notes = {
    5: NOTE_INTERNAL,
    9: NOTE_EXTERNAL,
    13: NOTE_THROUGHPUT,
    17: NOTE_OVERDUE,
    21: NOTE_WIP,
    25: NOTE_INT_COUNT,
    29: NOTE_EXT_COUNT,
    33: NOTE_AVG_EXEC,
    37: NOTE_TIMELINE,
    41: NOTE_ETA_COMPLIANCE,
}

for row, note in thais_notes.items():
    add_note(THAIS_SID, row, 4, note)
print("  {} KPI notes -> Thais Calculations (col D headers)".format(len(thais_notes)))

# ============================================================
# EXECUTE
# ============================================================
print("\nExecuting {} batchUpdate requests...".format(len(batch_requests)))
url = 'https://sheets.googleapis.com/v4/spreadsheets/{}:batchUpdate'.format(KPI)
resp = requests.post(url, headers={
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}, json={'requests': batch_requests})
print("Status: {}".format(resp.status_code))
if resp.status_code != 200:
    err = resp.json().get('error', {})
    print("Error: {}".format(err.get('message', '')))
else:
    print("OK!")

print("\nDone. {} KPI notes added, {} stale notes cleared.".format(
    len(thiago_notes) + len(thais_notes), stale_count))
