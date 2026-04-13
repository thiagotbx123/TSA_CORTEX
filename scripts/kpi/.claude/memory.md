# KPI Dashboard — Estado Persistente

> Atualize este arquivo ao final de cada sessao via `/consolidar`.
> LEIA ESTE ARQUIVO INTEIRO antes de qualquer trabalho no projeto.

## Estado Atual

**Versao:** v3.2 (audit-hardened + UX improvements)
**Ultima Atualizacao:** 2026-04-13
**Status:** Pipeline funcional, dashboard HTML + XLSX, 5 membros ativos, 3 KPIs
**Membros ativos:** CARLOS, DIEGO, GABI, ALEXANDRA, THIAGO
**Membros REMOVIDOS:** Thais e Yasmim (excluidas do KPI por decisao do Thiago, 2026-04-09)

## Dados Atuais

| Arquivo | Ultima Atualizacao | Records |
|---------|-------------------|---------|
| `_kpi_all_members.json` | 2026-04-13 10:10 | 1177 issues (all teams) |
| `_dashboard_data.json` | 2026-04-13 10:10 | 718 records (590 linear + 128 spreadsheet) |
| `_kpi_data_complete.json` | 2026-03-18 | Sheets backlog CONGELADO |
| `_db_data.json` | congelado | DB_Data export |

## Infraestrutura (System Tray + ngrok)

### Desktop Icon
- **Atalho:** `C:\Users\adm_r\Desktop\KPI Dashboard.lnk`
- **Target:** `kpi_publish.bat` → lanca `kpi_tray.py` via `pythonw.exe`
- **Icon:** `kpi_dashboard.ico` (customizado)
- **WindowStyle:** Minimized (sem flash de CMD)
- **CUIDADO:** O bat DEVE apontar para `kpi_tray.py` (NAO `_tray_launcher.py` que nao existe mais)

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

## Mudancas Criticas (Sessao 2026-04-09 → 2026-04-13)

### 1. Spreadsheet data excluida dos KPIs (2026-04-09)
- **Problema:** Dados do Google Sheets (backlog historico) estavam impactando calculos de KPI
- **Fix:** `getFiltered()` em `build_html_dashboard.py` agora exclui `r.source === 'spreadsheet'`
- **Scrum Panel:** Ja filtrava por `source==='linear'` — nao foi afetado
- **REGRA:** Spreadsheet = backlog historico CONGELADO. NUNCA deve impactar KPIs.

### 2. ETA Coverage corrigido (2026-04-13)
- **Problema:** Mostrava "—" para Carlos/Gabi porque usava `getFiltered()` (filtro de semana)
- **Causa raiz:** ETA Coverage e metrica de snapshot real-time, nao historica por semana
- **Fix:** Agora usa `RAW.filter(r=>r.source!=='spreadsheet'&&r.tsa===p)` em vez de `pr` (que vinha de `getFiltered()`)
- **Localizacao:** `build_html_dashboard.py`, dentro de `renderMemberCards()`, bloco D.LIE12
- **REGRA:** ETA Coverage SEMPRE usa RAW (todos os tickets ativos da pessoa), nunca dados filtrados por semana

### 3. Desktop icon corrigido (2026-04-13)
- **Problema:** `kpi_publish.bat` apontava para `_tray_launcher.py` (arquivo que nao existe)
- **Causa:** Arquivo foi renomeado/deletado em algum momento
- **Fix:** Bat agora aponta para `kpi_tray.py`
- **CUIDADO:** Erro era SILENCIOSO (pythonw.exe nao mostra erros)

### 4. Tray menu melhorado (2026-04-13)
- Adicionado "Quick Rebuild (cached data)" — rebuild rapido sem API call
- Adicionado "Last refresh: HH:MM" — timestamp visivel no menu
- Adicionado Windows toast notifications para feedback pos-pipeline
- Auto-refresh agora tambem mostra notificacao

### 5. Scrum Copy → Scrum Panel (2026-04-09)
- Renomeado "Scrum Copy" para "Scrum Panel" no tab e heading
- Mostra TODOS os tickets (Internal + External) por TSA — sem filtro de category
- Filtra apenas por `source==='linear'` e `person`

