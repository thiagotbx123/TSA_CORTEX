# CODA Workspace Mapping - TestBox

> Exploracao completa do workspace CODA em 2026-01-26
> Objetivo: Mapear 100% do conteudo para aprendizado e referencia

## Resumo Executivo

| Doc | Paginas | Rows | Proposito | Relevancia TSA |
|-----|---------|------|-----------|----------------|
| **Solutions Central** | 114 | 327 | Hub de clientes TSA | **CRITICA** |
| **Integrations Central** | 503 | 6977 | Detalhes tecnicos integracoes | ALTA |
| **Product and Dev** | 586 | 3202 | Produto TestBox | MEDIA |
| **Go-To-Market** | 217 | 611 | Vendas/Marketing | BAIXA |
| **Developers** | 153 | 315 | Dev interno | MEDIA |
| **TestBox** | 54 | 1648 | Cultura/Handbook | BAIXA |
| Gayathri's Playground | 19 | 109 | Sandbox | BAIXA |

## Solutions Central (jfymaxsTtA) - PRINCIPAL

### Estrutura de Clientes (24 mapeados)

| Cliente | Status | TSA Atual | Ultima Atualizacao |
|---------|--------|-----------|---------------------|
| Apollo | ATIVO | Carlos | 2026-01 |
| Archer | ATIVO | - | - |
| Assembled | ATIVO | - | - |
| Assignar | ATIVO | - | - |
| **Brevo** | ATIVO | Diego | 2026-01 |
| **CallRail** | ATIVO | Diego | 2026-01 |
| **Dixa** | ATIVO | Gabrielle | 2026-01 |
| Gainsight | ATIVO | - | - |
| Gem | **OFF** | - | Desativado |
| **Gong** | ATIVO | Carlos | 2026-01 |
| HockeyStack | **OFF** | - | Desativado |
| **QuickBooks** | ATIVO | Thiago | 2026-01 |
| **MailChimp** | ATIVO | Gabrielle | 2026-01 |
| JupiterOne | ATIVO | - | - |
| **mParticle** | ATIVO | Alexandra | 2026-01 |
| **People.AI** | ATIVO | Diego | 2026-01 |
| Onyx | ATIVO | - | - |
| SiteImprove | ATIVO | - | - |
| **Syncari** | ATIVO | Alexandra | 2026-01 |
| Tabs | ATIVO | - | - |
| Tropic | ATIVO | - | - |
| **Zendesk** | ATIVO | Gabrielle | 2026-01 |
| Zuper | ATIVO | - | - |

### Subpaginas por Cliente (padrao)

Cada cliente tem estrutura similar:
- Customer Overview
- Maintained Accounts
- Instance Creation & Ingestion Playbook
- Dataset
- Running Automations
- Customer Contact Information
- Feature by Feature

### Paginas Operacionais

| Pagina | Conteudo | Utilidade |
|--------|----------|-----------|
| **Glossary** | Termos TestBox | ALTA |
| **Reporting and Resolving Customer Blockers** | Processo de blockers | CRITICA |
| **Post-Launch Customer Request Process** | Processo pos-launch | ALTA |
| **Implementation Timelines** | Customer Systems | ALTA |
| **AI Prompts** | Prompts padronizados | MEDIA |
| **Meeting Cadence & Routines** | Rotinas de reuniao | MEDIA |

## Integrations Central (bd-guBL5H_) - TECNICO

### Categorias Principais

1. **Customer Overview & Details** - Visao geral clientes
2. **Customer Experience QA Tracker** - QA de experiencia
3. **Integration Status Tracker** - Status integracoes
4. **Customer Support** - Suporte (Zendesk detalhado)
5. **Marketing Automation** - Automacao marketing
6. **CRM** - CRMs integrados
7. **Project Management** - Ferramentas de PM
8. **Knowledge Center** - Base conhecimento
9. **Customer Success** - CS integracoes
10. **Data Set Rules** - Regras de dados
11. **Solution Pods** - Pods de solucao

### Tabelas Criticas

