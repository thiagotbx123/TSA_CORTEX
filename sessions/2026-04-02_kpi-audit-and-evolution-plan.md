# Sessao: 2026-04-02 — KPI Audit, Fixes & Evolution Plan

## Resumo
Full audit cycle do KPI pipeline: executou AUDIT_ENGINE v3.1 (37 auditors, 3 layers), aplicou todas as correcoes (2 rodadas), re-auditou com v3.2, e definiu roadmap de evolucao (items 1-4 para proxima sessao).

Score: **68/100 YELLOW → 82/100 GREEN** (+14 pontos)

## O Que Foi Feito (3 commits)

### Commit 1: `9b34c0a` — Audit Fixes Rodada 1
- **A30-003 CRITICAL**: Eliminado dual `calc_perf` — `_placeholder_perf` no merge, normalize e autoridade unica
- **A06-001 HIGH**: requirements.txt atualizado (pystray, Pillow, google-auth, google-auth-oauthlib)
- **A04-003 HIGH**: HTTP server bind → 127.0.0.1
- **A04-004 HIGH**: ngrok com --basic-auth
- **A01-002 HIGH**: Mapas consolidados em team_config.py (CUSTOMER_MAP, PROJECT_TO_CUSTOMER, etc)
- **A37-002 HIGH**: API cache mtime injetado no dashboard
- **A21-002 HIGH**: Filename unificado → KPI_DASHBOARD.html
- **A07-001 MEDIUM**: .env.example criado
- **A07-002 MEDIUM**: OUTPUT_DIR centralizado em team_config.py
- **A02-003 MEDIUM**: Retry com backoff no upload Drive
- **A13-002 MEDIUM**: Log rotation (RotatingFileHandler)
- **A01-004 LOW**: Bare except → excepcoes especificas
- **A03-004 LOW**: Perf label constants (PERF_ON_TIME, PERF_LATE, etc)

### Commit 2: `94b44bd` — Re-Audit Fixes (N01-N04 + Hot-fixes)
Hot-fixes (bugs da rodada 1):
- A37-002: JS banner agora mostra API_REFRESH (estava injetado mas nao usado)
- A13-002: RotatingFileHandler conectado ao stream (estava criado mas desconectado)

Novos findings corrigidos:
- **N01**: upload catch JSONDecodeError em non-JSON bodies
- **N02**: ngrok creds movidas para env vars (NGROK_BASIC_AUTH)
- **N03**: `_status_gate()` extraido em normalize (elimina duplicacao)
- **N04**: _LOG_DIR le KPI_OUTPUT_DIR do env

Cleanups: spike:None→Internal, dedup REAL_CUSTOMERS, unused import, docstrings

### Commit 3: `27492a4` — Tooltip Format
- "26-03 W.5" → "MAR - 2026 W5" em todos os 9 tooltips da heatmap
- `fmtWeekPretty()` + `MONTH_NAMES` uppercase

## Metricas da Sessao
- **Commits:** 3
- **Arquivos alterados:** 13 (10 Python + 1 .env.example + 2 audit reports)
- **Testes:** 88/88 PASS (sem regressoes)
- **Findings resolvidos:** 18 de 40 (45%)
- **Score:** 68 → 82 (+14)

## Estado Atual do Pipeline

### Arquivos-Chave
| Arquivo | Funcao |
|---------|--------|
| `team_config.py` | SSOT: person maps, customer maps, perf constants, OUTPUT_DIR |
| `merge_opossum_data.py` | Merge Linear cache → _dashboard_data.json (usa _placeholder_perf) |
| `normalize_data.py` | Autoridade unica para calc_perf + calc_perf_with_history |
| `build_html_dashboard.py` | Gera HTML (2838 lines — monolith, principal tech debt) |
| `upload_dashboard_drive.py` | Upload para Google Drive (retry + backoff) |
| `kpi_tray.py` | System tray: pipeline + HTTP + ngrok (127.0.0.1, auth, log rotation) |
| `orchestrate.py` | Orquestra pipeline completo |
| `_gen_audit_xlsx.py` | Gera Excel de audit (re-audit v3.2 data) |

### Findings Restantes (22)
- **2 HIGH**: A03-001 (monolith 2838 lines), A08-001 (6/8 untested)
- **12 MEDIUM**: module-level exec, admin-close, CI/CD, a11y, bus factor, ETA gaming, state validation, velocity, Python 3.14
- **8 LOW**: dead code variants/, dual HTTP servers, upload JSONDecodeError edge, ngrok creds in source, bracket strip, year repair

---

## PROXIMA SESSAO — Roadmap Items 1-4

### Item 1: Weekly Insights Automaticos
**Objetivo:** Gerar resumo semanal interpretativo dos dados (nao so dashboard visual)

**Spec:**
- Input: `_dashboard_data.json` (ja existe, ~200+ tickets com historico)
- Output: Markdown ou bloco de texto para colar no Slack
- Conteudo:
  - **Accuracy delta**: quem melhorou/piorou vs semana anterior (>10% change)
  - **Streak alerts**: alguem abaixo de 50% accuracy por 2+ semanas seguidas
  - **Late ticket spotlight**: tickets atualmente Late com ETA ja vencida (acao imediata)
  - **Retroactive ETA flag**: tickets onde alguem mudou ETA apos delivery (gaming indicator)
  - **Team summary**: overall accuracy, velocity, count by status

