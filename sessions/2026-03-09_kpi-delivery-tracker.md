# Session: KPI Delivery Tracker

**Date:** 2026-03-09
**Duration:** ~2 hours (across 2 sessions)
**Status:** COMPLETE

## Objective

Build end-to-end KPI delivery performance tracker that:
1. Reads from 5 TSA individual tabs (DIEGO, GABI, CARLOS, ALEXANDRA, THIAGO)
2. Consolidates into a unified DB tab with normalized columns
3. Calculates delivery performance (On Time vs Late) based on ETA vs Delivery Date
4. Displays results in a KPI tab with weekly granularity

## Key Changes

### 1. DBBuilder.gs.js (Apps Script)
- **parseDates_()**: New shared helper that extracts all dates from multi-line cells
- **parseMinDate_()**: Returns earliest date (used for ETA and Date Add)
- **parseMaxDate_()**: Returns latest date (used for Delivery Date)
- **Timezone fix**: All dates created at noon (12:00) instead of midnight to prevent 1-day offset
- **weekRef_()**: Generates sortable week references (e.g., "26-01 W.1")
- **calcPerf_()**: Delivery Performance logic (On Time, Late, Overdue, On Track, N/A)

### 2. rebuild_kpi_tab.py (Python)
- Extended week range to include December 2025 through April 2026 (20 weeks)
- Year-aware week labels: "25-12 W.1" for Dec 2025, "26-01 W.1" for Jan 2026
- Month headers with year suffix for non-2026: "DECEMBER '25"
- COUNTIFS formula: `On Time / (On Time + Late)` per TSA per category per week
- Conditional formatting: green (>80%), yellow (60-80%), red (<60%)

### 3. add_week_ref.py (Python)
- One-time script to add Week Ref column (L) to existing DB tab
- Updates filter range and IMPORTRANGE formula

## Architecture

```
Source Tabs (DIEGO, GABI, CARLOS, ALEXANDRA, THIAGO)
    |
    v
DBBuilder.gs.js (Apps Script, auto-triggered on edit + hourly)
    |
    v
DB Tab (317 rows, 12 columns: A-L)
    |  IMPORTRANGE
    v
DB_Data Tab (KPIS Raccoons spreadsheet)
    |  COUNTIFS formulas
    v
"thiago test" Tab (KPI dashboard, 5 TSAs x 2 categories x 20 weeks)
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| ETA = MIN date | When ETAs are postponed (multiple dates), use original commitment date |
| Delivery Date = MAX date | Use the latest date as actual delivery date |
| Dates at noon | Prevents timezone boundary issues (midnight dates shift 1 day) |
| On Time/(On Time+Late) | Excludes in-progress tasks from KPI calculation |
| Dec 2025 start | Some tasks started in December, needed to track their delivery |
| Monaco injection | OAuth token lacks Apps Script API scope; use browser-based deployment |

## Audit Results

- **317 DB rows** across 5 TSAs
- **180 On Time, 15 Late** (92.3% overall on-time rate for completed tasks)
- Cross-validated all KPI cells against source data:
  - Diego External W2: 4/5=80% CORRECT
  - Diego External W3: 4/10=40% CORRECT
  - Carlos Internal W4: 0/2=0% CORRECT
  - Gabi External W7: 2/3=67% CORRECT

## Files Created/Modified

| File | Action |
|------|--------|
| scripts/DBBuilder.gs.js | Created (327 lines, deployed to Apps Script) |
| scripts/rebuild_kpi_tab.py | Created (~200 lines) |
| scripts/add_week_ref.py | Created (145 lines) |
| scripts/deploy_gs.py | Created (deploy helper, requires Apps Script API scope) |
| .claude/memory.md | Updated with KPI Delivery Tracker section |
| sessions/2026-03-09_kpi-delivery-tracker.md | This file |

## Deployment Notes

- Apps Script deployment requires browser-based Monaco editor injection (base64 approach)
- OAuth refresh token only has `spreadsheets` scope, not `script.projects`
- To redeploy: open Apps Script editor in browser, use `browser_evaluate` with base64 code injection
- buildDB function selected by default in the Run dropdown
