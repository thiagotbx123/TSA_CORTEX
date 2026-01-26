# CODA API - Documentacao TSA_CORTEX

> Referencia para integracao com CODA no contexto TSA.

## Configuracao

### Variaveis de Ambiente
```bash
CODA_API_TOKEN=d9214251-44f4-4e76-8cad-62379fc65d19
CODA_DOC_SOLUTIONS_CENTRAL=jfymaxsTtA
CODA_WORKSPACE=TestBox
```

### Base URL
```
https://coda.io/apis/v1
```

## Autenticacao

Header padrao:
```http
Authorization: Bearer {CODA_API_TOKEN}
Content-Type: application/json
```

## Endpoints Principais

### Listar Documentos
```bash
GET /docs
```

### Obter Tabelas de um Doc
```bash
GET /docs/{docId}/tables
```

### Listar Rows de uma Tabela
```bash
GET /docs/{docId}/tables/{tableId}/rows
```

### Atualizar Row
```bash
PUT /docs/{docId}/tables/{tableId}/rows/{rowId}
```

### Inserir Row
```bash
POST /docs/{docId}/tables/{tableId}/rows
```

## Documentos Conhecidos

| Doc | ID | Uso |
|-----|-----|-----|
| Solutions Central | `jfymaxsTtA` | Status de clientes |
| Intuit Knowledge | (verificar) | Docs Intuit/QBO |

## Tabelas Solutions Central

| Tabela | Colunas Principais |
|--------|-------------------|
| Clients | Name, Status, Account Lead, TSA |
| Projects | Client, Phase, Status, Deadline |
| Status Updates | Date, Client, Status, Notes |

## Exemplos de Uso

### Buscar Clientes
```typescript
const response = await fetch(
  'https://coda.io/apis/v1/docs/jfymaxsTtA/tables/grid-clients/rows',
  {
    headers: {
      'Authorization': `Bearer ${process.env.CODA_API_TOKEN}`
    }
  }
);
const data = await response.json();
```

### Atualizar Status
```typescript
await fetch(
  `https://coda.io/apis/v1/docs/jfymaxsTtA/tables/grid-clients/rows/${rowId}`,
  {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${process.env.CODA_API_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      row: {
        cells: [
          { column: 'c-status', value: 'Yellow' }
        ]
      }
    })
  }
);
```

## Rate Limits

| Tipo | Limite |
|------|--------|
| Requests/minuto | 100 |
| Rows por request | 500 |

## Troubleshooting

| Erro | Causa | Solucao |
|------|-------|---------|
| `401` | Token invalido | Regenerar em coda.io/account |
| `404` | Doc/Table ID errado | Verificar ID na URL do CODA |
| `429` | Rate limit | Aguardar 1 minuto |

## Referencias
- [CODA API Docs](https://coda.io/developers/apis/v1)
- [CODA API Playground](https://coda.io/developers/apis/v1#section/Using-the-API)

---

**Status:** Credenciais configuradas, collector a implementar
**Ultima atualizacao:** 2026-01-26
