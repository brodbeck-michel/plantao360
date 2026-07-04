# ADR-015: Assignment (ShiftPart) Domain Design

**Date:** Sprint 5
**Status:** Accepted
**Deciders:** Architecture Team

## Context

The `shift_parts` table existed as a simple junction table between Shift and Doctor. Sprint 5 transformed it into a rich domain entity representing **Doctor Assignment** — the core operational concept for allocating doctors to shifts.

## Decision

### Why ShiftPart represents Assignment

1. **Preserves DB schema** — no migration needed, avoids breakage
2. **Naming consistency** — existing code and tests remain valid
3. **Domain enrichment** — added `status` and `duration_minutes` fields
4. **Lifecycle management** — planned→confirmed→started→completed→cancelled

### Assignment Responsibilities

| Responsibility | Owner | Justification |
|---------------|-------|---------------|
| Time tracking | Assignment | Its core data |
| Status transitions | AssignmentStateMachine | Lifecycle management |
| Business rules | AssignmentRules | Validation logic |
| Duration calculation | Assignment | Computed on completion |
| Overlap detection | OverlapDetector | Cross-aggregate concern |
| Coverage validation | CoveragePolicy | Shift-level concern |

### Shift Responsibilities

| Responsibility | Owner | Justification |
|---------------|-------|---------------|
| Date/type management | Shift | Core attributes |
| Total duration | Shift | Aggregates from Assignments |
| Doctor count | Shift | Counts Assignments |
| Status transitions | ShiftStateMachine | Shift lifecycle |

### CoveragePolicy Design

- **Standalone class** — single responsibility, independently testable
- **Read-only** — answers questions, never mutates state
- **Injectable** — receives counts, makes decisions
- **Testable** — no database, no HTTP, pure logic

### OverlapDetector Design

- **Foundation only** — algorithm deferred to Sprint 6
- **Contract-based** — `OverlapCheckRequest` / `OverlapResult`
- **Repository-injected** — optional dependency, works without DB
- **Non-blocking** — detects but doesn't prevent (for now)

## Deferred Decisions

| Decision | Sprint | Reason |
|----------|--------|--------|
| Overlap algorithm | 6 | Complex time matching |
| Automatic distribution | 7 | Requires coverage optimization |
| Doctor replacement | 7 | Requires coverage validation |
| Payroll calculation | 8 | Financial domain |
| Primary/Backup Doctor | 7 | Role-based assignment |
| Justification tracking | 7 | Audit trail |

## Consequences

### Positive
- Rich domain entity ready for future features
- Clean separation of Assignment vs Shift responsibilities
- CoveragePolicy is independently testable
- OverlapDetector provides foundation for Sprint 6
- 7 domain events enable future integrations

### Negative
- Added `status` column to `shift_parts` table
- Added `duration_minutes` column (nullable)
- More complex than simple CRUD model
- State Machine adds indirection

### Risks
- Overlap algorithm not yet implemented (deferred)
- CoveragePolicy not yet integrated into Use Cases
- No database migration for new columns yet
