# Ticket Management System
## TSA TestBox - O Jeito Certo de Fazer as Coisas

```
 _____ _      _        _     __  __                                            _
|_   _(_) ___| | _____| |_  |  \/  | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_
  | | | |/ __| |/ / _ \ __| | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
  | | | | (__|   <  __/ |_  | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_
  |_| |_|\___|_|\_\___|\__| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
                                                     |___/
```

> **Versao:** 1.0 Draft
> **Data:** 2026-01-26
> **Autor:** Thiago Rodrigues
> **Escopo:** TSA/Platypus Team
> **Vibe:** Organizado, mas sem neura

---

## Por que este documento existe?

Porque "ah, depois eu documento" nunca funciona. E porque quando um ticket some no limbo, todo mundo sofre - o cliente, o dev, e voce que vai ter que explicar o que aconteceu.

Este sistema existe para que **qualquer pessoa** possa olhar um ticket e entender:
- O que precisa ser feito
- Por que importa
- Quem esta cuidando
- Quando vai ficar pronto (ou pelo menos um chute honesto)

---

## Indice

- [A. O Fluxo (End-to-End)](#a-o-fluxo-end-to-end)
- [B. Quem Faz O Que](#b-quem-faz-o-que)
- [C. Padrao Linear](#c-padrao-linear)
- [D. CODA (Nossa Wiki)](#d-coda-nossa-wiki)
- [E. Templates](#e-templates)
- [F. Quality Gates](#f-quality-gates)
- [G. Metricas](#g-metricas)
- [Recursos e Contatos](#recursos-e-contatos)

---

## A. O Fluxo (End-to-End)

### O Ciclo de Vida de um Ticket

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│   "Ei, algo                                                                         │
│    quebrou!"     INTAKE ──▶ TRIAGE ──▶ DUE DILIGENCE ──▶ TICKET ──▶ EXECUTION      │
│        │                                                                  │          │
│        │                                                                  ▼          │
│        │                                                            MONITORING      │
│        │                                                                  │          │
│        │                                                                  ▼          │
│   "Obrigado,     RETRO ◀── CLOSEOUT ◀── DELIVERY ◀── VALIDATION ◀────────┘          │
│    ficou otimo!"                                                                     │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

**TL;DR:** Alguem pede → a gente entende → a gente faz → a gente entrega → a gente aprende.

---

### 1. INTAKE - "Houston, Temos um Problema"

**O que e:** O momento que alguem grita por ajuda (educadamente, esperamos).

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│   [Customer]  [Interno]  [Sentry]  [CODA Request]     │
│       │           │          │           │            │
│       └───────────┴──────────┴───────────┘            │
│                       │                               │
│                       ▼                               │
│            ┌──────────────────┐                       │
│            │  REGISTRAR       │                       │
│            │  - Quem?         │                       │
│            │  - O que?        │                       │
│            │  - Urgente?      │                       │
│            └────────┬─────────┘                       │
│                     │                                 │
│                     ▼                                 │
│            [ATRIBUIR TSA OWNER]                       │
│                     │                                 │
│                     ▼                                 │
│               [→ TRIAGE]                              │
│                                                       │
└────────────────────────────────────────────────────────┘
```

**De onde vem:**

| Fonte | Canal | Quem Pega |
|-------|-------|-----------|
| Cliente pedindo algo | #customer-requests | TSA do cliente |
| Time interno | #tsa-internal | Quem viu primeiro |
| Sentry gritando | Alerts | TSA de plantao |
| CODA Post-Launch | Feature request formal | TSA do cliente |
| Escalacao | #escalations | TSA Lead |

**Regra de ouro:** Toda demanda precisa ter dono em ate 4h (horario comercial). Sem dono = problema.

---

### 2. TRIAGE - "Qual o Tamanho do Incendio?"

**O que e:** Decidir se e um incendio de verdade ou so fumaca.

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│            ┌──────────────────┐                        │
│            │   AVALIAR:       │                        │
│            │   Impacto +      │                        │
│            │   Urgencia       │                        │
│            └────────┬─────────┘                        │
│                     │                                  │
│         ┌──────────┬┴──────────┐                       │
│         ▼          ▼           ▼                       │
│       [P0]       [P1]        [P2/P3]                  │
│    "PARA TUDO"  "Hoje"     "Sprint"                   │
│         │          │           │                       │
│         └──────────┴───────────┘                       │
│                     │                                  │
│                     ▼                                  │
│            [Precisa investigar?]                       │
│              Sim → Due Diligence                       │
│              Nao → Ticket direto                       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Sistema de Prioridades - Sem Enrolacao:**

| Prioridade | Traducao | Quando Usar | Exemplo Real |
|:----------:|----------|-------------|--------------|
| **P0** | "Largue tudo e venha" | Producao quebrada, cliente enterprise parado | Sistema fora do ar, dados corrompidos |
| **P1** | "Precisa ser hoje" | Funcionalidade critica falhando | Login quebrado, ingestion parou |
| **P2** | "Essa semana" | Problema real, mas tem workaround | Bug afetando alguns usuarios |
| **P3** | "No sprint" | Melhoria ou feature nova | Tech debt, otimizacoes |

**Matriz de Decisao (pra quem gosta de tabela):**

| | Urgencia Critica | Urgencia Alta | Urgencia Normal |
|---|:---:|:---:|:---:|
| **Impacto Critico** | P0 | P1 | P1 |
| **Impacto Alto** | P1 | P1 | P2 |
| **Impacto Medio** | P1 | P2 | P3 |
| **Impacto Baixo** | P2 | P3 | P3 |

---

### 3. DUE DILIGENCE - "Vamos Entender Antes de Sair Fazendo"

**O que e:** Investigar o problema de verdade antes de criar ticket. Nada de chutar.

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│   ┌──────────────┐    ┌──────────────┐                │
│   │  REPRODUZIR  │───▶│  MAPEAR      │                │
│   │  o problema  │    │  - Quem afeta│                │
│   └──────────────┘    │  - Desde qdo │                │
│          │            │  - Relaciona │                │
│          │            │    com o que?│                │
│          ▼            └──────┬───────┘                │
│   [Nao consegui]             │                        │
│        │                     ▼                        │
│        ▼            ┌──────────────┐                  │
│   [Pedir mais      │  COLETAR     │                  │
│    contexto]       │  EVIDENCIAS  │                  │
│                    │  - Logs      │                  │
│                    │  - Sentry    │                  │
│                    │  - Screenshot│                  │
│                    └──────┬───────┘                  │
│                           │                          │
│                           ▼                          │
│                   [HIPOTESE/SOLUCAO]                 │
│                           │                          │
│                           ▼                          │
│                     [→ TICKET]                       │
│                                                      │
└────────────────────────────────────────────────────────┘
```

**Quando fazer:**
- P0 e P1: **Sempre** (obrigatorio)
- P2: Se a causa nao for obvia
- P3: So se for algo misterioso

**Checklist rapido:**
- [ ] Consegui reproduzir?
- [ ] Sei quem/quanto afeta?
- [ ] Ja teve ticket similar? (busca no Linear)
- [ ] Depende de outro time?
- [ ] Tenho uma ideia de solucao?
- [ ] Juntei evidencias?

---

### 4. TICKET CREATION - "Agora Sim, Bora Criar"

**O que e:** Criar um ticket que qualquer pessoa consiga entender.

**Formato padrao:**

```markdown
## Overview
[O QUE esta acontecendo + POR QUE importa]
[Link pra thread/CODA se tiver]

## Requirements
* [O que precisa fazer - seja especifico]
* [Outro requisito]

## Acceptance Criteria
* [Como sabemos que ta pronto - mensuravel]
* [Outro criterio]

## References
- [Links relevantes]
```

**Titulo:**
```
[CLIENTE] Verbo + Objeto

Exemplos bons:
[QuickBooks] Fix failing login task
[Gong] Refactor Engage email templates
[SPIKE] Investigate landing page issues
[CORTEX] Document worklog process
```

**Campos obrigatorios no Linear:**

| Campo | O que colocar |
|-------|---------------|
| Title | `[Cliente] Descricao` |
| Team | Platypus (PLA) |
| Priority | P0/P1/P2/P3 |
| Labels | Sprint (`2026.02`) + Tipo (`Bug`) |
| State | Backlog |

---

### 5. EXECUTION - "Mao na Massa"

**Fluxo de estados no Linear:**

```
[Backlog] ──▶ [Refinement] ──▶ [Refined] ──▶ [Todo]
                                              │
                                              ▼
                                        [In Progress]
                                         /    │    \
                                        /     │     \
                                       ▼      ▼      ▼
                                [Blocked] [Paused]  [PR]
                                        \     │     /
                                         \    │    /
                                          ▼   ▼   ▼
                                       [Needs Review]
                                             │
                                             ▼
                                     [Ready for Deploy]
                                             │
                                             ▼
                                      [Production QA]
                                             │
                                             ▼
                                          [Done] 🎉
```

**Regras:**
- Nao pula estado sem justificativa
- Blocked = tem que explicar POR QUE
- Paused = so com OK do Lead

---

### 6. MONITORING - "Nao Deixa Morrer no Limbo"

**O que e:** Ficar de olho pra garantir que o ticket ta andando.

**Cadencia por prioridade:**

| Prioridade | Com que frequencia olhar | Por que |
|:----------:|--------------------------|---------|
| **P0** | Constantemente | E emergencia, larguei tudo |
| **P1** | Varias vezes ao dia | Urgente, precisa sair |
| **P2** | Todo dia | Importante, mas controlado |
| **P3** | Standup/Review | Vai no ritmo normal |

**Quando um ticket para (stalled):**

1. **Descobre o motivo** - Bloqueio? Duvida? Sobrecarga?
2. **Desbloqueia** - Responde pergunta, aciona dependencia, renegocia
3. **Escala se precisar** - Nao consegue resolver? Chama o Lead
4. **Documenta** - Registra o que aconteceu no ticket

*Ticket parado = cliente esperando = problema.*

---

### 7-9. VALIDATION → DELIVERY → CLOSEOUT

**Validation:** Garante que atende os criterios de aceite antes de ir pra prod.

**Delivery:** Deploya e fica de olho na estabilidade.

**Closeout:**
- Muda pra Done
- Adiciona comentario final explicando o que foi feito
- Avisa stakeholders
- CODA atualizado se precisar

---

### 10. RETRO - "O Que Aprendemos?"

**Quando fazer:**
- Todo P0 (obrigatorio)
- P1 que demorou mais que o esperado
- Qualquer coisa que foi caotica

**Template simples:**

```markdown
## Ticket: PLA-XXXX - [Titulo]

### Timeline
- Entrada: DD/MM
- Resolucao: DD/MM
- Total: X dias

### O que funcionou
- [coisa boa 1]

### O que melhorar
- [coisa a melhorar 1]

### Acoes
- [ ] [Acao] - @responsavel - prazo
```

---

## B. Quem Faz O Que

### RACI (Quem e Dono de Que)

| Etapa | Requestor | TSA | Eng | QA |
|-------|:---------:|:---:|:---:|:--:|
| Intake | **R** | A | I | - |
| Triage | C | **R/A** | I | - |
| Due Diligence | I | **R/A** | C | - |
| Ticket | I | **R/A** | C | - |
| Execution | - | I | **R/A** | I |
| Monitoring | I | **R** | A | I |
| Validation | - | C | I | **R/A** |
| Closeout | I | **R/A** | I | I |

**R** = Faz | **A** = Responsavel final | **C** = Consultar | **I** = Informar

---

### TSA por Cliente

| Cliente | TSA Owner | Backup |
|---------|-----------|--------|
| QuickBooks | Thiago Rodrigues | Diego |
| Gong | Carlos | Thiago Rodrigues |
| Apollo | Carlos | Diego |
| Brevo | Diego | Carlos |
| CallRail | Diego | Carlos |
| People.ai | Diego | Gabrielle |
| Dixa | Gabrielle | Alexandra |
| Zendesk | Gabrielle | Alexandra |
| Mailchimp | Gabrielle | Diego |
| mParticle | Alexandra | Gabrielle |
| Syncari | Alexandra | Gabrielle |

---

## C. Padrao Linear

### Prioridades

| | Nome | Traducao |
|:-:|------|----------|
| **P0** | Emergencia | Sistema pegando fogo |
| **P1** | Urgente | Precisa sair hoje |
| **P2** | Alta | Essa semana |
| **P3** | Normal | No sprint |

### Labels

| Label | Quando Usar |
|-------|-------------|
| `Bug` | Algo quebrou |
| `Feature` | Coisa nova |
| `Spike` | Investigacao |
| `RCA` | Analise pos-incidente |
| `Internal Request` | Pedido interno |
| `Customer Request` | Pedido do cliente |
| `Technical Debt` | Refatoracao |
| `Worklog` | Documentacao/Processo |

### Definition of Ready (DoR)

Ticket pronto pra sprint quando:
- [ ] Titulo padrao
- [ ] Overview explica o problema
- [ ] Requirements claros
- [ ] Acceptance Criteria mensuraveis
- [ ] Prioridade definida
- [ ] Labels aplicadas

### Definition of Done (DoD)

Ticket fechado quando:
- [ ] Acceptance Criteria OK
- [ ] Em producao (se aplicavel)
- [ ] Testes passando
- [ ] Stakeholders avisados
- [ ] Comentario final no ticket

---

## D. CODA (Nossa Wiki)

### Onde as Coisas Estao

| Processo | Onde Fica | Quando Usar |
|----------|-----------|-------------|
| Post-Launch Request | Solutions Central | Novos pedidos de cliente |
| Blockers | Customer page | Documentar bloqueios |
| Playbooks | Por cliente | Setup/Ingestion |

### Estrutura de Cliente

```
[Cliente]/
├── Customer Overview    ← Status geral
├── Maintained Accounts  ← Contas ativas
├── Instance Creation    ← Como fazer setup
├── Dataset              ← Dados
├── Running Automations  ← O que ta rodando
└── Feature by Feature   ← Status por feature
```

---

## E. Templates

### Matriz Rapida

| # | Template | Uso | Campos Principais |
|:-:|----------|-----|-------------------|
| 1 | Bug | Algo quebrou | Problema, Impacto, Evidencia |
| 2 | Feature | Coisa nova | Objetivo, Requisitos, Out of Scope |
| 3 | Spike | Investigacao | Pergunta, Timebox |
| 4 | RCA | Pos-incidente | Timeline, Root Cause |
| 5 | Internal | Pedido interno | Solicitante, Justificativa |
| 6 | Customer | Pedido cliente | Cliente, Urgencia |
| 7 | Tech Debt | Refatoracao | Current/Desired State |
| 8 | Deploy | Releases | Changes, Rollback |
| 9 | Onboarding | Setup cliente | Pre-req, Steps |
| 10 | Worklog | Documentacao | Contexto, Artefatos, Learnings |

*(Templates completos nos arquivos de referencia)*

---

### Template 1: Bug Report

```markdown
## Overview
**Problema:** [O que ta quebrado]
**Impacto:** [Quem ta sofrendo]
**Frequencia:** [Sempre/As vezes/Uma vez]
**Evidencia:** [Link Sentry/log/screenshot]

## Requirements
* Identificar root cause
* Corrigir
* Testes pra nao voltar

## Acceptance Criteria
* Nao reproduz mais
* Testes passando
* Evidencia em prod

## References
- Sentry: [link]
```

---

### Template 10: Worklog/CORTEX

```markdown
## Overview
**Tipo:** [Documentacao/Automacao/Processo]
**Contexto:** [Por que estamos fazendo isso]
**Sistema:** CORTEX

## Objetivo
[O que queremos alcançar]

## Escopo
* [O que ta incluido]
* **Fora:** [O que NAO ta]

## Artefatos
| O que | Onde | Status |
|-------|------|--------|
| [item] | [path] | [Draft/Final] |

## Learnings
* [O que descobrimos]

## Proximos Passos
- [ ] [Acao]

## Acceptance Criteria
* Funcional
* Revisado
* Commitado
```

---

## F. Quality Gates

### Resumo Rapido

| Gate | Transicao | O que precisa | Quem aprova |
|:----:|-----------|---------------|-------------|
| 1 | Intake → Triage | Contexto, TSA owner | TSA |
| 2 | Triage → DD/Ticket | Prioridade | TSA |
| 3 | DD → Ticket | Problema entendido | TSA |
| 4 | Ticket → Refinement | DoR OK | TSA + Eng |
| 5 | Refinement → Refined | Estimativa | Eng Lead |
| 6 | Exec → Review | Codigo + testes | Dev |
| 7 | Review → Deploy | PR aprovado | Reviewer |
| 8 | Deploy → QA | Smoke tests | DevOps |
| 9 | QA → Done | DoD OK | QA/TSA |
| 10 | Done → Retro | Learnings | TSA Lead |

---

## G. Metricas

### O Que Medimos

| Tipo | Metrica | Meta |
|------|---------|------|
| **Volume** | Criados/semana | Baseline |
| | Fechados/semana | >= criados |
| | Tamanho backlog | Estavel |
| **Qualidade** | DoR compliance | > 95% |
| | DoD compliance | > 95% |
| | Reopen rate | < 5% |
| **Velocidade** | Lead time P0/P1 | Minimizar |
| | SLA compliance | > 90% |

### Quando Revisamos

| Cerimonia | Frequencia | Quem | Foco |
|-----------|------------|------|------|
| Standup | Diaria | TSA | Bloqueios |
| Sprint Review | 2 semanas | TSA + Eng | Entregas |
| Metrics Review | Mensal | TSA Lead | KPIs |
| Process Retro | Trimestral | Todos | Melhoria |

---

## Recursos e Contatos

```
╔═══════════════════════════════════════════════════════════════════════╗
║                         ONDE ACHAR AS COISAS                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  LINEAR           https://linear.app/testbox/team/PLA                ║
║                   Onde vivem os tickets                               ║
║                                                                       ║
║  CODA             https://coda.io/d/_djfymaxsTtA                     ║
║                   Documentacao de clientes                            ║
║                                                                       ║
║  SLACK            #tsa-internal      → Time TSA                      ║
║                   #customer-requests → Pedidos                        ║
║                   #tsa-bugs          → Bugs                          ║
║                   #escalations       → Urgencias                      ║
║                                                                       ║
║  GITHUB           TestBoxLab/integrations                            ║
║                   Codigo das integracoes                              ║
║                                                                       ║
║  CORTEX           C:\Users\adm_r\Projects\TSA_CORTEX                 ║
║                   Automacao e docs do TSA                             ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════╗
║                           QUEM CHAMAR                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  THIAGO RODRIGUES                                                    ║
║  TSA Lead | @thiago                                                  ║
║  QuickBooks, Padronizacao, Metricas                                  ║
║                                                                       ║
║  ─────────────────────────────────────────────────────────────────   ║
║                                                                       ║
║  LUCAS WAKIGAWA                                                      ║
║  Solutions Manager | @waki                                           ║
║  Estrategia, Escalacoes, Alinhamento Executivo                       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

### Historico

| Versao | Data | Autor | O que mudou |
|--------|------|-------|-------------|
| 1.0 | 2026-01-26 | Thiago Rodrigues | Versao inicial - "Chega de bagunca" |

---

*"Um bom processo e aquele que ninguem percebe, porque simplesmente funciona."*

**Fim do Documento** 🚀

