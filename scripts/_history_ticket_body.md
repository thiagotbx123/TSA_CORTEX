# TSA Historical Data — Alexandra Lacerda

> **Purpose:** This ticket preserves the original dates and KPI-critical fields from the TSA Tasks Consolidate spreadsheet (Jan-Mar 2026). Linear migration happened on 2026-03-17, so `createdAt` and `completedAt` on migrated issues reflect the migration date, NOT original dates. Use THIS ticket as the authoritative source for historical KPI calculations.

---

## KPI Snapshot (Jan 7 — Mar 17, 2026)

| Metric | Value |
|--------|-------|
| Total tasks | 61 |
| Done | 51 |
| In Progress | 6 |
| Canceled | 2 |
| Paused (BBC) | 2 |
| Tasks with ETA+Delivery | 43 |
| **On-time rate** | **95.3%** (41/43) |
| Late deliveries | 2 |
| Avg absolute delta | 0.1 days |
| **Within 1 week (Waki target >90%)** | **100.0%** (43/43) |
| Avg duration (Date Add → Delivery) | 4.6 days |
| Median duration | 4 days |
| Max duration | 21 days |

### Waki KPI Assessment

1. **ETA Accuracy (<1 week, >90%):** 100.0% of delivered tasks within 1 week of ETA
2. **Faster Implementations (4-week target):** Avg 4.6 days, median 4 days
3. **Implementation Reliability (90%):** 95.3% on-time delivery rate

---

## Customer Breakdown

- **QBO**: 51 tasks (44 done)
- **WFS**: 9 tasks (6 done)
- **HockeyStack**: 1 tasks (1 done)

## Demand Type Breakdown

- **External(Customer)**: 56
- **Routine**: 2
- **Data Gen.**: 1
- **Improvement**: 1
- **Maintenance**: 1

---

## Full Historical Record

