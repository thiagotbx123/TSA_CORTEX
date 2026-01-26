# SOPs - Procedimentos Operacionais TSA

> Documentacao de rotinas operacionais da equipe TSA para execucao padronizada.

## Estrutura

```
sops/
├── README.md              # Este arquivo
├── linear/               # Procedimentos Linear
│   ├── criar-ticket.md
│   ├── triage-ticket.md
│   └── escalar-ticket.md
├── coda/                 # Procedimentos CODA
│   ├── atualizar-status.md
│   └── documentar-cliente.md
├── comunicacao/          # Procedimentos de comunicacao
│   ├── daily-report.md
│   ├── escalation.md
│   └── handoff.md
└── investigacao/         # Procedimentos de investigacao
    ├── debug-integracao.md
    └── analise-root-cause.md
```

## Formato Padrao de SOP

Cada SOP deve seguir este template:

```markdown
# SOP: [Nome do Procedimento]

## Objetivo
[Por que esse procedimento existe]

## Quando Usar
[Trigger/gatilho para executar]

## Pre-requisitos
- [O que precisa estar pronto antes]

## Passos

### 1. [Primeiro Passo]
[Descricao detalhada]

### 2. [Segundo Passo]
[Descricao detalhada]

## Outputs Esperados
- [O que deve existir ao final]

## Troubleshooting
| Problema | Solucao |
|----------|---------|
| [Erro comum] | [Como resolver] |

## Referencias
- [Link para documentacao relacionada]
```

## APIs Disponiveis para Automacao

| API | Docs | Uso |
|-----|------|-----|
| Linear | `../api/linear.md` | Criar/atualizar tickets |
| CODA | `../api/coda.md` | Documentacao cliente |
| Slack | `../api/slack.md` | Notificacoes |
| Drive | `../api/drive.md` | Arquivos |

## Convencoes

1. **Nomes de arquivo:** kebab-case (ex: `criar-ticket.md`)
2. **Idioma:** Portugues para descricoes, ingles para comandos/codigo
3. **Exemplos:** Sempre incluir exemplo real
4. **Automacao:** Indicar se pode ser automatizado

---

**Mantido por:** Thiago Rodrigues (TSA Lead)
**Ultima atualizacao:** 2026-01-26
