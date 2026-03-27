"""Generate KPI Pipeline Audit v3 XLSX — 2026-03-26."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

OUTPUT = r'C:\Users\adm_r\Downloads\AUDIT_KPI_PIPELINE_V3_2026-03-26.xlsx'

# ── Styles ───────────────────────────────────────────────────────────────────
CRIT_FILL = PatternFill('solid', fgColor='DC2626')   # red
HIGH_FILL = PatternFill('solid', fgColor='F97316')   # orange
MED_FILL  = PatternFill('solid', fgColor='FDE047')   # yellow
LOW_FILL  = PatternFill('solid', fgColor='BAE6FD')   # light blue
HDR_FILL  = PatternFill('solid', fgColor='1E293B')   # dark slate
GREEN_FILL = PatternFill('solid', fgColor='DCFCE7')  # light green

HDR_FONT    = Font(bold=True, color='FFFFFF', size=11, name='Calibri')
WHITE_FONT  = Font(bold=True, color='FFFFFF', name='Calibri')
BOLD_FONT   = Font(bold=True, name='Calibri')
BASE_FONT   = Font(name='Calibri')
TITLE_FONT  = Font(bold=True, size=16, name='Calibri', color='1E293B')
H2_FONT     = Font(bold=True, size=12, name='Calibri', color='1E293B')
SCORE_FONT  = Font(bold=True, size=22, name='Calibri', color='D97706')  # amber

thin = Side(style='thin', color='CBD5E1')
BORDER = Border(top=thin, left=thin, bottom=thin, right=thin)
BTM    = Border(bottom=Side(style='thin', color='E2E8F0'))

SEV_FILL = {
    'CRITICAL': CRIT_FILL,
    'HIGH':     HIGH_FILL,
    'MEDIUM':   MED_FILL,
    'LOW':      LOW_FILL,
}

# ── Findings data ─────────────────────────────────────────────────────────────
FINDINGS = [
    ('C01','CRITICAL','SECURITY',
     'ngrok stable URL publicly committed, no auth',
     'kpi_publish.bat:46',
     'Add --basic-auth or rotate URL',
     'HIGH'),
    ('C02','CRITICAL','SECURITY',
     'Gantt tooltip data-tip XSS — tHtml not escaped before attribute embedding',
     'build_html_dashboard.py:1774',
     'Use esc(tHtml) before data-tip',
     'HIGH'),
    ('H01','HIGH','BUG',
     'calc_perf returns Overdue in merge but Late in normalize — semantic divergence',
     'merge_opossum_data.py:288',
     'Unify to Late',
     'HIGH'),
    ('H02','HIGH','BUG',
     'D.LIE23 original assignee logic may invert on immediate-assign tickets',
     'merge_opossum_data.py:107-114',
     'Add test coverage',
     'MEDIUM'),
    ('H04','HIGH','ERROR-HANDLING',
     'merge opens _dashboard_data.json with no FileNotFoundError handling',
     'merge_opossum_data.py:158',
     'Add try/except',
     'HIGH'),
    ('H05','HIGH','ERROR-HANDLING',
     'Partial fetch on timeout silently replaces good cache',
     'refresh_linear_cache.py:304-323',
     'Compare count before save',
     'HIGH'),
    ('H06','HIGH','BUSINESS-LOGIC',
     'originalEta preference causes false Late for legitimately extended ETAs',
     'normalize_data.py:140',
     'Use finalEta when etaChanges>=1',
     'HIGH'),
    ('H07','HIGH','INFRASTRUCTURE',
     'python -m http.server exposes directory listing via ngrok',
     'kpi_publish.bat:32-38',
     'Use serve_kpi.py instead',
     'MEDIUM'),
    ('H08','HIGH','INFRASTRUCTURE',
     'orchestrate --build-only uses numeric index STEPS[3] — fragile',
     'orchestrate.py:91',
     'Reference by name',
     'MEDIUM'),
    ('H10','HIGH','PERFORMANCE',
     'Full rebuild of ALL tabs on every filter change — 500K iterations',
     'build_html_dashboard.py:1552-1573',
     'Per-tab lazy rendering',
     'MEDIUM'),
    ('H11','HIGH','CONFIGURATION',
     'No requirements.txt — fresh install fails',
     'All files',
     'Create requirements.txt',
     'HIGH'),
    ('H12','HIGH','BUG',
     'Activity tab renderTrend uses accuracy bar breakdown instead of done/open',
     'build_html_dashboard.py:886-900',
     "Add barMode==='activity' branch",
     'HIGH'),
    ('H13','HIGH','SECURITY',
     'serve_kpi.py CORS wildcard allows any webpage to trigger pipeline refresh',
     'serve_kpi.py:73',
     'Restrict to localhost',
     'HIGH'),
    ('M01','MEDIUM','SECURITY',
     "API key parsing doesn't strip inline comments",
     'refresh_linear_cache.py:24',
     "Add split('#')[0].strip()",
     'MEDIUM'),
    ('M02','MEDIUM','SECURITY',
     'Personal Windows path exposed in HTML error message',
     'build_html_dashboard.py:616',
     'Replace with generic message',
     'MEDIUM'),
    ('M05','MEDIUM','BUSINESS-LOGIC',
     'Week formula uses custom day-of-month not ISO weeks',
     'merge_opossum_data.py:207',
     'Document or switch to ISO',
     'LOW'),
    ('M06','MEDIUM','BUSINESS-LOGIC',
     'admin-close detection Pattern 2 may misclassify same-day tickets',
     'normalize_data.py:391-395',
     'Add not-started guard',
     'MEDIUM'),
    ('M08','MEDIUM','DATA-INTEGRITY',
     'No cache freshness validation — stale data used silently',
     'merge_opossum_data.py:178',
     'Add mtime check',
     'MEDIUM'),
    ('M09','MEDIUM','DATA-INTEGRITY',
     'Dedup uses first 40 chars — collision risk',
     'normalize_data.py:422-436',
     'Increase to 60 chars or use ticketId',
     'MEDIUM'),
    ('M11','MEDIUM','INFRASTRUCTURE',
     'orchestrate timeout 120s too short for refresh step',
     'orchestrate.py:51',
     'Increase to 600s',
     'HIGH'),
    ('M12','MEDIUM','ACCESSIBILITY',
     'No keyboard support on collapse sections',
     'build_html_dashboard.py:316',
     'Add role/tabindex/aria-expanded',
     'MEDIUM'),
    ('M13','MEDIUM','ACCESSIBILITY',
     'Heatmap color coding only — no text differentiation',
     'build_html_dashboard.py:118',
     'Add symbols',
     'LOW'),
    ('M14','MEDIUM','CODE-QUALITY',
     'PERSON_MAP defined in 2 files independently',
     'merge/refresh',
     'Extract shared config',
     'HIGH'),
    ('M15','MEDIUM','CODE-QUALITY',
     'Unknown STATE_NAMES map to empty string silently',
     'merge_opossum_data.py:88',
     'Add logging',
     'MEDIUM'),
    ('M16','MEDIUM','CODE-QUALITY',
     '2088-line monolith mixing Python+HTML/CSS/JS',
     'build_html_dashboard.py',
     'Extract template',
     'LOW'),
    ('M17','MEDIUM','INFRASTRUCTURE',
     'netstat port check unreliable',
     'kpi_publish.bat:30',
     'Use curl liveness probe',
     'MEDIUM'),
    ('M18','MEDIUM','DATA-INTEGRITY',
     'Zero issues from API not caught as error',
     'refresh_linear_cache.py:372',
     'Log ERROR + non-zero exit',
     'HIGH'),
    ('L07','LOW','BUG',
     '${BUILD_DATE} unrendered in Guide modal — shows as literal text',
     'build_html_dashboard.py:1542',
     'Add to replace chain',
     'MEDIUM'),
]

# ── What's working (I01-I10) ──────────────────────────────────────────────────
WORKING = [
    ('I01', 'Linear API integration with pagination works reliably for standard issue fetch'),
    ('I02', 'History extraction correctly captures ETA changes, state transitions, and assignee changes'),
    ('I03', 'D.LIE scoring engine covers 6 distinct lie dimensions with clear threshold logic'),
    ('I04', 'Gantt chart rendering handles multi-week spans and color-codes by performance tier'),
    ('I05', 'Filter system (person / week / state) correctly narrows all computed tables'),
    ('I06', 'Heatmap generation correctly aggregates weekly on-time rates per person'),
    ('I07', 'orchestrate.py provides single-command full-pipeline execution'),
    ('I08', 'serve_kpi.py /refresh endpoint enables remote pipeline trigger without SSH'),
    ('I09', 'Cache-first architecture reduces API calls and allows offline dashboard viewing'),
    ('I10', 'Collapse sections provide clean progressive disclosure of detail rows'),
]

# ── Top 10 action items ───────────────────────────────────────────────────────
ACTIONS = [
    ('1', 'C01+C02', 'SECURITY',  'Rotate ngrok URL, add basic-auth; escape tHtml before data-tip attribute'),
    ('2', 'H13+M01', 'SECURITY',  'Restrict CORS to localhost; strip inline comments from API key parsing'),
    ('3', 'H04+H05', 'ERROR-HANDLING', 'Add FileNotFoundError guard on JSON open; compare cache count before save'),
    ('4', 'H11',     'CONFIG',    'Create requirements.txt with pinned versions'),
    ('5', 'H01+H12', 'BUG',       'Unify perf label to Late; fix Activity tab bar breakdown logic'),
    ('6', 'H06',     'BUSINESS-LOGIC', 'Use finalEta when etaChanges >= 1 to avoid false Late'),
    ('7', 'M14',     'CODE-QUALITY',   'Extract shared PERSON_MAP to team_config.json'),
    ('8', 'M08+M18', 'DATA-INTEGRITY', 'Add mtime freshness check; error on zero-issue API response'),
    ('9', 'H10',     'PERFORMANCE',    'Implement per-tab lazy rendering to avoid 500K-iteration rebuilds'),
    ('10','M11',     'INFRA',     'Raise orchestrate refresh timeout from 120s to 600s'),
]

# ── Category scores ───────────────────────────────────────────────────────────
CAT_SCORES = [
    ('Security',        30, 100, 'DC2626'),
    ('Error Handling',  55, 100, 'F97316'),
    ('Bug Quality',     60, 100, 'F97316'),
    ('Business Logic',  65, 100, 'FDE047'),
    ('Data Integrity',  60, 100, 'F97316'),
    ('Infrastructure',  65, 100, 'FDE047'),
    ('Performance',     55, 100, 'F97316'),
    ('Accessibility',   45, 100, 'F97316'),
    ('Code Quality',    60, 100, 'F97316'),
    ('Configuration',   55, 100, 'F97316'),
]


def apply_all_borders(ws, row, ncols):
    for col in range(1, ncols + 1):
        ws.cell(row=row, column=col).border = BORDER


def set_row_fill(ws, row, ncols, fill):
    for col in range(1, ncols + 1):
        ws.cell(row=row, column=col).fill = fill


def build_findings_sheet(wb):
    ws = wb.active
    ws.title = 'Findings'
    ws.freeze_panes = 'A2'

    headers = ['ID', 'Severity', 'Category', 'Summary', 'File:Line', 'Recommendation', 'Confidence']
    col_widths = [6, 12, 18, 60, 28, 55, 12]

    # Header row
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=col, value=h)
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.alignment = Alignment(horizontal='center', vertical='center')
        c.border = BORDER
    ws.row_dimensions[1].height = 20

    # Data rows
    for r, f in enumerate(FINDINGS, 2):
        sev = f[1]
        fill = SEV_FILL.get(sev)
        for col, val in enumerate(f, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.border = BORDER
            c.alignment = Alignment(wrap_text=True, vertical='top')
            c.font = BASE_FONT
        # Severity cell colouring
        sev_cell = ws.cell(row=r, column=2)
        if fill:
            sev_cell.fill = fill
        if sev == 'CRITICAL':
            sev_cell.font = WHITE_FONT
        elif sev in ('HIGH', 'MEDIUM', 'LOW'):
            sev_cell.font = BOLD_FONT
        # Light row shading for readability
        for col in (1, 3, 4, 5, 6, 7):
            cell = ws.cell(row=r, column=col)
            if r % 2 == 0:
                cell.fill = PatternFill('solid', fgColor='F8FAFC')

    # Column widths
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w

    # Auto row heights (approx)
    for r in range(2, len(FINDINGS) + 2):
        ws.row_dimensions[r].height = 40

    return ws


def build_summary_sheet(wb):
    ws = wb.create_sheet('Summary')

    def cell(row, col, value, font=None, fill=None, align=None):
        c = ws.cell(row=row, column=col, value=value)
        if font:  c.font = font
        if fill:  c.fill = fill
        if align: c.alignment = align
        return c

    # ── Title block ────────────────────────────────────────────────────────
    ws.merge_cells('A1:G1')
    c = ws.cell(row=1, column=1, value='KPI Pipeline Audit v3')
    c.font = TITLE_FONT
    c.alignment = Alignment(horizontal='left', vertical='center')
    c.fill = PatternFill('solid', fgColor='F1F5F9')
    ws.row_dimensions[1].height = 30

    ws.merge_cells('A2:G2')
    c2 = ws.cell(row=2, column=1, value='Date: 2026-03-26   |   Target: Tools/TSA_CORTEX/scripts/kpi/')
    c2.font = Font(name='Calibri', size=10, color='64748B')
    c2.fill = PatternFill('solid', fgColor='F1F5F9')

    # ── Overall score ──────────────────────────────────────────────────────
    ws.row_dimensions[4].height = 28
    cell(4, 1, 'OVERALL HEALTH SCORE', font=H2_FONT)
    cell(4, 2, '67 / 100', font=SCORE_FONT,
         align=Alignment(horizontal='center', vertical='center'))
    cell(4, 3, 'YELLOW', font=Font(bold=True, color='D97706', name='Calibri', size=13),
         align=Alignment(horizontal='center', vertical='center'))
    ws.merge_cells('D4:G4')
    cell(4, 4, 'Functional but with significant security and reliability gaps.',
         font=Font(italic=True, name='Calibri', color='475569'))

    # ── Severity counts ────────────────────────────────────────────────────
    ws.row_dimensions[6].height = 18
    cell(6, 1, 'SEVERITY BREAKDOWN', font=H2_FONT)

    hdr_row = 7
    for col, h in enumerate(['Severity', 'Count', 'Share'], 1):
        c = ws.cell(row=hdr_row, column=col, value=h)
        c.font = HDR_FONT
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal='center')
        c.border = BORDER

    total = len(FINDINGS)
    sev_counts = [
        ('CRITICAL', 2,  CRIT_FILL, WHITE_FONT),
        ('HIGH',     12, HIGH_FILL, BOLD_FONT),
        ('MEDIUM',   13, MED_FILL,  BOLD_FONT),
        ('LOW',      1,  LOW_FILL,  BOLD_FONT),
    ]
    for i, (sev, cnt, sfill, sfont) in enumerate(sev_counts, hdr_row + 1):
        c1 = ws.cell(row=i, column=1, value=sev)
        c1.fill = sfill; c1.font = sfont; c1.border = BORDER
        c1.alignment = Alignment(horizontal='center')
        c2 = ws.cell(row=i, column=2, value=cnt)
        c2.font = BOLD_FONT; c2.border = BORDER
        c2.alignment = Alignment(horizontal='center')
        c3 = ws.cell(row=i, column=3, value=f'{cnt/total*100:.0f}%')
        c3.border = BORDER
        c3.alignment = Alignment(horizontal='center')

    total_row = hdr_row + len(sev_counts) + 1
    ws.cell(row=total_row, column=1, value='TOTAL').font = BOLD_FONT
    ws.cell(row=total_row, column=1).alignment = Alignment(horizontal='center')
    ws.cell(row=total_row, column=2, value=total).font = BOLD_FONT
    ws.cell(row=total_row, column=2).alignment = Alignment(horizontal='center')
    for col in range(1, 4):
        ws.cell(row=total_row, column=col).border = BORDER

    # ── Category scores ────────────────────────────────────────────────────
    cat_start = total_row + 2
    cell(cat_start, 1, 'CATEGORY SCORES', font=H2_FONT)
    hcat = cat_start + 1
    for col, h in enumerate(['Category', 'Score', 'Out of', 'Grade'], 1):
        c = ws.cell(row=hcat, column=col, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL
        c.alignment = Alignment(horizontal='center')
        c.border = BORDER

    for i, (cat, score, out_of, color) in enumerate(CAT_SCORES, hcat + 1):
        pct = score / out_of
        grade = 'A' if pct >= .9 else 'B' if pct >= .8 else 'C' if pct >= .7 else 'D' if pct >= .6 else 'F'
        cfill = PatternFill('solid', fgColor=color)
        ws.cell(row=i, column=1, value=cat).border = BORDER
        ws.cell(row=i, column=2, value=score).border = BORDER
        ws.cell(row=i, column=2).alignment = Alignment(horizontal='center')
        ws.cell(row=i, column=3, value=out_of).border = BORDER
        ws.cell(row=i, column=3).alignment = Alignment(horizontal='center')
        gc = ws.cell(row=i, column=4, value=grade)
        gc.border = BORDER; gc.fill = cfill
        gc.alignment = Alignment(horizontal='center')
        if color in ('DC2626', 'F97316'):
            gc.font = Font(bold=True, color='FFFFFF', name='Calibri')
        else:
            gc.font = BOLD_FONT

    # ── Top 10 action items ────────────────────────────────────────────────
    act_start = hcat + len(CAT_SCORES) + 2
    cell(act_start, 1, 'TOP 10 ACTION ITEMS', font=H2_FONT)
    hact = act_start + 1
    for col, h in enumerate(['#', 'Finding(s)', 'Category', 'Action'], 1):
        c = ws.cell(row=hact, column=col, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL
        c.alignment = Alignment(horizontal='center')
        c.border = BORDER

    for i, (num, refs, cat, action) in enumerate(ACTIONS, hact + 1):
        ws.cell(row=i, column=1, value=num).border = BORDER
        ws.cell(row=i, column=1).alignment = Alignment(horizontal='center')
        rc = ws.cell(row=i, column=2, value=refs)
        rc.border = BORDER
        rc.font = Font(color='4F46E5', bold=True, name='Calibri')
        rc.alignment = Alignment(horizontal='center')
        ws.cell(row=i, column=3, value=cat).border = BORDER
        ac = ws.cell(row=i, column=4, value=action)
        ac.border = BORDER
        ac.alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 30

    # ── What's working well ────────────────────────────────────────────────
    good_start = hact + len(ACTIONS) + 2
    cell(good_start, 1, "WHAT'S WORKING WELL", font=H2_FONT)
    hgood = good_start + 1
    for col, h in enumerate(['ID', 'Observation'], 1):
        c = ws.cell(row=hgood, column=col, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL
        c.border = BORDER
        c.alignment = Alignment(horizontal='center')

    for i, (iid, obs) in enumerate(WORKING, hgood + 1):
        ic = ws.cell(row=i, column=1, value=iid)
        ic.fill = GREEN_FILL; ic.border = BORDER
        ic.font = Font(bold=True, color='166534', name='Calibri')
        ic.alignment = Alignment(horizontal='center')
        oc = ws.cell(row=i, column=2, value=obs)
        oc.fill = GREEN_FILL; oc.border = BORDER
        oc.alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 22

    # ── Column widths ──────────────────────────────────────────────────────
    ws.column_dimensions['A'].width = 18
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 65
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12

    return ws


# ── Build workbook ────────────────────────────────────────────────────────────
wb = openpyxl.Workbook()
build_findings_sheet(wb)
build_summary_sheet(wb)

wb.save(OUTPUT)
print(f'Saved: {OUTPUT}')
print(f'Findings sheet: {len(FINDINGS)} rows')
print(f'Summary sheet: top-10 actions + {len(WORKING)} strengths + {len(CAT_SCORES)} category scores')
