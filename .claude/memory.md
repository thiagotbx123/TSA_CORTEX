# Memory - Estado Persistente do Projeto TSA_CORTEX

> Este arquivo mantém o contexto entre sessões. Atualize ao final de cada sessão via `/consolidar`.

## Estado Atual

**Fase:** Producao (v2.0 - SOPs + Investigacao)
**Ultima Atualizacao:** 2026-01-26
**Status:** CLI coleta + Claude narra + SOPs documentados + CODA integrado
**Repo:** https://github.com/thiagotbx123/TSA_CORTEX

### Evolucao v2.0 (2026-01-26)

**Novo escopo do TSA_CORTEX - 3 pilares:**
1. **Worklog Automation** - Coleta e geracao (existente)
2. **Procedimentos Operacionais (SOPs)** - Documentacao padronizada (NOVO)
3. **Investigacao e Pesquisa** - Triangulacao de fontes (NOVO)

**Mudancas implementadas:**
- Credenciais CODA adicionadas ao `.env`
- Estrutura `knowledge-base/sops/` criada
- SOPs exemplo: `linear/criar-ticket.md`, `coda/atualizar-status.md`
- API docs: `api/coda.md`
- CLAUDE.md atualizado com novo escopo

**Pendente:**
- [ ] Implementar collector CODA em TypeScript
- [ ] Criar mais SOPs (comunicacao, investigacao)
- [ ] Testar integracao CODA via API

### Linear Auto-Assignment (2026-01-15)

**Melhoria no script de postagem:**
- Worklogs agora são criados automaticamente com:
  - **Project:** TSA's Worklog
  - **Assignee:** Usuário do .env (USER_DISPLAY_NAME)
  - **Team:** Raccoons (RAC)

**Script:** `output/post_worklog.js`

**Configuração via .env:**
```bash
USER_DISPLAY_NAME=Thiago Rodrigues  # Assignee automático
LINEAR_TEAM_KEY=RAC                  # Team (opcional)
LINEAR_PROJECT_NAME=TSA's Worklog    # Project (opcional)
```

**Worklogs criados:**
- RAC-19: Worklog 01-07 Jan (atualizado)
- RAC-36: Worklog 08-14 Jan (novo)

### ⚠️ REGRAS CRÍTICAS DO WORKLOG

| Regra | Valor | NUNCA fazer |
|-------|-------|-------------|
| **Idioma** | INGLÊS 100% | Português |
| **Pessoa** | Terceira pessoa | "Eu fiz...", "Trabalhei em..." |
| **Slack** | Apenas CONTEXTO | Citar mensagens diretamente |

**ANTES de gerar worklog, LER: `.claude/commands/worklog.md`**

### SpineHUB Python Integration (2026-01-08)

**Integração completa do SpineHUB Python no TSA_CORTEX:**

| Módulo | Python | TypeScript | Status |
|--------|--------|------------|--------|
| Bridge | bridge.py | python-bridge.ts | ✅ |
| Analyzers | code_analyzer.py | code-analyzer.ts | ✅ |
| Quality | benchmark.py | validator.ts | ✅ |
| Credentials | manager.py | manager.ts | ✅ |
| Templates | templates.py | templates.ts | ✅ |
| Utils | privacy, datetime | privacy, datetime, slack | ✅ |

**Novos Comandos CLI:**
```bash
tsa-cortex analyze [paths]     # Ruff, Bandit, Vulture, Radon
tsa-cortex validate <file>     # RAC-14 quality check
tsa-cortex credentials         # Credential status
tsa-cortex templates           # Linear templates
```

**Documentação:** `sessions/2026-01-08_spinehub_integration.md`

### RFC Reviews em Andamento (2026-01-06)

**RFC Category Definition:**
- Sugestão: "Product Readiness" como categoria
- Service model (TSA + DE) como moat diferencial
- Comentários preparados, aguardando post

**RFC Detailed Phases for Delivery:**
- Objetivo: Incorporar Data Engineering no processo
- Comentários inseridos no documento
- Cowork com Thais agendado para amanhã
- Principais mudanças: DE nos roles, stage gates com DE validation, escalation path

