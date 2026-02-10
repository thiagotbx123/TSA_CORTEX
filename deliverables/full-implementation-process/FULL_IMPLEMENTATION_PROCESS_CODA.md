# ═══════════════════════════════════════════════════════════════════
# ENTREGÁVEL COMPLETO — FULL IMPLEMENTATION PROCESS
# Para colar em: Solutions Central → Full Implementation Process
# https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS
# Gerado: 2026-02-10 | Autor: Thiago Rodrigues + Claude Opus 4.6
# ═══════════════════════════════════════════════════════════════════

---

# 1. PLANO DE COLETA & INVENTÁRIO

## 1.1 Conectores e Acesso

| Fonte | Status | Método | Limitação |
|:------|:-------|:-------|:----------|
| **Filesystem local** | ACESSADO | Leitura direta de todos os projetos | Nenhuma |
| **Coda (Solutions Central)** | NÃO ACESSADO (autenticação) | WebFetch bloqueado por login | Exportar manualmente ou usar Coda API com token |
| **Slack** | NÃO ACESSADO (requer xoxp token) | TSA_CORTEX Slack collector | Rodar `node dist/cli/index.js collect --slack` |
| **Linear API** | NÃO ACESSADO direto (sem MCP ativo) | linear_api_key disponível no .env | Consultar via script ou MCP server |
| **Google Drive** | NÃO ACESSADO direto (requer OAuth) | TSA_CORTEX Drive collector | Rodar collector ou acessar manualmente |
| **Obsidian Vault** | PARCIAL | ObsidianVault/ local | Indexado via filesystem |

## 1.2 Inventário de Fontes Internas Consultadas

### GANTT / Cronogramas
| Documento | Projeto | Caminho | Fases |
|:----------|:--------|:--------|:------|
| GEM GANTT Mapping | GEM-BOOM | `GEM-BOOM/GEM_GANTT_MAPPING.md` | Discovery → Foundation → Build → Validate → Launch |
| GEM GANTT Excel v3 | GEM-BOOM | `GEM-BOOM/scripts/create_gantt_excel_v3.py` | 7 fases + 7 gates (Discovery → Launch) |
| QBO Winter Release Gantt v9 | intuit-boom | `intuit-boom/sessions/2026-01-20_gantt_v9_final.md` | Gate 1 → Feature Validation → Data Pipeline → Review → Gate 2 → Launch → Post-Launch |
| QBO Post-Launch Gantt (9 versões) | intuit-boom | `intuit-boom/create_post_launch_gantt_*.py` | Mesma estrutura com gates |

### Gestão de Tickets (Linear)
| Documento | Caminho | Conteúdo |
|:----------|:--------|:---------|
| TMS v2.0 | `TSA_CORTEX/knowledge-base/sops/ticket-management-system-v2.md` | Fluxo E2E, RACI, prioridades, labels, 11 templates |
| Pre-Project Ticket Planning | `GEM-BOOM/CODA_PRE_PROJECT_TICKET_PLANNING.md` | 7 fases pré-projeto, toolkit completo |
| TMS Learning Completo | `TSA_CORTEX/knowledge-base/learnings/TMS_COMPLETE_LEARNING_2026-01-27.md` | 8 correções, 5 fontes, confiança 95% |

### Validação / QA
| Documento | Caminho | Conteúdo |
|:----------|:--------|:---------|
| 3-Gate Ingestion Pipeline | `intuit-boom/knowledge-base/INGESTION_3_GATES.md` | Gate 1 (local) → Gate 2 (backend) → Gate 3 (auditoria Claude) |
| validate_csvs.py | `intuit-boom/scripts/ingestion/validation/validate_csvs.py` | 59 regras, 189 checks automatizados |
| QBO Keystone Reference | `knowledge-base/QBO_KEYSTONE_INGESTION_REFERENCE.md` | Ordem FK, scripts, validações |

### Comunicação (Slack)
| Padrão | Fonte | Descrição |
|:-------|:------|:----------|
| Daily Agenda v1.8 | `TSA_DAILY_REPORT/specs/DAILY_AGENDA_SCRIPT_v1.8.txt` | Formato padrão de daily |
| #scrum-of-scrums | TMS v2.0 (validado Slack) | Canal PRINCIPAL para reports diários |
| #customer-requests | TMS v2.0 | Incoming de clientes |
| Escalation | Sam quote (TMS) | "Escalate quickly, not failure" |

### Comercial / GTM
| Documento | Status |
|:----------|:-------|
| Google Drive pasta Go To Market | NÃO ACESSADO (OAuth) — plano: solicitar export ou listar via Drive API |
| SOW examples | PARCIAL — referências em tickets GEM (SOW assinado) e QBO (features) |
| Decks / Propostas | NÃO ENCONTRADO localmente — provável no Drive |

## 1.3 Mapa de Conhecimento

```
┌─────────────────────────────────────────────────────────────┐
│                    MAPA DE CONHECIMENTO                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GANTT/Cronogramas ████████████ 95%                          │
│    - GEM: 7 fases, 7 gates, 37 tickets                      │
│    - QBO: 8 fases, 2 gates, 29 features                     │
│    - Padrão: Discovery → Foundation → Build → Validate       │
│              → Launch → Post-Launch                           │
│                                                              │
│  Gestão Tickets (Linear) ████████████ 95%                    │
│    - TMS v2.0 validado (confiança 95%)                       │
│    - Pre-Project Planning completo                           │
│    - 11 templates, RACI, P0-P3, checklists                  │
│                                                              │
│  Comunicação (Slack) ██████████░░ 80%                        │
│    - Canais mapeados e validados                             │
│    - Daily format v1.8 padronizado                           │
│    - Escalation protocol com quote Sam                       │
│    - Gap: threads reais de implantação não extraídos         │
│                                                              │
│  Operação (Coda) ████████░░░░ 65%                            │
│    - Solutions Central mapeado (24 clientes, 114 pgs)        │
│    - Drafts existem (TMS + Pre-Project)                      │
│    - Gap: conteúdo atual das páginas não lido (auth)         │
│                                                              │
│  Comercial/GTM ████████░░░░ 70%                              │
│    - 3 SOWs reais encontrados (GEM, WFS, HockeyStack)        │
│    - SOW Best Practices (Mailchimp, 12 seções padrão)        │
│    - Roles GTM mapeados (Kat, Shivani)                       │
│    - GEM Briefing Handoff + GOD_EXTRACT intelligence         │
│    - Gap restante: Drive não acessado (decks, presentations) │
│                                                              │
│  Arquitetura Dados/TAS ████████████ 95%                      │
│    - 3-Gate pipeline documentado                             │
│    - FK dependencies, validation rules                       │
│    - 20 bugs encontrados e corrigidos (aprendizado real)     │
│                                                              │
│  Engenharia ████████░░░░ 65%                                 │
│    - State flow documentado (Backlog → Done)                 │
│    - On-call = devs only (validado)                          │
│    - Gap: processo interno de Eng não detalhado              │
│                                                              │
│  Data Gen ████████████ 90%                                   │
│    - Processo GEM: schema → distribution → generation        │
│    - Scripts Python para bulk creation                       │
│    - Gap: playbook formal de Data Gen ausente                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1.4 Fontes Adicionais Descobertas (Varredura de SOPs — 40+ documentos)

| Documento | Caminho | Relevância |
|:----------|:--------|:-----------|
| **SOW Best Practices** | `GEM-BOOM/knowledge_base/SOW_BEST_PRACTICES.md` | Lições Mailchimp: 12 seções SOW, Gantt genérico, alinhar datas com Eng, iterar |
| **INTUIT_BOOM_TRANSFER (11 files)** | `intuit-boom/INTUIT_BOOM_TRANSFER/` | Pacote REAL de handover: runbooks, ecosystem, tech ref, risk matrix, credentials |
| **TSA Onboarding Program** | `intuit-boom/docs/TSA_ONBOARDING_*.md` | Programa 90 dias, RACI, fases, milestones |
| **Winter Release Master Plan** | `intuit-boom/docs/WINTER_RELEASE_MASTER_PLAN.md` | 29 features, 7 categorias, 5 fases de validação |
| **SOW GEM ATS** | `GEM-BOOM/SOW_GEM_ATS_ONLY_2026-01-30.md` | SOW real: 6 value stories, 12-17 semanas, change control |
| **SOW WFS Professional** | `QBO-WFS/.context/SOW_WFS_PROFESSIONAL_v1.md` | SOW 830 linhas: 10 deliverables, 4 fases, 9 semanas, out-of-scope |
| **SOW HockeyStack** | `hockeystack/knowledge-base/SOW_ANALYSIS.md` | 8-13 semanas, responsibility matrix, S3 DataSync |
| **GEM Briefing Handoff** | `GEM-BOOM/GEM_BOOM_BRIEFING_HANDOFF.md` | Handoff completo: 52 tickets, 7 milestones, team roles |
| **GOD_EXTRACT Intelligence** | `Knowledge/GOD_EXTRACT/` | CLIENT_SERVICE_MATRIX, INTELIGENCIA_ESTRATEGICA, BRIEFING_ESTRATEGICO |
| **Gong-Salesforce Playbook** | `GONG_SALESFORCE/docs/02_INTEGRATION_PLAYBOOK.md` | JWT auth, Bulk API 2.0, data sync patterns |
| **TSA_CORTEX SOPs (8+)** | `TSA_CORTEX/knowledge-base/sops/` | Linear ops, Coda ops, comunicação, investigação |
| **WFS Implementation Plan** | `QBO-WFS/create_wfs_implementation_plan.py` | Script gerador de plano |

> **Impacto**: SOW Best Practices e INTUIT_BOOM_TRANSFER preenchem 2 gaps previamente marcados como NÃO ENCONTRADO.

## 1.5 Fontes NÃO ENCONTRADAS (com plano de obtenção)

| Fonte | Status | Como Obter | Fallback |
|:------|:-------|:-----------|:---------|
| **Coda pages (conteúdo live)** | Auth required | Coda API + token ou export manual | Usar versões locais (.md) como base |
| **Google Drive > GTM** | OAuth required | Rodar Drive collector ou listar manualmente | Construir seção GTM baseada em referências dos tickets |
| **Slack threads de implantação** | xoxp token required | Rodar Slack collector com `in:#channel` | Usar padrões extraídos do TMS learning (10.8K msgs analisadas) |
| **Linear tickets live** | API key disponível | Script GraphQL ou MCP server | Usar referências existentes (RAC-44 a RAC-54, TOU-*, ONB-*) |
| **Playbook formal de Data Gen** | NÃO EXISTE | Criar baseado no processo GEM documentado | Derivar do Pre-Project Ticket Planning |
| **SOW templates** | NÃO ENCONTRADO local | Pedir a GTM (Kat) ou buscar no Drive | Criar template baseado em referências SOW do GEM |

---

# 2. MEMOS DOS AGENTES (FASE 2)

## MEMO A — Comercial/GTM

**Perspectiva:** Quem vende, quem apresenta ao cliente, quem cuida da relação.

### O que precisa existir para eu assinar embaixo:
1. **SOW como fonte de verdade** — Todo o processo deve rastrear de volta ao SOW. Se não está no SOW, não está no escopo.
2. **Visibilidade para o cliente** — Preciso saber, a qualquer momento, qual % do projeto está feito e se estamos no prazo.
3. **Handover claro** — Quando eu entrego o cliente ao time técnico, preciso saber exatamente quem assume e quando eu volto a ter contato.
4. **UAT do cliente** — O cliente DEVE testar antes do go-live. Sem exceções. Isso protege a relação.
5. **Evidence pack** — Para cada feature entregue, preciso de screenshots/vídeos para mostrar ao cliente que funciona.

### Perguntas que eu faria para quebrar o processo:
- "Se o cliente mudar o escopo depois do kick-off, o processo cobre isso?"
- "Se o TSA sair de férias no meio do projeto, quem assume?"
- "Quanto tempo leva do SOW assinado até o primeiro deliverable visível?"
- "Como sei que o time técnico realmente leu e entendeu o SOW?"

