# Engineering Freeze — Plantão 360

**Date:** 2026-06-26
**Sprint:** 5.2
**Status:** FROZEN

---

## Declaration

As of Sprint 5.2, the Plantão 360 engineering infrastructure is officially frozen.

All subsequent changes to frozen components require an Architecture Decision Record (ADR).

---

## Frozen Components

### 1. Foundation

| Component | Status | Notes |
|-----------|--------|-------|
| Docker Compose | FROZEN | Multi-service orchestration |
| Nginx | FROZEN | Reverse proxy configuration |
| FastAPI | FROZEN | Application factory pattern |
| React | FROZEN | Frontend framework |
| Database | FROZEN | SQLite dev / PostgreSQL prod |

**What can change:** Configuration values (ports, timeouts)
**What cannot change:** Architecture, patterns, dependencies

### 2. Golden Module

| Component | Status | Notes |
|-----------|--------|-------|
| Doctor Module | FROZEN | Reference architecture |
| File Structure | FROZEN | models/, services/, etc. |
| Patterns | FROZEN | Repository, Service, Mapper |
| DTOs | FROZEN | 7 specialized DTOs |
| Tests | FROZEN | Unit, integration, contracts |

**What can change:** Nothing without ADR
**What cannot change:** Everything

### 3. Internal Developer Platform (IDP)

| Component | Status | Notes |
|-----------|--------|-------|
| Module Generator | FROZEN | Scaffolds new modules |
| Architecture Validator | FROZEN | Validates capabilities |
| Golden Guard | FROZEN | Compares against Golden |
| Architecture Lint | FROZEN | Checks violations |
| Compliance Report | FROZEN | Generates reports |
| Documentation Generator | FROZEN | Generates docs |

**What can change:** Nothing without ADR
**What cannot change:** Everything

### 4. Platform Governance

| Component | Status | Notes |
|-----------|--------|-------|
| Quality Gates | FROZEN | Validation thresholds |
| Architecture Rules | FROZEN | YAML rule definitions |
| CI Pipeline | FROZEN | Automated checks |

**What can change:** Nothing without ADR
**What cannot change:** Everything

### 5. Domain Core

| Component | Status | Notes |
|-----------|--------|-------|
| AggregateRoot | FROZEN | Base class for aggregates |
| EventCollector | FROZEN | Event collection mechanism |
| State Machines | FROZEN | Lifecycle management |
| Value Objects | FROZEN | Shared value objects |
| Business Calendar | FROZEN | Date calculations |

**What can change:** Nothing without ADR
**What cannot change:** Everything

### 6. Module Manifest System

| Component | Status | Notes |
|-----------|--------|-------|
| Manifest Schema | FROZEN | YAML schema definition |
| Manifest Loader | FROZEN | Path resolution |
| Manifest Validator | FROZEN | Schema validation |
| Manifests | FROZEN | Per-aggregate manifests |

**What can change:** Nothing without ADR
**What cannot change:** Everything

### 7. CI Architecture Gate

| Component | Status | Notes |
|-----------|--------|-------|
| Architecture Validator | FROZEN | Automated validation |
| Golden Guard | FROZEN | Automated comparison |
| Lint | FROZEN | Automated linting |

**What can change:** Nothing without ADR
**What cannot change:** Everything

---

## Not Frozen (Domain Phase)

The following CAN evolve without ADR:

| Component | Can Change | Constraints |
|-----------|------------|-------------|
| Business Rules | Yes | Must follow Domain Core patterns |
| Domain Events | Yes | Must use .v1 versioning |
| Use Cases | Yes | Must follow Golden Module patterns |
| API Endpoints | Yes | Must use ApiResponse, pagination |
| DTOs | Yes | Must follow 7-DTO pattern |
| Tests | Yes | Must maintain ≥80% coverage |
| Documentation | Yes | Must keep manifests updated |

---

## Change Process

### For Frozen Components

1. Write ADR (use template)
2. Document context and decision
3. Get architecture team approval
4. Implement change
5. Update Architecture Baseline
6. Update affected manifests
7. Run quality gates
8. Document in release notes

### For Unfrozen Components

1. Implement change
2. Update tests
3. Update documentation
4. Update manifests if needed
5. Run quality gates

---

## Exceptions

No exceptions to this freeze are allowed without:

1. Written justification
2. Architecture team vote
3. ADR documenting the exception
4. Time-bound expiration date

---

## Effective Date

This Engineering Freeze is effective as of Sprint 5.2 (2026-06-26).

All future sprints will operate under these constraints.
