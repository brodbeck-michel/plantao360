> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-011: Platform Governance & CI Architecture Gate

**Date:** 2026-06-25

**Status:** accepted

**Deciders:** Plantão 360 Architecture Team

---

## Context

The Internal Developer Platform (IDP) was completed in Sprint 2.7. However, all architecture validation tools relied on manual execution by developers. This creates a significant risk:

- Developers may forget to run validators
- Architectural violations can slip through
- Inconsistencies accumulate over time
- No automatic enforcement of patterns

The project needs automated architecture protection that cannot be bypassed.

## Decision

Implement a comprehensive CI/CD architecture gate with the following components:

1. **CI Pipelines** — GitHub Actions workflows for architecture, quality, and release
2. **Architecture Rules Engine** — YAML-based rules for each layer (router, service, repository, etc.)
3. **Golden Guard** — Compares all modules against the Golden Module
4. **Template Consistency Check** — Ensures templates match Golden Module
5. **ADR Validator** — Ensures architectural changes have ADRs
6. **Technical Debt Detector** — Tracks TODOs, FIXMEs, deprecated code
7. **Architecture Score** — Quantitative architecture quality metric
8. **Release Readiness** — Blocks releases if quality gates fail
9. **Pre-commit Enterprise** — Validates before commit

## Rationale

Architecture should not depend on human discipline. Architecture should be validated by code.

Every documented pattern must have an automated verifier. Architecture as Code.

## Consequences

### Positive

- No architectural violation can enter the codebase without detection
- All PRs are automatically validated
- Quantitative architecture metrics available at all times
- Release readiness is objective, not subjective
- Developer experience improved with clear feedback

### Negative

- Initial setup complexity
- Pipeline execution time increased
- False positives may require tuning

### Neutral

- All existing modules must pass validation
- ADRs become mandatory for architectural changes
- Architecture score becomes a team metric

## Implementation

### CI Pipelines

- `architecture.yml` — Architecture validation on every PR
- `backend.yml` — Backend quality checks
- `quality.yml` — Full quality pipeline
- `frontend.yml` — Frontend quality checks
- `release-readiness.yml` — Release validation

### Architecture Rules (YAML)

- `router.yaml` — Router layer rules
- `service.yaml` — Service layer rules
- `repository.yaml` — Repository layer rules
- `mapper.yaml` — Mapper layer rules
- `validator.yaml` — Validator layer rules
- `dto.yaml` — DTO layer rules
- `events.yaml` — Event layer rules
- `audit.yaml` — Audit layer rules
- `tests.yaml` — Test layer rules

### Tools

| Tool | Purpose |
|------|---------|
| `golden_guard.py` | Module vs Golden comparison |
| `check_templates.py` | Template consistency |
| `check_adrs.py` | ADR coverage |
| `technical_debt.py` | Debt detection |
| `check_dependencies.py` | Dependency issues |
| `architecture_score.py` | Quality metric |
| `release_readiness.py` | Release validation |
| `module_maturity.py` | Module maturity |

## References

- ADR-001: Monolito Modular
- ADR-010: Enterprise Application Patterns
- Sprint 2.7: Internal Developer Platform
- Sprint 2.8: Platform Governance