**Implementacao sugerida:**
```
scripts/kpi/weekly_insights.py
├── load _dashboard_data.json
├── filter CORE_WEEKS (ultimas 2 semanas)
├── calc per-person accuracy current vs previous week
├── detect streaks (2+ weeks < 50%)
├── list late tickets com action items
├── detect retroactiveEta flags
├── format output (markdown + optional Slack block kit)
└── save to ~/Downloads/WEEKLY_INSIGHTS_{date}.md
```

**Dados disponiveis no _dashboard_data.json por ticket:**
- `tsa` (pessoa), `week`, `perf` (On Time/Late/etc), `eta`, `delivery`, `status`
- `retroactiveEta` (boolean), `etaChanges` (count), `originalEta`, `finalEta`
- `deliveryDate`, `inReviewDate`, `startedAt`
- `customer`, `category` (External/Internal)

**Decisao pendente:** formato do output (puro Markdown vs Slack Block Kit vs ambos?)

---

### Item 2: Organic ETA Accuracy
**Objetivo:** Metrica que exclui tickets com ETA retroativa para mostrar accuracy "real"

**Spec:**
- Filtrar tickets onde `retroactiveEta === true` do calculo de accuracy
- Mostrar no dashboard lado a lado: "Total: 78%" vs "Organic: 65%"
- Per-person tambem: heatmap pode ter tooltip mostrando "Organic: X%"

**Implementacao sugerida:**
- Em `normalize_data.py`: adicionar campo `organicPerf` (copia de perf, mas N/A se retroactive)
- Em `build_html_dashboard.py`: JS calc separado para organic accuracy
- No tooltip: linha extra "Organic: X% (excl. N retroactive)"
- Na summary bar: segundo indicador

**Flag ja existe:** `retroactiveEta` e calculado em `merge_opossum_data.py` baseado em `etaChanges` e comparacao `originalEta` vs `finalEta`

**Decisao pendente:** threshold — o que conta como "retroactive"? Qualquer mudanca de ETA, ou so mudancas apos delivery date?

---

### Item 3: Trend Analysis / Health Cards
**Objetivo:** Para cada membro, calcular tendencia (melhorando/piorando/estavel) com base no historico

**Spec:**
- Janela: ultimas 4-8 semanas
- Metrica: accuracy rate por semana → slope da reta (regressao linear simples)
- Output: emoji/seta por pessoa (↑ improving, → stable, ↓ declining)
- Threshold: slope > +5%/semana = improving, < -5% = declining, else stable
- Bonus: projetar accuracy para proxima semana

**Implementacao sugerida:**
```
scripts/kpi/trend_analysis.py
├── load data, group by person + week
├── calc accuracy per (person, week) — ultimas 8 semanas
├── linear regression (numpy ou manual least-squares)
├── classify: improving / stable / declining
├── output: JSON com trends por pessoa
└── inject no dashboard como "health cards" ou badges
```

**Dados necessarios:** ja existem todos em _dashboard_data.json

**Decisao pendente:** incluir no dashboard HTML ou manter como report separado?

---

### Item 4: Export para PPT (Weekly Review Slides)
**Objetivo:** Gerar slides automaticamente para reuniao semanal do time

**Spec:**
- 3-4 slides:
  1. **Team Overview**: accuracy %, velocity, total tickets, period
  2. **Per-Person Heatmap**: screenshot ou tabela colorida com ultimas 4 semanas
  3. **Risk Board**: tickets Late + tickets sem ETA + streaks negativas
  4. **Highlights**: melhorias da semana, entregas notaveis

**Implementacao sugerida:**
```
scripts/kpi/weekly_ppt.py
├── uses python-pptx
├── load _dashboard_data.json
├── calc summaries (reusa logica de weekly_insights.py)
├── slide 1: summary stats em boxes coloridos
├── slide 2: tabela heatmap (verde/vermelho por celula)
├── slide 3: lista de riscos com status icons
├── slide 4: highlights text
└── save to ~/Downloads/KPI_WEEKLY_{date}.pptx
```

**Dependencia:** `python-pptx` (adicionar a requirements.txt)
**Reusa:** logica do Item 1 (weekly_insights) — implementar 1 primeiro, depois 4

---

## Ordem de Execucao Recomendada

```
Sessao N+1: Item 1 (Weekly Insights) — base de dados → insights acionaveis
Sessao N+1: Item 2 (Organic ETA) — aproveita momentum, ~30min
Sessao N+2: Item 3 (Trends) — depende de ter semanas de dados
Sessao N+2: Item 4 (PPT) — reusa Item 1, fecha o loop de comunicacao
```

## Decisoes Para Tomar Antes de Comecar

1. **Formato do Weekly Insights**: Markdown puro? Slack Block Kit? Ambos?
2. **Threshold retroactiveEta**: qualquer mudanca de ETA = retroactive, ou so pos-delivery?
3. **Trends no dashboard**: embutir no HTML ou report separado?
4. **PPT template**: usar template corporativo TestBox ou generico?

---

*Sessao consolidada em: 2026-04-02T23:59*
*Transcripts: [KPI Audit & Evolution](4edda6d5-52bc-4332-9cad-87b33abbc6d9)*
