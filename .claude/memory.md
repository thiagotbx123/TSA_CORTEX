# Memory - Estado Persistente do Projeto TSA_CORTEX

> Este arquivo mantém o contexto entre sessões. Atualize ao final de cada sessão via `/consolidar`.

## Estado Atual

**Fase:** Produção (v1.0 Completo)
**Última Atualização:** 2025-12-24
**Status:** ✅ Pipeline completo + SpineHub + Repo público no GitHub
**Repo:** https://github.com/thiagotbx123/TSA_CORTEX

## Métricas de Coleta (última execução: 22-23 Dez 2025)

| Fonte | Eventos | MY_WORK | Status |
|-------|---------|---------|--------|
| Slack | 245 | 103 | ✅ Search API (ownership) |
| Linear | 12 | - | ✅ SDK |
| Drive | 101 | - | ✅ OAuth2 |
| Local | 58 | - | ✅ File scan |
| Claude | 69 | - | ✅ Filtered (was 816) |
| **Total** | **485** | | |

**Tickets criados:**
- RAC-2: https://linear.app/testbox/issue/RAC-2/weekly-update-thiago-rodrigues-2025-12-18
- RAC-11: Teste com narrative format
- RAC-12: https://linear.app/testbox/issue/RAC-12/worklog25-12-17-tsa-thiago-rodrigues (10-17 Dez)
- RAC-14: https://linear.app/testbox/issue/RAC-14/worklog25-12-23-tsa-thiago-rodrigues (22-23 Dez) **NARRATIVA COMPLETA**

## Pipeline de Execução (6 Steps)

```
Step 1: Collection     → Coleta de 5 fontes (Slack, Linear, Drive, Local, Claude)
Step 2: Normalization  → Remove duplicatas
Step 3: Clustering     → Agrupa por temas (11 clusters)
Step 3.5: SpineHub     → Consolida conteúdo real (NEW!)
Step 4: Generation     → Gera worklog narrativo
Step 5: Post           → Cria ticket no Linear
```

## Arquitetura Implementada

| Módulo | Status | Descrição |
|--------|--------|-----------|
| `types/` | ✅ | Tipos TypeScript |
| `utils/` | ✅ | Config, datetime, hash, privacy |
| `collectors/slack` | ✅ | Search API (xoxp- token) |
| `collectors/linear` | ✅ | Linear SDK |
| `collectors/drive` | ✅ | Google Drive API v3 |
| `collectors/local` | ✅ | Scan ~/Downloads, ~/Documents |
| `collectors/claude` | ✅ | Claude Code sessions |
| `normalizer/` | ✅ | Normalização de eventos |
| `clustering/` | ✅ | Agrupamento por keywords |
| `spinehub/` | ✅ | **Layer 3.5: Content Hub** |
| `worklog/narrative` | ✅ | **Narrative Renderer** |
| `linear/poster` | ✅ | Criação de tickets |
| `cli/` | ✅ | Interface CLI com 6 steps |

## Comandos Claude Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/worklog` | **PRINCIPAL** - Fluxo interativo de geração |
| `/status` | Visão geral do projeto |
| `/consolidar` | Fim de sessão - salva tudo |

### Fluxo do /worklog (OBRIGATÓRIO SEGUIR)

1. **Perguntar período** - NUNCA assumir datas
2. **Confirmar fontes** - Slack, Linear, Drive, Local, Claude
3. **Rodar coleta** - Mostrar progresso
4. **Montar worklog** - SpineHub + Narrative
5. **Apresentar resumo** - Preview ao usuário
6. **Pedir aprovação** - NUNCA criar ticket sem confirmação

## Credenciais Configuradas

| Serviço | Variáveis | Status |
|---------|-----------|--------|
| Slack | SLACK_USER_TOKEN (xoxp-), SLACK_USER_ID | ✅ |
| Linear | LINEAR_API_KEY | ✅ |
| Google | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN | ✅ |
| User | USER_DISPLAY_NAME = "Thiago Rodrigues" | ✅ |

## Decisões Importantes

