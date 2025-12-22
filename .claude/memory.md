# Memory - Estado Persistente do Projeto TSA_CORTEX

> Este arquivo mantém o contexto entre sessões. Atualize ao final de cada sessão via `/consolidar`.

## Estado Atual

**Fase:** Desenvolvimento Inicial
**Última Atualização:** 2024-12-22

## Arquitetura Implementada

| Módulo | Status | Descrição |
|--------|--------|-----------|
| `types/` | ✅ Completo | Tipos TypeScript (ActivityEvent, WorklogOutput, etc.) |
| `utils/` | ✅ Completo | Config, datetime, hash, privacy |
| `collectors/slack` | ✅ Completo | Coletor Slack API |
| `collectors/linear` | ✅ Completo | Coletor Linear SDK |
| `collectors/drive` | ✅ Completo | Coletor Google Drive |
| `collectors/local` | ✅ Completo | Coletor arquivos locais |
| `normalizer/` | ✅ Completo | Normalização e deduplicação |
| `clustering/` | ✅ Completo | Agrupamento por tópicos |
| `worklog/` | ✅ Completo | Gerador Markdown + JSON |
| `linear/poster` | ✅ Completo | Criação de tickets |
| `cli/` | ✅ Completo | Interface de linha de comando |

## Últimas Ações

| Data | Ação | Resultado |
|------|------|-----------|
| 2024-12-22 | Criação do projeto | Estrutura completa implementada |
| 2024-12-22 | Implementação de coletores | Slack, Linear, Drive, Local |
| 2024-12-22 | Sistema de clustering | Agrupamento por tópicos funcionando |
| 2024-12-22 | Aplicação ESPINHA_DORSAL | Estrutura de documentação |
| 2024-12-22 | Refatoração de output | Inglês natural, tom direto |

## Bloqueios Conhecidos

- [ ] Dependências não instaladas (npm install pendente)
- [ ] Credenciais não configuradas (.env)
- [ ] Coletor Claude não implementado (best-effort)

## Decisões Importantes

| Data | Decisão | Contexto |
|------|---------|----------|
| 2024-12-22 | TypeScript + Node.js | Stack ideal para APIs REST e CLI |
| 2024-12-22 | Zod para validação | Schemas runtime com tipos TypeScript |
| 2024-12-22 | date-fns-tz | Timezone handling robusto |
| 2024-12-22 | Team "raccoons" para TSAs | Roteamento padrão no Linear |
| 2024-12-22 | Output em inglês natural | Tom intermediário, direto, sem jargão técnico |

## Configuração de Routing

```json
{
  "tsa": { "linear_team": "raccoons", "labels": ["worklog", "weekly"] },
  "default": { "linear_team": "ops", "labels": ["worklog", "weekly"] }
}
```

## Próximos Passos

1. `npm install` - Instalar dependências
2. Configurar `.env` com API keys
3. Testar pipeline: `npm run dev run --dry-run`
4. Implementar testes unitários
5. Adicionar mais tipos de clustering

---

**Instruções:** Sempre leia este arquivo no início de cada sessão para recuperar contexto.
