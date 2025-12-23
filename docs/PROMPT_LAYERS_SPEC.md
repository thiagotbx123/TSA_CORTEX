# TSA CORTEX - Especificação de Camadas do Prompt

## Problema Atual
O output atual mistura:
- Trabalho que EU fiz
- Coisas que eu apenas VI nos canais
- Arquivos sensíveis/pessoais
- Contexto de outros projetos onde não participo

## Arquitetura Proposta: 5 Camadas Independentes

Cada camada tem:
- Input definido
- Output definido
- Regras próprias
- Pode ser modificada sem afetar as outras

---

# CAMADA 1: COLETA (Raw Data)

## Objetivo
Coletar dados brutos das fontes, aplicando apenas filtros técnicos básicos.

## Input
- Credenciais das APIs
- Período de datas
- User ID do owner

## Output
```
raw_events_{source}.json
```

## Fontes e O Que Coletar

### Slack
| Coletar | Não Coletar |
|---------|-------------|
| Mensagens do owner (by user_id) | Mensagens de outros users |
| DMs onde owner participou | Canais onde owner não postou nada |
| Threads onde owner respondeu | Mensagens de bots/integrações |

### Linear
| Coletar | Não Coletar |
|---------|-------------|
| Issues criadas pelo owner | Issues apenas visualizadas |
| Issues comentadas pelo owner | Issues de outros users |
| Issues atribuídas ao owner | |

### Google Drive
| Coletar | Não Coletar |
|---------|-------------|
| Arquivos owned by owner | Arquivos apenas visualizados |
| Arquivos editados pelo owner | Arquivos shared mas não tocados |
| Meeting recordings do owner | |

### Local Files
| Coletar | Não Coletar |
|---------|-------------|
| Arquivos modificados no período | Arquivos de sistema |
| Downloads relevantes | Arquivos temporários (~$, .tmp) |
| | Credenciais (*.json com secret) |

### Claude Code
| Coletar | Não Coletar |
|---------|-------------|
| Prompts do owner | |
| Responses relevantes | Warmup/sistema |
| Por projeto | |

## Filtros de Exclusão Automática (Blacklist)
```
ARQUIVOS_EXCLUIR = [
    "**/client_secret*.json",
    "**/*.env",
    "**/credentials*.json",
    "**/.tmp*",
    "**/~$*"
]

CANAIS_EXCLUIR_SE_NAO_POSTOU = true
```

---

# CAMADA 2: ATRIBUIÇÃO (Ownership)

## Objetivo
Determinar o que é TRABALHO DO OWNER vs o que é apenas CONTEXTO.

## Input
```
raw_events_{source}.json
```

## Output
```
attributed_events.json
{
  "my_work": [...],      // Ações diretas do owner
  "context": [...],      // Observado mas não feito
  "excluded": [...]      // Removido por regras
}
```

## Regras de Atribuição

### Slack
| Critério | Classificação |
|----------|---------------|
| user_id == owner | MY_WORK |
| Canal onde owner postou 0 msgs | EXCLUDED |
| Menção ao owner sem resposta | CONTEXT |
| Thread onde owner respondeu | MY_WORK (só a resposta) |

### Linear
| Critério | Classificação |
|----------|---------------|
| Criado pelo owner | MY_WORK |
| Comentado pelo owner | MY_WORK |
| Atribuído ao owner | MY_WORK |
| Apenas visualizado | EXCLUDED |

### Drive
| Critério | Classificação |
|----------|---------------|
| Owner == owner email | MY_WORK |
| lastModifyingUser == owner | MY_WORK |
| Apenas shared | CONTEXT |
| Meeting recording com owner | MY_WORK |

### Local/Claude
| Critério | Classificação |
|----------|---------------|
| Tudo do computador local | MY_WORK |

---

# CAMADA 3: CLASSIFICAÇÃO (Workstreams)

## Objetivo
Agrupar MY_WORK em workstreams/projetos reconhecíveis.

