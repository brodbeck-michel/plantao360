# Developer Onboarding Guide

**Date:** 2026-06-25

**Status:** Active

---

## Welcome to Plantão 360

This guide will help you get started with the Plantão 360 project.

## Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git
- Node.js 18+ (for frontend)

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Plantoes\ PS\ Unimed
```

## Step 2: Start Docker

```bash
cd plantao360
docker compose up -d
```

## Step 3: Run Tests

```bash
cd backend
python -m pytest app/tests/ -v --tb=short
```

## Step 4: Generate a Module

```bash
python tools/module_generator.py MyModule \
  --table my_modules \
  --route /my-modules \
  --unique-field code \
  --unique-field-label "Codigo"
```

## Step 5: Register the Router

Edit `app/api/app.py`:

```python
from app.api.routes import my_module
application.include_router(my_module.router, prefix="/api/v1")
```

## Step 6: Add Event Names

Edit `app/domain/events/event_names.py`:

```python
MY_MODULE_CREATED_V1 = "my_module.created.v1"
MY_MODULE_UPDATED_V1 = "my_module.updated.v1"
MY_MODULE_DEACTIVATED_V1 = "my_module.deactivated.v1"
```

## Step 7: Run Validation

```bash
python tools/validate_architecture.py MyModule
python tools/lint_architecture.py --module MyModule
```

## Step 8: Run Tests

```bash
python -m pytest app/tests/unit/test_my_module_* -v
python tools/dev.py tests MyModule
```

## Development Workflow

### Creating a New Feature

1. Create a branch: `git checkout -b feature/my-feature`
2. Implement changes
3. Write tests
4. Run validation: `python tools/dev.py validate MyModule`
5. Run linter: `python tools/dev.py lint`
6. Create ADR (if architectural): `python tools/adr_generator.py "Title"`
7. Create PR

### Creating an ADR

```bash
python tools/adr_generator.py "Decision Title" --status proposed
```

### Generating Documentation

```bash
python tools/docs_generator.py MyModule
```

### Running Full Review

```bash
python tools/dev.py review
```

## Project Structure

```
plantao360/
├── backend/
│   ├── app/
│   │   ├── api/routes/          # API endpoints
│   │   ├── models/              # SQLAlchemy models
│   │   ├── repositories/        # Data access
│   │   ├── services/            # Business logic
│   │   ├── mappers/             # DTO mapping
│   │   ├── validators/          # Validation rules
│   │   ├── schemas/             # DTOs
│   │   ├── domain/              # Domain events, errors
│   │   ├── use_cases/           # Use cases
│   │   └── tests/               # Tests
│   ├── templates/golden-module/ # Module templates
│   └── tools/                   # Development tools
├── frontend/                    # React frontend
└── docs/                        # Documentation
```

## Golden Module Pattern

Every module MUST follow the Doctor module pattern:

1. Repository Interface (Protocol)
2. 7 DTOs (Create, Update, Response, Summary, Filters, Query)
3. BaseMapper (3 generics)
4. Validation Rules
5. Error Codes (StrEnum)
6. Event Versioning (.v1)
7. AuditContext
8. Pagination Headers
9. Contract Tests
10. Documentation

## Tools Reference

| Tool | Purpose |
|------|---------|
| `dev.py` | Developer CLI |
| `module_generator.py` | Generate modules |
| `validate_architecture.py` | Validate architecture |
| `lint_architecture.py` | Check violations |
| `docs_generator.py` | Generate docs |
| `adr_generator.py` | Create ADRs |
| `project_metrics.py` | Project metrics |
| `compliance_report.py` | Compliance report |

## Getting Help

- Read the documentation in `docs/`
- Check the Golden Module: `docs/modules/doctor-module.md`
- Review ADRs: `docs/adr/`
- Run `python tools/dev.py --help`
