# Decisoes Arquitetonicas - Nivel de Detalhe do Worklog

## ADR-006: Coleta Completa de Canais Slack

**Data:** 2025-12-22
**Status:** Aceita

### Contexto
A abordagem inicial de busca por keywords no Slack resultava em worklogs muito resumidos.
O usuario precisa de visibilidade completa de todas as conversas em canais relevantes.

### Problema Identificado
- Busca por keywords perdia contexto das conversas
- Worklog de 5 dias de trabalho gerava apenas ~15 linhas
- Nao era possivel ver a "historia" das interacoes

### Decisao
Coletar TODOS os mensagens de canais-alvo usando `in:#channel` syntax:
```javascript
target_channels: [
  'intuit-internal',
  'testbox-intuit-wfs-external20251027',
  'dev-on-call',
  'product',
  'tsa-data-engineers',
  // ... outros canais relevantes
],
collect_dms: true,
search_from_me: true
```

### Sintaxe Slack Search API
- `in:#channel after:DATE before:DATE` - TODAS mensagens do canal
- `is:dm after:DATE before:DATE` - TODAS DMs
- `from:me after:DATE before:DATE` - Mensagens do usuario

### Consequencias
- Cobertura completa de todas as interacoes
- Volume maior de dados (~2000+ mensagens vs ~200 com keywords)
- Necessita processamento mais inteligente para criar resumo

---

## ADR-007: Dois Formatos de Worklog

**Data:** 2025-12-22
**Status:** Aceita

### Contexto
O pipeline principal gera worklog agrupado por clusters (temas).
Usuario precisa tambem de formato dia-a-dia extremamente detalhado.

### Decisao
Manter dois formatos:

#### 1. Pipeline Principal (Clustered)
```
npm run dev run
```
- Agrupa eventos por workstream
- Resume atividades por tema
- Ideal para visao executiva

#### 2. Script Standalone (Detailed)
```
node scripts/detailed-worklog.js 2025-12-10 2025-12-18
```
- Breakdown dia-a-dia
- Todas mensagens com horario e link
- Ideal para registro detalhado

### Consequencias
- Flexibilidade para diferentes necessidades
- Script standalone para casos de auditoria detalhada
- Pipeline principal para worklogs semanais

---

## ADR-008: Linear Sem Filtro por Projeto

**Data:** 2025-12-22
**Status:** Aceita

### Contexto
Usuario trabalha em multiplos projetos e precisa capturar toda atividade.

### Decisao
Linear collector ja coleta TUDO do usuario:
- Issues criadas no date range
- Issues onde usuario e assignee (atualizadas no range)
- Issues onde usuario comentou

NAO filtra por projeto ou keyword. Captura toda atividade independente do team/projeto.

### Consequencias
- Cobertura completa de atividade Linear
- Nenhuma atividade perdida por filtro

---

## Aprendizados Chave

1. **Keywords sao insuficientes** - Busca por palavras-chave perde contexto
2. **Canais completos sao necessarios** - `in:#channel` e melhor que keyword search
3. **DMs sao importantes** - Muito trabalho acontece em DMs
4. **Dois niveis de detalhe** - Executivo (clusters) vs Detalhado (dia-a-dia)
5. **Rate limiting** - Necessario 100ms delay entre chamadas Slack API

---

*Documentado em: 2025-12-22*
