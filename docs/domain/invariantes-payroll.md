# Invariantes — Payroll & Competência Financeira

**Sprint:** 9
**Data:** 2026-06-26

---

## Invariantes Fundamentais

### P1 — Toda competência possui versão
Toda `PayrollCompetency` deve possuir ao menos uma `PayrollVersion`. A versão inicial é criada junto com a competência.

### P2 — Toda competência possui selo após aprovação
Ao transitar para `approved`, uma `PayrollCompetency` deve ter um `PayrollSeal` associado contendo snapshot completo.

### P3 — Toda competência utiliza snapshots
O cálculo de uma competência é baseado exclusivamente em `FinancialSnapshot` e `RemunerationResult`. Nunca consulta dados operacionais.

### P4 — Nenhuma competência consulta dados operacionais durante processamento
Ao calcular, revisar ou aprovar, o sistema usa apenas dados já consolidados (FinancialSnapshot, RemuneraçãoResult). Nunca acessa Assignment, Shift, Extra ou Coverage.

### P5 — Competência aprovada é imutável
Após transitar para `approved`, nenhum dado da competência pode ser alterado. Apenas reabertura (que gera nova versão) permite modificação.

### P6 — Reabertura gera nova versão
Ao reabrir uma competência, o sistema cria uma nova `PayrollVersion` com os dados atualizados. A versão anterior permanece no histórico.

### P7 — Toda alteração é rastreável
Cada transição de estado registra: timestamp, responsável, ação executada, estado anterior, estado seguinte.

### P8 — Toda competência possui explicação
Cada `PayrollCompetency` deve possuir uma `PayrollExplanation` que documenta, passo a passo, como cada remuneração foi calculada.

### P9 — Toda competência possui snapshot de auditoria
Cada `PayrollCompetency` deve possuir um `PayrollAuditSnapshot` que registra todas as ações executadas sobre a competência.

### P10 — Versão é imutável
Uma `PayrollVersion`, após criada, não pode ser alterada. Qualquer mudança requer criação de nova versão.

---

## Invariantes de Transição

### P11 — Transições seguem ordem definida
O ciclo de vida segue: `draft → calculated → reviewed → approved → exported → paid → archived`. Nenhuma transição pode pular etapas (exceto reabertura).

### P12 — Reabertura requer justificativa
Ao reabrir uma competência, o campo `reopen_reason` deve ser obrigatoriamente preenchido.

### P13 — Reabertura invalida aprovações anteriores
Ao reabrir, a competência retorna ao estado `calculated`. Aprovções e exportações anteriores são invalidadas.

### P14 — Cálculo requer dados de entrada
Uma competência só pode transitar para `calculated` se existir um `FinancialSnapshot` válido associado.

### P15 — Revisão requer cálculo prévio
Uma competência só pode transitar para `reviewed` se estiver em estado `calculated`.

---

## Invariantes de Dados

### P16 — Selagem é irreversível
Após criar um `PayrollSeal`, ele não pode ser modificado ou removido. Apenas a competência pode ser reabriada (criando nova versão).

### P17 — Explicação é imutável
Cada `CalculationExplanation` dentro de uma `PayrollExplanation` não pode ser alterada após criação.

### P18 — Snapshot de auditoria é append-only
O `PayrollAuditSnapshot` pode receber novos registros, mas registros existentes não podem ser alterados.

### P19 — Competência não pode ser duplicada
Não pode existir mais de uma competência ativa para o mesmo período (year_month) no mesmo estado.

### P20 — Total da competência é consistente
O `total_value` de uma competência deve ser igual à soma dos `total_value` de todos os `DoctorRemuneration` associados.

---

## Invariantes de Consistência

### P21 — Regras aplicadas são snapshotadas
As `RemunerationRule` aplicadas em uma competência são copiadas para o `PayrollSeal`. Alterações futuras nas regras não afetam competências anteriores.

### P22 — Fatos de entrada são snapshotados
Os `FinancialFactData` de entrada são copiados para o `PayrollSeal`. Alterações futuras nos fatos não afetam competências anteriores.

### P23 — Resultados são snapshotados
Os `DoctorRemuneration` de resultado são copiados para o `PayrollSeal`. Alterações futuras nos resultados não afetam competências anteriores.

### P24 — Cálculos são reproduzíveis
Dado o mesmo `FinancialSnapshot` e as mesmas `RemunerationRule`, o `RemunerationEngine` sempre produz o mesmo resultado.

### P25 — Auditoria é consistente com estados
O `PayrollAuditSnapshot` deve refletir todas as transições de estado ocorridas. Nenhuma transição pode estar ausente.
