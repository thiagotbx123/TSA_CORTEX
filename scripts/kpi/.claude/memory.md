# KPI Dashboard — Estado Persistente

> Atualize este arquivo ao final de cada sessao via `/consolidar`.
> LEIA ESTE ARQUIVO INTEIRO antes de qualquer trabalho no projeto.

## Estado Atual

**Versao:** v3.2 (audit-hardened + UX improvements + audit engine verified)
**Ultima Atualizacao:** 2026-04-13
**Ultima Sessao:** 2026-04-13 (sessao longa, ~6h, muitas mudancas criticas)
**Status:** Pipeline funcional, dashboard HTML + XLSX, 5 membros ativos, 3 KPIs
**Membros ativos:** CARLOS, DIEGO, GABI, ALEXANDRA, THIAGO
**Membros REMOVIDOS:** Thais e Yasmim (excluidas do KPI por decisao do Thiago, 2026-04-09)

## Dados Atuais

| Arquivo | Ultima Atualizacao | Records |
|---------|-------------------|---------|
| `_kpi_all_members.json` | 2026-04-13 11:38 | 1177 issues (all teams) |
| `_dashboard_data.json` | 2026-04-13 11:38 | 719 records (591 linear + 128 spreadsheet) |
| `_kpi_data_complete.json` | 2026-03-18 | Sheets backlog CONGELADO |
| `_db_data.json` | congelado | DB_Data export |

## Infraestrutura (System Tray + ngrok)

### Desktop Icon
- **Atalho:** `C:\Users\adm_r\Desktop\KPI Dashboard.lnk`
- **Target:** `kpi_publish.bat` → lanca `kpi_tray.py` via `pythonw.exe`
- **Icon:** `kpi_dashboard.ico` (customizado)
- **WindowStyle:** Minimized (sem flash de CMD)
- **CUIDADO:** O bat DEVE apontar para `kpi_tray.py` (NAO `_tray_launcher.py` que nao existe)

### Tray Menu (kpi_tray.py)
```
Open Dashboard                    ← duplo-clique (abre ngrok URL)
Open Local                        ← abre localhost:8080
─────────────────
Refresh & Rebuild (Linear API)    ← pipeline completo (~35s)
Quick Rebuild (cached data)       ← so rebuild do cache (<1s)
─────────────────
Last refresh: HH:MM              ← timestamp dinamico
HTTP: OK  |  ngrok: OK           ← status ao vivo
─────────────────
Exit
```

### Notificacoes
- Windows toast notification apos cada pipeline (sucesso ou erro)
- Auto-refresh diario (09:00 weekdays) tambem notifica
- Pipeline runner centralizado em `_run_with_feedback()` — TODOS os caminhos passam por ele

### URLs e Portas
- **HTTP local:** `http://localhost:8080/KPI_DASHBOARD.html`
- **ngrok publico:** `https://uneffused-hoyt-unpunctually.ngrok-free.dev/KPI_DASHBOARD.html`
- **Auth ngrok:** `kpi:raccoons2026` (basic auth)
- **Serve dir:** `~/Downloads/kpi-serve/` (HTML copiado aqui apos cada build)
- **Auto-refresh:** weekdays 09:00 (full refresh com API)

---

## MUDANCAS CRITICAS DA SESSAO 2026-04-13 (LEIA COM ATENCAO)

### 1. REWORK DETECTION: AGORA LABEL-ONLY (FIX CRITICO)
- **Arquivo:** `merge_opossum_data.py`, linhas 479-483
- **Antes:** `has_rework = 'yes' if (has_rework_label or has_rework_history) else ''`
- **Agora:** `has_rework = 'yes' if has_rework_label else ''`
- **O que mudou:** Rework para KPI 3 agora depende EXCLUSIVAMENTE da label `rework:implementation` no Linear
- **Por que:** Deteccao por historico (Done → Todo/In Progress) gerava false positives. RAC-732 e RAC-710 da Alexandra foram flagados como rework mas eram apenas correcoes rapidas (Done → Todo em 5 minutos)
- **D.LIE20 history detection MANTIDA** para diagnostico: campo `reworkDetected` ainda e populado nos dados, mas NAO alimenta mais o campo `rework` que o dashboard usa
- **Verificacao pos-fix:** 5 tickets com rework=yes, TODOS com label `rework:implementation` confirmada via Linear API (RAC-738, TOU-1117, PLA-3395, PLA-3374, PLA-3266)

