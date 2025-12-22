# Linear SDK - TSA_CORTEX

## Visão Geral

Usamos o [@linear/sdk](https://www.npmjs.com/package/@linear/sdk) para coletar issues, comentários e atividades do Linear.

## Autenticação

```typescript
import { LinearClient } from '@linear/sdk';

const client = new LinearClient({
  apiKey: process.env.LINEAR_API_KEY
});
```

## Queries Utilizadas

### Obter Usuário Atual
```typescript
const me = await client.viewer;
const userId = me.id;
```

### Issues Criadas pelo Usuário
```typescript
const issues = await client.issues({
  filter: {
    creator: { id: { eq: userId } },
    createdAt: { gte: startDate, lte: endDate },
  },
  first: 100,
});
```

### Issues Atribuídas ao Usuário
```typescript
const issues = await client.issues({
  filter: {
    assignee: { id: { eq: userId } },
    updatedAt: { gte: startDate, lte: endDate },
  },
  first: 100,
});
```

### Comentários do Usuário
```typescript
const comments = await client.comments({
  filter: {
    user: { id: { eq: userId } },
    createdAt: { gte: startDate, lte: endDate },
  },
  first: 100,
});
```

### Detalhes de uma Issue
```typescript
const issue = await client.issue(issueId);
const state = await issue.state;
const assignee = await issue.assignee;
const comments = await issue.comments({ first: 50 });
```

### Criar Issue (para postar worklog)
```typescript
const issue = await client.createIssue({
  teamId: teamId,
  title: 'Worklog: ...',
  description: markdownBody,
  labelIds: ['label1', 'label2'],
});
```

### Listar Teams
```typescript
const teams = await client.teams();
for (const team of teams.nodes) {
  console.log(team.name, team.key);
}
```

## Estrutura de Dados

### Issue
```typescript
interface Issue {
  id: string;
  identifier: string;  // e.g., "ABC-123"
  title: string;
  description?: string;
  state: { name: string };
  assignee?: { id: string; name: string };
  creator?: { id: string; name: string };
  createdAt: Date;
  updatedAt: Date;
  url: string;
}
```

## Rate Limits

- 5000 requests/hour por API key
- Usar paginação para grandes volumes

## Referências

- [Linear API Docs](https://developers.linear.app/docs)
- [Linear SDK](https://www.npmjs.com/package/@linear/sdk)