| # | Linear | Customer | Focus | Status | Date Add | ETA | Delivery | Delta |
|---|--------|----------|-------|--------|----------|-----|----------|-------|
| 1 | RAC-275 | WFS | SOW improvement | Done | 2026-01-07 | 2026-01-22 | 2026-01-22 | 0 |
| 2 | RAC-290 | WFS | Environment decision (Pro/Cons) | Done | 2026-01-12 | 2026-01-16 | 2026-01-16 | 0 |
| 3 | RAC-294 | HockeyStack | Handover to Thiago | Done | 2026-01-12 | 2026-01-16 | 2026-01-16 | 0 |
| 4 | RAC-288 | QBO | Onboarding & handover | Done | 2026-01-07 | 2026-01-08 | 2026-01-08 | 0 |
| 5 | RAC-289 | QBO | Onboarding & handover (hypercare) | In Progress | 2026-07-01 | 2026-03-31 | - |  |
| 6 | RAC-286 | QBO | Documentation review | Done | 2026-01-12 | 2026-01-16 | 2026-01-16 | 0 |
| 7 | RAC-287 | QBO | Documentation review (features) | Done | 2026-01-12 | 2026-01-19 | 2026-01-19 | 0 |
| 8 | RAC-291 | WFS | Environment decision (first draft) | Done | 2026-01-07 | 2026-01-09 | 2026-01-09 | 0 |
| 9 | RAC-280 | QBO | Features review (TCO) | Done | 2026-01-12 | 2026-02-02 | 2026-02-02 | 0 |
| 10 | RAC-281 | QBO | Features review (Construction Sales | Canceled | 2026-01-12 | 2026-02-09 | - |  |
| 11 | RAC-282 | QBO | Features review (Construction Event | Canceled | 2026-01-12 | 2026-02-16 | - |  |
| 12 | RAC-276 | WFS | SOW draft | Done | 2026-01-19 | 2026-01-22 | 2026-01-22 | 0 |
| 13 | RAC-283 | QBO | Doc prep (features list for Intuit) | Done | 2026-01-19 | 2026-01-21 | 2026-01-21 | 0 |
| 14 | RAC-284 | QBO | Doc prep (IES rerun validation) | Done | 2026-01-28 | 2026-01-28 | 2026-01-28 | 0 |
| 15 | RAC-297 | QBO | Support on UAT Environment | Done | 2026-01-27 | 2026-01-27 | 2026-01-27 | 0 |
| 16 | RAC-269 | QBO | Ticket analysis PLA-3201 | Done | 2026-01-22 | 2026-01-22 | 2026-01-22 | 0 |
| 17 | RAC-270 | QBO | Ticket analysis PLA-3202 | Done | 2026-01-23 | 2026-01-23 | 2026-01-23 | 0 |
| 18 | RAC-271 | QBO | Ticket analysis PLA-3224 | Done | 2026-01-26 | 2026-01-26 | 2026-01-26 | 0 |
| 19 | RAC-272 | QBO | Ticket analysis PLA-3227 | Done | 2026-01-27 | 2026-01-28 | 2026-01-28 | 0 |
| 20 | RAC-295 | QBO | Intuit Winter Release docs review | Done | 2026-01-28 | 2026-01-30 | 2026-01-30 | 0 |
| 21 | RAC-277 | WFS | SOW improvement (scope lock) | Paused | 2026-01-28 | TBD | - |  |
| 22 | RAC-278 | WFS | SOW milestones draft | Paused | 2026-02-04 | TBD | - |  |
| 23 | RAC-285 | QBO | Doc prep (FY26 tracker update) | Done | 2026-02-04 | 2026-02-13 | 2026-02-13 | 0 |
| 24 | RAC-264 | QBO | Env prep (UAT delivery) | Done | 2026-02-02 | 2026-02-10 | 2026-02-10 | 0 |
| 25 | RAC-265 | QBO | Env prep (TestBook) | Done | 2026-02-02 | 2026-02-04 | 2026-02-04 | 0 |
| 26 | RAC-266 | QBO | Env prep (TestBook run + evidence) | Done | 2026-02-02 | 2026-02-05 | 2026-02-05 | 0 |
| 27 | RAC-273 | QBO | Ticket analysis KLA-2399 | Done | 2026-01-27 | 2026-01-28 | 2026-01-28 | 0 |
| 28 | RAC-279 | WFS | SOW improvement (internal review) | Done | 2026-01-30 | 2026-02-03 | 2026-02-03 | 0 |
| 29 | RAC-267 | QBO | Env prep (data ingestion UAT/Sales) | Done | 2026-02-05 | 2026-02-10 | 2026-02-10 | 0 |
| 30 | RAC-268 | QBO | Env prep (TestBook rerun UAT) | Done | 2026-02-10 | 2026-02-12 | 2026-02-12 | 0 |
| 31 | RAC-238 | QBO | WR: Review ingestion tickets | Done | 2026-02-10 | 2026-02-12 | 2026-02-12 | 0 |
| 32 | RAC-239 | QBO | WR: Action plan | Done | 2026-02-10 | 2026-02-11 | 2026-02-11 | 0 |
| 33 | RAC-240 | QBO | WR: IES Construction validation | Done | 2026-02-12 | 2026-02-19 | 2026-02-19 | 0 |
| 34 | RAC-241 | QBO | WR: Evidence Construction UAT | Done | 2026-02-12 | 2026-02-19 | 2026-02-19 | 0 |
| 35 | RAC-242 | QBO | WR: Evidence Construction Events | Done | 2026-02-12 | 2026-02-19 | 2026-02-19 | 0 |
| 36 | RAC-243 | QBO | WR: Evidence Construction Sales | Done | 2026-02-12 | 2026-02-19 | 2026-02-19 | 0 |
| 37 | RAC-244 | QBO | WR: Validate IES + daily updates | Done | 2026-02-10 | 2026-02-23 | 2026-02-23 | 0 |
| 38 | RAC-245 | QBO | WR: Answer Intuit tracker comments | Done | 2026-02-17 | 2026-02-19 | 2026-02-19 | 0 |
| 39 | RAC-246 | QBO | WR: Answer Intuit Slack comments | Done | 2026-02-17 | 2026-02-19 | 2026-02-23 | 4 |
| 40 | RAC-247 | QBO | WR: Close gaps all environments | Done | 2026-02-17 | 2026-02-23 | 2026-02-24 | 1 |
| 41 | RAC-248 | QBO | WR: Backlog tickets review | In Progress | 2026-03-09 | 2026-03-31 | - |  |
| 42 | RAC-249 | QBO | WR: Evidence TCO | Done | 2026-03-02 | 2026-03-09 | 2026-03-09 | 0 |
| 43 | RAC-250 | QBO | WR: Evidence Professional Services | Done | 2026-03-02 | 2026-03-09 | 2026-03-09 | 0 |
| 44 | RAC-251 | QBO | WR: Evidence QBOA | Done | 2026-03-02 | 2026-03-13 | - |  |
| 45 | RAC-252 | QBO | WR: Evidence Events | Done | 2026-03-02 | 2026-03-09 | 2026-03-09 | 0 |
| 46 | RAC-253 | QBO | WR: Evidence Non Profit | Done | 2026-03-02 | 2026-03-13 | - |  |
| 47 | RAC-254 | QBO | WR: Validate TCO | Done | 2026-03-02 | 2026-03-09 | 2026-03-09 | 0 |
| 48 | RAC-255 | QBO | WR: Validate Prof. Services | Done | 2026-03-02 | 2026-03-13 | - |  |
| 49 | RAC-256 | QBO | WR: Validate QBOA | Done | 2026-03-02 | 2026-03-13 | - |  |
| 50 | RAC-257 | QBO | WR: Validate Events | Done | 2026-03-02 | 2026-03-09 | 2026-03-09 | 0 |
| 51 | RAC-258 | QBO | WR: Evidence Manufacturing | Done | 2026-03-02 | 2026-03-13 | - |  |
| 52 | RAC-259 | QBO | WR: Validate Manufacturing | Done | 2026-03-02 | 2026-03-13 | - |  |
| 53 | RAC-260 | QBO | WR: Validate Non Profit | Done | 2026-03-02 | 2026-03-09 | - |  |
| 54 | RAC-296 | QBO | Playbook Preparation | In Progress | 2026-03-04 | 2026-03-20 | - |  |
| 55 | RAC-292 | WFS | Pre scoping (questions) | Done | 2026-03-03 | 2026-03-04 | 2026-03-04 | 0 |
| 56 | RAC-261 | QBO | WR: Action plan remaining envs | Done | 2026-03-03 | 2026-03-04 | 2026-03-04 | 0 |
| 57 | RAC-274 | QBO | Ticket analysis PLA-3308 | Done | 2026-02-25 | 2026-02-26 | 2026-02-26 | 0 |
| 58 | RAC-262 | QBO | WR: End-to-end support | Done | 2026-02-01 | 2026-03-11 | - |  |
| 59 | RAC-298 | QBO | Environment improvements & risk red | In Progress | 2026-03-11 | TBD | - |  |
| 60 | RAC-263 | QBO | WR: Lessons learned | In Progress | 2026-03-11 | 2026-03-27 | - |  |
| 61 | RAC-293 | WFS | Pre scoping (next steps) | In Progress | 2026-03-11 | 2026-03-17 | - |  |

---

*Generated by TSA_CORTEX migration script on 2026-03-17. Source: TSA_Tasks_Consolidate spreadsheet, ALEXANDRA tab.*