### 2. DEFAULT SEGMENT: CORRIGIDO DE 'External' PARA 'ALL' (BUG CRITICO DA AUDIT)
- **Arquivo:** `build_html_dashboard.py`, linha 703
- **Antes:** `let state={person:'ALL',category:'External',month:'ALL'};`
- **Agora:** `let state={person:'ALL',category:'ALL',month:'ALL'};`
- **Impacto:** Dashboard estava escondendo tickets Internal no load inicial — TODOS os KPIs eram calculados so com External por default
- **Encontrado por:** AUDIT_ENGINE (finding F37-1, CRITICAL)

### 3. Spreadsheet data excluida dos KPIs (2026-04-09)
- **Arquivo:** `build_html_dashboard.py`, funcao `getFiltered()` (~linha 708)
- **Fix:** `if(r.source==='spreadsheet')return false`
- **REGRA:** Spreadsheet = backlog historico CONGELADO. NUNCA deve impactar KPIs.

### 4. ETA Coverage corrigido (2026-04-13)
- **Arquivo:** `build_html_dashboard.py`, dentro de `renderMemberCards()`, bloco D.LIE12 (~linhas 1235-1241)
- **Fix:** Agora usa `RAW.filter(r=>r.source!=='spreadsheet'&&r.tsa===p)` com ACTIVE_STATUSES
- **REGRA:** ETA Coverage SEMPRE usa RAW (todos os tickets ativos da pessoa), nunca dados filtrados por semana

### 5. Scrum Copy → Scrum Panel (2026-04-09)
- Renomeado "Scrum Copy" para "Scrum Panel" no tab e heading
- Mostra TODOS os tickets (Internal + External) por TSA — sem filtro de category
- Filtra apenas por `source==='linear'` e `person`

### 6. Desktop icon corrigido (2026-04-13)
- `kpi_publish.bat` agora aponta para `kpi_tray.py` (era `_tray_launcher.py` que nao existe)
- Erro era SILENCIOSO (pythonw.exe nao mostra erros)

### 7. Tray menu melhorado (2026-04-13)
- Quick Rebuild (cached data) adicionado
- Windows toast notifications adicionadas (`_notify()`)
- `_run_with_feedback()` centraliza feedback visual
- `_last_refresh_label()` mostra timestamp dinamico no menu

### 8. CLAUDE.md corrigido (2026-04-13)
- Removido "7 dias = tolerancia On Time" → agora diz "Zero tolerancia On Time"
- A formula real e `delivery <= dueDate` (exato, sem buffer)

---

## AUDIT ENGINE — Resultado da Auditoria (2026-04-13)

9 perspectivas rodadas: A09, A11, A32, A35, A37, A07, A02, A13, A19

### Findings CORRIGIDOS nesta sessao
| ID | Sev | Descricao | Fix |
|----|-----|-----------|-----|
| F37-1 | CRITICAL | Default segment 'External' em vez de 'ALL' | Corrigido: linha 703 |
| F37-2 | HIGH | CLAUDE.md dizia "7 dias tolerancia" | Corrigido: zero tolerancia |
| Rework false positives | HIGH | RAC-732 e RAC-710 sem label | Corrigido: label-only detection |

