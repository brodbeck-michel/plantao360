# Matriz de Consistência

**Sprint:** 7
**Data:** 2026-06-26

---

## Definição

Documenta combinações inválidas de estado entre entidades. Cada inconsistência possui uma decisão documentada sobre como o Coverage Engine deve tratá-la.

---

## Inconsistências Identificadas

### IC-01: Assignment cancelado + Extra aprovado

**Cenário:** Um Assignment foi cancelado, mas um Extra associado ao mesmo Shift foi aprovado.

**Status:** Válido. Extra e Assignment são independentes.

**Decisão:** O Coverage Engine processa normalmente. O Assignment cancelado não gera direito. O Extra aprovado gera direito. Não há inconsistência.

---

### IC-02: Assignment inexistente + Extra criado

**Cenário:** Um Extra é criado para um Shift que não possui Assignment para o médico.

**Status:** Inconsistente.

**Decisão:** O Coverage Engine detecta e registra como `inconsistency.type=extra_without_assignment`. O Extra continua válido (pode ser work beyond shift), mas é marcado para revisão.

---

### IC-03: Período fechado + Novo Extra

**Cenário:** Um Extra é criado após o fechamento da competência.

**Status:** Inválido.

**Decisão:** O sistema deve impedir a criação de Extras em competências fechadas. Se ocorrer, o Coverage Engine registra como `inconsistency.type=extra_after_closure` e exclui o Extra da consolidação.

---

### IC-04: Médico inativo + Assignment iniciado

**Cenário:** Um médico foi desativado, mas possui Assignment com status `started`.

**Status:** Inconsistente.

**Decisão:** O Coverage Engine detecta e registra como `inconsistency.type=inactive_doctor_assignment`. O Assignment não gera direito enquanto o médico estiver inativo.

---

### IC-05: Assignment completed + Shift cancelled

**Cenário:** Um Assignment está `completed`, mas o Shift pai está `cancelled`.

**Status:** Inconsistente.

**Decisão:** O Coverage Engine detecta e registra como `inconsistency.type=completed_assignment_on_cancelled_shift`. O Assignment não gera direito (Shift cancelado revoga).

---

### IC-06: Dois Assignments sobrepostos no mesmo Shift

**Cenário:** Dois Assignments para o mesmo médico no mesmo Shift possuem horários sobrepostos.

**Status:** Inconsistente.

**Decisão:** O Coverage Engine detecta e registra como `inconsistency.type=overlapping_assignments`. Apenas um Assignment gera direito (o de menor duração ou o mais recente,取决于 política).

---

### IC-07: Extra sem justificativa

**Cenário:** Um Extra foi criado sem justificativa.

**Status:** Inválido (impedido pela modelagem).

**Decisão:** O campo `justification` é obrigatório no model. Não pode ocorrer.

---

### IC-08: Extra com duração zero ou negativa

**Cenário:** Um Extra possui `duration_minutes` igual a zero ou negativo.

**Status:** Inválido (impedido pela modelagem).

**Decisão:** CheckConstraint `duration_minutes > 0` impede. Não pode ocorrer.

---

### IC-09: Assignment started mas não completed após fechamento

**Cenário:** Um Assignment está `started` (não `completed`) e a competência foi fechada.

**Status:** Inconsistente.

**Decisão:** O Coverage Engine detecta e registra como `inconsistency.type=incomplete_assignment_at_closure`. O Assignment não gera direito. Registro pendente até correção.

---

### IC-10: Período paid + Correção solicitada

**Cenário:** Tenta-se alterar dados de uma competência já paga.

**Status:** Inválido.

**Decisão:** O sistema impede alterações em competências pagas. Se ocorrer, o Coverage Engine rejeita a consolidação e registra `inconsistency.type=modification_after_payment`.

---

### IC-11: Doctor hour_rate = 0

**Cenário:** Um médico possui `hour_rate` igual a zero.

**Status:** Permitido pela modelagem (CheckConstraint: `hour_rate >= 0`).

**Decisão:** O Coverage Engine registra `warning=zero_hour_rate` mas processa normalmente. O Payroll (Sprint 8) decidirá como tratar.

---

### IC-12: Extra approved para período não fechado

**Cenário:** Um Extra é aprovado enquanto a competência ainda está em `draft`.

**Status:** Válido.

**Decisão:** O Coverage Engine processa normalmente quando a competência for fechada. O Extra é incluído na consolidação.

---

### IC-13: Reabertura + Consolidação anterior

**Cenário:** Uma competência é reaberta após ter sido fechada e consolidada.

**Status:** Válido (processo esperado).

**Decisão:** O Coverage Engine invalida todos os snapshots anteriores e re-executa a consolidação completa.

---

## Resumo

| ID | Inconsistência | Severidade | Tratamento |
|---|---|---|---|
| IC-01 | Assignment cancelado + Extra aprovado | Info | Processa normalmente |
| IC-02 | Extra sem Assignment | Warning | Marca para revisão |
| IC-03 | Extra após fechamento | Error | Exclui da consolidação |
| IC-04 | Médico inativo + Assignment | Error | Não gera direito |
| IC-05 | Assignment completed + Shift cancelled | Error | Não gera direito |
| IC-06 | Assignments sobrepostos | Warning | Apenas um gera direito |
| IC-07 | Extra sem justificativa | Fatal | Impedido pelo model |
| IC-08 | Extra duração <= 0 | Fatal | Impedido pelo model |
| IC-09 | Assignment incompleto no fechamento | Warning | Não gera direito |
| IC-10 | Modificação após pagamento | Fatal | Impedido pelo sistema |
| IC-11 | Doctor hour_rate = 0 | Warning | Processa, Payroll decide |
| IC-12 | Extra approved antes do fechamento | Info | Processa no fechamento |
| IC-13 | Reabertura após consolidação | Info | Re-executa consolidação |
