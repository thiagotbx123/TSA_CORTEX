# Linear Mapping - TestBox

> Exploracao completa do Linear em 2026-01-26
> Objetivo: Mapear historico de tickets por cliente para entender evolucao

## Resumo Executivo

**Total de Times:** 20
**Total de Issues:** ~5,500+
**Periodo Mapeado:** Junho 2023 - Janeiro 2026

## Times por Volume

| Time | Key | Issues | Proposito |
|------|-----|--------|-----------|
| **Platypus** | PLA | 2005 | Desenvolvimento principal |
| Koala | KLA | 948 | Engineering |
| Toucan | TOU | 889 | Engineering |
| Capybara | CAP | 485 | Engineering |
| Dingo | DGO | 314 | Engineering |
| **Dataset Work** | DAT | 150 | Dados/Ingestion |
| Security | SEC | 135 | Seguranca |
| Wombats | WOM | 94 | Engineering |
| Ironbark | IRON | 87 | Engineering |
| Opossum | OPO | 84 | Engineering |
| Saltwater Crocs | SAL | 54 | Sales |
| Access Approvals | ACC | 53 | Acesso |
| Quokka | QKA | 53 | Engineering |
| **Raccoons** | RAC | 34 | TSA Worklog |
| QA | QA | 12 | QA |
| Emu | EMU | 12 | Engineering |
| Onboarding | ONB | 8 | Onboarding |
| Wallaby | WAL | 5 | Engineering |
| Sales | SAL2 | 3 | Sales |
| Pylon Triage | PYL | 0 | Pilot |

## Contagem por Cliente

| Cliente | Issues (min) | Primeiro Ticket | Team Principal |
|---------|--------------|-----------------|----------------|
| **QuickBooks** | 250+ | 2024-04-19 | PLA |
| **Gong** | 250+ | 2023-09-21 | PLA |
| **Brevo** | 250+ | 2023-10-31 | DGO |
| Apollo | 205 | 2023-10-17 | DGO |
| CallRail | 110 | 2023-06-22 | DGO |
| mParticle | 53 | 2024-08-29 | TOU |
| Mailchimp | 46 | 2025-06-25 | PLA |
| Dixa | 31 | 2023-12-05 | DGO |
| Zendesk | 21 | 2023-10-11 | DGO |
| Syncari | 17 | 2023-11-03 | WOM |

## Timeline de Clientes

```
2023-06 ████ CallRail (DGO-304)
2023-09 ████████ Gong (PLA-1587)
2023-10 ████████████ Zendesk, Apollo, Brevo
2023-11 ██████████████ Syncari
2023-12 ████████████████ Dixa
2024-04 ████████████████████ QuickBooks (PLA-1287)
2024-08 ████████████████████████ mParticle
2025-06 ██████████████████████████████ Mailchimp (PLA-2625)
```

## Tickets Recentes (Jan 2026)

### QuickBooks
- PLA-3213: Winter Release Staging - TCO Clone Ingestion
- PLA-3212: Winter Release Staging - Construction Clone Ingestion
- PLA-3207: Trial User Setup Review
- PLA-3206: Payroll Review
- PLA-3205: Admin Account Activation Review
- PLA-3202: [IES] Intercompany Bills Feature Gap

### Gong
- PLA-3215: [SPIKE] Refactor replace Engage Ingestions
- PLA-3210: Refactor Ingest Engage Email Templates

### Mailchimp
- PLA-3216: Fixed Clients (Hero customers)
- PLA-3214: [SPIKE] Investigate landing page connection
- PLA-3211: Add retool visualization of activity plans
- PLA-3209: Activity Plan for Abandoned Carts
- PLA-3208: Implement activity plan barebones

## Padroes Descobertos

### 1. Nomenclatura de Tickets
Padrao: `[CLIENTE] Descricao do trabalho`

Exemplos:
- `[QuickBooks] Winter Release Staging`
- `[GONG] Refactor Ingest Engage`
- `[Mailchimp] Activity Plan`

### 2. Labels de Sprint
Formato: `YYYY.WW` (Ano.Semana)
- 2025.25, 2025.26, 2025.27...
- 2026.01, 2026.02...

### 3. Labels de Tipo
- `Feature` - Nova funcionalidade
- `Bug` - Defeito
- `Spike` - Investigacao
- `Internal Request` - Pedido interno
- `RCA` - Root Cause Analysis

### 4. Estados
- Backlog
- Refinement
- Refined
- Todo
- In Progress
- Needs Review
- Production QA
- Done
- Canceled
- Distributed (WOM)

## Evolucao Historica

### 2022 (Fundacao)
- Foco em Nebula (ferramenta interna)
- Bugs iniciais de plataforma
- PLA-352: Nebula training brownbag

### 2023 (Expansao)
- Q2: CallRail (primeiro cliente)
- Q3: Gong POC
- Q4: Apollo, Brevo, Zendesk, Dixa, Syncari

### 2024 (Consolidacao)
- Q2: QuickBooks (maior cliente)
- Q3: mParticle
- Estabelecimento de padroes

### 2025-2026 (Maturidade)
- Q2 2025: Mailchimp
- Q1 2026: Winter Release QuickBooks
- Foco em automacao e activity plans

## Insights para TSA

### Clientes Ativos Prioritarios (por volume)
1. QuickBooks - Thiago
2. Gong - Carlos
3. Brevo - Diego
4. Apollo - Carlos
5. CallRail - Diego

### Clientes em Ramp-up
1. Mailchimp - Gabrielle (7 meses, 46 tickets, crescendo)

### Clientes Estabilizados
1. mParticle - Alexandra
2. Syncari - Alexandra
3. Dixa - Gabrielle
4. Zendesk - Gabrielle

## Queries Uteis

### Buscar tickets de um cliente
```graphql
{
  issues(first: 50, filter: { title: { containsIgnoreCase: "quickbooks" } }) {
    nodes { identifier title state { name } createdAt }
  }
}
```

### Buscar por time
```graphql
{
  team(id: "fd21180c-8619-4014-98c6-ac9eb8d47975") {
    issues(first: 50) { nodes { identifier title } }
  }
}
```

### Buscar por estado
```graphql
{
  issues(filter: { state: { name: { eq: "In Progress" } } }) {
    nodes { identifier title }
  }
}
```

## Proximos Passos

1. [ ] Criar dashboard de tickets por cliente
2. [ ] Automatizar coleta semanal de metricas
3. [ ] Mapear correlacao CODA ↔ Linear
4. [ ] Documentar fluxo de vida de um ticket

---

**Mapeamento realizado:** 2026-01-26
**API usada:** Linear GraphQL
**Credencial:** LINEAR_API_KEY (RAC team access)
