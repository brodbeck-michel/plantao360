# Invariantes de Remuneração

**Sprint:** 8
**Data:** 2026-06-26

---

## Invariantes Fundamentais

### IR-01: Todo cálculo possui origem financeira
Todo RemunerationResult deve ser derivado de pelo menos um FinancialFact. Não podem existir cálculos " órfãos " sem fatos de entrada.

### IR-02: Nenhuma remuneração existe sem FinancialFact
Não pode existir RemunerationResult sem que exista pelo menos um FinancialFact associado. A remuneração é sempre uma transformação de fatos.

### IR-03: Todo cálculo é reproduzível
Dado o mesmo FinancialFact e a mesma RemuneraçãoRule, o cálculo sempre produz o mesmo resultado. Não depende de estado externo, data de execução, ou aleatoriedade.

### IR-04: Toda remuneração é auditável
Todo RemuneraçãoResult deve possuir uma CalculationExplanation associada. A explicação deve ser completa e imutável.

### IR-05: Todo cálculo possui explicação
CalculationExplanation é obrigatória. Sem explicação, o cálculo é inválido.

### IR-06: Regra vigente é única por tipo e data
Para um determinado fact_type e data, apenas uma RemuneraçãoRule pode estar vigente. Não podem existir regras sobrepostas para o mesmo tipo.

### IR-07: Simulação não persiste
RemuneraçãoCalculator em modo simulação não altera banco de dados. Resultados são apenas objetos de memória.

### IR-08: Payroll é consumidor puro
Payroll não calcula regras. Apenas consolida resultados já calculados pelo Remuneration Engine.

### IR-09: Cálculo é determinístico
O mesmo input sempre produz o mesmo output. Não depende de horário de execução, estado do banco, ou fatores externos.

### IR-10: Regras são imutáveis
Uma RemuneraçãoRule criada não pode ser alterada. Para mudanças, cria-se uma nova versão com período de vigência diferente.

---

## Invariantes de Validação

### IV-01: Fact type deve ser suportado
Apenas fatos com `fact_type` conhecido podem ser calculados. Tipos suportados: `assignment_completion`, `extra_approved`.

### IV-02: Duração deve ser positiva
Todo FinancialFact utilizado deve possuir `duration_minutes > 0`.

### IV-03: Doctor deve existir e estar ativo
Todo FinancialFact utilizado deve referenciar um Doctor ativo com `hour_rate > 0`.

### IV-04: Regra deve estar vigente
A RemuneraçãoRule selecionada deve possuir `valid_from <= fact_date` e (`valid_until is null` ou `valid_until > fact_date`).

### IV-05: Resultado deve ser não negativo
O valor calculado para cada fato deve ser >= 0. Valores negativos são inválidos.

---

## Invariantes de Lifecycle

### IL-01: Resultado é imutável após criação
Um RemuneraçãoResult, uma vez criado, não pode ser alterado. Para recálculo, cria-se um novo resultado e invalida o anterior.

### IL-02: Explicação é imutável
CalculationExplanation, uma vez criada, não pode ser modificada.

### IL-03: Invalidação é registrada
Ao invalidar um resultado, o evento `remuneration.invalidated.v1` deve ser disparado.

### IL-04: Reabertura invalida resultados
Ao reabrir uma competência, todos os RemunerationResults anteriores devem ser invalidados.

---

## Resumo

| ID | Invariant | Tipo |
|---|---|---|
| IR-01 | Todo cálculo possui origem financeira | Fundamental |
| IR-02 | Nenhuma remuneração sem FinancialFact | Fundamental |
| IR-03 | Todo cálculo é reproduzível | Fundamental |
| IR-04 | Toda remuneração é auditável | Fundamental |
| IR-05 | Todo cálculo possui explicação | Fundamental |
| IR-06 | Regra vigente é única por tipo e data | Integridade |
| IR-07 | Simulação não persiste | Comportamento |
| IR-08 | Payroll é consumidor puro | Arquitetura |
| IR-09 | Cálculo é determinístico | Comportamento |
| IR-10 | Regras são imutáveis | Lifecycle |
| IV-01 | Fact type suportado | Validação |
| IV-02 | Duração positiva | Validação |
| IV-03 | Doctor ativo e válido | Referência |
| IV-04 | Regra vigente | Validação |
| IV-05 | Resultado não negativo | Validação |
| IL-01 | Resultado imutável | Lifecycle |
| IL-02 | Explicação imutável | Lifecycle |
| IL-03 | Invalidação registrada | Lifecycle |
| IL-04 | Reabertura invalida resultados | Lifecycle |
