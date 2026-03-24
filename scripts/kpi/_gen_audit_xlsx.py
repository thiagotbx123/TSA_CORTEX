"""Generate audit XLSX from findings."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Audit Findings'

CRIT_FILL = PatternFill('solid', fgColor='FF0000')
HIGH_FILL = PatternFill('solid', fgColor='FF8C00')
MED_FILL = PatternFill('solid', fgColor='FFD700')
LOW_FILL = PatternFill('solid', fgColor='87CEEB')
HDR_FILL = PatternFill('solid', fgColor='1E293B')
HDR_FONT = Font(bold=True, color='FFFFFF', size=11)
BOLD = Font(bold=True)
WHITE_FONT = Font(bold=True, color='FFFFFF')
thin = Side(style='thin', color='D1D5DB')
border = Border(bottom=thin)

headers = ['ID', 'Severity', 'Category', 'Summary', 'File:Line', 'Recommendation', 'Confidence']
for col, h in enumerate(headers, 1):
    c = ws.cell(row=1, column=col, value=h)
    c.fill = HDR_FILL
    c.font = HDR_FONT
    c.alignment = Alignment(horizontal='center')

findings = [
    ('F01', 'CRITICAL', 'SECURITY', 'ngrok exposes entire Downloads folder publicly via stable URL with no auth', 'kpi_publish.bat:26', 'Change --directory to dedicated kpi-serve/ folder with only dashboard HTML', 'HIGH'),
    ('F02', 'CRITICAL', 'SECURITY', 'Stable ngrok URL hardcoded and committed - permanently known public endpoint', 'kpi_publish.bat:39', 'Use dynamic ngrok URL or add ngrok basic-auth', 'HIGH'),
    ('F03', 'HIGH', 'BUG', 'serve_kpi.py looks for RACCOONS_KPI_DASHBOARD.html but build writes KPI_DASHBOARD.html - 404', 'serve_kpi.py:25', 'Align filenames: change DASHBOARD_PATH to KPI_DASHBOARD.html', 'HIGH'),
    ('F04', 'HIGH', 'BUG', 'fetch_team_issues() references undefined QUERY instead of QUERY_TEAM - NameError if called', 'refresh_linear_cache.py:243', 'Replace QUERY with QUERY_TEAM or remove dead function', 'HIGH'),
    ('F05', 'HIGH', 'ERROR-HANDLING', 'fetch_issues_by_query() silently swallows all API errors - data loss with no diagnostic', 'refresh_linear_cache.py:451', 'Add print in except blocks; propagate ok=False clearly', 'HIGH'),
    ('F06', 'HIGH', 'ERROR-HANDLING', 'merge_opossum_data.py opens _dashboard_data.json with no error handling - crashes on first run', 'merge_opossum_data.py:158', 'Wrap in try/except FileNotFoundError with helpful message', 'HIGH'),
    ('F07', 'HIGH', 'BUG', 'orchestrate.py announces wrong output filename (RACCOONS vs KPI)', 'orchestrate.py:117', 'Change to KPI_DASHBOARD.html', 'HIGH'),
    ('F08', 'HIGH', 'CODE-QUALITY', 'Issue node parsing duplicated 3x across fetch functions (~240 lines)', 'refresh_linear_cache.py:265-515', 'Extract parse_issue_node() helper function', 'HIGH'),
    ('F09', 'HIGH', 'MAINTAINABILITY', 'build_html_dashboard.py is 1696-line monolith mixing Python+HTML/CSS/JS', 'build_html_dashboard.py:1-1696', 'Extract JS/CSS to template file; add JS syntax check step', 'HIGH'),
    ('F10', 'HIGH', 'TEST', 'Zero automated tests for any KPI calculation or data transformation', 'All files', 'Add pytest suite covering calc_perf, extract_history_fields, date_to_week', 'HIGH'),
    ('F11', 'HIGH', 'BUSINESS-LOGIC', 'D.LIE24 reassignedInReview flag may miss reassignment at In Progress to In Review transition', 'merge_opossum_data.py:119-123', 'Add check for assignment change in same event as In Review transition', 'MEDIUM'),
    ('F12', 'HIGH', 'BUSINESS-LOGIC', 'calc_perf_with_history uses originalEta - legitimately extended ETAs produce false Late', 'normalize_data.py:137', 'Make eta preference configurable; use finalEta when etaChanges documented', 'HIGH'),
    ('F13', 'MEDIUM', 'SECURITY', 'serve_kpi.py /refresh has CORS wildcard - any webpage can trigger pipeline rebuild', 'serve_kpi.py:73', 'Restrict CORS to http://localhost:PORT', 'HIGH'),
    ('F14', 'MEDIUM', 'SECURITY', 'LINEAR_API_KEY parsing does not strip inline comments', 'refresh_linear_cache.py:24', 'Use split("#")[0].strip() after split("=")', 'MEDIUM'),
    ('F15', 'MEDIUM', 'BUG', 'calc_perf in merge returns Overdue while normalize uses Late - semantic divergence', 'merge_opossum_data.py:288', 'Unify: change merge calc_perf to return Late', 'HIGH'),
    ('F16', 'MEDIUM', 'BUG', 'D.LIE23 original assignee: using fromAssigneeId instead of toAssigneeId inverts ownership', 'merge_opossum_data.py:110-114', 'Use toAssigneeId of first history event as original', 'MEDIUM'),
    ('F17', 'MEDIUM', 'CONFIGURATION', 'PERSON_MAP defined independently in merge and refresh - dual maintenance', 'merge_opossum_data.py:308', 'Extract shared team_config.json', 'HIGH'),
    ('F18', 'MEDIUM', 'CONFIGURATION', 'orchestrate.py subprocess timeout 120s may kill refresh mid-fetch', 'orchestrate.py:51', 'Increase to 300s for refresh step', 'MEDIUM'),
    ('F19', 'MEDIUM', 'INTEGRATION', 'History query hardcoded first:200 - tickets with >200 events silently truncate', 'refresh_linear_cache.py:95', 'Add pagination or increase limit; log warning at limit', 'HIGH'),
    ('F20', 'MEDIUM', 'BUSINESS-LOGIC', 'Week assignment uses day-of-month formula not ISO weeks - misaligned boundaries', 'merge_opossum_data.py:207', 'Use datetime.isocalendar() or document convention', 'HIGH'),
    ('F21', 'MEDIUM', 'OBSERVABILITY', 'Active tasks with future ETAs invisible in heatmaps (outside core weeks)', 'merge_opossum_data.py:429', 'Add tooltip or open items panel showing future-ETA work', 'HIGH'),
    ('F22', 'MEDIUM', 'DEPLOYMENT', 'netstat check for HTTP server may incorrectly report port state', 'kpi_publish.bat:23', 'Use more reliable port check or always kill+restart', 'MEDIUM'),
    ('F23', 'MEDIUM', 'ACCESSIBILITY', 'Collapse sections: no aria-expanded, no keyboard support', 'build_html_dashboard.py:1667', 'Add tabindex=0, role=button, aria-expanded, keydown handler', 'HIGH'),
    ('F24', 'MEDIUM', 'ACCESSIBILITY', 'Heatmap color coding has no text differentiation for color-blind users', 'build_html_dashboard.py:118', 'Add text labels or patterns inside heat cells', 'HIGH'),
    ('F25', 'MEDIUM', 'DEPENDENCIES', 'No requirements.txt - fresh install fails on requests import', 'refresh_linear_cache.py:10', 'Add requirements.txt with requests', 'HIGH'),
    ('F26', 'LOW', 'SECURITY', 'Hardcoded personal Windows path in JS clipboard fallback visible via ngrok', 'build_html_dashboard.py:510', 'Remove or parameterize the hardcoded path', 'HIGH'),
    ('F27', 'LOW', 'BUG', 'STATE_NAMES missing unknown workflow states - new states map to empty string silently', 'merge_opossum_data.py:24', 'Log warning on miss; add fallback to raw state name', 'HIGH'),
    ('F28', 'LOW', 'CODE-QUALITY', 'fetch_team_issues() is dead code - uses undefined var, never called', 'refresh_linear_cache.py:227', 'Remove function', 'HIGH'),
    ('F29', 'LOW', 'COMPLIANCE', 'ngrok exposes employee performance data without access controls', 'kpi_publish.bat:39', 'Add ngrok IP allowlist or basic auth', 'MEDIUM'),
    ('F30', 'LOW', 'DATA-INTEGRITY', 'Cache freshness not validated - stale cache used without warning', 'merge_opossum_data.py:178', 'Add timestamp check: warn if cache >24h old', 'HIGH'),
]

sev_fill = {'CRITICAL': CRIT_FILL, 'HIGH': HIGH_FILL, 'MEDIUM': MED_FILL, 'LOW': LOW_FILL}

for i, f in enumerate(findings, 2):
    for col, val in enumerate(f, 1):
        c = ws.cell(row=i, column=col, value=val)
        c.border = border
        c.alignment = Alignment(wrap_text=True, vertical='top')
    sev_cell = ws.cell(row=i, column=2)
    fill = sev_fill.get(f[1])
    if fill:
        sev_cell.fill = fill
        if f[1] == 'CRITICAL':
            sev_cell.font = WHITE_FONT

ws.column_dimensions['A'].width = 6
ws.column_dimensions['B'].width = 12
ws.column_dimensions['C'].width = 16
ws.column_dimensions['D'].width = 65
ws.column_dimensions['E'].width = 30
ws.column_dimensions['F'].width = 55
ws.column_dimensions['G'].width = 12

# Summary sheet
ws2 = wb.create_sheet('Summary')
ws2.cell(row=1, column=1, value='KPI Pipeline Audit Report').font = Font(bold=True, size=14)
ws2.cell(row=2, column=1, value=f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
ws2.cell(row=3, column=1, value='Target: Tools/TSA_CORTEX/scripts/kpi/')
ws2.cell(row=4, column=1, value='Engine: AUDIT_ENGINE v1.1 - 30 auditors, 3 layers')
ws2.cell(row=6, column=1, value='OVERALL HEALTH SCORE').font = BOLD
ws2.cell(row=6, column=2, value='58 / 100').font = Font(bold=True, size=14, color='FF8C00')
ws2.cell(row=7, column=1, value='Status: YELLOW - Functional but with significant issues')

stats = [('CRITICAL', 2, 'FF0000'), ('HIGH', 10, 'FF8C00'), ('MEDIUM', 13, 'FFD700'), ('LOW', 5, '87CEEB')]
ws2.cell(row=9, column=1, value='Severity').font = BOLD
ws2.cell(row=9, column=2, value='Count').font = BOLD
for i, (sev, cnt, color) in enumerate(stats, 10):
    ws2.cell(row=i, column=1, value=sev).fill = PatternFill('solid', fgColor=color)
    ws2.cell(row=i, column=2, value=cnt)
ws2.cell(row=14, column=1, value='Total').font = BOLD
ws2.cell(row=14, column=2, value=30).font = BOLD

ws2.cell(row=16, column=1, value='TOP 5 ACTION ITEMS').font = Font(bold=True, size=12)
actions = [
    ('1. Fix ngrok security - serve from dedicated folder, not entire Downloads', 'F01, F02, F29'),
    ('2. Fix filename mismatch - serve_kpi.py + orchestrate.py point to wrong name', 'F03, F07'),
    ('3. Fix silent API failure logging in refresh_linear_cache', 'F05'),
    ('4. Deduplicate issue node parser (~240 lines 3x)', 'F08'),
    ('5. Add minimum pytest suite for KPI calculations', 'F10'),
]
for i, (action, refs) in enumerate(actions, 17):
    ws2.cell(row=i, column=1, value=action)
    ws2.cell(row=i, column=2, value=refs).font = Font(color='4F46E5')

ws2.cell(row=23, column=1, value='CATEGORY SCORES').font = Font(bold=True, size=12)
cats = [
    ('Security', '35/100'), ('Error Handling', '50/100'), ('Code Quality', '55/100'),
    ('Data Integrity', '65/100'), ('Business Logic', '75/100'), ('Deployment', '50/100'),
    ('Tests', '10/100'), ('Maintainability', '50/100'),
]
for i, (cat, score) in enumerate(cats, 24):
    ws2.cell(row=i, column=1, value=cat)
    ws2.cell(row=i, column=2, value=score)

ws2.column_dimensions['A'].width = 65
ws2.column_dimensions['B'].width = 20

path = r'C:\Users\adm_r\Downloads\AUDIT_KPI_PIPELINE_2026-03-24.xlsx'
wb.save(path)
print(f'Saved: {path}')
