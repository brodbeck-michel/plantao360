# ADR-017: Engineering Freeze

**Status:** Accepted
**Date:** 2026-06-26
**Sprint:** 5.2
**Deciders:** Architecture Team

---

## Context

The Plantão 360 platform has completed 5.2 sprints of engineering work. The following layers are implemented and stable:

- Foundation (Docker, Nginx, FastAPI, React)
- Golden Module (Doctor)
- Internal Developer Platform (IDP)
- Platform Governance (Quality Gates)
- Module Manifest System
- Domain Core (Aggregate Root, State Machines, Events)
- CI Architecture Gate

All existing modules use this common infrastructure. The architecture has been audited and found coherent (Architecture Audit V1).

## Decision

We will officially freeze the engineering infrastructure and transition to the Domain Phase.

### Engineering Freeze Scope

**Frozen (requires ADR for changes):**
- Foundation layer (Docker, Nginx, database config)
- Golden Module pattern (Doctor architecture)
- Internal Developer Platform (generators, validators, linters)
- Platform Governance (quality gates, manifest system)
- Domain Core (AggregateRoot, EventCollector, State Machines)
- Module Manifest System (schema, loader, validator)
- CI Architecture Gate

**Not Frozen (can evolve within Domain Phase):**
- Business rules within aggregates
- Domain events (new events can be added)
- Use cases (new use cases can be added)
- API endpoints (new endpoints can be added)
- DTOs (new DTOs can be added)
- Tests (new tests can be added)

### Criteria for Future Structural Changes

Any change to frozen components requires:

1. Written ADR with context, decision, and consequences
2. Architecture team approval
3. Impact analysis on existing modules
4. Update to Architecture Baseline
5. Quality gates re-validation

## Consequences

### Positive

- **Stability**: Infrastructure is reliable and well-tested
- **Predictability**: Teams know what can and cannot change
- **Quality**: All changes go through ADR process
- **Documentation**: Architecture is fully documented

### Negative

- **Rigidity**: Structural improvements require ADR overhead
- **Learning curve**: New team members must understand freeze scope

### Mitigations

- ADR process is lightweight (template exists)
- Architecture Baseline documents current state clearly
- Engineering Freeze document explains what's frozen

## References

- ADR-001: Monolito Modular
- ADR-002: Clean Architecture
- ADR-010: Enterprise Application Patterns
- ADR-011: Platform Governance
- ADR-013: Domain Core
- ADR-016: Module Manifest System
- Architecture Baseline V1
- Engineering Freeze Document
