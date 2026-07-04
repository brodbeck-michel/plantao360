# Invariantes — Extras de Plantão

**Data:** 2026-06-26
**Sprint:** 6

---

## Invariantes Obligatórias

Todas as invariantes listadas abaixo **nunca** poderão ser violadas pelo sistema.

### Estruturais

| ID | Invariante | Descrição |
|----|------------|-----------|
| I01 | Extra pertence a exatamente um Plantão | Todo Extra deve estar vinculado a um único Shift |
| I02 | Extra pertence a exatamente um Médico | Todo Extra deve estar vinculado a um único Doctor |
| I03 | Duração > 0 | A duração de um Extra deve ser sempre maior que zero |
| I04 | Justificativa obrigatória | Todo Extra deve possuir uma justificativa não vazia |
| I05 | Período deve existir | O Plantão vinculado deve pertencer a um Período válido |

### Temporais

| ID | Invariante | Descrição |
|----|------------|-----------|
| I06 | Extra não pode existir em Período fechado | O Período associado deve estar em status draft |
| I07 | Extra não pode existir em Período pago | O Período associado não pode estar em status paid |
| I08 | Extra registrado com timestamp | Todo Extra deve possuir created_at e updated_at |

### Comportamentais

| ID | Invariante | Descrição |
|----|------------|-----------|
| I09 | Extra cancelado não participa da remuneração | Extras com status cancelled são excluídos do cálculo |
| I10 | Extra removido não participa da remuneração | Extras removidos são excluídos do cálculo |
| I11 | Dados financeiros não editáveis após fechamento | Duração não pode ser alterada após Period.close() |
| I12 | Extra não pode ser transferido | shift_id e doctor_id são imutáveis após criação |

### Integridade

| ID | Invariante | Descrição |
|----|------------|-----------|
| I13 | Doctor deve existir | O doctor_id referenciado deve existir na tabela doctors |
| I14 | Shift deve existir | O shift_id referenciado deve existir na tabela shifts |
| I15 | Shift não pode estar cancelado | Extras não podem ser criados para Plantões cancelados |

---

## Validação no Código

```python
# I03: Duração > 0
CheckConstraint("duration_minutes > 0", name="ck_shift_extra_duration_positive")

# I04: Justificativa obrigatória
nullable=False  # na coluna justification

# I01, I02: Foreign Keys
ForeignKey("shifts.id", ondelete="CASCADE")  # I01
ForeignKey("doctors.id", ondelete="RESTRICT")  # I02
```

---

## Invariantes Futuras (Payroll)

| ID | Invariante | Descrição |
|----|------------|-----------|
| IF01 | Limite diário de Extras | Máximo X extras por médico por dia |
| IF02 | Limite mensal de Extras | Máximo Y extras por médico por mês |
| IF03 | Limite financeiro | Total não pode exceder Z% do salário |
| IF04 | Multiplicador válido | Tipo de Extra deve ter multiplicador definido |
