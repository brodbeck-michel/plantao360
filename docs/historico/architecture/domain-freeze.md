# Domain Freeze — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27
**Status:** FROZEN
**Auditoria:** Aprovado (domain-freeze-review.md)

---

## Declaração

A partir da Sprint 10.5, o domínio de negócio do Plantão 360 está oficialmente congelado.

Qualquer alteração em componentes congelados requer **ADR (Architecture Decision Record)** e aprovação formal.

---

## Componentes Congelados

### 1. Aggregates

| Aggregate | Módulo | Status | Notas |
|---|---|---|---|
| `PayrollCompetency` | `payroll/` | FROZEN | Lifecycle completo com state machine |
| `Doctor` | `entities/` | FROZEN | Via SQLAlchemy |
| `Period` | `entities/` | FROZEN | Via SQLAlchemy |
| `Shift` | `entities/` | FROZEN | Via SQLAlchemy |
| `Assignment` | `entities/` | FROZEN | Via SQLAlchemy |
| `Extra` | `entities/` | FROZEN | Via SQLAlchemy |

**O que pode mudar:** Valores de configuration (ports, timeouts)
**O que não pode mudar:** Arquitetura, padrões, dependências

---

### 2. Value Objects

| Value Object | Módulo | Status |
|---|---|---|
| `PayrollStatus` | `payroll/` | FROZEN |
| `PayrollAuditSnapshot` | `payroll/` | FROZEN |
| `ApprovalChecklist` | `payroll/governance.py` | FROZEN |
| `AdministrativeApproval` | `payroll/governance.py` | FROZEN |
| `AdministrativeLock` | `payroll/governance.py` | FROZEN |
| `ApprovalSnapshot` | `payroll/governance.py` | FROZEN |
| `PayrollReadiness` | `payroll/` | FROZEN |
| `CoverageStatus` | `coverage/` | FROZEN |
| `CoverageSummary` | `read_models/coverage_summary.py` | FROZEN |
| `DoctorSummary` | `read_models/doctor_summary.py` | FROZEN |
| `PeriodSummary` | `read_models/period_summary.py` | FROZEN |
| `ShiftSummary` | `read_models/shift_summary.py` | FROZEN |
| `AssignmentSummary` | `read_models/assignment_summary.py` | FROZEN |
| `FinancialSummary` | `read_models/financial_summary.py` | FROZEN |
| `PayrollSummary` | `read_models/payroll_summary.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 3. Domain Events

| Event Category | Quantidade | Status |
|---|---|---|
| Payroll Events | 12 | FROZEN |
| Coverage Events | 8 | FROZEN |
| Assignment Events | 6 | FROZEN |
| Doctor Events | 4 | FROZEN |
| Period Events | 3 | FROZEN |
| Administrative Events | 2 | FROZEN |

**Total:** 35 eventos

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 4. State Machines

| State Machine | Status | Notas |
|---|---|---|
| `PayrollStateMachine` | FROZEN | 7 states: DRAFT, PENDING, APPROVED, REJECTED, PROCESSING, COMPLETED, LOCKED |
| `CoverageStateMachine` | FROZEN | 5 states |
| `AssignmentStateMachine` | FROZEN | 4 states |
| `PeriodStateMachine` | FROZEN | 3 states |
| `DoctorStateMachine` | FROZEN | 3 states |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 5. Rules & Policies

| Component | Módulo | Status |
|---|---|---|
| `ShiftRules` | `rules/shift_rules.py` | FROZEN |
| `AssignmentRules` | `rules/assignment_rules.py` | FROZEN |
| `BusinessRules` | `rules/business_rules.py` | FROZEN |
| `PeriodPolicy` | `policies/period_policy.py` | FROZEN |
| `CoveragePolicy` | `policies/coverage_policy.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 6. Read Models

