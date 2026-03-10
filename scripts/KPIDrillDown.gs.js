/**
 * KPI Drill-Down Sidebar — bound to KPI_Team_Raccoons spreadsheet.
 * Menu: "⚡ KPI Tools" → "🔍 Drill Down"
 * Reads the active cell, determines TSA/DE + week + KPI section,
 * queries DB_Data in the CORTEX spreadsheet, and shows filtered
 * tasks in an HTML sidebar.
 */

var DB_SPREADSHEET_ID = '1XaJgJCExt_dQ-RBY0eINP-0UCnCH7hYjGC3ibPlluzw';
var DB_SHEET_NAME = 'DB';

// DB column indices (0-based): A=TSA, B=Week, C=Focus, D=Status, E=DemandType, F=Category, G=Customer, H=DateAdd, I=ETA, J=DeliveryDate, K=Performance
var DB_COL = { TSA: 0, WEEK: 1, FOCUS: 2, STATUS: 3, DEMAND_TYPE: 4, CATEGORY: 5, CUSTOMER: 6, DATE_ADD: 7, ETA: 8, DD: 9, PERF: 10 };

// Section configs per tab. startRow/endRow are 1-indexed (sheet rows).
var TAB_CONFIGS = {
  'Thiago Calculations': {
    nameCol: 4,  // Column D (1-indexed)
    weekRow: 3,  // Row 3 has DB week-range strings
    firstDataCol: 5,  // Column E (1-indexed)
    sections: [
      { name: 'Internal Delivery',  startRow: 6,  endRow: 10, filters: [{ dbCol: DB_COL.CATEGORY, values: ['Internal'] }, { dbCol: DB_COL.PERF, values: ['On Time', 'Late'] }] },
      { name: 'External Delivery',  startRow: 13, endRow: 17, filters: [{ dbCol: DB_COL.CATEGORY, values: ['External'] }, { dbCol: DB_COL.PERF, values: ['On Time', 'Late'] }] },
      { name: 'Throughput',         startRow: 20, endRow: 24, filters: [{ dbCol: DB_COL.STATUS, values: ['Done'] }] },
      { name: 'Overdue Snapshot',   startRow: 27, endRow: 31, filters: [{ dbCol: DB_COL.PERF, values: ['Overdue'] }] },
      { name: 'WIP',                startRow: 34, endRow: 38, filters: [{ dbCol: DB_COL.STATUS, values: ['In Progress'] }] },
      { name: 'Internal Tasks',     startRow: 41, endRow: 45, filters: [{ dbCol: DB_COL.CATEGORY, values: ['Internal'] }] },
      { name: 'External Tasks',     startRow: 48, endRow: 52, filters: [{ dbCol: DB_COL.CATEGORY, values: ['External'] }] }
    ]
  },
  'Thais Calculations': {
    nameCol: 4,
    weekRow: 3,
    firstDataCol: 5,
    sections: [
      { name: 'Internal Delivery',  startRow: 6,  endRow: 7,  filters: [{ dbCol: DB_COL.CATEGORY, values: ['Internal'] }, { dbCol: DB_COL.PERF, values: ['On Time', 'Late'] }] },
      { name: 'External Delivery',  startRow: 10, endRow: 11, filters: [{ dbCol: DB_COL.CATEGORY, values: ['External'] }, { dbCol: DB_COL.PERF, values: ['On Time', 'Late'] }] },
      { name: 'Throughput',         startRow: 14, endRow: 15, filters: [{ dbCol: DB_COL.STATUS, values: ['Done'] }] },
      { name: 'Overdue Snapshot',   startRow: 18, endRow: 19, filters: [{ dbCol: DB_COL.PERF, values: ['Overdue'] }] },
      { name: 'WIP',                startRow: 22, endRow: 23, filters: [{ dbCol: DB_COL.STATUS, values: ['In Progress'] }] },
      { name: 'Internal Tasks',     startRow: 26, endRow: 27, filters: [{ dbCol: DB_COL.CATEGORY, values: ['Internal'] }] },
      { name: 'External Tasks',     startRow: 30, endRow: 31, filters: [{ dbCol: DB_COL.CATEGORY, values: ['External'] }] }
    ]
  }
};

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('⚡ KPI Tools')
    .addItem('🔍 Drill Down', 'drillDown')
    .addToUi();
}