### Findings PENDENTES (nao criticos, documentar para futuro)
| ID | Sev | Descricao | Acao sugerida |
|----|-----|-----------|---------------|
| F-A07-01 | CRITICAL | ngrok credentials hardcoded como fallback default | Mover para .env only |
| F-A07-02 | CRITICAL | ngrok URL hardcoded no source | Mover para .env only |
| F-A07-03 | HIGH | Python path hardcoded no .bat | Usar `py -3` launcher |
| F-A07-04 | HIGH | 17 Linear state IDs hardcoded | Mover para team_config.py |
| F-A13-01 | HIGH | Sem log persistente de pipeline runs | Criar pipeline_runs.jsonl |
| F-A13-02 | HIGH | HTML nao registra qual cache usou | Injetar metadata no build |
| F35-1 | MEDIUM | retroactiveEta so pega exact date match | Heuristica de proximidade |
| F35-2 | MEDIUM | Velocity fallback para dateAdd infla | Filtrar startedAt-only |
| F37-3 | MEDIUM | Playbook diz "In Progress past ETA = Late" mas code aplica a todos | Atualizar playbook |
| F-A02-01 | HIGH | `_notify()` swallows all exceptions | Logar failures |
| F-A02-02 | HIGH | `_kill_old_instance()` roda em import time | Mover para main |
| F-A02-05 | MEDIUM | auto_refresh_loop sem try/except | Envolver em try/except |

---

## Coda KPI Playbook

- **Pagina:** `https://coda.io/d/Solutions-Central_djfymaxsTtA/TSAs-KPI_suMS1NeD`
- **Script:** `push_to_coda.py` (converte MD → HTML e publica via API)
- **Source:** `KPI_PLAYBOOK_FOR_CODA.md` (versao 3.0 publicada 2026-04-13)
- **CUIDADO:** `PUT` com `insertionMode: 'replace'` APAGA conteudo manual (imagens coladas)
- **Estrategia:** Clear page → replace bulk → append tail sections
- **Document Info table:** Adicionada no topo com metadados (Owner, Version, etc.)
- **Emojis h2:** Customizados em `EMOJI_MAP` dentro de `push_to_coda.py`
- **Ultima publicacao:** 2026-04-13 (inclui todas as mudancas da sessao)

---

## Pipeline Status

| Step | Script | Status | Notas |
|------|--------|--------|-------|
| 1. Refresh | refresh_linear_cache.py | OK | ~30s, puxa 1177 issues (all teams) |
| 2. Merge | merge_opossum_data.py | OK | Label-only rework. Inclui TOU/PLA/CAP se assignee do time |
| 3. Normalize | normalize_data.py | OK | 527 perf recalculated, 86 history-improved |
| 4. Build HTML | build_html_dashboard.py | OK | ~990KB, self-contained, default segment=ALL |
| 5. Upload Drive | upload_dashboard_drive.py | OK | Google Drive auto |

---

## Armadilhas Conhecidas (LEIA ANTES DE MEXER)

1. **`_tray_launcher.py` NAO EXISTE** — o bat deve apontar para `kpi_tray.py`
2. **ETA Coverage usa RAW, nao getFiltered()** — e snapshot real-time
3. **Spreadsheet data excluida de getFiltered()** — `if(r.source==='spreadsheet')return false`
4. **Scrum Panel NAO filtra por category** — mostra Internal + External
5. **Rework detection e LABEL-ONLY** — `has_rework = 'yes' if has_rework_label else ''`
6. **D.LIE20 (history detection) e APENAS diagnostico** — `reworkDetected` populado mas NAO alimenta `rework`
7. **TOU/PLA/CAP tickets entram no dashboard** se assignee esta em PERSON_MAP
8. **STATE_NAMES tem 59 IDs desconhecidos** de outros times — nao afeta KPIs
9. **Cache staleness** — ETAs adicionadas no Linear so aparecem apos refresh
10. **Coda PUT replace** apaga conteudo manual — usar version history para recuperar
11. **pythonw.exe** engole erros silenciosamente — testar com `python.exe` para debug
12. **Default segment e 'ALL'** — NUNCA mudar de volta para 'External'
13. **Zero tolerancia On Time** — delivery <= dueDate (sem buffer de dias)
14. **ngrok credentials** hardcoded como fallback — mover para .env (pendente)

---

## Pendencias

- [ ] Ativar KPI 3 quando rework labels estiverem em uso generalizado no Linear
- [ ] Mover ngrok credentials para .env only (sem fallback hardcoded)
- [ ] Criar pipeline_runs.jsonl para logging persistente
- [ ] Mapear os 59 state IDs desconhecidos de outros times (cosmetic)
- [ ] Considerar refresh mais frequente (a cada 4h?) ou webhook do Linear
- [ ] Envolver auto_refresh_loop em try/except
- [ ] Mover _kill_old_instance() para dentro de main()

