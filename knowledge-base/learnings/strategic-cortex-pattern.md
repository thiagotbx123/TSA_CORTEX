# Aprendizado: Strategic Cortex Pattern

**Data:** 2025-12-27
**Contexto:** Construcao de inteligencia estrategica completa para projeto Intuit-boom

## O Problema

Precisavamos consolidar conhecimento de multiplas fontes (Slack, Drive, Linear) em uma visao estrategica unificada que pudesse:
1. Responder perguntas executivas rapidamente
2. Rastrear riscos e decisoes
3. Detectar mudancas de direcao
4. Servir como base para futuras sessoes

## A Solucao: Strategic Cortex (5 Outputs)

### Arquitetura
```
Sources (Collectors)          Strategic Cortex (Outputs)
------------------           -------------------------
Slack MCP        ───┐
                    ├───> A: Executive Snapshot
DriveCollector  ───┤      B: Strategic Map
                    ├───> C: Knowledge Base JSON
Linear (manual)  ───┘      D: Keyword Map + Recipes
                          E: Delta Summary
```

### Output A: Executive Snapshot
**Proposito:** Resposta rapida para "onde estamos?"
**Estrutura:**
- Status por tema (WFS, QBO, TCO, etc)
- Top riscos e blockers com prioridade
- Decisoes recentes mais relevantes
- O que esta nebuloso (gaps)
- Proximos passos recomendados

**Uso:** Inicio de reuniao, sync rapido, onboarding

### Output B: Strategic Map
**Proposito:** Entender conexoes e arquitetura do projeto
**Estrutura:**
- Conexoes estrategia <-> requisitos <-> datasets
- Mapa de stakeholders e responsabilidades
- Dependencias entre workstreams
- Architecture decision records

**Uso:** Planning, debugging de processo, handoff

### Output C: Knowledge Base JSON
**Proposito:** Dados estruturados para queries e automacao
**Estrutura:**
```json
{
  "files_index": [...],      // Inventario de documentos
  "knowledge_items": [...],  // Fatos extraidos
  "decision_log": [...],     // Historico de decisoes
  "risk_register": [...],    // Riscos ativos
  "stakeholder_map": {...},  // Quem faz o que
  "timeline_events": [...]   // Cronologia
}
```

**Uso:** Automacao, integracao, analise de dados

### Output D: Keyword Map + Linear Recipes
**Proposito:** Encontrar informacao rapidamente
**Estrutura:**
- Keywords por tema (PT/EN, sinonimos, erros comuns)
- Queries prontas para Google Drive
- Queries prontas para Linear
- Mapeamento Drive <-> Linear

**Uso:** Busca manual, treinamento de novos membros

### Output E: Delta Summary
**Proposito:** Detectar mudancas de direcao
**Estrutura:**
- Metricas: ultimos 30 dias vs 30-60 dias
- Mudancas de foco estrategico
- Novos riscos identificados
- Alteracoes de escopo
- Atividade por stakeholder

**Uso:** Weekly review, identificar tendencias

## Processo de Geracao

### 1. Coleta
```javascript
// DriveCollector - scan completo
const files = await driveCollector.collect({
  folders: ['Fall Release', 'WFS', 'Contracts', ...],
  dateRange: '90d'
});
// Resultado: 20,426 arquivos
```

### 2. Classificacao
```javascript
// Relevance: high/medium/low
// doc_role: contract, strategy, data, ops, meeting
// topic_tags: wfs, qbo, tco, ingest, etc
// confidentiality: public, internal, restricted
```

### 3. Extracao
```javascript
// Knowledge items de arquivos high priority
// Decisoes de meeting notes
// Riscos de trackers e status docs
```

### 4. Geracao
```javascript
// Output A: Snapshot agregado
// Output B: Relacoes mapeadas
// Output C: JSON estruturado
// Output D: Keywords compilados
// Output E: Delta calculado
```

## Metricas de Sucesso

| Metrica | Valor | Significado |
|---------|-------|-------------|
| Total processado | 20,426 | Cobertura completa do Drive |
| Relevantes | 1,926 (9.4%) | Filtragem eficiente |
| High priority | 274 | Foco no que importa |
| Knowledge items | 847 | Fatos extraidos |
| Riscos identificados | 7 | Tracking ativo |
| Open questions | 6 | Gaps mapeados |

## Regras Aprendidas

### 1. Classificacao em 3 tiers funciona
- High: keywords primarios + doc_role importante
- Medium: keywords secundarios OU doc_role importante
- Low: sem match ou baixa relevancia

### 2. Delta 30 dias e o sweet spot
- Muito curto: pouca visibilidade
- Muito longo: ruido demais
- 30 dias: captura ciclo de sprint/release

### 3. Outputs devem ser standalone
- Cada output deve fazer sentido sozinho
- Nao depender de leitura sequencial
- Permitir consulta pontual

### 4. JSON para automacao, MD para humanos
- Output C: JSON para scripts e integracao
- Outputs A,B,D,E: Markdown para leitura

### 5. Recipes > Acesso direto
- Quando MCP nao disponivel (Linear), criar queries manuais
- Usuario pode executar e trazer resultados
- Melhor que nao ter nada

## Proximos Passos

1. **Automatizar refresh**: Script para regenerar outputs semanalmente
2. **Linear MCP**: Configurar para acesso direto
3. **Cross-reference**: Ligar Drive docs a Linear tickets automaticamente
4. **Alerts**: Notificar quando novos riscos P0/P1 aparecem
5. **Trend analysis**: Comparar deltas ao longo do tempo

## Aplicabilidade

Este pattern pode ser usado para:
- Qualquer projeto grande com multiplas fontes de dados
- Onboarding de novos membros
- Transicao entre TSAs
- Auditorias e reviews
- Weekly/monthly reporting

---

*Documentado em: 2025-12-27*
*Sessao: intuit-boom Strategic Cortex build*
*Duracao: ~4 horas*
