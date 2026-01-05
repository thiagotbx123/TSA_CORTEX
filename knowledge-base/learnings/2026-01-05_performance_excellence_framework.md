# Performance Excellence Framework v1

> Aprendizados da criação do sistema de feedback para TSAs - Jan 2026

## Contexto

Necessidade de criar um framework de feedback estruturado para o time de TSAs (Diego, Alexandra, Carlos, Gabrielle) que:
- Se alinhe ao TestBox 3.0 (AI-first, patterns, evidence)
- Não adicione overhead burocrático
- Produza desenvolvimento real, não apenas métricas

## Fontes Pesquisadas

| Fonte | O Que Aprendemos | Como Aplicamos |
|-------|------------------|----------------|
| **Netflix 4A** | Feedback direto: Aim to Assist, Actionable, Appreciate, Accept/Discard | Base filosófica do framework |
| **Spotify Health Check** | Sistema semáforo (verde/amarelo/vermelho) para auto-avaliação | Visual scoring system |
| **Google CFR** | Conversations, Feedback, Recognition contínuos | Weekly touchpoints |
| **Amy Edmondson PSI** | Psychological Safety como #1 preditor de performance | Team health dimensions |
| **Working Out Loud** | Knowledge sharing visível, generosidade | Learning capture behavior |
| **ONA** | Mapear influência real, detectar silos | Team-level collaboration metrics |

## Decisões Críticas

### 1. Top 10 Behaviors (não 40)

**Problema:** Framework original tinha 40 behaviors → fatigue garantida, sem foco.

**Solução:** Selecionar apenas 10 behaviors que:
- Impactam diretamente delivery (cycle time, rework)
- São observáveis com evidência
- Já fazem parte do workflow TSA
- Cobrem requisitos TestBox (DE gate, patterns, AI)

### 2. Zero New Meetings

**Problema:** Proposta original tinha weekly pulse, monthly health check, quarterly 360.

**Solução:** Embed tudo em rituais existentes:
- Daily Slack Update → template estruturado
- Friday Standup → +5 min patterns/learnings
- Biweekly Retro → +15 min team health pulse
- Monthly → async focus selection

### 3. Team-Only Slack Metrics

**Problema:** Individual response time tracking = surveillance vibes.

**Solução:**
- Apenas métricas de time (avg response, thread resolution)
- Core hours only
- "Signal, not score" - usado em retro, nunca para avaliação individual

### 4. Evidence Links Obrigatórios

**Problema:** Scoring subjetivo sem prova.

**Solução:** Cada behavior precisa de evidence link:
- "Done" → link para artifact
- "Blocked" → link para thread
- "Pattern" → link para library entry

### 5. DE Gate como Behavior Core

**Problema:** Data Engineering review não estava no framework original.

**Solução:** Behavior #8: DE Gate Compliance
- Toda data work passa por Thais/Yasmin
- Ticket mostra approval antes de deploy
- Triagem P0/P1/P2

## Top 10 Behaviors (Q1)

```
1. Clear Daily Update          → Done/Doing/Blocked + link
2. Blocker + Ask + Follow-up   → Ask thread com resolução
3. Ticket Ownership E2E        → Single owner, no orphans
4. Evidence for Claims         → Link para artifact
5. Pattern Contribution        → Entry com acceptance criteria
6. AI Usage (Analysis/Exec)    → Exemplo compartilhado
7. Data Quality Checklist      → Checkbox no ticket
8. DE Gate Compliance          → Approval de Thais/Yasmin
9. Escalation Timing           → <24h se blocked >4h
10. Learning Capture           → Post #learnings semanal
```

## Outcome Metrics (Tied to Delivery)

| Metric | Definition | Target |
|--------|------------|--------|
| Cycle Time | Ticket created → delivered | Trending down |
| Rework Rate | Reopened 7d OR dataset rejected | <10% |
| Pattern Contributions | New patterns in library | 1/person/month |
| Unblock Time | Blocked → unblocked | <24h avg |
| DE Gate Compliance | % data work reviewed | 100% |

## Ownership

| Role | Responsibility |
|------|----------------|
| **Thiago (Lead)** | Monthly focus selection, retro behavior review, 1st escalation |
| **Waki (Director)** | 2nd escalation, quarterly calibration, system adjustments |
| **Team** | Self-assess, provide evidence, flag blockers |
| **Thais/Yasmin** | DE gate reviewers |

## Templates Criados

1. **Daily Update** - Max 3 projects, Done/Today/Blocked + links
2. **15-min Feedback Script** - SBI + Feedforward
3. **Monthly Focus Selection** - 2 behaviors per person
4. **DE Review Packet** - Context, Objective, Changes, Evidence, P0/P1/P2
5. **Pattern Template** - Com acceptance criteria

## Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `Performance_Excellence_v1.docx` | Doc executivo para leadership |
| `Performance_Excellence_v1.xlsx` | Excel operacional (7 abas) |
| `PERFORMANCE_EXCELLENCE_v1_EXECUTIVE.md` | Markdown completo |

## Lições Aprendidas

### 1. Less is More
40 behaviors parece completo, mas ninguém vai seguir. 10 behaviors focados > 40 genéricos.

### 2. Embed, Don't Add
Novos rituais morrem. Embed em rituais existentes funciona.

### 3. Evidence Kills Subjectivity
"Eu acho que você fez bem" vs "Aqui está o link provando" - diferença brutal.

### 4. Team Metrics, Not Individual
Slack response time individual = medo e gaming. Team avg = signal útil.

### 5. Tie to Delivery
Behaviors sem conexão com outcomes (cycle time, rework) viram burocracia.

## Próximos Passos

1. Leadership alignment no docx
2. Introduzir ao time no Friday standup
3. Primeira monthly focus selection
4. Q1 retro na semana 12

---

*Documentado em: 2026-01-05*
*Sessão: sessions/2026-01-05_14-00.md*