---

## Historico de Versoes

### v3.2 — UX + Data Fixes + Audit (2026-04-09 → 2026-04-13)
- **Rework detection: label-only** (merge_opossum_data.py, eliminados false positives)
- **Default segment: ALL** (era External — bug critico encontrado pela audit engine)
- Spreadsheet excluida dos KPIs (getFiltered)
- ETA Coverage corrigido (RAW em vez de getFiltered)
- Desktop icon corrigido (bat → kpi_tray.py)
- Tray menu: Quick Rebuild + notifications + timestamp
- Scrum Copy → Scrum Panel
- Coda KPI Playbook v3.0 publicado
- CLAUDE.md: "7 dias tolerancia" corrigido para "zero tolerancia"
- 9-perspective AUDIT_ENGINE rodada (2 CRITICAL + 6 HIGH + 11 MEDIUM + 2 LOW findings)
- 3 findings CRITICAL/HIGH corrigidos, 12 pendentes documentados

### v3 — Audit-Hardened (2026-03-18 → 2026-04-02)
- 20 auditors simulados, MEGA_AUDIT com findings
- 16 regras D.LIE implementadas (data integrity)
- Activity-based perf (deliveryDate from In Review)
- D.LIE23: Owner = original assignee em review
- D.LIE19: Parent tickets excluidos
- Gantt/Timeline tab
- normalize_data.py com 20+ fix categories
- Testes unitarios

### v2 — Linear Integration (2026-03-10 → 2026-03-17)
- Linear API + Sheets backlog
- refresh_linear_cache.py, merge_opossum_data.py
- team_config.py, orchestrate.py
- Upload Google Drive

### v1 — Sheets Only (2026-03-09)
- build_waki_dashboard.py (XLSX)
- Google Sheets source

---

## Sessoes

- **2026-04-13 (sessao longa):** Rework label-only fix, default segment ALL fix, AUDIT_ENGINE 9-perspective, Coda playbook v3.0, deep memory consolidation
- 2026-04-13 (inicio): Fix desktop icon, ETA Coverage, tray UX improvements
- 2026-04-09: Spreadsheet exclusion, Scrum Panel rename, RAC-732 investigation, Coda playbook
- 2026-04-02: v3 audit-hardened release
- 2026-03-18: Mega audit, D.LIE rules
- 2026-03-09: v1 initial delivery

---

## Contexto Tecnico Chave (para proxima sessao nao perder)

### Arquivos que foram MODIFICADOS na sessao 2026-04-13
| Arquivo | O que mudou |
|---------|-------------|
| `merge_opossum_data.py` | Rework: label-only (linha 479-483) |
| `build_html_dashboard.py` | Default segment ALL (linha 703), ETA Coverage RAW (1235-1241), spreadsheet exclusion (~708) |
| `CLAUDE.md` | Zero tolerancia On Time, v3.2 |
| `KPI_PLAYBOOK_FOR_CODA.md` | Versao 3.0 com todos os aprendizados |
| `kpi_tray.py` | Quick Rebuild, notifications, _run_with_feedback |
| `kpi_publish.bat` | Target corrigido para kpi_tray.py |
| `.claude/memory.md` | Este arquivo (consolidacao profunda) |

### Tickets Linear investigados na sessao
| Ticket | Resultado | Contexto |
|--------|-----------|----------|
| RAC-732 | False positive rework (Done→Todo em 5min) | Alexandra, corrigido com label-only |
| RAC-710 | False positive rework (Done→Todo em 5min) | Alexandra, corrigido com label-only |
| TOU-1119 | ETA adicionada pelo Thiago, cache estava stale | Gabi, resolvido com refresh |

### Transcricao desta sessao
- **ID:** e14031fc-1f52-444a-a122-7b86dcccce79
- **Local:** `C:\Users\adm_r\.cursor\projects\c-Users-adm-r/agent-transcripts/`
- Consultar se precisar de contexto detalhado sobre decisoes tomadas
