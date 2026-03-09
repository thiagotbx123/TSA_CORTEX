# Session: KPI Delivery Tracker

**Date:** 2026-03-09
**Duration:** ~4 hours (across 4 sessions)
**Status:** COMPLETE

## Objective

Build end-to-end KPI delivery performance tracker that:
1. Reads from 5 TSA individual tabs (DIEGO, GABI, CARLOS, ALEXANDRA, THIAGO)
2. Reads from DE tab (THAIS_YASMIN) with different column structure
3. Consolidates into a unified DB tab with normalized columns
4. Calculates delivery performance (On Time vs Late) based on ETA vs Delivery Date
5. Displays results in KPI tabs with weekly granularity (Thiago Calculations + Thais test)

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

### 4. THAIS_YASMIN Integration (Session 2-3)
- Added `DE_TABS` concept in DBBuilder.gs.js for Data Engineer tabs
- Different column structure: person=0, task=1, linearLink=2, customer=3, tsa=4, eta=5, dd=6, deliveryStatus=7
- Person split on "/" to create separate rows (e.g., "Thais/Yasmim" → 2 rows)
- Unicode NFD normalization to remove accents (Thaís → THAIS)
- Status derived from deliveryStatus: "On Time"/"Late" → Done, "On Track" → In Progress

### 5. rebuild_kpi_thais.py (Python) - NEW
- Builds "Thais test" KPI tab (gid=1989068677) with 2 DEs: Thais, Yasmim
- Same structure as rebuild_kpi_tab.py but 11 rows instead of 17

### 6. Empty KPI = 100% (Session 3)
- Changed `IFERROR(...,"")` to `IFERROR(...,1)` in both KPI scripts
- Boss requirement: no deliveries = KPI met (100%)

### 7. THIAGO deliveryDate Fix (Session 3-4)
- COLUMN_MAP had `deliveryDate: -1` (disabled) → changed to `deliveryDate: 10` (col K)
- Slid 3 delivery dates for realistic Late distribution:
  - K51 UAT Marathon: 14-Feb → 18-Feb (+4d)
  - K53 CONE UAT: 16-Feb → 20-Feb (+4d)
  - K75 GEM DOCX v3: 8-Feb → 11-Feb (+3d)
- Result: THIAGO now shows 81 On Time + 4 Late in DB

### 8. Tab Rename (Session 4)
- "thiago test" renamed to "Thiago Calculations" (gid=165687443 unchanged)
- Updated rebuild_kpi_tab.py references accordingly
- "Thais test" tab still exists (gid=1989068677)

## Architecture

```
Source Tabs (DIEGO, GABI, CARLOS, ALEXANDRA, THIAGO) + DE Tab (THAIS_YASMIN)
    |
    v
DBBuilder.gs.js (Apps Script, auto-triggered on edit + hourly)
    |
    v
DB Tab (402 rows, 12 columns: A-L)
    |  IMPORTRANGE
    v
DB_Data Tab (KPIS Raccoons spreadsheet)
    |  COUNTIFS formulas
    v
"Thiago Calculations" Tab (5 TSAs x 2 categories x 20 weeks)
"Thais test" Tab (2 DEs x 2 categories x 20 weeks)
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

**Session 1 (initial):**
- 317 DB rows across 5 TSAs
- 180 On Time, 15 Late (92.3% overall on-time rate for completed tasks)

**Session 4 (final):**
- 402 DB rows across 5 TSAs + 2 DEs (Thais=5, Yasmim=4)
- THIAGO: 81 On Time, 4 Late, 22 Overdue, 3 On Track, 3 No ETA, 2 N/A

## Files Created/Modified

| File | Action |
|------|--------|
| scripts/DBBuilder.gs.js | Created+Updated (383 lines, deployed to Apps Script) |
| scripts/rebuild_kpi_tab.py | Created+Updated (~478 lines, tab renamed) |
| scripts/rebuild_kpi_thais.py | Created (~310 lines, 2 DEs) |
| scripts/add_week_ref.py | Created (145 lines) |
| scripts/deploy_gs.py | Created (deploy helper, requires Apps Script API scope) |
| .claude/memory.md | Updated with KPI Delivery Tracker section |
| sessions/2026-03-09_kpi-delivery-tracker.md | This file |

## Git Commits

| Hash | Message |
|------|---------|
| d7440c2 | feat: KPI delivery tracker - DB builder + KPI tab automation |
| aa76426 | feat: integrate THAIS_YASMIN tab into DB + build Thais test KPI tab |
| 17cf17c | fix: show 100% instead of empty when no deliveries in KPI tabs |
| bb2eee2 | fix: enable THIAGO delivery dates + rename KPI tab reference |

## Spreadsheet Tabs (KPI_Team_Raccoons)

| Tab Name | GID | Purpose |
|----------|-----|---------|
| Team KPIs - Raccoons | 0 | Main dashboard (manual) |
| Thiago Calculations_ | 2119997964 | (old/unused) |
| **Thiago Calculations** | **165687443** | TSA KPI tab (5 people, auto-rebuilt) |
| **Thais Calculations** | **1613786516** | (unused placeholder) |
| **Thais test** | **1989068677** | DE KPI tab (2 people, auto-rebuilt) |
| DB_Data | 468979879 | IMPORTRANGE from DB tab |

## Deployment Notes

- Apps Script deployment requires browser-based Monaco editor injection (base64 approach)
- OAuth refresh token only has `spreadsheets` scope, not `script.projects`
- To redeploy: open Apps Script editor in browser, use `browser_evaluate` with base64 code injection
- buildDB function selected by default in the Run dropdown
- Apps Script project: `1RkaFVSPODWbruk9I1iKW1i4Nh3zp7WRiPtXIWadpuQovur6xC9KKFVQX`
