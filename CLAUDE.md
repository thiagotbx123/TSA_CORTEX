# Instruções para Claude - TSA_CORTEX

> Este arquivo contém instruções que o Claude DEVE seguir em TODA sessão.

## Sobre o Projeto

**TSA_CORTEX** é um sistema de automação de worklog semanal que:
- Coleta dados de Slack, Linear, Google Drive e arquivos locais
- Normaliza e agrupa eventos por tópicos
- Gera worklogs com rastreabilidade de fontes
- Cria tickets automaticamente no Linear

**Stack:** TypeScript, Node.js

## Protocolo de Início de Sessão

**ANTES de responder qualquer coisa, SEMPRE:**

1. Leia `.claude/memory.md` para recuperar contexto
2. Verifique as últimas sessões em `sessions/`
3. Consulte `knowledge-base/` se necessário

## Protocolo de Fim de Sessão

**Ao finalizar trabalho, SEMPRE execute `/consolidar`:**

1. Documente o que foi feito
2. Atualize memory.md
3. Crie arquivo de sessão
4. Commit e push para Git

## Comandos Disponíveis

| Comando | Função |
|---------|--------|
| `/status` | Visão geral do estado do projeto |
| `/consolidar` | Consolidação de sessão (fim de trabalho) |

## Estrutura Principal

```
TSA_CORTEX/
├── src/
│   ├── cli/           # Interface de linha de comando
│   ├── collectors/    # Coletores (Slack, Linear, Drive, Local)
│   ├── normalizer/    # Normalização de eventos
│   ├── clustering/    # Agrupamento por tópicos
│   ├── worklog/       # Geração de worklog
│   ├── linear/        # Integração Linear
│   ├── types/         # Tipos TypeScript
│   └── utils/         # Utilitários
├── config/            # Configurações
├── output/            # Worklogs gerados
├── raw_exports/       # Dados brutos coletados
├── sessions/          # Histórico de sessões
├── knowledge-base/    # Base de conhecimento
└── .claude/           # Configurações Claude
```

## Regras de Ouro

1. **Nunca perca contexto** - Sempre leia memory.md primeiro
2. **Sempre documente** - Use /consolidar ao final
3. **Mantenha histórico** - Nunca delete sessões ou conhecimento
4. **Git é obrigatório** - Todo trabalho deve ser versionado
5. **TypeScript strict** - Sempre use tipagem forte
6. **Testes** - Toda feature nova deve ter testes

## Padrões de Código

- **Nomenclatura**: camelCase para variáveis, PascalCase para tipos/classes
- **Imports**: Usar path aliases (@types/, @utils/, etc.)
- **Exports**: Barrel exports via index.ts
- **Erros**: Sempre tratar erros explicitamente

## APIs Principais

| API | Documentação | Escopo |
|-----|-------------|--------|
| Slack Web API | knowledge-base/api/slack.md | Mensagens, canais, threads |
| Linear SDK | knowledge-base/api/linear.md | Issues, comentários |
| Google Drive API | knowledge-base/api/drive.md | Arquivos, metadados |

---

**IMPORTANTE:** Estas instruções garantem continuidade e qualidade entre sessões.
