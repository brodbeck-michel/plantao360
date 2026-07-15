# Domain Model Readiness

Documento de preparação para modelagem futura do banco de dados.

## ShiftType

**Origem:** `domain/constants/shift_types.py`

**Destino futuro:**
- `models/shifts.py` — Coluna `shift_type` com valores T1, T2, T3, R1, R2
- `schemas/shifts.py` — Campo `shift_type` com validação StrEnum
- `services/shifts.py` — Lógica de criação e validação

## PeriodStatus

**Origem:** `domain/constants/period_status.py`

**Destino futuro:**
- `models/periods.py` — Coluna `status` com valores draft, closed, paid
- `schemas/periods.py` — Campo `status` com validação StrEnum
- `services/periods.py` — Transições de estado (draft → closed → paid)

## BusinessRuleCode

**Origem:** `domain/rules/business_rules.py`

**Destino futuro:**
- `domain/exceptions/errors.py` — Exceções com código de regra
- `services/` — Validação de regras de negócio
- `api/routes/` — Tratamento de erros com código

## DomainEventName

**Origem:** `domain/events/event_names.py`

**Destino futuro:**
- `common/events.py` — DomainEvent com event_name do catálogo
- `audit/` — Eventos de auditoria alinhados
- `observability/` — Métricas de eventos

## AuditAction

**Origem:** `audit/events.py`

**Destino futuro:**
- `audit/models.py` — Campo `action` com valores do enum
- `services/` — Registro de ações de auditoria
