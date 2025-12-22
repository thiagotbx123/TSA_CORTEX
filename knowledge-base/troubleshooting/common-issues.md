# Troubleshooting - Problemas Comuns

## Instalação e Setup

### npm install falha

**Problema:** Erros durante `npm install`

**Soluções:**
```bash
# Limpar cache
npm cache clean --force

# Deletar node_modules e reinstalar
rm -rf node_modules package-lock.json
npm install

# Se problema persistir, usar yarn
yarn install
```

### TypeScript não compila

**Problema:** Erros de compilação TypeScript

**Verificar:**
1. Versão do Node.js >= 18
2. `tsconfig.json` existe e está correto
3. Path aliases configurados

```bash
# Verificar versão do Node
node --version

# Compilar com verbose
npx tsc --listFiles
```

---

## Credenciais

### Slack: invalid_auth

**Problema:** Token Slack inválido

**Soluções:**
1. Verificar se token começa com `xoxb-` (bot) ou `xoxp-` (user)
2. Verificar escopos necessários no Slack App
3. Regenerar token se necessário

### Linear: Unauthorized

**Problema:** API key Linear não funciona

**Soluções:**
1. Verificar se key começa com `lin_api_`
2. Verificar se key não expirou
3. Gerar nova key em linear.app/settings/api

### Google: Invalid Grant

**Problema:** Refresh token inválido

**Soluções:**
1. Revogar acesso e autorizar novamente
2. Verificar se projeto está ativo no Cloud Console
3. Verificar se escopos estão corretos

---

## Coleta de Dados

### Nenhuma mensagem do Slack

**Possíveis causas:**
1. User ID incorreto
2. Bot não é membro dos canais
3. Date range não tem mensagens

**Debug:**
```typescript
// Verificar user ID
console.log('SLACK_USER_ID:', process.env.SLACK_USER_ID);

// Listar canais onde bot é membro
const channels = await client.conversations.list();
console.log('Channels:', channels.channels?.map(c => c.name));
```

### Linear retorna poucas issues

**Possíveis causas:**
1. User ID não corresponde ao usuário logado
2. Issues foram criadas fora do date range

**Debug:**
```typescript
// Verificar usuário
const me = await client.viewer;
console.log('Linear user:', me.name, me.id);
```

---

## Geração de Worklog

### Clusters vazios

**Possíveis causas:**
1. Poucos eventos coletados
2. Keywords de clustering não detectadas

**Solução:** Eventos vão para "unclustered" e aparecem no worklog mesmo assim.

### Timeline muito longa

**Comportamento normal:** Timeline é truncada para 50 entries no Markdown.

---

## Linear Posting

### Team not found

**Problema:** Time especificado não existe

**Soluções:**
1. Verificar nome exato do time (case sensitive)
2. Usar key do time em vez do nome
3. Listar times disponíveis:
```typescript
const poster = new LinearPoster(config);
const teams = await poster.getTeams();
console.log(teams);
```

### Labels not applied

**Comportamento:** Labels são ignorados se não existem no time.

**Solução:** Criar labels manualmente no Linear primeiro.
