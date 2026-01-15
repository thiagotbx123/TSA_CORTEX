# Learning: Strategic Patterns Consolidation for TSA/QBO

**Data:** 2026-01-15
**Contexto:** Investigacao profunda de TSA_CORTEX e GOD_EXTRACT para extrair padroes aplicaveis ao trabalho de TSA no QuickBooks

---

## Projetos Analisados

| Projeto | Funcao | Maturidade |
|---------|--------|------------|
| TSA_CORTEX | Automacao de worklog semanal | Production |
| GOD_EXTRACT | Extracao estrategica de documentos | Research |

---

## Padroes Estrategicos Descobertos

### 1. Strategic Cortex Pattern (TSA_CORTEX)

**O que e:** Framework de 5 outputs para inteligencia estrategica consolidada.

**Outputs:**
- **A: Executive Snapshot** - Status rapido, riscos, blockers
- **B: Strategic Map** - Conexoes e arquitetura
- **C: Knowledge Base JSON** - Dados estruturados
- **D: Keyword Map + Recipes** - Busca rapida
- **E: Delta Summary** - Detectar mudancas

**Aplicacao QBO/TSA:**
- Usar para onboarding de novos TSAs em conta Intuit
- Gerar snapshots semanais do estado de cada ambiente
- Mapear dependencias entre datasets e features

### 2. SpineHub Content Pattern (TSA_CORTEX)

**O que e:** Camada intermediaria que transforma metadata em narrativa.

**Principio:** `Conteudo > Metadata`

```
ERRADO: "SOW_WFS_v2.docx [ref:4]"
CERTO: "Negociacao do Statement of Work para WFS Phase 2,
        incluindo 6 stories e timeline de 12 semanas"
```

**Aplicacao QBO/TSA:**
- Ao documentar tickets Linear, descrever o PROBLEMA, nao so listar evidencias
- Worklogs devem contar historias, nao listar arquivos
- Learnings devem explicar o POR QUE, nao so o O QUE

### 3. Document Classification Pattern (GOD_EXTRACT)

**O que e:** Sistema automatico de classificacao de documentos.

**Dimensoes:**
- **Relevance:** high/medium/low (baseado em keywords)
- **Doc Role:** contract, strategy, roadmap, customer, security, etc.
- **Confidentiality:** public, internal, confidential
- **Topic Tags:** automaticas baseadas em path e nome

**Keywords de Alta Relevancia:**
```
strategy, roadmap, sow, msa, dpa, contract, pricing,
okr, kpi, soc, security, onboarding, playbook, master,
tracker, template, process, architecture, decision, plan
```

**Aplicacao QBO/TSA:**
- Ao organizar documentos de cliente, usar essas categorias
- Priorizar leitura de docs com keywords de alta relevancia
- Criar trackers de documentos por doc_role

### 4. Cross-Dataset Validation Pattern (TSA_CORTEX + PLA-3135)

**O que e:** Validacao de integridade referencial entre datasets.

**Regra:** Em Multi-Entity QBO, account_ids sao unicos por dataset, NAO globais.

**Query de Deteccao:**
```sql
SELECT *
FROM ENTITY_LINE L
JOIN HEADER H ON H.id = L.header_id
JOIN REFERENCE R ON R.id = L.reference_id
WHERE R.dataset_id != H.dataset_id
```

**Aplicacao QBO/TSA:**
- SEMPRE validar dataset_id antes de inserir dados
- Contas intercompany (Due to/Due from) sao especificas do ambiente
- Ao migrar dados, mapear IDs para o dataset correto

### 5. Evidence-First Processing Pattern (TSA_CORTEX)

**O que e:** Workflow de validacao que prioriza coleta de evidencias.

**Pipeline:**
```
1. COLLECT   - Dados brutos de multiplas fontes
2. CLASSIFY  - Categorizar por relevancia
3. VALIDATE  - Verificar contra criterios
4. EVIDENCE  - Capturar screenshots/logs
5. REPORT    - Gerar tracker com links
```

**Aplicacao QBO/TSA:**
- Ao validar features (Winter Release), capturar screenshots
- Naming convention: `WR-XXX_feature_name_timestamp.png`
- Linkar evidencias no ticket Linear

---

## Lacunas Identificadas

| Gap | Impacto | Sugestao |
|-----|---------|----------|
| Pipeline de ingestao QBO nao documentado | Alto | Pedir sessao com Lucas Soranzo |
| Schema validation rules nao mapeadas | Medio | Extrair do codigo fonte |
| Dataset isolation logic nao clara | Alto | Documentar apos investigacao |
| Feature validation nao automatizada para todos ambientes | Medio | Expandir qbo_checker |

---

## Recomendacoes para Proximas Sessoes

### Para Lucas Soranzo (Eng Lead)
1. Como funciona o pipeline de ingestao ponta a ponta?
2. Quais validators existem para integridade referencial?
3. Como detectar problemas de cross-dataset antes de irem pra prod?
4. Ha documentacao da API interna do BOOM?

### Para Equipe TSA
1. Adotar Strategic Cortex Pattern para cada cliente grande
2. Usar Document Classification ao organizar Drives
3. Implementar Cross-Dataset Validation em scripts de teste
4. Capturar evidencias com naming convention padronizada

### Para CORTEX Evolution
1. Integrar GOD_EXTRACT como coletor de Drive
2. Adicionar Classification automatica no SpineHub
3. Criar pattern library para problemas comuns
4. Automatizar deteccao de cross-dataset issues

---

## Tags

#strategic #patterns #tsa #qbo #cortex #god_extract #consolidation #2026-01-15
