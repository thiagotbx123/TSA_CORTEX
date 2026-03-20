# KPI Delivery Tracker - Explicacao dos Indicadores

> Documento de referencia sobre os 7 indicadores da aba **"Thiago Calculations"** na planilha KPI Team Raccoons.

---

## Visao Geral

A aba exibe **7 indicadores** para cada um dos 5 TSAs (Alexandra, Carlos, Diego, Gabrielle, Thiago), com granularidade **semanal** (segunda a sexta). Os dados vem da aba **DB**, que consolida todas as tarefas das abas individuais de cada TSA.

Cada celula representa **1 pessoa x 1 semana**. Semanas futuras ficam em branco.

---

## 1. TSA Internal Demands (Entregas Internas)

**Pergunta:** As estimativas de prazo das demandas internas estao sendo cumpridas?

**O que mede:** Percentual de tarefas **internas** (ex: melhorias de processo, automacoes, documentacao) entregues dentro do prazo (ETA).

**Formula:**
```
On Time / (On Time + Late)
```

- **On Time** = tarefa concluida ate a data do ETA original
- **Late** = tarefa concluida apos a data do ETA original
- Tarefas em andamento (In Progress, Overdue, On Track) **nao entram** no calculo
- Se nao ha nenhuma entrega na semana, o resultado e **100%** (considera-se meta atingida)

**Meta:** > 90%

**Cores:**
| Cor | Faixa |
|-----|-------|
| Verde | >= 90% |
| Amarelo | 50% a 89% |
| Vermelho | < 50% |

---

## 2. TSA External Demands (Entregas Externas)

**Pergunta:** As estimativas de prazo das demandas externas estao sendo cumpridas?

**O que mede:** Mesmo calculo do indicador anterior, porem filtrado apenas para tarefas **externas** (ex: entregas para clientes, configuracoes de ambiente, suporte a demos).

**Formula:**
```
On Time / (On Time + Late)
```

**Meta:** > 90%

**Cores:** Mesmas do Internal Demands.

**Por que separar Interno de Externo?** Demandas externas impactam diretamente clientes e parceiros. Separar permite identificar se o time esta priorizando entregas externas corretamente ou se ha desbalanco.

---

## 3. Throughput (Vazao de Entregas/Semana)

**Pergunta:** Quantas tarefas cada TSA conclui por semana?

**O que mede:** Contagem simples de tarefas com status **"Done"** naquela semana, independente de serem internas ou externas.

**Formula:**
```
COUNTIFS(pessoa, semana, status = "Done")
```

**Meta:** >= 5 tarefas/semana

**Cores:**
| Cor | Faixa |
|-----|-------|
| Verde | >= 5 |
| Amarelo | 2 a 4 |
| Vermelho | < 2 |

**Interpretacao:** Mede produtividade bruta. Um throughput consistentemente baixo pode indicar bloqueios, tarefas muito grandes sem quebra, ou sobrecarga em tarefas nao rastreadas.

---

## 4. Overdue Snapshot (Tarefas Atrasadas)

**Pergunta:** Quantas tarefas estao vencidas (passaram do ETA sem entrega) em cada semana?

**O que mede:** Contagem de tarefas com performance **"Overdue"** naquela semana — ou seja, tarefas que ainda nao foram concluidas e ja passaram do prazo.

**Formula:**
```
COUNTIFS(pessoa, semana, performance = "Overdue")
```

**Meta:** 0 (zero tarefas atrasadas)

**Cores:**
| Cor | Faixa |
|-----|-------|
| Verde | 0 |
| Amarelo | 1 a 2 |
| Vermelho | >= 3 |

**Interpretacao:** Diferente do Late (que ja foi entregue com atraso), Overdue significa que a tarefa **ainda esta aberta** alem do prazo. E um indicador de risco — tarefas overdue precisam de atencao imediata.

---

## 5. WIP - Work in Progress (Trabalho em Andamento)

**Pergunta:** Quantas tarefas cada TSA tem abertas simultaneamente por semana?

