# Learning: QuickBooks Cross-Dataset Journal Entry Reference

**Data:** 2026-01-13
**Ticket:** PLA-3135
**Conta afetada:** quickbooks-test-account-nv3@tbxofficial.com

---

## Problema

Ao rodar "create activity plan", erro de parsing em Journal Entry lines que não encontravam accounts.

## Causa Raiz

**Referência cruzada de account_ids entre datasets diferentes.**

As linhas de `QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY_LINE` estavam no dataset `b6695ca6-9184-41f3-862e-82a182409617`, mas referenciavam accounts do dataset `3e1337cc-70ca-4041-bc95-0fe29181bb12` (non-profit).

```
Dataset Journal Entry:  b6695ca6-9184-41f3-862e-82a182409617
Dataset Accounts:       3e1337cc-70ca-4041-bc95-0fe29181bb12  ← ERRADO
```

## Dados Afetados

| Métrica | Valor |
|---------|-------|
| Linhas afetadas | 84 (ids 133-216) |
| Journal Entries | 12 (ids 25-36) |
| Accounts órfãos | 6 (444, 465, 472, 703, 707, 708) |

## Por que não dava pra mapear

Os accounts tinham nomes como **"Due to Rise"** - contas intercompany específicas do ambiente non-profit. "Rise" é uma company que só existe no non-profit, então não faz sentido existir no outro dataset.

## Solução

**Deletar os dados órfãos** (não tinham como ser corrigidos):

```sql
-- Deletar linhas
DELETE FROM QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY_LINE
WHERE id BETWEEN 133 AND 216;

-- Deletar Journal Entries
DELETE FROM QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY
WHERE id BETWEEN 25 AND 36
  AND dataset_id = 'b6695ca6-9184-41f3-862e-82a182409617';
```

## Query útil para detectar o problema

```sql
SELECT
    QIJEL.id,
    journal_entry_id,
    QIJE.dataset_id AS journal_entry_dataset_id,
    account_id,
    QCOA.dataset_id AS account_dataset_id
FROM
    QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY_LINE QIJEL
LEFT JOIN QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY QIJE
    ON QIJE.ID = QIJEL.JOURNAL_ENTRY_ID
LEFT JOIN QUICKBOOKS_CHART_OF_ACCOUNTS QCOA
    ON QCOA.ID = QIJEL.ACCOUNT_ID
WHERE
    QCOA.DATASET_ID != QIJE.DATASET_ID;
```

## Aprendizados

1. **Em Multi-Entity/Multi-Dataset:** Account IDs são únicos por dataset, não globais
2. **Contas "Due to/Due from [Company]":** São específicas de intercompany e só fazem sentido se a company existir no mesmo ambiente
3. **Ao popular dados de teste:** Sempre verificar se os IDs referenciados pertencem ao mesmo dataset
4. **Validação sugerida:** Antes de inserir Journal Entry lines, verificar se `account_id` existe no mesmo `dataset_id` do Journal Entry

## Tabelas envolvidas

- `QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY` - Header dos JEs
- `QUICKBOOKS_INTERCOMPANY_JOURNAL_ENTRY_LINE` - Linhas dos JEs
- `QUICKBOOKS_CHART_OF_ACCOUNTS` - Plano de contas

## Tags

#quickbooks #dataset #journal-entry #intercompany #data-quality #PLA-3135
