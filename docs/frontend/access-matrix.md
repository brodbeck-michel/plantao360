# Matriz de Acesso — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## Visão Geral

Matriz completa de permissões: Persona → Tela → Botões → Ações → Endpoints → Permissões.

---

## Dashboard

### DashboardScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | KPIs, Alertas | Visualizar, Drill-down | `GET /api/v1/kpi/*` | user |
| Médico | ✅ | KPIs próprios | Visualizar | `GET /api/v1/kpi/*` | user |
| Financeiro | ✅ | Todos KPIs | Visualizar, Drill-down | `GET /api/v1/kpi/*` | admin |
| RH | ✅ | KPIs de pessoal | Visualizar | `GET /api/v1/kpi/*` | user |
| Auditor | ✅ | Todos KPIs | Visualizar, Exportar | `GET /api/v1/kpi/*` | admin |
| Administrador | ✅ | Todos KPIs | Visualizar, Configurar | `GET /api/v1/kpi/*` | admin |
| Diretor | ✅ | KPIs estratégicos | Visualizar | `GET /api/v1/kpi/*` | admin |

---

## Médicos

### DoctorListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Novo, Editar, Desativar | CRUD completo | `GET /api/v1/doctors` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ❌ | — | — | — | — |
| RH | ✅ | Novo, Editar, Desativar | CRUD completo | `GET /api/v1/doctors` | user |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/doctors` | admin |
| Administrador | ✅ | Novo, Editar, Desativar | CRUD completo | `GET /api/v1/doctors` | admin |
| Diretor | ❌ | — | — | — | — |

### DoctorDetailScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Editar, Desativar | Editar, Desativar | `GET /api/v1/doctors/{id}` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ❌ | — | — | — | — |
| RH | ✅ | Editar, Desativar | Editar, Desativar | `GET /api/v1/doctors/{id}` | user |
| Auditor | ✅ | — | Somente leitura | `GET /api/v1/doctors/{id}` | admin |
| Administrador | ✅ | Editar, Desativar | Editar, Desativar | `GET /api/v1/doctors/{id}` | admin |
| Diretor | ❌ | — | — | — | — |

### DoctorFormScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Salvar, Cancelar | Criar, Editar | `POST/PUT /api/v1/doctors` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ❌ | — | — | — | — |
| RH | ✅ | Salvar, Cancelar | Criar, Editar | `POST/PUT /api/v1/doctors` | user |
| Auditor | ❌ | — | — | — | — |
| Administrador | ✅ | Salvar, Cancelar | Criar, Editar | `POST/PUT /api/v1/doctors` | admin |
| Diretor | ❌ | — | — | — | — |

---

## Períodos

### PeriodListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Novo, Editar, Fechar | CRUD + Fechar | `GET /api/v1/periods` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ✅ | Visualizar | Somente leitura | `GET /api/v1/periods` | user |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/periods` | admin |
| Administrador | ✅ | Novo, Editar, Fechar | CRUD completo | `GET /api/v1/periods` | admin |
| Diretor | ✅ | Visualizar | Somente leitura | `GET /api/v1/periods` | admin |

### PeriodDetailScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Editar, Fechar, Reabrir | Editar, Fechar, Reabrir | `GET /api/v1/periods/{id}` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ✅ | — | Somente leitura | `GET /api/v1/periods/{id}` | user |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | — | Somente leitura | `GET /api/v1/periods/{id}` | admin |
| Administrador | ✅ | Editar, Fechar, Reabrir | CRUD completo | `GET /api/v1/periods/{id}` | admin |
| Diretor | ✅ | — | Somente leitura | `GET /api/v1/periods/{id}` | admin |

---

## Plantões

### ShiftListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Novo, Editar, Cancelar | CRUD completo | `GET /api/v1/shifts` | user |
| Médico | ✅ | — | Somente leitura (próprios) | `GET /api/v1/shifts` | user |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/shifts` | admin |
| Administrador | ✅ | Novo, Editar, Cancelar | CRUD completo | `GET /api/v1/shifts` | admin |
| Diretor | ❌ | — | — | — | — |

### ShiftCalendarScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Novo, Arrastar | Criar, Reatribuir | `GET /api/v1/shifts` | user |
| Médico | ✅ | — | Visualizar (próprios) | `GET /api/v1/shifts` | user |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | — | Visualizar | `GET /api/v1/shifts` | admin |
| Administrador | ✅ | Novo, Arrastar | CRUD completo | `GET /api/v1/shifts` | admin |
| Diretor | ❌ | — | — | — | — |

---

## Atribuições

### AssignmentListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Nova, Editar, Cancelar | CRUD completo | `GET /api/v1/assignments` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/assignments` | admin |
| Administrador | ✅ | Nova, Editar, Cancelar | CRUD completo | `GET /api/v1/assignments` | admin |
| Diretor | ❌ | — | — | — | — |

---

## Cobertura

### CoverageListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Aprovar, Rejeitar | Aprovar, Rejeitar | `GET /api/v1/coverage` | user |
| Médico | ✅ | Nova, Visualizar | Criar, Visualizar (próprias) | `GET /api/v1/coverage` | user |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/coverage` | admin |
| Administrador | ✅ | Aprovar, Rejeitar | CRUD completo | `GET /api/v1/coverage` | admin |
| Diretor | ❌ | — | — | — | — |

### CoverageDetailScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Aprovar, Rejeitar | Aprovar, Rejeitar | `GET /api/v1/coverage/{id}` | user |
| Médico | ✅ | — | Visualizar (própria) | `GET /api/v1/coverage/{id}` | user |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | — | Somente leitura | `GET /api/v1/coverage/{id}` | admin |
| Administrador | ✅ | Aprovar, Rejeitar | CRUD completo | `GET /api/v1/coverage/{id}` | admin |
| Diretor | ❌ | — | — | — | — |

---

## Extras

### ExtraListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Novo, Editar, Cancelar | CRUD completo | `GET /api/v1/extras` | user |
| Médico | ✅ | Novo, Visualizar | Criar, Visualizar (próprios) | `GET /api/v1/extras` | user |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/extras` | admin |
| Administrador | ✅ | Novo, Editar, Cancelar | CRUD completo | `GET /api/v1/extras` | admin |
| Diretor | ❌ | — | — | — | — |

---

## Payroll

### PayrollListScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ❌ | — | — | — | — |
| Médico | ❌ | — | — | — | — |
| Financeiro | ✅ | Nova, Editar | CRUD | `GET /api/v1/payroll` | admin |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Visualizar | Somente leitura | `GET /api/v1/payroll` | admin |
| Administrador | ✅ | Nova, Editar | CRUD completo | `GET /api/v1/payroll` | admin |
| Diretor | ✅ | Visualizar | Somente leitura | `GET /api/v1/payroll` | admin |

### PayrollDetailScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ❌ | — | — | — | — |
| Médico | ❌ | — | — | — | — |
| Financeiro | ✅ | Aprovar, Rejeitar, Processar | Aprovar, Rejeitar, Processar | `GET /api/v1/payroll/{id}` | admin |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | — | Somente leitura | `GET /api/v1/payroll/{id}` | admin |
| Administrador | ✅ | Aprovar, Rejeitar, Processar, Bloquear | CRUD completo | `GET /api/v1/payroll/{id}` | admin |
| Diretor | ✅ | — | Somente leitura | `GET /api/v1/payroll/{id}` | admin |

### PayrollApprovalScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Financeiro | ✅ | Aprovar, Rejeitar | Aprovar, Rejeitar | `POST /api/v1/payroll/{id}/approve` | admin |
| Administrador | ✅ | Aprovar, Rejeitar, Bloquear | Aprovar, Rejeitar, Bloquear | `POST /api/v1/payroll/{id}/*` | admin |
| Diretor | ✅ | Aprovar | Aprovar (alto nível) | `POST /api/v1/payroll/{id}/approve` | admin |

---

## Analytics

### AnalyticsDashboardScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Filtros, Exportar | Visualizar, Filtrar | `GET /api/v1/analytics/*` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ✅ | Filtros, Exportar | Visualizar, Filtrar | `GET /api/v1/analytics/*` | admin |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Filtros, Exportar | Visualizar, Filtrar, Exportar | `GET /api/v1/analytics/*` | admin |
| Administrador | ✅ | Filtros, Exportar | Visualizar, Filtrar, Exportar | `GET /api/v1/analytics/*` | admin |
| Diretor | ✅ | Filtros | Visualizar | `GET /api/v1/analytics/*` | admin |

### TimelineScreen

| Persona | Acessa? | Botões Visíveis | Ações | Endpoints | Permissões |
|---|---|---|---|---|---|
| Coordenador | ✅ | Filtros | Visualizar | `GET /api/v1/analytics/timeline` | user |
| Médico | ❌ | — | — | — | — |
| Financeiro | ❌ | — | — | — | — |
| RH | ❌ | — | — | — | — |
| Auditor | ✅ | Filtros, Exportar | Visualizar, Exportar | `GET /api/v1/analytics/timeline` | admin |
| Administrador | ✅ | Filtros, Exportar | Visualizar, Exportar | `GET /api/v1/analytics/timeline` | admin |
| Diretor | ✅ | Filtros | Visualizar | `GET /api/v1/analytics/timeline` | admin |

---

## Resumo de Acesso por Persona

| Persona | Telas Acessíveis | Ações Disponíveis |
|---|---|---|
| Coordenador | Dashboard, Médicos, Períodos, Plantões, Atribuições, Cobertura, Extras, Analytics | CRUD completo + Aprovar Cobertura |
| Médico | Dashboard, Plantões (próprios), Cobertura (próprias), Extras (próprios) | Visualizar, Solicitar Cobertura, Registrar Extra |
| Financeiro | Dashboard, Períodos, Payroll, Readiness, Analytics | Visualizar, Aprovar Payroll, Processar |
| RH | Dashboard, Médicos | CRUD de Médicos |
| Auditor | Dashboard, Todos os módulos, Timeline, Relatórios | Somente leitura + Exportar |
| Administrador | Todos os módulos | CRUD completo + Governance |
| Diretor | Dashboard, Períodos, Payroll, Analytics | Visualizar + Aprovar Payroll (alto nível) |

---

## Validação

| Critério | Status |
|---|---|
| Todas as personas mapeadas | ✅ |
| Todas as telas mapeadas | ✅ |
| Todos os botões listados | ✅ |
| Todas as ações definidas | ✅ |
| Todos os endpoints listados | ✅ |
| Todas as permissões definidas | ✅ |
