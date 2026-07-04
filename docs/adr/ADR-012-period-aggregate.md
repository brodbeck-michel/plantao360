# ADR-012: Period Aggregate Architecture

## Status

Accepted

## Context

The Period module is the first Aggregate Root in the Plantão 360 domain. It manages billing periods (year/month) with a lifecycle: draft → closed → paid.

## Decision

We implement Period as a full Aggregate Root with:

1. **State Machine** — validates lifecycle transitions
2. **Policy** — queries allowed operations
3. **ClockProvider** — time abstraction for testing
4. **Transition** — immutable domain event representation
5. **Snapshot** — read-only state for export/audit
6. **Contract** — formal permissions for external Aggregates
7. **Metrics** — domain-level KPIs

## Rationale

### Why Period is Aggregate Root

Period is the temporal boundary for all shift operations. Shifts cannot exist without a Period. Period owns the lifecycle that determines whether shifts can be created or modified.

### Which Aggregates depend on Period

- **Shift** — references Period by period_id, reads status
- **ShiftPart** — references Shift (indirectly depends on Period)
- **ShiftExtra** — references Period for billing
- **Payroll** — depends on Period being closed

### Why State Machine is separate

The State Machine encapsulates all transition logic in one place. Use Cases delegate to it instead of duplicating transition checks. This makes transitions testable, configurable, and auditable independently.

### Why Policy is separate

The Policy provides a query interface for external code. Other Aggregates can ask "can I close this period?" without executing the close operation. The Aggregate remains responsible for enforcing invariants.

### Why ClockProvider exists

Testing time-dependent logic requires deterministic time. `FutureClock` enables testing transitions that depend on timestamps without mocking `datetime.now()`.

## Consequences

- All state changes flow through Use Cases → State Machine
- No Use Case directly checks status values
- External Aggregates interact only through the Contract
- Domain events carry full transition metadata
- Snapshots enable audit without database queries

## Compliance

- Follows ADR-001 (Modular Monolith)
- Follows ADR-010 (Event Versioning)
- No new patterns introduced — uses established enterprise patterns
