# Module Compliance Report: Query Domain

**Generated:** 2026-06-27 12:00
**Module ID:** domain.query
**Storage:** read-only (no storage)
**Validation Profile:** default
**Sprint:** 10 — Reporting Domain, Audit Analytics & Explainability Foundation

---

| **Component** | **Status** | **Details** |
|---|---|---|
| Read Models | ✓ | 7 models (Doctor, Period, Shift, Assignment, Coverage, Financial, Payroll) |
| Query Objects | ✓ | 5 objects (Doctor, Coverage, Financial, Payroll, Timeline) |
| Projections | ✓ | 4 projections (Coverage, Financial, Payroll, Institution) |
| Explainability | ✓ | DomainExplanation + ExplanationStep + ExplanationContext |
| Audit Analytics | ✓ | AuditAnalytics + CompetencyAudit + ApprovalAudit + ChangeAudit |
| KPI Domain | ✓ | 4 KPIs (Coverage, Financial, Payroll, Operational) |
| Timeline | ✓ | InstitutionTimeline + TimelineEvent |
| Report Definitions | ✓ | ReportDefinition + ReportField + ReportFilter |
| Query Service | ✓ | `query_service.py` |
| Query Routes | ✓ | `query.py` (13 endpoints) |
| Tests (domain) | ✓ | `test_query_domain.py` (37 tests) |
| Documentation | ✓ | `analise-consultas-negocio.md` |
| Glossary | ✓ | `glossario-consultas.md` |
| Query Matrix | ✓ | `matriz-consultas.md` |
| ADR | ✓ | `ADR-023-query-domain-explainability.md` |

---

## Summary

| Metric | Value |
|--------|-------|
| Module | Query Domain |
| Components Checked | 15 |
| Passed | 15 |
| Failed | 0 |
| Compliance | 100% |

---

## Sprint 10 Deliverables

| Deliverable | Status |
|---|---|
| Análise das consultas de negócio | ✓ |
| Glossário | ✓ |
| Matriz de consultas | ✓ |
| Read Models (7) | ✓ |
| Query Objects (5) | ✓ |
| Projeções (4) | ✓ |
| DomainExplanation | ✓ |
| Audit Analytics | ✓ |
| KPI Domain (4) | ✓ |
| InstitutionTimeline | ✓ |
| ReportDefinitions | ✓ |
| Query Service | ✓ |
| Query Endpoints (13) | ✓ |
| Testes (37 tests passing) | ✓ |
| Coverage Gap Report | ✓ |
| ADR-023 | ✓ |

---

## Test Coverage

| Test File | Tests | Status |
|---|---|---|
| `test_query_domain.py` | 37 | ✓ All passing |

---

## Component Summary

| Category | Count |
|---|---|
| Read Models | 7 |
| Query Objects | 5 |
| Projections | 4 |
| Explainability | 3 |
| Audit Analytics | 4 |
| KPIs | 4 |
| Timeline | 2 |
| Report Definitions | 3 |
| **Total Domain** | **32** |
| Query Service | 1 |
| API Endpoints | 13 |
| Tests | 37 |

---

## Architecture Compliance

| Rule | Status |
|---|---|
| Read-only queries | ✓ No state modification |
| Desacoplamento | ✓ Read Models ≠ SQLAlchemy Models |
| Query Objects ≠ HTTP filters | ✓ Domain questions |
| Explainability reproduzível | ✓ Steps + rules + evidence |
| KPIs com fórmula e evidências | ✓ All 4 KPIs |
| Timeline rastreável | ✓ Events + timestamps |
| Nenhuma regra duplicada | ✓ Consumes existing aggregates |
