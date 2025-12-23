# Comando /worklog - Geração de Worklog Semanal

> Este comando define o fluxo OBRIGATÓRIO para geração de worklogs.

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
Executar coletores para o período definido:
```bash
node dist/cli/index.js collect --start {DATA_INICIO} --end {DATA_FIM}
```

Mostrar progresso ao usuário.

### Passo 4: Montar Worklog Completo
1. Rodar SpineHub para consolidar conteúdo
2. Gerar Narrative com a história real
3. Salvar worklog em output/

```bash
node dist/cli/index.js run --start {DATA_INICIO} --end {DATA_FIM} --dry-run
```

### Passo 5: Apresentar Resumo
Mostrar ao usuário:
- Quantidade de eventos por fonte
- Workstreams/temas detectados
- Preview do worklog (primeiras seções)

Perguntar:
- "Quer remover algum workstream?"
- "Algum arquivo sensível para excluir?"

### Passo 6: Aprovação Final
Mostrar preview completo e perguntar:
- "Aprovar e criar ticket no Linear? (s/n)"

Se aprovado:
```bash
node dist/cli/index.js run --start {DATA_INICIO} --end {DATA_FIM}
```

---

## Regras

1. **NUNCA pular o Passo 1** - Sempre perguntar período
2. **NUNCA criar ticket sem aprovação** - Passo 6 é obrigatório
3. **Mostrar progresso** - Usuário deve saber o que está acontecendo
4. **Permitir cancelamento** - Usuário pode parar a qualquer momento

---

## Exemplo de Interação

```
Usuário: "Oi, quero gerar meu worklog"

Claude: "Vamos gerar seu worklog! Primeiro, qual período?"
        [Opções de período]

Usuário: "Últimos 5 dias úteis"

Claude: "Confirma coletar de: Slack, Linear, Drive, Local, Claude?"

Usuário: "Sim"

Claude: "Coletando dados..."
        [Progresso da coleta]
        "Pronto! Encontrei:
         - 450 mensagens Slack
         - 8 issues Linear
         - 25 arquivos Drive

         Workstreams detectados:
         1. WFS SOW Development
         2. TSA CORTEX
         3. Team Meetings

         Quer ver o preview?"

Usuário: "Sim"

Claude: [Mostra preview do worklog]
        "Aprovar e criar ticket no Linear?"

Usuário: "Aprova"

Claude: "Ticket criado: https://linear.app/..."
```

---

*Criado em: 2025-12-23*
