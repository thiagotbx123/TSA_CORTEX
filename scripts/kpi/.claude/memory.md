# KPI Dashboard — Estado Persistente

> Atualize este arquivo ao final de cada sessao via `/consolidar`.

## Estado Atual

**Versao:** v3 (audit-hardened)
**Ultima Atualizacao:** 2026-04-02
**Status:** Pipeline funcional, dashboard HTML + XLSX, 7 membros, 3 KPIs

## Dados Atuais

| Arquivo | Ultima Atualizacao | Records |
|---------|-------------------|---------|
| `_kpi_all_members.json` | 2026-04-02 09:36 | ~7MB (cache Linear) |
| `_dashboard_data.json` | 2026-04-02 09:12 | ~500 records merged |
| `_kpi_data_complete.json` | 2026-03-18 | Sheets backlog |
| `_opossum_raw.json` | 2026-03-26 | Opossum team |

## Historico de Evolucao

### v3 — Audit-Hardened (2026-03-18 → 2026-04-02)
- 20 auditors simulados, MEGA_AUDIT com findings
- 16 regras D.LIE implementadas (data integrity)
- Activity-based perf (deliveryDate from In Review, not just completedAt)
- D.LIE23: Owner = original assignee quando reassigned em In Review
- D.LIE19: Parent tickets excluidos (contam subtasks)
- Gantt/Timeline tab no dashboard
- Implementation timeline JSON
- normalize_data.py com 20+ fix categories
- Testes unitarios

### v2 — Linear Integration (2026-03-10 → 2026-03-17)
- Migrou de Sheets-only para Linear API + Sheets backlog
- refresh_linear_cache.py (fetch all 7 members, assignee + creator)
- merge_opossum_data.py (Opossum + Raccoons teams)
- team_config.py (single source of truth)
- Orchestrate.py (pipeline runner)
- Upload para Google Drive automatizado

### v1 — Sheets Only (2026-03-09)
- build_waki_dashboard.py (XLSX com 3 KPIs)
- Dados de Google Sheets (TSA_Tasks_Consolidate)
- 4 membros: Alexandra, Carlos, Gabi, Thiago
- Diego excluido (ja trackeado no Linear)

## Pipeline Status

| Step | Script | Status |
|------|--------|--------|
| 1. Refresh | refresh_linear_cache.py | OK (rodou hoje) |
| 2. Merge | merge_opossum_data.py | OK |
| 3. Normalize | normalize_data.py | OK |
| 4. Build HTML | build_html_dashboard.py | OK |
| 5. Upload Drive | upload_dashboard_drive.py | OK (opcional) |

## Issues Conhecidos

1. Thais: 79% issues sem dueDate → KPI1 baseado em 4 tasks apenas
2. Yasmim: 26% sem dueDate → borderline reliable
3. 13 outliers de datas no Sheets (2019, negativos) — left as-is
4. KPI 3 (Reliability) marcado NOT ACTIVE ate rework labels adotados

## Pendencias

- [ ] Thais: Setar dueDates nas 37 issues sem dueDate
- [ ] SOP para Opossum team: dueDate obrigatorio
- [ ] Migrar Sheets members para Linear-only (single source of truth)
- [ ] Revisar 13 outliers de duracao com o time
- [ ] Ativar KPI 3 quando rework labels estiverem em uso

## Sessoes Anteriores

As sessoes deste projeto estavam documentadas no TSA_CORTEX:
- `TSA_CORTEX/sessions/2026-03-09_kpi-delivery-tracker.md`
- Mega Audit: `TSA_CORTEX/scripts/kpi/MEGA_AUDIT_20_AUDITORS.md`
- Audit Report: `TSA_CORTEX/scripts/kpi/AUDIT_REPORT.md`