**Documentação:**
- `sessions/2026-01-06_19-00.md`
- `knowledge-base/learnings/2026-01-06_rfc_reviews.md`

### Mudança Crítica v1.1 (2025-12-24)

### Performance Excellence Framework v1 (2026-01-05)

**Novo artefato:** Sistema de feedback para TSAs baseado em Netflix, Spotify, Google.

**Arquivos:**
- `output/Performance_Excellence_v1.docx` - Doc executivo
- `output/Performance_Excellence_v1.xlsx` - Excel operacional (7 abas)
- `output/PERFORMANCE_EXCELLENCE_v1_EXECUTIVE.md` - Markdown completo

**Top 10 Behaviors (Q1):**
1. Clear Daily Update
2. Blocker + Ask + Follow-up
3. Ticket Ownership E2E
4. Evidence for Claims
5. Pattern Contribution
6. AI Usage (Analysis/Execution)
7. Data Quality Checklist
8. DE Gate Compliance
9. Escalation Timing
10. Learning Capture

**Ownership:** Thiago (1st) | Waki (2nd)
**Team:** Diego, Alexandra, Carlos, Gabrielle

**Documentação:** `knowledge-base/learnings/2026-01-05_performance_excellence_framework.md`


**ANTES (ruim):** CLI gerava narrativa via templates → output genérico
**AGORA (bom):** CLI só coleta dados → Claude gera narrativa de qualidade RAC-14

**Novo Fluxo:**
1. `node dist/cli/index.js collect --start X --end Y`
2. Gera `output/context_for_narrative.json`
3. Claude lê o arquivo e gera narrativa manualmente
4. Claude posta no Linear com aprovação

## Métricas de Coleta (última execução: 08-14 Jan 2026)

| Fonte | Eventos | MY_WORK | Status |
|-------|---------|---------|--------|
| Slack | 1051 | 494 | ✅ Search API (ownership) |
| Claude | 320 | - | ✅ Filtered |
| Drive | 158 | - | ✅ OAuth2 |
| Local | 75 | - | ✅ File scan |
| Linear | 2 | - | ✅ SDK |
| **Total** | **1606** | | |

### Métricas Anteriores (22-23 Dez 2025)

| Fonte | Eventos | MY_WORK | Status |
|-------|---------|---------|--------|
| Slack | 245 | 103 | ✅ Search API (ownership) |
| Linear | 12 | - | ✅ SDK |
| Drive | 101 | - | ✅ OAuth2 |
| Local | 58 | - | ✅ File scan |
| Claude | 69 | - | ✅ Filtered (was 816) |
| **Total** | **485** | | |

**Tickets criados:**
- RAC-2: https://linear.app/testbox/issue/RAC-2/weekly-update-thiago-rodrigues-2025-12-18
- RAC-11: Teste com narrative format
- RAC-12: https://linear.app/testbox/issue/RAC-12/worklog25-12-17-tsa-thiago-rodrigues (10-17 Dez)
- RAC-14: https://linear.app/testbox/issue/RAC-14/worklog25-12-23-tsa-thiago-rodrigues (22-23 Dez) **NARRATIVA COMPLETA**

## Pipeline de Execução (6 Steps)

```
Step 1: Collection     → Coleta de 5 fontes (Slack, Linear, Drive, Local, Claude)
Step 2: Normalization  → Remove duplicatas
Step 3: Clustering     → Agrupa por temas (11 clusters)
Step 3.5: SpineHub     → Consolida conteúdo real (NEW!)
Step 4: Generation     → Gera worklog narrativo
Step 5: Post           → Cria ticket no Linear
```

## Arquitetura Implementada

