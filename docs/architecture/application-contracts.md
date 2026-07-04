# Application Contracts — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

Application Contracts definem os contratos entre a camada de Application e a camada de Domain. Estes contratos são usados pelo Frontend e por sistemas externos.

---

## Contratos de Comando

### 1. Doctor Commands

```python
class CreateDoctorCommand:
    name: str
    specialty: str
    crm: str
    email: str

class UpdateDoctorCommand:
    doctor_id: str
    name: Optional[str]
    specialty: Optional[str]
    email: Optional[str]

class DeactivateDoctorCommand:
    doctor_id: str
    reason: str
```

---

### 2. Period Commands

```python
class CreatePeriodCommand:
    name: str
    start_date: date
    end_date: date
    period_type: str

class ClosePeriodCommand:
    period_id: str

class ReopenPeriodCommand:
    period_id: str
    reason: str
```

---

### 3. Shift Commands

```python
class CreateShiftCommand:
    period_id: str
    doctor_id: str
    shift_date: date
    shift_type: str
    start_time: time
    end_time: time

class UpdateShiftCommand:
    shift_id: str
    shift_date: Optional[date]
    shift_type: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]

class CancelShiftCommand:
    shift_id: str
    reason: str
```

---

### 4. Assignment Commands

```python
class CreateAssignmentCommand:
    shift_id: str
    doctor_id: str
    assignment_type: str

class UpdateAssignmentCommand:
    assignment_id: str
    assignment_type: Optional[str]

class CancelAssignmentCommand:
    assignment_id: str
    reason: str
```

---

### 5. Coverage Commands

```python
class RequestCoverageCommand:
    shift_id: str
    coverage_type: str
    reason: str

class ApproveCoverageCommand:
    coverage_id: str
    approved_by: str

class RejectCoverageCommand:
    coverage_id: str
    rejected_by: str
    reason: str
```

---

### 6. Payroll Commands

```python
class CreatePayrollCommand:
    competency: str
    period_id: str

class ApprovePayrollCommand:
    payroll_id: str
    approved_by: str
    checklist: ApprovalChecklist

class RejectPayrollCommand:
    payroll_id: str
    rejected_by: str
    reason: str

class ProcessPayrollCommand:
    payroll_id: str

class CompletePayrollCommand:
    payroll_id: str

class LockPayrollCommand:
    payroll_id: str
    locked_by: str
```

---

## Contratos de Query

### 1. Doctor Queries

```python
class DoctorQuery:
    doctor_id: Optional[str]
    name: Optional[str]
    specialty: Optional[str]
    status: Optional[str]
    page: int = 1
    page_size: int = 20
```

---

### 2. Period Queries

```python
class PeriodQuery:
    period_id: Optional[str]
    name: Optional[str]
    period_type: Optional[str]
    status: Optional[str]
    page: int = 1
    page_size: int = 20
```

---

### 3. Shift Queries

```python
class ShiftQuery:
    shift_id: Optional[str]
    period_id: Optional[str]
    doctor_id: Optional[str]
    shift_date: Optional[date]
    shift_type: Optional[str]
    status: Optional[str]
    page: int = 1
    page_size: int = 20
```

---

### 4. Assignment Queries

```python
class AssignmentQuery:
    assignment_id: Optional[str]
    shift_id: Optional[str]
    doctor_id: Optional[str]
    assignment_type: Optional[str]
    status: Optional[str]
    page: int = 1
    page_size: int = 20
```

---

### 5. Coverage Queries

```python
class CoverageQuery:
    coverage_id: Optional[str]
    shift_id: Optional[str]
    coverage_type: Optional[str]
    status: Optional[str]
    page: int = 1
    page_size: int = 20
```

---

### 6. Financial Queries

```python
class FinancialQuery:
    period_id: Optional[str]
    doctor_id: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    page: int = 1
    page_size: int = 20
```

---

### 7. Payroll Queries

```python
class PayrollQuery:
    payroll_id: Optional[str]
    competency: Optional[str]
    period_id: Optional[str]
    status: Optional[str]
    page: int = 1
    page_size: int = 20
```

---

## Contratos de Read Model

### 1. DoctorSummary

```python
class DoctorSummary:
    doctor_id: str
    name: str
    specialty: str
    crm: str
    email: str
    status: str
    total_shifts: int
    total_assignments: int
    total_hours: float
```

---

### 2. PeriodSummary

```python
class PeriodSummary:
    period_id: str
    name: str
    start_date: date
    end_date: date
    period_type: str
    status: str
    total_shifts: int
    total_doctors: int
    total_hours: float
```

---

### 3. ShiftSummary

```python
class ShiftSummary:
    shift_id: str
    period_id: str
    doctor_id: str
    doctor_name: str
    shift_date: date
    shift_type: str
    start_time: time
    end_time: time
    status: str
    coverage_status: Optional[str]
```

---

### 4. AssignmentSummary

```python
class AssignmentSummary:
    assignment_id: str
    shift_id: str
    doctor_id: str
    doctor_name: str
    assignment_type: str
    status: str
    created_at: datetime
    updated_at: datetime
```

---

### 5. CoverageSummary

```python
class CoverageSummary:
    coverage_id: str
    shift_id: str
    coverage_type: str
    status: str
    requested_at: datetime
    resolved_at: Optional[datetime]
    resolved_by: Optional[str]
```

---

### 6. FinancialSummary

```python
class FinancialSummary:
    period_id: str
    doctor_id: str
    doctor_name: str
    total_shifts: int
    total_hours: float
    total_extras: int
    total_amount: float
    status: str
```

---

### 7. PayrollSummary

```python
class PayrollSummary:
    payroll_id: str
    competency: str
    period_id: str
    status: str
    total_doctors: int
    total_amount: float
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime]
    completed_at: Optional[datetime]
```

---

## Validação

| Critério | Status |
|---|---|
| Todos os comandos documentados | ✅ |
| Todas as queries documentadas | ✅ |
| Todos os read models documentados | ✅ |
| Contratos são imutáveis | ✅ |
| Contratos são usados pelo Frontend | ✅ |
