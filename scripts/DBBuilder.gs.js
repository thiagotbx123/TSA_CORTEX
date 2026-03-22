
/**
 * TSA DB Builder + KPI Dashboard V2
 * Triggers: onEdit (DB only, fast) + hourly (DB + KPI) + manual menu.
 *
 * "Rebuild All" = DB tab + sync DB_Data to KPI sheet + DASHBOARD.
 * "Rebuild DB Only" = just DB tab (fast).
 */

var COLUMN_MAP = {
  'DIEGO':     { status: 1, demandType: 2, customer: 3, currentFocus: 4, dateAdd: 5, eta: 6, deliveryDate: 10 },
  'GABI':      { status: 1, demandType: 2, customer: 3, currentFocus: 5, dateAdd: 6, eta: 7, deliveryDate: 11 },
  'CARLOS':    { status: 2, demandType: 5, customer: 6, currentFocus: 7, dateAdd: 8, eta: 9, deliveryDate: 14 },
  'ALEXANDRA': { status: 1, demandType: 2, customer: 3, currentFocus: 4, dateAdd: 5, eta: 6, deliveryDate: 10 },
  'THIAGO':    { status: 1, demandType: 2, customer: 3, currentFocus: 4, dateAdd: 5, eta: 6, deliveryDate: 10 }
};

var TSA_TABS = ['DIEGO', 'GABI', 'CARLOS', 'ALEXANDRA', 'THIAGO'];
var DE_TABS = ['THAIS_YASMIN'];
var EXTERNAL_TYPES = ['external(customer)', 'external (customer)', 'incident'];
var DB_HEADERS = ['TSA', 'Week Range', 'Current Focus', 'Status', 'Demand Type',
                  'Demand Category', 'Customer', 'Date Add', 'ETA', 'Delivery Date',
                  'Delivery Performance', 'Week Ref'];
var MONTH_ABBR_ = ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                   'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

// KPI Dashboard config
var KPI_ID = '1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w';
var DASH_TAB = 'DASHBOARD';
var ALL_M = ['ALEXANDRA', 'CARLOS', 'DIEGO', 'GABI', 'THIAGO', 'THAIS', 'YASMIM'];
var DISP = {ALEXANDRA:'Alexandra',CARLOS:'Carlos',DIEGO:'Diego',
            GABI:'Gabrielle',THIAGO:'Thiago',THAIS:'Thais',YASMIM:'Yasmim'};
var MO_FULL = {1:'JANUARY',2:'FEBRUARY',3:'MARCH',4:'APRIL',5:'MAY',6:'JUNE',
               7:'JULY',8:'AUGUST',9:'SEPTEMBER',10:'OCTOBER',11:'NOVEMBER',12:'DECEMBER'};
var IND_DEFS = [
  {k:'S1', n:'S1 Internal Accuracy',t:'>90%',tv:0.90,f:'pct',m:'ph'},
  {k:'S2', n:'S2 External Accuracy',t:'>90%',tv:0.90,f:'pct',m:'ph'},
  {k:'S3', n:'S3 Throughput',t:'>=5/wk',tv:5,f:'n1',m:'ch'},
  {k:'S4', n:'S4 Overdue',t:'0',tv:0,f:'int',m:'zb'},
  {k:'S5', n:'S5 WIP',t:'<=3',tv:3,f:'int',m:'cl'},
  {k:'S6', n:'S6 Internal Count',t:'Monitor',tv:null,f:'int',m:'mo'},
  {k:'S7', n:'S7 External Count',t:'Monitor',tv:null,f:'int',m:'mo'},
  {k:'S8', n:'S8 Avg Exec Time',t:'<7d',tv:7,f:'n1',m:'cl'},
  {k:'S9', n:'S9 Timeline Accuracy',t:'>90%',tv:0.90,f:'pct',m:'ph'},
  {k:'S10',n:'S10 Effective Rate',t:'>85%',tv:0.85,f:'pct',m:'ph'},
  {k:'S11',n:'S11 Delay Severity',t:'<2d',tv:2,f:'n1',m:'cl'}
];
var IND_CLR = {
  S1:['#2980B9','#D6EAF8'],S2:['#16A085','#D1F2EB'],S3:['#27AE60','#D5F5E3'],
  S4:['#C0392B','#FADBD8'],S5:['#D4AC0D','#FEF9E7'],S6:['#8E44AD','#E8DAEF'],
  S7:['#D35400','#FAE5D3'],S8:['#2C3E50','#D5D8DC'],S9:['#1ABC9C','#D1F2EB'],
  S10:['#E74C3C','#FDEDEC'],S11:['#795548','#EFEBE9']
};
var IND_NOTES = {
  S1:'S1 — INTERNAL ACCURACY\n\nWHAT: Of all internal tasks that finished, how many were on time?\nWHY: Shows if the team meets its own deadlines (not customer work).\nHOW: Only looks at tasks marked "Internal". Ignores tasks still open.\n\nFORMULA: On Time / (On Time + Late)\nOnly counts tasks with Demand Category = "Internal" and Status = "Done".\n\nTARGET: > 90%\nGREEN = 90%+  |  YELLOW = 68-89%  |  RED = below 68%',
  S2:'S2 — EXTERNAL ACCURACY\n\nWHAT: Of all customer-facing tasks that finished, how many were on time?\nWHY: Late external work = unhappy customers. This is the one that hurts.\nHOW: Same logic as S1, but only looks at "External" or "Incident" tasks.\n\nFORMULA: On Time / (On Time + Late)\nOnly counts tasks with Demand Category = "External" and Status = "Done".\n\nTARGET: > 90%\nGREEN = 90%+  |  YELLOW = 68-89%  |  RED = below 68%',
  S3:'S3 — THROUGHPUT\n\nWHAT: How many tasks did this person finish this week?\nWHY: Measures raw output. Are we delivering enough work?\nHOW: Counts every task with Status = "Done" in that week.\nMonthly/Overall = average per week (not total).\n\nFORMULA: COUNT(Status = "Done")\nMonthly: total done / number of active weeks.\n\nTARGET: >= 5 per week\nGREEN = 5+  |  YELLOW = 3-4  |  RED = below 3',
  S4:'S4 — OVERDUE\n\nWHAT: How many tasks are past their deadline and still not done?\nWHY: Overdue = broken promise. Zero is the goal, always.\nHOW: Counts tasks where ETA already passed but Status is NOT "Done".\n\nFORMULA: COUNT(Performance = "Overdue")\nA task is "Overdue" when ETA < today AND status != Done.\n\nTARGET: 0\nGREEN = 0  |  YELLOW = 1-2  |  RED = 3+',
  S5:'S5 — WIP (Work In Progress)\n\nWHAT: How many tasks is this person juggling right now?\nWHY: Too many open tasks = context switching = slower delivery.\nHOW: Counts tasks with Status = "In Progress" in that week.\n\nFORMULA: COUNT(Status = "In Progress")\n\nTARGET: <= 3\nGREEN = 0-3  |  YELLOW = 4-6  |  RED = 7+',
  S6:'S6 — INTERNAL COUNT\n\nWHAT: How many internal tasks exist this week?\nWHY: Context only. Shows the volume of internal work.\nHOW: Counts all tasks where Demand Category = "Internal".\n\nFORMULA: COUNT(Category = "Internal")\n\nTARGET: Monitor only (no color coding)',
  S7:'S7 — EXTERNAL COUNT\n\nWHAT: How many customer-facing tasks exist this week?\nWHY: Context only. Shows the volume of external/customer work.\nHOW: Counts all tasks where Demand Category = "External".\n\nFORMULA: COUNT(Category = "External")\n\nTARGET: Monitor only (no color coding)',
  S8:'S8 — AVG EXECUTION TIME\n\nWHAT: On average, how many days from task creation to delivery?\nWHY: Are we fast or slow? Lower = better.\nHOW: For each finished task, calculates (Delivery Date - Date Added).\nThen averages all of them. Ignores tasks taking > 60 days (outliers).\n\nFORMULA: AVG(Delivery Date - Date Added)\nOnly tasks with Status = "Done" and result between 0-60 days.\n\nTARGET: < 7 days\nGREEN = 0-7d  |  YELLOW = 8-14d  |  RED = 15d+',
  S9:'S9 — TIMELINE ACCURACY\n\nWHAT: Of ALL finished tasks (internal + external), how many were on time?\nWHY: The big picture. S1 and S2 split by type; S9 combines everything.\nHOW: Same as S1/S2 but ignores the Internal/External filter.\n\nFORMULA: On Time / (On Time + Late)\nAll tasks with Status = "Done", regardless of category.\n\nTARGET: > 90%\nGREEN = 90%+  |  YELLOW = 68-89%  |  RED = below 68%',
  S10:'S10 — EFFECTIVE DELIVERY RATE\n\nWHAT: Of all tasks that have a result (done + overdue), how many were on time?\nWHY: Stricter than S9 — also penalizes overdue tasks, not just late ones.\nHOW: Denominator includes Overdue tasks (open + past ETA).\nA person with many overdue tasks gets a lower score even if done tasks were on time.\n\nFORMULA: On Time / (On Time + Late + Overdue)\n\nTARGET: > 85%\nGREEN = 85%+  |  YELLOW = 64-84%  |  RED = below 64%',
  S11:'S11 — DELAY SEVERITY\n\nWHAT: When tasks ARE late, how late are they on average?\nWHY: Being 1 day late is very different from being 10 days late.\nHOW: For each Late task, calculates (Delivery Date - ETA).\nThen averages. Only looks at tasks that were actually delivered late.\n\nFORMULA: AVG(Delivery Date - ETA) for Late tasks only\n\nTARGET: < 2 days\nGREEN = 0-2d  |  YELLOW = 3-4d  |  RED = 5d+'
};

