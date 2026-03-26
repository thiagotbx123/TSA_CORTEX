# Architecture note: This file generates a self-contained HTML dashboard.
# The HTML/CSS/JS is embedded as a raw string for single-file deployment.
# Structure: CSS (lines ~45-270) | HTML (270-440) | JS (440-2080)
# To lint JS independently, extract the <script> block to a temp file.

"""Build Raccoons KPI HTML Dashboard v3 — audit-hardened version.

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
OUTPUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'KPI_DASHBOARD.html')

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
build_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
# Find the most recent dateAdd in data for staleness comparison (only past/present dates)
data_dates = [r.get('dateAdd', '') for r in data_raw
              if r.get('dateAdd', '') and len(r.get('dateAdd', '')) >= 10 and r['dateAdd'][:10] <= build_date[:10]]
latest_data_date = max(data_dates) if data_dates else build_date

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KPI Dashboard</title>
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
.top-strip{display:flex;gap:8px;margin-bottom:18px;align-items:stretch}
.strip-group{display:flex;gap:6px;flex:1;padding:6px;border-radius:10px;background:var(--white);border:1px solid var(--border)}
.strip-group.filters-group{flex:0 0 auto;background:#f0fdf4;border-color:#a7f3d0}
.strip-group.filters-group::before{content:'FILTERS';position:absolute;top:-8px;left:12px;font-size:.5em;font-weight:700;color:#065f46;background:#f0fdf4;padding:0 4px;letter-spacing:1px;display:none}
.strip-group.kpi-group{background:#eff6ff;border-color:#bfdbfe}
.kpi-cell{flex:1;background:transparent;border:1px solid transparent;border-radius:8px;padding:10px 8px;text-align:center;position:relative;cursor:pointer;transition:all .15s}
.kpi-cell:hover{background:#dbeafe;border-color:#93c5fd}
.kpi-cell.kpi-active{border-color:var(--accent);border-width:2px;background:#dbeafe}
.kpi-cell .kc-name{font-size:.65em;color:var(--dim);text-transform:uppercase;letter-spacing:.5px;font-weight:600;margin-bottom:2px}
.kpi-cell .kc-val{font-size:1.3em;font-weight:800;line-height:1.3}
.kpi-cell .kc-meta{font-size:.6em;color:var(--dim);margin-top:1px}
.kpi-cell .badge{font-size:.52em;font-weight:700;padding:1px 5px;border-radius:20px;display:inline-block;margin-top:4px}
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
.info-btn{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--gray-bg);color:var(--dim);font-size:.7em;font-weight:700;cursor:help;margin-left:4px;border:1px solid var(--border)}
.heatmap{width:100%;border-collapse:collapse;font-size:.88em}
.heatmap th,.heatmap td{padding:9px 12px;text-align:center;white-space:nowrap}
.heatmap thead th{background:var(--gray-bg);font-weight:600;color:var(--dim);font-size:.8em;text-transform:uppercase;letter-spacing:.3px;border-bottom:1px solid var(--border)}
.heatmap .month-header{background:#eef2ff;color:var(--blue);font-weight:700;font-size:.88em;letter-spacing:.5px;border-bottom:2px solid var(--blue-l);padding:10px 8px;border-left:3px solid var(--accent)}
.heatmap .week-header{background:var(--gray-bg);font-size:.78em;color:var(--dim);padding:7px 8px}
.heatmap .month-first{border-left:3px solid var(--accent)!important}
.heatmap .person-label{text-align:left;font-weight:600;padding-left:16px;background:var(--white);border-right:2px solid var(--border);min-width:120px;font-size:.9em;color:var(--text);position:sticky;left:0;z-index:2}
.heatmap .team-row td{font-weight:800;background:#eef2ff;border-top:3px solid var(--accent);font-size:.92em}
.heatmap .team-row .person-label{background:#eef2ff;color:var(--accent);font-size:.82em;text-transform:uppercase;letter-spacing:.3px;font-weight:800;white-space:normal;line-height:1.3;position:sticky;left:0;z-index:2}
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
.tooltip{position:fixed;background:linear-gradient(135deg,rgba(15,23,42,.88),rgba(30,41,59,.92));backdrop-filter:blur(8px);color:#fff;padding:14px 18px;border-radius:10px;font-size:.82em;pointer-events:none;z-index:999;max-width:420px;line-height:1.6;box-shadow:0 8px 30px rgba(0,0,0,.4);display:none;border:1px solid rgba(255,255,255,.08)}
.tooltip b{color:#93c5fd}
.tooltip .tip-hdr{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,.12)}
.tooltip .tip-hdr b{font-size:1.05em;color:#60a5fa}
.tooltip .tip-hdr .tip-pct{font-size:1.3em;font-weight:800;color:#fff}
.tooltip .tip-hdr .tip-pct.good{color:#34d399}
.tooltip .tip-hdr .tip-pct.bad{color:#f87171}
.tooltip .tip-hdr .tip-pct.mid{color:#fbbf24}
.tooltip .tip-stats{display:flex;gap:12px;margin:6px 0;font-size:.88em}
.tooltip .tip-stat{text-align:center}
.tooltip .tip-stat b{display:block;font-size:1.1em;color:#fff}
.tooltip .tip-stat span{color:#94a3b8;font-size:.85em}
.tooltip .tip-section{margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,.12)}
.tooltip .tip-task{color:#e2e8f0;font-size:.88em;padding:4px 0 4px 10px;border-left:2px solid transparent;margin:2px 0}
.tooltip .tip-task.tip-late{border-left-color:#f87171}
.tooltip .tip-task.tip-ontime{border-left-color:#34d399}
.tooltip .tip-task.tip-overdue{border-left-color:#fbbf24}
.tooltip .tip-task .tip-cust{color:#a78bfa;font-size:.9em;font-weight:600}
.tooltip .tip-task .tip-dates{color:#64748b;font-size:.85em}
.tooltip .tip-task .tip-delay{color:#fbbf24;font-weight:700;font-size:.9em}
.tooltip .tip-label{color:#94a3b8;font-size:.82em;font-weight:600;text-transform:uppercase;letter-spacing:.5px}
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
.segment-btn{flex:1;padding:10px 8px;border-radius:8px;font-size:.85em;font-weight:700;color:#065f46;cursor:pointer;transition:all .15s;border:1px solid transparent;background:transparent;letter-spacing:.2px;text-align:center}
.segment-btn:hover{background:#d1fae5;border-color:#a7f3d0}
.segment-btn.active{background:#065f46;color:#fff;border-color:#065f46;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.segment-btn .seg-count{display:block;font-size:.75em;font-weight:400;opacity:.7;margin-top:2px}
.audit-section{background:var(--white);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-top:20px}
.audit-header{display:flex;align-items:center;padding:14px 20px;border-bottom:1px solid var(--border);cursor:pointer;user-select:none;gap:10px}
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
.audit-table .perf-on-track{color:#2563eb;font-weight:600}
.audit-table .perf-overdue{color:var(--yellow);font-weight:600}
.audit-table .perf-na{color:var(--light)}
.audit-table .perf-not-started{color:#a78bfa;font-weight:500}
.audit-table .rework-yes{color:var(--red);font-weight:700}
.audit-stats{padding:10px 20px;font-size:.72em;color:var(--dim);border-top:1px solid var(--gray-l);display:flex;gap:16px;flex-wrap:wrap}
.member-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:18px}
.member-card{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:12px 14px;position:relative;overflow:hidden;display:flex;flex-direction:column}
.member-card .mc-name{font-weight:700;font-size:.88em;margin-bottom:6px;color:var(--text)}
.member-card .mc-body{flex:1}
.member-card .mc-row{display:flex;justify-content:space-between;font-size:.72em;color:var(--dim);padding:2px 0}
.member-card .mc-row span[title]{cursor:help;border-bottom:1px dotted var(--dim)}
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
.scrum-card{background:var(--white);border:1px solid var(--border);border-radius:10px;overflow:hidden;cursor:pointer;transition:all .15s}
.scrum-card:hover{border-color:var(--accent);box-shadow:0 2px 12px rgba(37,99,235,.12)}
.scrum-card.copied{border-color:#059669;background:#ecfdf5}
.scrum-card .sc-header{padding:12px 16px;background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;display:flex;justify-content:space-between;align-items:center}
.scrum-card .sc-name{font-weight:700;font-size:.95em}
.scrum-card .sc-stats{display:flex;gap:8px;font-size:.7em}
.scrum-card .sc-stats span{padding:2px 8px;border-radius:10px}
.scrum-card .sc-body{padding:12px 16px;font-size:.82em;line-height:1.7;font-family:'Consolas','Menlo',monospace;white-space:pre-wrap;color:#334155;max-height:400px;overflow-y:auto}
.scrum-card .sc-customer{color:#6366f1;font-weight:700;margin-top:6px}
.scrum-card .sc-task{padding-left:4px}
.scrum-card .sc-g{color:#059669}.scrum-card .sc-y{color:#d97706}.scrum-card .sc-r{color:#dc2626}
.scrum-card .sc-copy-hint{text-align:center;padding:6px;font-size:.68em;color:var(--light);border-top:1px solid var(--gray-l)}
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
/* ── Gantt chart styles (gt- prefix) ───────────── */
.gt-months{display:flex;position:sticky;top:0;z-index:21;background:var(--white);border-bottom:2px solid var(--border)}
.gt-months .gt-label-col{min-width:280px;max-width:280px;position:sticky;left:0;z-index:30;background:#0f172a;padding:6px 12px;display:flex;align-items:center;box-shadow:6px 0 12px rgba(0,0,0,.2)}
.gt-months .gt-label-col span{color:#94a3b8;font-size:.72em;font-weight:600}
.gt-month-cell{display:flex;align-items:center;justify-content:center;font-size:.72em;font-weight:700;color:#1e293b;background:#f8fafc;border-right:2px solid #94a3b8;padding:4px 0}
.gt-header{display:flex;position:sticky;top:28px;z-index:20;background:var(--white);border-bottom:1px solid var(--border)}
.gt-header .gt-label-col{min-width:280px;max-width:280px;position:sticky;left:0;z-index:28;background:#f1f5f9;padding:2px 12px;display:flex;align-items:center;box-shadow:6px 0 12px rgba(0,0,0,.1)}
.gt-header .gt-label-col span{color:#94a3b8;font-size:.6em}
.gt-days{display:flex}
.gt-day{min-width:6px;max-width:6px;text-align:center;font-size:.45em;color:#94a3b8;padding:1px 0;border-right:1px solid #f1f5f9}
.gt-day.gt-weekend{background:#f1f5f9;color:#cbd5e1}
.gt-day.gt-month-start{border-left:2px solid #cbd5e1}
.gt-day.gt-today-col{background:#fef2f2;color:#dc2626;font-weight:700}
.gt-row{display:flex;border-bottom:1px solid #e8ecf1;min-height:28px;align-items:stretch}
.gt-row:hover{background:#f8fafc}
.gt-label{min-width:280px;max-width:280px;position:sticky;left:0;z-index:15;background:var(--white);display:flex;align-items:center;padding:0 8px;border-right:2px solid #cbd5e1;box-shadow:6px 0 12px rgba(0,0,0,.1)}
.gt-row:hover .gt-label{background:#f8fafc}
.gt-group{background:#f8fafc;border-bottom:2px solid var(--border);cursor:pointer;user-select:none}
.gt-group:hover{background:#e2e8f0}
.gt-group .gt-label{background:#f8fafc;font-weight:700;font-size:.82em;gap:8px;box-shadow:6px 0 12px rgba(0,0,0,.1)}
.gt-group:hover .gt-label{background:#e2e8f0}
.gt-group .gt-arrow{font-size:.65em;color:#64748b;transition:transform .2s;width:14px;text-align:center}
.gt-group.gt-open .gt-arrow{transform:rotate(90deg)}
.gt-group .gt-count{font-size:.65em;color:#94a3b8;font-weight:400;margin-left:4px}
.gt-group .gt-badges{display:flex;gap:4px;margin-left:auto;margin-right:4px}
.gt-group .gt-badge{font-size:.6em;padding:1px 6px;border-radius:8px;font-weight:600}
.gt-task .gt-label{font-size:.72em;color:#475569;padding-left:28px;gap:6px}
.gt-task .gt-label a{color:var(--accent);text-decoration:none;font-weight:600;font-size:.95em}
.gt-task .gt-label a:hover{text-decoration:underline}
.gt-task .gt-label .gt-tname{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px}
.gt-task .gt-label .gt-person{font-size:.85em;color:#94a3b8;margin-left:auto;white-space:nowrap}
.gt-task.gt-hidden{display:none}
.gt-bars{display:flex;position:relative;flex:1;min-height:26px}
.gt-cell{min-width:6px;border-right:1px solid #f8fafc00}
.gt-cell.gt-weekend{background:#f8fafc}
.gt-cell.gt-month-start{border-left:1px solid var(--border)}
.gt-bar{position:absolute;top:4px;height:18px;border-radius:4px;min-width:4px;cursor:pointer;transition:filter .12s;z-index:2;box-shadow:0 1px 4px rgba(0,0,0,.12)}
.gt-bar:hover{filter:brightness(1.15);box-shadow:0 2px 8px rgba(0,0,0,.2)}
.gt-bar-done{background:linear-gradient(90deg,#059669,#34d399)}
.gt-bar-late{background:linear-gradient(90deg,#dc2626,#f87171)}
.gt-bar-active{background:linear-gradient(90deg,#2563eb,#60a5fa)}
.gt-bar-noeta{background:linear-gradient(90deg,#94a3b8,#cbd5e1)}
.gt-bar-blocked{background:linear-gradient(90deg,#d97706,#fbbf24)}
.gt-bar-projected{border:2px dashed #94a3b8;background:#94a3b815;top:6px;height:14px}
.gt-bar-summary{background:linear-gradient(90deg,#1e40af33,#3b82f633);border-radius:4px;top:5px;height:16px;border:1px solid #3b82f644}
.gt-today-marker{position:absolute;top:0;bottom:0;width:2px;background:#dc2626;z-index:3;pointer-events:none;opacity:.8}
.gt-month-line{position:absolute;top:0;bottom:0;width:1px;background:#94a3b8;z-index:1;pointer-events:none;opacity:.6}
@media(max-width:900px){.top-strip{flex-direction:column}.strip-group{flex-direction:row;flex-wrap:wrap}.heatmap{font-size:.7em}.audit-table{font-size:.65em}}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>KPI Dashboard</h1>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <a href="https://linear.app/testbox/team/RAC/projects" target="_blank" class="linear-link"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M2.886 4.18A11.982 11.982 0 0 1 11.99 0C18.624 0 24 5.376 24 12.009c0 3.64-1.62 6.903-4.18 9.105L2.887 4.18ZM1.817 5.626l16.556 16.556c-.524.33-1.075.62-1.65.866L.951 7.277c.247-.575.537-1.126.866-1.65ZM.322 9.163l14.515 14.515c-.71.172-1.443.282-2.195.322L0 11.358a12 12 0 0 1 .322-2.195Zm-.17 4.862 9.823 9.824a12.02 12.02 0 0 1-9.824-9.824Z"/></svg>View in Linear</a>
      <a href="javascript:void(0)" onclick="showGuide()" class="linear-link" style="background:linear-gradient(135deg,#1e293b,#334155);border-color:#475569"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>Guide</a>
    </div>
  </div>
  <img src="https://cdn.prod.website-files.com/62f1899cd374937577f36d5f/6529d8cb022a253f2009f59a_testbox.svg" alt="TestBox" class="tbx-logo">
  <div class="filters">
    <label>Month</label><select id="fMonth" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;padding:5px 10px;border-radius:6px;font-size:.82em;cursor:pointer"><option value="ALL">All</option></select>
    <label>Person</label><select id="fPerson"><option value="ALL">All</option></select>
    <select id="fCategory" style="display:none"><option value="ALL">All</option><option value="Internal">Internal</option><option value="External">External</option></select>
    <button id="btnRefresh" onclick="refreshDashboard()" style="margin-left:12px;background:linear-gradient(135deg,#1e40af,#2563eb);border:1px solid #3b82f6;color:#fff;padding:6px 14px;border-radius:6px;font-size:.78em;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:all .15s;letter-spacing:.3px" onmouseover="this.style.background='linear-gradient(135deg,#1e3a8a,#1d4ed8)'" onmouseout="this.style.background='linear-gradient(135deg,#1e40af,#2563eb)'"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>Refresh Data</button>
    <span id="refreshDate" style="font-size:.72em;font-style:italic;color:#a7f3d0;margin-left:6px"></span>
  </div>
</div>

<div id="stalenessBanner"></div>

<div class="top-strip" id="topStrip">
  <div class="strip-group filters-group">
    <button class="segment-btn active" data-seg="ALL">All<span class="seg-count" id="segAll"></span></button>
    <button class="segment-btn" data-seg="Internal">Internal<span class="seg-count" id="segInt"></span></button>
    <button class="segment-btn" data-seg="External">External<span class="seg-count" id="segExt"></span></button>
  </div>
  <div class="strip-group kpi-group">
    <div class="kpi-cell kpi-active" id="kpiCell1" data-tab="accuracy"></div>
    <div class="kpi-cell" id="kpiCell2" data-tab="velocity"></div>
    <div class="kpi-cell" id="kpiCell3" data-tab="reliability"></div>
    <div class="kpi-cell" id="kpiCell4" data-tab="activity"></div>
  </div>
</div>

<div class="member-cards" id="memberCards"></div>

<div class="tabs" id="tabBar">
  <div class="tab active" data-tab="accuracy">ETA Accuracy</div>
  <div class="tab" data-tab="velocity">Execution Time</div>
  <div class="tab" data-tab="reliability">Reliability</div>
  <div class="tab" data-tab="activity">Team Activity</div>
  <div class="tab" data-tab="scrum">Scrum Copy</div>
  <div class="tab" data-tab="gantt">Gantt</div>
</div>

<div class="tab-panel active" id="panel-accuracy">
  <div class="audit-section" style="margin-top:0">
    <div class="audit-header collapse-toggle">
      <span class="toggle">&#9660;</span>
      <h3><span class="dot" style="background:var(--blue);position:relative;top:0"></span>ETA Accuracy<span class="info-btn" onmouseenter="showTip(event,'<b>ETA Accuracy</b><br><span class=tip-label>Formula</span>: On Time / (On Time + Late)<br><span class=tip-label>Target</span>: &gt;90%<br><span class=tip-label>Late</span>: Past ETA — delivered after deadline or not delivered yet<br><span class=tip-label>Not Started</span>: Backlog/Todo/Triage — ETA not applicable<br><span class=tip-label>Excludes</span>: No ETA, Not Started, On Track, Blocked, N/A')" onmouseleave="hideTip()" onclick="event.stopPropagation()">?</span></h3>
    </div>
    <div class="audit-body">
      <div class="trend-wrap" id="trend-accuracy"></div>
      <div style="overflow-x:auto"><table class="heatmap" id="grid-accuracy"></table></div>
    </div>
  </div>
</div>

<div class="tab-panel" id="panel-velocity">
  <div class="audit-section" style="margin-top:0">
    <div class="audit-header collapse-toggle">
      <span class="toggle">&#9660;</span>
      <h3><span class="dot" style="background:var(--yellow);position:relative;top:0"></span>Execution Time<span class="info-btn" onmouseenter="showTip(event,'<b>Avg Execution Time</b><br><span class=tip-label>Formula</span>: Average(Delivery - Start Date)<br><span class=tip-label>Start Date</span>: startedAt (In Progress) or dateAdd as fallback<br><span class=tip-label>Target</span>: &lt;28 days<br><span class=tip-label>Includes</span>: Only Done tasks with both dates<br><br>Measures implementation speed. Lower = faster delivery.')" onmouseleave="hideTip()" onclick="event.stopPropagation()">?</span></h3>
    </div>
    <div class="audit-body">
      <div class="trend-wrap" id="trend-velocity"></div>
      <div style="overflow-x:auto"><table class="heatmap" id="grid-velocity"></table></div>
    </div>
  </div>
</div>

<div class="tab-panel" id="panel-reliability">
  <div class="audit-section" style="margin-top:0">
    <div class="audit-header collapse-toggle">
      <span class="toggle">&#9660;</span>
      <h3><span class="dot" style="background:var(--dim);position:relative;top:0"></span>Implementation Reliability <span style="font-size:.6em;background:var(--gray-l);color:var(--dim);padding:2px 8px;border-radius:4px;font-weight:700">NOT ACTIVE</span><span class="info-btn" onmouseenter="showTip(event,'<b>Implementation Reliability — NOT ACTIVE</b><br><span class=tip-label>Formula</span>: Done without Rework / Total Done<br><span class=tip-label>Target</span>: &gt;90%<br><span class=tip-label>Rework</span>: Flagged via rework:implementation label in Linear<br><br><b style=color:#fbbf24>Status: No rework labels have been applied yet.</b><br>This metric will become active once the team starts using the rework:implementation label on Linear tickets that required rework after delivery.')" onmouseleave="hideTip()" onclick="event.stopPropagation()">?</span></h3>
    </div>
    <div class="audit-body">
      <div class="trend-wrap" id="trend-reliability"></div>
      <div style="overflow-x:auto"><table class="heatmap" id="grid-reliability"></table></div>
      <div style="margin-top:16px;padding:0 20px">
        <div style="font-weight:700;font-size:.9em;margin-bottom:8px"><span class="dot" style="background:var(--red);position:relative;top:0"></span>Rework Log</div>
        <div id="reworkLog"></div>
      </div>
    </div>
  </div>
</div>

<div class="tab-panel" id="panel-activity">
  <div class="audit-section" style="margin-top:0">
    <div class="audit-header collapse-toggle">
      <span class="toggle">&#9660;</span>
      <h3><span class="dot" style="background:var(--accent);position:relative;top:0"></span>Team Activity<span class="info-btn" onmouseenter="showTip(event,'<b>Task Volume</b><br><span class=tip-label>Shows</span>: Number of tasks per person per week<br><span class=tip-label>Includes</span>: All tasks regardless of status<br><span class=tip-label>Color</span>: Darker = more tasks')" onmouseleave="hideTip()" onclick="event.stopPropagation()">?</span></h3>
    </div>
    <div class="audit-body">
      <div class="trend-wrap" id="trend-activity"></div>
      <div style="overflow-x:auto"><table class="heatmap" id="grid-activity"></table></div>
    </div>
  </div>
</div>

<div class="tab-panel" id="panel-scrum">
  <div class="audit-section" style="margin-top:0">
    <div class="audit-header collapse-toggle">
      <span class="toggle">&#9660;</span>
      <h3><span class="dot" style="background:#8b5cf6;position:relative;top:0"></span>Scrum Copy<span style="font-size:.72em;color:var(--dim);font-weight:400;margin-left:8px">Click any card to copy to clipboard</span></h3>
    </div>
    <div class="audit-body">
      <div id="scrumCards" style="padding:16px 20px;display:grid;grid-template-columns:repeat(2,1fr);gap:12px"></div>
    </div>
  </div>
</div>

<div class="tab-panel" id="panel-gantt">
  <div style="background:var(--white);border:1px solid var(--border);border-radius:10px;margin-top:0">
    <div class="audit-header collapse-toggle" style="cursor:pointer" id="ganttCollapseHdr">
      <span class="toggle">&#9660;</span>
      <h3><span class="dot" style="background:#0ea5e9;position:relative;top:0"></span>Gantt Chart <span style="font-size:.6em;background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:4px;font-weight:700">WIP</span></h3>
    </div>
    <div id="ganttCollapseBody" style="display:none">
      <div id="ganttControls" style="padding:10px 20px;display:flex;gap:10px;align-items:center;flex-wrap:wrap">
        <label style="font-size:.72em;color:var(--dim);font-weight:600">Person</label>
        <select id="gtPerson" style="padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:.78em;background:var(--white);cursor:pointer">
          <option value="ALL">All People</option>
        </select>
        <label style="font-size:.72em;color:var(--dim);font-weight:600">View</label>
        <select id="gtView" style="padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:.78em;background:var(--white);cursor:pointer">
          <option value="ALL">All Tasks</option>
          <option value="implementing">Active Implementations</option>
        </select>
        <label style="font-size:.72em;color:var(--dim);font-weight:600">Customer</label>
        <select id="gtCustomer" style="padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:.78em;background:var(--white);cursor:pointer">
          <option value="ALL">All Customers</option>
        </select>
        <label style="font-size:.72em;color:var(--dim);font-weight:600">Demand</label>
        <select id="gtDemand" style="padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:.78em;background:var(--white);cursor:pointer">
          <option value="ALL">All</option>
          <option value="External">External</option>
          <option value="Internal">Internal</option>
        </select>
        <label style="font-size:.72em;color:var(--dim);font-weight:600">Status</label>
        <select id="gtStatus" style="padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:.78em;background:var(--white);cursor:pointer">
          <option value="ALL">All</option>
          <option value="active">Active Only</option>
        </select>
        <label style="font-size:.72em;color:var(--dim);font-weight:600">Period</label>
        <select id="gtPeriod" style="padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:.78em;background:var(--white);cursor:pointer">
          <option value="3m">Last 3 Months</option>
          <option value="1m">Last Month</option>
          <option value="6m" selected>Last 6 Months</option>
          <option value="all">All Time</option>
        </select>
        <span id="gtStats" style="font-size:.72em;color:var(--dim);margin-left:auto"></span>
      </div>
      <div id="ganttWrap" style="overflow:auto;max-height:600px;position:relative">
        <div id="ganttCanvas"></div>
      </div>
      <div id="ganttLegend" style="padding:8px 20px;display:flex;gap:14px;font-size:.7em;color:#64748b;flex-wrap:wrap">
        <span style="display:flex;align-items:center;gap:4px"><i style="display:inline-block;width:14px;height:10px;border-radius:2px;background:linear-gradient(90deg,#059669,#34d399)"></i> On Time</span>
        <span style="display:flex;align-items:center;gap:4px"><i style="display:inline-block;width:14px;height:10px;border-radius:2px;background:linear-gradient(90deg,#dc2626,#f87171)"></i> Late</span>
        <span style="display:flex;align-items:center;gap:4px"><i style="display:inline-block;width:14px;height:10px;border-radius:2px;background:linear-gradient(90deg,#2563eb,#60a5fa)"></i> Active</span>
        <span style="display:flex;align-items:center;gap:4px"><i style="display:inline-block;width:14px;height:10px;border-radius:2px;background:linear-gradient(90deg,#d97706,#fbbf24)"></i> Blocked</span>
        <span style="display:flex;align-items:center;gap:4px"><i style="display:inline-block;width:14px;height:10px;border-radius:2px;background:linear-gradient(90deg,#94a3b8,#cbd5e1)"></i> No ETA</span>
        <span style="display:flex;align-items:center;gap:4px"><i style="display:inline-block;width:14px;height:10px;border-radius:2px;border:2px dashed #94a3b8;background:#94a3b822"></i> Projected</span>
        <span style="color:#dc2626;font-weight:700">| Today</span>
      </div>
    </div>
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

<div class="audit-section" id="customerKPISection" style="margin-top:20px">
  <div class="audit-header" id="customerKPIToggle">
    <span class="toggle">&#9660;</span>
    <h3><span id="customerKPITitle">KPI by Customer</span><span class="info-btn" id="clientKpiInfo" onclick="event.stopPropagation()">?</span></h3>
  </div>
  <div class="audit-body" id="customerKPIBody">
    <div style="overflow-x:auto"><table class="heatmap" id="customerKPITable"></table></div>
  </div>
</div>

<div class="audit-section" id="auditSection">
  <div class="audit-header" id="auditToggle">
    <span class="toggle">&#9660;</span>
    <h3>Audit Data Table</h3>
    <div style="display:flex;align-items:center;gap:12px;margin-left:auto">
      <div style="display:flex;gap:6px;align-items:center" onclick="event.stopPropagation()">
        <select id="auditFilterPerson" style="background:var(--gray-bg);border:1px solid var(--border);border-radius:6px;padding:4px 8px;font-size:.72em;font-weight:600;color:var(--dim);cursor:pointer" onchange="renderAuditTable()">
          <option value="ALL">All People</option>
        </select>
        <select id="auditFilterWorkStatus" style="background:var(--gray-bg);border:1px solid var(--border);border-radius:6px;padding:4px 8px;font-size:.72em;font-weight:600;color:var(--dim);cursor:pointer" onchange="renderAuditTable()">
          <option value="ALL">All Status</option>
        </select>
        <select id="auditFilterPerf" style="background:var(--gray-bg);border:1px solid var(--border);border-radius:6px;padding:4px 8px;font-size:.72em;font-weight:600;color:var(--dim);cursor:pointer" onchange="renderAuditTable()">
          <option value="ALL">All Performance</option>
          <option value="On Time">On Time</option>
          <option value="Late">Late</option>
          <option value="On Track">On Track</option>
          <option value="No ETA">No ETA</option>
          <option value="Blocked">Blocked</option>
          <option value="N/A">N/A</option>
          <option value="Not Started">Not Started</option>
        </select>
        <select id="auditFilterCustomer" style="background:var(--gray-bg);border:1px solid var(--border);border-radius:6px;padding:4px 8px;font-size:.72em;font-weight:600;color:var(--dim);cursor:pointer" onchange="renderAuditTable()">
          <option value="ALL">All Customers</option>
        </select>
      </div>
      <div class="audit-tools">
        <button onclick="event.stopPropagation();downloadXLSX()">&#8681; XLSX</button>
        <button onclick="event.stopPropagation();copyTSV()">&#128203; Copy</button>
      </div>
    </div>
  </div>
  <div class="audit-body" id="auditBody">
    <table class="audit-table" id="auditTable"></table>
    <div class="audit-stats" id="auditStats"></div>
  </div>
</div>

<div class="footer">
  KPI Dashboard &nbsp;&middot;&nbsp; Source: Linear + Spreadsheet (backlog) &nbsp;&middot;&nbsp; Generated __DATE__ &nbsp;&middot;&nbsp; Latest data: __LATEST_DATA__
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

/* Compute period label for staleness banner */
let PERIOD_LABEL='';
if(CORE_WEEKS.length>0){
  const first=CORE_WEEKS[0],last=CORE_WEEKS[CORE_WEEKS.length-1];
  const[fy,fm]=parseWeek(first),[ly,lm]=parseWeek(last);
  PERIOD_LABEL=monthLabel(fy,fm)+' — '+monthLabel(ly,lm);
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

/* M11: Staleness indicator (inline next to Refresh button) */
(function(){
  const el=document.getElementById('refreshDate');
  const banner=document.getElementById('stalenessBanner');
  if(banner)banner.style.display='none';
  if(el)el.textContent='Last update: '+BUILD_DATE;
})();

/* ── State — M12: default to ALL ──────────────────── */
let state={person:'ALL',category:'ALL',month:'ALL'};
const charts={};

function getFiltered(){
  return RAW.filter(r=>{
    if(!r.week||!isCoreWeek(r.week))return false;
    if(state.person!=='ALL'&&r.tsa!==state.person)return false;
    if(state.category!=='ALL'&&r.category!==state.category)return false;
    if(state.month!=='ALL'){
      const[y,m]=parseWeek(r.week);
      if(monthLabel(y,m)!==state.month)return false;
    }
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

function refreshDashboard(){
  const btn=document.getElementById('btnRefresh');
  const orig=btn.innerHTML;
  if(!['localhost','127.0.0.1'].includes(location.hostname)){
    alert("For dashboard updates, please reach out to Thiago Rodrigues.");
    return;
  }
  btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13" style="animation:spin 1s linear infinite"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>Refreshing...';
  btn.disabled=true;btn.style.opacity='.7';
  fetch('/refresh',{method:'POST'}).then(r=>r.json()).then(d=>{
    if(d.success){
      btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><polyline points="20 6 9 17 4 12"/></svg>Done!';
      btn.style.background='linear-gradient(135deg,#065f46,#059669)';btn.style.opacity='1';
      setTimeout(()=>location.reload(),800);
    } else {
      btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>Error';
      btn.style.background='linear-gradient(135deg,#991b1b,#dc2626)';btn.style.opacity='1';
      setTimeout(()=>{btn.innerHTML=orig;btn.style.background='linear-gradient(135deg,#1e40af,#2563eb)';btn.disabled=false},3000);
    }
  }).catch(()=>{
    /* Server not running — try localhost:8787 in case file:// was opened directly */
    fetch('http://localhost:8787/refresh',{method:'POST'}).then(r=>r.json()).then(d=>{
      if(d.success){
        btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><polyline points="20 6 9 17 4 12"/></svg>Done! Redirecting...';
        btn.style.background='linear-gradient(135deg,#065f46,#059669)';btn.style.opacity='1';
        setTimeout(()=>{window.location.href='http://localhost:8787'},800);
      } else {
        btn.innerHTML='Error';btn.style.background='linear-gradient(135deg,#991b1b,#dc2626)';btn.style.opacity='1';
        setTimeout(()=>{btn.innerHTML=orig;btn.style.background='linear-gradient(135deg,#1e40af,#2563eb)';btn.disabled=false},3000);
      }
    }).catch(()=>{
      btn.style.opacity='1';btn.disabled=false;
      btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>Server offline';
      btn.style.background='linear-gradient(135deg,#991b1b,#dc2626)';
      navigator.clipboard.writeText('python kpi/serve_kpi.py');
      setTimeout(()=>{btn.innerHTML=orig+' <span style="font-size:.7em;opacity:.8">(start server first)</span>';btn.style.background='linear-gradient(135deg,#1e40af,#2563eb)'},2500);
    });
  });
}

function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/'/g,'&#39;').replace(/"/g,'&quot;').replace(/`/g,'&#96;')}

/* ── KPI Calculations ──────────────────────────────── */
function calcAccuracy(rows){
  const ot=rows.filter(r=>r.perf==='On Time').length;
  const lt=rows.filter(r=>r.perf==='Late').length;
  const d=ot+lt; /* H2: On Time / (On Time + Late) — no Overdue concept, past ETA = Late */
  return{val:d>0?ot/d:null,num:ot,den:d,n:rows.length,late:lt};
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

  let h1='<tr><th rowspan="2" style="text-align:left;min-width:120px;border-right:2px solid var(--border);background:var(--white);font-size:.72em;color:var(--light);font-weight:500;letter-spacing:.5px;padding-left:16px;position:sticky;left:0;z-index:3">TEAM</th>';
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

  /* Replace table node to clear old event listeners */
  const fresh=table.cloneNode(false);
  table.parentNode.replaceChild(fresh,table);
  fresh.innerHTML=`<thead>${h1}${h2}</thead><tbody>${bodyRows}${teamRow}</tbody>`;

  fresh.addEventListener('mouseenter',function(e){
    const td=e.target.closest('td[data-tip]');
    if(td){const html=tipCache[td.dataset.tip];if(html)showTip(e,html)}
  },true);
  fresh.addEventListener('mouseleave',function(e){
    const td=e.target.closest('td[data-tip]');
    if(td)hideTip();
  },true);
  fresh.addEventListener('mousemove',function(e){
    const td=e.target.closest('td[data-tip]');
    if(td&&tip.style.display==='block'){
      const x=Math.min(e.clientX+14,window.innerWidth-tip.offsetWidth-20);
      const y=Math.min(e.clientY-10,window.innerHeight-tip.offsetHeight-20);
      tip.style.left=x+'px';tip.style.top=Math.max(10,y)+'px';
    }
  },true);
}

/* ── Tip helpers ───────────────────────────────────── */
function fmtDate(d){if(!d||d.length<10)return'';const p=d.slice(0,10).split('-');return p[2]+'/'+p[1]}
function tipAccuracy(person,week,calc,rows){
  if(rows.length===0)return`<div class="tip-hdr"><b>${person}</b><span style="color:#64748b">${week}</span></div><span class="tip-label">No tasks this week</span>`;
  const pctCls=calc.val===null?'mid':calc.val>=.85?'good':calc.val>=.5?'mid':'bad';
  let html=`<div class="tip-hdr"><b>${person} &middot; ${week}</b><span class="tip-pct ${pctCls}">${fmtPct(calc.val,calc.den)}</span></div>`;
  html+=`<div class="tip-stats">`;
  html+=`<div class="tip-stat"><b style="color:#34d399">${calc.num}</b><span>on time</span></div>`;
  html+=`<div class="tip-stat"><b style="color:#f87171">${calc.late||0}</b><span>late</span></div>`;
  html+=`<div class="tip-stat"><b>${calc.den}</b><span>measured</span></div>`;
  html+=`</div>`;
  const excluded=rows.filter(r=>r.perf!=='On Time'&&r.perf!=='Late');
  if(excluded.length>0)html+=`<div style="font-size:.8em;color:#64748b;margin-top:2px">${excluded.length} excluded (${[...new Set(excluded.map(r=>r.perf))].join(', ')})</div>`;
  const lateOnes=rows.filter(r=>r.perf==='Late');
  if(lateOnes.length>0){
    html+=`<div class="tip-section"><span class="tip-label">Late</span>`;
    lateOnes.slice(0,5).forEach(r=>{
      const delay=r.eta&&r.delivery?daysBetween(r.eta,r.delivery):null;
      const cust=r.customer?`<span class="tip-cust">${esc(r.customer)}</span> &middot; `:'';
      const dates=r.eta?`<span class="tip-dates">ETA ${fmtDate(r.eta)}${r.delivery?' → '+fmtDate(r.delivery):''}</span>`:'';
      const delayTag=delay!==null&&delay>0?` <span class="tip-delay">+${delay}d</span>`:(!r.delivery?' <span class="tip-delay" style="color:#f87171">NOT DELIVERED</span>':'');
      const tid=r.ticketId?`<span style="color:#818cf8;font-size:.85em;font-weight:600">${esc(r.ticketId)}</span> `:'';
      html+=`<div class="tip-task tip-late">${tid}${cust}${esc(r.focus.slice(0,50))}${delayTag}<br>${dates}</div>`;
    });
    if(lateOnes.length>5)html+=`<div style="color:#64748b;font-size:.85em;padding-left:10px">+ ${lateOnes.length-5} more</div>`;
    html+=`</div>`;
  }
  const onTimeOnes=rows.filter(r=>r.perf==='On Time');
  if(onTimeOnes.length>0&&onTimeOnes.length<=3){
    html+=`<div class="tip-section"><span class="tip-label">On time</span>`;
    onTimeOnes.forEach(r=>{
      const cust=r.customer?`<span class="tip-cust">${esc(r.customer)}</span> &middot; `:'';
      const tid=r.ticketId?`<span style="color:#818cf8;font-size:.85em;font-weight:600">${esc(r.ticketId)}</span> `:'';
      html+=`<div class="tip-task tip-ontime">${tid}${cust}${esc(r.focus.slice(0,50))}</div>`;
    });
    html+=`</div>`;
  }
  return html;
}
function tipVelocity(person,week,calc,rows){
  if(rows.length===0)return`<div class="tip-hdr"><b>${person}</b><span style="color:#64748b">${week}</span></div><span class="tip-label">No tasks this week</span>`;
  if(calc.n===0)return`<div class="tip-hdr"><b>${person} &middot; ${week}</b></div>${rows.length} tasks, none with delivery dates`;
  const sorted=[...calc.durs].sort((a,b)=>a-b);
  const med=sorted[Math.floor(sorted.length/2)];
  const min=sorted[0],max=sorted[sorted.length-1];
  let html=`<div class="tip-hdr"><b>${person} &middot; ${week}</b><span class="tip-pct">${fmtDays(calc.val)}</span></div>`;
  html+=`<div class="tip-stats">`;
  html+=`<div class="tip-stat"><b>${med}d</b><span>median</span></div>`;
  html+=`<div class="tip-stat"><b>${min}d</b><span>fastest</span></div>`;
  html+=`<div class="tip-stat"><b>${max}d</b><span>slowest</span></div>`;
  html+=`<div class="tip-stat"><b>${calc.n}</b><span>tasks</span></div>`;
  html+=`</div>`;
  const slow=rows.filter(r=>r.delivery&&(r.startedAt||r.dateAdd)&&r.status==='Done').map(r=>({f:r.focus,c:r.customer||'',d:daysBetween(r.startedAt||r.dateAdd,r.delivery),eta:r.eta,del:r.delivery,start:r.startedAt||r.dateAdd})).filter(x=>x.d!==null&&x.d>=0).sort((a,b)=>b.d-a.d);
  if(slow.length>0&&slow[0].d>14){
    html+=`<div class="tip-section"><span class="tip-label">Slowest deliveries</span>`;
    slow.slice(0,4).forEach(x=>{
      const cust=x.c?`<span class="tip-cust">${esc(x.c)}</span> &middot; `:'';
      html+=`<div class="tip-task tip-late">${cust}${esc(x.f.slice(0,45))} <span class="tip-delay">${x.d}d</span><br><span class="tip-dates">${fmtDate(x.start)} → ${fmtDate(x.del)}</span></div>`;
    });
    html+=`</div>`;
  }
  return html;
}
function tipReliability(person,week,calc,rows){
  if(rows.length===0)return`<div class="tip-hdr"><b>${person}</b><span style="color:#64748b">${week}</span></div><span class="tip-label">No tasks this week</span>`;
  let html=`<div class="tip-hdr"><b>${person} &middot; ${week}</b><span class="tip-pct">${fmtPct(calc.val,calc.den)}</span></div>`;
  html+=`<div class="tip-stats">`;
  html+=`<div class="tip-stat"><b style="color:#34d399">${calc.num}</b><span>clean</span></div>`;
  html+=`<div class="tip-stat"><b style="color:#f87171">${calc.reworked}</b><span>rework</span></div>`;
  html+=`<div class="tip-stat"><b>${calc.den}</b><span>done</span></div>`;
  html+=`</div>`;
  if(calc.reworked===0&&calc.den>0)html+=`<div style="color:#fbbf24;font-size:.85em;margin-top:4px">No rework labels applied yet</div>`;
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

  /* Activity KPI */
  const act=calcActivity(data);
  const doneAct=data.filter(x=>x.status==='Done').length;
  const openAct=data.filter(x=>x.status!=='Done'&&x.status!=='Canceled').length;

  const items=[
    {el:'kpiCell1',name:'ETA Accuracy',val:a.val,fmt:v=>fmtPct(v,a.den),target:'>90%',pass:a.val!==null&&a.val>=.9,meta:`${a.num}/${a.den} on time, ${a.late||0} late`},
    {el:'kpiCell2',name:'Avg Execution Time',val:v.val,fmt:fmtDays,target:'<28 days',pass:v.val!==null&&v.val<=28,meta:`${v.n} tasks measured`},
    {el:'kpiCell3',name:'Reliability',val:hasReworkData?r.val:null,fmt:v=>fmtPct(v,r.den),target:'>90%',pass:hasReworkData&&r.val!==null&&r.val>=.9,inactive:!hasReworkData,meta:hasReworkData?`${r.num}/${r.den} clean`:'NOT ACTIVE'},
    {el:'kpiCell4',name:'Team Activity',val:act.val,fmt:fmtCount,pass:true,isActivity:true,meta:`${doneAct} done · ${openAct} open`},
  ];
  items.forEach(i=>{
    const cell=document.getElementById(i.el);
    const badge=i.inactive?'badge-inactive':i.isActivity?'badge-pass':(i.val===null?'badge-warn':(i.pass?'badge-pass':'badge-fail'));
    const badgeTxt=i.inactive?'N/A':i.isActivity?`${doneAct}`:( i.val===null?'—':(i.pass?'ON TARGET':'BELOW'));
    cell.innerHTML=`<div class="kc-name">${i.name}</div>
      <div class="kc-val">${i.inactive?'—':(i.val!==null?i.fmt(i.val):'—')}</div>
      <div class="kc-meta">${i.meta}</div>
      <div class="badge ${badge}">${i.isActivity?'&#10003; '+badgeTxt:badgeTxt}</div>`;
  });
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
  const bar3Label=barMode==='velocity'?'28-60d':barMode==='reliability'?'':'';
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
      bar3.push(0); /* Overdue merged into Late */
      bar4.push(rows.filter(r=>r.perf==='No ETA'||r.perf==='No Delivery Date').length);
    }
  });

  /* Build weekly task lookup for rich tooltips */
  const weekTaskDetail={};
  CORE_WEEKS.forEach((w,i)=>{
    const rows=data.filter(r=>r.week===w);
    weekTaskDetail[i]={
      onTime:rows.filter(r=>r.perf==='On Time').map(r=>({f:r.focus,c:r.customer||''})),
      late:rows.filter(r=>r.perf==='Late').map(r=>({f:r.focus,c:r.customer||'',d:r.eta&&r.delivery?daysBetween(r.eta,r.delivery):null})),
      overdue:[], /* merged into late */
      noEta:rows.filter(r=>r.perf==='No ETA'||r.perf==='No Delivery Date').map(r=>({f:r.focus,c:r.customer||''})),
    };
  });

  const datasets=[];
  datasets.push({type:'bar',label:bar1Label,data:bar1,backgroundColor:bar1Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});
  datasets.push({type:'bar',label:bar2Label,data:bar2,backgroundColor:bar2Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});
  if(bar3Label)datasets.push({type:'bar',label:bar3Label,data:bar3,backgroundColor:bar3Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});
  if(bar4Label)datasets.push({type:'bar',label:bar4Label,data:bar4,backgroundColor:bar4Color,borderRadius:2,yAxisID:'yBar',stack:'comp',order:2});

  datasets.push({type:'line',label:fmtLabel,data:teamVals,borderColor:color,backgroundColor:color+'22',borderWidth:1.5,fill:false,tension:.3,pointRadius:2,pointHoverRadius:5,pointBackgroundColor:color,yAxisID:'yLine',order:1,spanGaps:true});
  /* Target line removed — target is visible in KPI pill badges */

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
                const fmtVal=isInverse?val.toFixed(0)+'d':barMode==='activity'?val:(val*100).toFixed(0)+'%';
                return ` ${fmtLabel}: ${fmtVal}`;
              }
              return ' '+name+': '+ctx.raw;
            },
            afterBody:function(items){
              if(!items[0]||barMode==='velocity'||barMode==='reliability')return'';
              const idx=items[0].dataIndex;
              const wt=weekTaskDetail[idx];if(!wt)return'';
              const lines=[];
              if(wt.late.length>0){
                lines.push('','Late:');
                wt.late.slice(0,4).forEach(t=>{
                  const delay=t.d!==null&&t.d>0?' (+'+t.d+'d)':'';
                  const cust=t.c?' ['+t.c+']':'';
                  lines.push('  '+t.f.slice(0,40)+cust+delay);
                });
                if(wt.late.length>4)lines.push('  ... +'+(wt.late.length-4)+' more');
              }
              if(wt.overdue.length>0){
                lines.push('','Overdue:');
                wt.overdue.slice(0,3).forEach(t=>{
                  const cust=t.c?' ['+t.c+']':'';
                  lines.push('  '+t.f.slice(0,40)+cust);
                });
                if(wt.overdue.length>3)lines.push('  ... +'+(wt.overdue.length-3)+' more');
              }
              return lines.join('\n');
            }
          }
        }
      },
      scales:{
        yBar:{position:'left',stacked:true,ticks:{color:'#6b7280',font:{size:10},stepSize:1},grid:{color:'#e5e7eb88'},title:{display:true,text:'Tasks',color:'#9ca3af',font:{size:10}},beginAtZero:true},
        yLine:{position:'right',ticks:{color:color,font:{size:10},stepSize:isInverse?5:undefined,callback:function(v){return isInverse?v+'d':barMode==='activity'?v:(v*100).toFixed(0)+'%'}},grid:{drawOnChartArea:false},title:{display:true,text:fmtLabel,color:color,font:{size:10}},beginAtZero:true,min:0,max:barMode==='activity'?undefined:(isInverse?undefined:1)},
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
  if(rows.length===0)return`<div class="tip-hdr"><b>${person}</b><span style="color:#64748b">${week}</span></div><span class="tip-label">No tasks this week</span>`;
  let html=`<div class="tip-hdr"><b>${person} &middot; ${week}</b><span class="tip-pct">${calc.n}</span></div>`;
  html+=`<div class="tip-stats">`;
  html+=`<div class="tip-stat"><b style="color:#34d399">${calc.done}</b><span>done</span></div>`;
  html+=`<div class="tip-stat"><b style="color:#60a5fa">${calc.open}</b><span>open</span></div>`;
  if(calc.canceled>0)html+=`<div class="tip-stat"><b style="color:#94a3b8">${calc.canceled}</b><span>canceled</span></div>`;
  html+=`</div>`;
  if(rows.length<=8){
    html+=`<div class="tip-section"><span class="tip-label">Tasks</span>`;
    rows.forEach(r=>{
      const cls=r.status==='Done'?'tip-ontime':r.status==='Canceled'?'':'tip-late';
      const cust=r.customer?`<span class="tip-cust">${esc(r.customer)}</span> &middot; `:'';
      html+=`<div class="tip-task ${cls}">${cust}${esc(r.focus.slice(0,50))}</div>`;
    });
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
    const overdue=0; /* merged into Late */
    const noEta=pr.filter(r=>r.perf==='No ETA').length;
    const total=pr.length;
    const donePct=total>0?Math.round(done/total*100):0;

    /* H2: Same formula as KPI1 — On Time / (On Time + Late) */
    const measured=onTime+late;
    const accPct=measured>0?Math.round(onTime/measured*100):null;

    /* D.LIE12: ETA Coverage */
    const withEta=pr.filter(r=>r.eta&&r.eta.length>=10).length;
    const etaCov=total>0?Math.round(withEta/total*100):0;

    const recent=pr.filter(r=>{const lw=CORE_WEEKS.slice(-2);return lw.includes(r.week)}).length;

    let alert='';
    if(recent===0&&total>0)alert='<span class="mc-alert mc-alert-warn">NO RECENT</span>';
    else if(noEta>total*0.5)alert='<span class="mc-alert mc-alert-warn">'+noEta+' NO ETA</span>';
    else if(accPct!==null&&accPct>=85)alert='<span class="mc-alert mc-alert-ok">ON TRACK</span>';

    const barColor=donePct>=80?'var(--green)':donePct>=50?'var(--yellow)':'var(--red)';

    return`<div class="member-card">${alert}
      <div class="mc-name">${p}</div>
      <div class="mc-body">
        <div class="mc-row"><span title="All tickets assigned to this person in the selected period">Total</span><b>${total}</b></div>
        <div class="mc-row"><span title="Tickets marked as Done. Percentage is Done / Total">Done</span><b>${done} (${donePct}%)</b></div>
        <div class="mc-row"><span title="Active tickets (not Done or Canceled)">Open</span><b>${open}</b></div>
        <div class="mc-row"><span title="Delivered on or before the ETA deadline">On Time</span><b style="color:var(--green)">${onTime}</b></div>
        <div class="mc-row"><span title="Past ETA — delivered after deadline or still not delivered">Late</span><b style="color:${late>0?'var(--red)':'var(--dim)'}">${late}</b></div>
        <div class="mc-row"><span title="On Time / (On Time + Late). Excludes: No ETA, Not Started, Blocked, N/A">Accuracy</span><b>${accPct!==null?accPct+'%':'—'}</b></div>
        <div class="mc-row"><span title="% of tickets with an ETA date set. Yellow when below 50%">ETA Coverage</span><b style="color:${etaCov<50?'var(--yellow)':'var(--dim)'}">${etaCov}% (${withEta}/${total})</b></div>
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
  const cols=['Customer','Tasks','Done','On Time','Late','No ETA','ETA Accuracy','Avg Execution','Reliability'];
  let rowIdx=0;
  function kpiRow(label,rows,isTeam){
    const t=rows.length,dn=rows.filter(r=>r.status==='Done').length;
    const ot=rows.filter(r=>r.perf==='On Time').length,lt=rows.filter(r=>r.perf==='Late').length;
    const ne=rows.filter(r=>r.perf==='No ETA').length;
    const ad=ot+lt,acc=ad>0?ot/ad:null;
    const doneRows=rows.filter(r=>r.status==='Done');const rw=doneRows.filter(r=>r.rework==='yes').length;const rd=doneRows.length,rel=rd>0?(rd-rw)/rd:null;
    const ds=rows.filter(r=>r.delivery&&(r.startedAt||r.dateAdd)&&r.status==='Done').map(r=>daysBetween(r.startedAt||r.dateAdd,r.delivery)).filter(d=>d!==null&&d>=0);
    const avg=ds.length>0?ds.reduce((a,b)=>a+b,0)/ds.length:null;
    const cls=isTeam?' class="team-row"':'';
    const bg=isTeam?'':((rowIdx%2===0)?'background:#f9fafb;':'');
    const lbl=isTeam?`<td class="person-label">OVERALL</td>`:`<td class="person-label" style="${bg}">${label}</td>`;
    if(!isTeam)rowIdx++;
    return`<tr${cls}>${lbl}<td style="${bg}">${t}</td><td style="${bg}">${dn}</td><td style="${bg}color:var(--green);font-weight:600">${ot}</td><td style="${bg}color:${lt?'var(--red)':'var(--dim)'}">${lt}</td><td style="${bg}color:${ne?'var(--yellow)':'var(--dim)'}">${ne}</td><td class="cell ${acc!==null?heatPct(acc):'heat-na'}" style="font-weight:700">${fmtPct(acc,ad)}</td><td class="cell ${avg!==null?heatDays(avg):'heat-na'}" style="font-weight:700">${fmtDays(avg)}</td><td class="cell ${rel!==null?heatPct(rel):'heat-na'}" style="font-weight:700">${fmtPct(rel,rd)}</td></tr>`;
  }
  let h='<thead><tr>'+cols.map(c=>'<th>'+c+'</th>').join('')+'</tr></thead>';
  rowIdx=0;
  let b='<tbody>';
  custs.forEach(c=>{b+=kpiRow(c,base.filter(r=>r.customer===c),false)});
  b+=kpiRow('OVERALL',base,true);
  b+='</tbody>';
  el.innerHTML=h+b;
}

/* ── Audit table ──────────────────────────────────── */
let auditSortCol=0, auditSortAsc=true;

function getAuditRows(){
  const fPerson=document.getElementById('auditFilterPerson').value;
  const fWorkStatus=document.getElementById('auditFilterWorkStatus').value;
  const fPerf=document.getElementById('auditFilterPerf').value;
  const fCustomer=document.getElementById('auditFilterCustomer').value;
  let data=getFiltered();
  if(fPerson!=='ALL')data=data.filter(r=>r.tsa===fPerson);
  if(fWorkStatus!=='ALL')data=data.filter(r=>r.status===fWorkStatus);
  if(fPerf!=='ALL')data=data.filter(r=>r.perf===fPerf);
  if(fCustomer!=='ALL')data=data.filter(r=>(r.customer||'')===(fCustomer==='(empty)'?'':fCustomer));
  return data.map((r,i)=>{
    const start=r.startedAt||r.dateAdd;const dur=(r.delivery&&start)?daysBetween(start,r.delivery):null;
    return [i+1, r.tsa||'—', r.week||'—', r.ticketId||'—', r.focus||'—', r.status||'—', r.category||'—', r.demandType||'—', r.customer||'—', r.dateAdd||'—', r.eta||'—', r.delivery||'—', r.perf||'—', r.rework==='yes'?'YES':'—', dur!==null&&dur>=0?dur+'d':'—', r.source||'—', r.ticketUrl||'', r.milestone||'—', r.parentId||'—'];
  });
}
function populateAuditFilters(){
  const selP=document.getElementById('auditFilterPerson');
  const selS=document.getElementById('auditFilterWorkStatus');
  const selC=document.getElementById('auditFilterCustomer');
  const data=getFiltered();
  const curP=selP.value,curS=selS.value,curC=selC.value;

  const people=[...new Set(data.map(r=>r.tsa||''))].filter(Boolean).sort();
  selP.innerHTML='<option value="ALL">All People</option>';
  people.forEach(p=>{selP.innerHTML+=`<option value="${esc(p)}">${esc(p)}</option>`});
  selP.value=curP;

  const statuses=[...new Set(data.map(r=>r.status||''))].filter(Boolean).sort();
  selS.innerHTML='<option value="ALL">All Status</option>';
  statuses.forEach(s=>{selS.innerHTML+=`<option value="${esc(s)}">${esc(s)}</option>`});
  selS.value=curS;

  const custs=[...new Set(data.map(r=>r.customer||''))].sort();
  selC.innerHTML='<option value="ALL">All Customers</option>';
  custs.forEach(c=>{
    const label=c||'(empty)';
    selC.innerHTML+=`<option value="${c?esc(c):'(empty)'}">${esc(label)}</option>`;
  });
  selC.value=curC;
}

const AUDIT_COLS=['#','Person','Week','Ticket','Focus/Task','Status','Category','Demand Type','Customer','Date Added','ETA','Delivery','Performance','Rework','Duration','Source','Ticket URL','Milestone','Parent'];

function perfClass(v){
  if(v==='On Time')return'perf-on-time';if(v==='Late')return'perf-late';if(v==='On Track')return'perf-on-track';
  if(v==='Not Started')return'perf-not-started';
  return'perf-na';
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
  /* Overdue merged into Late */
  const done=sdata.filter(r=>r.status==='Done').length;
  const open=sdata.filter(r=>r.status!=='Done'&&r.status!=='Canceled').length;
  const reworkCount=sdata.filter(r=>r.rework==='yes').length;
  /* M13: Note about On Track exclusion */
  const onTrack=sdata.filter(r=>r.perf==='On Track').length;
  stats.innerHTML=`<span><b>${rows.length}</b> records</span><span>Done: <b>${done}</b></span><span>Open: <b>${open}</b></span><span style="color:var(--green)">On Time: <b>${onTime}</b></span><span style="color:var(--red)">Late: <b>${late}</b></span><span>On Track: <b>${onTrack}</b> (excluded)</span><span style="color:var(--red)">Rework: <b>${reworkCount}</b></span>`;
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

/* ── Dashboard Guide ────────────────────────────────── */
function showGuide(){
  const ov=document.createElement('div');
  ov.id='guideOverlay';
  ov.style.cssText='position:fixed;inset:0;background:rgba(15,23,42,.7);backdrop-filter:blur(4px);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px';
  ov.onclick=e=>{if(e.target===ov)ov.remove()};
  const box=document.createElement('div');
  box.style.cssText='background:#fff;border-radius:16px;max-width:860px;width:100%;max-height:92vh;overflow-y:auto;box-shadow:0 25px 80px rgba(0,0,0,.35);font-family:Inter,Segoe UI,sans-serif;color:#1e293b;line-height:1.7;font-size:14px';
  const S=`
    .g-hdr{background:linear-gradient(135deg,#064e3b,#065f46,#047857);color:#fff;padding:32px 40px 28px;border-radius:16px 16px 0 0;position:relative;overflow:hidden}
    .g-hdr::after{content:'';position:absolute;top:-40px;right:-40px;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.06)}
    .g-hdr::before{content:'';position:absolute;bottom:-60px;left:-20px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,.04)}
    .g-hdr h1{font-size:1.6em;font-weight:800;margin:0 0 4px;position:relative}
    .g-hdr p{font-size:.88em;opacity:.8;margin:0;position:relative}
    .g-close{position:absolute;top:16px;right:20px;background:rgba(255,255,255,.15);border:none;color:#fff;font-size:1.3em;width:36px;height:36px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s}
    .g-close:hover{background:rgba(255,255,255,.3)}
    .g-body{padding:28px 40px 36px}
    .g-section{margin-bottom:28px;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden}
    .g-section-hdr{display:flex;align-items:center;gap:12px;padding:14px 20px;background:linear-gradient(135deg,#f8fafc,#f1f5f9);border-bottom:1px solid #e2e8f0;cursor:default}
    .g-section-hdr .g-icon{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1em;flex-shrink:0}
    .g-section-hdr h2{font-size:1em;font-weight:700;color:#0f172a;margin:0;flex:1}
    .g-section-hdr .g-tag{font-size:.6em;font-weight:700;padding:2px 8px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px}
    .g-section-body{padding:16px 20px}
    .g-section-body p{margin:0 0 10px;color:#334155}
    .g-section-body ul,.g-section-body ol{margin:6px 0 12px 20px;color:#475569}
    .g-section-body li{margin-bottom:6px}
    .g-section-body li b{color:#0f172a}
    .g-section-body code{background:#f1f5f9;color:#6366f1;padding:1px 6px;border-radius:4px;font-size:.9em;font-weight:600}
    .g-formula{background:linear-gradient(135deg,#eff6ff,#e0e7ff);border:1px solid #c7d2fe;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:monospace;font-size:.92em;color:#4338ca;font-weight:600;text-align:center}
    .g-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}
    .g-grid-item{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 14px}
    .g-grid-item b{display:block;font-size:.92em;color:#0f172a;margin-bottom:2px}
    .g-grid-item span{font-size:.8em;color:#64748b}
    .g-badge{display:inline-flex;align-items:center;gap:4px;padding:2px 10px;border-radius:20px;font-size:.78em;font-weight:700;margin:0 3px}
    .g-pipe{display:flex;align-items:center;gap:0;margin:12px 0}
    .g-pipe-step{flex:1;text-align:center;padding:10px 6px;background:#f8fafc;border:1px solid #e2e8f0;position:relative;font-size:.78em}
    .g-pipe-step:first-child{border-radius:8px 0 0 8px}
    .g-pipe-step:last-child{border-radius:0 8px 8px 0}
    .g-pipe-step b{display:block;color:#0f172a;font-size:.95em;margin-bottom:2px}
    .g-pipe-step::after{content:"\\2192";position:absolute;right:-8px;top:50%;transform:translateY(-50%);color:#94a3b8;font-size:1.1em;z-index:1}
    .g-pipe-step:last-child::after{display:none}
    .g-color{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:middle;margin-right:6px;border:1px solid rgba(0,0,0,.1)}
    .g-footer{padding:20px 40px;background:#f8fafc;border-top:1px solid #e2e8f0;border-radius:0 0 16px 16px;text-align:center;font-size:.78em;color:#94a3b8}
  `;
  box.innerHTML=`<style>${S}</style>
    <div class="g-hdr">
      <button class="g-close" onclick="document.getElementById('guideOverlay').remove()">&times;</button>
      <h1>KPI Dashboard</h1>
      <p>Complete reference guide — every screen, metric, and interaction explained.</p>
    </div>
    <div class="g-body">

      <!-- 1. CONTROL STRIP -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#ecfdf5;color:#059669">&#9881;</div>
          <h2>Control Strip</h2>
          <span class="g-tag" style="background:#ecfdf5;color:#065f46">Filters + KPIs</span>
        </div>
        <div class="g-section-body">
          <p>The top strip is divided into two groups:</p>
          <div class="g-grid">
            <div class="g-grid-item" style="border-left:3px solid #059669">
              <b>Filters (green group)</b>
              <span><b>All</b> / <b>Internal</b> / <b>External</b> — click to filter every chart, heatmap, member card, and KPI by category. Counts update in real time.</span>
            </div>
            <div class="g-grid-item" style="border-left:3px solid #2563eb">
              <b>KPI Indicators (blue group)</b>
              <span>4 metrics that summarize team performance. <b>Click any KPI to jump to its detailed tab</b> below. The active KPI has a blue highlight.</span>
            </div>
          </div>
          <div class="g-grid" style="grid-template-columns:repeat(4,1fr)">
            <div class="g-grid-item" style="text-align:center">
              <b style="color:#2563eb">ETA Accuracy</b>
              <span>% delivered on or before ETA</span>
            </div>
            <div class="g-grid-item" style="text-align:center">
              <b style="color:#d97706">Execution Time</b>
              <span>Avg days from start to delivery</span>
            </div>
            <div class="g-grid-item" style="text-align:center">
              <b style="color:#6b7280">Reliability</b>
              <span>% without rework needed</span>
            </div>
            <div class="g-grid-item" style="text-align:center">
              <b style="color:#7c3aed">Team Activity</b>
              <span>Total tasks in period</span>
            </div>
          </div>
          <div class="g-formula">ETA Accuracy = On Time / (On Time + Late)<br><span style="font-size:.85em;color:#6366f1;font-weight:400">Late = past ETA (delivered or not). Excludes: On Track, No ETA, Not Started, Blocked (B.B.C), N/A</span></div>
        </div>
      </div>

      <!-- 2. STALENESS BANNER -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#ecfdf5;color:#059669">&#128337;</div>
          <h2>Data Freshness</h2>
          <span class="g-tag" style="background:#dbeafe;color:#1e40af">Auto-detected</span>
        </div>
        <div class="g-section-body">
          <p>The banner below the header shows how recent the data is:</p>
          <div style="display:flex;gap:8px;margin:8px 0 12px">
            <div style="flex:1;padding:8px 12px;border-radius:6px;background:#ecfdf5;border:1px solid #a7f3d0;text-align:center"><b style="color:#065f46;font-size:.85em"><span class="g-color" style="background:#059669"></span>Fresh</b><br><span style="font-size:.72em;color:#065f46">0-3 days</span></div>
            <div style="flex:1;padding:8px 12px;border-radius:6px;background:#fffbeb;border:1px solid #fde68a;text-align:center"><b style="color:#92400e;font-size:.85em"><span class="g-color" style="background:#d97706"></span>Aging</b><br><span style="font-size:.72em;color:#92400e">3-7 days</span></div>
            <div style="flex:1;padding:8px 12px;border-radius:6px;background:#fef2f2;border:1px solid #fecaca;text-align:center"><b style="color:#991b1b;font-size:.85em"><span class="g-color" style="background:#dc2626"></span>Stale</b><br><span style="font-size:.72em;color:#991b1b">&gt; 7 days</span></div>
          </div>
          <p>The <i>period label</i> (e.g. Nov 2025 — Mar 2026) is a <b>rolling 4-month window</b> computed automatically from today's date. No manual configuration needed — it always shows the most relevant time range.</p>
        </div>
      </div>

      <!-- 3. MEMBER CARDS -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#ede9fe;color:#7c3aed">&#128100;</div>
          <h2>Member Cards</h2>
          <span class="g-tag" style="background:#ede9fe;color:#6d28d9">Per-person</span>
        </div>
        <div class="g-section-body">
          <p>One card per team member, showing individual performance at a glance:</p>
          <div class="g-grid">
            <div class="g-grid-item"><b>Total / Done / Open</b><span>Task counts with completion %</span></div>
            <div class="g-grid-item"><b>On Time <span style="color:#059669">(green)</span></b><span>Delivered on or before ETA</span></div>
            <div class="g-grid-item"><b>Late <span style="color:#dc2626">(red)</span></b><span>Past ETA — delivered after deadline or not delivered yet</span></div>
            <div class="g-grid-item"><b>Accuracy</b><span>On Time / (On Time + Late). Hover heatmap cells for detail</span></div>
            <div class="g-grid-item"><b>ETA Coverage</b><span>% of tasks with ETA set. <span style="color:#d97706">Yellow</span> if &lt; 50%</span></div>
            <div class="g-grid-item"><b>Progress Bar</b><span>Visual completion rate — green &ge; 80%, yellow &ge; 50%, red &lt; 50%</span></div>
          </div>
          <p style="margin-top:12px"><b>Badges:</b>
            <span class="g-badge" style="background:#d1fae5;color:#065f46">ON TRACK</span> accuracy &ge; 85%
            <span class="g-badge" style="background:#fef3c7;color:#92400e">NO RECENT</span> no tasks in last 2 weeks
            <span class="g-badge" style="background:#fef3c7;color:#92400e">X NO ETA</span> &gt; 50% tasks lack ETA
          </p>
        </div>
      </div>

      <!-- 4. TABS -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#dbeafe;color:#2563eb">&#128200;</div>
          <h2>Analysis Tabs</h2>
          <span class="g-tag" style="background:#dbeafe;color:#1e40af">4 views</span>
        </div>
        <div class="g-section-body">
          <p>Each tab provides two synchronized views of the same metric:</p>
          <div class="g-grid">
            <div class="g-grid-item" style="border-left:3px solid #4f46e5">
              <b>Weekly Trend Chart</b>
              <span>Stacked bars show the breakdown per week (On Time vs Late vs No ETA). A line traces the overall metric value across weeks.</span>
              <br><span style="font-size:.78em;color:#6366f1;font-weight:600;margin-top:4px;display:inline-block">Hover any bar for task-level detail: task name, customer, and delay days.</span>
            </div>
            <div class="g-grid-item" style="border-left:3px solid #059669">
              <b>Heatmap Grid</b>
              <span>Person x Week matrix with color-coded cells. Hover any cell for full breakdown including individual task names and statuses.</span>
              <br><span style="font-size:.78em;color:#059669;font-weight:600;margin-top:4px;display:inline-block">Colors: green = good, yellow = warning, red = needs attention.</span>
            </div>
          </div>
          <div class="g-grid" style="grid-template-columns:repeat(4,1fr);margin-top:10px">
            <div class="g-grid-item" style="text-align:center;background:#eef2ff"><b style="color:#4f46e5;font-size:.85em">ETA Accuracy</b><br><span style="font-size:.72em">On Time vs Late</span></div>
            <div class="g-grid-item" style="text-align:center;background:#fffbeb"><b style="color:#b45309;font-size:.85em">Execution Time</b><br><span style="font-size:.72em">&lt;14d / 14-28d / 28-60d / &gt;60d</span></div>
            <div class="g-grid-item" style="text-align:center;background:#ecfdf5"><b style="color:#047857;font-size:.85em">Reliability</b><br><span style="font-size:.72em">Clean vs Rework</span></div>
            <div class="g-grid-item" style="text-align:center;background:#f5f3ff"><b style="color:#7c3aed;font-size:.85em">Team Activity</b><br><span style="font-size:.72em">Task volume per week</span></div>
          </div>
        </div>
      </div>

      <!-- 5. KPI BY CUSTOMER -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#fef3c7;color:#d97706">&#127970;</div>
          <h2>KPI by Customer</h2>
          <span class="g-tag" style="background:#fef3c7;color:#92400e">Drill-down</span>
        </div>
        <div class="g-section-body">
          <p>Table showing per-customer metrics: <b>accuracy</b>, <b>avg execution time</b>, <b>reliability</b>, and <b>task count</b>. Color-coded cells use the same heat scale as the main heatmaps.</p>
          <p>The table automatically switches between <b>External customers</b> and <b>Internal contexts</b> based on the active segment filter.</p>
        </div>
      </div>

      <!-- 6. AUDIT TABLE -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#f1f5f9;color:#475569">&#128203;</div>
          <h2>Audit Data Table</h2>
          <span class="g-tag" style="background:#f1f5f9;color:#475569">Expandable</span>
        </div>
        <div class="g-section-body">
          <p>Click to expand. Full record-level table with <b>19 columns</b>. Click any column header to sort. Two export options in the header:</p>
          <div class="g-grid">
            <div class="g-grid-item"><b>XLSX Export</b><span>Downloads a formatted Excel file with all visible records, hyperlinked ticket IDs</span></div>
            <div class="g-grid-item"><b>Copy TSV</b><span>Copies tab-separated data to clipboard for pasting into spreadsheets</span></div>
          </div>
          <p style="margin-top:10px"><b>Performance Labels:</b></p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin:6px 0">
            <span class="g-badge" style="background:#d1fae5;color:#065f46">On Time</span>
            <span class="g-badge" style="background:#fee2e2;color:#991b1b">Late</span>
            <span class="g-badge" style="background:#f3f4f6;color:#6b7280">No ETA</span>
            <span class="g-badge" style="background:#dbeafe;color:#1e40af">On Track</span>
            <span class="g-badge" style="background:#fce7f3;color:#9d174d">Blocked (B.B.C)</span>
            <span class="g-badge" style="background:#ede9fe;color:#7c3aed">Not Started</span>
            <span class="g-badge" style="background:#f3f4f6;color:#9ca3af">N/A (Canceled)</span>
          </div>
          <p style="margin-top:8px;font-size:.88em;color:#64748b">
            <b>Late</b> = ETA passed (delivered after or not delivered yet). <b>No ETA</b> = active work without a due date set. <b>Not Started</b> = ticket in Backlog/Todo/Triage — ETA not applicable yet. <b>B.B.C</b> = Blocked By Customer — excluded from accuracy. <b>N/A</b> = Canceled or not measurable.
          </p>
        </div>
      </div>

      <!-- 7. REWORK LOG -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#fef2f2;color:#dc2626">&#128260;</div>
          <h2>Rework Log</h2>
          <span class="g-tag" style="background:#fef2f2;color:#991b1b">Quality</span>
        </div>
        <div class="g-section-body">
          <p>Lists tickets flagged with the <code>rework:implementation</code> label in Linear. Shows ticket link, person, customer, and delivery date.</p>
          <p>This section feeds the <b>Reliability KPI</b>. When rework labels are applied in Linear, the KPI3 pill activates automatically and starts tracking the clean delivery rate.</p>
        </div>
      </div>

      <!-- 8. DATA PIPELINE -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#e0e7ff;color:#4338ca">&#9881;</div>
          <h2>Data Pipeline</h2>
          <span class="g-tag" style="background:#e0e7ff;color:#3730a3">Technical</span>
        </div>
        <div class="g-section-body">
          <p>The dashboard is generated by a <b>4-step Python pipeline</b>, each step feeding the next:</p>
          <div class="g-pipe">
            <div class="g-pipe-step" style="background:#eef2ff"><b>1. Refresh</b>Linear API &rarr; cache</div>
            <div class="g-pipe-step" style="background:#ecfdf5"><b>2. Merge</b>Linear + spreadsheet</div>
            <div class="g-pipe-step" style="background:#fffbeb"><b>3. Normalize</b>Clean &amp; fix data</div>
            <div class="g-pipe-step" style="background:#fce7f3"><b>4. Build</b>Generate HTML</div>
          </div>
          <p>Run the full pipeline:</p>
          <div class="g-formula" style="background:#1e293b;color:#a5f3fc;border-color:#334155;text-align:left;font-size:.88em">
            <span style="color:#94a3b8">$</span> python kpi/orchestrate.py<br>
            <span style="color:#94a3b8">$</span> python kpi/orchestrate.py --skip-refresh &nbsp;<span style="color:#64748b"># reuse cached API data</span><br>
            <span style="color:#94a3b8">$</span> python kpi/orchestrate.py --build-only &nbsp;&nbsp;<span style="color:#64748b"># rebuild HTML only</span>
          </div>
          <p style="font-size:.85em;color:#64748b">All writes are <b>atomic</b> (write to .tmp, then replace). Pipeline stops on first error. Each step has a 120s timeout.</p>
        </div>
      </div>

      <!-- 9. GLOSSARY -->
      <div class="g-section">
        <div class="g-section-hdr">
          <div class="g-icon" style="background:#f0fdf4;color:#16a34a">&#128218;</div>
          <h2>Glossary</h2>
          <span class="g-tag" style="background:#f0fdf4;color:#166534">Reference</span>
        </div>
        <div class="g-section-body">
          <div class="g-grid">
            <div class="g-grid-item"><b>ETA</b><span>Due date set in Linear — the committed delivery date</span></div>
            <div class="g-grid-item"><b>On Time</b><span>Delivered on or before ETA</span></div>
            <div class="g-grid-item"><b>Late</b><span>Past ETA — delivered after deadline or still not delivered</span></div>
            <div class="g-grid-item"><b>No ETA</b><span>Active work (In Progress/Done) without a due date set</span></div>
            <div class="g-grid-item"><b>Not Started</b><span>Ticket in Backlog/Todo/Triage — ETA not applicable yet</span></div>
            <div class="g-grid-item"><b>On Track</b><span>In progress, ETA is in the future</span></div>
            <div class="g-grid-item"><b>B.B.C</b><span>Blocked By Customer — excluded from accuracy</span></div>
            <div class="g-grid-item"><b>Core Week</b><span>A week within the rolling 4-month window</span></div>
            <div class="g-grid-item"><b>Rework</b><span>Task re-implemented after delivery (rework:implementation label)</span></div>
            <div class="g-grid-item"><b>Velocity</b><span>Days between start (In Progress) and delivery (In Review/Done)</span></div>
            <div class="g-grid-item"><b>Source: Linear</b><span>Live data from Linear API — primary source</span></div>
            <div class="g-grid-item"><b>Source: Spreadsheet</b><span>Historical backlog from CODA/sheets</span></div>
          </div>
        </div>
      </div>

    </div>
    <div class="g-footer">
      KPI Dashboard v3 &middot; Built ${BUILD_DATE} &middot; Team Raccoons &middot; Powered by Linear + Python + Chart.js
    </div>
  `;
  ov.appendChild(box);
  document.body.appendChild(ov);
}

/* ── Render all ─────────────────────────────────────── */
let _renderTimer=null;
function debouncedRender(){clearTimeout(_renderTimer);_renderTimer=setTimeout(render,150)}
function render(){
  Object.keys(tipCache).forEach(k => delete tipCache[k]);
  tipCounter = 0;
  const activeTab=document.querySelector('.tab.active');
  const activeTabName=activeTab?activeTab.dataset.tab:'accuracy';
  /* Always-run: shared across all tabs */
  updateSegmentCounts();
  renderMemberCards();
  renderKPIStrip();
  populateAuditFilters();
  renderAuditTable();
  renderReworkLog();
  renderCustomerKPI();
  /* Per-tab lazy rendering: only build the currently visible tab */
  if(activeTabName==='accuracy'){
    buildGrid('grid-accuracy',calcAccuracy,fmtPct,heatPct,tipAccuracy);
    renderTrend('trend-accuracy',calcAccuracy,'ETA Accuracy','#4f46e5',.9,'Target 90%',false,'accuracy');
  }
  if(activeTabName==='velocity'){
    buildGrid('grid-velocity',calcVelocity,fmtDays,heatDays,tipVelocity);
    renderTrend('trend-velocity',calcVelocity,'Execution Time','#b45309',28,'Target 28d',true,'velocity');
  }
  if(activeTabName==='reliability'){
    buildGrid('grid-reliability',calcReliability,fmtPct,heatPct,tipReliability);
    renderTrend('trend-reliability',calcReliability,'Reliability','#047857',.9,'Target 90%',false,'reliability');
  }
  if(activeTabName==='activity'){
    buildGrid('grid-activity',calcActivity,fmtCount,heatVol,tipActivity);
    renderTrend('trend-activity',calcActivity,'Task Volume','#4338ca',5,'Avg 5/week',false,'activity');
  }
  if(activeTabName==='scrum'){
    renderScrumCards();
  }
  /* Only render Gantt when its tab is active — expensive DOM rebuild */
  const ganttPanel=document.getElementById('panel-gantt');
  if(ganttPanel&&ganttPanel.classList.contains('active'))renderGantt();
}

/* ── Gantt Chart ─────────────────────────────────── */
const GT_DAY_W=6;
const gtCollapsed={};

function gtGetFiltered(){
  const gtPerson=document.getElementById('gtPerson').value;
  const view=document.getElementById('gtView').value;
  const customer=document.getElementById('gtCustomer').value;
  const demand=document.getElementById('gtDemand').value;
  const gtStatus=document.getElementById('gtStatus').value;
  const period=document.getElementById('gtPeriod').value;
  let cutoff=null;
  if(period!=='all'){const d=new Date();d.setMonth(d.getMonth()-(period==='1m'?1:period==='3m'?3:6));cutoff=d.toISOString().slice(0,10)}

  let activeCustomers=null;
  if(view==='implementing'){
    activeCustomers=new Set();
    RAW.forEach(r=>{
      if(['In Progress','In Review','Production QA','Ready to Deploy'].includes(r.status)&&r.customer)activeCustomers.add(r.customer);
    });
  }

  return RAW.filter(r=>{
    const s=r.startedAt||r.dateAdd||'';
    if(!s||s<'2025-01-01')return false;
    if(r.status==='Canceled')return false;
    const pf=gtPerson!=='ALL'?gtPerson:state.person;
    if(pf!=='ALL'&&r.tsa!==pf)return false;
    if(customer!=='ALL'&&r.customer!==customer)return false;
    if(demand!=='ALL'&&r.category!==demand)return false;
    if(gtStatus==='active'&&(r.status==='Done'||r.status==='Canceled'))return false;
    if(gtStatus!=='ALL'&&gtStatus!=='active'&&r.status!==gtStatus)return false;
    if(view==='implementing'&&activeCustomers&&!activeCustomers.has(r.customer))return false;
    const e=r.delivery||r.eta||'';
    if(cutoff&&(s||'9999')<cutoff&&(e||'9999')<cutoff)return false;
    return true;
  });
}

function gtBarCls(r){
  if(r.perf==='Blocked'||r.status==='B.B.C')return'gt-bar-blocked';
  if(r.status==='Done')return r.perf==='Late'?'gt-bar-late':'gt-bar-done';
  if(['In Progress','In Review','Production QA','Ready to Deploy','Paused'].includes(r.status))return'gt-bar-active';
  return'gt-bar-noeta';
}

function gtTipHtml(r){
  const cls=r.perf==='On Time'?'good':r.perf==='Late'?'bad':'mid';
  const s=r.startedAt||r.dateAdd,e=r.delivery||r.eta;
  const dur=(s&&e)?daysBetween(s,e):null;
  let h='<b>'+esc(r.focus||'')+'</b>'+(r.customer?' ['+esc(r.customer)+']':'')+'<br>';
  h+='<span style="color:#94a3b8">Person:</span> '+esc(r.tsa||'')+'<br>';
  h+='<span style="color:#94a3b8">Status:</span> <span class="tip-pct '+cls+'">'+esc(r.status||'')+'</span> · '+esc(r.perf||'')+'<br>';
  h+='<span style="color:#94a3b8">Start:</span> '+esc(s||'\u2014')+' · <span style="color:#94a3b8">ETA:</span> '+esc(r.eta||'\u2014')+' · <span style="color:#94a3b8">Done:</span> '+esc(r.delivery||'\u2014')+'<br>';
  if(dur!==null)h+='<span style="color:#94a3b8">Duration:</span> '+dur+'d<br>';
  if(r.ticketId)h+='<span style="color:#94a3b8">Ticket:</span> '+esc(r.ticketId||'');
  return h;
}

function gtToggleGroup(el){
  el.classList.toggle('gt-open');
  const gid=el.dataset.gtgrp;
  if(!gid)return;
  gtCollapsed[gid]=!el.classList.contains('gt-open');
  document.querySelectorAll('.gt-task[data-gtgrp="'+gid+'"]').forEach(r=>r.classList.toggle('gt-hidden'));
}

function renderGantt(){
  const data=gtGetFiltered();
  const todayStr=new Date().toISOString().slice(0,10);

  function pd(s){if(!s||s.length<10)return null;return new Date(s.slice(0,10)+'T12:00:00Z')}
  function db(a,b){return Math.round((b-a)/864e5)}

  /* Date range */
  let minD=todayStr,maxD=todayStr;
  data.forEach(r=>{
    const s=r.startedAt||r.dateAdd||'';
    const e=r.delivery||r.eta||s;
    if(s&&s<minD)minD=s;if(e&&e>maxD)maxD=e;if(s&&s>maxD)maxD=s;
  });
  const sd=pd(minD),ed=pd(maxD);
  if(!sd||!ed){document.getElementById('ganttCanvas').innerHTML='<p style="padding:20px;color:var(--dim)">No data for Gantt chart.</p>';return}
  sd.setDate(sd.getDate()-5);ed.setDate(ed.getDate()+10);
  const totalDays=db(sd,ed)+1;

  /* Build day index */
  const days=[];
  for(let i=0;i<totalDays;i++){const d=new Date(sd);d.setDate(d.getDate()+i);days.push(d)}
  function dayIdx(dateStr){const d=pd(dateStr);if(!d)return-1;return db(sd,d)}

  /* Group by customer */
  const groups={};
  data.forEach(r=>{const c=r.customer||'No Customer';if(!groups[c])groups[c]=[];groups[c].push(r)});
  const sortedGroups=Object.entries(groups).sort((a,b)=>b[1].length-a[1].length);

  /* Month spans */
  const mNames=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const months=[];let curM=-1,curY=-1,curCount=0;
  days.forEach(d=>{
    if(d.getMonth()!==curM||d.getFullYear()!==curY){
      if(curCount>0)months.push({label:mNames[curM]+' '+curY,days:curCount});
      curM=d.getMonth();curY=d.getFullYear();curCount=0;
    }
    curCount++;
  });
  if(curCount>0)months.push({label:mNames[curM]+' '+curY,days:curCount});

  /* Month header */
  let html='<div class="gt-months"><div class="gt-label-col"><span>Customer / Task</span></div>';
  months.forEach(m=>{html+='<div class="gt-month-cell" style="min-width:'+m.days*GT_DAY_W+'px;max-width:'+m.days*GT_DAY_W+'px">'+m.label+'</div>'});
  html+='</div>';

  /* Day header */
  html+='<div class="gt-header"><div class="gt-label-col"><span></span></div><div class="gt-days">';
  days.forEach(d=>{
    const ds=d.toISOString().slice(0,10);
    const dow=d.getDay();const isWe=dow===0||dow===6;const isMs=d.getDate()===1;const isToday=ds===todayStr;
    let cls=isWe?'gt-day gt-weekend':'gt-day';
    if(isMs)cls+=' gt-month-start';if(isToday)cls+=' gt-today-col';
    const label=(d.getDate()%7===1||d.getDate()===1)?d.getDate():'';
    html+='<div class="'+cls+'" style="min-width:'+GT_DAY_W+'px;max-width:'+GT_DAY_W+'px">'+label+'</div>';
  });
  html+='</div></div>';

  /* Month divider positions */
  const monthDividers=[];
  days.forEach((d,i)=>{if(d.getDate()===1)monthDividers.push(i)});
  function mLines(){return monthDividers.map(i=>'<div class="gt-month-line" style="left:'+i*GT_DAY_W+'px"></div>').join('')}

  /* Groups */
  sortedGroups.forEach(([cust,tasks])=>{
    tasks.sort((a,b)=>(a.startedAt||a.dateAdd||'z').localeCompare(b.startedAt||b.dateAdd||'z'));

    const done=tasks.filter(t=>t.status==='Done').length;
    const active=tasks.filter(t=>['In Progress','In Review','Todo','Paused','Production QA'].includes(t.status)).length;
    const late=tasks.filter(t=>t.perf==='Late').length;
    const onTime=tasks.filter(t=>t.perf==='On Time').length;
    const tbd=tasks.filter(t=>!t.eta&&t.status!=='Done'&&t.status!=='Canceled').length;

    /* Summary bar range */
    let gMin=null,gMax=null;
    tasks.forEach(t=>{
      const s=t.startedAt||t.dateAdd||'';const e=t.delivery||t.eta||s;
      if(s&&(!gMin||s<gMin))gMin=s;if(e&&(!gMax||e>gMax))gMax=e;
    });
    const gStartIdx=dayIdx(gMin);const gEndIdx=dayIdx(gMax);
    const gLen=Math.max(1,gEndIdx-gStartIdx+1);

    const gid='gt_'+cust.replace(/[^a-zA-Z0-9]/g,'_');
    const isOpen=!gtCollapsed[gid];

    html+='<div class="gt-row gt-group'+(isOpen?' gt-open':'')+'" data-gtgrp="'+gid+'" onclick="gtToggleGroup(this)">';
    html+='<div class="gt-label">';
    html+='<span class="gt-arrow">&#9654;</span>';
    html+='<span>'+esc(cust)+'</span>';
    html+='<span class="gt-count">'+tasks.length+'</span>';
    html+='<div class="gt-badges">';
    if(onTime)html+='<span class="gt-badge" style="background:#d1fae5;color:#065f46">'+onTime+' ok</span>';
    if(late)html+='<span class="gt-badge" style="background:#fee2e2;color:#991b1b">'+late+' late</span>';
    if(active)html+='<span class="gt-badge" style="background:#dbeafe;color:#1e40af">'+active+' active</span>';
    if(tbd)html+='<span class="gt-badge" style="background:#bfdbfe;color:#1e3a8a">'+tbd+' TBD</span>';
    html+='</div></div>';

    /* Summary bar area */
    html+='<div class="gt-bars" style="min-width:'+totalDays*GT_DAY_W+'px">';
    html+=mLines();
    if(gStartIdx>=0)html+='<div class="gt-bar gt-bar-summary" style="left:'+gStartIdx*GT_DAY_W+'px;width:'+gLen*GT_DAY_W+'px"></div>';
    const tIdx=dayIdx(todayStr);
    if(tIdx>=0&&tIdx<totalDays)html+='<div class="gt-today-marker" style="left:'+tIdx*GT_DAY_W+'px"></div>';
    html+='</div></div>';

    /* Task rows */
    let lastPerson='';
    tasks.sort((a,b)=>{const pc=(a.tsa||'').localeCompare(b.tsa||'');return pc!==0?pc:(a.startedAt||a.dateAdd||'z').localeCompare(b.startedAt||b.dateAdd||'z')});
    tasks.forEach(t=>{
      const s=t.startedAt||t.dateAdd||'';const e=t.delivery||t.eta||'';
      let si=dayIdx(s),ei=dayIdx(e||s);
      si=Math.max(0,Math.min(si,totalDays-1));ei=Math.max(0,Math.min(ei,totalDays-1));
      const len=Math.max(1,ei-si+1);
      const cls=gtBarCls(t);
      const isProj=!t.delivery&&t.eta&&t.status!=='Done';
      const bCls=cls+(isProj?' gt-bar-projected':'');
      const tHtml=gtTipHtml(t);
      const focusTxt=t.focus||'';

      html+='<div class="gt-row gt-task'+(isOpen?'':' gt-hidden')+'" data-gtgrp="'+gid+'">';
      html+='<div class="gt-label">';
      if(t.ticketUrl&&t.ticketUrl.startsWith('http'))html+='<a href="'+esc(t.ticketUrl)+'" target="_blank">'+esc(t.ticketId||'')+'</a>';
      else if(t.ticketId)html+='<span>'+esc(t.ticketId)+'</span>';
      html+='<span class="gt-tname" title="'+esc(focusTxt)+'">'+esc(focusTxt.length>35?focusTxt.slice(0,33)+'...':focusTxt)+'</span>';
      const showPerson=(t.tsa||'')!==lastPerson;lastPerson=t.tsa||'';
      if(showPerson)html+='<span class="gt-person">'+esc(t.tsa||'')+'</span>';
      html+='</div>';

      html+='<div class="gt-bars" style="min-width:'+totalDays*GT_DAY_W+'px">';
      html+=mLines();
      if(si<=totalDays&&ei>=0){
        html+='<div class="gt-bar '+bCls+'" style="left:'+si*GT_DAY_W+'px;width:'+len*GT_DAY_W+'px" onmouseenter="showTip(event,this.dataset.tip)" onmousemove="showTip(event,this.dataset.tip)" onmouseleave="hideTip()" data-tip="'+esc(tHtml)+'"></div>';
      }
      html+='</div></div>';
    });
  });

  document.getElementById('ganttCanvas').innerHTML=html;

  /* Stats */
  const doneC=data.filter(r=>r.status==='Done').length;
  const activeC=data.filter(r=>['In Progress','In Review','Todo','Paused'].includes(r.status)).length;
  document.getElementById('gtStats').innerHTML=data.length+' tasks · '+doneC+' done · '+activeC+' active · '+sortedGroups.length+' customers';

  /* Scroll listener for hiding tooltip */
  const wrap=document.getElementById('ganttWrap');
  wrap.removeEventListener('scroll',hideTip);
  wrap.addEventListener('scroll',hideTip);
}

/* Gantt: populate Customer filter dynamically + Status filter */
(function(){
  const gtCustEl=document.getElementById('gtCustomer');
  const gtStatusEl=document.getElementById('gtStatus');
  const gtPersonEl=document.getElementById('gtPerson');
  if(gtPersonEl){
    PEOPLE_ALL.forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;gtPersonEl.appendChild(o)});
  }
  if(gtCustEl){
    const custs=[...new Set(RAW.map(r=>r.customer).filter(Boolean))].sort();
    custs.forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;gtCustEl.appendChild(o)});
  }
  if(gtStatusEl){
    const sts=[...new Set(RAW.map(r=>r.status).filter(Boolean))].sort();
    sts.forEach(s=>{const o=document.createElement('option');o.value=s;o.textContent=s;gtStatusEl.appendChild(o)});
  }
})();

/* Gantt-specific filter change handlers */
['gtPerson','gtView','gtPeriod','gtCustomer','gtDemand','gtStatus'].forEach(id=>{
  const el=document.getElementById(id);
  if(el)el.addEventListener('change',function(){renderGantt()});
});

function renderScrumCards(){
  const todayStr=new Date().toISOString().slice(0,10);
  const today=new Date(todayStr);

  /* Split: active (In Progress/In Review/Paused/Todo) + completed today — respects person filter */
  const pf=state.person;
  const active=RAW.filter(r=>r.source==='linear'&&['In Progress','In Review','Paused','Todo'].includes(r.status)&&(pf==='ALL'||r.tsa===pf));
  /* Done in last 48h — on weekends (Sat/Sun) extend back to Friday */
  const todayDate=new Date(todayStr+'T12:00:00');
  const dow=todayDate.getDay();
  const lookbackDays=dow===1?3:dow===0?2:dow===6?1:2; /* Mon→Fri(3d), Sun→Fri(2d), Sat→Fri(1d), weekday→48h(2d) */
  const cutoffDate=new Date(todayDate);cutoffDate.setDate(cutoffDate.getDate()-lookbackDays);
  const cutoffStr=cutoffDate.toISOString().slice(0,10);
  const doneRecent=RAW.filter(r=>r.source==='linear'&&r.status==='Done'&&r.delivery&&r.delivery.slice(0,10)>=cutoffStr&&(pf==='ALL'||r.tsa===pf));

  const people=[...new Set([...active,...doneRecent].map(r=>r.tsa))].sort();
  const el=document.getElementById('scrumCards');
  if(!el)return;

  const fmtD=d=>{if(!d||d.length<10)return'TBD';const p=d.slice(5,10).split('-');return p[0]+'/'+p[1]};

  function taskSignal(t){
    if(t.perf==='Blocked'||t.status==='B.B.C')return'blocked';
    if(t.perf==='Late')return'atrisk';
    /* If task has an ETA in the past and status is still active (not Done), flag as at risk
       This catches reassigned-in-review tickets where the original delivery was on time
       but the review is still pending past ETA */
    if(t.eta&&t.status!=='Done'){
      try{const eta=new Date(t.eta);if(eta<today)return'atrisk'}catch(e){}
    }
    return'ontrack';
  }
  function slackEmoji(sig){return sig==='blocked'?':red_circle:':sig==='atrisk'?':large_yellow_circle:':':large_green_circle:'}
  function htmlDot(sig){return sig==='blocked'?'🔴':sig==='atrisk'?'🟡':'🟢'}
  function htmlCls(sig){return sig==='blocked'?'sc-r':sig==='atrisk'?'sc-y':'sc-g'}

  function cleanName(focus,cust){
    let s=focus;
    s=s.replace(/^\[.*?\]\s*/,'');
    if(cust&&s.toLowerCase().startsWith(cust.toLowerCase()))s=s.slice(cust.length).replace(/^\s*[-–—:]\s*/,'');
    return s.slice(0,75)||focus.slice(0,75);
  }

  const cards=people.map(person=>{
    const myActive=active.filter(r=>r.tsa===person);
    const myDone=doneRecent.filter(r=>r.tsa===person);

    /* Group active by customer */
    const byCust={};
    myActive.forEach(t=>{
      const c=t.customer||'General';
      if(!byCust[c])byCust[c]=[];
      byCust[c].push(t);
    });
    /* Group done today by customer */
    const doneByCust={};
    myDone.forEach(t=>{
      const c=t.customer||'General';
      if(!doneByCust[c])doneByCust[c]=[];
      doneByCust[c].push(t);
    });

    let green=0,yellow=0,red=0;
    const tbd=myActive.filter(t=>!t.eta).length;
    myActive.forEach(t=>{
      const sig=taskSignal(t);
      if(sig==='ontrack')green++;else if(sig==='atrisk')yellow++;else red++;
    });

    /* Build Slack text */
    let text=`[Daily Agenda – ${todayStr}]\n`;
    /* Sort: TBD (no ETA) first, then by ETA oldest→newest */
    const sortTasks=arr=>arr.sort((a,b)=>{if(!a.eta&&b.eta)return-1;if(a.eta&&!b.eta)return 1;return(a.eta||'').localeCompare(b.eta||'')});
    /* Sort customers by urgency: most at-risk/blocked first, then by task count */
    const custKeys=Object.keys(byCust).sort((a,b)=>{
      const urgA=byCust[a].filter(t=>{const s=taskSignal(t);return s==='atrisk'||s==='blocked'}).length;
      const urgB=byCust[b].filter(t=>{const s=taskSignal(t);return s==='atrisk'||s==='blocked'}).length;
      if(urgB!==urgA)return urgB-urgA;
      return byCust[b].length-byCust[a].length;
    });
    custKeys.forEach(cust=>{
      text+=`\n${cust}\n`;
      sortTasks(byCust[cust]).forEach(t=>{
        const name=cleanName(t.focus,cust);
        text+=`  :black_small_square: [${t.status}] ${name} ETA: ${fmtD(t.eta)} ${slackEmoji(taskSignal(t))}\n`;
      });
    });
    /* Done today section */
    const allDoneCusts=Object.keys(doneByCust).sort();
    if(allDoneCusts.length>0){
      text+=`\n———— Recently Completed ————\n`;
      allDoneCusts.forEach(cust=>{
        doneByCust[cust].forEach(t=>{
          const name=cleanName(t.focus,cust);
          text+=`  :white_check_mark: Done: ${name} (${cust})\n`;
        });
      });
    }

    /* Build HTML preview */
    let html='';
    custKeys.forEach(cust=>{
      html+=`<div class="sc-customer">${esc(cust)}</div>`;
      sortTasks(byCust[cust]).forEach(t=>{
        const sig=taskSignal(t);
        const tid=t.ticketId?`<a href="${esc(t.ticketUrl||'')}" target="_blank" style="color:#818cf8;text-decoration:none;font-size:.85em">${esc(t.ticketId)}</a> `:'';
        const name=cleanName(t.focus,cust);
        const statusColor=t.status==='In Progress'?'#3b82f6':t.status==='In Review'?'#8b5cf6':t.status==='Todo'?'#94a3b8':'#64748b';
        html+=`<div class="sc-task"><span style="color:${statusColor};font-size:.8em;font-weight:600">[${esc(t.status)}]</span> ${tid}${esc(name)} <span style="color:var(--dim)">ETA:${fmtD(t.eta)}</span> <span class="${htmlCls(sig)}">${htmlDot(sig)}</span></div>`;
      });
    });
    /* Done today with strikethrough line */
    if(allDoneCusts.length>0){
      html+=`<div style="border-top:2px dashed var(--green);margin:10px 0 6px;position:relative"><span style="position:absolute;top:-9px;left:12px;background:var(--white);padding:0 8px;font-size:.7em;font-weight:700;color:var(--green);text-transform:uppercase">Recently Completed</span></div>`;
      allDoneCusts.forEach(cust=>{
        doneByCust[cust].forEach(t=>{
          const tid=t.ticketId?`<a href="${esc(t.ticketUrl||'')}" target="_blank" style="color:#818cf8;text-decoration:none;font-size:.85em">${esc(t.ticketId)}</a> `:'';
          const name=cleanName(t.focus,cust);
          html+=`<div class="sc-task" style="text-decoration:line-through;opacity:.6">✅ ${tid}${esc(name)} <span style="color:var(--dim)">(${esc(cust)})</span></div>`;
        });
      });
    }

    return{person,active:myActive.length,done:myDone.length,green,yellow,red,tbd,text,html};
  });

  el.innerHTML=cards.map(c=>`
    <div class="scrum-card" onclick="copyScrumCard(this)" data-scrum="${esc(c.text).replace(/"/g,'&quot;')}">
      <div class="sc-header">
        <span class="sc-name">${c.person}</span>
        <div class="sc-stats">
          <span style="background:#065f46;color:#a7f3d0">${c.green} 🟢</span>
          ${c.yellow?`<span style="background:#92400e;color:#fde68a">${c.yellow} 🟡</span>`:''}
          ${c.red?`<span style="background:#991b1b;color:#fecaca">${c.red} 🔴</span>`:''}
          ${c.done?`<span style="background:#059669;color:#fff">✅ ${c.done}</span>`:''}
          <span style="background:#1e293b;color:#94a3b8">${c.active} active</span>
          ${c.tbd?`<span style="background:#1e3a8a;color:#bfdbfe">${c.tbd} TBD</span>`:''}
        </div>
      </div>
      <div class="sc-body">${c.html}</div>
      <div class="sc-copy-hint">Click to copy Slack-ready text</div>
    </div>
  `).join('');
}

function copyScrumCard(el){
  const text=el.dataset.scrum.replace(/&quot;/g,'"').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#39;/g,"'").replace(/&#96;/g,'`');
  navigator.clipboard.writeText(text).then(()=>{
    el.classList.add('copied');
    const hint=el.querySelector('.sc-copy-hint');
    if(hint)hint.textContent='Copied!';
    setTimeout(()=>{el.classList.remove('copied');if(hint)hint.textContent='Click to copy Slack-ready text'},1500);
  });
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

  /* Populate month filter from available months */
  const fm=document.getElementById('fMonth');
  MONTHS.forEach(mo=>{const o=document.createElement('option');o.value=mo.label;o.textContent=mo.label;fm.appendChild(o)});

  const cki=document.getElementById('clientKpiInfo');
  cki.addEventListener('mouseenter',e=>showTip(e,CLIENT_TIP));
  cki.addEventListener('mouseleave',()=>hideTip());

  document.getElementById('fMonth').addEventListener('change',e=>{state.month=e.target.value;debouncedRender()});
  document.getElementById('fPerson').addEventListener('change',e=>{state.person=e.target.value;debouncedRender()});

  /* M12: Segment bar — default ALL */
  document.querySelectorAll('.segment-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      document.querySelectorAll('.segment-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      state.category=btn.dataset.seg;
      document.getElementById('fCategory').value=btn.dataset.seg;
      debouncedRender();
    });
  });
  document.getElementById('fCategory').addEventListener('change',e=>{
    state.category=e.target.value;
    document.querySelectorAll('.segment-btn').forEach(b=>{
      b.classList.toggle('active',b.dataset.seg===state.category);
    });
    debouncedRender();
  });

  function switchTab(tabName){
    document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.tab===tabName));
    document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
    const panel=document.getElementById('panel-'+tabName);
    panel.classList.add('active');
    document.querySelectorAll('.kpi-cell').forEach(c=>c.classList.toggle('kpi-active',c.dataset.tab===tabName));
    /* Auto-open the collapse inside the active tab */
    const hdr=panel.querySelector('.audit-header');
    const body=panel.querySelector('.audit-body');
    if(hdr&&body&&!body.classList.contains('open')){hdr.classList.add('open');body.classList.add('open')}
    /* Gantt collapse uses display:none (sticky needs no overflow:hidden in ancestors) */
    const gBody=document.getElementById('ganttCollapseBody');
    const gHdr=document.getElementById('ganttCollapseHdr');
    if(tabName==='gantt'&&gBody&&gHdr){gBody.style.display='';gHdr.classList.add('open');renderGantt()}
    /* Hide summary sections on Gantt/Scrum — show only on KPI tabs */
    const isFullscreen=tabName==='gantt'||tabName==='scrum';
    const custSection=document.getElementById('customerKPISection');
    const topStrip=document.getElementById('topStrip');
    const memberCards=document.getElementById('memberCards');
    if(custSection)custSection.style.display=isFullscreen?'none':'';
    if(topStrip)topStrip.style.display=isFullscreen?'none':'';
    if(memberCards)memberCards.style.display=isFullscreen?'none':'';
    /* Render the newly active tab */
    render();
  }

  document.querySelectorAll('.tab').forEach(tab=>{
    tab.addEventListener('click',()=>switchTab(tab.dataset.tab));
  });

  /* KPI cells click → switch tab */
  document.querySelectorAll('.kpi-cell').forEach(cell=>{
    cell.addEventListener('click',()=>switchTab(cell.dataset.tab));
  });

  /* Generic collapse toggle for all audit-header elements */
  document.querySelectorAll('.audit-header').forEach(header=>{
    header.addEventListener('click',()=>{
      header.classList.toggle('open');
      const body=header.nextElementSibling;
      if(body&&body.classList.contains('audit-body'))body.classList.toggle('open');
      /* Gantt uses display:none instead of max-height (sticky needs no overflow:hidden) */
      if(body&&body.id==='ganttCollapseBody'){body.style.display=header.classList.contains('open')?'':'none'}
    });
    header.setAttribute('role','button');
    header.setAttribute('tabindex','0');
    header.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();header.click()}});
  });

  render();
}

init();
</script>
</body>
</html>"""

# Inject data and date
html = HTML.replace('__DATA__', data_json_safe).replace('__DATE__', build_date).replace('__LATEST_DATA__', latest_data_date).replace('${BUILD_DATE}', build_date)

# C3: Atomic write
tmp_path = OUTPUT + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(html)
os.replace(tmp_path, OUTPUT)

print(f'Dashboard saved: {OUTPUT}')
print(f'Size: {len(html)//1024}KB')
print(f'Records: {len(data_raw)} | Core weeks: dynamically computed')
print(f'Build date: {build_date} | Latest data: {latest_data_date}')
