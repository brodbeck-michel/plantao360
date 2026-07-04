# ADR-014: Shift Aggregate Design

**Date:** Sprint 4
**Status:** Accepted
**Deciders:** Architecture Team

## Context

The Shift module is the central operational Aggregate of Plantão 360. The initial model was a persistence skeleton (id, period_id, shift_date, shift_type) lacking lifecycle management, state transitions, and domain events. Sprint 4 enhanced it to a full Aggregate.

## Decision

### Shift as Aggregate Root

Shift becomes the Aggregate Root managing:
- Lifecycle state (scheduled → in_progress → completed → cancelled)
- Time tracking (scheduled_start/end, actual_start/end)
- Computed fields (total_duration_minutes, doctor_count)

### State Machine

Centralized in `ShiftStateMachine`:
- **scheduled → in_progress** (start)
- **in_progress → completed** (complete)
- **scheduled → in_progress → cancelled** (cancel)

### Business Rules

Separated into `ShiftRules`:
- State validation (can_update, can_start, can_complete, can_cancel)
- Period boundary validation
- Time range validation

### Events

Five lifecycle events dispatched through EventDispatcher:
- `shift.created.v1`
- `shift.updated.v1`
- `shift.started.v1`
- `shift.completed.v1`
- `shift.cancelled.v1`

### Value Objects

- `ShiftTimeRange` — immutable time range with duration calculation
- `ShiftTimeline` — mutable timeline tracking schedule vs actual
- Allocation contracts (AssignDoctor, RemoveDoctor, ValidateCoverage, ValidateOverlap)

## Consequences

### Positive
- Full lifecycle management from creation to completion
- Clear separation of concerns (State Machine, Rules, Timeline)
- Domain events enable future integrations (Notifications, Reports)
- Immutability enforced for completed/cancelled shifts

### Negative
- Increased complexity over simple CRUD model
- Additional fields in database (status, scheduled_start/end, actual_start/end)
- State Machine adds indirection for status changes

### Risks
- ShiftParts overlap validation not yet implemented (deferred to Allocation sprint)
- Doctor double-booking not yet enforced (deferred to Allocation sprint)

## Alternatives Considered

1. **Simple status field without State Machine** — Rejected: lacks validation and lifecycle hooks
2. **Event Sourcing for Shift** — Rejected: overengineering for current requirements
3. **Separate ShiftService for lifecycle** — Rejected: State Machine provides cleaner abstraction
