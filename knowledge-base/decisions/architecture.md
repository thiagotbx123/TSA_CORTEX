# Decisões Arquitetônicas - TSA_CORTEX

## ADR-001: Stack Tecnológica

**Data:** 2024-12-22
**Status:** Aceita

### Contexto
Precisamos escolher a stack para um sistema de automação de worklog que:
- Coleta dados de múltiplas APIs (Slack, Linear, Drive)
- Processa e normaliza eventos
- Gera outputs em múltiplos formatos
- Funciona como CLI

### Decisão
**TypeScript + Node.js**

### Alternativas Consideradas
| Opção | Prós | Contras |
|-------|------|---------|
| Python | Boas libs de data processing | Tipagem fraca, packaging complexo |
| Go | Alta performance, binário único | Ecossistema menor para APIs |
| TypeScript | Tipagem forte, bom ecossistema | Overhead de compilação |

### Consequências
- Tipagem forte ajuda com schemas complexos
- Excelente suporte para APIs REST
- CLI com Commander.js
- Fácil integração com APIs do ecossistema

---

## ADR-002: Estrutura de Eventos Canônica

**Data:** 2024-12-22
**Status:** Aceita

### Contexto
Eventos vêm de múltiplas fontes com formatos diferentes. Precisamos de um formato canônico.

### Decisão
Interface `ActivityEvent` com campos obrigatórios e source pointers.

```typescript
interface ActivityEvent {
  event_id: string;           // Hash estável
  source_system: SourceSystem;
  source_record_id: string;
  actor_user_id: string;
  event_timestamp_utc: string;
  event_type: EventType;
  title: string;
  body_text_excerpt: string;  // Max 500 chars
  source_pointers: SourcePointer[];
  confidence: 'low' | 'medium' | 'high';
}
```

### Consequências
- Todos os eventos são comparáveis
- Deduplicação possível via source pointers
- Rastreabilidade garantida

---

## ADR-003: Clustering por Tópicos

**Data:** 2024-12-22
**Status:** Aceita

### Contexto
Worklog precisa agrupar eventos relacionados em "workstreams".

### Decisão
Clustering em duas fases:
1. Agrupar por issue ID (Linear)
2. Agrupar por keywords para eventos restantes

### Tipos de Cluster
- customer, project, incident, feature
- ops, internal, meeting, documentation, other

### Consequências
- Issues do Linear automaticamente agrupadas
- Eventos sem issue agrupados por contexto
- Alguns eventos podem ficar "unclustered"

---

## ADR-004: Roteamento por Role

**Data:** 2024-12-22
**Status:** Aceita

### Contexto
Diferentes pessoas/roles devem postar worklogs em times diferentes do Linear.

### Decisão
Configuração de routing por role:
```json
{
  "tsa": { "linear_team": "raccoons", "labels": ["worklog", "weekly"] },
  "default": { "linear_team": "ops", "labels": ["worklog", "weekly"] }
}
```

### Consequências
- TSAs postam automaticamente no time "raccoons"
- Fácil adicionar novos roles
- Labels configuráveis por role

---

## ADR-005: PII Redaction

**Data:** 2024-12-22
**Status:** Aceita

### Contexto
Worklogs podem conter informações sensíveis.

### Decisão
Redação automática de:
- Emails
- Telefones
- CPF/CNPJ
- Números de cartão
- Patterns customizáveis

### Consequências
- Worklogs seguros para compartilhar
- Dados brutos mantidos localmente (encrypted)
- Flag `pii_redaction_applied` indica se houve redação
