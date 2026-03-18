# TSA Historical Data — Carlos Pereira

> **Purpose:** This ticket preserves the original dates and KPI-critical fields from the TSA Tasks Consolidate spreadsheet (Dec 2025 - Mar 2026). Linear migration happened on 2026-03-18, so `createdAt` and `completedAt` on migrated issues reflect the migration date, NOT original dates. Use THIS ticket as the authoritative source for historical KPI calculations.

---

## KPI Snapshot (2025-12-05 — 2026-03-18)

| Metric | Value |
|--------|-------|
| Total tasks | 132 |
| Done | 106 |
| In Progress | 5 |
| Todo | 7 |
| Canceled | 7 |
| Paused (BBC/On Hold) | 7 |
| Backlog | 0 |
| Tasks with ETA+Delivery | 0 |

---

## Customer Breakdown

- **Siteimprove**: 66 tasks (60 done)
- **Gong**: 61 tasks (41 done)
- **Apollo**: 3 tasks (3 done)
- **TBX**: 2 tasks (2 done)

## Demand Type Breakdown

- **Data Gen.**: 47
- **Improvement**: 35
- **Strategic**: 21
- **Maintenance**: 17
- **External(Customer)**: 8
- **Routine**: 3
- **Incident**: 1

---

## Full Historical Record

