# RFC Reviews - Learnings

> Aprendizados da análise dos RFCs de Category Definition e Delivery Phases - Jan 2026

## Contexto

Dois RFCs importantes para revisão:
1. **RFC Category Definition** - Definir categoria de mercado da TestBox
2. **RFC Detailed Phases for Delivery** - Processo de delivery com incorporação de Data Engineering

## RFC 1: Category Definition

### O Problema
- "Demo automation" é armadilha - commoditizado, TAM limitado
- Clientes usam vocabulário antigo ("demo", "sandbox")
- TestBox está underselling - clientes se surpreendem com a profundidade

### Paralelo com Gong
- Gong: "Conversation Intelligence" → "Revenue Intelligence"
- Pattern: [Domain] + [Noun] que cria gap recognition
- TestBox: "Do you have _______?" → qual palavra?

### Sugestão: Product Readiness
- "Do you have product readiness?" → gap imediato
- Cobre todos os use cases (demo-ready, test-ready, training-ready)
- Não é jargon, qualquer exec entende

### Insight Adicional: Service Model como Moat
- TestBox não é só plataforma, é modelo de serviço
- TSA/FDE embedded + DE support + GTM envolvido
- Competidor pode copiar tech, não pode copiar o cuidado
- Categoria deveria refletir isso de alguma forma

### Linguagem Real de Cliente
- "Same results as our live account" - Intuit
- "Is this real data or fake?" - pergunta comum
- Fidelity + Control = core value

## RFC 2: Detailed Phases for Delivery

### Gap Principal: DE não incorporado
O RFC foi escrito antes do time DE ser formalizado. Precisa atualizar para refletir:
- Thais como DE Lead
- Yasmin como Associate DE
- DE como parte do processo, não "if available"

### Modelo de Dados - Questão Central
Três opções possíveis:
1. FDE define requirements → DE gera datasets → FDE valida para cenário
2. FDE gera dados simples → DE gera dados complexos
3. FDE faz tudo → DE só valida

**Recomendação:** Opção 1 parece ser o modelo na prática. Clarificar no RFC.

### Onde DE Deve Entrar

| Fase | Mudança Necessária |
|------|-------------------|
| Phase 1 | Adicionar [DE Lead] Data engineering resource allocation |
| Phase 3 | Adicionar DE nos Roles; mudar "[TSAs] Generate datasets" para "[DE] Generate" |
| Phase 3 Stage Gate | Adicionar "DE validated" |
| Phase 5 | Mudar "Data Quality (if available)" para "[DE Lead] Final validation" |
| Escalation | Adicionar DE → DE Lead → Director |

### Conexão com Performance Excellence
- DE Gate Compliance é behavior core no Performance Excellence Framework
- RFC Phases deve refletir isso como stage gate formal
- Toda data work passa por Thais/Yasmin antes de deploy

### Terminologia
- RFC usa "TSA"
- Solutions Excellence 2026 usa "FDE" (Forward Deployed Engineer)
- Atualizar para consistência

## Lições Aprendidas

### 1. Tom de Comentários
- Comentários "polidos demais" parecem AI-made
- Usar inglês básico, tom humilde
- Fazer perguntas ao invés de afirmar

### 2. Análise Específica > Genérica
- Primeiro round de análise foi genérico ("precisa de 4 weeks")
- Segundo round focou no pedido real: incorporar DE
- Sempre entender o que foi pedido antes de analisar

### 3. Usar Evidência dos Projetos
- Projetos reais (WFS, TCO, Canada) são evidência
- "Na prática, fazemos assim" > "Deveria ser assim"
- Conectar com experiência de implementação

### 4. Perguntar ao Invés de Afirmar
- "Should DE be in roles here?" > "DE must be in roles"
- "What do you think?" convida discussão
- Humildade abre portas

## Arquivos de Referência

| Arquivo | Uso |
|---------|-----|
| Solutions_Excellence_2026_CEO_v7.docx | Estrutura do time, 4-week mentality |
| PERFORMANCE_EXCELLENCE_v1_EXECUTIVE.md | DE Gate Compliance, Top 10 Behaviors |
| RFC_ Detailed Phases for delivery.docx | Documento sendo revisado |
| RFC_ TestBox Category Definition.docx | Documento de positioning |

---

*Documentado em: 2026-01-06*
*Sessão: sessions/2026-01-06_19-00.md*
