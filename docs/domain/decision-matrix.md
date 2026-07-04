# Plantão 360 — Decision Matrix

## Aggregate Decisions

| Decision | Chosen | Alternatives Rejected | Rationale |
|----------|--------|----------------------|-----------|
| ShiftPart as Assignment | Enhance existing table | New table | Preserves DB schema, avoids migration |
| AssignmentStatus lifecycle | planned→confirmed→started→completed→cancelled | Simpler 3-state | Supports future confirmation workflow |
| CoveragePolicy as separate | Standalone policy class | Inside Shift | Single responsibility, testable |
| OverlapDetector | Read-only detector | Real-time enforcement | Algorithm deferred to Sprint 6 |
| Value Objects | Immutable dataclasses | NamedTuple | Better validation, clearer intent |

## Lifecycle Decisions

| Entity | Lifecycle | States | Notes |
|--------|-----------|--------|-------|
| Period | State Machine | draft→closed→paid | Aggregate Root |
| Shift | State Machine | scheduled→in_progress→completed→cancelled | Aggregate Root |
| ShiftPart | State Machine | planned→confirmed→started→completed→cancelled | Child of Shift |

## Deferred Decisions

| Decision | Deferred To | Reason |
|----------|-------------|--------|
| Overlap algorithm | Sprint 6 | Requires complex time matching |
| Automatic distribution | Sprint 7 | Requires coverage optimization |
| Doctor replacement | Sprint 7 | Requires coverage validation |
| Payroll calculation | Sprint 8 | Requires financial domain |
| Multi-sector support | Sprint 10 | Requires architecture change |
| AI optimization | Sprint 9+ | Requires ML infrastructure |