| Módulo | Status | Descrição |
|--------|--------|-----------|
| `types/` | ✅ | Tipos TypeScript |
| `utils/` | ✅ | Config, datetime, hash, privacy |
| `collectors/slack` | ✅ | Search API (xoxp- token) |
| `collectors/linear` | ✅ | Linear SDK |
| `collectors/drive` | ✅ | Google Drive API v3 |
| `collectors/local` | ✅ | Scan ~/Downloads, ~/Documents |
| `collectors/claude` | ✅ | Claude Code sessions |
| `normalizer/` | ✅ | Normalização de eventos |
| `clustering/` | ✅ | Agrupamento por keywords |
| `spinehub/` | ✅ | **Layer 3.5: Content Hub** |
| `worklog/narrative` | ✅ | **Narrative Renderer** |
| `linear/poster` | ✅ | Criação de tickets |
| `cli/` | ✅ | Interface CLI com 6 steps |

## Comandos Claude Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/worklog` | **PRINCIPAL** - Fluxo interativo de geração |
| `/status` | Visão geral do projeto |
| `/consolidar` | Fim de sessão - salva tudo |

### Fluxo do /worklog (OBRIGATÓRIO SEGUIR)

1. **Perguntar período** - NUNCA assumir datas
2. **Confirmar fontes** - Slack, Linear, Drive, Local, Claude
3. **Rodar coleta** - Mostrar progresso
4. **Montar worklog** - SpineHub + Narrative
5. **Apresentar resumo** - Preview ao usuário
6. **Pedir aprovação** - NUNCA criar ticket sem confirmação

## Credenciais Configuradas

| Serviço | Variáveis | Status |
|---------|-----------|--------|
| Slack | SLACK_USER_TOKEN (xoxp-), SLACK_USER_ID | ✅ |
| Linear | LINEAR_API_KEY | ✅ |
| Google | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN | ✅ |
| User | USER_DISPLAY_NAME = "Thiago Rodrigues" | ✅ |

## Decisões Importantes

| Data | Decisão | Contexto |
|------|---------|----------|
| 2025-12-22 | Slack Search API | User token (xoxp-) com search:read |
| 2025-12-22 | Coleta por canal completo | `in:#channel` ao invés de keywords |
| 2025-12-22 | USER_DISPLAY_NAME | Nome no título do ticket |
| 2025-12-23 | SpineHub Layer 3.5 | Consolida conteúdo ANTES da narrativa |
| 2025-12-23 | Narrative Renderer | Conta HISTÓRIA, não lista metadata |
| 2025-12-23 | Comando /worklog | Fluxo interativo obrigatório |
| 2025-12-23 | Repo público GitHub | Para compartilhar com outros TSAs |

## Aprendizados Chave (Session 2025-12-23)

### 1. SpineHub é Essencial
O problema era que o worklog listava arquivos e links, não contava a história.
SpineHub resolve isso consolidando o CONTEÚDO real antes de gerar a narrativa.

### 2. Fluxo Interativo é Obrigatório
NUNCA rodar worklog sem perguntar:
- Qual período?
- Quais fontes?
- Aprovar antes de criar ticket?

### 3. Secrets no Git
Scripts com credenciais hardcoded bloqueiam push no GitHub.
Solução: Usar variáveis de ambiente (.env) sempre.

### 4. Narrative vs Metadata
- **Errado:** "SOW_WFS_v2.docx modificado em 10/12"
- **Certo:** "Às 14:00, finalizei a versão 2 do SOW após feedback da Katherine"

## Aprendizados Chave (Session 2025-12-24)

### 5. CRÍTICO: Varrer TODOS os canais antes de gerar narrativa

**Problema detectado:** Narrativa gerada manualmente perdeu temas importantes:
- Gabrielle (67 msgs, 23 my_work) - GEM/Mailchimp - PERDIDO
- Diego (10 msgs, 9 my_work) - PERDIDO
- Lucas Soranzo (13 msgs, 5 my_work) - PERDIDO
- Kat + Alexandra (WFS onboarding) - PERDIDO inicialmente

**Root Cause:** Geração de narrativa baseada em primeiros matches, sem varrer dataset completo.

