# Screen Inventory — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## Visão Geral

Inventário completo de todas as telas do Plantão 360.

---

## 1. Dashboard Principal

### Tela: `DashboardScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visão consolidada da operação |
| **Persona** | Todas |
| **Dados Exibidos** | KPIs, alertas, resumo de atividades |
| **Endpoints** | `GET /api/v1/kpi/coverage`, `GET /api/v1/kpi/financial`, `GET /api/v1/kpi/payroll`, `GET /api/v1/kpi/operational` |
| **KPIs** | Coverage, Financial, Payroll, Operational |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Todas |

---

## 2. Módulo de Médicos

### Tela: `DoctorListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar e gerenciar médicos |
| **Persona** | Coordenador, RH, Administrador |
| **Dados Exibidos** | Nome, CRM, Especialidade, Status, Ações |
| **Endpoints** | `GET /api/v1/doctors` |
| **KPIs** | — |
| **Read Models** | DoctorSummary |
| **Queries** | DoctorQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, RH, Administrador |

### Tela: `DoctorDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes do médico |
| **Persona** | Coordenador, RH, Administrador |
| **Dados Exibidos** | Dados completos, histórico, estatísticas |
| **Endpoints** | `GET /api/v1/doctors/{id}`, `GET /api/v1/query/doctors` |
| **KPIs** | — |
| **Read Models** | DoctorSummary |
| **Queries** | DoctorQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, RH, Administrador |

### Tela: `DoctorFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Criar/editar médico |
| **Persona** | Coordenador, RH, Administrador |
| **Dados Exibidos** | Formulário de cadastro |
| **Endpoints** | `POST /api/v1/doctors`, `PUT /api/v1/doctors/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador, RH, Administrador |

---

## 3. Módulo de Períodos

### Tela: `PeriodListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar e gerenciar períodos |
| **Persona** | Coordenador, Financeiro, Administrador |
| **Dados Exibidos** | Nome, Datas, Tipo, Status, Ações |
| **Endpoints** | `GET /api/v1/periods` |
| **KPIs** | — |
| **Read Models** | PeriodSummary |
| **Queries** | PeriodQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Financeiro, Administrador |

### Tela: `PeriodDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes do período |
| **Persona** | Coordenador, Financeiro, Administrador |
| **Dados Exibidos** | Dados completos, métricas, timeline |
| **Endpoints** | `GET /api/v1/periods/{id}`, `GET /api/v1/query/periods` |
| **KPIs** | — |
| **Read Models** | PeriodSummary |
| **Queries** | PeriodQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Financeiro, Administrador |

### Tela: `PeriodFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Criar/editar período |
| **Persona** | Coordenador, Administrador |
| **Dados Exibidos** | Formulário de período |
| **Endpoints** | `POST /api/v1/periods`, `PUT /api/v1/periods/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador, Administrador |

---

## 4. Módulo de Plantões

### Tela: `ShiftListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar e gerenciar plantões |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Data, Horário, Médico, Tipo, Status, Ações |
| **Endpoints** | `GET /api/v1/shifts` |
| **KPIs** | — |
| **Read Models** | ShiftSummary |
| **Queries** | ShiftQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprios) |

### Tela: `ShiftDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes do plantão |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Dados completos, atribuições, cobertura |
| **Endpoints** | `GET /api/v1/shifts/{id}`, `GET /api/v1/query/shifts` |
| **KPIs** | — |
| **Read Models** | ShiftSummary |
| **Queries** | ShiftQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprios) |

### Tela: `ShiftFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Criar/editar plantão |
| **Persona** | Coordenador |
| **Dados Exibidos** | Formulário de plantão |
| **Endpoints** | `POST /api/v1/shifts`, `PUT /api/v1/shifts/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador |

### Tela: `ShiftCalendarScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar plantões em calendário |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Calendário com plantões, conflitos, coberturas |
| **Endpoints** | `GET /api/v1/shifts` |
| **KPIs** | — |
| **Read Models** | ShiftSummary |
| **Queries** | ShiftQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprios) |

---

## 5. Módulo de Atribuições

### Tela: `AssignmentListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar e gerenciar atribuições |
| **Persona** | Coordenador |
| **Dados Exibidos** | Plantão, Médico, Tipo, Status, Ações |
| **Endpoints** | `GET /api/v1/assignments` |
| **KPIs** | — |
| **Read Models** | AssignmentSummary |
| **Queries** | AssignmentQuery |
| **Explainability** | — |
| **Permissões** | Coordenador |

### Tela: `AssignmentDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes da atribuição |
| **Persona** | Coordenador |
| **Dados Exibidos** | Dados completos, histórico |
| **Endpoints** | `GET /api/v1/assignments/{id}`, `GET /api/v1/query/assignments` |
| **KPIs** | — |
| **Read Models** | AssignmentSummary |
| **Queries** | AssignmentQuery |
| **Explainability** | — |
| **Permissões** | Coordenador |

### Tela: `AssignmentFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Criar/editar atribuição |
| **Persona** | Coordenador |
| **Dados Exibidos** | Formulário de atribuição |
| **Endpoints** | `POST /api/v1/assignments`, `PUT /api/v1/assignments/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador |

---

## 6. Módulo de Cobertura

### Tela: `CoverageListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar e gerenciar coberturas |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Plantão, Tipo, Status, Data Solicitação, Ações |
| **Endpoints** | `GET /api/v1/coverage` |
| **KPIs** | — |
| **Read Models** | CoverageSummary |
| **Queries** | CoverageQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprias) |

