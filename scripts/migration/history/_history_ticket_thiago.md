# TSA Historical Data — Thiago Brito

> **Purpose:** This ticket preserves the original dates and KPI-critical fields from the TSA Tasks Consolidate spreadsheet (Dec 2025 - Mar 2026). Linear migration happened on 2026-03-18, so `createdAt` and `completedAt` on migrated issues reflect the migration date, NOT original dates. Use THIS ticket as the authoritative source for historical KPI calculations.

---

## KPI Snapshot (2025-01-07 — 2026-03-18)

| Metric | Value |
|--------|-------|
| Total tasks | 115 |
| Done | 86 |
| In Progress | 27 |
| Todo | 0 |
| Canceled | 0 |
| Paused (BBC/On Hold) | 2 |
| Backlog | 0 |
| Tasks with ETA+Delivery | 81 |
| **On-time rate** | **95.1%** (77/81) |
| Late deliveries | 4 |
| Avg absolute delta | 0.3 days |
| **Within 1 week (Waki target >90%)** | **98.8%** (80/81) |
| Avg duration (Date Add → Delivery) | 0.6 days |
| Median duration | 0 days |
| Max duration | 11 days |

### Waki KPI Assessment

1. **ETA Accuracy (<1 week, >90%):** 98.8% of delivered tasks within 1 week of ETA
2. **Faster Implementations (4-week target):** Avg 0.6 days, median 0 days
3. **Implementation Reliability (90%):** 95.1% on-time delivery rate

---

## Customer Breakdown

- **QBO**: 34 tasks (32 done)
- **GENERAL**: 24 tasks (18 done)
- **CODA**: 20 tasks (1 done)
- **GEM**: 9 tasks (8 done)
- **MAILCHIMP**: 5 tasks (5 done)
- **Waki**: 4 tasks (4 done)
- **GONG**: 4 tasks (4 done)
- **CALLRAIL**: 3 tasks (3 done)
- **Routine**: 2 tasks (2 done)
- **MailChimp**: 2 tasks (2 done)
- **SITEIMPROVE**: 2 tasks (2 done)
- **HOCKEYSTACK**: 2 tasks (2 done)
- **HockeyStack**: 1 tasks (0 done)
- **PEOPLE.AI**: 1 tasks (1 done)
- **APOLLO**: 1 tasks (1 done)
- **TROPIC**: 1 tasks (1 done)

## Demand Type Breakdown

- **Improvement**: 49
- **Maintenance**: 41
- **Strategic**: 14
- **External(Customer)**: 7
- **Routine**: 2
- **Incident**: 2

---

## Full Historical Record

