# ShiftPart (Doctor Assignment) — Critical Review v1

**Date:** Sprint 5
**Author:** Architecture Team

---

## 1. ShiftPart representa corretamente uma alocação?

**Resposta: Parcialmente.**

O modelo atual é uma tabela de junção enriquecida:
- `id`, `shift_id`, `doctor_id`, `start_time`, `end_time`

Uma alocação de médico (Doctor Assignment) requer:
- ✅ Identidade (`id`)
- ✅ Referência ao Shift (`shift_id`)
- ✅ Referência ao Doctor (`doctor_id`)
- ✅ Horário de início/fim (`start_time`, `end_time`)
- ❌ Status da alocação (planned, confirmed, started, completed, cancelled)
- ❌ Papel do médico (primary, backup)
- ❌ Duração calculada (para remuneração)
- ❌ Justificativa (para cancelamentos e substituições)
- ❌ Referência a quem confirmou (audit trail)

**Veredicto:** O modelo é um esqueleto de persistência. Deve ser enriquecido.

---

## 2. Existem atributos faltantes para suportar remuneração?

**Sim, criticamente:**

| Atributo | Necessidade | Status |
|----------|-------------|--------|
| Duração em minutos | Cálculo de valor | ❌ Ausente |
| Tipo de hora (normal, adicional) | Classificação | ❌ Ausente |
| Taxa aplicada (doctor.hour_rate) | Cálculo de valor | ✅ Via Doctor |
| Data de referência | Período de pagamento | ✅ Via Shift.shift_date |

**Decisão:** A duração será calculada a partir de `start_time` e `end_time`. O tipo de hora e a taxa pertencem ao módulo Payroll.

---

## 3. Existem atributos faltantes para substituições futuras?

**Sim:**

| Atributo | Necessidade | Status |
|----------|-------------|--------|
| Original doctor_id | Rastrear substituição | ❌ Ausente |
| Motivo da substituição | Auditoria | ❌ Ausente |
| Data/hora da substituição | Auditoria | ❌ Ausente |
| Quem autorizou | Audit trail | ❌ Ausente |

**Decisão:** Esses atributos serão adiados para o Sprint de Substituições. A estrutura atual suporta a adição posterior.

---

## 4. Existem regras de sobreposição não documentadas?

**Sim, crítico:**

1. Um médico não pode ter dois ShiftParts simultâneos no mesmo período
2. Um médico não pode ter ShiftParts com sobreposição de horário
3. Um médico não pode ser asignado a um Shift que conflite com outro
4. A remoção de um médico pode deixar o Shift sem cobertura mínima

**Decisão:** O Algoritmo de detecção de sobreposição será implementado no Sprint 6. A sprint atual cria os contratos e a foundation.

---

## 5. Existem responsabilidades que pertencem ao Shift e não ao ShiftPart?

**Sim:**

| Responsabilidade | Pertence a | Justificativa |
|-----------------|------------|---------------|
| Duração total do Shift | Shift | Agrega todas as partes |
| Contagem de médicos | Shift | Conta ShiftParts |
| Validação de cobertura mínima | Shift | Regra do Shift |
| Transição de status do Shift | Shift | Lifecycle do Shift |

**Decisão:** ShiftPart é uma entidade filha que consulta Shift para validações de cobertura. ShiftPart não altera estado do Shift.

---

## 6. Quais decisões devem ser adiadas?

| Decisão | Motivo | Sprint |
|---------|--------|--------|
| Algoritmo de detecção de sobreposição | Complexidade algorítmica | Sprint 6 |
| Substituição automática | Requer validação de cobertura | Sprint 7 |
| Cálculo financeiro | Pertence ao Payroll | Sprint 8 |
| Otimização de cobertura | Requer IA/ML | Sprint 9 |
| Múltiplos setores | Arquitetura de dados | Sprint 10 |
| Tipo de hora (normal/adicional) | Payroll domain | Sprint 8 |
| Justificativa de cancelamento | Auditoria simples | Sprint 7 |
| Audit trail de confirmação | Auditoria completa | Sprint 7 |

---

## Plano de Implementação

1. Enriquecer modelo ShiftPart com status
2. Criar AssignmentStatus (planned→confirmed→started→completed→cancelled)
3. Criar AssignmentStateMachine
4. Criar Value Objects (AssignmentTimeline, AssignmentDuration, DoctorReference, ShiftReference)
5. Criar AssignmentRules
6. Criar Overlap Foundation (contratos)
7. Criar CoveragePolicy
8. Criar Use Cases (9)
9. Criar Eventos (7)
10. Documentar
11. Testar
