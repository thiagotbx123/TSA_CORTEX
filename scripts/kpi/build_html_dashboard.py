"""Build TSA Waki KPI HTML Dashboard v2 — weekly heatmap grid design."""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os, json

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, '..', '_dashboard_data.json')
OUTPUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'TSA_WAKI_KPI_DASHBOARD.html')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data_json = f.read()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Raccoons KPI Dashboard</title>
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

/* Header */
.header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;background:#1b1b1b;color:#fff;padding:18px 28px;border-radius:10px}
.header h1{font-size:1.4em;font-weight:700;color:#fff}
.header .sub{font-size:.82em;color:#9ca3af}

/* Filters */
.filters{display:flex;gap:8px;align-items:center;margin-bottom:20px;flex-wrap:wrap}
.filters label{font-size:.72em;color:#9ca3af;font-weight:500;text-transform:uppercase;letter-spacing:.5px}
.filters select{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;padding:5px 10px;border-radius:6px;font-size:.82em;cursor:pointer}
.filters select option{background:#1b1b1b;color:#fff}
.filters select:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 2px rgba(37,99,235,.3)}

/* KPI Summary Strip */
.kpi-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px;margin-top:18px}
.kpi-pill{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:10px 14px;display:flex;align-items:center;gap:10px}
.kpi-pill .icon{width:32px;height:32px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1em;flex-shrink:0}
.kpi-pill.k1 .icon{background:var(--blue-bg);color:var(--blue)}
.kpi-pill.k2 .icon{background:var(--yellow-bg);color:var(--yellow)}
.kpi-pill.k3 .icon{background:var(--green-bg);color:var(--green)}
.kpi-pill .info{flex:1}
.kpi-pill .info .name{font-size:.7em;color:var(--dim);text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.kpi-pill .info .val{font-size:1.3em;font-weight:800;line-height:1.2}
.kpi-pill .info .meta{font-size:.68em;color:var(--dim)}
.kpi-pill .badge{font-size:.6em;font-weight:700;padding:2px 7px;border-radius:20px}
.badge-pass{background:var(--green-l);color:var(--green)}
.badge-fail{background:var(--red-l);color:var(--red)}
.badge-warn{background:var(--yellow-l);color:var(--yellow)}

/* Tabs */
.tabs{display:flex;gap:0;margin-bottom:0;border-bottom:2px solid var(--border)}
.tab{padding:12px 24px;font-size:.9em;font-weight:600;color:var(--dim);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;transition:all .15s}
.tab:hover{color:var(--text)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-panel{display:none;padding-top:16px}
.tab-panel.active{display:block}

/* Grid Container */
.grid-section{background:var(--white);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-bottom:16px}
.grid-section .title{padding:14px 20px;font-size:.9em;font-weight:700;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px}
.grid-section .title .dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.grid-section .title .info-btn{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--gray-bg);color:var(--dim);font-size:.7em;font-weight:700;cursor:help;margin-left:4px;border:1px solid var(--border)}

/* Heatmap Grid */
.heatmap{width:100%;border-collapse:collapse;font-size:.88em}
.heatmap th,.heatmap td{padding:9px 12px;text-align:center;white-space:nowrap}
.heatmap thead th{background:var(--gray-bg);font-weight:600;color:var(--dim);font-size:.8em;text-transform:uppercase;letter-spacing:.3px;border-bottom:1px solid var(--border)}
.heatmap .month-header{background:#eef2ff;color:var(--blue);font-weight:700;font-size:.88em;letter-spacing:.5px;border-bottom:2px solid var(--blue-l);padding:10px 8px;border-left:3px solid var(--accent)}
.heatmap .week-header{background:var(--gray-bg);font-size:.78em;color:var(--dim);padding:7px 8px}
.heatmap .month-first{border-left:3px solid var(--accent)!important}
.heatmap .person-label{text-align:left;font-weight:600;padding-left:16px;background:var(--white);border-right:2px solid var(--border);min-width:120px;font-size:.9em;color:var(--text)}
.heatmap .team-row td{font-weight:800;background:var(--gray-bg);border-top:2px solid var(--border);font-size:.92em}
.heatmap .team-row .person-label{background:var(--gray-bg);color:var(--accent);font-size:.82em;text-transform:uppercase;letter-spacing:.3px;font-weight:800;white-space:normal;line-height:1.3}
.heatmap td.cell{min-width:60px;font-weight:600;font-size:.9em;border:1px solid var(--gray-l);cursor:default;position:relative;transition:transform .1s}
.heatmap td.cell:hover{transform:scale(1.05);z-index:1;box-shadow:0 2px 8px rgba(0,0,0,.12)}
.heatmap td.total-col{background:#eef2ff!important;font-weight:800;border-left:3px solid var(--accent);font-size:.92em}

/* Heat colors */
.heat-great{background:#d1fae5;color:#065f46}
.heat-good{background:#ecfdf5;color:#059669}
.heat-ok{background:#fefce8;color:#92400e}
.heat-bad{background:#fef2f2;color:#991b1b}
.heat-terrible{background:#fecaca;color:#7f1d1d}
.heat-na{background:var(--white);color:#d5d8dd;font-weight:300;font-size:.75em}
.heat-zero{background:var(--gray-bg);color:var(--light);font-style:italic}

/* Tooltip */
.tooltip{position:fixed;background:#1e293b;color:#fff;padding:12px 16px;border-radius:8px;font-size:.82em;pointer-events:none;z-index:999;max-width:380px;line-height:1.6;box-shadow:0 4px 16px rgba(0,0,0,.25);display:none}
.tooltip b{color:#93c5fd}
.tooltip .tip-section{margin-top:6px;padding-top:6px;border-top:1px solid rgba(255,255,255,.15)}
.tooltip .tip-task{color:#d1d5db;font-size:.9em;padding-left:8px;text-indent:-8px}
.tooltip .tip-task::before{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;margin-right:4px;vertical-align:middle}
.tooltip .tip-late::before{background:#f87171}
.tooltip .tip-ontime::before{background:#34d399}
.tooltip .tip-overdue::before{background:#fbbf24}
.tooltip .tip-label{color:#9ca3af;font-size:.85em;font-weight:600;text-transform:uppercase;letter-spacing:.5px}

/* Detail panel */
.detail-panel{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:16px;margin-top:16px}
.detail-panel h3{font-size:.85em;font-weight:700;margin-bottom:8px;color:var(--text)}
.detail-table{width:100%;border-collapse:collapse;font-size:.78em}
.detail-table th{background:var(--gray-bg);padding:6px 10px;text-align:left;font-weight:600;color:var(--dim);font-size:.75em;text-transform:uppercase;letter-spacing:.3px}
.detail-table td{padding:5px 10px;border-bottom:1px solid var(--gray-l)}
.detail-table tr:hover td{background:var(--blue-bg)}

/* Trend chart (inside grid-section) */
.trend-row{padding:0}
.trend-wrap{padding:16px 20px;border-bottom:1px solid var(--border)}
.trend-wrap h4{font-size:.78em;color:var(--dim);font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}
.trend-wrap canvas{width:100%!important;height:160px!important}

/* Segment bar */
.segment-bar{display:flex;gap:6px;margin-bottom:14px;background:var(--white);border:1px solid var(--border);border-radius:8px;padding:4px;width:fit-content}
.segment-btn{padding:8px 20px;border-radius:6px;font-size:.82em;font-weight:600;color:var(--dim);cursor:pointer;transition:all .15s;border:none;background:transparent;letter-spacing:.2px}
.segment-btn:hover{color:var(--text);background:var(--gray-bg)}
.segment-btn.active{background:#1b1b1b;color:#fff;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.segment-btn .seg-count{font-size:.78em;font-weight:400;opacity:.7;margin-left:4px}

/* Audit section */
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
.audit-table th{background:#1b1b1b;color:#fff;padding:8px 10px;text-align:left;font-weight:600;font-size:.78em;text-transform:uppercase;letter-spacing:.5px;position:sticky;top:0;cursor:pointer;white-space:nowrap}
.audit-table th:hover{background:#333}
.audit-table th .sort-arrow{margin-left:4px;font-size:.7em;opacity:.5}
.audit-table td{padding:5px 10px;border-bottom:1px solid var(--gray-l);white-space:nowrap}
.audit-table tr:nth-child(even) td{background:#fafbfc}
.audit-table tr:hover td{background:var(--blue-bg)}
.audit-table .perf-on-time{color:var(--green);font-weight:600}
.audit-table .perf-late{color:var(--red);font-weight:600}
.audit-table .perf-overdue{color:var(--yellow);font-weight:600}
.audit-table .perf-na{color:var(--light)}
.audit-stats{padding:10px 20px;font-size:.72em;color:var(--dim);border-top:1px solid var(--gray-l);display:flex;gap:16px;flex-wrap:wrap}

/* Footer */
.footer{text-align:center;margin-top:24px;padding:12px;color:var(--light);font-size:.7em}

@media(max-width:900px){.kpi-strip{grid-template-columns:1fr}.heatmap{font-size:.7em}.segment-bar{flex-wrap:wrap}.audit-table{font-size:.65em}}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>Raccoons KPI Dashboard</h1>
    <div class="sub">Dec 2025 — Mar 2026</div>
  </div>
  <div class="filters">
    <label>Person</label><select id="fPerson"><option value="ALL">All</option></select>
    <label>Category</label><select id="fCategory"><option value="ALL">All</option><option value="Internal">Internal</option><option value="External">External</option></select>
  </div>
</div>

<div class="segment-bar" id="segmentBar">
  <button class="segment-btn active" data-seg="External">Clients &amp; Projects<span class="seg-count" id="segExt"></span></button>
  <button class="segment-btn" data-seg="Internal">Internal<span class="seg-count" id="segInt"></span></button>
</div>

<div class="kpi-strip" id="kpiStrip"></div>

<div class="tabs" id="tabBar">
  <div class="tab active" data-tab="accuracy">ETA Accuracy</div>
  <div class="tab" data-tab="velocity">Faster Implementations</div>
  <div class="tab" data-tab="reliability">Implementation Reliability</div>
</div>

<div class="tab-panel active" id="panel-accuracy">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--blue)"></span>ETA Accuracy<span class="info-btn" onmouseenter="showTip(event,'<b>ETA Accuracy (S9)</b><br><span class=tip-label>Formula</span>: On Time / (On Time + Late)<br><span class=tip-label>Target</span>: &gt;90%<br><span class=tip-label>Tolerance</span>: Delivery within 7 days of ETA = On Time<br><span class=tip-label>Excludes</span>: Tasks with No ETA, No Delivery Date, Canceled, On Track<br><br>Measures whether the committed ETA was met. Higher = more predictable team.')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-accuracy"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-accuracy"></table></div>
  </div>
</div>

<div class="tab-panel" id="panel-velocity">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--yellow)"></span>Faster Implementations<span class="info-btn" onmouseenter="showTip(event,'<b>Avg Execution Time (S8)</b><br><span class=tip-label>Formula</span>: Average(Delivery Date - Date Added)<br><span class=tip-label>Target</span>: &lt;28 days (4-week onboarding)<br><span class=tip-label>Includes</span>: Only Done tasks with both dates, duration &ge;0<br><span class=tip-label>Excludes</span>: Open tasks, tasks without dates, negative durations<br><br>Measures implementation speed. Lower = faster delivery. Hover cells to see slowest tasks.')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-velocity"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-velocity"></table></div>
  </div>
</div>

<div class="tab-panel" id="panel-reliability">
  <div class="grid-section">
    <div class="title"><span class="dot" style="background:var(--green)"></span>Implementation Reliability<span class="info-btn" onmouseenter="showTip(event,'<b>Effective Delivery Rate (S10)</b><br><span class=tip-label>Formula</span>: On Time / (On Time + Late + Overdue)<br><span class=tip-label>Target</span>: &gt;85%<br><span class=tip-label>Key Difference</span>: Unlike KPI1, this also penalizes open overdue tasks<br><span class=tip-label>Excludes</span>: Tasks with No ETA, No Delivery, Canceled<br><br>Strictest reliability metric. Counts both past failures (Late) and current risks (Overdue). Hover cells to see problematic tasks.')" onmouseleave="hideTip()">?</span></div>
    <div class="trend-wrap" id="trend-reliability"></div>
    <div style="overflow-x:auto"><table class="heatmap" id="grid-reliability"></table></div>
  </div>
</div>

<div class="tooltip" id="tooltip"></div>

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
  Raccoons KPI Dashboard &nbsp;&middot;&nbsp; Source: KPI_Team_Raccoons &nbsp;&middot;&nbsp; Generated __DATE__
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>
<script>
const RAW = __DATA__;

/* ── Helpers ─────────────────────────────────────────── */
function parseWeek(w){const m=w.match(/(\d{2})-(\d{2})\s+W\.(\d+)/);return m?[+m[1],+m[2],+m[3]]:[99,99,99]}
function weekSort(a,b){const[y1,m1,w1]=parseWeek(a),[y2,m2,w2]=parseWeek(b);return y1-y2||m1-m2||w1-w2}
function daysBetween(a,b){if(!a||!b)return null;const d1=new Date(a),d2=new Date(b);if(isNaN(d1)||isNaN(d2))return null;return Math.round((d2-d1)/864e5)}
function monthLabel(y,m){const names=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];return(names[m]||'?')+' '+(y<50?'20'+y:'19'+y)}

/* ── Core period: Dec 25 → Mar 26 ─────────────────── */
function isCoreWeek(w){const[y,m]=parseWeek(w);return(y===25&&m>=12)||(y===26&&m<=3)}
const CORE_WEEKS=[...new Set(RAW.map(r=>r.week).filter(w=>w&&isCoreWeek(w)))].sort(weekSort);
const PEOPLE_ALL=[...new Set(RAW.map(r=>r.tsa))].sort();

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

/* ── State ──────────────────────────────────────────── */
let state={person:'ALL',category:'External'};
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
  tip.style.left=x+'px';
  tip.style.top=Math.max(10,y)+'px';
}
function hideTip(){tip.style.display='none'}

/* ── Escape HTML for tooltip ───────────────────────── */
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/'/g,'&#39;').replace(/"/g,'&quot;')}

/* ── KPI Calculations per cell ──────────────────────── */
function calcAccuracy(rows){
  const ot=rows.filter(r=>r.perf==='On Time').length;
  const lt=rows.filter(r=>r.perf==='Late').length;
  const d=ot+lt;
  return{val:d>0?ot/d:null,num:ot,den:d,n:rows.length};
}
function calcVelocity(rows){
  const durs=rows.filter(r=>r.delivery&&r.dateAdd&&r.status==='Done').map(r=>daysBetween(r.dateAdd,r.delivery)).filter(d=>d!==null&&d>=0);
  const avg=durs.length>0?durs.reduce((a,b)=>a+b,0)/durs.length:null;
  return{val:avg,n:durs.length,durs};
}
function calcReliability(rows){
  const ot=rows.filter(r=>r.perf==='On Time').length;
  const lt=rows.filter(r=>r.perf==='Late').length;
  const ov=rows.filter(r=>r.perf==='Overdue').length;
  const d=ot+lt+ov;
  return{val:d>0?ot/d:null,num:ot,den:d,n:rows.length,late:lt,overdue:ov};
}

/* ── Heat class ─────────────────────────────────────── */
function heatPct(val){
  if(val===null||val===undefined||isNaN(val))return'heat-na';
  if(val>=.9)return'heat-great';
  if(val>=.75)return'heat-good';
  if(val>=.6)return'heat-ok';
  if(val>=.4)return'heat-bad';
  return'heat-terrible';
}
function heatDays(val){
  if(val===null||val===undefined||isNaN(val))return'heat-na';
  if(val<=14)return'heat-great';
  if(val<=28)return'heat-good';
  if(val<=42)return'heat-ok';
  if(val<=60)return'heat-bad';
  return'heat-terrible';
}

/* ── Tooltip cache for cells ────────────────────────── */
const tipCache={};
let tipCounter=0;

/* ── Build heatmap grid ─────────────────────────────── */
function buildGrid(tableId, calcFn, fmtFn, heatFn, tipFn){
  const table=document.getElementById(tableId);
  const data=getFiltered();
  const people=getPeople();
  const months=MONTHS;

  // Header row 1: Month spans (no AVG columns)
  let h1='<tr><th rowspan="2" style="text-align:left;min-width:120px;border-right:2px solid var(--border);background:var(--white);font-size:.72em;color:var(--light);font-weight:500;letter-spacing:.5px;padding-left:16px">TEAM</th>';
  months.forEach(mo=>{
    h1+=`<th class="month-header" colspan="${mo.weeks.length}">${mo.label}</th>`;
  });
  h1+='<th class="month-header" rowspan="2" style="border-left:3px solid var(--accent);font-size:.78em;line-height:1.2">OVERALL<br><span style="font-weight:400;font-size:.8em;color:var(--dim)">all weeks</span></th></tr>';

  // Header row 2: Week labels with month-first border
  let h2='<tr>';
  months.forEach(mo=>{
    mo.weeks.forEach((w,i)=>{
      const[,,wn]=parseWeek(w);
      const first=i===0?'border-left:3px solid var(--accent);':'';
      h2+=`<th class="week-header" style="${first}">W${wn}</th>`;
    });
  });
  h2+='</tr>';

  // Helper to build a cell with cached tooltip
  function cell(cls,txt,tipHtml,isFirstOfMonth){
    const id='t'+(tipCounter++);
    tipCache[id]=tipHtml;
    const mf=isFirstOfMonth?' month-first':'';
    return`<td class="cell ${cls}${mf}" data-tip="${id}">${txt}</td>`;
  }

  // Data rows
  let bodyRows='';
  people.forEach(person=>{
    let row=`<tr><td class="person-label">${person}</td>`;

    months.forEach(mo=>{
      mo.weeks.forEach((w,i)=>{
        const rows=data.filter(r=>r.tsa===person&&r.week===w);
        const calc=calcFn(rows);
        const v=calc.val;
        const cls=rows.length===0?'heat-na':heatFn(v);
        const txt=rows.length===0?'—':fmtFn(v);
        row+=cell(cls,txt,tipFn(person,w,calc,rows),i===0);
      });
    });

    // Total column
    const totalRows=data.filter(r=>r.tsa===person);
    const totalCalc=calcFn(totalRows);
    const totalCls=totalRows.length===0?'heat-na':heatFn(totalCalc.val);
    row+=`<td class="cell total-col ${totalCls}">${totalRows.length===0?'—':fmtFn(totalCalc.val)}</td>`;
    row+='</tr>';
    bodyRows+=row;
  });

  // Team average row
  let teamRow='<tr class="team-row"><td class="person-label">OVERALL<br><span style="font-weight:400;font-size:.75em;color:var(--dim)">all members</span></td>';
  months.forEach(mo=>{
    mo.weeks.forEach((w,i)=>{
      const rows=data.filter(r=>r.week===w);
      const calc=calcFn(rows);
      const cls=rows.length===0?'heat-na':heatFn(calc.val);
      teamRow+=cell(cls,rows.length===0?'—':fmtFn(calc.val),tipFn('TEAM',w,calc,rows),i===0);
    });
  });
  const allRows=data;
  const allCalc=calcFn(allRows);
  const allCls=allRows.length===0?'heat-na':heatFn(allCalc.val);
  teamRow+=`<td class="cell total-col ${allCls}">${allRows.length===0?'—':fmtFn(allCalc.val)}</td></tr>`;

  table.innerHTML=`<thead>${h1}${h2}</thead><tbody>${bodyRows}${teamRow}</tbody>`;

  // Attach tooltip events via delegation
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

/* ── Format & Tip helpers ───────────────────────────── */
function fmtPct(v){return(v===null||v===undefined||isNaN(v))?'—':(v*100).toFixed(0)+'%'}
function fmtDays(v){return(v===null||v===undefined||isNaN(v))?'—':v.toFixed(0)+'d'}

function tipAccuracy(person,week,calc,rows){
  if(rows.length===0)return`<b>${person}</b> &middot; ${week}<br><span class="tip-label">No tasks this week</span>`;
  let html=`<b>${person}</b> &middot; ${week}`;
  html+=`<br><span class="tip-label">ETA Accuracy</span>: <b>${fmtPct(calc.val)}</b>`;
  html+=`<br>${calc.num} on time + ${calc.den-calc.num} late = ${calc.den} measured`;
  // Excluded
  const excluded=rows.filter(r=>r.perf!=='On Time'&&r.perf!=='Late');
  if(excluded.length>0)html+=`<br>${excluded.length} excluded (${[...new Set(excluded.map(r=>r.perf))].join(', ')})`;
  // Show late tasks by name
  const lateOnes=rows.filter(r=>r.perf==='Late');
  if(lateOnes.length>0){
    html+=`<div class="tip-section"><span class="tip-label">Late tasks:</span>`;
    lateOnes.slice(0,5).forEach(r=>{html+=`<div class="tip-task tip-late">${esc(r.focus.slice(0,50))}</div>`});
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
  html+=`<br><span class="tip-label">Execution Time</span>: <b>${fmtDays(calc.val)}</b> avg`;
  html+=`<br>Median: ${med}d &middot; Min: ${min}d &middot; Max: ${max}d`;
  html+=`<br>${calc.n} completed tasks measured`;
  // Show slowest tasks
  const slow=rows.filter(r=>r.delivery&&r.dateAdd&&r.status==='Done').map(r=>({f:r.focus,d:daysBetween(r.dateAdd,r.delivery)})).filter(x=>x.d!==null&&x.d>=0).sort((a,b)=>b.d-a.d);
  if(slow.length>0&&slow[0].d>14){
    html+=`<div class="tip-section"><span class="tip-label">Slowest:</span>`;
    slow.slice(0,3).forEach(x=>{html+=`<div class="tip-task tip-late">${x.d}d &mdash; ${esc(x.f.slice(0,45))}</div>`});
    html+=`</div>`;
  }
  return html;
}
function tipReliability(person,week,calc,rows){
  if(rows.length===0)return`<b>${person}</b> &middot; ${week}<br><span class="tip-label">No tasks this week</span>`;
  let html=`<b>${person}</b> &middot; ${week}`;
  html+=`<br><span class="tip-label">Delivery Rate</span>: <b>${fmtPct(calc.val)}</b>`;
  html+=`<br>${calc.num} on time + ${calc.late} late + ${calc.overdue} overdue = ${calc.den}`;
  const excluded=rows.filter(r=>r.perf!=='On Time'&&r.perf!=='Late'&&r.perf!=='Overdue');
  if(excluded.length>0)html+=`<br>${excluded.length} excluded (${[...new Set(excluded.map(r=>r.perf))].join(', ')})`;
  // Show problematic tasks
  const problems=rows.filter(r=>r.perf==='Late'||r.perf==='Overdue');
  if(problems.length>0){
    html+=`<div class="tip-section"><span class="tip-label">Issues:</span>`;
    problems.slice(0,5).forEach(r=>{
      const cls=r.perf==='Late'?'tip-late':'tip-overdue';
      html+=`<div class="tip-task ${cls}">[${r.perf}] ${esc(r.focus.slice(0,42))}</div>`;
    });
    if(problems.length>5)html+=`<div class="tip-task">... +${problems.length-5} more</div>`;
    html+=`</div>`;
  }
  return html;
}

/* ── KPI Summary Cards ──────────────────────────────── */
function renderKPIStrip(){
  const data=getFiltered();
  const a=calcAccuracy(data);
  const v=calcVelocity(data);
  const r=calcReliability(data);

  const strip=document.getElementById('kpiStrip');
  const items=[
    {cls:'k1',icon:'&#9201;',name:'ETA Accuracy',val:a.val,fmt:fmtPct,target:'>90%',pass:a.val!==null&&a.val>=.9,meta:`${a.num}/${a.den} on time`},
    {cls:'k2',icon:'&#9889;',name:'Avg Execution Time',val:v.val,fmt:fmtDays,target:'<28 days',pass:v.val!==null&&v.val<=28,meta:`${v.n} tasks measured`},
    {cls:'k3',icon:'&#10003;',name:'Effective Delivery Rate',val:r.val,fmt:fmtPct,target:'>85%',pass:r.val!==null&&r.val>=.85,meta:`${r.num}/${r.den} (incl ${r.overdue} overdue)`},
  ];
  strip.innerHTML=items.map(i=>{
    const badge=i.val===null?'badge-warn':(i.pass?'badge-pass':'badge-fail');
    const badgeTxt=i.val===null?'—':(i.pass?'ON TARGET':'BELOW');
    return`<div class="kpi-pill ${i.cls}">
      <div class="icon">${i.icon}</div>
      <div class="info">
        <div class="name">${i.name}</div>
        <div class="val">${i.val!==null?i.fmt(i.val):'—'}</div>
        <div class="meta">${i.meta} · Target: ${i.target}</div>
      </div>
      <div class="badge ${badge}">${badgeTxt}</div>
    </div>`;
  }).join('');
}

/* ── Mini trend charts ──────────────────────────────── */
function destroyChart(id){if(charts[id]){charts[id].destroy();delete charts[id]}}

function renderTrend(containerId, calcFn, fmtLabel, color, targetVal, targetLabel, isInverse){
  const el=document.getElementById(containerId);
  const data=getFiltered();
  const people=getPeople();

  // Compute team overall + per-person min/max band
  const teamVals=[], minVals=[], maxVals=[];
  CORE_WEEKS.forEach(w=>{
    const rows=data.filter(r=>r.week===w);
    const teamCalc=calcFn(rows);
    teamVals.push(teamCalc.val!==null?(typeof teamCalc.val==='number'?+teamCalc.val.toFixed(2):teamCalc.val):null);

    // Per-person values for this week (for range band)
    const personVals=people.map(p=>{
      const pr=data.filter(r=>r.tsa===p&&r.week===w);
      const c=calcFn(pr);return c.val;
    }).filter(v=>v!==null);
    minVals.push(personVals.length>0?Math.min(...personVals):null);
    maxVals.push(personVals.length>0?Math.max(...personVals):null);
  });

  const datasets=[];

  // Range band (max line — filled down to min)
  datasets.push({label:'Range (min-max)',data:maxVals,borderColor:'transparent',backgroundColor:color+'18',borderWidth:0,fill:'+1',tension:.3,pointRadius:0,pointHoverRadius:0});
  datasets.push({label:'_min',data:minVals,borderColor:'transparent',backgroundColor:'transparent',borderWidth:0,fill:false,tension:.3,pointRadius:0,pointHoverRadius:0});

  // Team overall
  datasets.push({label:'Team',data:teamVals,borderColor:color,backgroundColor:color+'22',borderWidth:2.5,fill:false,tension:.3,pointRadius:4,pointHoverRadius:7,pointBackgroundColor:color});

  // Target line
  datasets.push({label:targetLabel,data:CORE_WEEKS.map(()=>targetVal),borderColor:'#ef4444aa',borderDash:[6,4],borderWidth:1.5,pointRadius:0,pointHoverRadius:0,fill:false});

  // Week labels matching table (W1, W2, etc — grouped by month)
  const weekLabels=CORE_WEEKS.map(w=>{const[,,wn]=parseWeek(w);return'W'+wn});

  const canvasId=containerId+'-canvas';
  el.innerHTML=`<h4>Weekly Trend</h4><canvas id="${canvasId}"></canvas>`;

  destroyChart(canvasId);
  charts[canvasId]=new Chart(document.getElementById(canvasId),{
    type:'line',
    data:{labels:weekLabels,datasets},
    options:{
      responsive:true,maintainAspectRatio:false,
      interaction:{mode:'index',intersect:false},
      plugins:{
        legend:{display:true,position:'bottom',labels:{
          color:'#374151',font:{size:11,weight:'500'},boxWidth:10,padding:10,usePointStyle:true,pointStyle:'circle',
          filter:function(item){return item.text!=='_min'}
        }},
        tooltip:{
          enabled:true,backgroundColor:'#1e293bee',titleColor:'#93c5fd',titleFont:{size:12,weight:'700'},
          bodyColor:'#e2e8f0',bodyFont:{size:11},padding:12,cornerRadius:8,boxPadding:4,
          filter:function(item){return item.dataset.label!=='_min'&&item.dataset.label!=='Range (min-max)'},
          callbacks:{
            title:function(items){if(!items[0])return'';const idx=items[0].dataIndex;return CORE_WEEKS[idx]||'';},
            label:function(ctx){
              if(ctx.raw===null||ctx.raw===undefined)return null;
              const name=ctx.dataset.label;
              if(name===targetLabel||name==='_min'||name==='Range (min-max)')return null;
              const val=ctx.raw;
              const fmtVal=isInverse?val.toFixed(0)+'d':(val*100).toFixed(0)+'%';
              const diff=isInverse?(val-targetVal):(val-targetVal)*100;
              const diffStr=isInverse?(diff>0?'+'+diff.toFixed(0)+'d':diff.toFixed(0)+'d'):(diff>0?'+'+diff.toFixed(0)+'pp':diff.toFixed(0)+'pp');
              const icon=isInverse?(val<=targetVal?'ON TARGET':'BELOW'):(val>=targetVal?'ON TARGET':'BELOW');
              return ` Team: ${fmtVal}  (${diffStr} vs target) — ${icon}`;
            },
            afterBody:function(items){
              const idx=items[0]?items[0].dataIndex:-1;
              if(idx<0)return'';
              const mn=minVals[idx],mx=maxVals[idx];
              if(mn===null)return'';
              const fmn=isInverse?mn.toFixed(0)+'d':(mn*100).toFixed(0)+'%';
              const fmx=isInverse?mx.toFixed(0)+'d':(mx*100).toFixed(0)+'%';
              return '  Range: '+fmn+' — '+fmx;
            }
          }
        }
      },
      scales:{
        y:{ticks:{color:'#6b7280',font:{size:10},callback:function(v){return isInverse?v+'d':(v*100).toFixed(0)+'%'}},grid:{color:'#e5e7eb88'},beginAtZero:!isInverse},
        x:{ticks:{color:'#6b7280',font:{size:10}},grid:{color:'#f3f4f622'}}
      }
    }
  });
}

/* ── Segment counts ────────────────────────────────── */
function updateSegmentCounts(){
  const base=RAW.filter(r=>r.week&&isCoreWeek(r.week)&&(state.person==='ALL'||r.tsa===state.person));
  document.getElementById('segExt').textContent=' ('+base.filter(r=>r.category==='External').length+')';
  document.getElementById('segInt').textContent=' ('+base.filter(r=>r.category==='Internal').length+')';
}

/* ── Audit table ──────────────────────────────────── */
let auditSortCol=0, auditSortAsc=true;

function getAuditRows(){
  return getFiltered().map((r,i)=>{
    const dur=(r.delivery&&r.dateAdd)?daysBetween(r.dateAdd,r.delivery):null;
    return [i+1, r.tsa||'—', r.week||'—', r.ticketId||'—', r.focus||'—', r.status||'—', r.category||'—', r.demandType||'—', r.customer||'—', r.dateAdd||'—', r.eta||'—', r.delivery||'—', r.perf||'—', dur!==null&&dur>=0?dur+'d':'—', r.source||'—', r.ticketUrl||''];
  });
}

const AUDIT_COLS=['#','Person','Week','Ticket','Focus/Task','Status','Category','Demand Type','Customer','Date Added','ETA','Delivery','Performance','Duration','Source','Ticket URL'];

function perfClass(v){
  if(v==='On Time')return'perf-on-time';
  if(v==='Late')return'perf-late';
  if(v==='Overdue')return'perf-overdue';
  return'perf-na';
}

function renderAuditTable(){
  const rows=getAuditRows();
  // Re-number after filter
  rows.forEach((r,i)=>r[0]=i+1);
  // Sort
  rows.sort((a,b)=>{
    let va=a[auditSortCol],vb=b[auditSortCol];
    if(typeof va==='string'&&typeof vb==='string'){va=va.toLowerCase();vb=vb.toLowerCase()}
    if(va<vb)return auditSortAsc?-1:1;
    if(va>vb)return auditSortAsc?1:-1;
    return 0;
  });

  const table=document.getElementById('auditTable');
  let thead='<thead><tr>';
  AUDIT_COLS.forEach((c,i)=>{
    if(i===15)return; /* hide raw URL column in HTML */
    const arrow=i===auditSortCol?(auditSortAsc?'&#9650;':'&#9660;'):'';
    thead+=`<th data-col="${i}">${c}<span class="sort-arrow">${arrow}</span></th>`;
  });
  thead+='</tr></thead>';

  let tbody='<tbody>';
  rows.forEach(r=>{
    tbody+='<tr>';
    r.forEach((v,i)=>{
      if(i===15)return; /* hide raw URL column in HTML */
      const cls=i===12?' class="'+perfClass(v)+'"':'';
      /* Ticket col: link if URL exists */
      if(i===3&&r[15]){
        tbody+=`<td><a href="${r[15]}" target="_blank" style="color:var(--accent);text-decoration:none;font-weight:600">${v}</a></td>`;
      }else{
        tbody+=`<td${cls}>${v}</td>`;
      }
    });
    tbody+='</tr>';
  });
  tbody+='</tbody>';

  table.innerHTML=thead+tbody;

  // Sort click
  table.querySelectorAll('th').forEach(th=>{
    th.addEventListener('click',()=>{
      const col=+th.dataset.col;
      if(col===auditSortCol)auditSortAsc=!auditSortAsc;
      else{auditSortCol=col;auditSortAsc=true}
      renderAuditTable();
    });
  });

  // Stats
  const stats=document.getElementById('auditStats');
  const data=getFiltered();
  const onTime=data.filter(r=>r.perf==='On Time').length;
  const late=data.filter(r=>r.perf==='Late').length;
  const overdue=data.filter(r=>r.perf==='Overdue').length;
  const done=data.filter(r=>r.status==='Done').length;
  const open=data.filter(r=>r.status!=='Done'&&r.status!=='Canceled').length;
  stats.innerHTML=`<span><b>${rows.length}</b> records</span><span>Done: <b>${done}</b></span><span>Open: <b>${open}</b></span><span style="color:var(--green)">On Time: <b>${onTime}</b></span><span style="color:var(--red)">Late: <b>${late}</b></span><span style="color:var(--yellow)">Overdue: <b>${overdue}</b></span>`;
}

/* ── Export functions ──────────────────────────────── */
function downloadXLSX(){
  const rows=getAuditRows();
  rows.forEach((r,i)=>r[0]=i+1);
  const aoa=[AUDIT_COLS,...rows];
  const ws=XLSX.utils.aoa_to_sheet(aoa);
  /* column widths: #,Person,Week,Ticket,Focus,Status,Category,DemandType,Customer,DateAdd,ETA,Delivery,Perf,Duration,Source,TicketURL */
  ws['!cols']=[{wch:5},{wch:14},{wch:12},{wch:12},{wch:45},{wch:12},{wch:11},{wch:18},{wch:25},{wch:12},{wch:12},{wch:12},{wch:13},{wch:10},{wch:12},{wch:55}];
  /* Make Ticket URL column actual hyperlinks */
  for(let r=1;r<=rows.length;r++){
    const urlCol=15; /* column P (0-indexed=15) = Ticket URL */
    const urlCell=XLSX.utils.encode_cell({r:r,c:urlCol});
    const ticketCell=XLSX.utils.encode_cell({r:r,c:3}); /* column D = Ticket ID */
    if(ws[urlCell]&&ws[urlCell].v&&ws[urlCell].v.startsWith('http')){
      ws[urlCell].l={Target:ws[urlCell].v,Tooltip:'Open in Linear'};
      /* Also make Ticket ID column a hyperlink */
      if(ws[ticketCell]&&ws[ticketCell].v&&ws[ticketCell].v!=='—'){
        ws[ticketCell].l={Target:ws[urlCell].v,Tooltip:'Open in Linear'};
      }
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
  renderKPIStrip();
  buildGrid('grid-accuracy',calcAccuracy,fmtPct,heatPct,tipAccuracy);
  buildGrid('grid-velocity',calcVelocity,fmtDays,heatDays,tipVelocity);
  buildGrid('grid-reliability',calcReliability,fmtPct,heatPct,tipReliability);
  renderTrend('trend-accuracy',calcAccuracy,'ETA Accuracy','#3b82f6',.9,'Target 90%',false);
  renderTrend('trend-velocity',calcVelocity,'Faster Implementations','#d97706',28,'Target 28d',true);
  renderTrend('trend-reliability',calcReliability,'Implementation Reliability','#059669',.85,'Target 85%',false);
  renderAuditTable();
}

/* ── Init ───────────────────────────────────────────── */
function init(){
  // Populate person filter
  const fp=document.getElementById('fPerson');
  PEOPLE_ALL.forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;fp.appendChild(o)});

  // Filter events
  document.getElementById('fPerson').addEventListener('change',e=>{state.person=e.target.value;render()});

  // Segment bar events
  document.querySelectorAll('.segment-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      document.querySelectorAll('.segment-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      state.category=btn.dataset.seg;
      // Sync dropdown
      document.getElementById('fCategory').value=btn.dataset.seg;
      render();
    });
  });
  // Sync dropdown → segment bar
  document.getElementById('fCategory').addEventListener('change',e=>{
    state.category=e.target.value;
    document.querySelectorAll('.segment-btn').forEach(b=>{
      b.classList.toggle('active',b.dataset.seg===state.category);
    });
    render();
  });

  // Tab events
  document.querySelectorAll('.tab').forEach(tab=>{
    tab.addEventListener('click',()=>{
      document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById('panel-'+tab.dataset.tab).classList.add('active');
    });
  });

  // Audit toggle
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
import datetime
html = HTML.replace('__DATA__', data_json).replace('__DATE__', datetime.date.today().strftime('%Y-%m-%d'))

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Dashboard saved: {OUTPUT}')
print(f'Size: {len(html)//1024}KB')
