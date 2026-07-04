# Domain Coverage Matrix — Plantão 360

**Date:** 2026-06-26
**Sprint:** 5.2

---

## Module Coverage

| Module | Status | Sprint | Maturity | Notes |
|--------|--------|--------|----------|-------|
| Doctor | COMPLETE | 2.5 | HIGH | Golden Module |
| Period | COMPLETE | 3 | HIGH | Aggregate Root |
| Shift | COMPLETE | 4 | HIGH | Central Aggregate |
| Assignment | COMPLETE | 5 | HIGH | ShiftPart Domain |
| Shift Extras | PENDING | 6 | NONE | Extra shifts |
| Coverage | PENDING | 7 | FOUNDATION | Policy exists |
| Payroll | PENDING | 8 | NONE | Hours calculation |
| Import | PENDING | 9 | NONE | Tasy integration |
| Analytics | PENDING | 10 | NONE | Dashboards |
| Reports | FUTURE | - | NONE | PDF generation |
| Notifications | FUTURE | - | NONE | Alerts |
| Audit | FUTURE | - | NONE | Audit trail |
| Multi-Sector | FUTURE | - | NONE | Multiple sectors |

---

## Domain Component Coverage

### Aggregates

| Aggregate | Implemented | State Machine | Events | Tests |
|-----------|-------------|---------------|--------|-------|
| Doctor | ✓ | - | ✓ | ✓ |
| Period | ✓ | ✓ | ✓ | ✓ |
| Shift | ✓ | ✓ | ✓ | ✓ |
| Assignment | ✓ | ✓ | ✓ | ✓ |
| ShiftExtra | ✗ | - | - | - |

### Domain Core

| Component | Implemented | Tests |
|-----------|-------------|-------|
| AggregateRoot | ✓ | ✓ |
| EventCollector | ✓ | ✓ |
| BusinessCalendar | ✓ | ✓ |
| State Machines | ✓ | ✓ |
| Value Objects | ✓ | ✓ |
| Policies | ✓ | ✓ |
| Rules | ✓ | ✓ |
| Contracts | ✓ | ✓ |
| Overlap | FOUNDATION | ✓ |

### Infrastructure

| Component | Implemented | Tests |
|-----------|-------------|-------|
| Repository Pattern | ✓ | ✓ |
| Service Layer | ✓ | ✓ |
| DTOs | ✓ | ✓ |
| Validators | ✓ | ✓ |
| Mappers | ✓ | ✓ |
| API Routes | ✓ | ✓ |
| Error Codes | ✓ | ✓ |

---

## Test Coverage

| Module | Unit | Integration | Contracts | Total |
|--------|------|-------------|-----------|-------|
| Doctor | ✓ | ✓ | ✓ | HIGH |
| Period | ✓ | ✓ | ✓ | HIGH |
| Shift | ✓ | ✓ | ✓ | HIGH |
| Assignment | ✓ | ✓ | ✓ | HIGH |
| Domain Core | ✓ | - | ✓ | HIGH |

---

## Documentation Coverage

| Module | Manifest | ADR | Docs | Compliance |
|--------|----------|-----|------|------------|
| Doctor | ✓ | ✓ | ✓ | ✓ |
| Period | ✓ | ✓ | ✓ | ✓ |
| Shift | ✓ | ✓ | ✓ | ✓ |
| Assignment | ✓ | ✓ | ✓ | ✓ |

---

## Recommendations

1. **Sprint 6:** Implement Shift Extras module
2. **Sprint 7:** Implement Coverage algorithm
3. **Sprint 8:** Implement Payroll calculations
4. **Sprint 9:** Research Tasy integration
5. **Sprint 10:** Implement Analytics
