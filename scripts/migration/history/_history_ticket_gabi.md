# TSA Historical Data — Gabrielle Caputo

> **Purpose:** This ticket preserves the original dates and KPI-critical fields from the TSA Tasks Consolidate spreadsheet (Dec 2025 - Mar 2026). Linear migration happened on 2026-03-18, so `createdAt` and `completedAt` on migrated issues reflect the migration date, NOT original dates. Use THIS ticket as the authoritative source for historical KPI calculations.

---

## KPI Snapshot (2025-12-08 — 2026-03-18)

| Metric | Value |
|--------|-------|
| Total tasks | 43 |
| Done | 35 |
| In Progress | 3 |
| Todo | 0 |
| Canceled | 1 |
| Paused (BBC/On Hold) | 4 |
| Backlog | 0 |
| Tasks with ETA+Delivery | 31 |
| **On-time rate** | **93.5%** (29/31) |
| Late deliveries | 2 |
| Avg absolute delta | 0.3 days |
| **Within 1 week (Waki target >90%)** | **100.0%** (31/31) |
| Avg duration (Date Add → Delivery) | 2.5 days |
| Median duration | 0 days |
| Max duration | 39 days |

### Waki KPI Assessment

1. **ETA Accuracy (<1 week, >90%):** 100.0% of delivered tasks within 1 week of ETA
2. **Faster Implementations (4-week target):** Avg 2.5 days, median 0 days
3. **Implementation Reliability (90%):** 93.5% on-time delivery rate

---

## Customer Breakdown

- **Mailchimp**: 25 tasks (23 done)
- **Archer**: 9 tasks (6 done)
- **Staircase**: 9 tasks (6 done)

## Demand Type Breakdown

- **External(Customer)**: 25
- **Improvement**: 8
- **Data Gen.**: 7
- **Routine**: 2
- **Strategic**: 1

---

## Full Historical Record

