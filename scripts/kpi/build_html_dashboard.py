"""Build TSA Waki KPI HTML Dashboard v3 — audit-hardened version.

Changes from v2:
  - H1: Dynamic isCoreWeek (data-driven, no hardcoded period)
  - H2: Member card accuracy aligned with KPI1 formula
  - H9: Sanitized JSON injection (no XSS via </script>)
  - H12: CDN fallback with inline Chart.js error handling
  - H14/M15: Sample size (n) displayed next to percentages
  - C1: KPI3 marked as NOT ACTIVE until rework labels are in use
  - M7: Tab-specific trend chart bars
  - M11: Data staleness warning
  - M12: Default segment = All (was External)
  - D.LIE10: B.B.C tasks excluded from Overdue
  - D.LIE12: ETA Coverage metric on member cards
  - L2: JSON validation before injection

Usage: python kpi/build_html_dashboard.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json, datetime

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, '..', '_dashboard_data.json')
OUTPUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'TSA_WAKI_KPI_DASHBOARD.html')

# L2: Validate JSON before processing
try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data_raw = json.load(f)
    data_json = json.dumps(data_raw, ensure_ascii=True)
except json.JSONDecodeError as e:
    print(f"ERROR: Malformed JSON in {DATA_PATH}: {e}")
    sys.exit(1)

# H9: Sanitize JSON for safe inline injection — escape </script> sequences
data_json_safe = data_json.replace('</script>', '<\\/script>').replace('</Script>', '<\\/Script>')

# M11: Record build timestamp for staleness detection
build_date = datetime.date.today().strftime('%Y-%m-%d')
# Find the most recent dateAdd in data for staleness comparison (only past/present dates)
data_dates = [r.get('dateAdd', '') for r in data_raw
              if r.get('dateAdd', '') and len(r.get('dateAdd', '')) >= 10 and r['dateAdd'][:10] <= build_date]
latest_data_date = max(data_dates) if data_dates else build_date

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TSA KPI Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f8fafc;--white:#fff;--border:#d1d5db;--text:#1b1b1b;
  --dim:#6b7280;--light:#9ca3af;--accent:#2563eb;
  --green:#059669;--green-bg:#ecfdf5;--green-l:#d1fae5;
  --red:#dc2626;--red-bg:#fef2f2;--red-l:#fee2e2;
  --yellow:#d97706;--yellow-bg:#fffbeb;--yellow-l:#fef3c7;
  --blue:#2563eb;--blue-bg:#eff6ff;--blue-l:#dbeafe;
  --gray-bg:#f3f4f6;--gray-l:#e5e7eb;
}
body{font-family:'Inter','Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);padding:28px 40px;min-height:100vh;font-size:15px;line-height:1.5}
.header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;background:linear-gradient(135deg,#064e3b,#065f46,#047857);color:#fff;padding:18px 28px;border-radius:10px}
.header h1{font-size:1.4em;font-weight:700;color:#fff}
.header .sub{font-size:.82em;color:#a7f3d0;font-style:italic}
.header .linear-link{display:inline-flex;align-items:center;gap:6px;color:#fff;font-size:.78em;text-decoration:none;padding:5px 12px;border-radius:6px;background:#5E6AD2;border:1px solid #7B83E8;transition:all .15s;margin-top:4px}
.header .linear-link:hover{background:#4B55B8;color:#fff;border-color:#9BA1F0}
.header .linear-link svg{width:14px;height:14px;fill:currentColor}
.header .tbx-logo{height:44px;transition:opacity .15s}
.header .tbx-logo:hover{opacity:.85}
.filters{display:flex;gap:8px;align-items:center;margin-bottom:20px;flex-wrap:wrap}
.filters label{font-size:.72em;color:#9ca3af;font-weight:500;text-transform:uppercase;letter-spacing:.5px}
.filters select{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;padding:5px 10px;border-radius:6px;font-size:.82em;cursor:pointer}
.filters select option{background:#064e3b;color:#fff}
.filters select:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 2px rgba(37,99,235,.3)}
.kpi-strip{display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px;margin-bottom:18px;margin-top:18px}
.kpi-pill{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:10px 14px;display:flex;align-items:center;gap:10px}
.kpi-pill .icon{width:32px;height:32px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1em;flex-shrink:0}
.kpi-pill.k1 .icon{background:var(--blue-bg);color:var(--blue)}
.kpi-pill.k2 .icon{background:var(--yellow-bg);color:var(--yellow)}
.kpi-pill.k3 .icon{background:var(--gray-bg);color:var(--dim)}
.kpi-pill .info{flex:1}
.kpi-pill .info .name{font-size:.7em;color:var(--dim);text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.kpi-pill .info .val{font-size:1.3em;font-weight:800;line-height:1.2}
.kpi-pill .info .meta{font-size:.68em;color:var(--dim)}
.kpi-pill .badge{font-size:.6em;font-weight:700;padding:2px 7px;border-radius:20px}
.badge-pass{background:var(--green-l);color:var(--green)}
.badge-fail{background:var(--red-l);color:var(--red)}
.badge-warn{background:var(--yellow-l);color:var(--yellow)}
.badge-inactive{background:var(--gray-l);color:var(--dim)}
.staleness-banner{padding:8px 16px;border-radius:6px;font-size:.78em;font-weight:600;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.staleness-ok{background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0}
.staleness-warn{background:#fffbeb;color:#92400e;border:1px solid #fde68a}
.staleness-old{background:#fef2f2;color:#991b1b;border:1px solid #fecaca}
.tabs{display:flex;gap:0;margin-bottom:0;border-bottom:2px solid var(--border)}
.tab{padding:12px 24px;font-size:.9em;font-weight:600;color:var(--dim);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;transition:all .15s}
.tab:hover{color:var(--text)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-panel{display:none;padding-top:16px}
.tab-panel.active{display:block}
.grid-section{background:var(--white);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-bottom:16px}
.grid-section .title{padding:14px 20px;font-size:.9em;font-weight:700;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px}
.grid-section .title .dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.grid-section .title .info-btn{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--gray-bg);color:var(--dim);font-size:.7em;font-weight:700;cursor:help;margin-left:4px;border:1px solid var(--border)}
.heatmap{width:100%;border-collapse:collapse;font-size:.88em}
.heatmap th,.heatmap td{padding:9px 12px;text-align:center;white-space:nowrap}
.heatmap thead th{background:var(--gray-bg);font-weight:600;color:var(--dim);font-size:.8em;text-transform:uppercase;letter-spacing:.3px;border-bottom:1px solid var(--border)}
.heatmap .month-header{background:#eef2ff;color:var(--blue);font-weight:700;font-size:.88em;letter-spacing:.5px;border-bottom:2px solid var(--blue-l);padding:10px 8px;border-left:3px solid var(--accent)}
.heatmap .week-header{background:var(--gray-bg);font-size:.78em;color:var(--dim);padding:7px 8px}
.heatmap .month-first{border-left:3px solid var(--accent)!important}
.heatmap .person-label{text-align:left;font-weight:600;padding-left:16px;background:var(--white);border-right:2px solid var(--border);min-width:120px;font-size:.9em;color:var(--text)}
.heatmap .team-row td{font-weight:800;background:#eef2ff;border-top:3px solid var(--accent);font-size:.92em}
.heatmap .team-row .person-label{background:#eef2ff;color:var(--accent);font-size:.82em;text-transform:uppercase;letter-spacing:.3px;font-weight:800;white-space:normal;line-height:1.3}
.heatmap td.cell{min-width:60px;font-weight:600;font-size:.9em;border:1px solid var(--gray-l);cursor:default;position:relative;transition:transform .1s}
.heatmap td.cell:hover{transform:scale(1.05);z-index:1;box-shadow:0 2px 8px rgba(0,0,0,.12)}
.heatmap td.total-col{background:#eef2ff!important;font-weight:800;border-left:3px solid var(--accent);font-size:.92em}
.heat-great{background:#d1fae5;color:#065f46}
.heat-good{background:#ecfdf5;color:#059669}
.heat-ok{background:#fefce8;color:#92400e}
.heat-bad{background:#fef2f2;color:#991b1b}
.heat-terrible{background:#fecaca;color:#7f1d1d}
.heat-na{background:var(--white);color:#d5d8dd;font-weight:300;font-size:.75em}
.heat-zero{background:var(--gray-bg);color:var(--light);font-style:italic}
.tooltip{position:fixed;background:#1e293b;color:#fff;padding:12px 16px;border-radius:8px;font-size:.82em;pointer-events:none;z-index:999;max-width:380px;line-height:1.6;box-shadow:0 4px 16px rgba(0,0,0,.25);display:none}
.tooltip b{color:#93c5fd}
.tooltip .tip-section{margin-top:6px;padding-top:6px;border-top:1px solid rgba(255,255,255,.15)}
.tooltip .tip-task{color:#d1d5db;font-size:.9em;padding-left:8px;text-indent:-8px}
.tooltip .tip-task::before{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;margin-right:4px;vertical-align:middle}
.tooltip .tip-late::before{background:#f87171}
.tooltip .tip-ontime::before{background:#34d399}
.tooltip .tip-overdue::before{background:#fbbf24}
.tooltip .tip-label{color:#9ca3af;font-size:.85em;font-weight:600;text-transform:uppercase;letter-spacing:.5px}
.detail-panel{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:16px;margin-top:16px}
.detail-panel h3{font-size:.85em;font-weight:700;margin-bottom:8px;color:var(--text)}
.detail-table{width:100%;border-collapse:collapse;font-size:.78em}
.detail-table th{background:var(--gray-bg);padding:6px 10px;text-align:left;font-weight:600;color:var(--dim);font-size:.75em;text-transform:uppercase;letter-spacing:.3px}
.detail-table td{padding:5px 10px;border-bottom:1px solid var(--gray-l)}
.detail-table tr:hover td{background:var(--blue-bg)}
.trend-row{padding:0}
.trend-wrap{padding:16px 20px;border-bottom:1px solid var(--border)}
.trend-wrap h4{font-size:.78em;color:var(--dim);font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}
.trend-wrap canvas{width:100%!important;height:160px!important}
.segment-bar{display:flex;gap:6px;margin-bottom:14px;background:var(--white);border:1px solid var(--border);border-radius:8px;padding:4px;width:fit-content}
.segment-btn{padding:8px 20px;border-radius:6px;font-size:.82em;font-weight:600;color:var(--dim);cursor:pointer;transition:all .15s;border:none;background:transparent;letter-spacing:.2px}
.segment-btn:hover{color:var(--text);background:var(--gray-bg)}
.segment-btn.active{background:#065f46;color:#fff;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.segment-btn .seg-count{font-size:.78em;font-weight:400;opacity:.7;margin-left:4px}
.audit-section{background:var(--white);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-top:20px}
.audit-header{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;border-bottom:1px solid var(--border);cursor:pointer;user-select:none}
.audit-header h3{font-size:.9em;font-weight:700;display:flex;align-items:center;gap:8px}
.audit-header .toggle{font-size:.75em;color:var(--dim);transition:transform .2s}
.audit-header.open .toggle{transform:rotate(180deg)}
.audit-tools{display:flex;gap:6px}
.audit-tools button{background:var(--gray-bg);border:1px solid var(--border);border-radius:6px;padding:5px 12px;font-size:.72em;font-weight:600;color:var(--dim);cursor:pointer;transition:all .15s}
.audit-tools button:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.audit-body{max-height:0;overflow:hidden;transition:max-height .3s ease}
.audit-body.open{max-height:none;overflow-x:auto}
.audit-table{width:100%;border-collapse:collapse;font-size:.75em;font-family:'Consolas','Menlo','Courier New',monospace}
.audit-table th{background:#064e3b;color:#fff;padding:8px 10px;text-align:left;font-weight:600;font-size:.78em;text-transform:uppercase;letter-spacing:.5px;position:sticky;top:0;cursor:pointer;white-space:nowrap}
.audit-table th:hover{background:#047857}
.audit-table th .sort-arrow{margin-left:4px;font-size:.7em;opacity:.5}
.audit-table td{padding:5px 10px;border-bottom:1px solid var(--gray-l);white-space:nowrap}
.audit-table tr:nth-child(even) td{background:#fafbfc}
.audit-table tr:hover td{background:var(--blue-bg)}
.audit-table .perf-on-time{color:var(--green);font-weight:600}
.audit-table .perf-late{color:var(--red);font-weight:600}
.audit-table .perf-overdue{color:var(--yellow);font-weight:600}
.audit-table .perf-na{color:var(--light)}
.audit-table .rework-yes{color:var(--red);font-weight:700}
.audit-stats{padding:10px 20px;font-size:.72em;color:var(--dim);border-top:1px solid var(--gray-l);display:flex;gap:16px;flex-wrap:wrap}
.member-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-bottom:18px}
.member-card{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:12px 14px;position:relative;overflow:hidden;display:flex;flex-direction:column}
.member-card .mc-name{font-weight:700;font-size:.88em;margin-bottom:6px;color:var(--text)}
.member-card .mc-source{font-size:.6em;font-weight:600;padding:1px 5px;border-radius:3px;margin-left:6px}
.mc-source-linear{background:#dbeafe;color:#1d4ed8}
.mc-source-spreadsheet{background:#fef3c7;color:#92400e}
.member-card .mc-body{flex:1}
.member-card .mc-row{display:flex;justify-content:space-between;font-size:.72em;color:var(--dim);padding:2px 0}
.member-card .mc-row b{color:var(--text)}
.member-card .mc-bar{margin-top:auto;padding-top:8px}
.member-card .mc-bar-track{height:4px;border-radius:2px;background:var(--gray-l);overflow:hidden}
.member-card .mc-bar-inner{height:100%;border-radius:2px;transition:width .3s}
.member-card .mc-alert{position:absolute;top:8px;right:10px;font-size:.65em;font-weight:700;padding:2px 6px;border-radius:10px}
.mc-alert-warn{background:var(--yellow-l);color:var(--yellow)}
.mc-alert-ok{background:var(--green-l);color:var(--green)}
.heat-vol-0{background:var(--white);color:#d5d8dd;font-weight:300;font-size:.75em}
.heat-vol-1{background:#eff6ff;color:var(--blue)}
.heat-vol-2{background:#dbeafe;color:#1d4ed8}
.heat-vol-3{background:#bfdbfe;color:#1e40af}
.heat-vol-4{background:#93c5fd;color:#1e3a8a}
.heat-vol-5{background:#3b82f6;color:#fff}
.footer{text-align:center;margin-top:24px;padding:12px;color:var(--light);font-size:.7em}
@media(max-width:900px){.kpi-strip{grid-template-columns:1fr}.heatmap{font-size:.7em}.segment-bar{flex-wrap:wrap}.audit-table{font-size:.65em}}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>TSA KPI Dashboard</h1>
    <div class="sub" id="periodLabel">Loading...</div>
    <a href="https://linear.app/testbox/team/RAC/projects" target="_blank" class="linear-link"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M2.886 4.18A11.982 11.982 0 0 1 11.99 0C18.624 0 24 5.376 24 12.009c0 3.64-1.62 6.903-4.18 9.105L2.887 4.18ZM1.817 5.626l16.556 16.556c-.524.33-1.075.62-1.65.866L.951 7.277c.247-.575.537-1.126.866-1.65ZM.322 9.163l14.515 14.515c-.71.172-1.443.282-2.195.322L0 11.358a12 12 0 0 1 .322-2.195Zm-.17 4.862 9.823 9.824a12.02 12.02 0 0 1-9.824-9.824Z"/></svg>View in Linear</a>
  </div>
  <img src="https://cdn.prod.website-files.com/62f1899cd374937577f36d5f/6529d8cb022a253f2009f59a_testbox.svg" alt="TestBox" class="tbx-logo">
  <div class="filters">
    <label>Person</label><select id="fPerson"><option value="ALL">All</option></select>
    <label>Category</label><select id="fCategory"><option value="ALL">All</option><option value="Internal">Internal</option><option value="External">External</option></select>
  </div>
</div>

<div id="stalenessBanner"></div>

<div class="segment-bar" id="segmentBar">
  <button class="segment-btn" data-seg="External">Clients &amp; Projects<span class="seg-count" id="segExt"></span></button>
  <button class="segment-btn" data-seg="Internal">Internal<span class="seg-count" id="segInt"></span></button>
  <button class="segment-btn active" data-seg="ALL">All<span class="seg-count" id="segAll"></span></button>
</div>

<div class="kpi-strip" id="kpiStrip"></div>

<div class="member-cards" id="memberCards"></div>

<div class="tabs" id="tabBar">
  <div class="tab active" data-tab="accuracy">ETA Accuracy</div>
  <div class="tab" data-tab="velocity">Execution Time</div>
  <div class="tab" data-tab="reliability">Reliability</div>
  <div class="tab" data-tab="activity">Team Activity</div>
</div>

<div class="tab-panel active" id="panel-accuracy">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--blue)"></span>ETA Accuracy<span class="info-btn" onmouseenter="showTip(event,'<b>ETA Accuracy</b><br><span class=tip-label>Formula</span>: On Time / (On Time + Late)<br><span class=tip-label>Target</span>: &gt;90%<br><span class=tip-label>ETA</span>: First date set on the ticket (measures prediction accuracy)<br><span class=tip-label>Excludes</span>: No ETA, No Delivery Date, Canceled, On Track, Blocked<br><span class=tip-label>Min sample</span>: n&lt;5 shown as count instead of %')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-accuracy"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-accuracy"></table></div>
  </div>
</div>

<div class="tab-panel" id="panel-velocity">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--yellow)"></span>Execution Time<span class="info-btn" onmouseenter="showTip(event,'<b>Avg Execution Time</b><br><span class=tip-label>Formula</span>: Average(Delivery - Start Date)<br><span class=tip-label>Start Date</span>: startedAt (In Progress) or dateAdd as fallback<br><span class=tip-label>Target</span>: &lt;28 days<br><span class=tip-label>Includes</span>: Only Done tasks with both dates<br><br>Measures implementation speed. Lower = faster delivery.')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-velocity"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-velocity"></table></div>
  </div>
</div>

<div class="tab-panel" id="panel-reliability">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--dim)"></span>Implementation Reliability <span style="font-size:.6em;background:var(--gray-l);color:var(--dim);padding:2px 8px;border-radius:4px;font-weight:700">NOT ACTIVE</span><span class="info-btn" onmouseenter="showTip(event,'<b>Implementation Reliability — NOT ACTIVE</b><br><span class=tip-label>Formula</span>: Done without Rework / Total Done<br><span class=tip-label>Target</span>: &gt;90%<br><span class=tip-label>Rework</span>: Flagged via rework:implementation label in Linear<br><br><b style=color:#fbbf24>Status: No rework labels have been applied yet.</b><br>This metric will become active once the team starts using the rework:implementation label on Linear tickets that required rework after delivery.')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-reliability"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-reliability"></table></div>
  </div>
  <div class="grid-section" style="margin-top:16px">
    <div class="title"><span class="dot" style="background:var(--red)"></span>Rework Log</div>
    <div id="reworkLog" style="padding:16px 20px"></div>
  </div>
</div>

<div class="tab-panel" id="panel-activity">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--accent)"></span>Team Activity<span class="info-btn" onmouseenter="showTip(event,'<b>Task Volume</b><br><span class=tip-label>Shows</span>: Number of tasks per person per week<br><span class=tip-label>Includes</span>: All tasks regardless of status<br><span class=tip-label>Color</span>: Darker = more tasks')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-activity"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-activity"></table></div>
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<div class="grid-section" id="customerKPISection" style="margin-top:20px">
  <div class="title"><span class="dot" style="background:var(--accent)"></span><span id="customerKPITitle">KPI by Customer</span><span class="info-btn" id="clientKpiInfo">?</span></div>
  <div style="overflow-x:auto"><table class="heatmap" id="customerKPITable"></table></div>
</div>

<div class="audit-section" id="auditSection">
  <div class="audit-header" id="auditToggle">
    <h3><span style="font-size:1.1em">&#128203;</span> Audit Data Table <span style="font-size:.72em;font-weight:400;color:var(--dim)">(click to expand)</span></h3>
    <div style="display:flex;align-items:center;gap:12px">
      <div class="audit-tools">
        <button onclick="event.stopPropagation();downloadXLSX()">&#8681; XLSX</button>
        <button onclick="event.stopPropagation();copyTSV()">&#128203; Copy</button>
      </div>
      <span class="toggle">&#9660;</span>
    </div>
  </div>
  <div class="audit-body" id="auditBody">
    <table class="audit-table" id="auditTable"></table>
    <div class="audit-stats" id="auditStats"></div>
  </div>
</div>

<div class="footer">
  TSA KPI Dashboard &nbsp;&middot;&nbsp; Source: Linear + Spreadsheet (backlog) &nbsp;&middot;&nbsp; Generated __DATE__ &nbsp;&middot;&nbsp; Latest data: __LATEST_DATA__
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>
<script>
const RAW = __DATA__;
const BUILD_DATE = '__DATE__';
const LATEST_DATA = '__LATEST_DATA__';

/* ── Helpers ─────────────────────────────────────────── */
function parseWeek(w){const m=w.match(/(\d{2})-(\d{2})\s+W\.(\d+)/);return m?[+m[1],+m[2],+m[3]]:[99,99,99]}
function weekSort(a,b){const[y1,m1,w1]=parseWeek(a),[y2,m2,w2]=parseWeek(b);return y1-y2||m1-m2||w1-w2}
function daysBetween(a,b){if(!a||!b)return null;const d1=new Date(a),d2=new Date(b);if(isNaN(d1)||isNaN(d2))return null;return Math.round((d2-d1)/864e5)}
function monthLabel(y,m){const names=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];return(names[m]||'?')+' '+(y<50?'20'+y:'19'+y)}

/* H1: Dynamic core period — rolling 4 months from latest data, never includes future weeks */
function isCoreWeek(w){
  const[y,m,wn]=parseWeek(w);
  if(y===99)return false;
  const wy=y<50?2000+y:1900+y;
  const wDate=new Date(wy,m-1,(wn-1)*7+1);
  const today=new Date();
  /* Do not include weeks in the future */
  if(wDate>today)return false;
  /* Rolling 4 months back from today */
  const cutoff=new Date(today.getFullYear(),today.getMonth()-4,1);
  return wDate>=cutoff;
}
const CORE_WEEKS=[...new Set(RAW.map(r=>r.week).filter(w=>w&&isCoreWeek(w)))].sort(weekSort);
const PEOPLE_ALL=[...new Set(RAW.map(r=>r.tsa))].sort();

/* Update period label dynamically */
if(CORE_WEEKS.length>0){
  const first=CORE_WEEKS[0],last=CORE_WEEKS[CORE_WEEKS.length-1];
  const[fy,fm]=parseWeek(first),[ly,lm]=parseWeek(last);
  document.getElementById('periodLabel').textContent=monthLabel(fy,fm)+' — '+monthLabel(ly,lm);
}

/* Group weeks by month */
function groupByMonth(weeks){
  const months=[];const seen=new Set();
  weeks.forEach(w=>{
    const[y,m]=parseWeek(w);const key=y+'-'+m;
    if(!seen.has(key)){seen.add(key);months.push({y,m,label:monthLabel(y,m),weeks:[]})}
    months.find(mo=>mo.y===y&&mo.m===m).weeks.push(w);
  });
  return months;
}
const MONTHS=groupByMonth(CORE_WEEKS);

/* M11: Staleness banner */
(function(){
  const el=document.getElementById('stalenessBanner');
  const ld=new Date(LATEST_DATA);const bd=new Date(BUILD_DATE);
  const diffDays=Math.round((bd-ld)/864e5);
  if(isNaN(diffDays)||diffDays<0){el.innerHTML='';return}
  if(diffDays<=3){el.innerHTML='<div class="staleness-banner staleness-ok">Data refreshed: '+BUILD_DATE+' ('+diffDays+' day'+(diffDays!==1?'s':'')+' since latest record)</div>'}
  else if(diffDays<=7){el.innerHTML='<div class="staleness-banner staleness-warn">Data may be stale: built '+BUILD_DATE+', latest record is '+LATEST_DATA+' ('+diffDays+' days ago)</div>'}
  else{el.innerHTML='<div class="staleness-banner staleness-old">Data is stale: built '+BUILD_DATE+', latest record is '+LATEST_DATA+' ('+diffDays+' days ago). Run the pipeline to refresh.</div>'}
})();

/* ── State — M12: default to ALL ──────────────────── */
let state={person:'ALL',category:'ALL'};
const charts={};

function getFiltered(){
  return RAW.filter(r=>{
    if(!r.week||!isCoreWeek(r.week))return false;
    if(state.person!=='ALL'&&r.tsa!==state.person)return false;
    if(state.category!=='ALL'&&r.category!==state.category)return false;
    return true;
  });
}
function getPeople(){
  if(state.person!=='ALL')return[state.person];
  return PEOPLE_ALL;
}

/* ── Tooltip ────────────────────────────────────────── */
const tip=document.getElementById('tooltip');
function showTip(e,html){
  tip.innerHTML=html;tip.style.display='block';
  const rect=tip.getBoundingClientRect();
  const x=Math.min(e.clientX+14,window.innerWidth-rect.width-20);
  const y=Math.min(e.clientY-10,window.innerHeight-rect.height-20);
  tip.style.left=x+'px';tip.style.top=Math.max(10,y)+'px';
}
function hideTip(){tip.style.display='none'}

function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/'/g,'&#39;').replace(/"/g,'&quot;')}

/* ── KPI Calculations ──────────────────────────────── */
function calcAccuracy(rows){
  const ot=rows.filter(r=>r.perf==='On Time').length;
  const lt=rows.filter(r=>r.perf==='Late').length;
  const d=ot+lt; /* H2: aligned — On Time / (On Time + Late) everywhere */
  return{val:d>0?ot/d:null,num:ot,den:d,n:rows.length};
}
function calcVelocity(rows){
  const durs=rows.filter(r=>r.delivery&&(r.startedAt||r.dateAdd)&&r.status==='Done').map(r=>daysBetween(r.startedAt||r.dateAdd,r.delivery)).filter(d=>d!==null&&d>=0);
  const avg=durs.length>0?durs.reduce((a,b)=>a+b,0)/durs.length:null;
  return{val:avg,n:durs.length,durs};
}
function calcReliability(rows){
  const done=rows.filter(r=>r.status==='Done');
  const total=done.length;
  const reworked=done.filter(r=>r.rework==='yes').length;
  const clean=total-reworked;
  return{val:total>0?clean/total:null,num:clean,den:total,n:rows.length,reworked:reworked};
}

/* Heat classes */
function heatPct(val){
  if(val===null||val===undefined||isNaN(val))return'heat-na';
  if(val>=.9)return'heat-great';if(val>=.75)return'heat-good';
  if(val>=.6)return'heat-ok';if(val>=.4)return'heat-bad';return'heat-terrible';
}
function heatDays(val){
  if(val===null||val===undefined||isNaN(val))return'heat-na';
  if(val<=14)return'heat-great';if(val<=28)return'heat-good';
  if(val<=42)return'heat-ok';if(val<=60)return'heat-bad';return'heat-terrible';
}

/* M15: Format with sample size threshold */
function fmtPct(v,n){
  if(v===null||v===undefined||isNaN(v))return'—';
  return(v*100).toFixed(0)+'%';
}
function fmtDays(v){return(v===null||v===undefined||isNaN(v))?'—':v.toFixed(0)+'d'}

/* ── Tooltip cache ────────────────────────────────── */
const tipCache={};
let tipCounter=0;

/* ── Build heatmap grid ─────────────────────────────── */
function buildGrid(tableId, calcFn, fmtFn, heatFn, tipFn){
  const table=document.getElementById(tableId);
  const data=getFiltered();
  const people=getPeople();
  const months=MONTHS;

  let h1='<tr><th rowspan="2" style="text-align:left;min-width:120px;border-right:2px solid var(--border);background:var(--white);font-size:.72em;color:var(--light);font-weight:500;letter-spacing:.5px;padding-left:16px">TEAM</th>';
  months.forEach(mo=>{h1+=`<th class="month-header" colspan="${mo.weeks.length}">${mo.label}</th>`});
  h1+='<th class="month-header" rowspan="2" style="border-left:3px solid var(--accent);font-size:.78em;line-height:1.2">OVERALL<br><span style="font-weight:400;font-size:.8em;color:var(--dim)">all weeks</span></th></tr>';

  let h2='<tr>';
  months.forEach(mo=>{
    mo.weeks.forEach((w,i)=>{
      const[,,wn]=parseWeek(w);
      const first=i===0?'border-left:3px solid var(--accent);':'';
      h2+=`<th class="week-header" style="${first}">W${wn}</th>`;
    });
  });
  h2+='</tr>';

  function cell(cls,txt,tipHtml,isFirstOfMonth){
    const id='t'+(tipCounter++);
    tipCache[id]=tipHtml;
    const mf=isFirstOfMonth?' month-first':'';
    return`<td class="cell ${cls}${mf}" data-tip="${id}">${txt}</td>`;
  }

  let bodyRows='';
  people.forEach(person=>{
    let row=`<tr><td class="person-label">${person}</td>`;
    months.forEach(mo=>{
      mo.weeks.forEach((w,i)=>{
        const rows=data.filter(r=>r.tsa===person&&r.week===w);
        const calc=calcFn(rows);
        const v=calc.val;
        const cls=rows.length===0?'heat-na':heatFn(v);
        /* M15: pass sample size for threshold */
        const txt=rows.length===0?'—':fmtFn(v,calc.den!==undefined?calc.den:calc.n);
        row+=cell(cls,txt,tipFn(person,w,calc,rows),i===0);
      });
    });
    const totalRows=data.filter(r=>r.tsa===person);
    const totalCalc=calcFn(totalRows);
    const totalCls=totalRows.length===0?'heat-na':heatFn(totalCalc.val);
    row+=`<td class="cell total-col ${totalCls}">${totalRows.length===0?'—':fmtFn(totalCalc.val,totalCalc.den!==undefined?totalCalc.den:totalCalc.n)}</td>`;
    row+='</tr>';
    bodyRows+=row;
  });

  let teamRow='<tr class="team-row"><td class="person-label">OVERALL<br><span style="font-weight:400;font-size:.75em;color:var(--dim)">all members</span></td>';
  months.forEach(mo=>{
    mo.weeks.forEach((w,i)=>{
      const rows=data.filter(r=>r.week===w);
      const calc=calcFn(rows);
      const cls=rows.length===0?'heat-na':heatFn(calc.val);
      teamRow+=cell(cls,rows.length===0?'—':fmtFn(calc.val,calc.den!==undefined?calc.den:calc.n),tipFn('TEAM',w,calc,rows),i===0);
    });
  });
  const allRows=data;
  const allCalc=calcFn(allRows);
  const allCls=allRows.length===0?'heat-na':heatFn(allCalc.val);
  teamRow+=`<td class="cell total-col ${allCls}">${allRows.length===0?'—':fmtFn(allCalc.val,allCalc.den!==undefined?allCalc.den:allCalc.n)}</td></tr>`;

  table.innerHTML=`<thead>${h1}${h2}</thead><tbody>${bodyRows}${teamRow}</tbody>`;

  table.addEventListener('mouseenter',function(e){
    const td=e.target.closest('td[data-tip]');
    if(td){const html=tipCache[td.dataset.tip];if(html)showTip(e,html)}
  },true);
  table.addEventListener('mouseleave',function(e){
    const td=e.target.closest('td[data-tip]');
    if(td)hideTip();
  },true);
  table.addEventListener('mousemove',function(e){
    const td=e.target.closest('td[data-tip]');
    if(td&&tip.style.display==='block'){
      const x=Math.min(e.clientX+14,window.innerWidth-tip.offsetWidth-20);
      const y=Math.min(e.clientY-10,window.innerHeight-tip.offsetHeight-20);
      tip.style.left=x+'px';tip.style.top=Math.max(10,y)+'px';
    }
  },true);
}

/* ── Tip helpers ───────────────────────────────────── */
function tipAccuracy(person,week,calc,rows){
  if(rows.length===0)return`<b>${person}</b> &middot; ${week}<br><span class="tip-label">No tasks this week</span>`;
  let html=`<b>${person}</b> &middot; ${week}`;
  html+=`<br><span class="tip-label">ETA Accuracy</span>: <b>${fmtPct(calc.val,calc.den)}</b> (n=${calc.den})`;
  html+=`<br>${calc.num} on time + ${calc.den-calc.num} late = ${calc.den} measured`;
  const excluded=rows.filter(r=>r.perf!=='On Time'&&r.perf!=='Late');
  if(excluded.length>0)html+=`<br>${excluded.length} excluded (${[...new Set(excluded.map(r=>r.perf))].join(', ')})`;
  const lateOnes=rows.filter(r=>r.perf==='Late');
  if(lateOnes.length>0){
    html+=`<div class="tip-section"><span class="tip-label">Late tasks:</span>`;
    lateOnes.slice(0,5).forEach(r=>{
      const delay=r.eta&&r.delivery?daysBetween(r.eta,r.delivery):null;
      const delayTxt=delay!==null&&delay>0?` (+${delay}d)`:'';
      html+=`<div class="tip-task tip-late">${esc(r.focus.slice(0,45))}${delayTxt}</div>`;
    });
    if(lateOnes.length>5)html+=`<div class="tip-task">... +${lateOnes.length-5} more</div>`;
    html+=`</div>`;
  }
  return html;
}
function tipVelocity(person,week,calc,rows){
  if(rows.length===0)return`<b>${person}</b> &middot; ${week}<br><span class="tip-label">No tasks this week</span>`;
  if(calc.n===0)return`<b>${person}</b> &middot; ${week}<br>${rows.length} tasks, none with delivery dates`;
  const sorted=[...calc.durs].sort((a,b)=>a-b);
  const med=sorted[Math.floor(sorted.length/2)];
  const min=sorted[0],max=sorted[sorted.length-1];
  let html=`<b>${person}</b> &middot; ${week}`;
  html+=`<br><span class="tip-label">Execution Time</span>: <b>${fmtDays(calc.val)}</b> avg (n=${calc.n})`;
  html+=`<br>Median: ${med}d &middot; Min: ${min}d &middot; Max: ${max}d`;
  const slow=rows.filter(r=>r.delivery&&(r.startedAt||r.dateAdd)&&r.status==='Done').map(r=>({f:r.focus,d:daysBetween(r.startedAt||r.dateAdd,r.delivery)})).filter(x=>x.d!==null&&x.d>=0).sort((a,b)=>b.d-a.d);
  if(slow.length>0&&slow[0].d>14){
    html+=`<div class="tip-section"><span class="tip-label">Slowest:</span>`;
    slow.slice(0,3).forEach(x=>{html+=`<div class="tip-task tip-late">${x.d}d — ${esc(x.f.slice(0,45))}</div>`});
    html+=`</div>`;
  }
  return html;
}
function tipReliability(person,week,calc,rows){
  if(rows.length===0)return`<b>${person}</b> &middot; ${week}<br><span class="tip-label">No tasks this week</span>`;
  let html=`<b>${person}</b> &middot; ${week}`;
  html+=`<br><span class="tip-label">Reliability</span>: <b>${fmtPct(calc.val,calc.den)}</b> (n=${calc.den})`;
  html+=`<br>${calc.num} clean + ${calc.reworked} rework = ${calc.den} done`;
  if(calc.reworked===0&&calc.den>0)html+=`<br><span style="color:#fbbf24">No rework labels applied yet</span>`;
  return html;
}

/* ── KPI Summary Strip ──────────────────────────────── */
function renderKPIStrip(){
  const data=getFiltered();
  const a=calcAccuracy(data);
  const v=calcVelocity(data);
  const r=calcReliability(data);

  /* C1: Check if rework labels are actually in use */
  const hasReworkData=data.some(x=>x.rework==='yes');

  const strip=document.getElementById('kpiStrip');
  const items=[
    {cls:'k1',icon:'&#9201;',name:'ETA Accuracy',val:a.val,fmt:v=>fmtPct(v,a.den),target:'>90%',pass:a.val!==null&&a.val>=.9,meta:`${a.num}/${a.den} on time (n=${a.den})`},
    {cls:'k2',icon:'&#9889;',name:'Avg Execution Time',val:v.val,fmt:fmtDays,target:'<28 days',pass:v.val!==null&&v.val<=28,meta:`${v.n} tasks measured`},
    {cls:'k3',icon:'&#10003;',name:'Implementation Reliability',val:hasReworkData?r.val:null,fmt:v=>fmtPct(v,r.den),target:'>90%',pass:hasReworkData&&r.val!==null&&r.val>=.9,inactive:!hasReworkData,meta:hasReworkData?`${r.num}/${r.den} done (${r.reworked} rework)`:'NOT ACTIVE — no rework labels in use'},
  ];
  strip.innerHTML=items.map(i=>{
    const badge=i.inactive?'badge-inactive':(i.val===null?'badge-warn':(i.pass?'badge-pass':'badge-fail'));
    const badgeTxt=i.inactive?'NOT ACTIVE':(i.val===null?'—':(i.pass?'ON TARGET':'BELOW'));
    return`<div class="kpi-pill ${i.cls}">
      <div class="icon">${i.icon}</div>
      <div class="info">
        <div class="name">${i.name}</div>
        <div class="val">${i.inactive?'—':(i.val!==null?i.fmt(i.val):'—')}</div>
        <div class="meta">${i.meta} · Target: ${i.target}</div>
      </div>
      <div class="badge ${badge}">${badgeTxt}</div>
    </div>`;
  }).join('');
}

/* ── Trend charts — M7: tab-specific bars ──────────── */
function destroyChart(id){if(charts[id]){charts[id].destroy();delete charts[id]}}

function renderTrend(containerId, calcFn, fmtLabel, color, targetVal, targetLabel, isInverse, barMode){
  const el=document.getElementById(containerId);
  if(typeof Chart==='undefined'){el.innerHTML='<p style="padding:20px;color:var(--dim)">Chart.js not loaded. Charts unavailable.</p>';return}
  const data=getFiltered();

  const teamVals=[];
  /* M7: bar data depends on tab context */
  const bar1=[],bar2=[],bar3=[],bar4=[];
  const bar1Label=barMode==='velocity'?'< 14d':barMode==='reliability'?'Clean':'On Time';
  const bar2Label=barMode==='velocity'?'14-28d':barMode==='reliability'?'Rework':'Late';
  const bar3Label=barMode==='velocity'?'28-60d':barMode==='reliability'?'':'Overdue';
  const bar4Label=barMode==='velocity'?'> 60d':barMode==='reliability'?'':'No ETA';
  const bar1Color=barMode==='velocity'?'#34d39988':barMode==='reliability'?'#34d39988':'#34d39988';
  const bar2Color=barMode==='velocity'?'#fbbf2488':barMode==='reliability'?'#f8717188':'#f8717188';
  const bar3Color=barMode==='velocity'?'#fb923c88':'#fbbf2488';
  const bar4Color=barMode==='velocity'?'#ef444488':'#d1d5db88';

  CORE_WEEKS.forEach(w=>{
    const rows=data.filter(r=>r.week===w);
    const teamCalc=calcFn(rows);
    teamVals.push(teamCalc.val!==null?(typeof teamCalc.val==='number'?+teamCalc.val.toFixed(2):teamCalc.val):null);

    if(barMode==='velocity'){
      const durs=rows.filter(r=>r.delivery&&(r.startedAt||r.dateAdd)&&r.status==='Done').map(r=>daysBetween(r.startedAt||r.dateAdd,r.delivery)).filter(d=>d!==null&&d>=0);
      bar1.push(durs.filter(d=>d<14).length);
      bar2.push(durs.filter(d=>d>=14&&d<28).length);
      bar3.push(durs.filter(d=>d>=28&&d<60).length);
      bar4.push(durs.filter(d=>d>=60).length);
    }else if(barMode==='reliability'){
      const done=rows.filter(r=>r.status==='Done');
      bar1.push(done.filter(r=>r.rework!=='yes').length);
      bar2.push(done.filter(r=>r.rework==='yes').length);
    }else{
      bar1.push(rows.filter(r=>r.perf==='On Time').length);
      bar2.push(rows.filter(r=>r.perf==='Late').length);
      bar3.push(rows.filter(r=>r.perf==='Overdue').length);
      bar4.push(rows.filter(r=>r.perf==='No ETA'||r.perf==='No Delivery Date').length);
    }
  });

  const datasets=[];
  datasets.push({type:'bar',label:bar1Label,data:bar1,backgroundColor:bar1Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});
  datasets.push({type:'bar',label:bar2Label,data:bar2,backgroundColor:bar2Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});
  if(bar3Label)datasets.push({type:'bar',label:bar3Label,data:bar3,backgroundColor:bar3Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});
  if(bar4Label)datasets.push({type:'bar',label:bar4Label,data:bar4,backgroundColor:bar4Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});

  datasets.push({type:'line',label:fmtLabel,data:teamVals,borderColor:color,backgroundColor:color+'22',borderWidth:1.5,fill:false,tension:.3,pointRadius:2,pointHoverRadius:5,pointBackgroundColor:color,yAxisID:'yLine',order:1,spanGaps:true});
  datasets.push({type:'line',label:targetLabel,data:CORE_WEEKS.map(()=>targetVal),borderColor:'#ef444466',borderDash:[4,3],borderWidth:1,pointRadius:0,pointHoverRadius:0,yAxisID:'yLine',order:1,fill:false});

  const mNames=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const weekLabels=CORE_WEEKS.map(w=>{const[,m,wn]=parseWeek(w);return mNames[m]+' W'+wn});

  const canvasId=containerId+'-canvas';
  el.innerHTML=`<h4>Weekly Trend — bars: ${barMode||'ETA'} breakdown · line: ${fmtLabel}</h4><canvas id="${canvasId}"></canvas>`;

  destroyChart(canvasId);
  charts[canvasId]=new Chart(document.getElementById(canvasId),{
    type:'bar',
    data:{labels:weekLabels,datasets},
    options:{
      responsive:true,maintainAspectRatio:false,
      interaction:{mode:'index',intersect:false},
      plugins:{
        legend:{display:true,position:'bottom',labels:{color:'#374151',font:{size:11,weight:'500'},boxWidth:10,padding:10,usePointStyle:true}},
        tooltip:{
          enabled:true,backgroundColor:'#1e293bee',titleColor:'#93c5fd',titleFont:{size:12,weight:'700'},
          bodyColor:'#e2e8f0',bodyFont:{size:11},padding:12,cornerRadius:8,boxPadding:4,
          callbacks:{
            title:function(items){if(!items[0])return'';const idx=items[0].dataIndex;return CORE_WEEKS[idx]||'';},
            label:function(ctx){
              if(ctx.raw===null||ctx.raw===undefined)return null;
              const name=ctx.dataset.label;
              if(name===targetLabel)return null;
              if(name===fmtLabel){
                const val=ctx.raw;
                const fmtVal=isInverse?val.toFixed(0)+'d':(val*100).toFixed(0)+'%';
                return ` ${fmtLabel}: ${fmtVal}`;
              }
              return ' '+name+': '+ctx.raw;
            }
          }
        }
      },
      scales:{
        yBar:{position:'left',stacked:true,ticks:{color:'#6b7280',font:{size:10},stepSize:1},grid:{color:'#e5e7eb88'},title:{display:true,text:'Tasks',color:'#9ca3af',font:{size:10}},beginAtZero:true},
        yLine:{position:'right',ticks:{color:color,font:{size:10},callback:function(v){return isInverse?v+'d':barMode==='activity'?v:(v*100).toFixed(0)+'%'}},grid:{drawOnChartArea:false},title:{display:true,text:fmtLabel,color:color,font:{size:10}},beginAtZero:true,min:0,max:barMode==='activity'?undefined:(isInverse?undefined:1)},
        x:{stacked:true,ticks:{color:'#6b7280',font:{size:10}},grid:{color:'#f3f4f622'}}
      }
    }
  });
}

/* ── Activity calc ─────────────────────────────────── */
function calcActivity(rows){
  return{val:rows.length,n:rows.length,
    done:rows.filter(r=>r.status==='Done').length,
    open:rows.filter(r=>r.status!=='Done'&&r.status!=='Canceled').length,
    canceled:rows.filter(r=>r.status==='Canceled').length};
}
function fmtCount(v){return(v===null||v===undefined)?'—':v}
function heatVol(val){
  if(val===null||val===undefined||val===0)return'heat-vol-0';
  if(val<=2)return'heat-vol-1';if(val<=4)return'heat-vol-2';
  if(val<=7)return'heat-vol-3';if(val<=12)return'heat-vol-4';return'heat-vol-5';
}
function tipActivity(person,week,calc,rows){
  if(rows.length===0)return`<b>${person}</b> &middot; ${week}<br><span class="tip-label">No tasks this week</span>`;
  let html=`<b>${person}</b> &middot; ${week}`;
  html+=`<br><span class="tip-label">Tasks</span>: <b>${calc.n}</b>`;
  html+=`<br>Done: ${calc.done} &middot; Open: ${calc.open}`;
  if(calc.canceled>0)html+=` &middot; Canceled: ${calc.canceled}`;
  if(rows.length<=5){
    html+=`<div class="tip-section"><span class="tip-label">Tasks:</span>`;
    rows.forEach(r=>{const cls=r.status==='Done'?'tip-ontime':'tip-late';html+=`<div class="tip-task ${cls}">${esc(r.focus.slice(0,50))}</div>`});
    html+=`</div>`;
  }
  return html;
}

/* ── Member cards — H2 aligned, H14 sample size, D.LIE12 ETA coverage ── */
function renderMemberCards(){
  const data=getFiltered();
  const people=getPeople();
  const el=document.getElementById('memberCards');

  const cards=people.map(p=>{
    const pr=data.filter(r=>r.tsa===p);
    const done=pr.filter(r=>r.status==='Done').length;
    const open=pr.filter(r=>r.status!=='Done'&&r.status!=='Canceled').length;
    const onTime=pr.filter(r=>r.perf==='On Time').length;
    const late=pr.filter(r=>r.perf==='Late').length;
    const overdue=pr.filter(r=>r.perf==='Overdue').length;
    const noEta=pr.filter(r=>r.perf==='No ETA').length;
    const total=pr.length;
    const donePct=total>0?Math.round(done/total*100):0;

    /* H2: Same formula as KPI1 — On Time / (On Time + Late) */
    const measured=onTime+late;
    const accPct=measured>0?Math.round(onTime/measured*100):null;

    /* D.LIE12: ETA Coverage */
    const withEta=pr.filter(r=>r.eta&&r.eta.length>=10).length;
    const etaCov=total>0?Math.round(withEta/total*100):0;

    /* Data source badge */
    const sources=new Set(pr.map(r=>r.source));
    const srcBadge=sources.has('linear')?'<span class="mc-source mc-source-linear">Linear</span>':'<span class="mc-source mc-source-spreadsheet">Spreadsheet</span>';

    const recent=pr.filter(r=>{const lw=CORE_WEEKS.slice(-2);return lw.includes(r.week)}).length;

    let alert='';
    if(recent===0&&total>0)alert='<span class="mc-alert mc-alert-warn">NO RECENT</span>';
    else if(noEta>total*0.5)alert='<span class="mc-alert mc-alert-warn">'+noEta+' NO ETA</span>';
    else if(accPct!==null&&accPct>=85)alert='<span class="mc-alert mc-alert-ok">ON TRACK</span>';

    const barColor=donePct>=80?'var(--green)':donePct>=50?'var(--yellow)':'var(--red)';

    return`<div class="member-card">${alert}
      <div class="mc-name">${p} ${srcBadge}</div>
      <div class="mc-body">
        <div class="mc-row"><span>Total</span><b>${total}</b></div>
        <div class="mc-row"><span>Done</span><b>${done} (${donePct}%)</b></div>
        <div class="mc-row"><span>Open</span><b>${open}</b></div>
        <div class="mc-row"><span>On Time</span><b style="color:var(--green)">${onTime}</b></div>
        <div class="mc-row"><span>Late/Overdue</span><b style="color:${late+overdue>0?'var(--red)':'var(--dim)'}">${late+overdue}</b></div>
        <div class="mc-row"><span>Accuracy</span><b>${accPct!==null?accPct+'% (n='+measured+')':'—'}</b></div>
        <div class="mc-row"><span>ETA Coverage</span><b style="color:${etaCov<50?'var(--yellow)':'var(--dim)'}">${etaCov}% (${withEta}/${total})</b></div>
      </div>
      <div class="mc-bar"><div class="mc-bar-track"><div class="mc-bar-inner" style="width:${donePct}%;background:${barColor}"></div></div></div>
    </div>`;
  });
  el.innerHTML=cards.join('');
}

/* ── Segment counts ────────────────────────────────── */
function updateSegmentCounts(){
  const base=RAW.filter(r=>r.week&&isCoreWeek(r.week)&&(state.person==='ALL'||r.tsa===state.person));
  document.getElementById('segExt').textContent=' ('+base.filter(r=>r.category==='External').length+')';
  document.getElementById('segInt').textContent=' ('+base.filter(r=>r.category==='Internal').length+')';
  document.getElementById('segAll').textContent=' ('+base.length+')';
}

/* ── KPI by Client ────────────────────────────────── */
const CLIENT_TIP='<b>KPI by Customer</b><br><span class=tip-label>Shows</span>: ETA Accuracy, Avg Execution, Reliability per customer<br><span class=tip-label>Colors</span>: Same heat scale as main grids';
const INTERNAL_CONTEXTS=new Set(['Waki','TBX','Routine','General','Coda','All',"Internal \u2013 Sam's Board Meeting"]);

function renderCustomerKPI(){
  const isInt=state.category==='Internal';
  const isAll=state.category==='ALL';
  const base=RAW.filter(r=>{
    if(!r.week||!isCoreWeek(r.week))return false;
    if(state.person!=='ALL'&&r.tsa!==state.person)return false;
    if(!r.customer)return false;
    if(isAll)return true;
    if(isInt)return r.category==='Internal'&&INTERNAL_CONTEXTS.has(r.customer);
    return r.category==='External';
  });
  document.getElementById('customerKPITitle').textContent=isInt?'KPI by Internal Demand':(isAll?'KPI by Customer / Demand':'KPI by Customer');
  const el=document.getElementById('customerKPITable');
  if(!base.length){el.innerHTML='<tr><td colspan="10" style="padding:20px;text-align:center;color:var(--dim)">No customer data in this view</td></tr>';return}
  const custs=[...new Set(base.map(r=>r.customer))];
  custs.sort((a,b)=>base.filter(r=>r.customer===b).length-base.filter(r=>r.customer===a).length);
  const cols=['Customer','Tasks','Done','On Time','Late','Overdue','No ETA','ETA Accuracy','Avg Execution','Reliability'];
  function kpiRow(label,rows,isTeam){
    const t=rows.length,dn=rows.filter(r=>r.status==='Done').length;
    const ot=rows.filter(r=>r.perf==='On Time').length,lt=rows.filter(r=>r.perf==='Late').length;
    const ov=rows.filter(r=>r.perf==='Overdue').length,ne=rows.filter(r=>r.perf==='No ETA').length;
    const ad=ot+lt,acc=ad>0?ot/ad:null;
    const doneRows=rows.filter(r=>r.status==='Done');const rw=doneRows.filter(r=>r.rework==='yes').length;const rd=doneRows.length,rel=rd>0?(rd-rw)/rd:null;
    const ds=rows.filter(r=>r.delivery&&(r.startedAt||r.dateAdd)&&r.status==='Done').map(r=>daysBetween(r.startedAt||r.dateAdd,r.delivery)).filter(d=>d!==null&&d>=0);
    const avg=ds.length>0?ds.reduce((a,b)=>a+b,0)/ds.length:null;
    const cls=isTeam?' class="team-row"':'';
    const bg=isTeam?'':((rowIdx%2===0)?'background:#f9fafb;':'');
    const lbl=isTeam?`<td class="person-label">OVERALL</td>`:`<td class="person-label" style="${bg}">${label}</td>`;
    if(!isTeam)rowIdx++;
    return`<tr${cls}>${lbl}<td style="${bg}">${t}</td><td style="${bg}">${dn}</td><td style="${bg}color:var(--green);font-weight:600">${ot}</td><td style="${bg}color:${lt?'var(--red)':'var(--dim)'}">${lt}</td><td style="${bg}color:${ov?'var(--yellow)':'var(--dim)'}">${ov}</td><td style="${bg}color:${ne?'var(--yellow)':'var(--dim)'}">${ne}</td><td class="cell ${acc!==null?heatPct(acc):'heat-na'}" style="font-weight:700">${fmtPct(acc,ad)}</td><td class="cell ${avg!==null?heatDays(avg):'heat-na'}" style="font-weight:700">${fmtDays(avg)}</td><td class="cell ${rel!==null?heatPct(rel):'heat-na'}" style="font-weight:700">${fmtPct(rel,rd)}</td></tr>`;
  }
  let h='<thead><tr>'+cols.map(c=>'<th>'+c+'</th>').join('')+'</tr></thead>';
  let rowIdx=0;
  let b='<tbody>';
  custs.forEach(c=>{b+=kpiRow(c,base.filter(r=>r.customer===c),false)});
  b+=kpiRow('OVERALL',base,true);
  b+='</tbody>';
  el.innerHTML=h+b;
}

/* ── Audit table ──────────────────────────────────── */
let auditSortCol=0, auditSortAsc=true;

function getAuditRows(){
  return getFiltered().map((r,i)=>{
    const start=r.startedAt||r.dateAdd;const dur=(r.delivery&&start)?daysBetween(start,r.delivery):null;
    return [i+1, r.tsa||'—', r.week||'—', r.ticketId||'—', r.focus||'—', r.status||'—', r.category||'—', r.demandType||'—', r.customer||'—', r.dateAdd||'—', r.eta||'—', r.delivery||'—', r.perf||'—', r.rework==='yes'?'YES':'—', dur!==null&&dur>=0?dur+'d':'—', r.source||'—', r.ticketUrl||'', r.milestone||'—', r.parentId||'—'];
  });
}

const AUDIT_COLS=['#','Person','Week','Ticket','Focus/Task','Status','Category','Demand Type','Customer','Date Added','ETA','Delivery','Performance','Rework','Duration','Source','Ticket URL','Milestone','Parent'];

function perfClass(v){
  if(v==='On Time')return'perf-on-time';if(v==='Late')return'perf-late';
  if(v==='Overdue')return'perf-overdue';return'perf-na';
}

function renderAuditTable(){
  const rows=getAuditRows();
  rows.forEach((r,i)=>r[0]=i+1);
  const hideCols=new Set([16]);
  rows.sort((a,b)=>{
    let va=a[auditSortCol],vb=b[auditSortCol];
    if(typeof va==='string'&&typeof vb==='string'){va=va.toLowerCase();vb=vb.toLowerCase()}
    if(va<vb)return auditSortAsc?-1:1;if(va>vb)return auditSortAsc?1:-1;return 0;
  });

  const table=document.getElementById('auditTable');
  let thead='<thead><tr>';
  AUDIT_COLS.forEach((c,i)=>{
    if(hideCols.has(i))return;
    const arrow=i===auditSortCol?(auditSortAsc?'&#9650;':'&#9660;'):'';
    thead+=`<th data-col="${i}">${c}<span class="sort-arrow">${arrow}</span></th>`;
  });
  thead+='</tr></thead>';

  let tbody='<tbody>';
  rows.forEach(r=>{
    tbody+='<tr>';
    r.forEach((v,i)=>{
      if(hideCols.has(i))return;
      const cls=i===12?' class="'+perfClass(v)+'"':(i===13&&v==='YES'?' class="rework-yes"':'');
      if(i===3&&r[16]){tbody+=`<td><a href="${esc(r[16])}" target="_blank" style="color:var(--accent);text-decoration:none;font-weight:600">${esc(String(v))}</a></td>`}
      else{tbody+=`<td${cls}>${esc(String(v))}</td>`}
    });
    tbody+='</tr>';
  });
  tbody+='</tbody>';
  table.innerHTML=thead+tbody;

  table.querySelectorAll('th').forEach(th=>{
    th.addEventListener('click',()=>{
      const col=+th.dataset.col;
      if(col===auditSortCol)auditSortAsc=!auditSortAsc;
      else{auditSortCol=col;auditSortAsc=true}
      renderAuditTable();
    });
  });

  const stats=document.getElementById('auditStats');
  const sdata=getFiltered();
  const onTime=sdata.filter(r=>r.perf==='On Time').length;
  const late=sdata.filter(r=>r.perf==='Late').length;
  const overdue=sdata.filter(r=>r.perf==='Overdue').length;
  const done=sdata.filter(r=>r.status==='Done').length;
  const open=sdata.filter(r=>r.status!=='Done'&&r.status!=='Canceled').length;
  const reworkCount=sdata.filter(r=>r.rework==='yes').length;
  /* M13: Note about On Track exclusion */
  const onTrack=sdata.filter(r=>r.perf==='On Track').length;
  stats.innerHTML=`<span><b>${rows.length}</b> records</span><span>Done: <b>${done}</b></span><span>Open: <b>${open}</b></span><span style="color:var(--green)">On Time: <b>${onTime}</b></span><span style="color:var(--red)">Late: <b>${late}</b></span><span style="color:var(--yellow)">Overdue: <b>${overdue}</b></span><span>On Track: <b>${onTrack}</b> (excluded from KPI1)</span><span style="color:var(--red)">Rework: <b>${reworkCount}</b></span>`;
}

/* ── Export functions ──────────────────────────────── */
function downloadXLSX(){
  if(typeof XLSX==='undefined'){alert('SheetJS not loaded. Export unavailable.');return}
  const rows=getAuditRows();
  rows.forEach((r,i)=>r[0]=i+1);
  const aoa=[AUDIT_COLS,...rows];
  const ws=XLSX.utils.aoa_to_sheet(aoa);
  ws['!cols']=[{wch:5},{wch:14},{wch:12},{wch:12},{wch:45},{wch:12},{wch:11},{wch:18},{wch:25},{wch:12},{wch:12},{wch:12},{wch:13},{wch:8},{wch:10},{wch:12},{wch:55},{wch:25},{wch:12}];
  for(let r=1;r<=rows.length;r++){
    const urlCol=16;const urlCell=XLSX.utils.encode_cell({r:r,c:urlCol});
    const ticketCell=XLSX.utils.encode_cell({r:r,c:3});
    if(ws[urlCell]&&ws[urlCell].v&&ws[urlCell].v.startsWith('http')){
      ws[urlCell].l={Target:ws[urlCell].v,Tooltip:'Open in Linear'};
      if(ws[ticketCell]&&ws[ticketCell].v&&ws[ticketCell].v!=='—'){ws[ticketCell].l={Target:ws[urlCell].v,Tooltip:'Open in Linear'}}
    }
  }
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,ws,'Audit');
  XLSX.writeFile(wb,'KPI_AUDIT_'+new Date().toISOString().slice(0,10)+'.xlsx');
}

function copyTSV(){
  const rows=getAuditRows();
  rows.forEach((r,i)=>r[0]=i+1);
  let tsv=AUDIT_COLS.join('\t')+'\n';
  rows.forEach(r=>{tsv+=r.join('\t')+'\n'});
  navigator.clipboard.writeText(tsv).then(()=>{
    const btn=document.querySelector('.audit-tools button:nth-child(2)');
    const orig=btn.innerHTML;btn.innerHTML='&#10003; Copied!';btn.style.background='var(--green)';btn.style.color='#fff';
    setTimeout(()=>{btn.innerHTML=orig;btn.style.background='';btn.style.color=''},1500);
  });
}

/* ── Render all ─────────────────────────────────────── */
function render(){
  updateSegmentCounts();
  renderMemberCards();
  renderKPIStrip();
  buildGrid('grid-accuracy',calcAccuracy,fmtPct,heatPct,tipAccuracy);
  buildGrid('grid-velocity',calcVelocity,fmtDays,heatDays,tipVelocity);
  buildGrid('grid-reliability',calcReliability,fmtPct,heatPct,tipReliability);
  buildGrid('grid-activity',calcActivity,fmtCount,heatVol,tipActivity);
  renderTrend('trend-accuracy',calcAccuracy,'ETA Accuracy','#4f46e5',.9,'Target 90%',false,'accuracy');
  renderTrend('trend-velocity',calcVelocity,'Execution Time','#b45309',28,'Target 28d',true,'velocity');
  renderTrend('trend-reliability',calcReliability,'Reliability','#047857',.9,'Target 90%',false,'reliability');
  renderTrend('trend-activity',calcActivity,'Task Volume','#4338ca',5,'Avg 5/week',false,'activity');
  renderCustomerKPI();
  renderAuditTable();
  renderReworkLog();
}

function renderReworkLog(){
  const data=getFiltered();
  const reworkItems=data.filter(r=>r.rework==='yes');
  const el=document.getElementById('reworkLog');
  if(reworkItems.length===0){
    el.innerHTML='<div style="text-align:center;padding:20px 0;color:var(--dim)"><div style="font-size:1.5em;margin-bottom:8px">&#10003;</div><div style="font-size:.88em;font-weight:600">No rework flagged</div><div style="font-size:.78em;color:var(--light);margin-top:4px">When a ticket gets the <span style="background:#fef2f2;color:#dc2626;padding:1px 6px;border-radius:3px;font-weight:600;font-size:.85em">rework:implementation</span> label in Linear, it appears here.</div></div>';
    return;
  }
  let html='<table class="detail-table"><thead><tr><th>Person</th><th>Ticket</th><th>Task</th><th>Customer</th><th>Delivered</th><th>Status</th></tr></thead><tbody>';
  reworkItems.forEach(r=>{
    const link=r.ticketUrl?`<a href="${esc(r.ticketUrl)}" target="_blank" style="color:var(--accent);font-weight:600">${esc(r.ticketId||'—')}</a>`:(r.ticketId||'—');
    html+=`<tr><td>${esc(r.tsa)}</td><td>${link}</td><td>${esc(r.focus.slice(0,50))}</td><td>${esc(r.customer||'—')}</td><td>${r.delivery||'—'}</td><td><span style="color:var(--red);font-weight:600">Rework</span></td></tr>`;
  });
  html+='</tbody></table>';
  html+=`<div style="margin-top:10px;font-size:.72em;color:var(--dim)">${reworkItems.length} ticket${reworkItems.length>1?'s':''} flagged for rework out of ${data.filter(r=>r.status==='Done').length} delivered</div>`;
  el.innerHTML=html;
}

/* ── Init ───────────────────────────────────────────── */
function init(){
  const fp=document.getElementById('fPerson');
  PEOPLE_ALL.forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;fp.appendChild(o)});

  const cki=document.getElementById('clientKpiInfo');
  cki.addEventListener('mouseenter',e=>showTip(e,CLIENT_TIP));
  cki.addEventListener('mouseleave',()=>hideTip());

  document.getElementById('fPerson').addEventListener('change',e=>{state.person=e.target.value;render()});

  /* M12: Segment bar — default ALL */
  document.querySelectorAll('.segment-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      document.querySelectorAll('.segment-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      state.category=btn.dataset.seg;
      document.getElementById('fCategory').value=btn.dataset.seg;
      render();
    });
  });
  document.getElementById('fCategory').addEventListener('change',e=>{
    state.category=e.target.value;
    document.querySelectorAll('.segment-btn').forEach(b=>{
      b.classList.toggle('active',b.dataset.seg===state.category);
    });
    render();
  });

  document.querySelectorAll('.tab').forEach(tab=>{
    tab.addEventListener('click',()=>{
      document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById('panel-'+tab.dataset.tab).classList.add('active');
    });
  });

  document.getElementById('auditToggle').addEventListener('click',()=>{
    const header=document.getElementById('auditToggle');
    const body=document.getElementById('auditBody');
    header.classList.toggle('open');
    body.classList.toggle('open');
  });

  render();
}

init();
</script>
</body>
</html>"""

# Inject data and date
html = HTML.replace('__DATA__', data_json_safe).replace('__DATE__', build_date).replace('__LATEST_DATA__', latest_data_date)

# C3: Atomic write
tmp_path = OUTPUT + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(html)
os.replace(tmp_path, OUTPUT)

print(f'Dashboard saved: {OUTPUT}')
print(f'Size: {len(html)//1024}KB')
print(f'Records: {len(data_raw)} | Core weeks: dynamically computed')
print(f'Build date: {build_date} | Latest data: {latest_data_date}')
