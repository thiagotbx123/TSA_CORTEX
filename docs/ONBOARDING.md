# Guia de Onboarding - TSA_CORTEX

Este guia ajuda novos usuarios a configurar o CORTEX do zero.

## O Que e o CORTEX?

TSA_CORTEX e um sistema de automacao de worklog que:
- Coleta dados de **Slack, Linear, Google Drive, arquivos locais e Claude Code**
- Consolida conteudo via **SpineHub** (Layer 3.5)
- Gera **narrativas** baseadas em conteudo real, nao apenas metadata
- Cria **tickets automaticamente** no Linear

## Pre-requisitos

- Node.js >= 18
- npm ou yarn
- Acesso aos servicos: Slack workspace, Linear workspace, Google Drive
- (Opcional) Claude Code para uso interativo

---

## Passo 1: Clonar e Instalar

```bash
git clone <repo-url>
cd TSA_CORTEX

# Instalar dependencias
npm install

# Compilar TypeScript
npm run build
```

## Passo 2: Configurar .env

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais (detalhes abaixo).

---

## Passo 3: Configurar Slack

O CORTEX usa **Search API** para encontrar mensagens. Requer **User Token** (nao Bot Token).

### 3.1 Criar Slack App

1. Acesse https://api.slack.com/apps
2. Clique em **Create New App** > **From scratch**
3. Nome: "CORTEX" (ou outro nome)
4. Selecione seu workspace

### 3.2 Configurar Scopes

1. Va em **OAuth & Permissions**
2. Em **User Token Scopes**, adicione:
   - `search:read` (OBRIGATORIO)

### 3.3 Instalar no Workspace

1. Clique em **Install to Workspace**
2. Autorize o app
3. Copie o **User OAuth Token** (comeca com `xoxp-`)

### 3.4 Obter User ID

1. No Slack, clique no seu perfil
2. Clique em **More** > **Copy member ID**

### 3.5 Adicionar ao .env

```env
SLACK_USER_TOKEN=xoxp-seu-token-aqui
SLACK_USER_ID=U09XXXXXXXX
```

---

## Passo 4: Configurar Linear

### 4.1 Gerar API Key

1. Acesse https://linear.app/settings/api
2. Clique em **Create key**
3. Copie a key (comeca com `lin_api_`)

### 4.2 Adicionar ao .env

```env
LINEAR_API_KEY=lin_api_sua-key-aqui
```

---

## Passo 5: Configurar Google Drive

### 5.1 Criar Projeto no Google Cloud

1. Acesse https://console.cloud.google.com
2. Crie um novo projeto ou selecione existente
3. Va em **APIs & Services** > **Enable APIs**
4. Habilite **Google Drive API**

### 5.2 Criar Credenciais OAuth

1. Va em **APIs & Services** > **Credentials**
2. Clique **Create Credentials** > **OAuth client ID**
3. Tipo: **Desktop application**
4. Baixe o JSON das credenciais

### 5.3 Obter Refresh Token

Execute o script de autorizacao:

```bash
node scripts/get-google-token.js
```

1. Copie a URL exibida e abra no navegador
2. Autorize o acesso ao Drive
3. Copie o codigo da URL de callback
4. Cole no terminal
5. O script exibe o refresh token

### 5.4 Adicionar ao .env

```env
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-sua-secret
GOOGLE_REFRESH_TOKEN=1//seu-refresh-token
```

---

## Passo 6: Configurar Identificacao

```env
USER_DISPLAY_NAME=Seu Nome Completo
USER_ROLE=tsa
```

O `USER_DISPLAY_NAME` aparece no titulo do ticket no Linear.

---

## Passo 7: Configurar Canais Slack (Opcional)

Edite `config/default.json` para personalizar os canais coletados:

```json
{
  "collectors": {
    "slack": {
      "enabled": true,
      "target_channels": [
        "seu-canal-1",
        "seu-canal-2"
      ],
      "collect_dms": true,
      "search_from_me": true
    }
  }
}
```

