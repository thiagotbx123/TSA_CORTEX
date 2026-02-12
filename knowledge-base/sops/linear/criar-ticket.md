# SOP: Criar Ticket no Linear

## Objetivo
Documentar e rastrear trabalho no Linear de forma padronizada para a equipe TSA.

## Quando Usar
- Novo bug reportado pelo cliente
- Nova feature request
- Task de investigacao
- Blocker identificado
- Worklog semanal

## Pre-requisitos
- Acesso ao Linear (linear.app)
- API Key configurada no `.env` (LINEAR_API_KEY)
- Conhecimento do time correto (RAC para TSA)

## Passos

### 1. Identificar o Team e Project

| Situacao | Team | Project |
|----------|------|---------|
| Bug/Issue de cliente | PLA (Platform) | Cliente especifico |
| Worklog TSA | RAC (Raccoons) | TSA's Worklog |
| Melhoria interna | RAC | Internal Improvements |
| Investigacao | RAC | Research |

### 2. Definir Titulo

**Formato:** `[CLIENTE] Descricao curta do problema`

**Exemplos:**
- `[GONG] OAuth token refresh failing`
- `[INTUIT] IC Bills table missing`
- `[BREVO] Backdating option A implementation`

### 3. Preencher Descricao

**Template:**
```markdown
## Context
[O que esta acontecendo e por que importa]

## Current Behavior
[O que acontece agora]

## Expected Behavior
[O que deveria acontecer]

## Evidence
- [Link para Slack thread]
- [Link para documento]
- [Screenshot se aplicavel]

## Proposed Solution
[Se souber, sugerir solucao]
```

### 4. Definir Prioridade

| Priority | Criterio |
|----------|----------|
| **Urgent** | Blocker de producao, cliente parado |
| **High** | Impacta demo, deadline proximo |
| **Medium** | Importante mas nao urgente |
| **Low** | Nice-to-have |

### 5. Adicionar Labels

Labels comuns TSA (corrigido TMS v2.0):
- `Customer Issues` - Defeito ou problema reportado pelo cliente
- `Feature` - Nova funcionalidade
- `Spike` - Investigacao/analise necessaria
- `Refactor` - Tech debt / refatoracao
- `Deploy` - Tarefas de deploy
- `RCA` - Root Cause Analysis
- `Internal Request` - Pedido interno
- `Customer Request` - Pedido do cliente

### 6. Atribuir (se souber)

| Area | Assignee Padrao |
|------|-----------------|
| QuickBooks | Lucas Soranzo |
| Salesforce | Engineering |
| Gong | Carlos |
| Mailchimp | Gabrielle |
| WFS | Alexandra |

### 7. Via CLI (Automacao)

```bash
# Usando TSA_CORTEX
node dist/cli/index.js linear create \
  --title "[CLIENTE] Descricao" \
  --team RAC \
  --priority high

# Usando Linear CLI diretamente
linear issue create \
  --title "[CLIENTE] Descricao" \
  --team-key RAC
```

### 8. Via API (Codigo)

```typescript
import { LinearClient } from '@linear/sdk';

const linear = new LinearClient({ apiKey: process.env.LINEAR_API_KEY });

await linear.createIssue({
  teamId: 'RAC_TEAM_ID',
  title: '[CLIENTE] Descricao',
  description: 'Context...',
  priority: 2, // 1=urgent, 2=high, 3=medium, 4=low
  labelIds: ['bug-label-id']
});
```

## Outputs Esperados
- Ticket criado no Linear
- URL do ticket para referencia
- Notificacao no Slack (se configurado)

## Troubleshooting

| Problema | Solucao |
|----------|---------|
| `Unauthorized` | Verificar LINEAR_API_KEY no .env |
| Team nao encontrado | Usar team key (RAC, PLA) nao nome |
| Assignee invalido | Buscar user ID via API primeiro |

## Referencias
- [Linear API Docs](https://developers.linear.app/docs)
- [TSA_CORTEX Linear Module](../api/linear.md)
- [Linear Teams](https://linear.app/testbox/settings/teams)

---

**Automacao disponivel:** SIM - via TSA_CORTEX CLI
**Ultima atualizacao:** 2026-02-12 (labels corrigidos per TMS v2.0)
