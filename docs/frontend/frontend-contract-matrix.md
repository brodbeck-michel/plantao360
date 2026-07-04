# Frontend Contract Matrix — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## Visão Geral

Matriz completa de contratos entre telas do Frontend e endpoints do Backend.

---

## Dashboard

### DashboardScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| KPICard Cobertura | `GET /api/v1/kpi/coverage` | CoverageKPI | — | — | — | CoverageKPI | — |
| KPICard Financeiro | `GET /api/v1/kpi/financial` | FinancialKPI | — | — | — | FinancialKPI | — |
| KPICard Payroll | `GET /api/v1/kpi/payroll` | PayrollKPI | — | — | — | PayrollKPI | — |
| KPICard Operacional | `GET /api/v1/kpi/operational` | OperationalKPI | — | — | — | OperationalKPI | — |
| Resumo Alertas | `GET /api/v1/analytics/explain` | DomainExplanation | — | — | — | — | DomainExplanation |

---

## Médicos

### DoctorListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Médicos | `GET /api/v1/doctors` | DoctorResponse[] | DoctorQuery | DoctorSummary | DoctorProjection | — | — |
| Filtro por Nome | `GET /api/v1/doctors?name=` | DoctorResponse[] | DoctorQuery | — | — | — | — |
| Filtro por Especialidade | `GET /api/v1/doctors?specialty=` | DoctorResponse[] | DoctorQuery | — | — | — | — |
| Filtro por Status | `GET /api/v1/doctors?status=` | DoctorResponse[] | DoctorQuery | — | — | — | — |

### DoctorDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados do Médico | `GET /api/v1/doctors/{id}` | DoctorDetail | — | DoctorSummary | — | — | — |
| Estatísticas | `GET /api/v1/query/doctors` | DoctorQuery | DoctorQuery | DoctorSummary | — | — | — |

### DoctorFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Criar Médico | `POST /api/v1/doctors` | DoctorCreate | — | — | — | — | — |
| Atualizar Médico | `PUT /api/v1/doctors/{id}` | DoctorUpdate | — | — | — | — | — |

---

## Períodos

### PeriodListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Períodos | `GET /api/v1/periods` | PeriodResponse[] | PeriodQuery | PeriodSummary | PeriodProjection | — | — |
| Filtro por Status | `GET /api/v1/periods?status=` | PeriodResponse[] | PeriodQuery | — | — | — | — |

### PeriodDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados do Período | `GET /api/v1/periods/{id}` | PeriodDetail | — | PeriodSummary | — | — | — |
| Métricas | `GET /api/v1/query/periods` | PeriodQuery | PeriodQuery | PeriodSummary | — | — | — |

### PeriodFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Criar Período | `POST /api/v1/periods` | PeriodCreate | — | — | — | — | — |
| Atualizar Período | `PUT /api/v1/periods/{id}` | PeriodUpdate | — | — | — | — | — |
| Fechar Período | `POST /api/v1/periods/{id}/close` | — | — | — | — | — | — |
| Reabrir Período | `POST /api/v1/periods/{id}/reopen` | — | — | — | — | — | — |

---

## Plantões

### ShiftListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Plantões | `GET /api/v1/shifts` | ShiftResponse[] | ShiftQuery | ShiftSummary | ShiftProjection | — | — |
| Filtro por Data | `GET /api/v1/shifts?date=` | ShiftResponse[] | ShiftQuery | — | — | — | — |
| Filtro por Médico | `GET /api/v1/shifts?doctor_id=` | ShiftResponse[] | ShiftQuery | — | — | — | — |

### ShiftDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados do Plantão | `GET /api/v1/shifts/{id}` | ShiftDetail | — | ShiftSummary | — | — | — |
| Atribuições | `GET /api/v1/query/shifts` | ShiftQuery | ShiftQuery | ShiftSummary | — | — | — |

### ShiftFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Criar Plantão | `POST /api/v1/shifts` | ShiftCreate | — | — | — | — | — |
| Atualizar Plantão | `PUT /api/v1/shifts/{id}` | ShiftUpdate | — | — | — | — | — |
| Cancelar Plantão | `DELETE /api/v1/shifts/{id}` | — | — | — | — | — | — |

### ShiftCalendarScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Calendário | `GET /api/v1/shifts` | ShiftResponse[] | ShiftQuery | ShiftSummary | — | — | — |

---

## Atribuições

### AssignmentListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Atribuições | `GET /api/v1/assignments` | AssignmentResponse[] | AssignmentQuery | AssignmentSummary | AssignmentProjection | — | — |

### AssignmentDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados da Atribuição | `GET /api/v1/assignments/{id}` | AssignmentDetail | — | AssignmentSummary | — | — | — |
| Histórico | `GET /api/v1/query/assignments` | AssignmentQuery | AssignmentQuery | AssignmentSummary | — | — | — |

### AssignmentFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Criar Atribuição | `POST /api/v1/assignments` | AssignmentCreate | — | — | — | — | — |
| Atualizar Atribuição | `PUT /api/v1/assignments/{id}` | AssignmentUpdate | — | — | — | — | — |
| Cancelar Atribuição | `DELETE /api/v1/assignments/{id}` | — | — | — | — | — | — |