### 6. Rework detection false positive (2026-04-09)
- **Ticket:** RAC-732 flagado como rework sem label "Rework Implementation"
- **Causa:** D.LIE20 detecta rework automaticamente quando status transiciona Done → Todo/In Progress/Backlog
- **RAC-732:** Alexandra marcou Done, 5 min depois voltou pra Todo (correcao rapida, nao rework real)
- **STATUS:** Nao corrigido ainda. Duas opcoes propostas:
  1. Adicionar tolerancia de tempo (ex: >24h entre Done→Todo = rework)
  2. Exigir label "Rework Implementation" como unico trigger
- **Aguardando:** Decisao do Thiago sobre qual abordagem usar

## Coda KPI Playbook

- **Pagina:** `https://coda.io/d/Solutions-Central_djfymaxsTtA/TSAs-KPI_suMS1NeD`
- **Script:** `push_to_coda.py` (converte MD → HTML e publica via API)
- **Source:** `KPI_PLAYBOOK_FOR_CODA.md`
- **CUIDADO:** `PUT` com `insertionMode: 'replace'` APAGA conteudo manual (imagens coladas)
- **Estrategia:** Clear page → replace bulk → append tail sections
- **Document Info table:** Adicionada no topo com metadados (Owner, Version, etc.)
- **Emojis h2:** Customizados em `EMOJI_MAP` dentro de `push_to_coda.py`

## Pipeline Status

| Step | Script | Status | Notas |
|------|--------|--------|-------|
| 1. Refresh | refresh_linear_cache.py | OK | ~30s, puxa 1177 issues (all teams) |
| 2. Merge | merge_opossum_data.py | OK | Inclui TOU/PLA/CAP tickets se assignee e do time |
| 3. Normalize | normalize_data.py | OK | 527 perf recalculated, 86 history-improved |
| 4. Build HTML | build_html_dashboard.py | OK | ~989KB, self-contained |
| 5. Upload Drive | upload_dashboard_drive.py | OK | Google Drive auto |

## Armadilhas Conhecidas (LEIA ANTES DE MEXER)

1. **`_tray_launcher.py` NAO EXISTE** — o bat deve apontar para `kpi_tray.py`
2. **ETA Coverage usa RAW, nao getFiltered()** — e snapshot real-time
3. **Spreadsheet data excluida de getFiltered()** — `if(r.source==='spreadsheet')return false`
4. **Scrum Panel NAO filtra por category** — mostra Internal + External
5. **D.LIE20 detecta rework por transicao de status** — pode gerar false positives
6. **TOU/PLA/CAP tickets entram no dashboard** se assignee esta em PERSON_MAP
7. **STATE_NAMES tem 59 IDs desconhecidos** de outros times — nao afeta KPIs (status ja vem resolvido)
8. **Cache staleness** — ETAs adicionadas no Linear so aparecem apos refresh
9. **Coda PUT replace** apaga conteudo manual — usar version history para recuperar
10. **pythonw.exe** engole erros silenciosamente — testar com `python.exe` para debug

## Pendencias

- [ ] Decidir abordagem para rework false positives (tolerancia de tempo vs label obrigatoria)
- [ ] Ativar KPI 3 quando rework labels estiverem em uso no Linear
- [ ] Mapear os 59 state IDs desconhecidos de outros times (cosmetic, nao bloqueia)
- [ ] Considerar refresh mais frequente (a cada 4h?) ou webhook do Linear

## Historico de Versoes

### v3.2 — UX + Data Fixes (2026-04-09 → 2026-04-13)
- Spreadsheet excluida dos KPIs
- ETA Coverage corrigido (RAW em vez de getFiltered)
- Desktop icon corrigido (bat → kpi_tray.py)
- Tray menu: Quick Rebuild + notifications + timestamp
- Scrum Copy → Scrum Panel
- Coda KPI Playbook publicado
- Investigacao rework RAC-732

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

## Sessoes

- 2026-04-13: Fix desktop icon, ETA Coverage, tray UX improvements
- 2026-04-09: Spreadsheet exclusion, Scrum Panel rename, RAC-732 rework investigation, Coda playbook
- 2026-04-02: v3 audit-hardened release
- 2026-03-18: Mega audit, D.LIE rules
- 2026-03-09: v1 initial delivery