**CHECKLIST OBRIGATÓRIO antes de gerar narrativa:**
1. Listar TODOS os canais únicos no Slack
2. Ordenar por volume de my_work (desc)
3. Ignorar apenas bots (heytaco, google drive)
4. Gerar seção narrativa para CADA canal com my_work > 0
5. Validar: "Tem algum canal com my_work > 3 que não está na narrativa?"

**Script de validação:** `analyze-channels.js`

### 8. CRÍTICO: Slack = CONTEXTO, nunca citar diretamente

**REGRA ABSOLUTA:** Dados do Slack servem APENAS para:
- Interpretar CONTEXTO
- Identificar TEMAS de trabalho
- Analisar COM QUEM se trabalhou
- Inferir OUTCOMES

**NUNCA fazer:**
- ❌ Citar mensagens: "Thiago disse: 'posso te chamar?'"
- ❌ Reproduzir conversas
- ❌ Incluir quotes diretos do Slack

**SEMPRE fazer:**
- ✅ "Thiago coordenou com Gabrielle detalhes técnicos do projeto GEM"
- ✅ "Houve alinhamento pré-reunião com Alexandra sobre WFS"
- ✅ Descrever OUTCOMES, não conversas

### 9. Título dinâmico baseado no período

**Problema:** "Weekly Worklog" para período de 2 dias quebra confiança.

**Regra:**
- 1-6 dias → "Worklog"
- 7+ dias → "Weekly Worklog"

### 10. Contagens DEVEM reconciliar

**SEMPRE listar TODAS as fontes na tabela:**
```
| Slack | 245 events |
| Drive | 101 events |
| Claude | 69 events |
| Local | 58 events |
| Linear | 12 events |
| **Total** | **485 events** |
```

**Soma DEVE bater.** Se houver dedupe, adicionar linha explicando.

### 11. Artifacts com links inline

Cada seção temática deve ter seus **Artifacts** com links clicáveis:
```markdown
**Artifacts:**
- [Nome do arquivo](https://link) - Descrição
```

### 12. Estrutura final do Worklog

```markdown
# Worklog - {Owner Name}

| Field | Value |
|-------|-------|
| Period | {dates} |
| Owner | {name} |
| {source} | {count} events |
| **Total** | **{sum} events** |
| Generation Time | {time}s |

## Objective
{1 parágrafo descrevendo escopo}

### {Tema 1}
{Narrativa sem quotes de Slack}
**Artifacts:** {links}
**Outcome:** {resultado}

...

## References
{Tabela consolidada de todos os links}

---
*Generated by TSA_CORTEX v{version}*
```

### 6. Slack Collector - Ownership Classification
- DMs: `is:dm` → my_work se user enviou, context se recebeu
- Channels: `from:me -is:dm` → my_work
- Mentions: `<@userId> -is:dm` → mentioned
- Resultado: 245 eventos (103 my_work, 13 mentioned, 129 context)

### 7. Claude Collector - Noise Reduction
- Filtrar apenas `type: user` (não assistant, tool_use, snapshot)
- Ignorar projetos genéricos (system32, windows)
- Ignorar prompts curtos (c, y, n, ok)
- Resultado: 816 → 69 eventos (-92% ruído)

## Documentação

| Arquivo | Descrição |
|---------|-----------|
| CLAUDE.md | Instruções para Claude Code |
| .claude/commands/worklog.md | Fluxo do comando /worklog |
| .claude/memory.md | Este arquivo (estado persistente) |
| docs/ONBOARDING.md | Guia para novos usuários |
| docs/PROMPT_LAYERS_SPEC.md | Especificação das 5 camadas |

## Próximos Passos

1. ✅ Pipeline completo funcionando
2. ✅ SpineHub implementado
3. ✅ Narrative Renderer implementado
4. ✅ Comando /worklog definido
5. ✅ Repo público no GitHub
6. ✅ Documentação de onboarding
7. [ ] Amigo testar em outra máquina
8. [ ] Melhorar geração de narrative blocks
9. [ ] Adicionar mais contexto do Claude Code
10. [ ] Implementar testes unitários

---

**Instruções:** Sempre leia este arquivo no início de cada sessão.