| # | Linear | Customer | Focus | Status | Date Add | ETA | Delivery | Delta |
|---|--------|----------|-------|--------|----------|-----|----------|-------|
| 1 | RAC-603 | Waki | TSA CODA DOC | Done | 2025-12-12 | 01/30/26 | - |  |
| 2 | RAC-565 | QBO | Handover QBO to Alexandra | Done | 2025-12-12 | 01/16/26 | - |  |
| 3 | RAC-572 | GEM | GEM Integration Support | In Progress | 01/30/26 | TBD | - |  |
| 4 | RAC-518 | CODA | TSA Documentation Process | In Progress | 2025-12-12 | 02/28/26 | - |  |
| 5 | RAC-519 | CODA | TSA Communication Process | In Progress | 2025-12-12 | 02/28/26 | - |  |
| 6 | RAC-520 | CODA | TSA Feedback Plan Doc | In Progress | 2025-12-12 | 02/28/26 | - |  |
| 7 | RAC-521 | CODA | TSA Routine Guide | In Progress | 2025-12-12 | 02/28/26 | - |  |
| 8 | RAC-522 | CODA | TSA Documentation Process | In Progress | 2025-12-12 | 02/28/26 | - |  |
| 9 | RAC-525 | CODA | Customer Overview - GONG | In Progress | 2025-01-25 | 02/15/26 | - |  |
| 10 | RAC-526 | CODA | Customer Overview - QBO | In Progress | 2025-01-25 | 02/18/26 | - |  |
| 11 | RAC-527 | CODA | Customer Overview - MAILCHIMP | In Progress | 2025-01-25 | 02/21/26 | - |  |
| 12 | RAC-528 | CODA | Customer Overview - ARCHER | In Progress | 2025-01-25 | 02/24/26 | - |  |
| 13 | RAC-529 | CODA | Customer Overview - TABS | In Progress | 2025-01-25 | 02/27/26 | - |  |
| 14 | RAC-530 | CODA | Customer Overview - TROPIC | In Progress | 2025-01-25 | 03/02/26 | - |  |
| 15 | RAC-531 | CODA | Customer Overview - PEOPLE.AI | In Progress | 2025-01-25 | 03/05/26 | - |  |
| 16 | RAC-532 | CODA | Customer Overview - PEOPLE.AI | In Progress | 2025-01-25 | 03/08/26 | - |  |
| 17 | RAC-597 | HockeyStack | TSA Routine of DATA GEN | Paused | 2025-22-12 | TBD | - |  |
| 18 | RAC-533 | CODA | Customer Overview - GAINSIGHT | In Progress | 2025-01-25 | 02/28/26 | - |  |
| 19 | RAC-534 | CODA | Customer Overview - BREVO | In Progress | 2025-01-25 | 02/28/26 | - |  |
| 20 | RAC-535 | CODA | Customer Overview - Others | In Progress | 2025-01-25 | 03/28/26 | - |  |
| 21 | RAC-536 | CODA | TSA Flowchart | In Progress | 2025-01-25 | 03/28/26 | - |  |
| 22 | RAC-566 | QBO | Winter Release Support | In Progress | 2025-01-07 | 02/13/26 | - |  |
| 23 | RAC-607 | GENERAL | TSA Feedback Plan | In Progress | 2026-01-30 | 02/06/26 | - |  |
| 24 | RAC-608 | GENERAL | Gantt Routine | In Progress | 2026-02-02 | 02/06/26 | - |  |
| 25 | RAC-609 | Routine | Dailys Reports Team improvements | Done | 2025-12-12 | 2025-12-17 | 2025-12-17 | 0 |
| 26 | RAC-610 | Routine | Organize weekly SYNC routine with Thais | Done | 2025-12-12 | 2025-12-17 | 2025-12-17 | 0 |
| 27 | RAC-604 | Waki | Build 2026 Roadmap | Done | 2025-12-12 | 01/16/26 | - |  |
| 28 | RAC-605 | Waki | Build 2026 stratetgic | Done | 2025-12-12 | 01/16/26 | - |  |
| 29 | RAC-611 | GENERAL | Help Waki Q.A. Monarch | In Progress | 2025-12-12 | 02/07/26 | - |  |
| 30 | RAC-612 | GENERAL | Build a professional onboarding | Paused | 2025-12-12 | TBD | - |  |
| 31 | RAC-613 | GENERAL | TSA KPI | In Progress | 2025-01-25 | 02/15/26 | - |  |
| 32 | RAC-523 | CODA | TSA routine mapping | In Progress | 2026-01-28 | 02/15/26 | - |  |
| 33 | RAC-585 | MailChimp | Support Gabi | Done | 2026-01-12 | 2026-01-12 | 2026-01-12 | 0 |
| 34 | RAC-586 | MailChimp | Auto Slack report RETRO | Done | 2026-01-12 | 2026-01-12 | 2026-01-12 | 0 |
| 35 | RAC-524 | CODA | SALES FORCE AT CODA | In Progress | 2026-02-02 | 03/28/26 | - |  |
| 36 | RAC-614 | GENERAL | Solutions Excellence
2026 Strategic Pla | In Progress | 2026-01-30 | 02/13/26 | - |  |
| 37 | RAC-606 | Waki | FEEDBACK CODA | Done |  |  | - |  |
| 38 | RAC-567 | QBO | Canonical Intuit QBO Guide - 12-part con | Done | 2026-01-07 | 2026-01-08 | 2026-01-08 | 0 |
| 39 | RAC-538 | QBO | Winter Release Validation Matrix v4 | Done | 2026-01-12 | 2026-01-12 | 2026-01-12 | 0 |
| 40 | RAC-539 | QBO | Winter Release Gantt v9 FINAL | Done | 2026-01-20 | 2026-01-20 | 2026-01-20 | 0 |
| 41 | RAC-555 | QBO | IC Bills Gap Investigation (PLA-3202) | Done | 2026-01-22 | 2026-01-22 | 2026-01-22 | 0 |
| 42 | RAC-540 | QBO | Winter Release Staging Linear Tickets (P | Done | 2026-01-23 | 2026-01-23 | 2026-01-23 | 0 |
| 43 | RAC-556 | QBO | Keystone Consolidated Balance Sheet Fix | Done | 2026-01-26 | 2026-01-26 | 2026-01-26 | 0 |
| 44 | RAC-557 | QBO | Employee Duplication Fix + Admin Account | Done | 2026-01-27 | 2026-01-27 | 2026-01-27 | 0 |
| 45 | RAC-558 | QBO | IES Release Readiness Intel Report | Done | 2026-01-27 | 2026-01-27 | 2026-01-27 | 0 |
| 46 | RAC-559 | QBO | QBO WAR ROOM - Complete Ingestion Sessio | Done | 2026-02-05 | 2026-02-05 | 2026-02-05 | 0 |
| 47 | RAC-546 | QBO | Health Check Cycle - Keystone Constructi | Done | 2026-02-09 | 2026-02-09 | 2026-02-09 | 0 |
| 48 | RAC-568 | QBO | QBO Super Access System Build | Done | 2026-02-13 | 2026-02-13 | 2026-02-13 | 0 |
| 49 | RAC-541 | QBO | Winter Release Feature #28 Cost Groups V | Done | 2026-02-13 | 2026-02-13 | 2026-02-13 | 0 |
| 50 | RAC-542 | QBO | UAT Marathon - 5 Sessions (Rows 29-31, P | Done | 2026-02-14 | 2026-02-14 | 2026-02-18 | 4 |
| 51 | RAC-543 | QBO | 177 UAT Screenshots Downloaded & Annotat | Done | 2026-02-15 | 2026-02-15 | 2026-02-15 | 0 |
| 52 | RAC-544 | QBO | CONE UAT Dual-Persona Audit (32 Features | Done | 2026-02-16 | 2026-02-16 | 2026-02-20 | 4 |
| 53 | RAC-545 | QBO | UAT Sales Prints Grouped into PDFs + Hyp | Done | 2026-02-17 | 2026-02-17 | 2026-02-17 | 0 |
| 54 | RAC-560 | QBO | Accounting AI Ready-to-Post Investigatio | Done | 2026-02-23 | 2026-02-24 | 2026-02-24 | 0 |
| 55 | RAC-561 | QBO | IC Account Mapping Investigation | Done | 2026-02-23 | 2026-02-23 | 2026-02-23 | 0 |
| 56 | RAC-562 | QBO | Bank Rules Creation & Auto-Post Experime | Done | 2026-02-23 | 2026-02-23 | 2026-02-23 | 0 |
| 57 | RAC-547 | QBO | TCO Feature Checker Audit - Apex Tire (1 | Done | 2026-02-26 | 2026-02-26 | 2026-02-26 | 0 |
| 58 | RAC-548 | QBO | NV2 Non-Profit Health Check v1 + v2 (30  | Done | 2026-03-04 | 2026-03-04 | 2026-03-04 | 0 |
| 59 | RAC-549 | QBO | NV2 Deep Audit v3 - P0 FIXED (40+ Statio | Done | 2026-03-05 | 2026-03-05 | 2026-03-05 | 0 |
| 60 | RAC-550 | QBO | QBO Sweep v3.0 Master Prompt Creation (4 | Done | 2026-03-05 | 2026-03-06 | 2026-03-06 | 0 |
| 61 | RAC-551 | QBO | Mid Market Sweep v1 + v2 (Keystone Const | Done | 2026-03-06 | 2026-03-06 | 2026-03-06 | 0 |
| 62 | RAC-552 | QBO | QSP Events Sweep v1 + v2 + Revalidation | Done | 2026-03-06 | 2026-03-06 | 2026-03-06 | 0 |
| 63 | RAC-553 | QBO | Product Events Sweep + Fix + Revalidatio | Done | 2026-03-06 | 2026-03-06 | 2026-03-06 | 0 |
| 64 | RAC-554 | QBO | NV3 Manufacturing + Construction Clone S | Done | 2026-03-06 | 2026-03-06 | 2026-03-06 | 0 |
| 65 | RAC-569 | QBO | QBO Playbook Cockpit XLSX (94 Items, 10  | Done | 2026-03-08 | 2026-03-08 | 2026-03-08 | 0 |
| 66 | RAC-563 | QBO | Dataset vs SALES Audit Master Worklog (P | Done | 2026-02-04 | 2026-02-05 | 2026-02-05 | 0 |
| 67 | RAC-564 | QBO | P&L Negative for Professional Services ( | In Progress | 2026-03-05 |  | - |  |
| 68 | RAC-573 | GEM | GEM Milestone Plan + Code Quality Audit | Done | 2026-01-13 | 2026-01-13 | 2026-01-13 | 0 |
| 69 | RAC-574 | GEM | GEM Deep-Learn Intelligence (34 Value St | Done | 2026-01-18 | 2026-01-29 | 2026-01-29 | 0 |
| 70 | RAC-575 | GEM | GEM Pre-Signature Due Diligence + Green  | Done | 2026-01-30 | 2026-01-30 | 2026-01-30 | 0 |
| 71 | RAC-576 | GEM | GEM Pipeline (28 Linear Tickets + Visual | Done | 2026-02-02 | 2026-02-02 | 2026-02-02 | 0 |
| 72 | RAC-577 | GEM | GEM Linear Evidence + Taufer Pattern Ana | Done | 2026-02-03 | 2026-02-03 | 2026-02-03 | 0 |
| 73 | RAC-578 | GEM | GEM Linear Reorganization - Timeline Cor | Done | 2026-02-05 | 2026-02-05 | 2026-02-05 | 0 |
| 74 | RAC-579 | GEM | GEM DOCX v3 Delivery (31 Screenshots, Dr | Done | 2026-02-08 | 2026-02-08 | 2026-02-11 | 3 |
| 75 | RAC-580 | GEM | GEM Linear Tickets - Stories 1-6 + Demo  | Done | 2026-02-03 | 2026-02-05 | 2026-02-05 | 0 |
| 76 | RAC-581 | GONG | Gong API Exploration (6,530 Calls, 40 Us | Done | 2026-01-22 | 2026-01-22 | 2026-01-22 | 0 |
| 77 | RAC-582 | GONG | Gong Sandboxes Stuck Investigation | Done | 2026-01-29 | 2026-01-29 | 2026-01-29 | 0 |
| 78 | RAC-583 | GONG | Gong SFDC SAML Login Investigation | Done | 2026-02-16 | 2026-02-16 | 2026-02-16 | 0 |
| 79 | RAC-584 | GONG | Gong Engage Analytics Deep Investigation | Done | 2026-02-26 | 2026-02-26 | 2026-02-26 | 0 |
| 80 | RAC-587 | MAILCHIMP | Mailchimp Project Setup (SpineHUB Struct | Done | 2026-01-12 | 2026-01-12 | 2026-01-12 | 0 |
| 81 | RAC-588 | MAILCHIMP | Mailchimp signup_date Fix (80 Anonymous  | Done | 2026-01-27 | 2026-01-27 | 2026-01-27 | 0 |
| 82 | RAC-589 | MAILCHIMP | Mailchimp Audit (Duplicate IDs + Timesta | Done | 2026-01-28 | 2026-01-28 | 2026-01-28 | 0 |
| 83 | RAC-590 | MAILCHIMP | Mailchimp UAT Audit (3 Critical Errors i | Done | 2026-01-29 | 2026-01-29 | 2026-01-29 | 0 |
| 84 | RAC-591 | MAILCHIMP | Mailchimp Weekly Analysis + Confidence C | Done | 2026-02-03 | 2026-02-03 | 2026-02-03 | 0 |
| 85 | RAC-595 | SITEIMPROVE | Siteimprove Deep Learning (273 Slack + 4 | Done | 2026-01-27 | 2026-01-27 | 2026-01-27 | 0 |
| 86 | RAC-596 | SITEIMPROVE | Siteimprove SQL Validation (~150 Flow St | Done | 2026-01-29 | 2026-01-29 | 2026-01-29 | 0 |
| 87 | RAC-592 | CALLRAIL | CallRail Deep Learning (1,542 Slack + 97 | Done | 2026-01-26 | 2026-01-26 | 2026-01-26 | 0 |
| 88 | RAC-593 | CALLRAIL | CallRail NoFrame Response Strategy | Done | 2026-01-29 | 2026-01-29 | 2026-01-29 | 0 |
| 89 | RAC-594 | CALLRAIL | CallRail INC-26 Account Center Discovery | Done | 2026-03-04 | 2026-03-05 | 2026-03-05 | 0 |
| 90 | RAC-598 | HOCKEYSTACK | HockeyStack Deep Analysis (259 Slack, De | Done | 2026-01-15 | 2026-01-15 | 2026-01-15 | 0 |
| 91 | RAC-599 | HOCKEYSTACK | HockeyStack Thiago Onboarding Book (650+ | Done | 2026-01-18 | 2026-01-18 | 2026-01-18 | 0 |
| 92 | RAC-600 | PEOPLE.AI | People.ai REST API Full Mapping (40+ End | Done | 2026-01-29 | 2026-01-29 | 2026-01-29 | 0 |
| 93 | RAC-601 | APOLLO | Apollo Deep-Learn v2.1 (276 Linear, 2,23 | Done | 2026-02-16 | 2026-02-16 | 2026-02-16 | 0 |
| 94 | RAC-602 | TROPIC | Tropic General Update + Ingestion Pipeli | Done | 2026-03-02 | 2026-03-02 | 2026-03-02 | 0 |
| 95 | RAC-615 | GENERAL | SpineHUB v3.0 Collectors Ported to Pytho | Done | 2026-01-08 | 2026-01-08 | 2026-01-08 | 0 |
| 96 | RAC-616 | GENERAL | TSA_CORTEX Worklog Automation v1.3 (RAC- | Done | 2026-01-15 | 2026-01-15 | 2026-01-15 | 0 |
| 97 | RAC-617 | GENERAL | RETRO-TSA Project Created (Retrospective | Done | 2026-01-15 | 2026-01-15 | 2026-01-15 | 0 |
| 98 | RAC-618 | GENERAL | REPORT_CHECK Project (OBM Matrix, 100-Po | Done | 2026-01-19 | 2026-01-19 | 2026-01-19 | 0 |
| 99 | RAC-619 | GENERAL | TSA Routine Indicators (26 Indicators, 6 | Done | 2026-01-20 | 2026-01-20 | 2026-01-20 | 0 |
| 100 | RAC-620 | GENERAL | ALL_PEDALS AMA Report Setup | Done | 2026-01-27 | 2026-01-27 | 2026-01-27 | 0 |
| 101 | RAC-621 | GENERAL | TSA_DAILY_REPORT Project Created | Done | 2026-02-02 | 2026-02-02 | 2026-02-02 | 0 |
| 102 | RAC-622 | GENERAL | TSA_CORTEX Full Implementation Process P | Done | 2026-02-10 | 2026-02-10 | 2026-02-10 | 0 |
| 103 | RAC-623 | GENERAL | TSA_CORTEX Internal Audit v2.3 (18 Findi | Done | 2026-02-12 | 2026-02-12 | 2026-02-12 | 0 |
| 104 | RAC-626 | GENERAL | TSA Feedback Reports (5 DOCX, 4 Individu | Done | 2026-02-25 | 2026-02-25 | 2026-02-25 | 0 |
| 106 | RAC-624 | GENERAL | Weekly Standup PPT Automation (/weekly-p | Done | 2026-02-27 | 2026-02-27 | 2026-02-27 | 0 |
| 107 | RAC-625 | GENERAL | tbx-feature-checker Sync (15 Python File | Done | 2026-03-05 | 2026-03-05 | 2026-03-05 | 0 |
| 108 | RAC-627 | GENERAL | Coaching Analysis: Carlos Standup (Score | Done | 2026-02-02 | 2026-02-02 | 2026-02-12 | 10 |
| 109 | RAC-628 | GENERAL | Coaching Analysis: Gayathri Communicatio | Done | 2026-01-29 | 2026-01-29 | 2026-01-29 | 0 |
| 110 | RAC-629 | GENERAL | Horizontal Audit of 25 Projects (8 Retro | Done | 2026-01-28 | 2026-01-28 | 2026-01-28 | 0 |
| 111 | RAC-570 | QBO | WFS Milestone Plan (5 Phases, Dec 17 - M | Done | 2026-01-13 | 2026-01-13 | 2026-01-13 | 0 |
| 112 | RAC-571 | QBO | Gantt Audit (WFS + MailChimp - Both Unto | Done | 2026-01-22 | 2026-01-22 | 2026-01-22 | 0 |
| 113 | RAC-537 | CODA | Intuit Coda Extraction (44 Pages, Winter | Done | 2026-01-16 | 2026-01-16 | 2026-01-16 | 0 |
| 114 | RAC-630 | GENERAL | SHOCK_PLAN Project Consolidation (GM Pro | Done | 2026-03-03 | 2026-03-03 | 2026-03-03 | 0 |
| 115 | RAC-631 | GENERAL | Intuit QBO Post-Deal Playbook v5 (1,453  | Done | 2026-03-08 | 2026-03-08 | 2026-03-08 | 0 |
| 116 | RAC-632 | GENERAL | QBO Environment Master XLSX (79 Items) | Done | 2026-03-08 | 2026-03-08 | 2026-03-08 | 0 |

---

*Generated by TSA_CORTEX migration script on 2026-03-18. Source: TSA_Tasks_Consolidate spreadsheet, THIAGO tab.*