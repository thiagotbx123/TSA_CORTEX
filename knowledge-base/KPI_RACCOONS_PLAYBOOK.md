# KPI Team Raccoons — Calculation Playbook

> Complete reference for all KPI indicators: formula logic, data sources, thresholds, interpretation, and known limitations.

---

## Data Pipeline

```
Source Sheet (individual tabs)     →    DB tab (consolidated)    →    KPI Sheet (DB_Data via IMPORTRANGE)
├── DIEGO                                404 rows                      ├── Thiago Calculations (TSA team: 5 people)
├── GABI                                                               ├── Thais Calculations (DE team: 2 people)
├── CARLOS                                                             ├── Team KPIs - Raccoons (summary)
├── ALEXANDRA                                                          └── DB_Data (mirror of DB via IMPORTRANGE)
├── THIAGO
└── THAIS_YASMIN
```

**Source Sheet**: `1XaJgJCExt_dQ-RBY0eINP-0UCnCH7hYjGC3ibPlluzw`
**KPI Sheet**: `1SPyvjXW9OJ4_CywHqroRwKbSbdGI98O0xxkc4y1Sy9w`

### DB_Data Columns

| Col | Field              | Example                    | Used By          |
|-----|--------------------|----------------------------|------------------|
| A   | TSA (name)         | CARLOS                     | All formulas     |
| B   | Week Range         | 01/12 - 01/16/2026         | All formulas     |
| C   | Current Focus      | SOW improvement             | —                |
| D   | Status             | Done / In Progress / To do  | S3, S5, S8       |
| E   | Demand Type        | External(Customer) / Routine | S6, S7           |
| F   | Demand Category    | Internal / External         | S1, S2           |
| G   | Customer           | QBO / Gong / Brevo          | —                |
| H   | Date Add           | 2026-01-07                  | S8               |
| I   | ETA                | 2026-01-22                  | —                |
| J   | Delivery Date      | 2026-01-22                  | S8               |
| K   | Delivery Performance| On Time / Late / Overdue   | S1, S2, S4, S9, S10 |
| L   | Week Ref           | 26-01 W.1                   | —                |

### Name Mapping

- TSA sheet (Thiago Calculations): `IF(name="Gabrielle","GABI",UPPER(name))`
- DE sheet (Thais Calculations): `UPPER(name)` — no mapping needed

---

## Grid Layout

