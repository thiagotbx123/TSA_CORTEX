# Memory - Estado Persistente do Projeto TSA_CORTEX

> Este arquivo mantém o contexto entre sessões. Atualize ao final de cada sessão via `/consolidar`.

## Estado Atual

**Fase:** Produção (MVP Completo)
**Última Atualização:** 2025-12-22
**Status:** ✅ Todos os coletores funcionando

## Métricas de Coleta (última execução)

| Fonte | Eventos | Status |
|-------|---------|--------|
| Slack | 1854 | ✅ Search API |
| Linear | 6 | ✅ SDK |
| Drive | 145 | ✅ OAuth2 |
| Local | 50 | ✅ File scan |
| **Total** | **2055** | |

## Arquitetura Implementada

| Módulo | Status | Descrição |
|--------|--------|-----------|
| `types/` | ✅ Completo | Tipos TypeScript (ActivityEvent, WorklogOutput, etc.) |
| `utils/` | ✅ Completo | Config, datetime, hash, privacy |
| `collectors/slack` | ✅ Refatorado | **Search API** (não mais channel listing) |
| `collectors/linear` | ✅ Completo | Linear SDK com paginação |
| `collectors/drive` | ✅ Completo | Google Drive API v3 |
| `collectors/local` | ✅ Completo | Scan de arquivos locais |
| `normalizer/` | ✅ Completo | Normalização e deduplicação |
| `clustering/` | ✅ Completo | Agrupamento por tópicos |
| `worklog/` | ✅ Completo | Gerador Markdown + JSON |
| `linear/poster` | ✅ Completo | Criação de tickets |
| `cli/` | ✅ Completo | Interface de linha de comando |

## Credenciais Configuradas

| Serviço | Variáveis | Status |
|---------|-----------|--------|
| Slack | `SLACK_USER_TOKEN`, `SLACK_USER_ID` | ✅ Configurado |
| Linear | `LINEAR_API_KEY` | ✅ Configurado |
| Google | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` | ✅ Configurado |

## Últimas Ações

| Data | Ação | Resultado |
|------|------|-----------|
| 2024-12-22 | Criação do projeto | Estrutura completa implementada |
| 2024-12-22 | Aplicação ESPINHA_DORSAL | Estrutura de documentação |
| 2025-12-22 | Instalação dependências | Corrigido conflito date-fns v2/v3 |
| 2025-12-22 | Correção TypeScript | raw_data casting, null coalescing |
| 2025-12-22 | **Refatoração Slack** | Migrado de channel listing para Search API |
| 2025-12-22 | Configuração completa | Slack, Linear, Drive funcionando |

## Decisões Importantes

| Data | Decisão | Contexto |
|------|---------|----------|
| 2024-12-22 | TypeScript + Node.js | Stack ideal para APIs REST e CLI |
| 2024-12-22 | date-fns v2 + date-fns-tz v2 | Compatibilidade de versões |
| 2024-12-22 | Team "raccoons" para TSAs | Roteamento padrão no Linear |
| 2024-12-22 | Output em inglês natural | Tom intermediário, direto |
| 2025-12-22 | **Slack Search API** | User token (xoxp-) com search:read, não bot token |
| 2025-12-22 | Keywords configuráveis | `search_keywords` em config/default.json |

## Configuração de Routing

```json
{
  "tsa": { "linear_team": "raccoons", "labels": ["worklog", "weekly"] },
  "default": { "linear_team": "ops", "labels": ["worklog", "weekly"] }
}
```

## Slack Search Keywords

```json
{
  "search_keywords": ["intuit", "quickbooks", "WFS", "GEM", "testbox"],
  "search_from_me": true
}
```

## Problemas Resolvidos

| Problema | Solução | Arquivo |
|----------|---------|---------|
| date-fns v3 incompatível com date-fns-tz v2 | Downgrade para date-fns ^2.30.0 | package.json |
| `toZonedTime` não existe | Usar `utcToZonedTime` (v2 naming) | utils/datetime.ts |
| raw_data type mismatch | Cast via `as unknown as Record<string, unknown>` | collectors/*.ts |
| Slack `missing_scope` | Usar Search API com user token (xoxp-) | collectors/slack.ts |
| Slack 0 channels | Não depender de bot membership | collectors/slack.ts |
| Drive `denylist_folders` erro | Remover "Trash" (precisa ser folder ID) | config/default.json |

## Próximos Passos

1. ✅ ~~npm install~~ - Concluído
2. ✅ ~~Configurar .env~~ - Concluído
3. ✅ ~~Testar dry-run~~ - Concluído
4. [ ] Testar post real no Linear
5. [ ] Implementar testes unitários
6. [ ] Adicionar coletor Claude (se API disponível)
7. [ ] Melhorar clustering com ML

---

**Instruções:** Sempre leia este arquivo no início de cada sessão para recuperar contexto.