function drillDown() {
  var ui = SpreadsheetApp.getUi();
  var sheet = SpreadsheetApp.getActiveSheet();
  var tabName = sheet.getName();
  var config = TAB_CONFIGS[tabName];

  if (!config) {
    ui.alert('This tab is not configured for drill-down.\nSupported tabs: ' + Object.keys(TAB_CONFIGS).join(', '));
    return;
  }

  var cell = sheet.getActiveCell();
  var row = cell.getRow();
  var col = cell.getColumn();

  // Must be in a data column (>= firstDataCol)
  if (col < config.firstDataCol) {
    ui.alert('Click on a data cell (week column) first, then use Drill Down.');
    return;
  }

  // Find which section this row belongs to
  var section = null;
  for (var i = 0; i < config.sections.length; i++) {
    var s = config.sections[i];
    if (row >= s.startRow && row <= s.endRow) {
      section = s;
      break;
    }
  }

  if (!section) {
    ui.alert('This row is not in a KPI data section.\nClick on a TSA/DE data row.');
    return;
  }

  // Get TSA/DE name from column D of same row
  var personName = sheet.getRange(row, config.nameCol).getValue();
  if (!personName) {
    ui.alert('Could not determine TSA/DE name from column D.');
    return;
  }

  // Get week range from row 3 of same column
  var weekRange = sheet.getRange(config.weekRow, col).getValue();
  if (!weekRange) {
    ui.alert('Could not determine week range from row 3.');
    return;
  }

  // Convert person name to DB format (uppercase, handle Gabrielle→GABI)
  var dbName = String(personName).toUpperCase();
  if (dbName === 'GABRIELLE') dbName = 'GABI';
  // Remove accents
  dbName = dbName.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  // Query DB
  var results = queryDB_(dbName, String(weekRange), section.filters);

  // Build and show sidebar
  var html = buildSidebarHtml_(personName, weekRange, section.name, results, cell.getValue());
  var htmlOutput = HtmlService.createHtmlOutput(html)
    .setTitle('🔍 ' + section.name)
    .setWidth(420);
  ui.showSidebar(htmlOutput);
}

function queryDB_(tsaName, weekRange, filters) {
  var dbSS = SpreadsheetApp.openById(DB_SPREADSHEET_ID);
  var dbSheet = dbSS.getSheetByName(DB_SHEET_NAME);
  if (!dbSheet || dbSheet.getLastRow() < 2) return [];

  var data = dbSheet.getDataRange().getValues();
  var results = [];

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    // Match TSA name
    if (String(row[DB_COL.TSA]).toUpperCase() !== tsaName) continue;
    // Match week range
    if (String(row[DB_COL.WEEK]) !== weekRange) continue;

    // Apply section filters
    var match = true;
    for (var f = 0; f < filters.length; f++) {
      var filter = filters[f];
      var cellVal = String(row[filter.dbCol]);
      if (filter.values.indexOf(cellVal) === -1) {
        match = false;
        break;
      }
    }
    if (!match) continue;

    results.push({
      focus: row[DB_COL.FOCUS],
      status: row[DB_COL.STATUS],
      demandType: row[DB_COL.DEMAND_TYPE],
      category: row[DB_COL.CATEGORY],
      customer: row[DB_COL.CUSTOMER],
      eta: formatDate_(row[DB_COL.ETA]),
      dd: formatDate_(row[DB_COL.DD]),
      perf: row[DB_COL.PERF]
    });
  }

  return results;
}

function formatDate_(val) {
  if (val instanceof Date && !isNaN(val.getTime())) {
    return (val.getMonth() + 1) + '/' + val.getDate() + '/' + val.getFullYear();
  }
  return val ? String(val) : '';
}