| Data | Decisão | Contexto |
|------|---------|----------|
| 2025-12-22 | Slack Search API | User token (xoxp-) com search:read |
| 2025-12-22 | Coleta por canal completo | `in:#channel` ao invés de keywords |
| 2025-12-22 | USER_DISPLAY_NAME | Nome no título do ticket |
| 2025-12-23 | SpineHub Layer 3.5 | Consolida conteúdo ANTES da narrativa |
| 2025-12-23 | Narrative Renderer | Conta HISTÓRIA, não lista metadata |
| 2025-12-23 | Comando /worklog | Fluxo interativo obrigatório |
| 2025-12-23 | Repo público GitHub | Para compartilhar com outros TSAs |

## Aprendizados Chave (Session 2025-12-23)

### 1. SpineHub é Essencial
O problema era que o worklog listava arquivos e links, não contava a história.
SpineHub resolve isso consolidando o CONTEÚDO real antes de gerar a narrativa.

### 2. Fluxo Interativo é Obrigatório
NUNCA rodar worklog sem perguntar:
- Qual período?
- Quais fontes?
- Aprovar antes de criar ticket?

### 3. Secrets no Git
Scripts com credenciais hardcoded bloqueiam push no GitHub.
Solução: Usar variáveis de ambiente (.env) sempre.

### 4. Narrative vs Metadata
- **Errado:** "SOW_WFS_v2.docx modificado em 10/12"
- **Certo:** "Às 14:00, finalizei a versão 2 do SOW após feedback da Katherine"

## Aprendizados Chave (Session 2025-12-24)

### 5. CRÍTICO: Varrer TODOS os canais antes de gerar narrativa

**Problema detectado:** Narrativa gerada manualmente perdeu temas importantes:
- Gabrielle (67 msgs, 23 my_work) - GEM/Mailchimp - PERDIDO
- Diego (10 msgs, 9 my_work) - PERDIDO
- Lucas Soranzo (13 msgs, 5 my_work) - PERDIDO
- Kat + Alexandra (WFS onboarding) - PERDIDO inicialmente

**Root Cause:** Geração de narrativa baseada em primeiros matches, sem varrer dataset completo.

**CHECKLIST OBRIGATÓRIO antes de gerar narrativa:**
1. Listar TODOS os canais únicos no Slack
2. Ordenar por volume de my_work (desc)
3. Ignorar apenas bots (heytaco, google drive)
4. Gerar seção narrativa para CADA canal com my_work > 0
5. Validar: "Tem algum canal com my_work > 3 que não está na narrativa?"

**Script de validação:** `analyze-channels.js`

### 6. Slack Collector - Ownership Classification
- DMs: `is:dm` → my_work se user enviou, context se recebeu
- Channels: `from:me -is:dm` → my_work
- Mentions: `<@userId> -is:dm` → mentioned
- Resultado: 245 eventos (103 my_work, 13 mentioned, 129 context)

### 7. Claude Collector - Noise Reduction
- Filtrar apenas `type: user` (não assistant, tool_use, snapshot)
- Ignorar projetos genéricos (system32, windows)
- Ignorar prompts curtos (c, y, n, ok)
- Resultado: 816 → 69 eventos (-92% ruído)

## Documentação

| Arquivo | Descrição |
|---------|-----------|
| CLAUDE.md | Instruções para Claude Code |
| .claude/commands/worklog.md | Fluxo do comando /worklog |
| .claude/memory.md | Este arquivo (estado persistente) |
| docs/ONBOARDING.md | Guia para novos usuários |
| docs/PROMPT_LAYERS_SPEC.md | Especificação das 5 camadas |

## Próximos Passos

1. ✅ Pipeline completo funcionando
2. ✅ SpineHub implementado
3. ✅ Narrative Renderer implementado
4. ✅ Comando /worklog definido
5. ✅ Repo público no GitHub
6. ✅ Documentação de onboarding
7. [ ] Amigo testar em outra máquina
8. [ ] Melhorar geração de narrative blocks
9. [ ] Adicionar mais contexto do Claude Code
10. [ ] Implementar testes unitários

---

**Instruções:** Sempre leia este arquivo no início de cada sessão.