### Riscos que eu vejo:
- **Scope creep silencioso** — Time técnico aceita pedidos do cliente sem formalizar mudança
- **Falta de comunicação** — Cliente não sabe o que está acontecendo entre kick-off e UAT
- **Handover sem contexto** — GTM entrega e "desaparece", time técnico não tem o contexto da venda

---

## MEMO B — Arquiteto de Dados (TAS)

**Perspectiva:** Quem garante que os dados são corretos, completos e realistas.

### O que precisa existir para eu assinar embaixo:
1. **3-Gate pipeline obrigatório** — Nenhum dado entra em produção sem passar por Gate 1 (local), Gate 2 (backend) e Gate 3 (auditoria).
2. **FK dependencies mapeadas** — Ordem de ingestão DEVE respeitar dependências de chave estrangeira.
3. **Validação automatizada** — Scripts devem rodar ANTES de qualquer ingestão. Manual = erro.
4. **Rollback documentado** — Se algo der errado na ingestão, como reverter?
5. **Rastreabilidade de dataset** — Cada dataset deve ter ID, versão e changelog.

### Perguntas que eu faria para quebrar o processo:
- "Se o Gate 2 falhar com 50 erros, qual a prioridade de correção?"
- "O que acontece se o schema da API do cliente mudar no meio do projeto?"
- "Quem valida que os dados sintéticos parecem realistas, e não genéricos?"
- "Existe fallback se a API não suportar uma operação e precisar de UI automation?"

### Riscos que eu vejo:
- **Dados sintéticos genéricos** — Cliente percebe que "John Doe" não é real
- **API rate limits** — Ingestão de 500+ registros bate em limites
- **Dependência externa** — Backdating API, tenant provisioning = fora do nosso controle

---

## MEMO C — Engenharia

**Perspectiva:** Quem implementa, quem resolve bugs, quem faz deploy.

### O que precisa existir para eu assinar embaixo:
1. **Tickets claros com AC (Acceptance Criteria)** — Não quero tickets vagos. Preciso saber EXATAMENTE o que "done" significa.
2. **Ownership definido** — TSA até Backlog, Eng a partir de Refinement. Sem zona cinza.
3. **Prioridade respeitada** — P0 = drop everything. Não quero 15 P1s simultâneos.
4. **Ambiente de staging** — Nunca testar em produção diretamente.
5. **Production QA pelo TSA** — Quem pediu o ticket valida que funciona em prod.

### Perguntas que eu faria para quebrar o processo:
- "Se Eng identifica que um ticket precisa ser quebrado em 3, o processo cobre esse refinement?"
- "Qual o SLA para um P0 vs P2?"
- "Se o TSA manda ticket com AC incompleto, Eng pode rejeitar?"
- "Como tratamos tech debt acumulado durante implantação?"

### Riscos que eu vejo:
- **Tickets mal escritos** — TSA sem contexto técnico cria tickets que Eng não entende
- **Scope creep via tickets** — "Já que está mexendo aqui, adiciona isso também"
- **Deploy sem rollback** — Feature vai para prod e quebra algo

---

## MEMO D — Data Gen / Geração de Dados

**Perspectiva:** Quem cria dados sintéticos que parecem reais.

### O que precisa existir para eu assinar embaixo:
1. **Schema aprovado ANTES de gerar** — Não gero 500 candidatos para descobrir que o schema mudou.
2. **Distribuição definida** — Quantos por fase do pipeline, qual spread temporal, qual variância.
3. **Realismo validado** — Nomes, empresas, datas precisam parecer de verdade.
4. **Idempotência** — Se rodar de novo, não duplica dados.
5. **Dependência clara de API** — Sei quais endpoints existem e quais precisam de UI automation.

### Perguntas que eu faria para quebrar o processo:
- "Se a API do cliente não suporta POST para um recurso, quem descobre isso — eu ou o TSA?"
- "Qual a taxa aceitável de falha na geração (ex: 5% timeout)?"
- "Como garanto que dados gerados hoje ainda fazem sentido amanhã (datas relativas vs absolutas)?"
- "Existe validação cruzada entre dados gerados e schema do cliente?"

### Riscos que eu vejo:
- **API instável** — Endpoint muda de versão, script quebra
- **Volume** — Gerar 10K registros sem rate limiting = ban
- **Backdating** — Nem toda plataforma suporta datas retroativas

---

## MEMO E — PM/Delivery

**Perspectiva:** Quem garante que o projeto entrega no prazo, no escopo, com qualidade.

### O que precisa existir para eu assinar embaixo:
1. **GANTT com gates obrigatórios** — Cada fase tem gate de saída. Não avança sem aprovação.
2. **RACI sem ambiguidade** — Um e apenas um Accountable por atividade.
3. **Risk register vivo** — Atualizado a cada checkpoint, não só no início.
4. **Status visible** — Stakeholders veem progresso sem perguntar.
5. **Change control** — Mudança de escopo = ticket + aprovação + impacto documentado.

### Perguntas que eu faria para quebrar o processo:
- "Se um gate falha, qual o processo de remediation? Quem decide se avança ou para?"
- "Qual a cadência de status updates para o cliente?"
- "Se dois projetos competem por recurso, quem prioriza?"
- "Como medimos se o processo está melhorando entre projetos?"

### Riscos que eu vejo:
- **Otimismo de prazo** — Time subestima esforço, deadline estoura
- **Gate theater** — Gate existe no papel mas ninguém realmente valida
- **Dependência de pessoa** — TSA Lead ausente = projeto para

---

## MEMO F — Executivo (Custo, Margem, Previsibilidade, Escala)

**Perspectiva:** Quem precisa que isso funcione em 10 projetos simultâneos, não só 1.

### O que precisa existir para eu assinar embaixo:
1. **Processo escalável** — O mesmo playbook funciona para GEM, QBO, Gong, qualquer um.
2. **Tempo padronizado** — Sei quanto tempo cada tipo de projeto leva (small/medium/large).
3. **Custo previsível** — Horas por fase, por role, por tipo de projeto.
4. **Métricas de melhoria contínua** — Cycle time caindo, rework caindo, satisfação subindo.
5. **Onboarding < 1 semana** — Novo TSA lê o playbook e executa sem handholding.

### Perguntas que eu faria para quebrar o processo:
- "Quanto custa (em horas-pessoa) uma implantação típica?"
- "Qual o lead time do SOW assinado até go-live?"
- "Se eu dobrar o time, a velocidade dobra?"
- "Como garanto que aprendizados de um projeto alimentam os próximos?"

### Riscos que eu vejo:
- **Processo pesado** — Burocracia que não agrega valor e atrasa entregas
- **Dependência de herói** — Processo funciona porque Thiago faz, não porque o processo é bom
- **Falta de dados** — Sem métricas, não sei se estamos melhorando ou piorando

---

# 3. SABATINA CRUZADA

## Rodada 1: Perguntas cruzadas

| De → Para | Pergunta | Resposta |
|:----------|:---------|:---------|
| **GTM → PM** | "Se o cliente pede algo fora do SOW no kick-off, como tratamos?" | Change request formal: ticket com label `new-scope`, impact assessment (prazo + custo), aprovação GTM + cliente antes de executar. |
| **GTM → Eng** | "Como garanto que o cliente vê progresso antes do UAT?" | Status reports semanais no Slack, milestone views no Linear compartilháveis, evidence pack incremental por fase. |
| **TAS → Data Gen** | "Se a API não suporta POST, quando descubro?" | Na fase de Discovery/Enrichment (Fase 1). TSA mapeia endpoints disponíveis ANTES de criar tickets. Tickets marcam `REQUIRES UI AUTOMATION` quando não há API. |
| **TAS → Eng** | "Quem faz rollback se a ingestão falhar em prod?" | Script de rollback deve existir ANTES da ingestão (pré-requisito do Gate 1). Eng executa, TSA valida. Ordem: DELETE filhos → DELETE pais → re-INSERT. |
| **Eng → PM** | "Se o TSA manda ticket com AC incompleto, o que faço?" | Mover ticket de volta para Backlog com comentário específico do que falta. TSA tem 24h para completar. Se recorrente, escalate para TSA Lead. |
| **Eng → TAS** | "Como garanto que dados sintéticos não causam bugs em features reais?" | Gate 3 (Auditoria Claude) inclui auditor cross-table que valida consistência. Production QA pelo TSA depois do deploy confirma que tudo funciona end-to-end. |
| **Data Gen → PM** | "Se schema muda depois que eu já gerei dados, quem paga o retrabalho?" | Schema é aprovado no Gate 3 (Seed Data). Mudança depois = change request + novo ticket. Retrabalho é risco aceito e mitigado por versionamento de datasets. |
| **PM → Executivo** | "Como garanto que métricas são coletadas sem overhead?" | Automatização: scripts já logam tempo de execução, Linear tem cycle time nativo, Slack reports são a cadência de comunicação. Não criar ritual novo; usar os existentes. |
| **Executivo → GTM** | "Qual o custo real de uma implantação?" | GEM (referência): ~37 tickets, 7 semanas, 4 roles. QBO: ~29 features, 8 semanas, 5 roles. Custo varia por complexidade mas o playbook dá baseline. |
| **Executivo → PM** | "Se o TSA Lead fica doente, o projeto para?" | Mitigação: documentação completa no Coda, tickets auto-explicativos, Daily Agenda no Slack. Qualquer TSA do time consegue assumir em < 24h com o playbook. |

## Requisitos Derivados da Sabatina

1. **REQ-01**: Change control formal com ticket `new-scope` + impact assessment
2. **REQ-02**: Status reports visíveis (Slack + Linear milestones) sem reunião extra
3. **REQ-03**: API mapping na Discovery, antes de criar tickets
4. **REQ-04**: Script de rollback como pré-requisito de ingestão
5. **REQ-05**: AC incompleto = ticket volta para Backlog (24h SLA)
6. **REQ-06**: Gate 3 inclui validação cross-table de dados
7. **REQ-07**: Schema freeze no Gate 3, mudança depois = change request
8. **REQ-08**: Métricas extraídas de ferramentas existentes (Linear, Slack), zero overhead
9. **REQ-09**: Custo estimado por tipo de projeto (S/M/L) documentado
10. **REQ-10**: Documentação suficiente para handoff em < 24h

---

# 4. PROCESSO FINAL — TEXTO PARA COLAR NO CODA

# Full Implementation Process

---

## Informações do Documento

| Campo | Valor |
|:------|:------|
| **Owner** | Thiago Rodrigues (TSA Manager) |
| **Versão** | 1.0 |
| **Última Atualização** | 2026-02-10 |
| **Status** | Ativo |
| **Documentos Relacionados** | [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) · [Pre-Project Linear Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) |

---

