
/**
 * TSA DB Builder - Auto-maintains the DB tab.
 * Triggers: onEdit (any TSA tab) + hourly backup + manual menu.
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
// THAIS_YASMIN column map: person=0, task=1, linearLink=2, customer=3, tsa=4, eta=5, dd=6, deliveryStatus=7
var EXTERNAL_TYPES = ['external(customer)', 'external (customer)', 'incident'];
var DB_HEADERS = ['TSA', 'Week Range', 'Current Focus', 'Status', 'Demand Type',
                  'Demand Category', 'Customer', 'Date Add', 'ETA', 'Delivery Date',
                  'Delivery Performance', 'Week Ref'];
var MONTH_ABBR_ = ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                   'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('⚡ DB Builder')
    .addItem('🔄 Rebuild DB Now', 'buildDB')
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
  } catch(err) {
    // Silent fail on edit trigger
  }
}

function setupTriggers() {
  // Remove old triggers for buildDB
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === 'buildDB') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('buildDB').timeBased().everyHours(1).create();
  SpreadsheetApp.getUi().alert('Auto-refresh ativado: DB reconstroi a cada hora.');
}

function buildDB() {
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
        tab,
        wr,
        cf,
        status,
        dt,
        classifyDemand_(dt),
        cust,
        daParsed || String(da || ''),
        etaParsed || String(eta || ''),
        ddParsed || String(dd || ''),
        calcPerf_(status, etaParsed, ddParsed, today),
        weekRef_(wr)
      ]);
    }
  });

  // Process DE tabs (THAIS_YASMIN) - different column structure
  DE_TABS.forEach(function(tab) {
    var sheet = ss.getSheetByName(tab);
    if (!sheet || sheet.getLastRow() < 2) return;
    var data = sheet.getDataRange().getValues();

    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      var personRaw = getCell_(row, 0);
      if (!personRaw) continue;
      var task = getCell_(row, 1);
      if (!task) continue;

      var cust = getCell_(row, 3);
      var etaRaw = row[5];
      var ddRaw = row[6];
      var deliveryStatus = getCell_(row, 7);

      // Derive status for calcPerf_: On Time/Late = Done, On Track = In Progress
      var status = '';
      var ds = (deliveryStatus || '').toLowerCase();
      if (ds === 'on time' || ds === 'late') status = 'Done';
      else if (ds === 'on track') status = 'In Progress';

      var etaParsed = parseMinDate_(etaRaw);
      var ddParsed = parseMaxDate_(ddRaw);
      var daParsed = etaParsed; // Use ETA as Date Add (no separate column)

      var wr = daParsed ? weekRange_(daParsed) : '';

      // Split person on "/" to create separate rows
      var persons = String(personRaw).split('/').map(function(p) { return p.trim(); });
      for (var p = 0; p < persons.length; p++) {
        var name = persons[p].toUpperCase()
          .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        allRows.push([
          name,
          wr,
          task,
          status,
          'external (customer)',
          'External',
          cust,
          daParsed || String(etaRaw || ''),
          etaParsed || String(etaRaw || ''),
          ddParsed || String(ddRaw || ''),
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

  // Clear all
  dbSheet.clearContents();
  dbSheet.clearFormats();
  var existingFilter = dbSheet.getFilter();
  if (existingFilter) existingFilter.remove();

  // Write
  var output = [DB_HEADERS].concat(allRows);
  dbSheet.getRange(1, 1, output.length, DB_HEADERS.length).setValues(output);

  // Format
  formatDB_(dbSheet, output.length, DB_HEADERS.length);
}

// --- Helpers ---

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
  // Remove leading emoji/symbols
  s = s.replace(/^[^\w\s]*/u, '').trim();
  // Fallback: remove specific unicode ranges
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
  if (dates.length === 0) return null;
  return dates.reduce(function(mx, d) { return d > mx ? d : mx; });
}

function parseMinDate_(val) {
  var dates = parseDates_(val);
  if (dates.length === 0) return null;
  return dates.reduce(function(mn, d) { return d < mn ? d : mn; });
}

function tryParse_(s) {
  if (!s) return null;
  s = s.replace(/^[^0-9A-Za-z]*/, '').trim();
  if (!s) return null;

  // M/D/Y or M/D
  var m = s.match(/^(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?$/);
  if (m) {
    var yr = m[3] ? (m[3].length === 2 ? 2000 + parseInt(m[3]) : parseInt(m[3])) : 2026;
    return new Date(yr, parseInt(m[1]) - 1, parseInt(m[2]), 12, 0, 0);
  }

  // D-Mon or D-Mon-Y
  m = s.match(/^(\d{1,2})-([A-Za-z]{3})(?:-(\d{2,4}))?/);
  if (m) {
    var yr2 = m[3] ? (m[3].length === 2 ? 2000 + parseInt(m[3]) : parseInt(m[3])) : 2026;
    var dt = new Date(yr2, 0, 1, 12, 0, 0);
    var tmp = new Date(m[2] + ' ' + m[1] + ', ' + yr2);
    if (!isNaN(tmp.getTime())) return new Date(yr2, tmp.getMonth(), tmp.getDate(), 12, 0, 0);
  }

  // Mon D
  m = s.match(/^([A-Za-z]{3,})\s+(\d{1,2})/);
  if (m) {
    var tmp2 = new Date(m[1] + ' ' + m[2] + ', 2026');
    if (!isNaN(tmp2.getTime())) return new Date(2026, tmp2.getMonth(), tmp2.getDate(), 12, 0, 0);
  }

  // Y-M-D
  m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);
  if (m) {
    return new Date(parseInt(m[1]), parseInt(m[2]) - 1, parseInt(m[3]), 12, 0, 0);
  }

  // Native fallback
  var native = new Date(s);
  if (!isNaN(native.getTime()) && native.getFullYear() >= 2000) {
    return new Date(native.getFullYear(), native.getMonth(), native.getDate(), 12, 0, 0);
  }

  return null;
}

function weekRange_(dt) {
  var day = dt.getDay();
  var diff = (day === 0) ? -6 : 1 - day;
  var mon = new Date(dt);
  mon.setDate(dt.getDate() + diff);
  var fri = new Date(mon);
  fri.setDate(mon.getDate() + 4);
  return pad2_(mon.getMonth()+1) + '/' + pad2_(mon.getDate()) +
         ' - ' +
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

  // Header
  var hr = sheet.getRange(1, 1, 1, numCols);
  hr.setBackground('#333333').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');
  sheet.setFrozenRows(1);

  // Date format for Date Add (H=8), ETA (I=9), Delivery Date (J=10)
  if (numRows > 1) {
    sheet.getRange(2, 8, numRows - 1, 3).setNumberFormat('yyyy-mm-dd');
  }

  // Auto-resize
  for (var c = 1; c <= numCols; c++) sheet.autoResizeColumn(c);

  // Filter
  if (numRows > 1) sheet.getRange(1, 1, numRows, numCols).createFilter();

  // Conditional formatting
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
