> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-013: Domain Core Consolidation

## Status

Accepted (Sprint 3.1 — Frozen)

## Context

After implementing Doctor and Period Aggregates, the first opportunity to extract shared domain logic arose. The goal was to consolidate the Domain Core before implementing Shift.

## Decision

We extract only what already exists in at least two Aggregates:

1. **AggregateRoot** — base class with version and event collection
2. **EventCollector** — manages pending events per Aggregate
3. **BusinessCalendar** — business day calculations
4. **Lifecycle Hooks** — empty `before_transition()` / `after_transition()`

## Rationale

### Why now

Two Aggregates (Doctor, Period) existed, providing enough signal to identify common patterns.

### Why AggregateRoot is minimal

It contains only:
- `aggregate_id` — identity
- `version` — future optimistic locking
- `pending_events` — event collection
- `before/after_transition` — hooks

No persistence, no DTOs, no validation, no business rules.

### Why NO BasePolicy

Only Period has a Policy. Doctor has no Policy. Extracting BasePolicy now would be premature.

### Why NO BaseStateMachine

Only Period has a State Machine. Doctor has no lifecycle. Extracting BaseStateMachine would be speculation.

### Why NO BaseRepository in domain

Repositories belong to the application layer. The domain defines the interface (Protocol), not the base implementation.

### Why NOT BaseEntity

SQLAlchemy already provides `Base` with model features. A separate `BaseEntity` would add indirection without value.

### Why BusinessCalendar

Both Doctor and Period modules deal with dates. BusinessCalendar centralizes date logic that would otherwise scatter across Use Cases.

## Consequences

- Domain Core is frozen — any change requires new ADR
- Future Aggregates inherit AggregateRoot
- New abstractions require proof of repetition in ≥2 Aggregates
- `domain/services/` directory exists but is empty until a real domain service emerges

## Abstractions Rejected

| Rejected | Reason |
|----------|--------|
| BasePolicy | Only Period uses it |
| BaseStateMachine | Only Period uses it |
| BaseEntity | SQLAlchemy provides |
| DomainRegistry | Anti-pattern |
| Generic Factory | Overengineering |
| Service Locator | Anti-pattern |
| Event Bus | Too complex |
| CQRS | Not needed |
| Event Sourcing | Not needed |
| Outbox | Not needed |
| Workflow Engine | Not needed |