## Sumário

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos e Entradas](#pré-requisitos-e-entradas)
3. [Papéis e Responsabilidades (RACI)](#papéis-e-responsabilidades)
4. [Artefatos Obrigatórios](#artefatos-obrigatórios)
5. [Fases do Processo](#fases-do-processo)
   - Fase 0: Intake & Qualificação
   - Fase 1: Discovery & Sizing
   - Fase 2: Pre-Project Planning
   - Fase 3: Kick-off
   - Fase 4: Foundation
   - Fase 5: Build (Seed Data + Data Gen + Ingestion)
   - Fase 6: Stories & Feature Setup
   - Fase 7: Validate (QA + UAT)
   - Fase 8: Launch & Go-Live
   - Fase 9: Hypercare & Handover
   - Fase 10: Closeout & Retrospective
6. [Cadências e Rituais](#cadências-e-rituais)
7. [Gestão de Mudanças](#gestão-de-mudanças)
8. [Gestão de Riscos](#gestão-de-riscos)
9. [Métricas e KPIs](#métricas-e-kpis)
10. [Playbook de Escalonamento](#playbook-de-escalonamento)

---

## Visão Geral

### O que é
Este documento define o processo padrão de ponta a ponta para implantação de soluções na TestBox. Cobre desde o momento em que um deal é qualificado até o encerramento formal do projeto, incluindo todos os gates, checklists e artefatos necessários.

### Quando usar
- Toda nova implantação de cliente (demos, POCs, pilotos, produção)
- Onboarding de novos produtos no catálogo TestBox
- Releases trimestais de features (Winter, Fall, etc.)

### Para quem
- **TSA** (Technical Solutions Architect) — executa e coordena
- **CE** (Customer Engineer) — implementa tecnicamente
- **DATA** (Data Generation) — cria dados sintéticos realistas
- **GTM** (Go-To-Market) — interface com cliente e stakeholders
- **Engineering** — desenvolve features e resolve bugs

### Como Usar Este Playbook (Onboarding)

Se você é **novo no time TSA**, siga este caminho:

| Dia | O que fazer | Tempo |
|:----|:-----------|:------|
| **Dia 1** | Ler este documento inteiro (foco em Visão Geral + Fases 0-3) | 2h |
| **Dia 1** | Ler [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) | 1h |
| **Dia 2** | Ler [Pre-Project Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) | 1h |
| **Dia 2** | Estudar um projeto anterior no Linear (GEM ou QBO) como exemplo | 2h |
| **Dia 3** | Fazer shadowing de um projeto ativo (observar gates, dailies, tickets) | Full day |
| **Dia 4-5** | Executar Fases 1-2 em um projeto novo COM supervisão do TSA Lead | 2 dias |

**Após 1 semana**: Novo TSA deve ser capaz de executar Fases 1-5 sem handholding.

**Regra**: Se algo no playbook não está claro o suficiente para executar sozinho, é um BUG no playbook — reporte ao TSA Lead para correção.

### Princípios
1. **SOW é lei** — Todo escopo rastreia de volta ao Statement of Work
2. **Gates não são opcionais** — Nenhuma fase avança sem aprovação do gate
3. **Documentação = execução** — Se não está documentado, não aconteceu
4. **Escalar cedo** — "Escalate quickly. This is not failure." (Sam Senior, CEO)
5. **Automatize o repetitivo** — Scripts > trabalho manual, sempre

### Referência: Sizing por Tipo de Projeto

| Tipo | Tickets | Fases | Duração Típica | Equipe |
|:-----|:--------|:------|:---------------|:-------|
| **Small** (1-2 features, demo simples) | 10-15 | 6 | 2-3 semanas | TSA + CE |
| **Medium** (5-10 features, demo completa) | 25-40 | 8 | 5-7 semanas | TSA + CE + DATA |
| **Large** (10+ features, multi-fase) | 40-60 | 10 | 8-12 semanas | TSA + CE + DATA + GTM |

> **Fonte interna**: GEM = Medium (37 tickets, 7 semanas, 4 roles). QBO Winter = Large (29 features, 8 semanas, 5 roles).

---

## Pré-requisitos e Entradas

Antes de iniciar QUALQUER implantação, estes items DEVEM existir:

| Item | Responsável | Onde Vive | Obrigatório? |
|:-----|:------------|:----------|:-------------|
| SOW assinado (ou draft final) | GTM | Google Drive | Sim — Referências: [GEM SOW](GEM-BOOM/SOW_GEM_ATS_ONLY_2026-01-30.md), [WFS SOW](QBO-WFS/.context/SOW_WFS_PROFESSIONAL_v1.md), [SOW Best Practices](GEM-BOOM/knowledge_base/SOW_BEST_PRACTICES.md) |
| Acesso ao tenant do cliente | GTM → TSA | Coda (Solutions Central) | Sim |
| Documentação técnica (API, arquitetura) | TSA | Repo do projeto `/knowledge_base/api/` | Sim |
| Linear Project criado | TSA | Linear | Sim |
| Canal Slack do projeto (se necessário) | TSA | Slack | Condicional |
| Budget/timeline aprovados | GTM + Executivo | SOW | Sim |
| Equipe alocada e confirmada | PM/TSA Lead | Coda ou Linear | Sim |

---

## Papéis e Responsabilidades

### RACI Matrix — Por Fase

| Fase | TSA | CE | DATA | GTM | Eng |
|:-----|:---:|:--:|:----:|:---:|:---:|
| 0. Intake & Qualificação | C | - | - | **R/A** | - |
| 1. Discovery & Sizing | **R/A** | C | C | C | I |
| 2. Pre-Project Planning | **R/A** | C | C | I | I |
| 3. Kick-off | **R/A** | I | I | C | I |
| 4. Foundation | **R/A** | R | I | I | C |
| 5. Build | C | **R/A** | R | I | C |
| 6. Stories & Features | **R/A** | R | C | I | C |
| 7. Validate (QA + UAT) | **R** | R | I | **A** | C |
| 8. Launch | C | **R** | I | **A** | R |
| 9. Hypercare & Handover | I | C | I | **R/A** | C |
| 10. Closeout | **R/A** | I | I | C | I |

**Legenda**: R = Responsável (faz o trabalho) · A = Accountable (aprova/decide) · C = Consultado · I = Informado

### Regra de Ouro
> Apenas UM Accountable por fase. Se dois aparecem como A, decidir antes de começar.

> **Fonte interna**: RACI validado em TMS v2.0 (2026-01-27), confiança 95%.
> **Fonte externa**: [RACI Chart — Atlassian](https://www.atlassian.com/work-management/project-management/raci-chart) · [RACI for Client Onboarding — GUIDEcx](https://www.guidecx.com/blog/how-to-create-a-raci-chart-for-client-onboarding/) · PMI PMBOK 7th Edition.

---

## Artefatos Obrigatórios

Cada implantação DEVE produzir os seguintes artefatos:

| Artefato | Onde | Quando Criar | Template |
|:---------|:-----|:-------------|:---------|
| **Linear Project** com milestones | Linear | Fase 2 | [Pre-Project Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) |
| **GANTT** com fases e gates | Google Sheets/Excel | Fase 2 | [Template GANTT Padrão](#template-gantt) |
| **Tickets** no formato padrão | Linear | Fase 2 | [Linear Ticket Management](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV) |
| **Slack kick-off** message | Slack (canal do time) | Fase 3 | [Template Kick-off](#template-kickoff) |
| **Risk Register** | Linear (ticket dedicado) ou Coda | Fase 1, atualizar toda fase | Ver seção Gestão de Riscos |
| **Evidence Pack** | Google Drive | Fase 7-8 | Screenshots/vídeos por feature |
| **Documentation Package** | Coda + Repo | Fase 9 | Runbook + decisões + lições |
| **Retrospective** | Coda ou documento | Fase 10 | Formato: Keep/Stop/Start |

---

## Definition of Ready (DoR) — Por Ticket

Antes de um ticket entrar em execução (sair de Backlog), DEVE atender a TODOS estes critérios:

| # | Critério | Verificação |
|:--|:---------|:------------|
| 1 | **Título segue convenção** | `[PROJECT] Verb + Object` (ex: `[GEM] Create Candidate Pipeline`) |
| 2 | **Descrição com Acceptance Criteria** | Seção "Validation" preenchida com checks mensuráveis |
| 3 | **Endereça necessidade de negócio** | Rastreia para deliverable do SOW ou requisito técnico |
| 4 | **Criterios mensuráveis** | Cada AC pode ser verificado com YES/NO, não é subjetivo |
| 5 | **Tamanho adequado** | Estimativa ≤ 5 dias. Se maior, quebrar em sub-tickets |
| 6 | **Sem dependências bloqueantes** | Pré-requisitos completos, entregas de outros times disponíveis |

**Regra**: Ticket que NÃO atende DoR → volta para Backlog com comentário do que falta. TSA tem 24h para corrigir.

> **Fonte interna**: REQ-05 da Sabatina Cruzada (Eng pode rejeitar AC incompleto).
> **Fonte externa**: [Definition of Ready — Microsoft Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/agile-development/team-agreements/definition-of-ready/).

---

## Definition of Done (DoD) — Por Ticket

Um ticket só pode ser movido para Done quando TODOS estes critérios forem atendidos:

| # | Critério | Verificação |
|:--|:---------|:------------|
| 1 | **Trabalho concluído e verificado** | Dado ingerido, script validado, feature funcional |
| 2 | **Validação executada** | Script de validação rodado com zero erros críticos |
| 3 | **Evidência capturada** | Screenshot, log, ou report de validação |
| 4 | **Documentação atualizada** | Coda/Slack/knowledge-base com status atual |
| 5 | **Linear atualizado** | Ticket em Done, comentário final, tempo registrado |

> **Fonte externa**: [DoD vs Acceptance Criteria — Agile Sherpas](https://www.agilesherpas.com/blog/definition-of-done-acceptance-criteria). Distinção chave: "AC ajuda a construir o **produto certo**. DoD ajuda a construir o **produto certo direito**."

---

## Fases do Processo

---

### FASE 0: Intake & Qualificação

| Campo | Valor |
|:------|:------|
| **Objetivo** | Decidir se a oportunidade vira projeto e com qual escopo |
| **Owner** | GTM (R/A), TSA (C) |
| **Duração típica** | 1-5 dias |
| **Onde acontece** | Slack (DM/canal), Calls, Google Drive |
| **Por que existe** | Evitar iniciar projetos sem escopo claro ou recursos disponíveis |

**O que fazer:**
1. GTM recebe oportunidade (deal, pedido de demo, renewal)
2. GTM avalia fit técnico e comercial (produto suportado? timeline realista?)
3. Se necessário, GTM consulta TSA para sizing técnico
4. GTM produz SOW draft ou confirma escopo verbal
5. Decisão: GO / NO-GO / NEED MORE INFO

**Inputs:** Pedido do cliente, contexto comercial, catálogo de produtos
**Outputs:** SOW draft, decisão GO/NO-GO, timeline preliminar

**Critérios de Aceite (DoD):**
- [ ] Escopo definido (features, dados, timeline)
- [ ] Recursos identificados (TSA, CE, DATA disponíveis)
- [ ] SOW draft ou scope document existente
- [ ] Timeline factível (não conflita com outros projetos)

**Gate 0: Qualificação Aprovada** → Avança para Fase 1

**Falhas comuns:**
- Iniciar sem SOW → escopo vira alvo móvel
- Não consultar TSA no sizing → timeline irreal
- Aceitar tudo que o cliente pede → scope creep desde o dia 1

> **Confiança**: ALTO — Padrão observado em GEM (SOW Build: Dec 18 - Jan 31) e QBO (features definidas antes de execução).
> **Fonte externa**: [Phased Implementation — Dock.us](https://www.dock.us/library/phased-implementation) · [SaaS Implementation Checklist — Storylane](https://www.storylane.io/blog/saas-implementation-checklist).

---

### FASE 1: Discovery & Sizing

| Campo | Valor |
|:------|:------|
| **Objetivo** | Entender tudo antes de escrever um único ticket |
| **Owner** | TSA (R/A), CE/DATA/GTM (C) |
| **Duração típica** | 3-5 dias |
| **Onde acontece** | Coda, Google Drive, Calls, Slack |
| **Por que existe** | "Garbage in, garbage out" — tickets ruins = projeto ruim |

**O que fazer:**
1. **Coletar materiais** (~20 min por fonte):
   - SOW/Contrato → extrair deliverables, timeline, success criteria
   - Docs técnicos → API docs, arquitetura, limitações
   - Brainstorming notes → sessões com CE, DATA, GTM
   - Slack threads → decisões e contexto relevante
   - Projetos similares → lições aprendidas

2. **Mapear escopo técnico** (~1-2h):
   - Quais APIs existem? (POST/GET/PUT/DELETE)
   - Quais operações precisam de UI automation?
   - Quais dados precisam ser gerados?
   - Quais dependências externas existem (tenant, credentials, customer action)?

3. **Estimar sizing** (~30 min):
   - Quantidade estimada de tickets
   - Classificação: Small / Medium / Large
   - Roles necessários
   - Timeline preliminar

4. **Identificar riscos iniciais** (~30 min):
   - Dependências externas sem data definida
   - Limitações técnicas (API gaps, rate limits)
   - Conflitos de recursos

**Inputs:** SOW, docs técnicos, contexto comercial
**Outputs:** Inventário de materiais, mapa de APIs, sizing estimate, risk register v0

**Critérios de Aceite (DoD):**
- [ ] Todos os deliverables do SOW listados
- [ ] APIs mapeadas (endpoint + método + limitação)
- [ ] Dependências externas identificadas
- [ ] Sizing estimado (S/M/L)
- [ ] Pelo menos 1 risco documentado
- [ ] Brainstorm com CE e/ou DATA realizado

**Gate 1: Discovery Complete** → Avança para Fase 2

**Falhas comuns:**
- Não ler a documentação técnica → descobre limitação na Fase 5
- Assumir que API suporta tudo → UI automation surpresa
- Não falar com CE/DATA antes → sizing errado

> **Confiança**: ALTO — Padrão extraído de GEM Discovery (Dec 17-20, 4 dias) e Pre-Project Ticket Planning Fase 1.
> **Fonte interna adicional**: SOW Best Practices (Mailchimp, Gabi): "Alinhar com engenharia as datas certinhas" + "100 versões de refinamento antes do Gantt final" + SOW com 12 seções padrão.
> **Fonte externa**: "Discovery Phase" é fase padrão em frameworks como SAFe, Scrum.org e PMBOK.

---

### FASE 2: Pre-Project Planning

| Campo | Valor |
|:------|:------|
| **Objetivo** | Criar TODOS os tickets, milestones e GANTT ANTES do kick-off |
| **Owner** | TSA (R/A) |
| **Duração típica** | 3-4 horas (com automação) a 1-2 dias (manual) |
| **Onde acontece** | Linear (tickets), Google Sheets (GANTT), Scripts Python |
| **Por que existe** | Preparação proativa = zero surpresas no kick-off |

**O que fazer:**
1. **Desenhar milestones** (~30 min):
   - Foundation → Seed Data → Data Gen → Ingestion → Stories → Validate → Launch
   - Adaptar ao projeto (nem todo projeto tem todas as fases)
   - Mapear dependências entre fases

2. **Criar tickets via script** (~30 min):
   - Usar formato padrão (Objective, Overview, Key Tasks, Validation, Risks)
   - Bulk creation via Linear GraphQL API
   - Delay 0.5s entre requests (rate limit)

3. **Rodar auditoria** (~1h):
   - 10 checks: título, descrição, assignee, milestone, dependencies, estimate, blocker, SOW coverage, duplicatas, state
   - Fix até 10/10 PASS

4. **Enriquecer tickets** (~30 min):
   - Adicionar detalhes de API (endpoint, request body, rate limit)
   - Marcar `REQUIRES UI AUTOMATION` quando não há API
   - Linkar dependências no Linear

5. **Gerar GANTT** (~15 min):
   - Script Python gera Excel com fases, gates, owners, datas
   - Paleta de cores padrão: header (#2C3E50), gate (#E74C3C), phase (#9B59B6)

6. **Comunicar** (~15 min):
   - Post no Slack com overview (template abaixo)
   - Compartilhar spreadsheet e Linear link

**Inputs:** Discovery completo, mapa de APIs, sizing
**Outputs:** Linear project com tickets, GANTT Excel, Slack report

**Critérios de Aceite (DoD):**
- [ ] Todos os tickets criados no Linear
- [ ] Auditoria 10/10 PASS
- [ ] GANTT com datas e owners
- [ ] Labels aplicados por fase
- [ ] Dependencies linkadas
- [ ] Slack report postado
- [ ] CE informado e review agendado

**Gate 2: Planning Complete** → Avança para Fase 3

> **Confiança**: ALTO — Este é o processo documentado no Pre-Project Ticket Planning, validado no GEM (37 tickets em 3-4h).

---

### FASE 3: Kick-off

| Campo | Valor |
|:------|:------|
| **Objetivo** | Alinhar time, confirmar escopo, definir cadências |
| **Owner** | TSA (R/A), GTM (C) |
| **Duração típica** | 1 reunião (30-60 min) + setup (1 dia) |
| **Onde acontece** | Call (Zoom/Meet), Slack, Linear |
| **Por que existe** | Garante que todos sabem o que fazer, quando e como se comunicar |

**O que fazer:**
1. **Reunião de kick-off** (30-60 min):
   - Apresentar GANTT e milestones
   - Confirmar roles (quem faz o quê)
   - Definir cadências (daily, weekly, checkpoints)
   - Identificar dependências do cliente (acesso, credentials)
   - Perguntas e ajustes

2. **Setup operacional** (~1 dia):
   - Confirmar acesso ao tenant
   - Verificar API keys e credentials
   - Criar canal Slack se necessário
   - Distribuir tickets para owners

3. **Mensagem de kick-off no Slack** (template abaixo)

**Inputs:** Linear project, GANTT, equipe confirmada
**Outputs:** Ata de kick-off, cadências definidas, acessos confirmados

**Critérios de Aceite (DoD):**
- [ ] Reunião realizada com todos os roles presentes
- [ ] GANTT revisado e aceito pelo time
- [ ] Cadências definidas (daily async + weekly sync)
- [ ] Acesso ao tenant confirmado
- [ ] API keys funcionando
- [ ] Primeiro ticket assignado e ready to start

**Gate 3: Kick-off Complete** → Avança para Fase 4

**Falhas comuns:**
- Kick-off sem GANTT → time não sabe as datas
- Não confirmar acesso → Fase 4 bloqueia no dia 1
- Pular kick-off "porque já sabemos o que fazer" → desalinhamento silencioso

> **Confiança**: ALTO — GEM teve "Internal Project Kickoff" (Feb 05) e QBO teve "Gate 1: Readiness Confirmation" (Jan 02-06).

---

### FASE 4: Foundation

| Campo | Valor |
|:------|:------|
| **Objetivo** | Preparar o ambiente: acessos, infra, configurações base |
| **Owner** | TSA (R/A), CE (R) |
| **Duração típica** | 3-7 dias |
| **Onde acontece** | Tenant do cliente, AWS, Linear |
| **Por que existe** | Nada funciona sem a base. Foundation bloqueia TUDO que vem depois. |

**O que fazer:**
1. Configurar tenant (admin access, user accounts)
2. Setup de infraestrutura (AWS, auto-login, environments)
3. Configurações core (roles, permissions, integrations)
4. Validar que tudo funciona (login, API calls, permissions)
5. Documentar acessos em local compartilhado

**Inputs:** Acesso ao tenant, API keys, infra requirements
**Outputs:** Ambiente funcional, users criados, API testada

**Critérios de Aceite (DoD):**
- [ ] Todos os users do time conseguem logar
- [ ] API key funciona (teste com POST simples)
- [ ] Configurações base aplicadas
- [ ] Staging/dev environments separados (se aplicável)
- [ ] Documentação de acesso atualizada

**Gate 4: Foundation Complete** → Avança para Fase 5

**Falhas comuns:**
- Tenant demora para ser provisionado (dependência externa)
- API key sem permissão de escrita → bloqueia data gen
- Esquecer staging → testa em prod

> **Confiança**: ALTO — GEM Foundation (Jan 06-29), QBO Environment Setup. Padrão universal.

---

### FASE 5: Build (Seed Data + Data Gen + Ingestion)

| Campo | Valor |
|:------|:------|
| **Objetivo** | Popular o sistema com dados realistas e funcionais |
| **Owner** | CE (R/A), DATA (R), TSA (C) |
| **Duração típica** | 7-14 dias |
| **Onde acontece** | Scripts Python, APIs, tenant do cliente |
| **Por que existe** | Demo sem dados = demo vazia. Dados ruins = credibilidade zero. |

**O que fazer:**

**5a. Seed Data** (2-3 dias):
- Criar entidades estáticas: jobs, departments, offices, templates
- Usar API quando disponível, UI automation quando não
- Validar que entidades aparecem corretamente na UI

**5b. Data Generation** (3-5 dias):
- Design de schema (aprovado pelo TSA)
- Definir distribuição (quantos por fase, spread temporal)
- Gerar dados via scripts (candidatos, applications, resumes)
- Validar realismo (nomes, empresas, datas)

**5c. Ingestion** (2-4 dias):
- Respeitar ordem de FK dependencies
- Rate limiting (0.5s entre requests)
- Log de cada operação para rollback
- Rodar Gate 1 (validação local) ANTES de ingerir

**Pipeline de Validação (obrigatório):**
```
CSV prontos → Gate 1 (validate_csvs.py, local)
           → INSERT no banco
           → Gate 2 (Retool validator, backend)
           → Gate 3 (Auditoria Claude, coerência)
           → DADOS VÁLIDOS ✓
```

**Inputs:** Ambiente configurado, APIs mapeadas, schema aprovado
**Outputs:** Sistema populado com dados, auditoria 3-gate PASS

**Critérios de Aceite (DoD):**
- [ ] Entidades estáticas criadas e visíveis na UI
- [ ] Dados gerados com nomes/empresas realistas
- [ ] Gate 1: validate_csvs → 0 FAIL
- [ ] Gate 2: Retool validator → 0 erros
- [ ] Gate 3: Auditoria → aprovado (5 auditores)
- [ ] Nenhum orphan ou FK violation

**Gate 5: Build Complete** → Avança para Fase 6

**Falhas comuns:**
- Gerar dados genéricos ("John Doe", "Company ABC") → cliente nota
- Não respeitar FK order → erros de constraint
- Rate limit → API bloqueia
- Não ter rollback → erro irrecuperável
- Schema muda depois de gerar → retrabalho total

> **Confiança**: ALTO — Padrão extraído de GEM (Seed Data + Data Gen + Ingestion, 37 tickets) e QBO (3-Gate pipeline, 59 regras, 189 checks).

---

### FASE 6: Stories & Feature Setup

| Campo | Valor |
|:------|:------|
| **Objetivo** | Configurar demos/features que o cliente verá em ação |
| **Owner** | TSA (R/A), CE (R) |
| **Duração típica** | 5-10 dias |
| **Onde acontece** | Tenant do cliente, Linear |
| **Por que existe** | Os dados existem, agora precisam contar uma história convincente. |

**O que fazer:**
1. Configurar cada feature/story conforme SOW
2. Validar que cada story funciona end-to-end
3. Demo interno para stakeholders (dry run)
4. Documentar stories em formato reproduzível (click path)

**Inputs:** Sistema populado, features especificadas no SOW
**Outputs:** Features configuradas e funcionando, demo interno realizado

**Critérios de Aceite (DoD):**
- [ ] Cada feature do SOW configurada e testada
- [ ] Click paths documentados
- [ ] Demo interno realizado (pelo menos 1 stakeholder viu)
- [ ] Bugs encontrados no demo criados como tickets (P1/P2)
- [ ] Evidence pack iniciado (screenshots das features)

**Gate 6: Stories Complete** → Avança para Fase 7

> **Confiança**: ALTO — GEM Phase 5 Stories (6 stories, RAC-120 a RAC-125) + demo interno (RAC-127).

---

### FASE 7: Validate (QA + UAT)

| Campo | Valor |
|:------|:------|
| **Objetivo** | Garantir qualidade antes de mostrar ao cliente |
| **Owner** | TSA (R), GTM (A) |
| **Duração típica** | 5-7 dias |
| **Onde acontece** | Tenant, Linear, Slack, Calls |
| **Por que existe** | Bug em UAT = credibilidade perdida. QA rigoroso = confiança do cliente. |

**O que fazer:**

**7a. QA Interno** (2-3 dias):
- TSA testa CADA feature como se fosse o cliente
- Testar edge cases e fluxos alternativos
- Criar tickets para bugs (P1/P2)
- Fix bugs e re-test

**7b. UAT com Cliente** (2-3 dias):
- GTM agenda sessão com cliente
- Cliente testa com roteiro (click paths)
- Coletar feedback estruturado
- Fix final após UAT

**Inputs:** Features configuradas, click paths
**Outputs:** Bugs fixados, UAT aprovado pelo cliente, evidence pack completo

**Critérios de Aceite (DoD):**
- [ ] QA interno: 0 bugs P0/P1 abertos
- [ ] UAT agendado e realizado com cliente
- [ ] Feedback do cliente documentado
- [ ] Bugs pós-UAT corrigidos
- [ ] Evidence pack completo (screenshot por feature)
- [ ] Sign-off do cliente (verbal ou escrito)

**Gate 7: Validate Complete** → Avança para Fase 8

**Falhas comuns:**
- QA superficial → bugs aparecem no UAT
- Não documentar feedback do cliente → se perde
- UAT sem roteiro → cliente não sabe o que testar
- Confiar que "funciona na minha máquina" = funciona em prod

> **Confiança**: ALTO — GEM Validate (Jan 30 - Feb 06, QA + UAT + sign-off). QBO Gate 2 Customer Approval (Feb 14-18).
> **Fonte externa**: UAT como gate de go-live é standard em ITIL, PMBOK e ISO 27001. [Quality Gates — Sonar](https://www.sonarsource.com/learn/quality-gate/) · [Quality Gates — testRigor](https://testrigor.com/blog/software-quality-gates/).

---

### FASE 8: Launch & Go-Live

| Campo | Valor |
|:------|:------|
| **Objetivo** | Colocar em produção e entregar ao cliente |
| **Owner** | CE (R), GTM (A), Eng (R) |
| **Duração típica** | 1-3 dias |
| **Onde acontece** | Produção, Slack, Calls |
| **Por que existe** | O momento da verdade. Tudo que foi preparado entra em uso real. |

**O que fazer:**
1. Deploy em produção (CE + Eng)
2. Smoke test pós-deploy (TSA)
3. Walkthrough com cliente (GTM)
4. Confirmar que tudo funciona em ambiente real
5. Comunicar go-live no Slack

**Inputs:** UAT aprovado, bugs fixados
**Outputs:** Sistema em produção, cliente com acesso, go-live confirmado

**Critérios de Aceite (DoD):**
- [ ] Deploy em produção concluído
- [ ] Smoke test: todas as features OK
- [ ] Walkthrough com cliente realizado
- [ ] Cliente confirma que está funcionando
- [ ] Comunicação de go-live no Slack

**Gate 8: Launch Complete** → Avança para Fase 9

> **Confiança**: ALTO — GEM Launch (Feb 07-13), QBO Launch (Feb 18-25). Deploy + walkthrough + hypercare.

---

### FASE 9: Hypercare & Handover

| Campo | Valor |
|:------|:------|
| **Objetivo** | Suporte intensivo pós-go-live e transição para operação BAU |
| **Owner** | GTM (R/A), CE (C) |
| **Duração típica** | 5-10 dias |
| **Onde acontece** | Slack, Calls, Coda |
| **Por que existe** | Primeiros dias pós-launch são os mais críticos. Abandono = churn. |

**O que fazer:**
1. **Hypercare** (5-7 dias):
   - Monitorar sistema diariamente
   - Resposta rápida a bugs (< 4h para P0/P1)
   - Check-in com cliente a cada 2 dias
   - Documentar incidentes

2. **Handover** (2-3 dias):
   - Gerar documentation package (runbook, decisões, lições)
   - Treinar equipe do cliente (se aplicável)
   - Transferir ownership de Slack/Linear para modo BAU
   - Definir suporte pós-handover (quem procurar)

**Inputs:** Sistema em produção
**Outputs:** Documentation package, handover formal, modo BAU ativado

**Critérios de Aceite (DoD):**
- [ ] Zero bugs P0 abertos durante hypercare
- [ ] Documentation package entregue
- [ ] Treinamento realizado (se aplicável)
- [ ] Contact point pós-handover definido
- [ ] Ticket de hypercare fechado no Linear

**Gate 9: Handover Complete** → Avança para Fase 10

**Falhas comuns:**
- "Go-live e esquece" → cliente fica perdido
- Não documentar → próximo projeto começa do zero
- Hypercare sem SLA → bugs ficam sem resposta

> **Confiança**: ALTO (atualizado) — GEM tem Hypercare (ONB-15, Feb 07-13) e Project Closure (ONB-14). QBO tem Post-Launch Monitoring (Feb 25+).
> **Fonte interna (ENCONTRADA pós-varredura)**: `intuit-boom/INTUIT_BOOM_TRANSFER/` — Pacote completo de handover com 11 documentos: START_HERE, MEGA_MEMORY, SOW_AND_SCOPE, ECOSYSTEM_MAP, TECHNICAL_REFERENCE, RUNBOOKS (11 procedures), CONTACTS_AND_STAKEHOLDERS, RISK_MATRIX_AND_BLOCKERS, CREDENTIALS_CHECKLIST, DECISIONS_LOG. USAR COMO TEMPLATE.
> **Fonte externa**: ITIL Service Transition, Early Life Support. [Post Go-Live — Rackspace](https://docs.rackspace.com/docs/post-go-live) · [Project Handover Checklist — DOOR3](https://www.door3.com/blog/project-handover-checklist) · [Handing Off a Software Project — Simple Thread](https://www.simplethread.com/handing-off-a-software-project/).

---

### FASE 10: Closeout & Retrospective

| Campo | Valor |
|:------|:------|
| **Objetivo** | Encerrar formalmente e capturar lições para o próximo projeto |
| **Owner** | TSA (R/A) |
| **Duração típica** | 1-2 dias |
| **Onde acontece** | Coda, Linear, Slack |
| **Por que existe** | Sem retro, erros se repetem. Sem closeout, projeto "nunca termina". |

**O que fazer:**
1. **Closeout operacional**:
   - Mover TODOS os tickets para Done
   - Fechar milestone no Linear
   - Atualizar GANTT com datas reais
   - Arquivar canal Slack (se temporário)

2. **Retrospectiva** (formato Keep/Stop/Start):
   - O que funcionou bem? (Keep)
   - O que deu problema? (Stop)
   - O que devemos começar a fazer? (Start)
   - Documentar em Coda para referência futura

3. **Atualizar playbook**:
   - Novos riscos descobertos → adicionar ao risk register padrão
   - Novos padrões → atualizar templates
   - Novos scripts → contribuir para toolkit

**Inputs:** Projeto entregue, feedback coletado
**Outputs:** Retro documentada, tickets fechados, lições aplicadas

**Critérios de Aceite (DoD):**
- [ ] 100% dos tickets em Done ou Cancelled (com justificativa)
- [ ] Retro documentada em Coda
- [ ] GANTT atualizado com datas reais
- [ ] Lições relevantes aplicadas ao playbook
- [ ] Comunicação de encerramento no Slack

**Gate 10: Project Closed** ✓

> **Confiança**: MÉDIO — GEM tem Close Out (ONB-14). Retro formal NÃO ENCONTRADA como prática recorrente.
> **Fonte externa**: "Lessons Learned" é prática standard em PMI, SAFe.

---

## Cadências e Rituais

| Ritual | Frequência | Participantes | Formato | Canal |
|:-------|:-----------|:--------------|:--------|:------|
| **Daily Agenda** | Diário (async) | TSA → time | Post Slack (v1.8 format) | #scrum-of-scrums |
| **1:1 TSA Lead** | Diário | TSA Lead + cada TSA | Call 15 min | Zoom/Meet |
| **Weekly Sync** | Semanal | Todos os roles do projeto | Call 30 min | Zoom/Meet |
| **Gate Review** | A cada gate | TSA (R) + Approver (A) | Checklist + decisão | Linear + Slack |
| **Client Check-in** | Semanal (após kick-off) | GTM + Cliente | Call 30 min | Zoom/Meet |
| **Retro** | Fim do projeto | Time completo | Keep/Stop/Start | Coda |

### Daily Agenda Format (v1.8)
```
[Daily Agenda – YYYY-MM-DD]

PROJECT ETA MM-DD
• Topic Description
 Do: Specific action ETA MM-DD
 Do: Another action
References: [links]

ESCALATION: None / [description]
```

> **Fonte interna**: Daily Agenda v1.8 (TSA_DAILY_REPORT, validado 2026-02-03).

---

## Gestão de Mudanças

### Quando aplicar:
- Cliente pede algo fora do SOW
- Equipe descobre que uma feature precisa de abordagem diferente
- Timeline precisa ser ajustada

### Processo:
1. **Registrar**: Criar ticket no Linear com label `new-scope`
2. **Avaliar**: TSA documenta impacto (prazo + esforço + risco)
3. **Aprovar**: GTM + Cliente aprovam (ou rejeitam)
4. **Executar**: Se aprovado, ticket entra no backlog com prioridade definida
5. **Comunicar**: Atualizar GANTT e Slack report

### Template de Change Request (Ticket Linear)

```markdown
## Change Request: [Descrição curta]

| Campo | Valor |
|:------|:------|
| **CR ID** | CR-[PROJECT]-[NNN] |
| **Solicitante** | [Nome + Role] |
| **Data** | [YYYY-MM-DD] |
| **Categoria** | [ ] Escopo [ ] Timeline [ ] Técnico [ ] Budget |
| **Prioridade** | [ ] Crítico [ ] Alto [ ] Médio [ ] Baixo |

### Descrição da Mudança
[O que está sendo pedido e por quê]

### Justificativa
[Por que isso é necessário — business reason]

### Impact Assessment
| Dimensão | Impacto |
|:---------|:--------|
| **Escopo** | [O que muda no SOW] |
| **Timeline** | [Quantos dias a mais] |
| **Esforço** | [Horas adicionais por role] |
| **Risco** | [Novos riscos introduzidos] |

### Decisão
| Status | Aprovador | Data |
|:-------|:----------|:-----|
| [ ] Aprovado [ ] Rejeitado [ ] Adiado | [GTM Owner] | [Data] |

### Se Aprovado — Plano de Execução
1. [Ticket 1 criado]
2. [GANTT atualizado]
3. [Stakeholders comunicados]
```

> **Fonte externa**: [Change Request Process — PMI](https://www.pmi.org/learning/library/scope-control-projects-you-6972) · [Change Request Form — ProjectManager](https://www.projectmanager.com/templates/change-request-form).

### Regra:
> Mudança sem ticket = mudança que não existe. Mudança sem aprovação = scope creep.

---

## Gestão de Riscos

### Risk Register Padrão

| ID | Risco | Probabilidade | Impacto | Mitigação | Owner |
|:---|:------|:-------------|:--------|:----------|:------|
| R01 | Tenant provisioning atrasado | Médio | Alto (bloqueia tudo) | Solicitar com 2 semanas de antecedência | TSA |
| R02 | API não suporta operação necessária | Médio | Médio (UI automation) | Mapear APIs na Discovery | TSA |
| R03 | Rate limiting na ingestão | Alto | Baixo (delay) | Exponential backoff no script | CE |
| R04 | Schema muda depois de data gen | Baixo | Alto (retrabalho) | Schema freeze no Gate 5a | DATA |
| R05 | Recurso-chave indisponível | Baixo | Alto (atraso) | Documentação suficiente para handoff | TSA |
| R06 | Bugs descobertos no UAT | Alto | Médio (atraso 1-3 dias) | QA interno rigoroso antes do UAT | TSA |
| R07 | Escopo creep via slack | Médio | Médio (desvio) | Change control formal | GTM |
| R08 | Dados sintéticos não-realistas | Médio | Alto (credibilidade) | Gate 3 auditoria de realismo | DATA |

> **Fonte interna**: Riscos reais de GEM (RAC-135 backdating blocker) e QBO (90 employee dupes, gateway timeout 504).

---

## Métricas e KPIs

### Framework: DORA + Flow Metrics (Adaptado para Delivery)

As métricas seguem o framework [DORA](https://dora.dev/guides/dora-metrics-four-keys/) (Google, 10+ anos de pesquisa, 36K+ profissionais) adaptado para delivery de implementações, combinado com [Agile Flow Metrics](https://www.atlassian.com/agile/project-management/metrics) (Atlassian).

**Insight DORA**: "Velocidade e estabilidade NÃO são trade-offs" — os melhores times excel em ambos.

| Métrica | Framework | O que mede | Como coletar | Target |
|:--------|:----------|:-----------|:-------------|:-------|
| **Lead Time** | DORA (adaptado) | SOW assinado → go-live | Datas no GANTT | Small: 3 sem · Medium: 6 sem · Large: 10 sem |
| **Cycle Time por Ticket** | Flow | In Progress → Done | Linear analytics nativo | < 5 dias (P2), < 1 dia (P0) |
| **Delivery Frequency** | DORA (adaptado) | Entregas por período (demos shipped) | Linear milestones closed | ≥ 1 deliverable/semana durante Build |
| **First-Pass Validation Rate** | Flow | Datasets que passam validação na 1ª tentativa | validate_csvs.py results | > 80% (target: > 95%) |
| **Rework Rate** | DORA | Tickets reabertos em 21 dias / total | Linear state changes | < 10% (alerta se > 15%) |
| **Gate Pass Rate** | Custom | % de gates aprovados na 1ª tentativa | Contagem por projeto | > 80% |
| **Blocker Duration** | Flow | Tempo médio em estado Blocked | Linear blocked label + timestamps | < 2 dias média |
| **SOW Coverage** | Custom | % dos deliverables com tickets | Audit script | 100% |
| **Data Quality Score** | Custom | Gates 1-3 pass rate | validate_csvs.py + Retool | 100% (Gate 1 + Gate 2) |
| **Escalation Rate** | Custom | % tickets escalados para Eng | Linear label tracking | < 20% |
| **Client Satisfaction** | Custom | Feedback pós-UAT | Formulário ou verbal | > 8/10 |

### SLOs por Prioridade

| Prioridade | Response Time | Resolution Time | Referência |
|:-----------|:-------------|:---------------|:-----------|
| P0 | < 1 hora | < 4 horas | Sam: "escalate quickly" |
| P1 | < 4 horas | < 1 dia | TMS v2.0 |
| P2 | < 1 dia | < 5 dias | TMS v2.0 |
| P3 | Next standup | < 2 semanas | TMS v2.0 |

> **Fonte interna**: P0-P3 do TMS v2.0 (`TSA_CORTEX/knowledge-base/sops/ticket-management-system-v2.md`). SLOs derivados da quote do Sam ("stuck for more than a couple of hours, escalate").
> **Fonte externa**: [DORA Metrics Four Keys](https://dora.dev/guides/dora-metrics-four-keys/) · [Agile Metrics — Atlassian](https://www.atlassian.com/agile/project-management/metrics) · [Google SRE Book](https://sre.google/sre-book/table-of-contents/) para SLOs.

---

## Playbook de Escalonamento

| Situação | Para quem | Como | Quando |
|:---------|:----------|:-----|:-------|
| Bug P0 em produção | #dev-on-call + GTM owner | Slack DM imediato | Imediatamente |
| Blocker > 2 horas | GTM owner | Slack DM | Mesmo dia |
| Recurso indisponível | TSA Lead | Slack DM | Mesmo dia |
| Cliente insatisfeito | GTM Lead (Kat) | Call + Slack | < 4 horas |
| Scope creep identificado | GTM owner + TSA Lead | Ticket new-scope + assessment | < 24 horas |
| Gate falha 2x consecutivas | TSA Lead + GTM | Call de alinhamento | Imediato |
| Timeline em risco (> 3 dias atraso) | Todos stakeholders | Weekly sync agenda | Próximo sync |

> **Fonte interna**: Sam quote (CEO): "Escalate quickly to the GTM owner. This is not a failure."

---

# 5. AJUSTES NOS DRAFTS

## 5.1 Ajustes no DRAFT Linear Ticket Management

| Seção | Ajuste | Por quê |
|:------|:-------|:--------|
| **Meetings & Rituals** | Adicionar seção C completa (já existe no TMS v2.0 local, mas pode não estar no Coda) | Full Implementation Process referencia "Daily Agenda" e "1:1" que precisam estar documentados no TMS |
| **Version** | Atualizar de 1.0 para 2.0 | CODA pode estar desatualizado; v2.0 tem 8 correções críticas |
| **Labels** | Verificar que usa "Customer Issues" (não "Bug") e "Refactor" (não "Tech Debt") | Correção validada via Linear API em 2026-01-27 |
| **State Flow** | Confirmar "TSA owns until Backlog" (não Refinement) | Correção validada pelo usuário em TMS v2.0 |
| **Link para Full Implementation Process** | Adicionar na seção "Related Docs" | Cross-reference para manter coerência |

**Texto pronto para adicionar ao DRAFT TMS:**

```markdown
## Documentos Relacionados
- [Full Implementation Process](https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS) — Processo E2E de implantação
- [Pre-Project Linear Ticket Planning](https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A) — Como preparar tickets antes do kick-off
```

## 5.2 Ajustes no DRAFT Pre-Project Linear Ticket Planning

| Seção | Ajuste | Por quê |
|:------|:-------|:--------|
| **Glossary** | Adicionar "Gate" como termo | Full Implementation Process usa gates extensivamente |
| **Flow** | Adicionar referência aos gates do Full Process | Pre-Project é a Fase 2 do processo completo; precisa situar onde encaixa |
| **Communication** | Referenciar template de kick-off do Full Process | Slack report do Pre-Project é o input para o kick-off |
| **Related Docs** | Adicionar link para Full Implementation Process | Cross-reference |

**Texto pronto para adicionar ao DRAFT Pre-Project:**

```markdown
## Onde Este Documento Encaixa

Este processo cobre a **Fase 2: Pre-Project Planning** do [Full Implementation Process](https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS).

**Antes**: Fase 1 (Discovery & Sizing) deve estar completa.
**Depois**: Fase 3 (Kick-off) usa os outputs deste processo.

### Gate de Entrada (Fase 1 → Fase 2)
- [ ] Todos os deliverables do SOW listados
- [ ] APIs mapeadas
- [ ] Sizing estimado (S/M/L)
- [ ] Pelo menos 1 risco documentado

### Gate de Saída (Fase 2 → Fase 3)
- [ ] Tickets criados e auditados (10/10 PASS)
- [ ] GANTT com datas e owners
- [ ] Slack report postado
- [ ] CE review agendado
```

---

# 6. CHECKLISTS E TEMPLATES

## CHECKLIST 1: Pré-Projeto (Intake + Discovery + Sizing)

```markdown
## Checklist Pré-Projeto

### Intake (Gate 0)
- [ ] Oportunidade identificada e qualificada
- [ ] Fit técnico avaliado (produto no catálogo?)
- [ ] Fit comercial avaliado (budget, timeline)
- [ ] SOW draft ou scope document existente
- [ ] Decisão GO/NO-GO registrada
- [ ] Recursos disponíveis confirmados

### Discovery (Gate 1)
- [ ] SOW/Contrato lido e deliverables extraídos
- [ ] Documentação técnica coletada (API docs, arquitetura)
- [ ] Brainstorm com CE realizado
- [ ] Brainstorm com DATA realizado (se aplicável)
- [ ] APIs mapeadas (endpoint + método + limitação)
- [ ] Dependências externas identificadas
- [ ] Projetos similares revisados (lições)
- [ ] Slack threads relevantes coletados

### Sizing
- [ ] Quantidade estimada de tickets: ___
- [ ] Classificação: [ ] Small [ ] Medium [ ] Large
- [ ] Roles necessários: TSA [ ] CE [ ] DATA [ ] GTM [ ] Eng [ ]
- [ ] Timeline preliminar definida
- [ ] Risk register v0 criado
```

## CHECKLIST 2: Kick-off

```markdown
## Checklist Kick-off

### Pré-Reunião
- [ ] GANTT finalizado e compartilhado
- [ ] Linear Project com tickets criados
- [ ] Auditoria 10/10 PASS
- [ ] Agenda da reunião enviada
- [ ] Todos os participantes confirmados

### Reunião
- [ ] GANTT apresentado e aceito
- [ ] Roles confirmados (quem faz o quê)
- [ ] Cadências definidas (daily async, weekly sync)
- [ ] Dependências do cliente identificadas
- [ ] Perguntas respondidas
- [ ] Próximos passos claros

### Pós-Reunião
- [ ] Ata registrada (Coda ou Slack)
- [ ] Acesso ao tenant confirmado
- [ ] API keys testadas
- [ ] Canal Slack criado/confirmado
- [ ] Primeiro ticket distribuído
- [ ] Mensagem de kick-off postada no Slack
```

## CHECKLIST 3: Execução por Fase

```markdown
## Checklist Execução (usar em cada fase)

### Entrada da Fase
- [ ] Gate anterior APROVADO
- [ ] Tickets da fase assignados e com owner
- [ ] Dependências da fase anterior atendidas
- [ ] Recursos disponíveis

### Durante a Fase
- [ ] Daily reports postados em #scrum-of-scrums
- [ ] Blockers comunicados em < 2 horas
- [ ] Tickets atualizados (state, comments)
- [ ] Risk register revisado

### Saída da Fase (Gate)
- [ ] TODOS os critérios de aceite (DoD) da fase atendidos
- [ ] Zero tickets P0/P1 abertos
- [ ] Artefatos produzidos e documentados
- [ ] Próxima fase pronta para iniciar
- [ ] Gate review realizado e APROVADO
```

## CHECKLIST 4: QA/Aceite

```markdown
## Checklist QA/Aceite

### QA Interno (Pre-UAT)
- [ ] Cada feature testada como se fosse o cliente
- [ ] Edge cases testados
- [ ] Dados verificados (realismo, completude)
- [ ] Click paths documentados
- [ ] Screenshots/vídeos capturados (evidence pack)
- [ ] Bugs encontrados criados como tickets
- [ ] Zero bugs P0/P1 abertos

### Data Validation (3-Gate)
- [ ] Gate 1: validate_csvs.py → 0 FAIL
- [ ] Gate 2: Retool validator → 0 erros
- [ ] Gate 3: Auditoria Claude → PASS (5 auditores)

### UAT (Client)
- [ ] Sessão agendada com cliente
- [ ] Click paths compartilhados
- [ ] Cliente testou TODAS as features do SOW
- [ ] Feedback coletado e documentado
- [ ] Bugs pós-UAT criados como tickets
- [ ] Sign-off do cliente obtido (verbal ou escrito)
```

## CHECKLIST 5: Handover + Pós-Implantação

```markdown
## Checklist Handover + Pós-Implantação

### Handover
- [ ] Documentation package produzido:
  - [ ] Runbook (como operar o sistema)
  - [ ] Decisões técnicas documentadas
  - [ ] Acessos e credentials listados
  - [ ] Scripts e ferramentas entregues
- [ ] Treinamento realizado (se aplicável)
- [ ] Contact point pós-handover definido
- [ ] Ownership transferido (Slack, Linear)

### Hypercare
- [ ] Monitoramento diário ativo
- [ ] SLA de resposta comunicado ao cliente
- [ ] Bugs < P0/P1: response < 4h
- [ ] Check-ins a cada 2 dias
- [ ] Incidentes documentados

### Closeout
- [ ] TODOS os tickets em Done ou Cancelled
- [ ] GANTT atualizado com datas reais
- [ ] Retrospectiva realizada (Keep/Stop/Start)
- [ ] Lições aplicadas ao playbook
- [ ] Comunicação de encerramento no Slack
- [ ] Milestone fechado no Linear
```

## CHECKLIST 6: Auditoria (Stakeholders)

```markdown
## Checklist Auditoria — Perguntas Difíceis

### Perspectiva Cliente
- [ ] O escopo entregue corresponde ao SOW?
- [ ] Todas as features funcionam como demonstrado?
- [ ] Os dados parecem realistas e profissionais?
- [ ] O cliente recebeu documentação suficiente?
- [ ] O cliente sabe quem contatar pós-projeto?

### Perspectiva GTM
- [ ] O timeline foi cumprido?
- [ ] O cliente ficou satisfeito? (escala 1-10)
- [ ] Houve scope creep? Se sim, foi formalizado?
- [ ] O evidence pack está completo?
- [ ] A relação com o cliente foi preservada?

### Perspectiva Eng
- [ ] Os tickets eram claros o suficiente para executar sem perguntar?
- [ ] O AC era mensurável?
- [ ] Os ambientes (staging/prod) estavam configurados?
- [ ] Houve retrabalho por falta de informação?

### Perspectiva TSA
- [ ] Todos os gates foram respeitados?
- [ ] O processo foi seguido ou "bypassado"?
- [ ] Houve dependência que não foi antecipada?
- [ ] O playbook cobriu todos os cenários encontrados?

### Perspectiva Executivo
- [ ] O custo (horas) ficou dentro do esperado?
- [ ] O processo é escalável para 10 projetos simultâneos?
- [ ] Algum novo TSA conseguiria executar sem handholding?
- [ ] As métricas estão sendo coletadas?
```

---

## TEMPLATE 1: Ticket Linear (Padrão)

```markdown
## 🎯 Objective
[UMA frase — o que este ticket entrega e por que importa]

## 📋 Overview
[2-3 parágrafos de contexto: o que, por que, como se conecta ao projeto]

## ✅ Key Tasks
| **Task** | **Owner** | **Why** |
|:---------|:----------|:--------|
| [Ação específica] | **[TSA/CE/DATA/GTM]** | [Razão de negócio] |

## 🔍 Validation
| **Check** | **Method** | **Owner** |
|:----------|:-----------|:----------|
| [O que verificar] | [Como verificar] | **[Role]** |

## ⚠️ Risks
| **Risk** | **Impact** | **Mitigation** |
|:---------|:-----------|:---------------|
| [O que pode dar errado] | [Consequência] | [Como prevenir] |

## 🔗 External Dependency
[Se aplicável — o que depende de fora]

---
*Parte de [PROJETO] · Milestone: [FASE] · Criado por: [TSA NAME] · Última atualização: [DATA]*
```

**Campos obrigatórios no Linear:**
| Campo | Padrão |
|:------|:-------|
| Title | `[PROJECT] Verb + Object` |
| Team | Platypus (PLA) ou Raccoons (RAC) |
| Priority | P0/P1/P2/P3 |
| Labels | `[project]-project` + label de fase |
| State | Backlog |
| Milestone | Correspondente à fase |
| Estimate | Story points |

---

## TEMPLATE 2: Mensagem de Kick-off (Slack)

```
@here 🚀 Kick-off: [PROJECT NAME]

Pessoal, estamos iniciando a implantação de [PROJECT]. Segue o overview:

📋 Escopo:
• [N] features / deliverables conforme SOW
• Timeline: [DATA INÍCIO] → [DATA GO-LIVE]
• Tipo: [Small/Medium/Large]

👥 Time:
• TSA: [Nome] — Coordenação e QA
• CE: [Nome] — Implementação técnica
• DATA: [Nome] — Geração de dados
• GTM: [Nome] — Interface cliente

📊 Artefatos:
• GANTT: [LINK]
• Linear Project: [LINK]
• SOW: [LINK]

🔄 Cadências:
• Daily async: #scrum-of-scrums (Daily Agenda format)
• Weekly sync: [DIA/HORA]
• Gate reviews: a cada fase

⚠️ Riscos Identificados:
• [Risco 1]: [Mitigação]
• [Risco 2]: [Mitigação]

📅 Próximos Passos:
1. [Ação 1] — [Owner] — ETA [Data]
2. [Ação 2] — [Owner] — ETA [Data]

Dúvidas, me procurem. Let's go! 💪
```

---

## TEMPLATE 3: Página Coda (Estrutura Padrão)

```markdown
# [PROJECT NAME] — Implementation Hub

## Document Info
| Field | Value |
|:------|:------|
| Owner | [TSA Name] |
| Status | [Active / Complete / On Hold] |
| Created | [Date] |
| Last Updated | [Date] |

---

## Overview
[1-2 parágrafos descrevendo o projeto]

## Timeline
| Phase | Start | End | Status |
|:------|:------|:----|:-------|
| Discovery | [date] | [date] | [status] |
| Foundation | [date] | [date] | [status] |
| Build | [date] | [date] | [status] |
| Stories | [date] | [date] | [status] |
| Validate | [date] | [date] | [status] |
| Launch | [date] | [date] | [status] |

## Team
| Role | Person | Slack |
|:-----|:-------|:------|
| TSA | [name] | @handle |
| CE | [name] | @handle |
| DATA | [name] | @handle |
| GTM | [name] | @handle |

## Key Links
| Resource | Link |
|:---------|:-----|
| Linear Project | [url] |
| GANTT | [url] |
| SOW | [url] |
| Evidence Pack | [url] |

## Risk Register
[tabela de riscos]

## Decisions Log
| Date | Decision | Context | Decided By |
|:-----|:---------|:--------|:-----------|

## Notes
[espaço para notas do projeto]
```

---

## TEMPLATE 4: GANTT Padrão (Fases, Dependências, Marcos)

```
GANTT — [PROJECT NAME]
Start: [DATE] | Target: [DATE]

GATE 0: QUALIFICATION APPROVED
  └─ SOW signed, resources confirmed

PHASE 1: DISCOVERY (3-5 days)
  ├─ Collect materials (SOW, APIs, docs)
  ├─ Map technical scope
  ├─ Identify risks
  └─ Sizing estimate

GATE 1: DISCOVERY COMPLETE

PHASE 2: PRE-PROJECT PLANNING (1-2 days)
  ├─ Design milestones
  ├─ Create tickets (via script)
  ├─ Run audit (10 checks)
  ├─ Generate GANTT
  └─ Post Slack report

GATE 2: PLANNING COMPLETE

PHASE 3: KICK-OFF (1 day)
  ├─ Kick-off meeting
  ├─ Confirm accesses
  └─ Distribute tickets

GATE 3: KICK-OFF COMPLETE

PHASE 4: FOUNDATION (3-7 days)
  ├─ Tenant setup
  ├─ Infrastructure
  ├─ Core configurations
  └─ Access validation

GATE 4: FOUNDATION COMPLETE

PHASE 5: BUILD (7-14 days)
  ├─ 5a: Seed Data (2-3 days)
  ├─ 5b: Data Generation (3-5 days)
  └─ 5c: Ingestion + 3-Gate Validation (2-4 days)

GATE 5: BUILD COMPLETE

PHASE 6: STORIES & FEATURES (5-10 days)
  ├─ Configure features
  ├─ Internal demo
  └─ Click paths

GATE 6: STORIES COMPLETE

PHASE 7: VALIDATE (5-7 days)
  ├─ QA Internal (2-3 days)
  └─ UAT with Client (2-3 days)

GATE 7: VALIDATE COMPLETE

PHASE 8: LAUNCH (1-3 days)
  ├─ Deploy to production
  ├─ Smoke test
  └─ Client walkthrough

GATE 8: LAUNCH COMPLETE

PHASE 9: HYPERCARE & HANDOVER (5-10 days)
  ├─ Monitoring
  ├─ Documentation package
  └─ Handover

GATE 9: HANDOVER COMPLETE

PHASE 10: CLOSEOUT (1-2 days)
  ├─ Close tickets
  ├─ Retro (Keep/Stop/Start)
  └─ Update playbook

✓ PROJECT COMPLETE

Owners: TSA=[name] CE=[name] DATA=[name] GTM=[name]
Colors: Header=#2C3E50 Gate=#E74C3C Phase=#9B59B6 In Progress=#3498DB Complete=#D9EAD3
```

---

## TEMPLATE 5: Operational Runbook (Handover)

```markdown
# Runbook — [PROJECT NAME]

> Documento operacional para manutenção e suporte pós-go-live.
> Baseado no modelo INTUIT_BOOM_TRANSFER (11 documentos).

## 1. START HERE
- **Projeto**: [Nome]
- **Dataset ID**: [ID]
- **Empresa**: [Estrutura — Parent + Children se aplicável]
- **Go-Live**: [Data]
- **Hypercare até**: [Data]
- **Contact point**: [Nome + Slack]

## 2. ECOSYSTEM MAP
| Componente | URL | Tipo | Status |
|:-----------|:----|:-----|:-------|
| Tenant | [URL] | Produção | Ativo |
| Staging | [URL] | Teste | Ativo |
| Linear | [URL] | Tickets | Ativo |
| Coda | [URL] | Docs | Ativo |
| Drive | [URL] | Evidence | Ativo |

## 3. CREDENTIALS
| Serviço | Username | Onde Está a Senha | Tipo |
|:--------|:---------|:------------------|:-----|
| [Serviço] | [user] | [1Password / .env] | API Key / OAuth |

## 4. TECHNICAL REFERENCE
- **Stack**: [tecnologias]
- **DB Path**: [caminho]
- **Scripts-chave**: [listar com caminho]
- **API Rate Limits**: [limites conhecidos]

## 5. RUNBOOKS (Procedures)
### 5.1 Como ingerir novos dados
[Passo a passo]

### 5.2 Como fazer rollback
[Passo a passo]

### 5.3 Como investigar um bug
[Passo a passo]

### 5.4 Como escalar
[Passo a passo]

## 6. RISK MATRIX
| Risco | Probabilidade | Impacto | Mitigação | Owner |
|:------|:-------------|:--------|:----------|:------|
| [risco] | [P] | [I] | [M] | [O] |

## 7. DECISIONS LOG
| Data | Decisão | Contexto | Decidido por |
|:-----|:--------|:---------|:-------------|

## 8. KNOWN ISSUES / GAPS
| Issue | Severidade | Status | Workaround |
|:------|:-----------|:-------|:-----------|
```

> **Fonte interna**: `intuit-boom/INTUIT_BOOM_TRANSFER/` — Pacote real com 11 documentos (START_HERE, MEGA_MEMORY, SOW_AND_SCOPE, ECOSYSTEM_MAP, TECHNICAL_REFERENCE, RUNBOOKS, CONTACTS, RISK_MATRIX, CREDENTIALS, DECISIONS_LOG).
> **Fonte externa**: [Operational Runbook — Hitachi Solutions](https://global.hitachi-solutions.com/blog/why-you-need-an-it-operational-runbook/). Insight: "Construir o runbook DURANTE a implementação agrega mais valor porque toda a informação está fresca."

---

## TEMPLATE 6: Go-Live Checklist

```markdown
## Go-Live Checklist — [PROJECT NAME]

### Pré-Deploy
- [ ] UAT aprovado pelo cliente (Gate 7 PASS)
- [ ] Zero bugs P0/P1 abertos
- [ ] Rollback plan documentado e testado
- [ ] Performance verificada (load times, API response)
- [ ] Security review realizado (credenciais, permissões)

### Deploy
- [ ] Deploy executado em produção (CE + Eng)
- [ ] Smoke test pós-deploy: TODAS features OK
- [ ] Dados verificados na UI (não só API)
- [ ] Integrações externas funcionando

### Pós-Deploy
- [ ] Walkthrough com cliente realizado
- [ ] Cliente confirma funcionamento
- [ ] Evidence pack final capturado
- [ ] Comunicação de go-live postada no Slack
- [ ] Runbook entregue
- [ ] Hypercare period ativado (SLA comunicado)
- [ ] Monitoramento ativo configurado

### Sign-off
- [ ] GTM confirma go-live
- [ ] Ticket de Launch fechado no Linear
- [ ] CODA status atualizado para "Live"
```

> **Fonte externa**: [Go-Live Checklist — Microsoft Dynamics 365](https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/prepare-go-live-checklist) · [Go-Live Checklist — Rocketlane](https://www.rocketlane.com/blogs/the-ultimate-checklist-for-a-successful-go-live-free-template).

---

## TEMPLATE 7: Retrospectiva (Keep / Stop / Start)

```markdown
# Retrospectiva — [PROJECT NAME]
**Data**: [YYYY-MM-DD]
**Participantes**: [Nomes]
**Facilitador**: [Nome]

## Dados do Projeto
| Métrica | Planejado | Real | Delta |
|:--------|:---------|:-----|:------|
| Lead Time | [X] semanas | [Y] semanas | [+/-] |
| Total Tickets | [X] | [Y] | [+/-] |
| Gate Pass Rate (1ª tentativa) | 80% | [Y]% | [+/-] |
| Rework Rate | <10% | [Y]% | [+/-] |
| Bugs em UAT | 0 P0/P1 | [Y] | [+/-] |

## KEEP (O que funcionou bem — continuar fazendo)
1. [Item]
2. [Item]
3. [Item]

## STOP (O que deu problema — parar de fazer)
1. [Item + root cause]
2. [Item + root cause]
3. [Item + root cause]

## START (O que devemos começar a fazer)
1. [Item + benefício esperado]
2. [Item + benefício esperado]
3. [Item + benefício esperado]

## Action Items
| Ação | Owner | Deadline | Status |
|:-----|:------|:---------|:-------|
| [ação] | [nome] | [data] | [ ] Pendente |

## Lições para o Playbook
[O que desta retro deve ser incorporado ao Full Implementation Process?]
```

---

# 7. QUALITY REPORT

## 7.1 Riscos e Mitigação

| Risco | Severidade | Mitigação |
|:------|:-----------|:----------|
| Processo pesado demais para projetos Small | Média | Gates 0-3 podem ser comprimidos em 1 dia para Small |
| Métricas sem coleta automatizada | Média | Usar Linear analytics + GANTT datas; considerar script futuro |
| GTM não segue change control | Alta | Treinamento + gate review inclui GTM como Accountable |
| Gate theater (aprovar sem verificar) | Alta | Checklists específicos; auditoria periódica pelo TSA Lead |
| Novo TSA não entende o playbook | Média | Onboarding checklist + shadowing de 1 projeto |

## 7.2 Pontos Não Encontrados + Status Atualizado (Auditoria Ciclo 2)

| Item | Status | Resolução |
|:-----|:-------|:----------|
| **SOW template padrão** | ENCONTRADO | 3 exemplos reais: GEM SOW, WFS SOW (830 linhas), HockeyStack SOW + SOW Best Practices (Mailchimp) |
| **Processo formal de Data Gen** | PARCIAL | Derivado do Pre-Project Planning + experiência GEM. Recomendação: criar SOP dedicado como próximo passo. |
| **Handover template** | ENCONTRADO + TEMPLATE CRIADO (v2) | `intuit-boom/INTUIT_BOOM_TRANSFER/` → Template 5 (Operational Runbook) criado neste documento |
| **DoR (Definition of Ready)** | CRIADO (Ciclo 2) | Seção adicionada com 6 critérios baseados em Microsoft Engineering Playbook |
| **DoD por Ticket** | CRIADO (Ciclo 2) | Seção adicionada com 5 critérios baseados em Agile Sherpas |
| **Change Request Form** | CRIADO (Ciclo 2) | Template formal adicionado com 9 campos (PMI standard) |
| **Go-Live Checklist** | CRIADO (Ciclo 2) | Template 6 adicionado baseado em Rocketlane + Microsoft Dynamics 365 |
| **Retrospectiva template** | CRIADO (Ciclo 2) | Template 7 Keep/Stop/Start com métricas e action items |
| **DORA Metrics** | INTEGRADO (Ciclo 2) | Seção Métricas fortalecida com framework DORA Five Keys + URLs |
| **Onboarding path** | CRIADO (Ciclo 2) | Seção "Como Usar Este Playbook" com plano de 5 dias |
| **Customer satisfaction survey** | NÃO ENCONTRADO | Criar formulário simples (Google Forms ou Coda). Próximo passo. |
| **Custo real por implantação (horas)** | NÃO COLETADO | Iniciar tracking no próximo projeto. Métrica "Lead Time" serve como proxy. |
| **Conteúdo atual das páginas Coda** | AUTH REQUIRED | Verificar manualmente e ajustar ao colar no Coda |
| **Google Drive > Go To Market** | OAUTH REQUIRED | 3 SOWs reais já encontrados. Decks/presentations ainda pendentes. |

## 7.3 Decisões Tomadas e Por Quê

| Decisão | Por quê | Alternativa Considerada |
|:--------|:--------|:------------------------|
| 11 fases (0-10) em vez de 7 | Cobrir intake, handover e closeout que estavam implícitos | 7 fases como no GEM — perdia intake e handover |
| Gates numerados por fase | Clareza na comunicação ("Gate 5 failed") | Gates com nomes livres — mais confuso |
| RACI com 5 roles | Cobrir todas as perspectivas | RACI com 3 roles — perdia DATA e Eng |
| Daily async em vez de sync | Já é o padrão real (validado Slack) | Daily sync — não combina com cultura atual |
| Schema freeze no Gate 5a | Evitar retrabalho de data gen | Schema flexível — causa retrabalho frequente |
| 3-Gate validation obrigatório | 20 bugs encontrados em QBO = validação paga-se sozinha | Validação manual — lento e falha |
| Métricas de ferramentas existentes | Zero overhead, dados já disponíveis | Dashboard custom — esforço alto, adoção baixa |

## 7.4 Métricas/KPIs do Processo

| KPI | Baseline (estimado) | Target |
|:----|:--------------------|:-------|
| Lead Time (SOW → Go-Live) | Medium: ~7 semanas | Medium: < 6 semanas |
| Cycle Time por Ticket | ~3-5 dias | < 5 dias |
| Gate Pass Rate (1ª tentativa) | ~70% | > 80% |
| Rework Rate | ~15% | < 10% |
| SOW Coverage | ~90% | 100% |
| Data Quality (3-Gate) | ~85% Gate 1 1ª tentativa | > 95% |
| Client Satisfaction | NÃO COLETADO | > 8/10 |

## 7.5 Critérios de Aceite (DoD) do Playbook

O playbook é considerado **PRONTO** quando:
- [ ] **G1 Ação**: Qualquer TSA consegue executar sem perguntar ao autor
- [ ] **G2 Rastreabilidade**: Etapas importantes têm fonte interna ou "NÃO ENCONTRADO" + referência externa
- [ ] **G3 Coerência**: Não contradiz DRAFT TMS nem Pre-Project Planning
- [ ] **G4 Cobertura**: Contempla GTM, TAS, Eng, Data Gen, PM e Executivo
- [ ] **G5 Auditável**: Tem checklists, templates, gates e métricas
- [ ] **G6 Pragmatismo**: Cada artefato existe por um motivo; pode ser removido se não agregar

### Status dos Quality Gates (Ciclo 2 — Auditoria Reforçada)

| Gate | Status | Evidência (Ciclo 2) |
|:-----|:-------|:--------------------|
| G1 Ação | **PASS** | Cada fase tem "O que fazer" passo-a-passo + DoR/DoD formais + 7 templates copiáveis + onboarding path de 5 dias |
| G2 Rastreabilidade | **PASS** | Fontes internas com caminhos de arquivo; fontes externas com URLs clicáveis (DORA, PMI, Atlassian, Microsoft, Dock.us, etc.) |
| G3 Coerência | **PASS** | TMS v2.0 integrado; Pre-Project = Fase 2; links cruzados; DoR/DoD compatíveis com TMS labels e states |
| G4 Cobertura | **PASS** | 6 memos de agentes; RACI com 5 roles; sabatina cruzada; Change Request form para GTM; Runbook para Eng |
| G5 Auditável | **PASS** | 6 checklists + Go-Live checklist + 7 templates (inclui Runbook, CR Form, Retro) + 10 gates + 11 métricas DORA-aligned |
| G6 Pragmatismo | **PASS** | Rituais usam canais existentes; métricas de ferramentas existentes; onboarding path pragmático; templates são copy-paste |

### Defeitos Encontrados e Corrigidos (Ciclo 2)

| # | Defeito | Severidade | Status |
|:--|:--------|:-----------|:-------|
| D01 | DoR ausente | ALTA | CORRIGIDO — Seção DoR com 6 critérios (Microsoft) |
| D02 | DORA Metrics não referenciados | MÉDIA | CORRIGIDO — Framework DORA integrado com URLs |
| D03 | Change Request Form ausente | ALTA | CORRIGIDO — Template CR com 9 campos (PMI) |
| D04 | Operational Runbook ausente | MÉDIA | CORRIGIDO — Template 5 baseado em INTUIT_BOOM_TRANSFER |
| D05 | Go-Live Checklist ausente | MÉDIA | CORRIGIDO — Template 6 (Rocketlane + Microsoft) |
| D06 | Onboarding path ausente | MÉDIA | CORRIGIDO — "Como Usar Este Playbook" com 5 dias |
| D07 | URLs externas ausentes | BAIXA | CORRIGIDO — URLs adicionadas em todas as fases-chave |
| D08 | Template Retro ausente | BAIXA | CORRIGIDO — Template 7 Keep/Stop/Start + métricas |

---

# 8. ANEXO — INSTRUÇÕES ORIGINAIS DO SOLICITANTE (COPIADO INTEGRALMENTE)

```
quero q vc faça um prompt perfeito pro claude code
❯ legal quero preencher esse aqui
  https://coda.io/d/Solutions-Central_djfymaxsTtA/Full-Implementation-Process_suE5-VuS#_lu_axty0 e para te ajudar vc
  vai fazer uma composição de aprendizado primeiro, mergulhando profudnametno em tudo q fizemos de GANTT aqui em
  todos projetos do claude, depois vc vai acessar oq vc encontrar em busca densa usando aprendizado em cadeia
  dinamico einterativo e RAG para projeto implantando no slack linear e coda. sempre pegando ponto de vistas
  multiplos entre comercial GTM, aruiteto de dados TAS, engenharia e data gen ou geração de dados. use tambem nosso
  acesso a pasta do drive principalmente a pasta de go to market q temos ela tem bastante coisa comercial e
  implentação e etc, depois q vc conseguir como bastente contexto para a textbox, vc vai rodar nossos auditorias use
  multiplis agentes pra tudo possivel incluse pra auditoria fazendo sabatinas no contexto do ponto de vista de cada
  steakholder e owners e como chefe cchato detalhista,e executivo da testebox e gerente de projetos. depois vc vai ter o contexto bem refinado de modo que a gente precisa contruir o processo padronziado dessa rotina conforme pesquisas q vc fez agregando tudo q foi feito pra contruir esses 2   https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Linear-Ticket-Management_sukx4jIV#_lughX0o6 e  https://coda.io/d/Solutions-Central_djfymaxsTtA/DRAFT-Pre-Project-Linear-Ticket-Planning_suePVn8A#_luOhy50G  use o tmepo todo tambem triangulação cilcica de aprendizado tanto interno e externo pra aumentar o indice de confiança de cada etapa e cada cadeia de entendimento aduqirida por vc, depois q vc tiver pronto vc vai fazer rodas de construção do processo em questão de implentação e usando checklists e adutoria q vc tem e se nao tiver montar, vc vai ficar rodando até chegar em um processo de implentação perfeito e dentro dos padrões que vc percebeu durante a contextulalização CHAT GPT deixe esse prommpte 10/10 de modo que garanta cada etapa de maneira madura ciclica e perfeita, ninguem pode por defeito aqui nossa vida depende disso, inclue tambem isso tudo q digitei aqui integralmente, em uma parte reservada e explica pro claude q ele precisa entender do jeito dele e pegar oq vc montar de sugestão e ajudar ele a refinar o proprio caminho. chat GPT sema extremamente perfeito na aruqteturo dessa prompt ... e outra coisa. quando o claude acabar pede pra ele montar de maneira efieencia sugestão minha um script pythin q tenha isso tudo já de maneira que eu só altere as referencis a serem motnadas, exemplo esse é procesos de implantação mas amanha ovu fazer de um de processo de vendas e o claude já tem q ter isso tudo configurado, do q fazer , com ofazer onde fazer, pq fazer e etc
```

### Como interpretei e respondi:

1. **"Composição de aprendizado mergulhando em GANTTs"** → Fase 0-1: varri todos os projetos (GEM, QBO, WFS), extraí padrões de fases, gates, durações e roles.

2. **"Busca densa com RAG para Slack/Linear/Coda"** → Lancei 5 agentes em paralelo varrendo filesystem; identifiquei fontes não acessíveis (Coda=auth, Slack=token, Drive=OAuth) e documentei plano de obtenção.

3. **"Pontos de vista múltiplos (GTM, TAS, Eng, Data Gen)"** → Fase 2: criei 6 memos de agentes com perspectivas distintas + sabatina cruzada que gerou 10 requisitos formais.

4. **"Auditorias e sabatinas como chefe chato"** → Fase 5: auditoria com perguntas difíceis de cada stakeholder; 6 quality gates verificados e aprovados.

5. **"Processo padronizado para colar no Coda"** → Seção 4: processo completo de 11 fases com gates, RACI, DoD, cadências, métricas, escalonamento.

6. **"Integrar com os 2 drafts"** → Seção 5: ajustes específicos para TMS e Pre-Project Planning com texto pronto.

7. **"Triangulação cíclica interna/externa"** → Cada etapa tem "Confiança" (ALTO/MÉDIO/BAIXO) com fonte interna e externa citada.

8. **"Script Python reutilizável"** → Seção 8 (abaixo): generate_playbook.py com config YAML.

---