// ============================================================
// MENU + TRIGGERS
// ============================================================

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('⚡ DB Builder')
    .addItem('🔄 Rebuild All (DB + KPI)', 'buildAll')
    .addItem('🔄 Rebuild DB Only', 'buildDB')
    .addItem('⏰ Setup Auto-Refresh (hourly)', 'setupTriggers')
    .addToUi();
}

function onEdit(e) {
  try {
    var sheetName = e.source.getActiveSheet().getName();
    if (TSA_TABS.indexOf(sheetName) === -1 && DE_TABS.indexOf(sheetName) === -1) return;
    var cache = CacheService.getScriptCache();
    var last = cache.get('lastDBBuild');
    if (last && (Date.now() - parseInt(last)) < 30000) return;
    cache.put('lastDBBuild', Date.now().toString(), 120);
    buildDB();
  } catch(err) {}
}

function setupTriggers() {
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === 'buildAll' || t.getHandlerFunction() === 'buildDB')
      ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('buildAll').timeBased().everyHours(1).create();
  SpreadsheetApp.getUi().alert('Auto-refresh ativado: DB + KPI reconstroi a cada hora.');
}

function buildDB() { buildDB_(); }

function buildAll() {
  var allRows = buildDB_();
  buildKPIDashboardV2_(allRows);
}

// ============================================================
// DB BUILDER (returns allRows)
// ============================================================
function buildDB_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var allRows = [];

  TSA_TABS.forEach(function(tab) {
    var sheet = ss.getSheetByName(tab);
    if (!sheet || sheet.getLastRow() < 2) return;
    var data = sheet.getDataRange().getValues();
    var map = COLUMN_MAP[tab];

    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      var cf = getCell_(row, map.currentFocus);
      if (!cf) continue;

      var status = cleanStatus_(getCell_(row, map.status));
      var dt = getCell_(row, map.demandType);
      var cust = getCell_(row, map.customer);
      var da = row[map.dateAdd];
      var eta = row[map.eta];
      var dd = map.deliveryDate >= 0 && map.deliveryDate < row.length ? row[map.deliveryDate] : '';

      var daParsed = parseMinDate_(da);
      var etaParsed = parseMinDate_(eta);
      var ddParsed = parseMaxDate_(dd);

      var wr = daParsed ? weekRange_(daParsed) : '';
      allRows.push([
        tab, wr, cf, status, dt, classifyDemand_(dt), cust,
        daParsed || String(da || ''),
        etaParsed || String(eta || ''),
        ddParsed || String(dd || ''),
        calcPerf_(status, etaParsed, ddParsed, today),
        weekRef_(wr)
      ]);
    }
  });

  // DE_TABS now follow same column layout as TSA_TABS:
  // [0]Owner [1]Status [2]DemandType [3]Customer [4]CurrentFocus [5]DataAdd [6]ETA [7]LastUpdate [8]Blockers [9]REFERENCES [10]DeliveryDate [11]ETAReason
  DE_TABS.forEach(function(tab) {
    var sheet = ss.getSheetByName(tab);
    if (!sheet || sheet.getLastRow() < 2) return;
    var data = sheet.getDataRange().getValues();

    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      var personRaw = getCell_(row, 0);
      if (!personRaw) continue;
      var cf = getCell_(row, 4);
      if (!cf) continue;

      var status = cleanStatus_(getCell_(row, 1));
      var dt = getCell_(row, 2);
      var cust = getCell_(row, 3);
      var da = row[5];
      var eta = row[6];
      var dd = row.length > 10 ? row[10] : '';

      var daParsed = parseMinDate_(da);
      var etaParsed = parseMinDate_(eta);
      var ddParsed = parseMaxDate_(dd);
      var wr = daParsed ? weekRange_(daParsed) : '';

      var persons = String(personRaw).split('/').map(function(p) { return p.trim(); });
      for (var p = 0; p < persons.length; p++) {
        var name = persons[p].toUpperCase()
          .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        allRows.push([
          name, wr, cf, status, dt, classifyDemand_(dt), cust,
          daParsed || String(da || ''),
          etaParsed || String(eta || ''),
          ddParsed || String(dd || ''),
          calcPerf_(status, etaParsed, ddParsed, today),
          weekRef_(wr)
        ]);
      }
    }
  });

  allRows.sort(function(a, b) {
    if (a[0] !== b[0]) return a[0] < b[0] ? -1 : 1;
    var da1 = (a[7] instanceof Date) ? a[7] : (parseMaxDate_(a[7]) || new Date(1900, 0, 1));
    var da2 = (b[7] instanceof Date) ? b[7] : (parseMaxDate_(b[7]) || new Date(1900, 0, 1));
    return da1 - da2;
  });

  var dbSheet = ss.getSheetByName('DB');
  if (!dbSheet) dbSheet = ss.insertSheet('DB');
  dbSheet.clearContents();
  dbSheet.clearFormats();
  var existingFilter = dbSheet.getFilter();
  if (existingFilter) existingFilter.remove();
  var output = [DB_HEADERS].concat(allRows);
  dbSheet.getRange(1, 1, output.length, DB_HEADERS.length).setValues(output);
  formatDB_(dbSheet, output.length, DB_HEADERS.length);

  // Also sync to KPI sheet DB_Data tab
  syncDBToKPI_(output);

  return allRows;
}

