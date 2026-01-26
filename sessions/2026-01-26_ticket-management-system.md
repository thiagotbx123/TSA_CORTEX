# Sessao: Ticket Management System v1.0
**Data:** 2026-01-26
**Duracao:** ~3 horas
**Autor:** Thiago Rodrigues (via Claude)

---

## Objetivo da Sessao

Criar documentacao completa do **Ticket Management System** para a equipe TSA, cobrindo todo o ciclo de vida de tickets desde intake ate closeout.

---

## O Que Foi Feito

### 1. Discovery e Mapeamento
- Consultado Linear API para workflow states, labels e estrutura do time PLA
- Mapeado CODA workspace para integrar com Solutions Central
- Identificadas as paginas relevantes para publicacao

### 2. Documento Principal Criado
**Arquivo:** `knowledge-base/sops/ticket-management-system-coda.md`

**Estrutura final:**
- **A. The Flow** - End-to-end: Intake, Triage, Due Diligence, Ticket Creation, Execution, Monitoring, Validation, Delivery, Closeout
- **B. Critical Visibility Protocol** - Quando e como escalar
- **C. Who Does What** - RACI Matrix (TSA vs Engineering)
- **D. Linear Standard** - Prioridades (P0-P3), labels, DoR, DoD
- **E. Templates** - 10 templates (Bug, Feature, Spike, RCA, etc.)
- **Resources & Contacts** - Links rapidos e contatos

### 3. Snippets para CODA
Criados arquivos separados para copy/paste:
- `intro-recorte.md` - Overview profissional
- `raci-recorte.md` - Matriz RACI corrigida
- `resources-recorte.md` - Tabela de recursos

### 4. Refinamentos Aplicados
- **TSA Role:** Definido como bridge entre GTM/Customers e Engineering (Solutions Architect + Project Manager)
- **RACI Corrigido:** Apenas um Accountable por atividade
- **Tom:** Balanceado entre startup casual e profissional
- **Idioma:** Ingles para publicacao no CODA

---

## Decisoes Importantes

| Decisao | Contexto |
|---------|----------|
| TSA owns ate Refinement | Apos handoff, Engineering assume ownership |
| Critical Visibility Protocol | TSA deve escalar imediatamente blockers/criticos |
| RACI simplificado | Apenas TSA e Eng como colunas principais |
| 10 templates | Cobrem 95% dos casos de uso |
| P0-P3 priority system | Alinhado com Linear existente |

---

## Arquivos Criados/Modificados

| Arquivo | Status |
|---------|--------|
| `knowledge-base/sops/ticket-management-system.md` | Criado (PT-BR) |
| `knowledge-base/sops/ticket-management-system-en.md` | Criado (EN full) |
| `knowledge-base/sops/ticket-management-system-coda.md` | Criado (CODA-ready) |
| `knowledge-base/sops/intro-recorte.md` | Criado (snippet) |
| `knowledge-base/sops/raci-recorte.md` | Criado (snippet) |
| `knowledge-base/sops/resources-recorte.md` | Criado (snippet) |

---

## Publicacao

**CODA URL:** https://coda.io/d/Solutions-Central_djfymaxsTtA/Linear-Ticket-Management_sukx4jIV

**Nota:** CODA API v1 nao suporta edicao de canvas pages (apenas tables/rows), entao conteudo foi colado manualmente.

---

## Aprendizados

### 1. CODA API Limitacao
A API nao permite editar conteudo de paginas canvas - apenas criar/editar tabelas. Para documentacao textual, manual copy/paste e necessario.

### 2. RACI Validation
Sempre validar que existe apenas UM Accountable por linha. Multiplos R/A na mesma atividade causa confusao de ownership.

### 3. Tom de Documento
Startup tone pode ser casual mas precisa de estrutura clara. Balance entre "porque documentar depois nao funciona" e tabelas profissionais.

### 4. Snippets Approach
Criar arquivos MD separados para cada secao facilita copy/paste incremental no CODA.

---

## Proximos Passos

1. [ ] Criar templates detalhados no Linear (Bug, Feature, Spike, etc.)
2. [ ] Treinar equipe TSA no novo processo
3. [ ] Integrar CODA collector no TSA_CORTEX
4. [ ] Automatizar criacao de tickets via CLI

---

## Referencias

- Linear Team PLA: https://linear.app/testbox/team/PLA
- CODA Solutions Central: https://coda.io/d/_djfymaxsTtA
- Documento final: `knowledge-base/sops/ticket-management-system-coda.md`