function buildSidebarHtml_(person, week, sectionName, results, cellValue) {
  var perfColors = {
    'On Time': '#b6d7a8',
    'Late': '#f4cccc',
    'Overdue': '#fce5cd',
    'On Track': '#c9daf8',
    'No ETA': '#e0e0e0',
    'No Delivery Date': '#e0e0e0',
    'N/A': '#f5f5f5'
  };

  var statusColors = {
    'Done': '#b6d7a8',
    'In Progress': '#c9daf8',
    'To Do': '#fff2cc'
  };

  var html = '';
  html += '<!DOCTYPE html><html><head>';
  html += '<style>';
  html += 'body { font-family: "Segoe UI", Arial, sans-serif; font-size: 13px; color: #333; margin: 0; padding: 16px; background: #fafafa; }';
  html += '.header { background: #2c3e50; color: white; padding: 14px 16px; margin: -16px -16px 16px -16px; }';
  html += '.header h2 { margin: 0 0 6px 0; font-size: 15px; font-weight: 600; }';
  html += '.header .meta { font-size: 12px; opacity: 0.85; }';
  html += '.header .value { font-size: 22px; font-weight: 700; margin-top: 8px; }';
  html += '.count { color: #7f8c8d; font-size: 12px; margin-bottom: 10px; }';
  html += 'table { width: 100%; border-collapse: collapse; margin-top: 4px; }';
  html += 'th { background: #ecf0f1; padding: 6px 8px; text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; color: #555; border-bottom: 2px solid #bdc3c7; }';
  html += 'td { padding: 6px 8px; border-bottom: 1px solid #e8e8e8; font-size: 12px; vertical-align: top; }';
  html += 'tr:hover { background: #f0f4f8; }';
  html += '.pill { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 500; }';
  html += '.focus { max-width: 180px; word-wrap: break-word; }';
  html += '.empty { text-align: center; padding: 30px; color: #999; }';
  html += '</style>';
  html += '</head><body>';

  // Header
  html += '<div class="header">';
  html += '<h2>' + escHtml_(sectionName) + '</h2>';
  html += '<div class="meta">' + escHtml_(person) + ' &bull; ' + escHtml_(week) + '</div>';
  var displayVal = (cellValue !== undefined && cellValue !== '') ? cellValue : '—';
  if (typeof displayVal === 'number') {
    displayVal = Math.round(displayVal * 10000) === displayVal * 10000 ? displayVal : (displayVal * 100).toFixed(0) + '%';
  }
  html += '<div class="value">' + escHtml_(String(displayVal)) + '</div>';
  html += '</div>';

  html += '<div class="count">' + results.length + ' task' + (results.length !== 1 ? 's' : '') + ' found</div>';

  if (results.length === 0) {
    html += '<div class="empty">No matching tasks in DB for this cell.</div>';
  } else {
    html += '<table>';
    html += '<tr><th>Task</th><th>Status</th><th>Customer</th><th>Perf</th></tr>';

    for (var i = 0; i < results.length; i++) {
      var r = results[i];
      var statusBg = statusColors[r.status] || '#f5f5f5';
      var perfBg = perfColors[r.perf] || '#f5f5f5';

      html += '<tr>';
      html += '<td class="focus">' + escHtml_(r.focus) + '</td>';
      html += '<td><span class="pill" style="background:' + statusBg + '">' + escHtml_(r.status) + '</span></td>';
      html += '<td>' + escHtml_(r.customer) + '</td>';
      html += '<td><span class="pill" style="background:' + perfBg + '">' + escHtml_(r.perf) + '</span></td>';
      html += '</tr>';
    }

    html += '</table>';

    // Detail section (collapsible)
    html += '<br><details><summary style="cursor:pointer;color:#2980b9;font-size:12px;">Show full details</summary>';
    html += '<table style="margin-top:8px">';
    html += '<tr><th>Task</th><th>Type</th><th>ETA</th><th>Delivery</th></tr>';
    for (var j = 0; j < results.length; j++) {
      var r2 = results[j];
      html += '<tr>';
      html += '<td class="focus">' + escHtml_(r2.focus) + '</td>';
      html += '<td>' + escHtml_(r2.demandType) + '</td>';
      html += '<td>' + escHtml_(r2.eta) + '</td>';
      html += '<td>' + escHtml_(r2.dd) + '</td>';
      html += '</tr>';
    }
    html += '</table></details>';
  }

  html += '</body></html>';
  return html;
}

function escHtml_(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