| Tabela | Colunas | Uso |
|--------|---------|-----|
| **Integration phasing** | Product, Proxy, State, Phase, Extension, Saturn, SDK, Convert | Status de cada integracao |
| **States** | Lookup de estados | Referencia |
| **Verticals** | Lookup de verticais | Referencia |
| **Customer Support Product Details** | Detalhes por produto | Suporte |

### Estrutura por Integracao (ex: Zendesk)

Cada integracao tem:
- Overview Expected Behavior
- Dev Items
- In Action (Appcues)
- In Action Steps
- Config
- Config Steps
- Omnichannel (Talk, Text)
- Chatbot

## Product and Dev (kBndzxmj8u)

### Estrutura Principal

1. **Intro** - Introducao ao produto
2. **Onboarding plan** - Plano onboarding
3. **TestBox Glossary** - Glossario tecnico
4. **TestBox Product Vision & Strategy**
   - Overall Product Strategy
   - TestBox Compare
   - Vendor onboarding
   - Roadmap

### Proposito

- Documentacao interna do produto
- Estrategia de produto
- Onboarding de devs
- Roadmap tecnico

## TestBox (OGqm7Zlwsu) - CULTURA

### Estrutura

1. **TestBox Strategy in 2024** - Estrategia anual
2. **How We Work Together**
   - Company Values
   - TestBox Handbook
   - Company Meetings
   - Onsites
   - Team Co-Locations
   - Celebrating Our Wins
   - Company Tools
   - Daily Puzzles

### Proposito

- Documento de cultura
- Handbook da empresa
- Valores
- Processos internos

## Aprendizados Chave

### 1. Hierarquia de Documentos

```
TestBox (cultura)
    └── Product and Dev (produto)
        └── Integrations Central (tecnico)
            └── Solutions Central (operacional TSA)
```

### 2. Padroes de Nomenclatura

- `[OFF]` = Cliente desativado (ex: Gem_[OFF])
- `[Archive]` = Conteudo arquivado
- `Copy of X` = Duplicata/Template

### 3. Owners por Area

| Area | Owner Principal |
|------|-----------------|
| Solutions Central | Lucas Wakigawa |
| Integrations Central | Sam Senior |
| Product and Dev | Nora Nguyen |
| TestBox | Sam Senior |

### 4. Frequencia de Atualizacao

| Doc | Ultima Atualizacao | Frequencia |
|-----|---------------------|------------|
| Solutions Central | 2026-01-24 | DIARIA |
| Integrations Central | 2025-12-16 | MENSAL |
| Product and Dev | 2026-01-22 | SEMANAL |
| TestBox | 2026-01-12 | ESPORADICA |

## O que Ainda e Util

### CRITICO (usar sempre)
- Solutions Central - Customer Overview
- Solutions Central - Glossary
- Solutions Central - Blockers Process
- Integrations Central - Integration Status Tracker

### UTIL (consultar quando necessario)
- Product and Dev - TestBox Glossary
- Product and Dev - Onboarding plan
- Integrations Central - Detalhes por integracao

### HISTORICO (referencia)
- TestBox - Company Values
- TestBox - Handbook

### OBSOLETO (ignorar)
- Gayathri's Playground
- Clientes [OFF]
- Paginas [Archive]

## APIs de Acesso

```bash
# Listar docs
GET https://coda.io/apis/v1/docs

# Listar paginas de um doc
GET https://coda.io/apis/v1/docs/{docId}/pages

# Listar tabelas
GET https://coda.io/apis/v1/docs/{docId}/tables

# Obter dados de tabela
GET https://coda.io/apis/v1/docs/{docId}/tables/{tableId}/rows
```

## Proximos Passos

1. [ ] Mapear Linear (Task #6)
2. [ ] Criar scripts de extracao automatica
3. [ ] Sincronizar glossario com knowledge-base
4. [ ] Documentar processo de blocker em SOP

---

**Mapeamento realizado:** 2026-01-26
**Total de paginas exploradas:** 1527+
**Total de rows:** 13,189
