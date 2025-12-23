# Memory - Estado Persistente do Projeto TSA_CORTEX

> Este arquivo mantém o contexto entre sessões. Atualize ao final de cada sessão via `/consolidar`.

## Estado Atual

**Fase:** Produção (MVP Completo + SpineHub Layer)
**Última Atualização:** 2025-12-23
**Status:** ✅ Todos os coletores funcionando + SpineHub Layer 3.5 implementado

## Métricas de Coleta (última execução: 10-18 Dez 2025)

| Fonte | Eventos | Status |
|-------|---------|--------|
| Slack | 2240 | ✅ Search API |
| Linear | 5 | ✅ SDK |
| Drive | 342 | ✅ OAuth2 |
| Local | 93 | ✅ File scan |
| **Total** | **2680** | |

**Ticket criado:** https://linear.app/testbox/issue/RAC-2/weekly-update-thiago-rodrigues-2025-12-18

## Arquitetura Implementada

| Módulo | Status | Descrição |
|--------|--------|-----------|
| `types/` | ✅ Completo | Tipos TypeScript |
| `utils/` | ✅ Completo | Config, datetime, hash, privacy |
| `collectors/slack` | ✅ Refatorado | **Search API** |
| `collectors/linear` | ✅ Completo | Linear SDK |
| `collectors/drive` | ✅ Completo | Google Drive API v3 |
| `collectors/local` | ✅ Completo | Scan de arquivos |
| `normalizer/` | ✅ Completo | Normalização |
| `clustering/` | ✅ Completo | Agrupamento |
| `spinehub/` | ✅ **NOVO** | **Layer 3.5: Content Hub** |
| `worklog/` | ✅ Atualizado | Markdown + JSON + **Narrative Renderer** |
| `linear/poster` | ✅ Completo | Criação de tickets |
| `cli/` | ✅ Completo | Interface CLI |

## Credenciais Configuradas

| Serviço | Variáveis | Status |
|---------|-----------|--------|
| Slack | SLACK_USER_TOKEN, SLACK_USER_ID | ✅ |
| Linear | LINEAR_API_KEY | ✅ |
| Google | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN | ✅ |
| User | USER_DISPLAY_NAME | ✅ "Thiago Rodrigues" |

## Decisões Importantes

| Data | Decisão | Contexto |
|------|---------|----------|
| 2025-12-22 | Slack Search API | User token (xoxp-) com search:read |
| 2025-12-22 | Keywords configuráveis | search_keywords em config |
| 2025-12-22 | USER_DISPLAY_NAME | Nome no título do ticket |
| 2025-12-23 | SpineHub Layer 3.5 | Consolidação de conteúdo antes da narrativa |
| 2025-12-23 | Narrative Renderer | Gera história baseada em conteúdo, não metadata |

## Documentação

| Arquivo | Descrição |
|---------|-----------|
| docs/ONBOARDING.md | Guia para novos usuários |
| knowledge-base/troubleshooting/ | Problemas comuns |

## Próximos Passos

1. ✅ Configuração completa - Concluído
2. ✅ Primeiro ticket criado - RAC-2
3. ✅ Guia de onboarding criado
4. [ ] Implementar testes unitários
5. [x] SpineHub Layer 3.5 implementado
6. [ ] Adicionar coletor Claude
7. [ ] Testar SpineHub com dados reais

---

**Instruções:** Sempre leia este arquivo no início de cada sessão.
