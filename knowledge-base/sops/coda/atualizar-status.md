# SOP: Atualizar Status no CODA

## Objetivo
Manter o Solutions Central atualizado com status dos clientes para visibilidade cross-functional.

## Quando Usar
- Status de cliente mudou (Green/Yellow/Red)
- Milestone completado
- Blocker identificado
- Handoff de projeto

## Pre-requisitos
- Acesso ao CODA (Solutions Central)
- API Token configurado no `.env` (CODA_API_TOKEN)
- Doc ID do Solutions Central (CODA_DOC_SOLUTIONS_CENTRAL)

## Passos

### 1. Identificar o Cliente no CODA

**URL padrao:** `https://coda.io/d/Solutions-Central_djfymaxsTtA`

**Tabelas principais:**
- `Clients` - Lista de clientes
- `Projects` - Projetos por cliente
- `Status Updates` - Historico de updates

### 2. Atualizar Status via UI

1. Abrir Solutions Central
2. Localizar cliente na tabela `Clients`
3. Clicar na celula de Status
4. Selecionar novo status:
   - **Green** - On track, sem blockers
   - **Yellow** - Risco identificado, precisa atencao
   - **Red** - Blocker critico, escalation necessario
5. Adicionar comentario com contexto

### 3. Atualizar via API

```bash
# Obter tabelas do documento
curl -H "Authorization: Bearer $CODA_API_TOKEN" \
  "https://coda.io/apis/v1/docs/jfymaxsTtA/tables"

# Atualizar linha especifica
curl -X PUT \
  -H "Authorization: Bearer $CODA_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://coda.io/apis/v1/docs/jfymaxsTtA/tables/grid-xxx/rows/i-yyy" \
  -d '{
    "row": {
      "cells": [
        {"column": "c-status", "value": "Yellow"},
        {"column": "c-notes", "value": "Blocked on API access"}
      ]
    }
  }'
```

### 4. Via TypeScript (TSA_CORTEX)

```typescript
// knowledge-base/api/coda.md tem detalhes
import { CodaClient } from '../collectors/coda';

const coda = new CodaClient({
  token: process.env.CODA_API_TOKEN,
  docId: process.env.CODA_DOC_SOLUTIONS_CENTRAL
});

await coda.updateClientStatus({
  clientName: 'Gong',
  status: 'Yellow',
  notes: 'Blocked on OAuth investigation - PLA-3200',
  updatedBy: 'Thiago'
});
```

### 5. Comunicar Mudanca

Se status mudou para **Yellow** ou **Red**:
1. Postar no canal Slack do cliente
2. Marcar Account Lead
3. Linkar ticket Linear se existir

**Template Slack:**
```
:yellow_circle: Status Update - [CLIENTE]

Status: Yellow (was: Green)
Reason: [Descricao breve]
Linear: [Link se aplicavel]
Next Steps: [O que vai acontecer]

cc @account-lead
```

## Outputs Esperados
- Status atualizado no CODA
- Historico registrado
- Stakeholders notificados (se Yellow/Red)

## Troubleshooting

| Problema | Solucao |
|----------|---------|
| `401 Unauthorized` | Verificar CODA_API_TOKEN |
| `404 Table not found` | Verificar CODA_DOC_SOLUTIONS_CENTRAL |
| Nao consigo editar | Verificar permissoes no doc |

## Referencias
- [CODA API Docs](https://coda.io/developers/apis/v1)
- [Solutions Central](https://coda.io/d/Solutions-Central_djfymaxsTtA)
- [TSA_CORTEX CODA Module](../api/coda.md) (a ser criado)

---

**Automacao disponivel:** PARCIAL - API pronta, collector a implementar
**Ultima atualizacao:** 2026-01-26
