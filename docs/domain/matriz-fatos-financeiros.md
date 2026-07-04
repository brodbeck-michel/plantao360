# Matriz de Fatos Financeiros

**Sprint:** 7
**Data:** 2026-06-26

---

## Definição

Cada linha representa um evento de domínio existente. Para cada evento, documenta-se:
- **Gera remuneração?** → Cria direito financeiro
- **Gera auditoria?** → Registro de rastreabilidade
- **Gera relatório?** → Dados para relatórios
- **Pode ser revertido?** → Permite cancelamento/estorno
- **Altera fechamento?** → Afeta consolidação da competência

---

## Eventos de Domínio

### Doctor Events

| Evento | Gera Remuneração? | Gera Auditoria? | Gera Relatório? | Pode ser Revertido? | Altera Fechamento? |
|---|---|---|---|---|---|
| `doctor.created.v1` | Não | Sim | Sim | Não | Não |
| `doctor.updated.v1` | Não | Sim | Sim | Não | Não |
| `doctor.deactivated.v1` | Não | Sim | Sim | Não | Não |

**Justificativa:** Doctor é entidade de referência. Não gera fatos financeiros diretamente.

---

### Period Events

| Evento | Gera Remuneração? | Gera Auditoria? | Gera Relatório? | Pode ser Revertido? | Altera Fechamento? |
|---|---|---|---|---|---|
| `period.created.v1` | Não | Sim | Sim | Não | Não |
| `period.updated.v1` | Não | Sim | Sim | Não | Não |
| `period.closed.v1` | **Sim** (dispara consolidação) | Sim | Sim | Sim (reabertura) | **Sim** |
| `period.reopened.v1` | **Sim** (invalida snapshots) | Sim | Sim | Não | **Sim** |

**Justificativa:** Fechamento dispara Coverage Engine. Reabertura invalida snapshots.

---

### Shift Events

| Evento | Gera Remuneração? | Gera Auditoria? | Gera Relatório? | Pode ser Revertido? | Altera Fechamento? |
|---|---|---|---|---|---|
| `shift.created.v1` | Não | Sim | Sim | Sim (delete) | Não |
| `shift.updated.v1` | Não | Sim | Sim | Não | Não |
| `shift.started.v1` | Não | Sim | Sim | Não | Não |
| `shift.completed.v1` | Não | Sim | Sim | Não | Não |
| `shift.cancelled.v1` | **Indireto** (afeta assignments) | Sim | Sim | Não | **Sim** |

**Justificativa:** Shift cancelado revoga elegibilidade dos Assignments associados.

---

### Assignment Events

| Evento | Gera Remuneração? | Gera Auditoria? | Gera Relatório? | Pode ser Revertido? | Altera Fechamento? |
|---|---|---|---|---|---|
| `assignment.created.v1` | Não | Sim | Sim | Sim (cancel/remove) | Não |
| `assignment.updated.v1` | Não | Sim | Sim | Não | Não |
| `assignment.confirmed.v1` | Não | Sim | Sim | Sim (cancel) | Não |
| `assignment.started.v1` | Não | Sim | Sim | Não | Não |
| `assignment.completed.v1` | **Sim** | Sim | Sim | Sim (cancel retroativo) | **Sim** |
| `assignment.cancelled.v1` | **Revoga** direito anterior | Sim | Sim | Não | **Sim** |
| `assignment.removed.v1` | Não (nunca completou) | Sim | Sim | Não | Não |

**Justificativa:** Apenas `completed` gera direito. Cancelamento revoga retroativamente.

---

### Extra Events

| Evento | Gera Remuneração? | Gera Auditoria? | Gera Relatório? | Pode ser Revertido? | Altera Fechamento? |
|---|---|---|---|---|---|
| `extra.created.v1` | Não | Sim | Sim | Sim (cancel/delete) | Não |
| `extra.deleted.v1` | Não (era pending) | Sim | Sim | Não | Não |
| `extra.approved.v1` | **Sim** | Sim | Sim | Sim (cancel retroativo) | **Sim** |
| `extra.rejected.v1` | Nunca (rejeitado) | Sim | Sim | Não | Não |
| `extra.cancelled.v1` | **Revoga** direito anterior | Sim | Sim | Não | **Sim** |

**Justificativa:** Apenas `approved` gera direito. Rejeição e cancelamento revogam.

---

### Financial Events (Sprint 7)

| Evento | Gera Remuneração? | Gera Auditoria? | Gera Relatório? | Pode ser Revertido? | Altera Fechamento? |
|---|---|---|---|---|---|
| `coverage.consolidated.v1` | **Sim** (consolidação) | Sim | Sim | Sim (reabertura) | **Sim** |
| `financial.snapshot.created.v1` | **Sim** (registro) | Sim | Sim | Sim (reabertura) | **Sim** |
| `financial.fact.generated.v1` | **Sim** (fato individual) | Sim | Sim | Sim (revogação) | **Sim** |
| `financial.fact.revoked.v1` | **Revoga** fato anterior | Sim | Sim | Não | **Sim** |

**Justificativa:** Estes eventos representam a consolidação financeira em si.

---

## Resumo

| Total de Eventos | Gera Remuneração | Gera Auditoria | Gera Relatório | Pode ser Revertido | Altera Fechamento |
|---|---|---|---|---|---|
| 27 (existentes) + 4 (novos) = 31 | 8 | 31 | 31 | 10 | 9 |

---

## Eventos que Geram Direito Financeiro

1. `assignment.completed.v1` → FatoFinanceiro tipo `assignment_completion`
2. `extra.approved.v1` → FatoFinanceiro tipo `extra_approved`
3. `coverage.consolidated.v1` → CoverageSnapshot
4. `financial.snapshot.created.v1` → FinancialSnapshot
5. `financial.fact.generated.v1` → FatoFinanceiro individual
6. `period.closed.v1` → Dispara consolidação
7. `assignment.cancelled.v1` → Revoga FatoFinanceiro
8. `extra.cancelled.v1` → Revoga FatoFinanceiro