| # | Linear | Customer | Focus | Status | Date Add | ETA | Delivery | Delta |
|---|--------|----------|-------|--------|----------|-----|----------|-------|
| 1 | RAC-367 | Gong | Deals history refactor | Done | 2025-12-05 | 2025-12-08 | - |  |
| 2 | RAC-428 | Siteimprove | Dataset creation | Done | 2025-12-12 | 2025-12-12 | - |  |
| 3 | RAC-368 | Gong | Sandbox improvements | Done | 2025-12-10 | 2025-12-15 | - |  |
| 4 | RAC-369 | Gong | Gong sandbox improvements and custom met | Done | 2025-12-08 | 2025-12-17 | - |  |
| 5 | RAC-429 | Siteimprove | Open tickets for the CE team | Done | 2025-12-10 | 2025-12-12 | - |  |
| 6 | RAC-408 | Gong | Fix the AI Trackers | Done | 2025-12-15 | 2026-01-16 | - |  |
| 7 | RAC-497 | TBX | Alinhar ticket mais objetivos | Done | 2025-12-10 | 2025-12-11 | - |  |
| 8 | RAC-430 | Siteimprove | Add screenshots and records for the site | Done | 2025-12-15 | 2025-12-15 | - |  |
| 9 | RAC-431 | Siteimprove | Improve the user simulator script | Done | 2025-12-15 | 2025-12-16 | - |  |
| 10 | RAC-389 | Gong | Fix the Deals Score ingestion step | Done | 2025-12-15 | 2026-01-16 | - |  |
| 11 | RAC-409 | Gong | Open Spike ticket for the Workspace disc | Paused | 2025-12-15 | 2025-12-17 | - |  |
| 12 | RAC-390 | Gong | Understand how the Deals Score field wor | Done | 2025-12-15 | 2025-12-19 | - |  |
| 13 | RAC-424 | Gong | Work on the Gong Visualizer platform | Paused | 2025-12-15 | 2026-02-11 | - |  |
| 14 | RAC-370 | Gong | Fix the New Business ~Generated and Fore | Done | 2025-12-22 | 2025-12-23 | - |  |
| 15 | RAC-379 | Gong | Ingest the Test Account using the Salesf | Done | 2026-01-08 | 2026-01-09 | - |  |
| 16 | RAC-410 | Gong | Analyze the New Business dashboard inter | Done | 2025-12-15 | 2026-01-16 | - |  |
| 17 | RAC-432 | Siteimprove | Siteimprove work is centered on the acti | Done | 2025-12-08 | 2025-12-18 | - |  |
| 18 | RAC-433 | Siteimprove | Add VPN or proxy to the simulator script | Canceled | 2025-12-15 | 2025-12-16 | - |  |
| 19 | RAC-434 | Siteimprove | Open ticket for adding Keywords monitore | Done | 2025-12-15 | 2025-12-18 | - |  |
| 20 | RAC-411 | Gong | Fix Hubspot accounts to show the MEDDICC | Done | 2025-12-22 | 2025-12-23 | - |  |
| 21 | RAC-437 | Siteimprove | Create the tables in the Siteimprove Dat | Done | 2025-12-15 | 2025-12-20 | - |  |
| 22 | RAC-435 | Siteimprove | Open Spike ticket to investigate how can | Done | 2025-12-15 | 2025-12-18 | - |  |
| 23 | RAC-478 | Siteimprove | Open ticket to add monitored keywords to | Canceled | 2026-01-05 | 2026-01-12 | - |  |
| 24 | RAC-414 | Gong | Customer Call | Done | 2026-01-12 | 2026-01-12 | - |  |
| 25 | RAC-436 | Siteimprove | Create ticket for the dataset rotation s | Done | 2026-01-12 | 2026-01-12 | - |  |
| 26 | RAC-380 | Gong | Demo Account Refresh | In Progress | 2026-01-08 | 2026-01-30 | - |  |
| 27 | RAC-415 | Gong | Customer Call | Done | 2026-01-14 | 2026-01-14 | - |  |
| 28 | RAC-381 | Gong | Historical Data model | In Progress | 2026-01-08 | 2026-01-30 | - |  |
| 29 | RAC-371 | Gong | Sandbox mirrors demo | Todo | 2026-01-08 | 2026-02-06 | - |  |
| 30 | RAC-372 | Gong | Automate the MEDDICC AI trackers for Hub | Todo | 2026-01-05 | TBD | - |  |
| 31 | RAC-373 | Gong | Sandbox ingestion visibility | Todo | 2026-01-08 | TBD | - |  |
| 32 | RAC-412 | Gong | Gmail token disconnect | Todo | 2026-01-08 | TBD | - |  |
| 33 | RAC-374 | Gong | Automate the entire Hubspot Gong account | Todo | 2026-01-08 | TBD | - |  |
| 34 | RAC-375 | Gong | Deals Forecast Hiding team members | Done | 2026-01-08 | 2026-01-14 | - |  |
| 35 | RAC-382 | Gong | Add the missing custom fields in the dev | Done | 2026-01-08 | 2026-01-09 | - |  |
| 36 | RAC-438 | Siteimprove | Create Website rotation Logic | Done | - | 2026-01-08 | - |  |
| 37 | RAC-416 | Gong | Align with Soranzo resource alocation fo | Done | 2026-01-08 | 2026-01-09 | - |  |
| 38 | RAC-391 | Gong | Fix forecast page to have forecast in al | Done | 2026-01-14 | 2026-01-30 | - |  |
| 39 | RAC-439 | Siteimprove | Change the dataset table for key metrics | Done | 2026-01-13 | 2026-01-13 | - |  |
| 40 | RAC-440 | Siteimprove | Create the dataset table for siteimprove | Canceled | 2026-01-08 | 2026-01-16 | - |  |
| 41 | RAC-392 | Gong | Move or Create more deals between the en | Done | 2026-01-14 | 2026-01-30 | - |  |
| 42 | RAC-393 | Gong | Adjust the values from the Forecast page | Done | 2026-01-14 | 2026-02-18 | - |  |
| 43 | RAC-394 | Gong | Add the "Pushed Out" category to the Dea | Done | 2026-01-14 | 2026-01-30 | - |  |
| 44 | RAC-441 | Siteimprove | Create the data to power the dashboards  | Canceled | 2026-01-08 | 2026-01-16 | - |  |
| 45 | RAC-395 | Gong | Fix the Deals Analytics Accuracy Page | Paused | 2026-01-14 | 2026-01-30 | - |  |
| 46 | RAC-401 | Gong | Change the Engage To-Dos Page to display | Done | 2026-01-14 | 2026-02-18 | - |  |
| 47 | RAC-442 | Siteimprove | Create new versions from the Government  | Done | 2025-12-19 | 2026-01-09 | - |  |
| 48 | RAC-402 | Gong | Fix the Engage Analytics page | Done | 2026-01-14 | 2026-02-18 | - |  |
| 49 | RAC-413 | Gong | New Salesforce Custom fields | Done | 2026-01-14 | 2026-01-30 | - |  |
| 50 | RAC-403 | Gong | Engage templates with inline prompts | Done | 2026-01-08 | 2026-01-14 | - |  |
| 51 | RAC-396 | Gong | Remove some of the deal pipeline dashboa | Done | 2026-01-08 | 2026-01-30 | - |  |
| 52 | RAC-404 | Gong | Custom dashboards and metrics | Done | 2026-01-08 | 2026-01-14 | - |  |
| 53 | RAC-405 | Gong | AI Trainer | Paused | 2026-01-08 | 2026-01-14 | - |  |
| 54 | RAC-406 | Gong | AI populated CRM fields (AI Data Extract | Done | 2026-01-08 | 2026-01-21 | - |  |
| 55 | RAC-417 | Gong | Post Customer Call Alignment with Shivan | Done | 2026-01-14 | 2026-01-14 | - |  |
| 56 | RAC-376 | Gong | AI Builder | Paused | 2026-01-14 | TBD | - |  |
| 57 | RAC-397 | Gong | Add missing deals pipeline board to the  | Done | 2026-01-12 | 2026-01-13 | - |  |
| 58 | RAC-418 | Gong | Post Customer Call Alignment with Shivan | Done | 2026-01-12 | 2026-01-12 | - |  |
| 59 | RAC-398 | Gong | Update the Forecast column named "Commit | Paused | 2026-01-14 | 2026-01-16 | - |  |
| 60 | RAC-443 | Siteimprove | Create the logic to schedule userflows d | Done | 2026-01-14 | 2026-01-16 | - |  |
| 61 | RAC-399 | Gong | Change the forecast page view to show th | Done | 2026-01-14 | 2026-02-18 | - |  |
| 62 | RAC-444 | Siteimprove | Create Metadata table and open the ticke | Done | 2026-01-26 | 2026-01-26 | - |  |
| 63 | RAC-400 | Gong | Investigate empty values for the Deals A | Done | 2026-01-26 | 2026-01-29 | - |  |
| 64 | RAC-383 | Gong | Ingest the dev59 account with the new de | Canceled | 2026-01-28 | 2026-01-29 | - |  |
| 65 | RAC-377 | Gong | Sandbox Login error | Done | 2026-01-28 | 2026-01-28 | - |  |
| 66 | RAC-384 | Gong | Check dev60 Ingestion | Done | 2026-02-02 | 2026-02-02 | - |  |
| 67 | RAC-385 | Gong | Import team members manually to dev60 ac | Canceled | 2026-02-02 | 2026-02-02 | - |  |
| 68 | RAC-386 | Gong | Start ingestion for the dev61 account | Canceled | 2026-02-02 | 2026-02-03 | - |  |
| 69 | RAC-479 | Siteimprove | Check Userflows schedules | Done | 2026-02-02 | 2026-02-02 | - |  |
| 70 | RAC-480 | Siteimprove | Check Userflows distribution | Done | 2026-02-02 | 2026-02-05 | - |  |
| 71 | RAC-498 | TBX | Fill the routine spreadsheet (initial wo | Done | 2026-02-02 | 2026-02-03 | - |  |
| 72 | RAC-447 | Siteimprove | Generate the userflows for the governmen | Done | 2026-02-03 | 2026-02-04 | - |  |
| 73 | RAC-448 | Siteimprove | Generate the usersteps for the governmen | Done | 2026-02-03 | 2026-02-04 | - |  |
| 74 | RAC-449 | Siteimprove | Generate the funnels for the government  | Done | 2026-02-03 | 2026-02-04 | - |  |
| 75 | RAC-450 | Siteimprove | Generate the events for the government w | Done | 2026-02-03 | 2026-02-05 | - |  |
| 76 | RAC-451 | Siteimprove | Generate the key metrics for the governm | Done | 2026-02-03 | 2026-02-05 | - |  |
| 77 | RAC-452 | Siteimprove | Generate the keywords for the government | Done | 2026-02-03 | 2026-02-05 | - |  |
| 78 | RAC-445 | Siteimprove | Open ticket for the elements update for  | Done | 2026-02-03 | 2026-02-04 | - |  |
| 79 | RAC-481 | Siteimprove | Increase the ammount of simulated users  | Done | 2026-03-09 | 2026-03-11 | - |  |
| 80 | RAC-387 | Gong | Make the final adjustments on dev64 | Done | 2026-03-09 | 2026-03-11 | - |  |
| 81 | RAC-446 | Siteimprove | Migrate the Siteimprove dataset to the n | Todo | 2026-03-09 | 2026-03-16 | - |  |
| 82 | RAC-484 | Siteimprove | Finish the V1 for the Financial Story we | Done | 2026-03-09 | 2026-03-13 | - |  |
| 83 | RAC-487 | Siteimprove | Customer Call | Done | 2026-02-03 | 2026-02-03 | - |  |
| 84 | RAC-453 | Siteimprove | Generate the userflows for the governmen | Done | 2026-02-04 | 2026-02-09 | - |  |
| 85 | RAC-454 | Siteimprove | Generate the usersteps for the governmen | Done | 2026-02-04 | 2026-02-09 | - |  |
| 86 | RAC-455 | Siteimprove | Generate the funnels for the government  | Done | 2026-02-04 | 2026-02-09 | - |  |
| 87 | RAC-456 | Siteimprove | Generate the events for the government w | Done | 2026-02-04 | 2026-02-09 | - |  |
| 88 | RAC-457 | Siteimprove | Generate the key metrics for the governm | Done | 2026-02-04 | 2026-02-10 | - |  |
| 89 | RAC-458 | Siteimprove | Generate the keywords for the government | Done | 2026-02-04 | 2026-02-10 | - |  |
| 90 | RAC-419 | Gong | Customer Call | Done | 2026-02-04 | 2026-02-04 | - |  |
| 91 | RAC-388 | Gong | Ingest account dev62 creating team membe | Done | 2026-02-04 | 2026-02-06 | - |  |
| 92 | RAC-459 | Siteimprove | Fix flow branches for v1, v2 and v3 | Done | 2026-02-06 | 2026-02-10 | - |  |
| 93 | RAC-407 | Gong | Add the A tier accounts into two differe | Done | 2026-01-14 | 2026-02-18 | - |  |
| 94 | RAC-485 | Siteimprove | Create the bank website | Done | 2026-01-17 | 2026-02-24 | - |  |
| 95 | RAC-460 | Siteimprove | Generate the userflows for the governmen | Done | 2026-02-09 | 2026-02-13 | - |  |
| 96 | RAC-461 | Siteimprove | Generate the usersteps for the governmen | Done | 2026-02-09 | 2026-02-13 | - |  |
| 97 | RAC-462 | Siteimprove | Generate the funnels for the government  | Done | 2026-02-09 | 2026-02-13 | - |  |
| 98 | RAC-463 | Siteimprove | Generate the events for the government w | Done | 2026-02-09 | 2026-02-13 | - |  |
| 99 | RAC-464 | Siteimprove | Generate the key metrics for the governm | Done | 2026-02-09 | 2026-02-13 | - |  |
| 100 | RAC-465 | Siteimprove | Generate the keywords for the government | Done | 2026-02-09 | 2026-02-13 | - |  |
| 101 | RAC-466 | Siteimprove | Generate the userflows for the governmen | Done | 2026-02-09 | 2026-02-18 | - |  |
| 102 | RAC-467 | Siteimprove | Generate the usersteps for the governmen | Done | 2026-02-09 | 2026-02-18 | - |  |
| 103 | RAC-468 | Siteimprove | Generate the funnels for the government  | Done | 2026-02-09 | 2026-02-18 | - |  |
| 104 | RAC-469 | Siteimprove | Generate the events for the government w | Done | 2026-02-09 | 2026-02-18 | - |  |
| 105 | RAC-470 | Siteimprove | Generate the key metrics for the governm | Done | 2026-02-09 | 2026-02-18 | - |  |
| 106 | RAC-471 | Siteimprove | Generate the keywords for the government | Done | 2026-02-09 | 2026-02-18 | - |  |
| 107 | RAC-472 | Siteimprove | Generate the userflows for the governmen | Done | 2026-02-09 | 2026-02-24 | - |  |
| 108 | RAC-473 | Siteimprove | Generate the usersteps for the governmen | Done | 2026-02-09 | 2026-02-24 | - |  |
| 109 | RAC-474 | Siteimprove | Generate the funnels for the government  | Done | 2026-02-09 | 2026-02-24 | - |  |
| 110 | RAC-475 | Siteimprove | Generate the events for the government w | Done | 2026-02-09 | 2026-02-24 | - |  |
| 111 | RAC-476 | Siteimprove | Generate the key metrics for the governm | Done | 2026-02-09 | 2026-02-24 | - |  |
| 112 | RAC-477 | Siteimprove | Generate the keywords for the government | Done | 2026-02-09 | 2026-02-24 | - |  |
| 113 | RAC-494 | Apollo | Study the Apollo documentation to get on | Done | 2026-02-17 | 2026-02-18 | - |  |
| 114 | RAC-482 | Siteimprove | Adjust Siteimprove data to ensure that a | Done | 2026-02-17 | 2026-02-24 | - |  |
| 115 | RAC-378 | Gong | Configure Hubspot 18 account | Done | 2026-02-17 | 2026-02-18 | - |  |
| 116 | RAC-421 | Gong | Create the Story generation framework fo | In Progress | 2026-03-09 | 2026-03-20 | - |  |
| 117 | RAC-425 | Gong | Create Slack Workflow to deliver Sandbox | Todo | 2026-03-09 | 2026-03-18 | - |  |
| 118 | RAC-426 | Gong | Reorganize Gong Drive | Done | 2026-03-09 | 2026-03-10 | - |  |
| 119 | RAC-488 | Siteimprove | Reorganize Siteimprove Drive | Done | 2026-03-09 | 2026-03-11 | - |  |
| 120 | RAC-486 | Siteimprove | Generate Funnels, Key metrics, Events, U | Done | 2026-03-09 | 2026-03-24 | - |  |
| 121 | RAC-422 | Gong | Ingest the partner demo account | Paused | 2026-03-09 | TBD | - |  |
| 122 | RAC-423 | Gong | Work on a new date format for the Gong t | In Progress | 2026-03-09 | 2026-04-03 | - |  |
| 123 | RAC-489 | Siteimprove | Document the story elements for the Site | Done | 2026-02-03 | 2026-02-27 | - |  |
| 124 | RAC-490 | Siteimprove | Document the Siteimprove platform workfl | Done | 2026-02-03 | 2026-02-27 | - |  |
| 125 | RAC-491 | Siteimprove | Document the Siteimprove technical imple | Done | 2026-02-03 | 2026-02-27 | - |  |
| 126 | RAC-427 | Gong | Document the Gong platform workflow and  | Done | 2026-02-03 | 2026-02-27 | - |  |
| 127 | RAC-492 | Siteimprove | Get timelines on the website rotation fi | Done | 2026-03-16 | 2026-03-16 | - |  |
| 128 | RAC-495 | Apollo | Document Apollo Platform Usage and Workf | Done | 2026-03-16 | 2026-03-20 | - |  |
| 129 | RAC-496 | Apollo | Plan Apollo Implementation Improvements | Done | 2026-03-16 | 2026-03-18 | - |  |
| 130 | RAC-420 | Gong | Customer Call | Done | 2026-03-16 | 2026-03-16 | - |  |
| 131 | RAC-483 | Siteimprove | Fix dataset values to work with the curr | Done | 2026-03-16 | 2026-03-17 | - |  |
| 132 | RAC-493 | Siteimprove | Release new dataset version and monitore | In Progress | 2026-03-16 | 2026-03-17 | - |  |

---

*Generated by TSA_CORTEX migration script on 2026-03-18. Source: TSA_Tasks_Consolidate spreadsheet, CARLOS tab.*