## Input
```
attributed_events.json (apenas my_work)
```

## Output
```
classified_work.json
{
  "workstreams": [
    {
      "name": "WFS SOW",
      "type": "customer_project",
      "items": [...],
      "summary": "..."
    }
  ]
}
```

## Regras de Classificação

### Por Keywords/Patterns
```
WORKSTREAM_PATTERNS = {
    "WFS SOW": ["wfs", "workforce", "mineral", "sow"],
    "GEM Project": ["gem", "ats", "recruiting"],
    "TSA CORTEX": ["cortex", "worklog", "automation"],
    "Intuit Release": ["release", "fall", "february", "quickbooks"],
    "TSA Management": ["daily", "sync", "standup", "tsa-"],
}
```

### Por Canal/Projeto
```
CANAL_TO_WORKSTREAM = {
    "intuit-internal": "Intuit WFS",
    "gem-internal": "GEM Project",
    "tsa-data-engineers": "TSA Internal",
}
```

### Por Tipo de Arquivo
```
FILE_TYPE_WORKSTREAM = {
    "SOW*.docx": "Customer SOW",
    "*_Training*.md": "Documentation",
    "*recording*": "Meetings",
}
```

---

# CAMADA 4: SÍNTESE (Narrativa Cronológica por Tema)

## Objetivo
Contar a HISTÓRIA do que aconteceu no período, correlacionando dados de
múltiplas fontes por TEMA, seguindo cronologia. Documentar a rotina de
trabalho como um relato, não como lista de itens.

## Input
```
classified_work.json
```

## Output
```
worklog_narrative.md
```

## Estrutura do Output (ORDEM FIXA)

### Seção 1: Título
Formato: `[Worklog]{YY_MM_DD} TSA {Nome da Pessoa}`

```markdown
# [Worklog]25_12_17 TSA Thiago Rodrigues
```

### Seção 2: Summary (Metadata da Coleta)
```markdown
## Summary

| Campo | Valor |
|-------|-------|
| Período | 10/12/2025 a 17/12/2025 |
| Owner | Thiago Rodrigues |
| Gerado em | 17/12/2025 às 14:30 BRT |
| Fontes | Slack, Drive, Linear, Local, Claude |
```

### Seção 3: NARRATIVA POR TEMA (Núcleo do Documento)
```markdown
## Narrativa da Semana

### Tema: WFS SOW Development

**Contexto:**
Projeto de criação do Statement of Work para Intuit Workforce Solutions,
incluindo análise de Mineral HR e definição de escopo para demos.

**Cronologia:**

**Terça-feira, 10/12**

Às 09:30, iniciei a análise do documento base do SOW que havia sido
compartilhado pela Alexandra no Drive [ref:1]. O documento continha o
template padrão da TestBox mas precisava ser adaptado para o contexto
específico do WFS.

Durante a tarde, às 14:15, troquei mensagens com Katherine no Slack
discutindo o escopo do Mineral HR e se deveria ser incluído como módulo
separado ou integrado ao WFS principal [ref:2]. A decisão foi manter
integrado por ora.

**Quarta-feira, 11/12**

Participei da reunião de sync às 10:00 com o time TSA onde apresentei
o progresso do SOW. A gravação está disponível [ref:3]. O feedback
principal foi incluir mais detalhes sobre timeline de implementação.

Às 15:30, baseado no feedback, criei a primeira versão consolidada do
SOW e subi para o Drive [ref:4].

**Quinta-feira, 12/12**

Katherine enviou feedback via Slack às 09:45 pedindo ajustes na seção
de deliverables [ref:5]. Fiz as alterações e atualizei o documento
às 14:00 [ref:6].

Criei uma issue no Linear para tracking do projeto [ref:7].

**Resultado:**
SOW v2 finalizado e aguardando review final do cliente.

---

### Tema: TSA CORTEX Development

**Contexto:**
Desenvolvimento de ferramenta interna para automatizar geração de worklogs.

**Cronologia:**

**Segunda-feira, 16/12**

Às 07:48, iniciei sessão no Claude Code para trabalhar no projeto
intuit-boom [ref:8]. O objetivo era criar o coletor de dados do Claude.

{... continua com narrativa real ...}

**Resultado:**
CORTEX v1.0 funcional com 5 coletores integrados.

---
```

