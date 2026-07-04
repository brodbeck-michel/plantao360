# Domain Phase — Plantão 360

**Date:** 2026-06-26
**Sprint:** 5.2
**Status:** ACTIVE

---

## Declaration

As of Sprint 5.2, Plantão 360 officially enters the Domain Phase.

All subsequent sprints will focus exclusively on business rules, operational logic, and hospital domain modeling.

---

## Phase Transition

| Aspect | Engineering Phase | Domain Phase |
|--------|-------------------|--------------|
| Focus | Infrastructure, patterns | Business rules, operations |
| Changes | Structural | Behavioral |
| ADR Required | For infrastructure | For structural only |
| Testing | Unit, integration | Business scenarios |
| Documentation | Architecture | Domain rules |

---

## Domain Phase Process

Every future sprint MUST begin with:

### 1. Business Rule Review

- What hospital rules apply?
- What are the invariants?
- What are the edge cases?

### 2. Domain Event Identification

- What events occur in the hospital?
- What triggers them?
- What are the side effects?

### 3. Impact Analysis

- Operational impact?
- Financial impact?
- Audit impact?
- Compliance impact?

### 4. Implementation

- Only after steps 1-3 are complete
- Follow existing patterns
- Maintain quality gates

---

## Domain Modules

### Next Sprints (Priority Order)

| Sprint | Module | Focus |
|--------|--------|-------|
| 6 | Shift Extras | Extra shifts, justifications, approval |
| 7 | Coverage | Minimum coverage, alerts, replacement |
| 8 | Payroll | Hours calculation, payments, reports |
| 9 | Import | Tasy integration, data import |
| 10 | Analytics | Dashboards, reports, metrics |

### Future Modules

| Module | Description |
|--------|-------------|
| Reports | PDF generation, exports |
| Notifications | Alerts, reminders |
| Audit | Complete audit trail |
| Multi-Sector | Multiple sectors support |

---

## Domain Rules Framework

### Rule Categories

1. **Operational Rules** — How shifts work
2. **Financial Rules** — How payments are calculated
3. **Compliance Rules** — Regulatory requirements
4. **Business Rules** — Hospital-specific logic

### Rule Documentation

Each rule must be documented with:

- Name and description
- Invariants
- Edge cases
- Test cases
- Impact analysis

---

## Success Criteria

The Domain Phase is successful when:

- All hospital rules are implemented
- All edge cases are handled
- All financial calculations are accurate
- All audit requirements are met
- All compliance rules are satisfied
- System is ready for production use
