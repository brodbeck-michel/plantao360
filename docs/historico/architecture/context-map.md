# Context Map — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

O Context Map mostra todos os Bounded Contexts do Plantão 360 e seus relacionamentos.

---

## Bounded Contexts

### 1. Doctor Context
**Responsabilidade:** Gestão de médicos

**Componentes:**
- Aggregate: `Doctor`
- Value Objects: `DoctorStatus`, `DoctorSpecialty`
- Events: `DoctorCreatedEvent`, `DoctorUpdatedEvent`, `DoctorDeactivatedEvent`
- State Machine: `DoctorStateMachine`
- Query: `DoctorQuery`
- Read Model: `DoctorSummary`
- Projection: `DoctorProjection`

---

### 2. Period Context
**Responsabilidade:** Gestão de períodos de referência

**Componentes:**
- Aggregate: `Period`
- Value Objects: `PeriodStatus`, `PeriodType`
- Events: `PeriodCreatedEvent`, `PeriodClosedEvent`, `PeriodReopenedEvent`
- State Machine: `PeriodStateMachine`
- Query: `PeriodQuery`
- Read Model: `PeriodSummary`
- Projection: `PeriodProjection`

---

### 3. Shift Context
**Responsabilidade:** Gestão de plantões

**Componentes:**
- Aggregate: `Shift`
- Value Objects: `ShiftType`, `ShiftStatus`
- Events: `ShiftCreatedEvent`, `ShiftAssignedEvent`, `ShiftCompletedEvent`
- State Machine: `ShiftStateMachine`
- Rules: `ShiftRules`
- Query: `ShiftQuery`
- Read Model: `ShiftSummary`
- Projection: `ShiftProjection`

---

### 4. Assignment Context
**Responsabilidade:** Atribuição de médicos a plantões

**Componentes:**
- Aggregate: `Assignment`
- Value Objects: `AssignmentStatus`, `AssignmentType`
- Events: `AssignmentCreatedEvent`, `AssignmentConfirmedEvent`, `AssignmentCancelledEvent`
- State Machine: `AssignmentStateMachine`
- Rules: `AssignmentRules`
- Query: `AssignmentQuery`
- Read Model: `AssignmentSummary`
- Projection: `AssignmentProjection`

---

### 5. Coverage Context
**Responsabilidade:** Cobertura de plantões

**Componentes:**
- Value Objects: `CoverageStatus`, `CoverageType`
- Events: `CoverageRequestedEvent`, `CoverageApprovedEvent`, `CoverageRejectedEvent`
- State Machine: `CoverageStateMachine`
- Policy: `CoveragePolicy`
- Query: `CoverageQuery`
- Read Model: `CoverageSummary`

---

### 6. Financial Context
**Responsabilidade:** Aspectos financeiros

**Componentes:**
- Value Objects: `FinancialStatus`, `FinancialType`
- Events: `FinancialCalculatedEvent`, `FinancialApprovedEvent`
- Query: `FinancialQuery`
- Read Model: `FinancialSummary`
- KPI: `FinancialKPI`

---

### 7. Payroll Context
**Responsabilidade:** Gestão de folha de pagamento

**Componentes:**
- Aggregate: `PayrollCompetency`
- Value Objects: `PayrollStatus`, `PayrollAuditSnapshot`, `ApprovalChecklist`, `AdministrativeApproval`, `AdministrativeLock`, `ApprovalSnapshot`, `PayrollReadiness`
- Events: 12 payroll events
- State Machine: `PayrollStateMachine`
- Query: `PayrollQuery`
- Read Model: `PayrollSummary`
- KPI: `PayrollKPI`

---

### 8. Analytics Context
**Responsabilidade:** Análises e relatórios

**Componentes:**
- Explainability: `DomainExplanation`, `AuditAnalytics`, `InstitutionTimeline`, `ReportDefinitions`
- KPIs: `CoverageKPI`, `FinancialKPI`, `PayrollKPI`, `OperationalKPI`

---

## Relacionamentos

```
Doctor ──────┐
             │
Period ──────┼─── Shift ─────── Assignment
             │
Coverage ────┘
     │
     │
Financial ────────────── Payroll
     │
     │
Analytics ────────────── KPIs
```

### Tipo de Relacionamento

| De | Para | Tipo | Descrição |
|---|---|---|---|
| Doctor | Shift | Conforme | Médicos são atribuídos a plantões |
| Period | Shift | Conforme | Plantões pertencem a períodos |
| Shift | Assignment | Conforme | Plantões recebem atribuições |
| Coverage | Shift | Conforme | Coberturas cobrem plantões |
| Financial | Assignment | Conforme | Assignments geram dados financeiros |
| Payroll | Financial | Conforme | Payroll consolida dados financeiros |
| Analytics | Todos | Conforme | Analytics consolida dados de todos contextos |

---

## Bordas do Contexto

### Doctor Context
- **Inside:** Doctor, DoctorStatus, DoctorSpecialty
- **Outside:** Period, Shift, Assignment

### Period Context
- **Inside:** Period, PeriodStatus, PeriodType
- **Outside:** Doctor, Shift

### Shift Context
- **Inside:** Shift, ShiftType, ShiftStatus
- **Outside:** Doctor, Period, Assignment, Coverage

### Assignment Context
- **Inside:** Assignment, AssignmentStatus, AssignmentType
- **Outside:** Doctor, Shift, Financial

### Coverage Context
- **Inside:** CoverageStatus, CoverageType
- **Outside:** Shift

### Financial Context
- **Inside:** FinancialStatus, FinancialType
- **Outside:** Assignment, Payroll

### Payroll Context
- **Inside:** PayrollCompetency, PayrollStatus, Governance
- **Outside:** Financial

### Analytics Context
- **Inside:** DomainExplanation, AuditAnalytics, KPIs
- **Outside:** Todos os contextos

---

## Fluxos Principais

### 1. Fluxo de Atribuição
```
Doctor → Shift → Assignment → Financial
```

### 2. Fluxo de Cobertura
```
Shift → Coverage → Assignment
```

### 3. Fluxo de Payroll
```
Assignment → Financial → Payroll
```

### 4. Fluxo de Analytics
```
Todos os contextos → Analytics → KPIs
```

---

## Validação

| Critério | Status |
|---|---|
| Todos os Bounded Contexts mapeados | ✅ |
| Todos os relacionamentos documentados | ✅ |
| Bordas do contexto definidas | ✅ |
| Fluxos principais documentados | ✅ |
