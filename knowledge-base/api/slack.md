# Slack Web API - TSA_CORTEX

## Visão Geral

Usamos a [@slack/web-api](https://www.npmjs.com/package/@slack/web-api) para coletar mensagens, threads e arquivos do Slack.

## Escopos Necessários

```
channels:history    # Ler histórico de canais públicos
channels:read       # Listar canais públicos
groups:history      # Ler histórico de canais privados
groups:read         # Listar canais privados
im:history          # Ler DMs
mpim:history        # Ler group DMs
users:read          # Info de usuários
files:read          # Acessar arquivos
search:read         # Buscar mensagens
```

## Endpoints Utilizados

### conversations.list
Lista canais onde o usuário é membro.
```typescript
const response = await client.conversations.list({
  types: 'public_channel,private_channel',
  limit: 200,
});
```

### conversations.history
Busca mensagens de um canal.
```typescript
const response = await client.conversations.history({
  channel: channelId,
  oldest: dateToSlackTs(startDate),
  latest: dateToSlackTs(endDate),
  limit: 200,
});
```

### conversations.replies
Busca replies de uma thread.
```typescript
const response = await client.conversations.replies({
  channel: channelId,
  ts: threadTs,
  limit: 100,
});
```

### chat.getPermalink
Obtém link permanente de uma mensagem.
```typescript
const response = await client.chat.getPermalink({
  channel: channelId,
  message_ts: messageTs,
});
```

## Rate Limits

- Tier 2: ~20 requests/min para a maioria dos endpoints
- Tier 3: ~50 requests/min para conversations.history

## Formato de Timestamp

Slack usa timestamp no formato Unix com microsegundos:
```typescript
// Date -> Slack ts
const slackTs = (date.getTime() / 1000).toFixed(6);

// Slack ts -> Date
const date = new Date(parseFloat(slackTs) * 1000);
```

## Referências

- [Slack API Docs](https://api.slack.com/methods)
- [Node SDK](https://slack.dev/node-slack-sdk/)
