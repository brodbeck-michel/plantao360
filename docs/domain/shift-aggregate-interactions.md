# Shift Aggregate — Aggregate Interactions

## Shift ↔ Period

```
Shift reads Period (via FK period_id)
Shift validates date within Period boundaries
Period lifecycle affects Shift availability
```

## Shift ↔ Doctor (via ShiftPart)

```
ShiftPart assigns Doctor to Shift
Doctor availability checked at ShiftPart level
No direct Shift↔Doctor mutation
```

## Shift → Events

```
shift.created.v1  → dispatched on creation
shift.updated.v1  → dispatched on update
shift.started.v1  → dispatched on status transition to in_progress
shift.completed.v1 → dispatched on status transition to completed
shift.cancelled.v1 → dispatched on status transition to cancelled
```

## Rules

1. Shift date must fall within Period year/month
2. Shift cannot be updated after completion or cancellation
3. Shift cannot be started unless status is scheduled
4. Shift cannot be completed unless status is in_progress
5. Shift cannot be cancelled if already completed
6. ShiftParts cannot overlap in time for same Doctor