**O que mede:** Contagem de tarefas com status **"In Progress"** naquela semana.

**Formula:**
```
COUNTIFS(pessoa, semana, status = "In Progress")
```

**Meta:** <= 3 tarefas simultaneas

**Cores:**
| Cor | Faixa |
|-----|-------|
| Verde | <= 3 |
| Amarelo | 4 a 6 |
| Vermelho | >= 7 |

**Interpretacao:** WIP alto indica multitasking excessivo. Estudos mostram que mais de 3-4 tarefas simultaneas reduz a qualidade e aumenta o tempo de entrega de todas elas. O ideal e manter o WIP baixo e focar em concluir antes de iniciar novas tarefas.

---

## 6. Internal Tasks - Count (Contagem de Tarefas Internas)

**Pergunta:** Quantas tarefas internas cada TSA tem registradas por semana?

**O que mede:** Contagem total de tarefas classificadas como **"Internal"** naquela semana, independente do status (Done, In Progress, Overdue, etc).

**Formula:**
```
COUNTIFS(pessoa, semana, categoria = "Internal")
```

**Meta:** Sem meta fixa (indicador de volume/distribuicao)

**Cores:** Sem formatacao condicional (numeros puros)

**Interpretacao:** Permite visualizar a carga de trabalho interno vs externo. Se um TSA tem muitas tarefas internas e poucas externas, pode indicar que esta sendo subutilizado em demandas de cliente, ou que esta investindo em melhorias de processo.

---

## 7. External Tasks - Count (Contagem de Tarefas Externas)

**Pergunta:** Quantas tarefas externas (voltadas a clientes) cada TSA tem por semana?

**O que mede:** Contagem total de tarefas classificadas como **"External"** naquela semana, independente do status.

**Formula:**
```
COUNTIFS(pessoa, semana, categoria = "External")
```

**Meta:** Sem meta fixa (indicador de volume/distribuicao)

**Cores:** Sem formatacao condicional (numeros puros)

**Interpretacao:** Complementa o indicador anterior. Juntos, Internal + External Count mostram a distribuicao de esforco do time. O ideal e que a maior parte das tarefas sejam externas (entrega de valor ao cliente), com internas sendo investimento em eficiencia.

---

## Conceitos Importantes

### Como o ETA e calculado?
- Se uma tarefa tem **multiplas datas** no campo ETA (ex: prazos renegociados), o sistema usa a **data mais antiga** (compromisso original)
- Isso garante que renegociacoes nao "mascarem" atrasos

### Como a Delivery Date e calculada?
- Se ha multiplas datas no campo de entrega, o sistema usa a **data mais recente** (entrega final efetiva)

### Classificacao de Performance (coluna K do DB)
| Status | Significado |
|--------|-------------|
| **On Time** | Entregue (Done) dentro do ETA |
| **Late** | Entregue (Done) apos o ETA |
| **Overdue** | Nao entregue e ETA ja passou |
| **On Track** | Em andamento e ETA ainda nao chegou |
| **N/A** | Sem ETA definido |

### Semana sem entregas = 100%
- Por decisao do gestor (Waki), semanas onde um TSA nao tem nenhuma tarefa concluida (nem On Time nem Late) contam como **100%** nos indicadores de Delivery
- Logica: se nao havia nada para entregar, a meta foi cumprida

---

## Fonte dos Dados

```
Abas individuais (DIEGO, GABI, CARLOS, ALEXANDRA, THIAGO)
    |
    v
DBBuilder.gs.js (Apps Script, roda a cada edicao + 1x por hora)
    |
    v
Aba DB (consolidada, ~400 linhas, 12 colunas)
    |  IMPORTRANGE
    v
Aba DB_Data (na planilha KPI)
    |  COUNTIFS
    v
Aba "Thiago Calculations" (7 indicadores x 5 TSAs x semanas)
```

---

*Documento gerado em 2026-03-12 | Projeto: TSA_CORTEX/KPI Delivery Tracker*