### Tela: `CoverageDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes da cobertura |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Dados completos, motivo, decisão |
| **Endpoints** | `GET /api/v1/coverage/{id}`, `GET /api/v1/query/coverage` |
| **KPIs** | — |
| **Read Models** | CoverageSummary |
| **Queries** | CoverageQuery |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprias) |

### Tela: `CoverageFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Solicitar cobertura |
| **Persona** | Médico, Coordenador |
| **Dados Exibidos** | Formulário de solicitação |
| **Endpoints** | `POST /api/v1/coverage` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Médico, Coordenador |

---

## 7. Módulo de Extras

### Tela: `ExtraListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar e gerenciar extras |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Médico, Plantão, Tipo, Duração, Status, Ações |
| **Endpoints** | `GET /api/v1/extras` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprios) |

### Tela: `ExtraDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes do extra |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Dados completos, justificativa |
| **Endpoints** | `GET /api/v1/extras/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico (próprios) |

### Tela: `ExtraFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Criar/editar extra |
| **Persona** | Coordenador, Médico |
| **Dados Exibidos** | Formulário de extra |
| **Endpoints** | `POST /api/v1/extras`, `PUT /api/v1/extras/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Coordenador, Médico |

---

## 8. Módulo de Payroll

### Tela: `PayrollListScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Listar competências de folha |
| **Persona** | Financeiro, Administrador |
| **Dados Exibidos** | Competência, Período, Status, Valor Total, Ações |
| **Endpoints** | `GET /api/v1/payroll` |
| **KPIs** | — |
| **Read Models** | PayrollSummary |
| **Queries** | PayrollQuery |
| **Explainability** | — |
| **Permissões** | Financeiro, Administrador |

### Tela: `PayrollDetailScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar detalhes da competência |
| **Persona** | Financeiro, Administrador |
| **Dados Exibidos** | Dados completos, checklist, governança |
| **Endpoints** | `GET /api/v1/payroll/{id}`, `GET /api/v1/query/payroll` |
| **KPIs** | — |
| **Read Models** | PayrollSummary |
| **Queries** | PayrollQuery |
| **Explainability** | DomainExplanation |
| **Permissões** | Financeiro, Administrador |

### Tela: `PayrollFormScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Criar/editar competência |
| **Persona** | Financeiro, Administrador |
| **Dados Exibidos** | Formulário de competência |
| **Endpoints** | `POST /api/v1/payroll`, `PUT /api/v1/payroll/{id}` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Financeiro, Administrador |

### Tela: `PayrollApprovalScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Aprovar/rejeitar competência |
| **Persona** | Financeiro, Administrador |
| **Dados Exibidos** | Checklist, readiness, decisões |
| **Endpoints** | `POST /api/v1/payroll/{id}/approve`, `POST /api/v1/payroll/{id}/reject` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | DomainExplanation |
| **Permissões** | Financeiro, Administrador |

---

## 9. Módulo de Analytics

### Tela: `AnalyticsDashboardScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Dashboard de analytics |
| **Persona** | Coordenador, Financeiro, Auditor, Diretor |
| **Dados Exibidos** | KPIs, gráficos, tendências |
| **Endpoints** | `GET /api/v1/analytics/explain`, `GET /api/v1/analytics/audit` |
| **KPIs** | Todos |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | DomainExplanation, AuditAnalytics |
| **Permissões** | Coordenador, Financeiro, Auditor, Diretor |

### Tela: `TimelineScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Visualizar timeline da instituição |
| **Persona** | Auditor, Coordenador, Diretor |
| **Dados Exibidos** | Eventos cronológicos, filtros |
| **Endpoints** | `GET /api/v1/analytics/timeline` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | TimelineQuery |
| **Explainability** | InstitutionTimeline |
| **Permissões** | Auditor, Coordenador, Diretor |

### Tela: `ReportsScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Gerenciar relatórios |
| **Persona** | Financeiro, Auditor, Diretor |
| **Dados Exibidos** | Definições de relatórios, exportações |
| **Endpoints** | `GET /api/v1/analytics/reports` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | ReportDefinitions |
| **Permissões** | Financeiro, Auditor, Diretor |

---

## 10. Módulo de Readiness

### Tela: `ReadinessScreen`

| Propriedade | Valor |
|---|---|
| **Objetivo** | Verificar prontidão de payroll |
| **Persona** | Financeiro, Administrador |
| **Dados Exibidos** | Itens de readiness, status |
| **Endpoints** | `GET /api/v1/readiness/payroll` |
| **KPIs** | — |
| **Read Models** | — |
| **Queries** | — |
| **Explainability** | — |
| **Permissões** | Financeiro, Administrador |

---

## Resumo de Telas

| Módulo | Telas | Total |
|---|---|---|
| Dashboard | 1 | 1 |
| Médicos | 3 | 3 |
| Períodos | 3 | 3 |
| Plantões | 4 | 4 |
| Atribuições | 3 | 3 |
| Cobertura | 3 | 3 |
| Extras | 3 | 3 |
| Payroll | 4 | 4 |
| Analytics | 3 | 3 |
| Readiness | 1 | 1 |
| **Total** | — | **28** |

---

## Validação

| Critério | Status |
|---|---|
| Todas as telas listadas | ✅ |
| Objetivos definidos | ✅ |
| Personas mapeadas | ✅ |
| Dados exibidos documentados | ✅ |
| Endpoints mapeados | ✅ |
| KPIs listados | ✅ |
| Read Models mapeados | ✅ |
| Queries mapeadas | ✅ |
| Explainability mapeado | ✅ |
| Permissões definidas | ✅ |
