# Comando /worklog - Geração de Worklog Semanal

> Este comando define o fluxo OBRIGATÓRIO para geração de worklogs.
> **ARQUITETURA:** CLI coleta dados → Claude gera narrativa → Claude posta no Linear

## Fluxo de Execução

### Passo 1: Perguntar Período
**SEMPRE perguntar ao usuário:**
- Data de início
- Data de fim
- Sugerir opções comuns (última semana, últimos 5 dias úteis, etc.)

```
Exemplo:
"Qual período você quer para o worklog?"
- Última semana (7 dias)
- Últimos 5 dias úteis
- Semana passada (seg-sex)
- Personalizado (você define)
```

### Passo 2: Confirmar Fontes
**Perguntar quais fontes coletar:**
- Slack (mensagens e DMs)
- Linear (issues)
- Google Drive (arquivos)
- Local (arquivos locais)
- Claude (sessões de código)

Default: Todas habilitadas no config.

### Passo 3: Rodar Coleta
Executar **APENAS** o comando `collect` (NÃO usar `run`):
```bash
node dist/cli/index.js collect --start {DATA_INICIO} --end {DATA_FIM}
```

Isso gera:
- `raw_exports/raw_events_*.json` (dados brutos)
- `output/context_for_narrative.json` (contexto consolidado para Claude)

### Passo 4: Ler Contexto e Gerar Narrativa (CLAUDE FAZ ISSO)

**EU (Claude) leio o arquivo `output/context_for_narrative.json` e gero a narrativa manualmente.**

**REGRAS RAC-14 (OBRIGATÓRIAS):**

| Regra | Descrição |
|-------|-----------|
| Idioma | Inglês 100% |
| Pessoa | Terceira pessoa ("Thiago worked on...") |
| Slack | NUNCA citar mensagens. Usar apenas para CONTEXTO |
| Título | "Worklog" para < 7 dias, "Weekly Worklog" para >= 7 dias |
| Artifacts | Sempre incluir links clicáveis `[Nome](URL)` |
| Outcomes | Cada tema deve ter um resultado concreto |
| Contagens | DEVEM reconciliar (soma = total) |

**ESTRUTURA DO WORKLOG:**

```markdown
# Worklog - {Owner Name}

## Summary
| Period | {dates} |
|--------|---------|
| Sources | Slack (X), Drive (Y), Linear (Z), Local (W), Claude (C) |
| Total Events | {sum} |

## Objective
{1 parágrafo descrevendo escopo geral}

---

## {Tema 1}
{Narrativa em terceira pessoa, sem quotes de Slack}

**Artifacts:**
- [Nome do arquivo](URL)

**Outcome:** {resultado concreto}

---

## {Tema 2}
...

---

## References
| Document | Type | Link |
|----------|------|------|
| ... | ... | [Open](URL) |

---

| Author | {name} |
|--------|--------|
| Role | Technical Solutions Architect |
| Generated | {date} |
| Tool | TSA_CORTEX v1.0 |
```

### Passo 5: Apresentar Resumo
Mostrar ao usuário:
- Quantidade de eventos por fonte
- Preview da narrativa gerada
- Perguntar: "Aprovar e postar no Linear?"

### Passo 6: Postar no Linear (com aprovação)

**APENAS se o usuário aprovar**, usar a API do Linear para criar o ticket.

Opção 1 - Usar o CLI com markdown pronto:
```bash
# Salvar markdown em arquivo e usar poster
```

Opção 2 - Claude posta diretamente via API.

---

## Regras

1. **NUNCA pular o Passo 1** - Sempre perguntar período
2. **NUNCA usar `run` command** - O CLI `run` gera output ruim. Usar apenas `collect`
3. **NARRATIVA É GERADA POR CLAUDE** - Eu leio context_for_narrative.json e gero a história
4. **NUNCA citar Slack diretamente** - Slack = contexto, não quotes
5. **NUNCA criar ticket sem aprovação** - Passo 6 é obrigatório
6. **Mostrar progresso** - Usuário deve saber o que está acontecendo
7. **Permitir cancelamento** - Usuário pode parar a qualquer momento

---

## Exemplo de Interação

```
Usuário: "Oi, quero gerar meu worklog"

Claude: "Vamos gerar seu worklog! Primeiro, qual período?"
        [Opções de período]

Usuário: "18 a 19 de dezembro"

Claude: "Confirma coletar de: Slack, Linear, Drive, Local, Claude?"

Usuário: "Sim"

Claude: [Roda: node dist/cli/index.js collect --start 2025-12-18 --end 2025-12-19]
        "Coletando dados..."
        [Progresso da coleta]
        "Pronto! Encontrei:
         - Slack: 213 eventos
         - Linear: 3 eventos
         - Drive: 40 eventos
         - Local: 16 eventos
         - Claude: 18 eventos
         - Total: 290 eventos"

Claude: [Lê output/context_for_narrative.json]
        [Analisa dados e gera narrativa RAC-14]
        [Mostra preview do worklog em markdown]

        "Este é o worklog gerado. Aprovar e postar no Linear?"

Usuário: "Aprova"

Claude: [Posta no Linear]
        "Ticket criado: https://linear.app/testbox/issue/RAC-XX"
```

---

## Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `output/context_for_narrative.json` | Contexto consolidado que Claude lê |
| `raw_exports/raw_events_*.json` | Dados brutos por fonte |
| `data/spinehub.json` | Knowledge graph persistente |

---

*Atualizado em: 2025-12-24*
*Arquitetura: CLI coleta → Claude narra → Claude posta*
