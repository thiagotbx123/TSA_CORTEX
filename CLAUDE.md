# Instrucoes para Claude - TSA_CORTEX

> Este arquivo contem instrucoes que o Claude DEVE seguir em TODA sessao.

## Sobre o Projeto

**TSA_CORTEX** e o sistema central de operacoes da equipe TSA com tres pilares:

### 1. Worklog Automation
- Coleta dados de Slack, Linear, Drive, CODA e arquivos locais
- Normaliza e agrupa eventos por topicos
- Gera worklogs com rastreabilidade de fontes
- Cria tickets automaticamente no Linear

### 2. Procedimentos Operacionais (SOPs)
- Documentacao de rotinas padronizadas
- Guias para execucao consistente
- Automacao de tarefas repetitivas
- Base de conhecimento para onboarding

### 3. Investigacao e Pesquisa
- Capacidade de buscar em multiplas fontes
- Triangulacao de informacoes (Slack + Linear + CODA + Drive)
- Geracao de reports consolidados
- Analise de root cause

**Stack:** TypeScript, Node.js, Python (SpineHub)

## Protocolo de Inicio de Sessao

**ANTES de responder qualquer coisa, SEMPRE:**

1. Leia `.claude/memory.md` para recuperar contexto
2. Verifique as ultimas sessoes em `sessions/`
3. Consulte `knowledge-base/` se necessario
4. Identifique o tipo de tarefa: **worklog**, **sop**, ou **investigacao**

## Protocolo de Fim de Sessao

**Ao finalizar trabalho, SEMPRE execute `/consolidar`:**

1. Documente o que foi feito
2. Atualize memory.md
3. Crie arquivo de sessao
4. Commit e push para Git

## Comandos Disponiveis

| Comando | Funcao |
|---------|--------|
| `/status` | Visao geral do estado do projeto |
| `/consolidar` | Consolidacao de sessao (fim de trabalho) |
| `/worklog` | Fluxo interativo de geracao de worklog |

## Estrutura Principal

```
TSA_CORTEX/
├── src/
│   ├── cli/           # Interface de linha de comando
│   ├── collectors/    # Coletores (Slack, Linear, Drive, CODA, Local)
│   ├── normalizer/    # Normalizacao de eventos
│   ├── clustering/    # Agrupamento por topicos
│   ├── worklog/       # Geracao de worklog
│   ├── linear/        # Integracao Linear
│   ├── types/         # Tipos TypeScript
│   └── utils/         # Utilitarios
├── python/            # Modulos Python (SpineHub)
├── config/            # Configuracoes
├── output/            # Worklogs gerados
├── raw_exports/       # Dados brutos coletados
├── sessions/          # Historico de sessoes
├── knowledge-base/
│   ├── api/           # Documentacao de APIs
│   ├── sops/          # Procedimentos Operacionais
│   │   ├── linear/    # SOPs Linear
│   │   ├── coda/      # SOPs CODA
│   │   ├── comunicacao/ # SOPs Comunicacao
│   │   └── investigacao/ # SOPs Investigacao
│   ├── learnings/     # Aprendizados
│   ├── decisions/     # Decisoes arquiteturais
│   └── troubleshooting/ # Problemas conhecidos
└── .claude/           # Configuracoes Claude
```

## Regras de Ouro

1. **Nunca perca contexto** - Sempre leia memory.md primeiro
2. **Sempre documente** - Use /consolidar ao final
3. **Mantenha historico** - Nunca delete sessoes ou conhecimento
4. **Git e obrigatorio** - Todo trabalho deve ser versionado
5. **TypeScript strict** - Sempre use tipagem forte
6. **SOPs sao lei** - Seguir procedimentos documentados
7. **Triangular informacoes** - Usar multiplas fontes antes de concluir

## Regras do Worklog (CRITICO)

**ANTES de gerar qualquer worklog, LER `.claude/commands/worklog.md`**

| Regra | Descricao |
|-------|-----------|
| Idioma | **Ingles 100%** - NUNCA portugues |
| Pessoa | Terceira pessoa ("Thiago worked on...") |
| Slack | NUNCA citar mensagens. Usar apenas para CONTEXTO |
| Artifacts | Sempre incluir links clicaveis |
| Outcomes | Cada tema deve ter resultado concreto |

## APIs Integradas

| API | Documentacao | Escopo | Status |
|-----|--------------|--------|--------|
| Slack Web API | knowledge-base/api/slack.md | Mensagens, canais, threads | OK |
| Linear SDK | knowledge-base/api/linear.md | Issues, comentarios | OK |
| Google Drive API | knowledge-base/api/drive.md | Arquivos, metadados | OK |
| **CODA API** | knowledge-base/api/coda.md | Docs, tabelas, status | OK |
| GitHub API | (via gh CLI) | Repos, PRs | OK |

## Padroes de Codigo

- **Nomenclatura**: camelCase para variaveis, PascalCase para tipos/classes
- **Imports**: Usar path aliases (@types/, @utils/, etc.)
- **Exports**: Barrel exports via index.ts
- **Erros**: Sempre tratar erros explicitamente

## Capacidade Investigativa

Ao receber pedido de investigacao:

1. **Identificar fontes relevantes:**
   - Slack (search:read) - conversas e contexto
   - Linear - tickets e historico
   - CODA - documentacao oficial
   - Drive - arquivos e versoes
   - Obsidian - notas locais

2. **Triangular informacoes:**
   - Cruzar dados de pelo menos 2 fontes
   - Verificar timestamps para consistencia
   - Identificar gaps de informacao

3. **Gerar output estruturado:**
   - Resumo executivo
   - Evidencias com links
   - Nivel de confianca
   - Proximos passos

## Equipe TSA (Referencia)

| Pessoa | Foco | Contato |
|--------|------|---------|
| **Thiago** | Lead, Arquitetura | @thiago |
| **Diego** | Brevo, CallRail, People.ai | @diego |
| **Gabrielle** | Dixa, Zendesk, Mailchimp | @gabrielle |
| **Carlos** | Apollo, Gong | @carlos |
| **Alexandra** | mParticle, Syncari, WFS | @alexandra |

---

**IMPORTANTE:** Estas instrucoes garantem continuidade, qualidade e padronizacao entre sessoes.
**Ultima atualizacao:** 2026-01-26
