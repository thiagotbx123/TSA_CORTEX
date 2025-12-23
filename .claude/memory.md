# Memory - Estado Persistente do Projeto TSA_CORTEX

> Este arquivo mantém o contexto entre sessões. Atualize ao final de cada sessão via `/consolidar`.

## Estado Atual

**Fase:** Produção (v1.0 Completo)
**Última Atualização:** 2025-12-23
**Status:** ✅ Pipeline completo + SpineHub + Repo público no GitHub
**Repo:** https://github.com/thiagotbx123/TSA_CORTEX

## Métricas de Coleta (última execução: 10-17 Dez 2025)

| Fonte | Eventos | Status |
|-------|---------|--------|
| Slack | 1,919 | ✅ Search API |
| Linear | 4 | ✅ SDK |
| Drive | 317 | ✅ OAuth2 |
| Local | 87 | ✅ File scan |
| Claude | 359 | ✅ Session collector |
| **Total** | **2,686** | |

**Tickets criados:**
- RAC-2: https://linear.app/testbox/issue/RAC-2/weekly-update-thiago-rodrigues-2025-12-18
- RAC-11: Teste com narrative format
- RAC-12: https://linear.app/testbox/issue/RAC-12/worklog25-12-17-tsa-thiago-rodrigues (10-17 Dez)

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