### Seção 4: Referências (Logo após Narrativa)
```markdown
## Referências

| Ref | Fonte | Descrição | Link |
|-----|-------|-----------|------|
| 1 | Drive | SOW_WFS_Template.docx | [abrir](https://docs.google.com/...) |
| 2 | Slack | Thread #intuit-internal | [ver](https://testbox-talk.slack.com/...) |
| 3 | Drive | Recording TSA Sync 11/12 | [assistir](https://drive.google.com/...) |
| 4 | Drive | SOW_WFS_v1.docx | [abrir](https://docs.google.com/...) |
| 5 | Slack | DM Katherine | [ver](https://testbox-talk.slack.com/...) |
| 6 | Drive | SOW_WFS_v2.docx | [abrir](https://docs.google.com/...) |
| 7 | Linear | RAC-10 WFS SOW Tracking | [ver](https://linear.app/testbox/...) |
| 8 | Claude | Sessão intuit-boom 16/12 | local: ~/.claude/projects/... |
```

### Seção 5: Decisões e Bloqueios
```markdown
## Decisões Tomadas
- [12/12] Mineral HR será integrado ao WFS, não separado [ref:2]
- [15/12] Formato de worklog aprovado pelo time [ref:X]

## Bloqueios Identificados
- Aguardando acesso ao ambiente de homologação Mineral
- Pendente confirmação de data do February Release
```

### Seção 6: RESUMO EXECUTIVO (ÚLTIMO - Mostra Valor Estratégico)
```markdown
## Resumo Executivo

### Esforço Aplicado
| Indicador | Valor | Contexto |
|-----------|-------|----------|
| Horas de reunião | 12h | 8 reuniões com TSAs + 4 syncs externos |
| Mensagens enviadas | 550 | Coordenação com 6 stakeholders |
| Documentos produzidos | 12 | SOWs, specs, training materials |
| Issues gerenciadas | 9 | 7 criadas, 2 comentadas |

### Entregas do Período
| Entrega | Status | Impacto |
|---------|--------|---------|
| WFS SOW v2 | Concluído | Habilita kickoff com Intuit em Jan |
| GEM Training Docs | Concluído | 5 documentos de capacitação prontos |
| CORTEX v1.0 | MVP funcional | Automatiza ~4h/semana de reporting |
| February Release Analysis | Em andamento | 18 features mapeadas de 24 |

### Colaboração e Coordenação
| Métrica | Valor |
|---------|-------|
| Pessoas coordenadas diretamente | 8 |
| Canais Slack ativos | 6 |
| Clientes/Projetos impactados | 3 (Intuit WFS, GEM, Internal Tools) |
| Threads de decisão participadas | 15 |

### Volume de Trabalho Documentado
| Fonte | Quantidade | % do Total |
|-------|------------|------------|
| Slack (mensagens enviadas) | 550 | 55% |
| Drive (arquivos criados/editados) | 45 | 5% |
| Linear (issues tocadas) | 9 | 1% |
| Reuniões (com gravação) | 12 | 1% |
| Claude Code (prompts desenvolvimento) | 382 | 38% |
| **Total de evidências rastreáveis** | **998** | **100%** |

### Valor Gerado
- **Documentação**: 5 SOWs/specs que habilitam próximas fases de projeto
- **Automação**: Ferramenta CORTEX reduz 4h/semana em reporting manual
- **Coordenação**: 8 pessoas alinhadas em 3 projetos paralelos
- **Rastreabilidade**: 100% das atividades documentadas com evidência
```

