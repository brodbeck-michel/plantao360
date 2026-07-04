# Golden Module Lock

**Date:** 2026-06-25

**Status:** LOCKED

---

## Declaration

The **Doctor** module is officially the **Golden Module** of Plantão 360.

This module serves as the **reference implementation** for all future modules.

## Locked Components

| Component | File | Status |
|-----------|------|--------|
| Model | `app/models/doctor.py` | LOCKED |
| Repository Interface | `app/repositories/interfaces/doctor_repository.py` | LOCKED |
| Repository | `app/repositories/doctor_repository.py` | LOCKED |
| Service | `app/services/doctor_service.py` | LOCKED |
| Mapper | `app/mappers/doctor_mapper.py` | LOCKED |
| Validator | `app/validators/doctor_validator.py` | LOCKED |
| DTOs (7) | `app/schemas/doctor/` | LOCKED |
| Error Codes | `app/domain/errors/doctor_errors.py` | LOCKED |
| Router | `app/api/routes/doctors.py` | LOCKED |
| Events | `app/domain/events/event_names.py` | LOCKED |
| Tests | `app/tests/` | LOCKED |
| Documentation | `docs/modules/doctor-module.md` | LOCKED |

## Modification Rules

Any architectural change to the Golden Module MUST:

1. **Create an ADR** — Document the decision
2. **Pass review** — Architecture team approval required
3. **Update templates** — All templates must reflect the change
4. **Update generator** — Module generator must be updated
5. **Update documentation** — All docs must be updated
6. **Never change only one module** — Changes must propagate to all modules

## Propagation Process

```
Change Request
    ↓
ADR Created
    ↓
Review Approved
    ↓
Golden Module Updated
    ↓
Templates Updated
    ↓
Generator Updated
    ↓
Documentation Updated
    ↓
All Existing Modules Updated
```

## Golden Module Patterns (Mandatory)

Every future module MUST implement:

1. **Repository Interface** — Protocol-based dependency injection
2. **7 DTOs** — Create, Update, Response, Summary, Detail, Filters, Query
3. **BaseMapper** — 3 generics (Model, CreateDTO, ResponseDTO)
4. **Validation Rules** — Individual rule functions
5. **Error Codes** — StrEnum per module
6. **Event Versioning** — `.v1` suffix on all events
7. **AuditContext** — Audit trail support
8. **Pagination Headers** — X-Total-Count, X-Page, X-Page-Size, X-Total-Pages
9. **Contract Tests** — API and pattern contracts
10. **Documentation** — Module docs with Mermaid diagrams

## Template Files

Templates are located at:

```
backend/templates/golden-module/
├── models/model.py.j2
├── repositories/
│   ├── interfaces/repository_interface.py.j2
│   └── repository.py.j2
├── services/service.py.j2
├── mappers/mapper.py.j2
├── validators/
│   ├── validator.py.j2
│   └── rules/unique_field.py.j2
├── schemas/
│   ├── create.py.j2
│   ├── update.py.j2
│   ├── response.py.j2
│   ├── summary.py.j2
│   ├── filters.py.j2
│   ├── query.py.j2
│   └── __init__.py.j2
├── routes/router.py.j2
├── domain/errors/error_codes.py.j2
└── tests/
    ├── unit/test_model.py.j2
    ├── unit/test_repository.py.j2
    ├── unit/test_service.py.j2
    ├── unit/test_mapper.py.j2
    ├── unit/test_validator.py.j2
    ├── integration/test_api.py.j2
    └── contracts/test_contracts.py.j2
```

## Verification

Use the architecture validator to ensure compliance:

```bash
python tools/validate_architecture.py Doctor
python tools/lint_architecture.py --module Doctor
```
