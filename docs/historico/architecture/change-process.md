# Architecture Decision Pipeline

**Date:** 2026-06-25

**Status:** Active

---

## Overview

All architectural decisions in Plantão 360 must follow a mandatory pipeline.

## Decision Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE DECISION PIPELINE            │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  1. CHANGE   │  Someone identifies a need for change
    │   REQUEST    │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  2. ADR      │  Document the decision
    │   CREATED    │  python tools/adr_generator.py "Title"
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  3. REVIEW   │  Architecture team reviews
    │              │  Approval required
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  4. GOLDEN   │  Update Golden Module
    │   MODULE     │  Implement changes
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  5. GENERATOR│  Update module generator
    │              │  Update templates
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  6. TEMPLATES│  Update all templates
    │              │  Ensure consistency
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  7. ALL      │  Update all existing modules
    │   MODULES    │  Propagate changes
    └──────────────┘
```

## Step-by-Step Process

### Step 1: Change Request

- Identify the need for change
- Document the problem
- Assess impact

### Step 2: ADR Creation

```bash
python tools/adr_generator.py "Title of Decision"
```

ADR must include:
- Context
- Decision
- Rationale
- Consequences
- Alternatives considered

### Step 3: Review

- Architecture team reviews ADR
- Discuss alternatives
- Make final decision
- Update ADR status (accepted/rejected)

### Step 4: Golden Module Update

- Implement change in Doctor module
- Ensure all tests pass
- Update documentation

### Step 5: Generator Update

- Update `tools/module_generator.py`
- Update templates in `backend/templates/golden-module/`
- Test generator with new module

### Step 6: Template Update

- Update all affected templates
- Ensure consistency across templates
- Update `config.json`

### Step 7: Module Propagation

- Update all existing modules
- Run architecture validator
- Run linter
- Ensure all tests pass

## Rules

1. **Never skip steps** — All steps are mandatory
2. **Document everything** — ADRs are required
3. **No silent changes** — All changes must be reviewed
4. **Test before merge** — All validations must pass
5. **Propagate changes** — All modules must be updated

## Exceptions

Emergency fixes may bypass the pipeline but must:
- Be documented within 24 hours
- Create a retroactive ADR
- Be reviewed within 1 week

## Tools

| Tool | Purpose |
|------|---------|
| `adr_generator.py` | Create ADRs |
| `validate_architecture.py` | Validate modules |
| `lint_architecture.py` | Check violations |
| `module_generator.py` | Generate modules |
| `compliance_report.py` | Check compliance |