| Read Model | Módulo | Status |
|---|---|---|
| `DoctorSummary` | `read_models/doctor_summary.py` | FROZEN |
| `PeriodSummary` | `read_models/period_summary.py` | FROZEN |
| `ShiftSummary` | `read_models/shift_summary.py` | FROZEN |
| `AssignmentSummary` | `read_models/assignment_summary.py` | FROZEN |
| `CoverageSummary` | `read_models/coverage_summary.py` | FROZEN |
| `FinancialSummary` | `read_models/financial_summary.py` | FROZEN |
| `PayrollSummary` | `read_models/payroll_summary.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 7. Query Domain

| Component | Módulo | Status |
|---|---|---|
| `DoctorQuery` | `query/doctor_query.py` | FROZEN |
| `PeriodQuery` | `query/period_query.py` | FROZEN |
| `ShiftQuery` | `query/shift_query.py` | FROZEN |
| `AssignmentQuery` | `query/assignment_query.py` | FROZEN |
| `CoverageQuery` | `query/coverage_query.py` | FROZEN |
| `FinancialQuery` | `query/financial_query.py` | FROZEN |
| `PayrollQuery` | `query/payroll_query.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 8. Explainability

| Component | Módulo | Status |
|---|---|---|
| `DomainExplanation` | `explainability/domain_explanation.py` | FROZEN |
| `AuditAnalytics` | `explainability/audit_analytics.py` | FROZEN |
| `InstitutionTimeline` | `explainability/institution_timeline.py` | FROZEN |
| `ReportDefinitions` | `explainability/report_definitions.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 9. KPIs

| KPI | Módulo | Status |
|---|---|---|
| `CoverageKPI` | `kpi/coverage_kpi.py` | FROZEN |
| `FinancialKPI` | `kpi/financial_kpi.py` | FROZEN |
| `PayrollKPI` | `kpi/payroll_kpi.py` | FROZEN |
| `OperationalKPI` | `kpi/operational_kpi.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

### 10. Projections

| Projection | Módulo | Status |
|---|---|---|
| `DoctorProjection` | `projections/doctor_projection.py` | FROZEN |
| `PeriodProjection` | `projections/period_projection.py` | FROZEN |
| `ShiftProjection` | `projections/shift_projection.py` | FROZEN |
| `AssignmentProjection` | `projections/assignment_projection.py` | FROZEN |

**O que pode mudar:** Nada sem ADR
**O que não pode mudar:** Tudo

---

## Resumo do Domain Freeze

| Categoria | Quantidade | Status |
|---|---|---|
| Aggregates | 6 | FROZEN |
| Value Objects | 15 | FROZEN |
| Domain Events | 35 | FROZEN |
| State Machines | 5 | FROZEN |
| Rules & Policies | 5 | FROZEN |
| Read Models | 7 | FROZEN |
| Query Domain | 7 | FROZEN |
| Explainability | 4 | FROZEN |
| KPIs | 4 | FROZEN |
| Projections | 4 | FROZEN |
| **Total** | **92** | **FROZEN** |

---

## Impacto da Mudança

| Tipo de Mudança | Requisito |
|---|---|
| Adicionar novo Aggregate | ADR + Aprovação |
| Modificar Aggregate existente | ADR + Aprovação |
| Adicionar novo Domain Event | ADR + Aprovação |
| Modificar State Machine | ADR + Aprovação |
| Adicionar nova Rule/Policy | ADR + Aprovação |
| Modificar Read Model | ADR + Aprovação |
| Modificar Query Domain | ADR + Aprovação |
| Adicionar novo KPI | ADR + Aprovação |

---

## Pergunta Fundamental

> **"Se daqui a cinco anos a instituição trocar o Tasy por outro ERP hospitalar, quantas linhas do domínio precisarão ser alteradas?"**

**Resposta:** Nenhuma.

O domínio é completamente independente de sistemas externos. Todas as integrações ocorrem através de contratos e adaptadores na camada de infraestrutura. O domínio jamais conhece sistemas externos.