**Row 1**: Month group headers (DECEMBER '25, JANUARY, FEBRUARY...)
**Row 2**: Week labels (W1, W2, W3, W4, W5)
**Row 3**: Full date ranges (12/01 - 12/05/2025, ...)
**Columns**: A-C reserved, D = person name / target, E-BI = 57 week columns

### Thiago Calculations (TSA: Alexandra, Carlos, Diego, Gabrielle, Thiago)

| Section | Header Row | Data Rows | Team Avg | OBS Row |
|---------|-----------|-----------|----------|---------|
| S1 Internal Accuracy      | 5  | 6-10  | —  | —  |
| S2 External Accuracy      | 12 | 13-17 | —  | —  |
| S3 Throughput              | 19 | 20-24 | —  | —  |
| S4 Overdue Snapshot        | 26 | 27-31 | —  | —  |
| S5 WIP                    | 33 | 34-38 | —  | —  |
| S6 Internal Tasks Count   | 40 | 41-45 | —  | —  |
| S7 External Tasks Count   | 47 | 48-52 | —  | —  |
| S8 Avg Execution Time     | 54 | 55-59 | 60 | —  |
| S9 Timeline Combined      | 61 | 62-66 | 67 | —  |
| S10 ETA Compliance        | 68 | 69-73 | 74 | 75 |

### Thais Calculations (DE: Thais, Yasmim)

| Section | Header Row | Data Rows | Team Avg | OBS Row |
|---------|-----------|-----------|----------|---------|
| S1 Internal Accuracy      | 5  | 6-7   | —  | —  |
| S2 External Accuracy      | 9  | 10-11 | —  | —  |
| S3 Throughput              | 13 | 14-15 | —  | —  |
| S4 Overdue Snapshot        | 17 | 18-19 | —  | —  |
| S5 WIP                    | 21 | 22-23 | —  | —  |
| S6 Internal Tasks Count   | 25 | 26-27 | —  | —  |
| S7 External Tasks Count   | 29 | 30-31 | —  | —  |
| S8 Avg Execution Time     | 33 | 34-35 | 36 | —  |
| S9 Timeline Combined      | 37 | 38-39 | 40 | —  |
| S10 ETA Compliance        | 41 | 42-43 | 44 | 45 |

---

## Section 1: Internal Task Accuracy

**Question**: Are internal deadlines being met?
**Target**: >90%

### Formula

```
= IFERROR(
    COUNTIFS(Name, Week, Category="Internal", Performance="On Time")
    /
    (COUNTIFS(Name, Week, Category="Internal", Performance="On Time")
     + COUNTIFS(Name, Week, Category="Internal", Performance="Late"))
  , 1)
```

### Actual Google Sheets Formula (example: Carlos, col E)

```
=IFERROR(
  COUNTIFS(DB_Data!$A:$A, IF($D7="Gabrielle","GABI",UPPER($D7)),
           DB_Data!$B:$B, E$3,
           DB_Data!$F:$F, "Internal",
           DB_Data!$K:$K, "On Time")
  /
  (COUNTIFS(DB_Data!$A:$A, IF($D7="Gabrielle","GABI",UPPER($D7)),
            DB_Data!$B:$B, E$3,
            DB_Data!$F:$F, "Internal",
            DB_Data!$K:$K, "On Time")
   + COUNTIFS(DB_Data!$A:$A, IF($D7="Gabrielle","GABI",UPPER($D7)),
              DB_Data!$B:$B, E$3,
              DB_Data!$F:$F, "Internal",
              DB_Data!$K:$K, "Late"))
, 1)
```

### Data Flow

```
DB_Data col A (TSA name)  ──┐
DB_Data col B (Week Range) ──┤──→ COUNTIFS ──→ On Time count
DB_Data col F (Category)   ──┤                 Late count
DB_Data col K (Performance)──┘                     │
                                          On Time / (On Time + Late)
                                                   │
                                              Percentage
```

### Key Details

- **Filter column**: F (Demand Category), NOT E (Demand Type)
- **Counted values**: Only "On Time" and "Late" from col K
- **Excluded**: Overdue, On Track, No ETA, N/A, No Delivery Date — these don't affect the result
- **IFERROR fallback**: Returns **1** (100%) when no data — ⚠ this means empty weeks show 100%, not "-"
- **Format**: Percentage (0%)

### Conditional Formatting

| Color  | RGB                | Condition        |
|--------|--------------------|------------------|
| Green  | (0.56, 0.77, 0.49) | >= 90%           |
| Yellow | (1.00, 0.85, 0.40) | Between 50-89.9% |
| Red    | (0.91, 0.49, 0.45) | < 50%            |

### Decision Guide

| Value    | Signal                                       | Action                              |
|----------|----------------------------------------------|-------------------------------------|
| 100%     | All internal on time (or no data — see ⚠)   | Check if real data exists           |
| 90-99%   | Healthy — meeting target                     | No action needed                    |
| 70-89%   | Below target — pattern forming               | Review which tasks are late         |
| <70%     | Systemic issue — person consistently late    | 1:1 coaching, scope/ETA review      |

### Known Limitation

⚠ **False 100%**: When a person has zero internal tasks in a week (0 On Time, 0 Late), the formula returns 100% instead of "-". This inflates the visual. Sections S8-S10 handle this correctly with "-".

---

## Section 2: External Task Accuracy

**Question**: Are customer-facing deadlines being met?
**Target**: >90%

### Formula

Identical to S1 but filters on `Category = "External"` instead of "Internal".

```
= IFERROR(
    COUNTIFS(Name, Week, Category="External", Performance="On Time")
    /
    (COUNTIFS(Name, Week, Category="External", Performance="On Time")
     + COUNTIFS(Name, Week, Category="External", Performance="Late"))
  , 1)
```

### Decision Guide

Same thresholds as S1. External accuracy is often more critical because it directly impacts customer trust and SLA commitments.

### Known Limitation

Same false 100% issue as S1.

---

## Section 3: Throughput (Deliveries/Week)

**Question**: How many tasks is each person completing per week?
**Target**: >=5 deliveries/week

### Formula

```
= COUNTIFS(Name, Week, Status="Done")
```

### Actual Formula

```
=COUNTIFS(
  DB_Data!$A:$A, IF($D21="Gabrielle","GABI",UPPER($D21)),
  DB_Data!$B:$B, E$3,
  DB_Data!$D:$D, "Done")
```

### Key Details

- **No IFERROR needed**: COUNTIFS returns 0, never errors
- **Counts ALL Done tasks**: No category filter (internal + external + routine)
- **Format**: Integer
- **Zero is valid**: Shows 0 when no tasks completed, not "-"

### Decision Guide

| Value | Signal                                      | Action                           |
|-------|---------------------------------------------|----------------------------------|
| >=5   | Healthy throughput                          | On track                         |
| 3-4   | Below target — may be acceptable            | Check task complexity             |
| 1-2   | Low output                                  | Investigate blockers              |
| 0     | No deliveries — blocked, PTO, or data gap   | Verify cause                     |

---

## Section 4: Overdue Snapshot

**Question**: How many tasks are past their ETA and still open?
**Target**: 0

### Formula

```
= COUNTIFS(Name, Week, Performance="Overdue")
```

### Actual Formula

```
=COUNTIFS(
  DB_Data!$A:$A, IF($D28="Gabrielle","GABI",UPPER($D28)),
  DB_Data!$B:$B, E$3,
  DB_Data!$K:$K, "Overdue")
```

### Key Details

- **"Overdue" = open and past ETA**: Only applies to non-Done tasks (In Progress, On Hold, To do)
- **When a task is completed**: It transitions from "Overdue" to "Late" or "On Time" — never "Done + Overdue"
- **This is a snapshot**: Reflects the state at the time data was recorded for that week
- **Format**: Integer

### Decision Guide

| Value | Signal                  | Action                                |
|-------|-------------------------|---------------------------------------|
| 0     | Clean — no overdue work | Ideal state                           |
| 1-2   | Manageable backlog      | Review ETA accuracy, prioritize       |
| 3+    | Risk accumulating       | Immediate triage — reassign or re-ETA |

---

## Section 5: WIP (Work in Progress)

**Question**: How many tasks are simultaneously open per person?
**Target**: <=3

### Formula

```
= COUNTIFS(Name, Week, Status="In Progress")
```

### Key Details

- **Measures concurrent workload**: Too many tasks = context switching, slower delivery
- **All task types included**: Internal, external, routine
- **Format**: Integer

### Decision Guide

| Value | Signal              | Action                              |
|-------|---------------------|-------------------------------------|
| 1-3   | Focused workload    | Healthy                             |
| 4-5   | Overloaded          | Consider deprioritizing or handing off |
| 6+    | Unsustainable       | Redistribute immediately            |

---

## Section 6: Internal Tasks Count

**Question**: How many internal tasks assigned per person per week?
**Target**: Monitoring only (no fixed goal)

### Formula

```
= COUNTIFS(Name, Week, Category="Internal")
```

### Key Details

- **Counts all statuses**: Done, In Progress, To do, On Hold, Canceled
- **Use case**: Balance internal vs external workload
- **Combined with S7**: Shows workload distribution ratio

---

## Section 7: External Tasks Count

**Question**: How many customer-facing tasks per person per week?
**Target**: Monitoring only (no fixed goal)

### Formula

```
= COUNTIFS(Name, Week, Category="External")
```

### Key Details

- Same as S6 but for external tasks
- **Use case**: If external count is consistently higher than internal, the person is customer-heavy
- **Compare S6 + S7 totals**: Should roughly match S3 (Throughput Done + non-Done tasks)

---

## Section 8: Avg Execution Time (days)

**Question**: How fast are tasks being completed on average?
**Target**: Trend indicator — lower is better

### Formula

```
= IFERROR(
    AVERAGE(FILTER(
      Delivery Date - Date Add,
      Name match,
      Week match,
      Status = "Done",
      Delivery Date is not empty,
      Date Add is not empty,
      Duration >= 0 days,
      Duration <= 60 days
    ))
  , "-")
```

### Actual Formula

```
=IFERROR(AVERAGE(FILTER(
  DB_Data!$J$2:$J$1000 - DB_Data!$H$2:$H$1000,
  DB_Data!$A$2:$A$1000 = IF($D56="Gabrielle","GABI",UPPER($D56)),
  DB_Data!$B$2:$B$1000 = E$3,
  DB_Data!$D$2:$D$1000 = "Done",
  DB_Data!$J$2:$J$1000 <> "",
  DB_Data!$H$2:$H$1000 <> "",
  IFERROR(DB_Data!$J$2:$J$1000 - DB_Data!$H$2:$H$1000, {-999}) >= 0,
  IFERROR(DB_Data!$J$2:$J$1000 - DB_Data!$H$2:$H$1000, {-999}) <= 60
)), "-")
```

### Data Flow

```
DB_Data col H (Date Add)     ──┐
DB_Data col J (Delivery Date) ──┤──→ FILTER (7 conditions) ──→ Array of durations
DB_Data col A (Name)          ──┤                                      │
DB_Data col B (Week)          ──┤                                   AVERAGE
DB_Data col D (Status="Done") ──┘                                      │
                                                                  Days (decimal)
```

### Key Details

- **Calculation**: Delivery Date minus Date Add = days to complete
- **FILTER, not SUMPRODUCT**: SUMPRODUCT fails with IMPORTRANGE date arrays (#VALUE! error)
- **Exclusions**:
  - Tasks without Date Add or Delivery Date
  - Negative durations (date entry errors where Delivery < Date Add)
  - Durations > 60 days (outliers from wrong year entries)
- **Format**: Decimal number (e.g., 3.5 = 3 and a half days)
- **"-" for no data**: Correct behavior — IFERROR catches FILTER with no matches
- **Team Avg row**: `=IFERROR(AVERAGE(E55:E59), "-")` — simple average of 5 people

### Decision Guide

| Value   | Signal                      | Action                              |
|---------|-----------------------------|-------------------------------------|
| 1-3     | Fast execution              | Healthy pace                        |
| 4-7     | Normal                      | Acceptable for complex tasks        |
| 8-15    | Slow                        | Check blockers, scope creep         |
| 15+     | Very slow — process issue   | Deep review needed                  |

---

## Section 9: Accuracy of Timeline Commitments (Combined)

**Question**: What percentage of all tasks (internal + external) are delivered on time?
**Target**: >90%

### Formula

```
= IFERROR(
    COUNTIFS(Name, Week, Performance="On Time")
    /
    (COUNTIFS(Name, Week, Performance="On Time")
     + COUNTIFS(Name, Week, Performance="Late"))
  , "-")
```

### Actual Formula

```
=IFERROR(
  COUNTIFS(DB_Data!$A:$A, IF($D63="Gabrielle","GABI",UPPER($D63)),
           DB_Data!$B:$B, E$3,
           DB_Data!$K:$K, "On Time")
  /
  (COUNTIFS(DB_Data!$A:$A, IF($D63="Gabrielle","GABI",UPPER($D63)),
            DB_Data!$B:$B, E$3,
            DB_Data!$K:$K, "On Time")
   + COUNTIFS(DB_Data!$A:$A, IF($D63="Gabrielle","GABI",UPPER($D63)),
              DB_Data!$B:$B, E$3,
              DB_Data!$K:$K, "Late"))
, "-")
```

### Key Details

- **Identical logic to S1/S2** but without the Internal/External filter
- **IFERROR returns "-"** (not 1) — correctly shows blank for no data
- **Only counts On Time and Late**: Overdue, On Track, No ETA, N/A excluded
- **Difference from S1/S2**: S1/S2 filter by Demand Category; S9 counts everything
- **Format**: Percentage (0%)
- **Team Avg row**: `=IFERROR(AVERAGE(E62:E66), "-")`

### Relationship to S1 and S2

S9 is the weighted combination of S1 and S2. If a person has 8 internal On Time, 2 internal Late, 5 external On Time, 0 external Late:
- S1 (Internal) = 8/(8+2) = 80%
- S2 (External) = 5/(5+0) = 100%
- S9 (Combined) = 13/(13+2) = 87%

### Conditional Formatting

Same green/yellow/red as S1-S2.

---

## Section 10: Effective Delivery Rate

**Question**: Of everything assigned, how much was delivered on time? (Strictest metric)
**Target**: >85%

### Formula

```
= IFERROR(
    COUNTIFS(Name, Week, Performance="On Time")
    /
    (COUNTIFS(Name, Week, Performance="On Time")
     + COUNTIFS(Name, Week, Performance="Late")
     + COUNTIFS(Name, Week, Performance="Overdue"))
  , "-")
```

### Actual Formula

```
=IFERROR(
  COUNTIFS(DB_Data!$A:$A, IF($D$70="Gabrielle","GABI",UPPER($D$70)),
           DB_Data!$B:$B, E$3,
           DB_Data!$K:$K, "On Time")
  /
  (COUNTIFS(DB_Data!$A:$A, IF($D$70="Gabrielle","GABI",UPPER($D$70)),
            DB_Data!$B:$B, E$3,
            DB_Data!$K:$K, "On Time")
   + COUNTIFS(DB_Data!$A:$A, IF($D$70="Gabrielle","GABI",UPPER($D$70)),
              DB_Data!$B:$B, E$3,
              DB_Data!$K:$K, "Late")
   + COUNTIFS(DB_Data!$A:$A, IF($D$70="Gabrielle","GABI",UPPER($D$70)),
              DB_Data!$B:$B, E$3,
              DB_Data!$K:$K, "Overdue"))
, "-")
```

### Data Flow

```
DB_Data col A (Name)           ──┐
DB_Data col B (Week Range)     ──┤──→ 3 x COUNTIFS ──→ On Time count
DB_Data col K (Delivery Perf)  ──┘                      Late count
                                                        Overdue count
                                                            │
                                              On Time / (On Time + Late + Overdue)
                                                            │
                                                       Percentage
```

### Key Details

- **Includes Overdue in denominator**: This is the key difference from S9. Overdue = tasks past ETA that are still open (In Progress, On Hold, To do). They count AGAINST the rate.
- **No status filter**: Does not filter by Status="Done". Counts On Time, Late (from Done tasks) AND Overdue (from open tasks) all together.
- **Stricter than S9**: Same numerator (On Time) but bigger denominator (adds Overdue).
- **Lower target (85%)**: Because denominator includes unfinished work, achieving >85% is harder.
- **"-" for no data**: When 0 On Time + 0 Late + 0 Overdue = 0/0, IFERROR returns "-".
- **0% is meaningful**: Shows weeks where the ONLY activity is overdue (no deliveries at all). S9 shows "-" for these weeks because it has no On Time or Late data — S10 surfaces the problem.
- **Format**: Percentage (0%)
- **Team Avg row**: `=IFERROR(AVERAGE(E69:E73), "-")`

### Difference from S9 (Timeline Combined)

| Aspect          | S9 Timeline Combined               | S10 Effective Delivery Rate           |
|-----------------|-------------------------------------|---------------------------------------|
| Numerator       | On Time                             | On Time                               |
| Denominator     | On Time + Late                      | On Time + Late + **Overdue**          |
| Scope           | Only completed work                 | All work with a performance label     |
| Overdue impact  | Invisible — excluded                | Penalized — lowers the rate           |
| Empty weeks     | "-" (no deliveries)                 | **0%** if only Overdue exists         |
| Target          | >90%                                | >85%                                  |

### Real-World Example

Carlos, week 01/05 - 01/09/2026:
- On Time: 8 tasks delivered on schedule
- Late: 0 tasks delivered late
- Overdue: 7 open tasks past their ETA

| Metric     | Calculation        | Result |
|------------|--------------------|--------|
| S9 Timeline| 8 / (8 + 0) =     | **100%** ✓ "all deliveries were on time" |
| S10 Effective| 8 / (8 + 0 + 7) = | **53%** ✗ "only half the workload is under control" |

The manager sees two completely different stories:
- S9 says "Carlos delivered everything on time" (true, but incomplete)
- S10 says "Carlos has 7 overdue tasks dragging his rate down" (the full picture)

### Conditional Formatting

Same green/yellow/red as S1/S2/S9.

### Decision Guide

| Value    | Signal                                          | Action                              |
|----------|-------------------------------------------------|-------------------------------------|
| >85%     | Healthy — most work on time, few overdue        | On track                            |
| 70-84%   | Overdue backlog building up                     | Review overdue tasks, re-ETA or close |
| 50-69%   | Significant workload stuck or late              | Immediate triage — reassign or descope |
| <50%     | More overdue than on-time deliveries            | Escalate — systemic capacity issue  |
| 0%       | No deliveries, only overdue tasks that week     | Check if person is blocked or on PTO |

---

## Team Average Rows

Present in sections S8, S9, S10 only.

### Formula

```
= IFERROR(AVERAGE(range of 5 person cells above), "-")
```

- **S8 Avg Exec**: `=IFERROR(AVERAGE(E55:E59), "-")` — average days across team
- **S9 Timeline**: `=IFERROR(AVERAGE(E62:E66), "-")` — average on-time rate
- **S10 Effective Rate**: `=IFERROR(AVERAGE(E69:E73), "-")` — average effective delivery rate

### Note

"-" values are ignored by AVERAGE. If 3 of 5 people have data, the average is of those 3.

---

## Conditional Formatting Rules

21 rules per sheet. Applied to data cells (cols E-BI) in sections S1, S2, S9, S10.

### Percentage Sections (S1, S2, S9, S10)

| Priority | Condition      | Color  | RGB                |
|----------|----------------|--------|--------------------|
| 1        | >= 0.9 (90%)   | Green  | (0.56, 0.77, 0.49) |
| 2        | 0.5 to 0.8999  | Yellow | (1.00, 0.85, 0.40) |
| 3        | < 0.5 (50%)    | Red    | (0.91, 0.49, 0.45) |

### Sections S3-S7 (count-based)

Conditional formatting uses warning notes (⚠) on individual cells rather than color rules.

---

## Known Limitations & Edge Cases

### 1. False 100% in S1 and S2

Sections 1 and 2 use `IFERROR(..., 1)` — when no data exists (0 On Time, 0 Late), they show 100% instead of "-". This inflates results for weeks where a person had no tasks of that type. Sections S8-S10 correctly show "-".

### 2. 345-Row DB Consolidation Gap

Source tabs contain 749 total rows but DB consolidation only has 404. DB is maintained manually. Some historical data may not be reflected in KPIs.

### 3. Non-Standard Status Values

7 records use "B.B.C" or "B.B.C." instead of standard statuses. These are excluded from all COUNTIFS that filter by "Done", "In Progress", etc.

### 4. Overdue Never Transitions to Done+Overdue

When a task moves from Overdue to Done, the Delivery Performance changes to "On Time" or "Late". There is no "Done + Overdue" state. This means:
- S4 (Overdue) only shows currently-open overdue tasks
- S9 (Timeline) excludes overdue from its denominator — only sees finished work
- S10 (Effective Rate) includes Overdue in denominator — captures the full workload picture

### 5. Gabrielle → GABI Mapping

DB_Data stores names in UPPERCASE. "Gabrielle" in the name column maps to "GABI" in the data. All formulas in Thiago Calculations handle this. Thais Calculations does not need this mapping.

---

## Quick Reference Card

| # | Indicator                | Formula Summary                          | Target  | Format | Empty = |
|---|--------------------------|------------------------------------------|---------|--------|---------|
| 1 | Internal Accuracy        | OnTime / (OnTime + Late) [Internal]      | >90%    | 0%     | 100% ⚠ |
| 2 | External Accuracy        | OnTime / (OnTime + Late) [External]      | >90%    | 0%     | 100% ⚠ |
| 3 | Throughput               | COUNT(Done)                              | >=5     | #      | 0       |
| 4 | Overdue                  | COUNT(Overdue)                           | 0       | #      | 0       |
| 5 | WIP                      | COUNT(In Progress)                       | <=3     | #      | 0       |
| 6 | Internal Count           | COUNT(Internal)                          | —       | #      | 0       |
| 7 | External Count           | COUNT(External)                          | —       | #      | 0       |
| 8 | Avg Exec Time            | AVG(Delivery - DateAdd) [Done, 0-60d]    | ↓ lower | 0.0    | -       |
| 9 | Timeline Combined        | OnTime / (OnTime + Late) [All]           | >90%    | 0%     | -       |
| 10| Effective Delivery Rate   | OnTime / (OnTime + Late + Overdue)       | >85%    | 0%     | -       |

---

## How S9 and S10 Work Together — Executive Summary

These two indicators answer **different questions** about the same team:

```
S9: "Of the work we finished, how much was on time?"
    → Measures delivery quality
    → High S9 = good execution on completed work

S10: "Of ALL the work on our plate, how much was delivered on time?"
     → Measures workload health
     → High S10 = team is on top of everything, low backlog
```

**When S9 is high but S10 is low**: The team delivers quality work BUT has a growing backlog of overdue tasks. The finished work is good, but too much is stuck.

**When both are high**: Team is healthy — delivering on time AND not accumulating overdue.

**When both are low**: Systemic problem — late deliveries AND overdue backlog.

```
Real example — Carlos, week 01/05:

  S9 = 100%  →  "Everything he delivered was on time"  ✓
  S10 = 53%  →  "But 7 overdue tasks are stuck"        ✗

  Action: Don't celebrate the 100% — triage the 7 overdue tasks first.
```

---

*Generated 2026-03-12 — KPI Team Raccoons Calculation Playbook v2.0*