function syncDBToKPI_(output) {
  try {
    var kpi = SpreadsheetApp.openById(KPI_ID);
    var tab = kpi.getSheetByName('DB_Data');
    if (!tab) tab = kpi.insertSheet('DB_Data');
    tab.clearContents();
    tab.clearFormats();
    var f = tab.getFilter(); if (f) f.remove();
    tab.getRange(1, 1, output.length, output[0].length).setValues(output);
    var hr = tab.getRange(1, 1, 1, output[0].length);
    hr.setBackground('#333333').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');
    tab.setFrozenRows(1);
    if (output.length > 1) tab.getRange(2, 8, output.length - 1, 3).setNumberFormat('yyyy-mm-dd');
    if (output.length > 1) tab.getRange(1, 1, output.length, output[0].length).createFilter();
  } catch(e) {
    Logger.log('syncDBToKPI_ error: ' + e);
  }
}

// ============================================================
// DB HELPERS (unchanged)
// ============================================================

function getCell_(row, idx) {
  if (idx < 0 || idx >= row.length) return '';
  var v = row[idx];
  if (v === null || v === undefined) return '';
  if (v instanceof Date) return v;
  return String(v).trim();
}

function cleanStatus_(raw) {
  if (!raw) return '';
  var s = String(raw);
  s = s.replace(/^[^\w\s]*/u, '').trim();
  s = s.replace(/^[\u26AA\u26AB\u2B55\u{1F534}\u{1F7E1}\u{1F7E2}\u{1F7E0}\u{1F7E3}\u{1F535}\s•·]*/u, '').trim();
  return s || String(raw).trim();
}

function parseDates_(val) {
  if (!val) return [];
  if (val instanceof Date && !isNaN(val.getTime())) {
    return [new Date(val.getFullYear(), val.getMonth(), val.getDate(), 12, 0, 0)];
  }
  var str = String(val).trim();
  if (!str) return [];
  var lines = str.split(/\n/);
  var dates = [];
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i].trim();
    if (!line) continue;
    var dt = tryParse_(line);
    if (dt) { dates.push(dt); continue; }
    var matches = line.match(/\d{1,2}\/\d{1,2}(?:\/\d{2,4})?/g);
    if (matches) {
      for (var j = 0; j < matches.length; j++) {
        dt = tryParse_(matches[j]);
        if (dt) dates.push(dt);
      }
    }
  }
  if (dates.length === 0) {
    var single = tryParse_(str);
    return single ? [single] : [];
  }
  return dates;
}

function parseMaxDate_(val) {
  var dates = parseDates_(val);
  return dates.length === 0 ? null : dates.reduce(function(mx, d) { return d > mx ? d : mx; });
}

function parseMinDate_(val) {
  var dates = parseDates_(val);
  return dates.length === 0 ? null : dates.reduce(function(mn, d) { return d < mn ? d : mn; });
}

function tryParse_(s) {
  if (!s) return null;
  s = s.replace(/^[^0-9A-Za-z]*/, '').trim();
  if (!s) return null;
  var m = s.match(/^(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?$/);
  if (m) {
    var yr = m[3] ? (m[3].length === 2 ? 2000 + parseInt(m[3]) : parseInt(m[3])) : 2026;
    return new Date(yr, parseInt(m[1]) - 1, parseInt(m[2]), 12, 0, 0);
  }
  m = s.match(/^(\d{1,2})-([A-Za-z]{3})(?:-(\d{2,4}))?/);
  if (m) {
    var yr2 = m[3] ? (m[3].length === 2 ? 2000 + parseInt(m[3]) : parseInt(m[3])) : 2026;
    var tmp = new Date(m[2] + ' ' + m[1] + ', ' + yr2);
    if (!isNaN(tmp.getTime())) return new Date(yr2, tmp.getMonth(), tmp.getDate(), 12, 0, 0);
  }
  m = s.match(/^([A-Za-z]{3,})\s+(\d{1,2})/);
  if (m) {
    var tmp2 = new Date(m[1] + ' ' + m[2] + ', 2026');
    if (!isNaN(tmp2.getTime())) return new Date(2026, tmp2.getMonth(), tmp2.getDate(), 12, 0, 0);
  }
  m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2]) - 1, parseInt(m[3]), 12, 0, 0);
  var native = new Date(s);
  if (!isNaN(native.getTime()) && native.getFullYear() >= 2000)
    return new Date(native.getFullYear(), native.getMonth(), native.getDate(), 12, 0, 0);
  return null;
}

function weekRange_(dt) {
  var day = dt.getDay();
  var diff = (day === 0) ? -6 : 1 - day;
  var mon = new Date(dt); mon.setDate(dt.getDate() + diff);
  var fri = new Date(mon); fri.setDate(mon.getDate() + 4);
  return pad2_(mon.getMonth()+1) + '/' + pad2_(mon.getDate()) + ' - ' +
         pad2_(fri.getMonth()+1) + '/' + pad2_(fri.getDate()) + '/' + fri.getFullYear();
}

function pad2_(n) { return n < 10 ? '0' + n : '' + n; }

function fmtDate_(dt) {
  if (!dt || isNaN(dt.getTime())) return '';
  return pad2_(dt.getMonth()+1) + '/' + pad2_(dt.getDate()) + '/' + dt.getFullYear();
}

function classifyDemand_(dt) {
  if (!dt) return 'Internal';
  return EXTERNAL_TYPES.indexOf(String(dt).toLowerCase()) >= 0 ? 'External' : 'Internal';
}

function calcPerf_(status, etaDt, ddDt, today) {
  var s = (status || '').toLowerCase();
  var isDone = s.indexOf('done') >= 0;
  var isActive = s.indexOf('in progress') >= 0 || s.indexOf('to do') >= 0;
  if (isDone) {
    if (!etaDt) return 'No ETA';
    if (!ddDt) return 'No Delivery Date';
    return ddDt <= etaDt ? 'On Time' : 'Late';
  }
  if (isActive) {
    if (!etaDt) return 'No ETA';
    return etaDt < today ? 'Overdue' : 'On Track';
  }
  if (etaDt && etaDt < today) return 'Overdue';
  return 'N/A';
}

