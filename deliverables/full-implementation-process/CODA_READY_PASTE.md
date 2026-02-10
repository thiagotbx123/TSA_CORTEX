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