---

## Cobertura

### CoverageListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Coberturas | `GET /api/v1/coverage` | CoverageResponse[] | CoverageQuery | CoverageSummary | CoverageProjection | — | — |

### CoverageDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados da Cobertura | `GET /api/v1/coverage/{id}` | CoverageDetail | — | CoverageSummary | — | — | — |
| Detalhes | `GET /api/v1/query/coverage` | CoverageQuery | CoverageQuery | CoverageSummary | — | — | — |

### CoverageFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Solicitar Cobertura | `POST /api/v1/coverage` | CoverageCreate | — | — | — | — | — |
| Aprovar | `POST /api/v1/coverage/{id}/approve` | — | — | — | — | — | — |
| Rejeitar | `POST /api/v1/coverage/{id}/reject` | — | — | — | — | — | — |

---

## Extras

### ExtraListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Extras | `GET /api/v1/extras` | ExtraResponse[] | — | — | — | — | — |

### ExtraDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados do Extra | `GET /api/v1/extras/{id}` | ExtraDetail | — | — | — | — | — |

### ExtraFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Criar Extra | `POST /api/v1/extras` | ExtraCreate | — | — | — | — | — |
| Atualizar Extra | `PUT /api/v1/extras/{id}` | ExtraUpdate | — | — | — | — | — |
| Cancelar Extra | `DELETE /api/v1/extras/{id}` | — | — | — | — | — | — |

---

## Payroll

### PayrollListScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Tabela de Competências | `GET /api/v1/payroll` | PayrollResponse[] | PayrollQuery | PayrollSummary | PayrollProjection | — | — |

### PayrollDetailScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Dados da Competência | `GET /api/v1/payroll/{id}` | PayrollDetail | — | PayrollSummary | — | — | DomainExplanation |
| Governança | `GET /api/v1/query/payroll` | PayrollQuery | PayrollQuery | PayrollSummary | — | — | — |

### PayrollFormScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Criar Competência | `POST /api/v1/payroll` | PayrollCreate | — | — | — | — | — |

### PayrollApprovalScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Readiness | `GET /api/v1/readiness/payroll` | PayrollReadiness | — | — | — | — | — |
| Aprovar | `POST /api/v1/payroll/{id}/approve` | PayrollGovernance | — | — | — | — | DomainExplanation |
| Rejeitar | `POST /api/v1/payroll/{id}/reject` | — | — | — | — | — | — |
| Processar | `POST /api/v1/payroll/{id}/process` | — | — | — | — | — | — |
| Completar | `POST /api/v1/payroll/{id}/complete` | — | — | — | — | — | — |
| Bloquear | `POST /api/v1/payroll/{id}/lock` | — | — | — | — | — | — |

---

## Analytics

### AnalyticsDashboardScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| KPIs | `GET /api/v1/kpi/*` | KPI[] | — | — | — | Todos | — |
| Explicação | `GET /api/v1/analytics/explain` | DomainExplanation | — | — | — | — | DomainExplanation |
| Auditoria | `GET /api/v1/analytics/audit` | AuditAnalytics | — | — | — | — | AuditAnalytics |

### TimelineScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Timeline | `GET /api/v1/analytics/timeline` | InstitutionTimeline | TimelineQuery | — | — | — | InstitutionTimeline |

### ReportsScreen

| Componente | Endpoint | DTO | Query Object | Read Model | Projection | KPI | Explainability |
|---|---|---|---|---|---|---|---|
| Relatórios | `GET /api/v1/analytics/reports` | ReportDefinitions | — | — | — | — | ReportDefinitions |

---

## Resumo de Contratos

| Tela | Endpoints | DTOs | Queries | Read Models | KPIs | Explainability |
|---|---|---|---|---|---|---|
| Dashboard | 5 | 5 | 0 | 0 | 4 | 1 |
| Médicos | 5 | 5 | 2 | 2 | 0 | 0 |
| Períodos | 6 | 4 | 2 | 2 | 0 | 0 |
| Plantões | 5 | 4 | 2 | 2 | 0 | 0 |
| Atribuições | 5 | 3 | 2 | 2 | 0 | 0 |
| Cobertura | 6 | 2 | 2 | 2 | 0 | 0 |
| Extras | 5 | 3 | 0 | 0 | 0 | 0 |
| Payroll | 9 | 3 | 2 | 2 | 0 | 2 |
| Analytics | 4 | 3 | 1 | 0 | 4 | 4 |
| **Total** | **54** | **32** | **13** | **12** | **8** | **7** |

---

## Validação

| Critério | Status |
|---|---|
| Todas as telas mapeadas | ✅ |
| Todos os endpoints listados | ✅ |
| DTOs documentados | ✅ |
| Queries mapeadas | ✅ |
| Read Models mapeados | ✅ |
| KPIs listados | ✅ |
| Explainability mapeado | ✅ |
