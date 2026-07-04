# Invariantes Financeiras

**Sprint:** 7
**Data:** 2026-06-26

---

## Definição

Invariantes são regras que devem ser sempre verdadeiras no sistema. Se violadas, indicam corrupção de dados ou bug.

---

## Invariantes Fundamentais

### FI-01: Toda direito financeiro possui origem operacional
Todo FinancialSnapshot e todo FinancialFact devem ser rastreáveis a pelo menos um fato operacional (Assignment ou Extra). Não podem existir fatos financeiros " órfãos ".

### FI-02: Todo fato financeiro é rastreável
Cada FinancialFact deve conter referência ao evento de domínio que o gerou. O campo `source_event` deve estar preenchido.

### FI-03: Período fechado não recalcula automaticamente
Ao fechar uma competência, os snapshots são gerados uma única vez. Não há recálculo automático. Reconsolidação requer reabertura explícita.

### FI-04: Extra rejeitado nunca gera direito
Um Extra com status `rejected` não pode, em nenhuma circunstância, gerar FinancialFact. Estado terminal e imutável.

### FI-05: Assignment cancelado revoga elegibilidade
Um Assignment com status `cancelled` não gera direito financeiro, mesmo que anteriormente tenha estado `completed`. O cancelamento é retroativo.

### FI-06: Competência paga é imutável
Um Period com status `paid` não pode ter seus snapshots alterados. Qualquer correção requer processo manual fora do sistema.

### FI-07: CoverageSnapshot precede FinancialSnapshot
Não pode existir FinancialSnapshot sem CoverageSnapshot correspondente para a mesma competência. A ordem é: Coverage → Financial.

### FI-08: Todo snapshot pertence a exatamente uma competência
Cada CoverageSnapshot e FinancialSnapshot deve estar vinculado a exatamente um Period. Não podem existir snapshots " órfãos ".

### FI-09: Duração do fact é positiva
Todo FinancialFact deve possuir `duration_minutes > 0`. Fatos com duração zero ou negativa são inválidos.

### FI-10: Médico deve existir e estar ativo
Todo FinancialFact deve referenciar um Doctor que existe e está ativo (`active = true`). Doctors inativos não geram novos direitos.

### FI-11: Extra pendente não gera direito
Um Extra com status `pending` não pode gerar FinancialFact. Apenas `approved` gera direito.

### FI-12: Reabertura invalida snapshots anteriores
Ao reabrir uma competência, todos os CoverageSnapshots e FinancialSnapshots anteriores devem ser marcados como `invalidated`. Novos snapshots são gerados na reconsolidação.

### FI-13: Um médico não pode ter dois Assignments ativos no mesmo período
Não podem existir dois Assignments com status `started` ou `confirmed` para o mesmo médico em períodos sobrepostos do mesmo Shift.

### FI-14: Consolidação é idempotente
Executar o Coverage Engine duas vezes para a mesma competência (sem alterações) deve produzir o mesmo resultado.

### FI-15: Snapshot é imutável após criação
Um CoverageSnapshot ou FinancialSnapshot, uma vez criado, não pode ser alterado. Pode ser invalidado (por reabertura) mas não modificado.

---

## Invariantes de Validação

### FV-01: Todo FinancialFact possui tipo válido
O campo `fact_type` deve ser um dos: `assignment_completion`, `extra_approved`.

### FV-02: Todo FinancialFact possui competência válida
O campo `period_id` deve referenciar um Period existente.

### FV-03: Todo FinancialFact possui médico válido
O campo `doctor_id` deve referenciar um Doctor existente.

### FV-04: CoverageSnapshot contém pelo menos um fact
Um CoverageSnapshot não pode ser vazio. Se não há direitos, não deve ser criado.

### FV-05: FinancialSnapshot contém pelo menos um fact
Um FinancialSnapshot não pode ser vazio. Se não há direitos, não deve ser criado.

---

## Resumo

| ID | Invariant | Tipo |
|---|---|---|
| FI-01 | Toda direito possui origem operacional | Fundamental |
| FI-02 | Todo fato é rastreável | Fundamental |
| FI-03 | Período fechado não recalcula | Fundamental |
| FI-04 | Extra rejeitado nunca gera direito | Fundamental |
| FI-05 | Assignment cancelado revoga elegibilidade | Fundamental |
| FI-06 | Competência paga é imutável | Fundamental |
| FI-07 | Coverage precede Financial | Ordem |
| FI-08 | Todo snapshot pertence a uma competência | Referência |
| FI-09 | Duração do fact é positiva | Validação |
| FI-10 | Médico deve existir e estar ativo | Referência |
| FI-11 | Extra pendente não gera direito | Validação |
| FI-12 | Reabertura invalida snapshots | Lifecycle |
| FI-13 | Sem dois Assignments ativos sobrepostos | Integridade |
| FI-14 | Consolidação é idempotente | Comportamento |
| FI-15 | Snapshot é imutável após criação | Lifecycle |
| FV-01 | Tipo de fact válido | Validação |
| FV-02 | Competência válida | Referência |
| FV-03 | Médico válido | Referência |
| FV-04 | Snapshot não vazio (coverage) | Validação |
| FV-05 | Snapshot não vazio (financial) | Validação |