| # | Linear | Customer | Focus | Status | Date Add | ETA | Delivery | Delta |
|---|--------|----------|-------|--------|----------|-----|----------|-------|
| 1 | RAC-307 | Archer | BIA campaing | In Progress | 2025-12-12 | 2025-12-26 | - |  |
| 2 | RAC-308 | Archer | BIA base is done; team is focused on BIA | Canceled | 2025-12-08 | Work on BIA campaign (ETA 2025-12-10); finish resilience by end of December; meet with Josh and Waki to align strategy; create documentation for next audit (ETA 2025-12-10); gather information about data feeds configuration (ETA 2025-12-09). | - |  |
| 3 | RAC-309 | Archer | Arrumar Workflow | Done | 2025-12-10 | 2025-12-12 | 2025-12-12 | 0 |
| 4 | RAC-316 | Mailchimp | Initial configurations (C.E) | Done |  | 2025-12-12 | 2025-12-12 | 0 |
| 5 | RAC-317 | Mailchimp | Mailchimp dev integration is in test; we | Done | 2025-12-08 | Connect Shopify dev accounts to the website (ETA 2025-12-05); rebuild website to connect to the correct dev account; set API key for prod dev account; review automation flows (ETA 2025-12-08); build product catalog (ETA 2025-12-08). | 2025-12-08 |  |
| 6 | RAC-318 | Mailchimp | Manter configuração do website | Done | 2025-12-10 | 2025-12-12 | 2025-12-12 | 0 |
| 7 | RAC-341 | Staircase | Year N data | Paused | 2025-12-12 | N/A | - |  |
| 8 | RAC-347 | Staircase | Adjustments | Done | 2025-12-12 | 2025-12-12 | 2025-12-18 | 6 |
| 9 | RAC-348 | Staircase | Ajustar tabelas | Done | 2025-12-12 | 2025-12-12 | 2025-12-12 | 0 |
| 10 | RAC-337 | Mailchimp | Pop up forms and landing pages design | Done | 2025-12-16 | TBD | - |  |
| 11 | RAC-338 | Mailchimp | Tickets for spike | Done | 2025-12-15 | 2025-12-15 | 2025-12-15 | 0 |
| 12 | RAC-323 | Mailchimp | Ticket for email automation | Done | 12-15 |  | 2025-12-15 |  |
| 13 | RAC-324 | Mailchimp | Customer segmentation | Done | 2025-12-16 | 2025-12-19 | 2025-12-19 | 0 |
| 14 | RAC-336 | Mailchimp | Q/A table from dataset | Done | 12-17 | 2025-12-17 | 2025-12-17 | 0 |
| 15 | RAC-349 | Staircase | Bug list | Done | 2025-12-17 | 2025-12-18 | 2025-12-18 | 0 |
| 16 | RAC-319 | Mailchimp | Shopify Tool | Paused | 2025-12-17 | TBD | - |  |
| 17 | RAC-325 | Mailchimp | Framework A/B testing | Done |  | 2025-12-23 | 2025-12-23 | 0 |
| 18 | RAC-326 | Mailchimp | Design Event Tracking & Analytics Framew | Done |  | 2025-12-23 | 2025-12-23 | 0 |
| 19 | RAC-327 | Mailchimp | Abandonment cart automation | Done | 2026-01-05 | 2026-01-09 | 2026-01-09 | 0 |
| 20 | RAC-328 | Mailchimp | Browse abandonment automation | Done | 2026-01-05 | 2026-02-13 | 2026-02-13 | 0 |
| 21 | RAC-310 | Archer | Action plan definition | Done | 2026-01-05 | 2026-01-05 | 2026-01-05 | 0 |
| 22 | RAC-342 | Staircase | Meetings sync | Paused | 2025-12-12 | TBD | - |  |
| 23 | RAC-343 | Staircase | Japonese version | In Progress | 2026-01-05 | 2026-01-30 | - |  |
| 24 | RAC-311 | Archer | Audit data generation | In Progress | 2026-01-07 | 2026-01-30 | - |  |
| 25 | RAC-344 | Staircase | Japonese dataset | Done | 2026-01-12 | 01-13 | - |  |
| 26 | RAC-329 | Mailchimp | Emails template | Done | 2026-01-12 | 2026-01-12 | 2026-01-14 | 2 |
| 27 | RAC-320 | Mailchimp | Shopify Login | Done | 2026-01-14 | 2026-01-14 | 2026-01-14 | 0 |
| 28 | RAC-321 | Mailchimp | HTML block | Done | 2026-01-14 | 2026-01-14 | 2026-01-14 | 0 |
| 29 | RAC-322 | Mailchimp | Cloudinary | Paused | 2026-01-19 | TBD | - |  |
| 30 | RAC-332 | Mailchimp | Tags | Done | 2026-01-19 | 2026-01-19 | 2026-01-19 | 0 |
| 31 | RAC-333 | Mailchimp | Activity plan for customers | Done | 2026-01-19 | 2026-01-19 | 2026-01-19 | 0 |
| 32 | RAC-334 | Mailchimp | Activity plan for orders | Done | 2026-01-19 | 2026-01-19 | 2026-01-19 | 0 |
| 33 | RAC-335 | Mailchimp | Activity plan for abandoned carts | Done | 2026-01-19 | 2026-01-19 | 2026-01-19 | 0 |
| 34 | RAC-312 | Archer | Compliance | Done | 2026-01-19 | 2026-01-19 | 2026-01-19 | 0 |
| 35 | RAC-339 | Mailchimp | UAT Docs for Core stories | Done | 2026-02-04 | 2026-02-06 | 2026-02-06 | 0 |
| 36 | RAC-340 | Mailchimp | Scripts for browse abandonment | Done | 2026-02-04 | 2026-02-04 | 2026-02-04 | 0 |
| 37 | RAC-345 | Staircase | Sheets with CRM data japanese | Done | 2026-02-04 | 2026-02-04 | 2026-02-04 | 0 |
| 38 | RAC-346 | Staircase | Emails translation Year 1 | Done | 2026-02-09 | 2026-02-13 | 2026-02-13 | 0 |
| 39 | RAC-330 | Mailchimp | SMS portion | Done | 2026-09-02 | 2026-02-10 | 2026-02-10 | 0 |
| 40 | RAC-331 | Mailchimp | SMS story requirements | Done | 2026-02-09 | 2026-02-10 | 2026-02-10 | 0 |
| 41 | RAC-313 | Archer | Validate RCSA | Done | 2026-02-11 | 2026-02-11 | 2026-02-11 | 0 |
| 42 | RAC-314 | Archer | Validate RCSA campaigns | Done | 2026-02-11 | 2026-02-11 | 2026-02-11 | 0 |
| 43 | RAC-315 | Archer | Validate RCSA Hierarchy | Done | 2026-02-11 | 2026-02-12 | 2026-02-12 | 0 |

---

*Generated by TSA_CORTEX migration script on 2026-03-18. Source: TSA_Tasks_Consolidate spreadsheet, GABI tab.*