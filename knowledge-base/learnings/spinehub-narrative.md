# Aprendizado: SpineHub e Narrative Renderer

**Data:** 2025-12-23
**Contexto:** Resolver problema de worklogs que listavam metadata ao invés de contar histórias

## O Problema

O worklog gerado pelo CORTEX estava assim:
```
### Documentation
- SOW_WFS_v2.docx [ref:4]
- Meeting_Notes_12-10.md [ref:7]
- Spreadsheet.xlsx [ref:12]
```

Isso é **metadata**, não uma **história**. O usuário quer saber O QUE ACONTECEU, não uma lista de arquivos.

## A Solução: SpineHub (Layer 3.5)

### Conceito
SpineHub é uma camada intermediária que CONSOLIDA o conteúdo real antes de gerar a narrativa.

### Pipeline
```
Collection → Normalization → Clustering → SpineHub → Narrative → Post
                                            ↑
                                    (Layer 3.5 - NOVO)
```

### O que o SpineHub faz
1. Lê os raw_exports de todas as fontes
2. Extrai o CONTEÚDO real (texto das mensagens, não só metadata)
3. Separa mensagens do owner vs contexto
4. Agrupa por tema/projeto
5. Gera NarrativeBlocks prontos para storytelling

### Estrutura do SpineHubData
```typescript
{
  slack: {
    ownerMessages: [],    // Mensagens que EU enviei
    contextMessages: [],  // Mensagens que vi/recebi
    channelsSummary: Map  // Resumo por canal
  },
  drive: { files },
  local: { files },
  claude: { interactions },
  linear: { issues },
  narrativeBlocks: []     // Blocos prontos para narrativa
}
```

## O Resultado

Agora o worklog fica assim:
```
### Intuit WFS Project

**Context:** Release and deployment coordination

**Tuesday, Dec 16, 2025**

At 19:52, Hey guys quick update to support the WFS SOW...
```

Isso é uma **HISTÓRIA** - conta o que aconteceu, quando, e em que contexto.

## Regras Aprendidas

### 1. Conteúdo > Metadata
- ERRADO: Listar nomes de arquivos
- CERTO: Descrever o que foi feito com os arquivos

### 2. Cronologia é Importante
- Agrupar por tema
- Dentro de cada tema, seguir ordem cronológica
- Usar datas e horários reais

### 3. Contexto é Essencial
- Não basta dizer "arquivo modificado"
- Precisa dizer POR QUE foi modificado

### 4. Owner vs Context
- Separar o que EU fiz do que eu apenas VI
- Worklog é sobre MEU trabalho

## Implementação Técnica

### SpineHub (`src/spinehub/index.ts`)
- `buildSpineHub()` - Função principal
- Lê arquivos de raw_exports
- Processa cada fonte separadamente
- Gera NarrativeBlocks

### Narrative Renderer (`src/worklog/narrative.ts`)
- `renderNarrativeWorklog()` - Gera markdown narrativo
- Usa SpineHub.narrativeBlocks quando disponível
- Fallback para workstreams se não tiver SpineHub

## Próximos Passos

1. Melhorar extração de conteúdo do Claude Code
2. Adicionar correlação entre eventos (Slack + arquivo = relacionados)
3. Implementar resumo automático de threads longas

---

*Documentado em: 2025-12-23*