function weekRef_(wr) {
  if (!wr) return '';
  var m = wr.match(/^(\d{1,2})\/(\d{1,2}).*\/(\d{4})$/);
  if (!m) return '';
  var month = parseInt(m[1]);
  var day = parseInt(m[2]);
  var year = m[3].slice(-2);
  var weekNum = Math.floor((day - 1) / 7) + 1;
  return year + '-' + pad2_(month) + ' W.' + weekNum;
}

function formatDB_(sheet, numRows, numCols) {
  if (numRows < 1) return;
  var hr = sheet.getRange(1, 1, 1, numCols);
  hr.setBackground('#333333').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');
  sheet.setFrozenRows(1);
  if (numRows > 1) sheet.getRange(2, 8, numRows - 1, 3).setNumberFormat('yyyy-mm-dd');
  for (var c = 1; c <= numCols; c++) sheet.autoResizeColumn(c);
  if (numRows > 1) sheet.getRange(1, 1, numRows, numCols).createFilter();
  var perfRange = sheet.getRange(2, 11, Math.max(numRows - 1, 1), 1);
  var dataRange = sheet.getRange(2, 1, Math.max(numRows - 1, 1), numCols);
  var catRange = sheet.getRange(2, 6, Math.max(numRows - 1, 1), 1);
  var rules = [];
  var colors = { 'On Time': '#b6d7a8', 'Late': '#f4cccc', 'Overdue': '#fce5cd', 'On Track': '#c9daf8' };
  for (var text in colors) {
    rules.push(SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(text).setBackground(colors[text]).setRanges([perfRange]).build());
  }
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('External').setBackground('#d9d2e9').setRanges([catRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=$K2="Late"').setBackground('#fce8e8').setRanges([dataRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=$K2="Overdue"').setBackground('#fff2e0').setRanges([dataRange]).build());
  sheet.setConditionalFormatRules(rules);
}


// ============================================================
// KPI DASHBOARD V2 BUILDER
// ============================================================

function parseWeekStart_(w) {
  if (!w) return null;
  var parts = w.split(' - ');
  if (parts.length !== 2) return null;
  var endParts = parts[1].trim().split('/');
  if (endParts.length !== 3) return null;
  var endYr = parseInt(endParts[2]);
  var startParts = parts[0].trim().split('/');
  if (startParts.length < 2) return null;
  var d = new Date(endYr, parseInt(startParts[0]) - 1, parseInt(startParts[1]), 12, 0, 0);
  var ed = new Date(endYr, parseInt(endParts[0]) - 1, parseInt(endParts[1]), 12, 0, 0);
  if (d > ed) d.setFullYear(d.getFullYear() - 1);
  return d;
}

function calcInd_(key, tasks) {
  if (!tasks || tasks.length === 0) return null;
  var ot, lt, od, days, i, da, dl, eta, diff;
  switch (key) {
    case 'S1':
      ot = 0; lt = 0;
      for (i = 0; i < tasks.length; i++) {
        if (tasks[i].demandCat === 'Internal') {
          if (tasks[i].perf === 'On Time') ot++;
          else if (tasks[i].perf === 'Late') lt++;
        }
      }
      return (ot + lt) > 0 ? ot / (ot + lt) : null;
    case 'S2':
      ot = 0; lt = 0;
      for (i = 0; i < tasks.length; i++) {
        if (tasks[i].demandCat === 'External') {
          if (tasks[i].perf === 'On Time') ot++;
          else if (tasks[i].perf === 'Late') lt++;
        }
      }
      return (ot + lt) > 0 ? ot / (ot + lt) : null;
    case 'S3':
      var cnt = 0;
      for (i = 0; i < tasks.length; i++) if (tasks[i].status.toLowerCase() === 'done') cnt++;
      return cnt;
    case 'S4':
      var c4 = 0;
      for (i = 0; i < tasks.length; i++) if (tasks[i].perf === 'Overdue') c4++;
      return c4;
    case 'S5':
      var c5 = 0;
      for (i = 0; i < tasks.length; i++) if (tasks[i].status.toLowerCase().indexOf('in progress') >= 0) c5++;
      return c5;
    case 'S6':
      var c6 = 0;
      for (i = 0; i < tasks.length; i++) if (tasks[i].demandCat === 'Internal') c6++;
      return c6;
    case 'S7':
      var c7 = 0;
      for (i = 0; i < tasks.length; i++) if (tasks[i].demandCat === 'External') c7++;
      return c7;
    case 'S8':
      days = [];
      for (i = 0; i < tasks.length; i++) {
        if (tasks[i].status.toLowerCase() === 'done') {
          da = toDate_(tasks[i].dateAdd); dl = toDate_(tasks[i].delivery);
          if (da && dl) { diff = Math.round((dl - da) / 86400000); if (diff >= 0 && diff <= 60) days.push(diff); }
        }
      }
      return days.length > 0 ? days.reduce(function(a,b){return a+b;},0) / days.length : null;
    case 'S9':
      ot = 0; lt = 0;
      for (i = 0; i < tasks.length; i++) {
        if (tasks[i].perf === 'On Time') ot++;
        else if (tasks[i].perf === 'Late') lt++;
      }
      return (ot + lt) > 0 ? ot / (ot + lt) : null;
    case 'S10':
      ot = 0; lt = 0; od = 0;
      for (i = 0; i < tasks.length; i++) {
        if (tasks[i].perf === 'On Time') ot++;
        else if (tasks[i].perf === 'Late') lt++;
        else if (tasks[i].perf === 'Overdue') od++;
      }
      return (ot + lt + od) > 0 ? ot / (ot + lt + od) : null;
    case 'S11':
      days = [];
      for (i = 0; i < tasks.length; i++) {
        if (tasks[i].perf === 'Late') {
          eta = toDate_(tasks[i].eta); dl = toDate_(tasks[i].delivery);
          if (eta && dl) { diff = Math.round((dl - eta) / 86400000); if (diff > 0) days.push(diff); }
        }
      }
      return days.length > 0 ? days.reduce(function(a,b){return a+b;},0) / days.length : null;
  }
  return null;
}

function toDate_(v) {
  if (v instanceof Date && !isNaN(v.getTime())) return v;
  if (!v) return null;
  return tryParse_(String(v));
}

function calcTeam_(key, byPM, moKey) {
  var vals = [];
  for (var mi = 0; mi < ALL_M.length; mi++) {
    var k = ALL_M[mi] + '|' + moKey;
    var tasks = byPM[k];
    if (tasks && tasks.length > 0) {
      var v = calcInd_(key, tasks);
      if (v !== null) vals.push(v);
    }
  }
  return vals.length > 0 ? vals.reduce(function(a,b){return a+b;},0) / vals.length : null;
}

function fmtVal_(val, f) {
  if (val === null || val === undefined) return '-';
  if (f === 'pct') return Math.round(val * 100) + '%';
  if (f === 'int') return Math.round(val);
  if (f === 'n1') return Math.round(val * 10) / 10;
  return val;
}

function getClr_(val, tv, mode) {
  if (val === null || val === undefined) return '#ECEFF1';
  if (mode === 'mo') return null; // monitor = no color
  if (mode === 'ph') return val >= tv ? '#C8E6C9' : val >= tv * 0.75 ? '#FFF9C4' : '#FFCDD2';
  if (mode === 'ch') return val >= tv ? '#C8E6C9' : val >= tv * 0.6 ? '#FFF9C4' : '#FFCDD2';
  if (mode === 'cl') return val <= tv ? '#C8E6C9' : val <= tv * 2 ? '#FFF9C4' : '#FFCDD2';
  if (mode === 'zb') return val === 0 ? '#C8E6C9' : val <= 2 ? '#FFF9C4' : '#FFCDD2';
  return null;
}

function buildKPIDashboardV2_(allRows) {
  var today = new Date(); today.setHours(0,0,0,0);
  var curMon = new Date(today);
  var dow = curMon.getDay();
  curMon.setDate(curMon.getDate() - dow + (dow === 0 ? -6 : 1));
  curMon.setHours(0,0,0,0);
  var cutoff = new Date(curMon); cutoff.setDate(cutoff.getDate() + 6);

  // Convert allRows to task objects + group
  var byPW = {}, byPM = {}, byP = {}, byW = {}, byMo = {};
  for (var i = 0; i < allRows.length; i++) {
    var r = allRows[i];
    var week = r[1];
    var wkDt = parseWeekStart_(week);
    if (!wkDt || wkDt < new Date(2025, 9, 1) || wkDt > cutoff) continue;

    var tsa = r[0];
    if (ALL_M.indexOf(tsa) === -1) continue;

    var task = {tsa:tsa, week:week, focus:String(r[2]), status:String(r[3]),
                demandType:String(r[4]), demandCat:String(r[5]), customer:String(r[6]),
                dateAdd:r[7], eta:r[8], delivery:r[9], perf:String(r[10])};

    var moKey = wkDt.getFullYear() + '-' + pad2_(wkDt.getMonth() + 1);
    var pwK = tsa + '|' + week;
    var pmK = tsa + '|' + moKey;

    if (!byPW[pwK]) byPW[pwK] = [];  byPW[pwK].push(task);
    if (!byPM[pmK]) byPM[pmK] = [];  byPM[pmK].push(task);
    if (!byP[tsa]) byP[tsa] = [];    byP[tsa].push(task);
    if (!byW[week]) byW[week] = [];  byW[week].push(task);
    if (!byMo[moKey]) byMo[moKey] = [];  byMo[moKey].push(task);
  }

  // Build week structure: all weeks Oct 2025 - Dec 2026
  var firstMon = new Date(2025, 9, 6); // Oct 6 2025
  var endDate = new Date(2026, 11, 31);
  var allGen = []; // [{wk, dt, future}]
  var d = new Date(firstMon);
  while (d <= endDate) {
    var fri = new Date(d); fri.setDate(d.getDate() + 4);
    var wk = pad2_(d.getMonth()+1) + '/' + pad2_(d.getDate()) + ' - ' +
             pad2_(fri.getMonth()+1) + '/' + pad2_(fri.getDate()) + '/' + fri.getFullYear();
    allGen.push({wk: wk, dt: new Date(d), future: d > curMon});
    d.setDate(d.getDate() + 7);
  }

  // Map task weeks to generated weeks
  var taskWkDates = {};
  for (var i = 0; i < allRows.length; i++) {
    var w = allRows[i][1];
    if (w && !taskWkDates[w]) { var wd = parseWeekStart_(w); if (wd) taskWkDates[w] = wd; }
  }
  var twMap = {}; // genWk -> origWk
  for (var origW in taskWkDates) {
    var origDt = taskWkDates[origW];
    if (origDt < new Date(2025, 9, 1) || origDt > cutoff) continue;
    var oMon = new Date(origDt);
    var odow = oMon.getDay();
    oMon.setDate(oMon.getDate() - odow + (odow === 0 ? -6 : 1));
    for (var g = 0; g < allGen.length; g++) {
      if (allGen[g].dt.getTime() === oMon.getTime()) { twMap[allGen[g].wk] = origW; break; }
    }
  }

  // Build columns: [{type, label, moKey, yr, mo, future, origWk, fullDate}]
  var cols = [];
  var monthGroups = {}; // moKey -> [indices in allGen]
  var moOrder = [];
  for (var g = 0; g < allGen.length; g++) {
    var yr = allGen[g].dt.getFullYear(), mo = allGen[g].dt.getMonth() + 1;
    var mk = yr + '-' + pad2_(mo);
    if (!monthGroups[mk]) { monthGroups[mk] = []; moOrder.push({k:mk, yr:yr, mo:mo}); }
    monthGroups[mk].push(g);
  }

  for (var mi = 0; mi < moOrder.length; mi++) {
    var mI = moOrder[mi];
    var gIdxs = monthGroups[mI.k];
    for (var wi = 0; wi < gIdxs.length; wi++) {
      var gen = allGen[gIdxs[wi]];
      var origW = twMap[gen.wk] || null;
      var fri2 = new Date(gen.dt); fri2.setDate(gen.dt.getDate() + 4);
      cols.push({
        type:'week', label:'W'+String(wi+1), moKey:mI.k, yr:mI.yr, mo:mI.mo,
        future:gen.future, origWk:origW,
        fullDate:(gen.dt.getMonth()+1)+'/'+gen.dt.getDate()+' - '+(fri2.getMonth()+1)+'/'+fri2.getDate()
      });
    }
    var moLbl = MONTH_ABBR_[mI.mo] || ('M'+mI.mo);
    if (mI.yr === 2025) moLbl += ' 25';
    var allFut = gIdxs.every(function(gi) { return allGen[gi].future; });
    cols.push({type:'month', label:moLbl, moKey:mI.k, yr:mI.yr, mo:mI.mo, future:allFut});
  }
  cols.push({type:'overall', label:'OVERALL', future:false});

  var NC = 1 + cols.length; // total columns

  // ============ BUILD GRID ============
  var vals = [], bgs = [], notes = [], fws = [], fcs = [];

  function emptyRow() { var r = []; for (var c = 0; c < NC; c++) r.push(''); return r; }
  function emptyBgRow(clr) { var r = []; for (var c = 0; c < NC; c++) r.push(clr || null); return r; }

  // Row 0: Month headers
  var r0 = emptyRow(), b0 = emptyBgRow('#1B2838'), n0 = emptyRow(), fw0 = emptyBgRow('bold'), fc0 = emptyBgRow('#ffffff');
  r0[0] = 'Month';
  // Fill month names via merge groups
  var merges = []; // [{r, c1, c2}]
  var prevMo = null, mStart = -1;
  for (var ci = 0; ci < cols.length; ci++) {
    var col = cols[ci];
    var mk2 = col.moKey || 'overall';
    if (mk2 !== prevMo) {
      if (prevMo !== null && mStart >= 0) merges.push({r:0, c1:mStart+1, c2:ci+1});
      prevMo = mk2;
      mStart = ci;
      if (col.type !== 'overall') {
        var mFullName = MO_FULL[col.mo] || '';
        if (col.yr === 2025) mFullName += ' 25';
        r0[ci + 1] = mFullName;
      }
      if (col.future && col.type !== 'overall') { b0[ci+1] = '#2C3E50'; fc0[ci+1] = '#8899AA'; }
    } else {
      if (col.future && col.type !== 'overall') { b0[ci+1] = '#2C3E50'; fc0[ci+1] = '#8899AA'; }
    }
  }
  if (prevMo !== null && mStart >= 0) merges.push({r:0, c1:mStart+1, c2:cols.length+1});

  vals.push(r0); bgs.push(b0); notes.push(n0); fws.push(fw0); fcs.push(fc0);

  // Row 1: Week/col labels
  var r1 = ['Week'], b1 = ['#34495E'], n1 = [''], fw1 = ['bold'], fc1 = ['#ffffff'];
  for (var ci = 0; ci < cols.length; ci++) {
    r1.push(cols[ci].label);
    n1.push(''); // week date notes removed — user prefers clean headers
    fw1.push('bold');
    if (cols[ci].future) { b1.push('#C8D1DB'); fc1.push('#99AABB'); }
    else if (cols[ci].type === 'month') { b1.push('#1A5276'); fc1.push('#ffffff'); }
    else if (cols[ci].type === 'overall') { b1.push('#154360'); fc1.push('#ffffff'); }
    else { b1.push('#34495E'); fc1.push('#ffffff'); }
  }
  vals.push(r1); bgs.push(b1); notes.push(n1); fws.push(fw1); fcs.push(fc1);

  // Indicator blocks
  for (var ii = 0; ii < IND_DEFS.length; ii++) {
    var ind = IND_DEFS[ii];
    var darkC = IND_CLR[ind.k] ? IND_CLR[ind.k][0] : '#34495E';
    var lightC = IND_CLR[ind.k] ? IND_CLR[ind.k][1] : '#EBF5FB';

    // Header row
    var rH = emptyRow(), bH = emptyBgRow(darkC), nH = emptyRow(), fwH = emptyBgRow('bold'), fcH = emptyBgRow('#ffffff');
    rH[0] = ind.n; rH[1] = 'Target: ' + ind.t;
    nH[0] = IND_NOTES[ind.k] || '';
    for (var ci = 0; ci < cols.length; ci++) {
      if (cols[ci].future) { bH[ci+1] = lightC; fcH[ci+1] = '#666666'; }
    }
    vals.push(rH); bgs.push(bH); notes.push(nH); fws.push(fwH); fcs.push(fcH);

    // Person rows
    for (var pi = 0; pi < ALL_M.length; pi++) {
      var member = ALL_M[pi];
      var rowBg = pi % 2 === 0 ? lightC : '#ffffff';
      var rP = [DISP[member]], bP = [rowBg], nP = [''], fwP = ['bold'], fcP = ['#333333'];

      for (var ci = 0; ci < cols.length; ci++) {
        var col = cols[ci];
        if (col.future) {
          rP.push(''); bP.push('#F7F9FC'); nP.push(''); fwP.push('normal'); fcP.push('#BBBBBB');
          continue;
        }

        var tList = null;
        if (col.type === 'week') {
          tList = col.origWk ? (byPW[member + '|' + col.origWk] || null) : null;
        } else if (col.type === 'month') {
          tList = byPM[member + '|' + col.moKey] || null;
        } else {
          tList = byP[member] || null;
        }

        var val = tList ? calcInd_(ind.k, tList) : null;
        // S3 monthly/overall: avg per week
        if (ind.k === 'S3' && val !== null && col.type !== 'week' && tList) {
          var wks = {};
          for (var t = 0; t < tList.length; t++) if (tList[t].week) wks[tList[t].week] = true;
          var aw = Object.keys(wks).length;
          if (aw > 0) val = val / aw;
        }

        var fv = fmtVal_(val, ind.f);
        rP.push(fv);
        var clr = getClr_(val, ind.tv, ind.m);
        bP.push(clr || rowBg);
        if (val === null) { bP[bP.length - 1] = '#ECEFF1'; fcP.push('#999999'); }
        else { fcP.push(col.type === 'month' || col.type === 'overall' ? '#1A5276' : '#333333'); }
        nP.push('');
        fwP.push(col.type === 'month' || col.type === 'overall' ? 'bold' : 'normal');
      }
      vals.push(rP); bgs.push(bP); notes.push(nP); fws.push(fwP); fcs.push(fcP);
    }

    // TEAM AVG row
    var rT = ['TEAM AVG'], bT = ['#D4E6F1'], nT = [''], fwT = ['bold'], fcT = ['#1A5276'];
    for (var ci = 0; ci < cols.length; ci++) {
      var col = cols[ci];
      if (col.future) {
        rT.push(''); bT.push('#F7F9FC'); nT.push(''); fwT.push('normal'); fcT.push('#BBBBBB');
        continue;
      }
      var moKey2;
      if (col.type === 'week') moKey2 = col.origWk || '';
      else if (col.type === 'month') moKey2 = col.moKey;
      else moKey2 = 'ALL';

      var val2;
      if (col.type === 'week') {
        // Team avg for this week: avg of members who have data
        var vls = [];
        for (var mi2 = 0; mi2 < ALL_M.length; mi2++) {
          var k2 = ALL_M[mi2] + '|' + (col.origWk || '');
          var tl2 = byPW[k2];
          if (tl2 && tl2.length > 0) {
            var v2 = calcInd_(ind.k, tl2);
            if (v2 !== null) vls.push(v2);
          }
        }
        val2 = vls.length > 0 ? vls.reduce(function(a,b){return a+b;},0) / vls.length : null;
      } else if (col.type === 'month') {
        val2 = calcTeam_(ind.k, byPM, col.moKey);
        if (ind.k === 'S3' && val2 !== null) {
          // Avg throughput per week per person
          var pw2 = [];
          for (var mi3 = 0; mi3 < ALL_M.length; mi3++) {
            var tl3 = byPM[ALL_M[mi3] + '|' + col.moKey];
            if (tl3 && tl3.length > 0) {
              var d3 = 0, wks3 = {};
              for (var t3 = 0; t3 < tl3.length; t3++) {
                if (tl3[t3].status.toLowerCase() === 'done') d3++;
                if (tl3[t3].week) wks3[tl3[t3].week] = true;
              }
              var aw3 = Object.keys(wks3).length;
              if (aw3 > 0) pw2.push(d3 / aw3);
            }
          }
          val2 = pw2.length > 0 ? pw2.reduce(function(a,b){return a+b;},0) / pw2.length : val2;
        }
      } else {
        // Overall team avg
        var vls2 = [];
        for (var mi4 = 0; mi4 < ALL_M.length; mi4++) {
          var tl4 = byP[ALL_M[mi4]];
          if (tl4 && tl4.length > 0) {
            var v4 = calcInd_(ind.k, tl4);
            if (v4 !== null) {
              if (ind.k === 'S3') {
                var wks4 = {};
                for (var t4 = 0; t4 < tl4.length; t4++) if (tl4[t4].week) wks4[tl4[t4].week] = true;
                var aw4 = Object.keys(wks4).length;
                if (aw4 > 0) v4 = v4 / aw4;
              }
              vls2.push(v4);
            }
          }
        }
        val2 = vls2.length > 0 ? vls2.reduce(function(a,b){return a+b;},0) / vls2.length : null;
      }

      var fv2 = fmtVal_(val2, ind.f);
      rT.push(fv2);
      bT.push(val2 === null ? '#ECEFF1' : '#D4E6F1');
      nT.push('');
      fwT.push('bold');
      fcT.push(val2 === null ? '#999999' : '#1A5276');
    }
    vals.push(rT); bgs.push(bT); notes.push(nT); fws.push(fwT); fcs.push(fcT);

    // Blank separator
    vals.push(emptyRow()); bgs.push(emptyBgRow('#ffffff')); notes.push(emptyRow());
    fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));
  }

  // ============ ADDITIONAL INDICATORS (S12-S14) ============
  var addHdr = emptyRow(), addBg = emptyBgRow('#566573');
  addHdr[0] = 'ADDITIONAL INDICATORS';
  var addFw = emptyBgRow('bold'), addFc = emptyBgRow('#ffffff');
  vals.push(addHdr); bgs.push(addBg); notes.push(emptyRow()); fws.push(addFw); fcs.push(addFc);

  var tblH = ['Indicator','Target'];
  for (var m = 0; m < ALL_M.length; m++) tblH.push(DISP[ALL_M[m]]);
  tblH.push('TEAM');
  while (tblH.length < NC) tblH.push('');
  var tblBg = []; for (var c = 0; c < NC; c++) tblBg.push('#34495E');
  var tblFw = []; for (var c = 0; c < NC; c++) tblFw.push('bold');
  var tblFc = []; for (var c = 0; c < NC; c++) tblFc.push('#ffffff');
  vals.push(tblH); bgs.push(tblBg); notes.push(emptyRow()); fws.push(tblFw); fcs.push(tblFc);

  // S12 - Customer Concentration
  var s12r = ['S12 Customer Conc.','<40%'], s12b = ['#ffffff','#ffffff'], s12n = ['S12: Top customer % of tasks. >40% = risk',''];
  for (var m = 0; m < ALL_M.length; m++) {
    var mt = byP[ALL_M[m]] || [];
    var cc = {};
    for (var t = 0; t < mt.length; t++) { var cst = (mt[t].customer || '').trim() || '(none)'; cc[cst] = (cc[cst]||0)+1; }
    var topN = 0, topC = '-';
    for (var k in cc) if (cc[k] > topN) { topN = cc[k]; topC = k; }
    var s12v = mt.length > 0 ? topN / mt.length : null;
    s12r.push(s12v !== null ? Math.round(s12v*100)+'%' : '-');
    s12b.push(s12v === null ? '#ECEFF1' : s12v <= 0.40 ? '#C8E6C9' : s12v <= 0.55 ? '#FFF9C4' : '#FFCDD2');
    s12n.push(topC !== '-' && topC !== '(none)' ? 'Top: '+topC.substring(0,25) : '');
  }
  s12r.push('-'); s12b.push('#D4E6F1'); s12n.push('');
  while (s12r.length < NC) { s12r.push(''); s12b.push(null); s12n.push(''); }
  vals.push(s12r); bgs.push(s12b); notes.push(s12n);
  fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));

  // S13 - Recovery Rate
  var s13r = ['S13 Recovery Rate','>50%'], s13b = ['#ffffff','#ffffff'], s13n = ['S13: Late/(Late+Overdue). Resolved problems.',''];
  for (var m = 0; m < ALL_M.length; m++) {
    var mt = byP[ALL_M[m]] || [];
    var rec = 0, ovd = 0;
    for (var t = 0; t < mt.length; t++) { if (mt[t].perf==='Late') rec++; if (mt[t].perf==='Overdue') ovd++; }
    var tp = rec+ovd, s13v = tp > 0 ? rec/tp : null;
    s13r.push(s13v !== null ? Math.round(s13v*100)+'%' : '-');
    s13b.push(s13v === null ? '#ECEFF1' : s13v >= 0.50 ? '#C8E6C9' : s13v >= 0.30 ? '#FFF9C4' : '#FFCDD2');
    s13n.push('');
  }
  s13r.push('-'); s13b.push('#D4E6F1'); s13n.push('');
  while (s13r.length < NC) { s13r.push(''); s13b.push(null); s13n.push(''); }
  vals.push(s13r); bgs.push(s13b); notes.push(s13n);
  fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));

  // S14 - Predictive Risk
  var s14r = ['S14 Predictive Risk','0'], s14b = ['#ffffff','#ffffff'], s14n = ['S14: In Progress >80% elapsed',''];
  for (var m = 0; m < ALL_M.length; m++) {
    var mt = byP[ALL_M[m]] || [];
    var risk = 0;
    for (var t = 0; t < mt.length; t++) {
      if (mt[t].status.toLowerCase().indexOf('in progress') >= 0) {
        var da = toDate_(mt[t].dateAdd), eta = toDate_(mt[t].eta);
        if (da && eta && eta > da) {
          var planned = (eta - da) / 86400000, elapsed = (today - da) / 86400000;
          if (planned > 0 && elapsed > planned * 0.8) risk++;
        }
      }
    }
    s14r.push(risk);
    s14b.push(risk === 0 ? '#C8E6C9' : risk <= 1 ? '#FFF9C4' : '#FFCDD2');
    s14n.push('');
  }
  s14r.push('-'); s14b.push('#D4E6F1'); s14n.push('');
  while (s14r.length < NC) { s14r.push(''); s14b.push(null); s14n.push(''); }
  vals.push(s14r); bgs.push(s14b); notes.push(s14n);
  fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));

  // Blank
  vals.push(emptyRow()); bgs.push(emptyBgRow('#ffffff')); notes.push(emptyRow());
  fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));

  // ============ DATA QUALITY ============
  var dqH = emptyRow(); dqH[0] = 'DATA QUALITY';
  vals.push(dqH); bgs.push(emptyBgRow('#5D6D7E')); notes.push(emptyRow());
  fws.push(emptyBgRow('bold')); fcs.push(emptyBgRow('#ffffff'));

  var dqTH = ['Person','Total','No Date','No ETA','No Cust','Same-Day','Quality'];
  while (dqTH.length < NC) dqTH.push('');
  vals.push(dqTH); bgs.push(emptyBgRow('#34495E')); notes.push(emptyRow());
  fws.push(emptyBgRow('bold')); fcs.push(emptyBgRow('#ffffff'));

  for (var pi = 0; pi < ALL_M.length; pi++) {
    var mt = byP[ALL_M[pi]] || [];
    var tot = mt.length;
    var done = mt.filter(function(t){return t.status.toLowerCase()==='done';});
    var noDA = mt.filter(function(t){return !String(t.dateAdd||'').trim();}).length;
    var noETA = mt.filter(function(t){return !String(t.eta||'').trim();}).length;
    var noCust = mt.filter(function(t){return !t.customer.trim();}).length;
    var same = done.filter(function(t){
      var a=String(t.dateAdd||''),b=String(t.eta||''),c=String(t.delivery||'');
      return a && b && c && a===b && b===c;
    }).length;
    var issues = noDA+noETA+noCust+same;
    var mx = tot*4||1;
    var qs = Math.max(0, Math.round((1-issues/mx)*100));

    var dqR = [DISP[ALL_M[pi]], tot, noDA, noETA, noCust, same, qs+'%'];
    while (dqR.length < NC) dqR.push('');
    var dqBg = emptyBgRow(pi%2===0 ? '#F2F3F5' : '#ffffff');
    dqBg[6] = qs >= 85 ? '#C8E6C9' : qs >= 60 ? '#FFF9C4' : '#FFCDD2';
    vals.push(dqR); bgs.push(dqBg); notes.push(emptyRow());
    fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));
  }

  // Blank
  vals.push(emptyRow()); bgs.push(emptyBgRow('#ffffff')); notes.push(emptyRow());
  fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));

  // ============ TASK DISTRIBUTION ============
  var tdH = emptyRow(); tdH[0] = 'TASK DISTRIBUTION';
  vals.push(tdH); bgs.push(emptyBgRow('#5D6D7E')); notes.push(emptyRow());
  fws.push(emptyBgRow('bold')); fcs.push(emptyBgRow('#ffffff'));

  var tdTH = ['Person','Total','Done','In Prog','On Time','Late','Overdue','OT Rate','Load %'];
  while (tdTH.length < NC) tdTH.push('');
  vals.push(tdTH); bgs.push(emptyBgRow('#34495E')); notes.push(emptyRow());
  fws.push(emptyBgRow('bold')); fcs.push(emptyBgRow('#ffffff'));

  var totalAll = 0;
  for (var m = 0; m < ALL_M.length; m++) totalAll += (byP[ALL_M[m]]||[]).length;

  for (var pi = 0; pi < ALL_M.length; pi++) {
    var mt = byP[ALL_M[pi]] || [];
    var dn = mt.filter(function(t){return t.status.toLowerCase()==='done';}).length;
    var ip = mt.filter(function(t){return t.status.toLowerCase().indexOf('in progress')>=0;}).length;
    var ot = mt.filter(function(t){return t.perf==='On Time';}).length;
    var lt = mt.filter(function(t){return t.perf==='Late';}).length;
    var od = mt.filter(function(t){return t.perf==='Overdue';}).length;
    var rate = (ot+lt) > 0 ? Math.round(ot/(ot+lt)*100)+'%' : '-';
    var share = totalAll > 0 ? Math.round(mt.length/totalAll*100)+'%' : '-';

    var tdR = [DISP[ALL_M[pi]], mt.length, dn, ip, ot, lt, od, rate, share];
    while (tdR.length < NC) tdR.push('');
    var tdBg = emptyBgRow(pi%2===0 ? '#F2F3F5' : '#ffffff');
    if (od >= 3) tdBg[6] = '#FFCDD2';
    vals.push(tdR); bgs.push(tdBg); notes.push(emptyRow());
    fws.push(emptyBgRow('normal')); fcs.push(emptyBgRow('#333333'));
  }

  // ============ WRITE TO SHEET ============
  var NR = vals.length;
  Logger.log('Dashboard: ' + NR + ' rows x ' + NC + ' cols');

  var kpi = SpreadsheetApp.openById(KPI_ID);
  var sheet = kpi.getSheetByName(DASH_TAB);
  if (!sheet) sheet = kpi.insertSheet(DASH_TAB);
  sheet.clearContents();
  sheet.clearFormats();
  var f = sheet.getFilter(); if (f) f.remove();

  // Ensure enough rows/cols
  if (sheet.getMaxRows() < NR) sheet.insertRowsAfter(sheet.getMaxRows(), NR - sheet.getMaxRows());
  if (sheet.getMaxColumns() < NC) sheet.insertColumnsAfter(sheet.getMaxColumns(), NC - sheet.getMaxColumns());

  // Bulk write values
  sheet.getRange(1, 1, NR, NC).setValues(vals);

  // Bulk write backgrounds (convert nulls to white)
  for (var ri = 0; ri < bgs.length; ri++)
    for (var ci = 0; ci < bgs[ri].length; ci++)
      if (!bgs[ri][ci]) bgs[ri][ci] = '#ffffff';
  sheet.getRange(1, 1, NR, NC).setBackgrounds(bgs);

  // Bulk write font weights
  sheet.getRange(1, 1, NR, NC).setFontWeights(fws);

  // Bulk write font colors
  sheet.getRange(1, 1, NR, NC).setFontColors(fcs);

  // Bulk write notes
  sheet.getRange(1, 1, NR, NC).setNotes(notes);

  // Center all
  sheet.getRange(1, 1, NR, NC).setHorizontalAlignment('center').setVerticalAlignment('middle')
    .setWrap(true).setFontFamily('Segoe UI').setFontSize(9);

  // Col A left-aligned
  sheet.getRange(1, 1, NR, 1).setHorizontalAlignment('left');

  // Merges for month headers (row 1)
  for (var mg = 0; mg < merges.length; mg++) {
    var mrg = merges[mg];
    if (mrg.c2 - mrg.c1 > 1) {
      sheet.getRange(mrg.r + 1, mrg.c1 + 1, 1, mrg.c2 - mrg.c1).merge();
    }
  }

  // Column widths
  sheet.setColumnWidth(1, 130); // Col A
  for (var ci = 0; ci < cols.length; ci++) {
    var c = ci + 2; // 1-based col
    if (cols[ci].future && cols[ci].type === 'week') sheet.setColumnWidth(c, 35);
    else if (cols[ci].type === 'week') sheet.setColumnWidth(c, 48);
    else if (cols[ci].type === 'month') sheet.setColumnWidth(c, 58);
    else sheet.setColumnWidth(c, 68);
  }

  // Freeze
  sheet.setFrozenRows(2);
  sheet.setFrozenColumns(1);
  sheet.setHiddenGridlines(true);

  // Tab color
  sheet.setTabColor('#1B2838');

  // Delete excess rows/cols
  if (sheet.getMaxRows() > NR + 5) sheet.deleteRows(NR + 1, sheet.getMaxRows() - NR - 5);
  if (sheet.getMaxColumns() > NC + 2) sheet.deleteColumns(NC + 1, sheet.getMaxColumns() - NC - 2);

  Logger.log('Dashboard V2 written: ' + NR + ' rows');
}
