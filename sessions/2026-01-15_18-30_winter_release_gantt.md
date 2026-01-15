# Sessao 2026-01-15 - Winter Release Gantt & Strategic Analysis

> **Data:** 2026-01-15
> **Projeto:** TSA_CORTEX + intuit-boom (cross-project)
> **Duracao:** ~2 horas

---

## Objetivo da Sessao

Apoiar Thiago na preparacao de deliverables e analise estrategica para o Winter Release FY26 do QuickBooks/Intuit.

---

## O Que Foi Feito

### 1. Analise Thread Slack - Winter Release Staging
- **Contexto:** Discussao entre Kat, Lucas Soranzo sobre staging environment
- **Pergunta chave:** Esforco para clonar TCO e Construction como staging
- **Resposta Lucas:** ~1 semana se forem contas prod (nao staging Intuit)
- **Alerta:** TCO tem configuracoes manuais que podem nao estar na integracao

### 2. Explicacao UAT Click Paths
- **O que e:** Roteiros passo-a-passo para testar features (clica aqui, depois aqui)
- **Quem usa:** Time TestBox, Intuit UAT, Sellers
- **Gap atual:** Sem owner para criar os roteiros das 29 features

### 3. Pesquisa Profunda - Releases QBO
Fontes consultadas:
- `strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md`
- `WINTER_RELEASE_CONTEXT_PACK.md`
- `IES_FEBRUARY_RELEASE_FY26_ANALISE_CRITICA.md`
- `features_rich.json` (35 features Fall Release)
- `features_winter.json` (29 features Winter Release)
- SpineHub entities

### 4. Criacao Gantt de Releases
Arquivo criado: `C:\Users\adm_r\Downloads\QBO_Releases_Gantt_v3.xlsx`

Releases mapeados:
| Release | Status | Timeline |
|---------|--------|----------|
| FALL RELEASE FY25 | Complete | Oct 01 - Nov 20, 2025 |
| WINTER RELEASE FY26 | In Progress | Jan 15 - Feb 25, 2026 |
| FEBRUARY RELEASE FY26 | Not Started | Mar 03 - Apr 07, 2026 |

Estrutura por release:
- Build tasks → GATE 1 → VALIDATE → GATE 2 → LAUNCH → Hypercare

### 5. Clarificacao Winter vs February Release
- **Winter Release:** Release oficial trimestral (29 features)
- **February Release:** Nome interno para doc de Conversational BI (parte do Winter)
- **Conclusao:** Sao relacionados, February e subset/extensao do Winter

### 6. Investigacao TSA_CORTEX e GOD_EXTRACT
- TSA_CORTEX: 5 collectors, SpineHub, patterns documentados
- GOD_EXTRACT: Document classification system
- Arquivo criado: `knowledge-base/learnings/2026-01-15_strategic_patterns_consolidation.md`

---

## Arquivos Criados/Modificados

| Arquivo | Acao |
|---------|------|
| `Downloads/QBO_Releases_Gantt_v3.xlsx` | Criado |
| `Downloads/QBO_Releases_Gantt_v2.xlsx` | Criado |
| `Downloads/QBO_Releases_Gantt.xlsx` | Criado |
| `TSA_CORTEX/knowledge-base/learnings/2026-01-15_strategic_patterns_consolidation.md` | Criado |
| `TSA_CORTEX/sessions/2026-01-15_18-30_winter_release_gantt.md` | Criado |

---

## Decisoes Tomadas

| Decisao | Contexto |
|---------|----------|
| Excluir WFS do Gantt | WFS nao esta lancado, foco em releases entregues |
| Usar colunas originais (CE, FDE, GTM) | Manter padrao do template |
| Separar February do Winter no Gantt | Clareza, mesmo sendo relacionados |

---

## Aprendizados

1. **UAT Click Paths** = roteiros de cliques para testar features
2. **Staging clone TCO** tem risco de configuracoes manuais
3. **Winter vs February Release** = February e subset do Winter
4. **Lucas Soranzo** pode estimar ~1 semana para ingestao de contas prod

---

## Proximos Passos

1. Validar Gantt com Kat
2. Decidir owner para UAT Click Paths
3. Acompanhar decisao do SteerCo sobre staging
4. Monitorar blockers TCO (PLA-2916, PLA-3013)

---

**Consolidado por:** Claude Code via /consolidar