### Seção 7: Footer
```markdown
---
*Gerado por TSA CORTEX v1.0.0 em 2min 34s*
*Fontes: Slack, Drive, Linear, Local Files, Claude Code*
*Filtros: Apenas ações do owner, sem trabalho de terceiros*
```

## Regras de Geração da Narrativa

1. **Agrupar por TEMA, não por fonte**
   - Um tema pode ter evidências de Slack + Drive + Linear + Claude
   - Mesmo tema aparece junto, mesmo que eventos sejam de dias diferentes

2. **Cronologia DENTRO de cada tema**
   - Ordenar por data/hora
   - Usar formato: "Dia da semana, DD/MM" + "Às HH:MM"

3. **Texto narrativo, não bullet points**
   - Escrever como relato: "Às 14:00, finalizei..."
   - Conectar eventos relacionados

4. **Toda afirmação tem referência**
   - Usar [ref:N] inline
   - Tabela de referências no final com links clicáveis

5. **Correlacionar eventos automaticamente**
   - Slack às 10:00 + arquivo editado às 10:30 = relacionados
   - Reunião + notas da reunião = mesmo contexto

### NÃO INCLUIR
- Next Week Plans (especulativo)
- Trabalho de outros (context)
- Arquivos sensíveis
- Afirmações sem referência verificável

---

# CAMADA 5: AUDITORIA (Validação)

## Objetivo
Permitir que o owner revise e aprove antes de publicar.

## Input
```
worklog_narrative.md
classified_work.json
```

## Output
```
worklog_final.md (aprovado)
audit_log.json (decisões do owner)
```

## Processo de Auditoria

### Passo 1: Apresentar Resumo
```
Workstreams detectados:
1. [x] WFS SOW (12 itens)
2. [x] GEM Project (8 itens)
3. [ ] TSA CORTEX (15 itens) <- owner desmarca se não quer

Remover algum? (digite números separados por vírgula)
```

### Passo 2: Arquivos Sensíveis
```
Arquivos potencialmente sensíveis detectados:
1. [!] conta_pessoal.xlsx
2. [!] DANFE.pdf

Remover? (s/n para cada)
```

### Passo 3: Preview Final
```
=== PREVIEW DO TICKET ===
[mostra o markdown final]

Aprovar e criar ticket? (s/n)
```

---

# VALIDAÇÃO COM O OWNER

## Perguntas para Cada Camada

### Camada 1 (Coleta)
- [ ] Os filtros de exclusão automática estão corretos?
- [ ] Alguma fonte deve ser ignorada completamente?
- [ ] Algum canal específico deve ser excluído?

### Camada 2 (Atribuição)
- [ ] A regra "excluir canal se não postou" está OK?
- [ ] Contexto de outros deve aparecer em algum lugar?
- [ ] Menções ao owner devem contar como work?

### Camada 3 (Classificação)
- [ ] Os workstreams detectados fazem sentido?
- [ ] Precisa adicionar/remover algum padrão?
- [ ] A classificação por canal está correta?

### Camada 4 (Síntese)
- [ ] A estrutura do output está boa?
- [ ] Falta alguma seção importante?
- [ ] Alguma seção deve ser removida?

### Camada 5 (Auditoria)
- [ ] O processo de review está adequado?
- [ ] Precisa de mais checkpoints?
- [ ] A preview final é suficiente?

---

# IMPLEMENTAÇÃO

Cada camada será um módulo separado:
```
src/
  layers/
    01_collection/
      index.ts
      filters.ts
      blacklist.ts
    02_attribution/
      index.ts
      rules.ts
    03_classification/
      index.ts
      patterns.ts
      workstreams.ts
    04_synthesis/
      index.ts
      templates.ts
      narrative.ts
    05_audit/
      index.ts
      prompts.ts
      approval.ts
```

Mudança em uma camada NÃO afeta as outras.
