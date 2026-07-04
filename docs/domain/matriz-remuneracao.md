# Matriz de Remuneração

**Sprint:** 8
**Data:** 2026-06-26

---

## Definição

Para cada tipo de fato financeiro, documenta-se como ele se transforma em remuneração.

---

## Fatos Financeiros e Remuneração

### assignment_completion

| Propriedade | Valor |
|---|---|
| **Gera remuneração?** | Sim |
| **Depende de tabela?** | Sim — RemunerationRule do tipo `assignment_completion` |
| **Depende de política?** | Sim — PricingPolicy seleciona regra vigente |
| **Pode ser recalculado?** | Sim — competência deve estar `draft` |
| **Pode ser estornado?** | Sim — competência reaberta + fact revogado |
| **Exige auditoria?** | Sim — CalculationExplanation obrigatória |
| **Fórmula base** | `hour_rate × duration_hours × multiplier` |
| **Fonte de hour_rate** | Doctor.hour_rate (pode ser sobrescrito por regra) |

### extra_approved

| Propriedade | Valor |
|---|---|
| **Gera remuneração?** | Sim |
| **Depende de tabela?** | Sim — RemunerationRule do tipo `extra_approved` |
| **Depende de política?** | Sim — PricingPolicy seleciona regra vigente |
| **Pode ser recalculado?** | Sim — competência deve estar `draft` |
| **Pode ser estornado?** | Sim — competência reaberta + fact revogado |
| **Exige auditoria?** | Sim — CalculationExplanation obrigatória |
| **Fórmula base** | `hour_rate × duration_hours × multiplier` |
| **Fonte de hour_rate** | Doctor.hour_rate (pode ser sobrescrito por regra) |

---

## Regras de Exemplo

### Regra Padrão (assignment_completion)

```yaml
rule_id: "AC-001"
fact_type: "assignment_completion"
version: "1.0"
valid_from: "2025-01-01"
valid_until: null
hour_rate_source: "doctor"
multiplier: 1.0
description: "Remuneração padrão para plantão completado"
```

### Regra Extra (extra_approved)

```yaml
rule_id: "EX-001"
fact_type: "extra_approved"
version: "1.0"
valid_from: "2025-01-01"
valid_until: null
hour_rate_source: "doctor"
multiplier: 1.0
description: "Remuneração padrão para hora extra aprovada"
```

### Regra Feriado (assignment_completion + holiday)

```yaml
rule_id: "AC-H01"
fact_type: "assignment_completion"
version: "1.0"
valid_from: "2025-01-01"
valid_until: null
hour_rate_source: "doctor"
multiplier: 1.5
condition: "is_holiday"
description: "Remuneração para plantão em feriado"
```

---

## Fluxo de Cálculo

```
1. FinancialFact(fact_type="assignment_completion", duration_minutes=480, doctor_id=1)
        │
2. PricingPolicy.evaluate(fact, doctor, period)
   → seleciona regra "AC-H01" (feriado detectado)
        │
3. RemuneraçãoCalculator.calculate(fact, rule)
   → hour_rate = 150.00 (do Doctor)
   → duration_hours = 8.0
   → multiplier = 1.5 (regra de feriado)
   → valor = 150.00 × 8.0 × 1.5 = 1800.00
        │
4. CalculationExplanation
   → fatos: [FinancialFact#123]
   → regra: "AC-H01" v1.0
   → etapas: [hour_rate=150, duration=8h, multiplier=1.5]
   → total: 1800.00
```

---

## Resumo

| Fato | Gera Remuneração | Regra Padrão | Multiplicador Base |
|---|---|---|---|
| `assignment_completion` | Sim | AC-001 | 1.0 |
| `extra_approved` | Sim | EX-001 | 1.0 |
