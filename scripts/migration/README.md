# TSA Sheets → Linear Migration

Migration of all TSA team activities from Google Sheets (`TSA_Tasks_Consolidate`) to Linear as the single source of truth.

## Execution Order

1. `create_labels_projects.py` — Created 12 labels + 9 projects
2. `migrate_alexandra_to_linear.py` — 10 parents + 71 subs (RAC-228..298)
3. `apply_labels_bulk.py` — Applied customer + scope labels to Alexandra's issues
4. `migrate_gabi_to_linear.py` — 7 parents + 43 subs (RAC-300..349)
5. `migrate_carlos_to_linear.py` — 17 parents + 132 subs (RAC-350..498)
6. `migrate_thiago_to_linear.py` — 19 parents + 115 subs (RAC-499..632)
7. `build_history_tickets_all.py` — 3 KPI reference tickets (RAC-633..635)

## Results

| Person | Parents | Subs | History | Range |
|--------|---------|------|---------|-------|
| Alexandra | 10 | 71 | RAC-299 | RAC-228..298 |
| Gabrielle | 7 | 43 | RAC-633 | RAC-300..349 |
| Carlos | 17 | 132 | RAC-634 | RAC-350..498 |
| Thiago | 19 | 115 | RAC-635 | RAC-499..632 |
| **TOTAL** | **53** | **361** | **4** | **408 tickets** |

## Data Files

- `data/_migration_data.json` — Extracted spreadsheet data (source of truth)
- `data/_infrastructure_ids.json` — Created label/project IDs
- `maps/_*_issue_map.json` — Row → Linear issue mapping per person
- `history/_history_ticket_*.md` — KPI reference ticket bodies

## Key Decisions (2026-03-18)

- Diego NOT migrated (already in Linear)
- CODA/GENERAL/Waki/Routine = Internal scope
- Customer labels for external clients only
- HockeyStack → Backlog without project
- Thiago QBO → same project as Alexandra (no overlap)
- Carlos has extra Product dimension (Demo/Sandbox labels)

## Date

Executed: 2026-03-18