---

## Passo 8: Testar

### Verificar Status

```bash
node dist/cli/index.js status
```

Deve mostrar:
```
Collectors:
  slack: Enabled
  linear: Enabled
  drive: Enabled
  local: Enabled
  claude: Enabled

Credentials:
  Slack: Set
  Linear: Set
  Google: Set
```

### Dry Run (sem postar no Linear)

```bash
node dist/cli/index.js run --dry-run
```

### Execucao Real

```bash
node dist/cli/index.js run
```

### Com Data Range Customizado

```bash
node dist/cli/index.js run --start 2025-12-10 --end 2025-12-17
```

---

## Uso com Claude Code (Recomendado)

Se voce tem Claude Code, pode usar o fluxo interativo:

1. Abra o terminal na pasta do projeto
2. Inicie o Claude Code
3. Diga: **"Quero gerar meu worklog"**

O Claude vai seguir o fluxo `/worklog`:
1. Perguntar o periodo desejado
2. Confirmar as fontes
3. Rodar a coleta
4. Montar o worklog com SpineHub
5. Mostrar preview
6. Pedir aprovacao antes de criar ticket

### Arquivos Importantes para o Claude

- `CLAUDE.md` - Instrucoes que o Claude segue
- `.claude/commands/worklog.md` - Fluxo do comando /worklog
- `.claude/memory.md` - Estado persistente do projeto

---

## Arquitetura do Pipeline

```
Step 1: Collection    -> Coleta dados de 5 fontes
Step 2: Normalization -> Remove duplicatas
Step 3: Clustering    -> Agrupa por temas
Step 3.5: SpineHub    -> Consolida conteudo real (NEW!)
Step 4: Generation    -> Gera worklog narrativo
Step 5: Post          -> Cria ticket no Linear
```

### SpineHub (Layer 3.5)

O SpineHub e o "cerebro" que consolida:
- Mensagens do owner vs contexto
- Conteudo real dos arquivos
- Gera blocos narrativos para contar a historia

---

## Troubleshooting

### Slack: missing_scope

**Causa:** Token sem `search:read`

**Solucao:** Adicione o scope `search:read` em User Token Scopes e reinstale o app.

### Slack: 0 mensagens

**Causa:** Usando Bot Token (xoxb-) em vez de User Token (xoxp-)

**Solucao:** Use o User OAuth Token, nao o Bot Token.

### date-fns: toZonedTime is not a function

**Causa:** date-fns v3 incompativel

**Solucao:** `npm install date-fns@^2.30.0`

### Drive: File not found

**Causa:** Config com nomes de pasta em vez de IDs

**Solucao:** Remova `denylist_folders` do config.

### Linear: Unauthorized

**Causa:** API key invalida ou expirada

**Solucao:** Gere nova key em linear.app/settings/api

### Build errors

**Causa:** TypeScript nao compilado

**Solucao:** `npm run build`

---

## Resultados Esperados

Uma execucao bem-sucedida exibe:

```
TSA_CORTEX - Weekly Worklog Automation

Step 1: Collecting data from sources...
  Slack: 1919 eventos
  Linear: 4 eventos
  Drive: 317 eventos
  Local: 87 eventos
  Claude: 359 eventos

Step 2: Normalizing events...
  Total events: 2686
  After dedup: 2686

Step 3: Clustering events into topics...
  Clusters created: 11

Step 3.5: Building SpineHub...
  Narrative blocks: 28
  Owner messages: 872

Step 4: Generating worklog...
  Saved JSON: output/worklog_XXXX.json
  Saved Markdown: output/worklog_XXXX.md

Step 5: Posting to Linear...
  Ticket created: https://linear.app/...

Worklog generation complete!
```

---

## Suporte

- Documentacao: `knowledge-base/` para detalhes tecnicos
- Troubleshooting: `knowledge-base/troubleshooting/`
- CLAUDE.md: Instrucoes para uso com Claude Code

---

*Ultima atualizacao: 2025-12-23*
