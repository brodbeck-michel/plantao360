# Public API Contract — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

O Public API Contract define todos os endpoints públicos, administrativos e internos do Plantão 360.

---

## Versionamento

| Prefixo | Uso | Estabilidade |
|---|---|---|
| `/api/v1/` | Versão atual | Stable |
| `/api/v2/` | Versão futura | Preparado |

---

## Endpoints Públicos

### Doctors

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/doctors` | Listar médicos |
| `GET` | `/api/v1/doctors/{id}` | Obter médico por ID |
| `POST` | `/api/v1/doctors` | Criar médico |
| `PUT` | `/api/v1/doctors/{id}` | Atualizar médico |
| `DELETE` | `/api/v1/doctors/{id}` | Desativar médico |

---

### Periods

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/periods` | Listar períodos |
| `GET` | `/api/v1/periods/{id}` | Obter período por ID |
| `POST` | `/api/v1/periods` | Criar período |
| `PUT` | `/api/v1/periods/{id}` | Atualizar período |
| `POST` | `/api/v1/periods/{id}/close` | Fechar período |
| `POST` | `/api/v1/periods/{id}/reopen` | Reabrir período |

---

### Shifts

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/shifts` | Listar plantões |
| `GET` | `/api/v1/shifts/{id}` | Obter plantão por ID |
| `POST` | `/api/v1/shifts` | Criar plantão |
| `PUT` | `/api/v1/shifts/{id}` | Atualizar plantão |
| `DELETE` | `/api/v1/shifts/{id}` | Cancelar plantão |

---

### Assignments

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/assignments` | Listar atribuições |
| `GET` | `/api/v1/assignments/{id}` | Obter atribuição por ID |
| `POST` | `/api/v1/assignments` | Criar atribuição |
| `PUT` | `/api/v1/assignments/{id}` | Atualizar atribuição |
| `DELETE` | `/api/v1/assignments/{id}` | Cancelar atribuição |

---

### Coverage

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/coverage` | Listar coberturas |
| `GET` | `/api/v1/coverage/{id}` | Obter cobertura por ID |
| `POST` | `/api/v1/coverage` | Solicitar cobertura |
| `PUT` | `/api/v1/coverage/{id}` | Atualizar cobertura |
| `POST` | `/api/v1/coverage/{id}/approve` | Aprovar cobertura |
| `POST` | `/api/v1/coverage/{id}/reject` | Rejeitar cobertura |

---

### Extras

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/extras` | Listar extras |
| `GET` | `/api/v1/extras/{id}` | Obter extra por ID |
| `POST` | `/api/v1/extras` | Criar extra |
| `PUT` | `/api/v1/extras/{id}` | Atualizar extra |
| `DELETE` | `/api/v1/extras/{id}` | Cancelar extra |

---

### Payroll

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/payroll` | Listar competências |
| `GET` | `/api/v1/payroll/{id}` | Obter competência por ID |
| `POST` | `/api/v1/payroll` | Criar competência |
| `PUT` | `/api/v1/payroll/{id}` | Atualizar competência |
| `POST` | `/api/v1/payroll/{id}/approve` | Aprovar competência |
| `POST` | `/api/v1/payroll/{id}/reject` | Rejeitar competência |
| `POST` | `/api/v1/payroll/{id}/process` | Processar competência |
| `POST` | `/api/v1/payroll/{id}/complete` | Completar competência |
| `POST` | `/api/v1/payroll/{id}/lock` | Bloquear competência |

---

## Endpoints Administrativos

### Readiness

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/readiness/payroll` | Verificar prontidão de payroll |

---

### Query Domain

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/query/doctors` | Consultar médicos (read-only) |
| `GET` | `/api/v1/query/periods` | Consultar períodos (read-only) |
| `GET` | `/api/v1/query/shifts` | Consultar plantões (read-only) |
| `GET` | `/api/v1/query/assignments` | Consultar atribuições (read-only) |
| `GET` | `/api/v1/query/coverage` | Consultar coberturas (read-only) |
| `GET` | `/api/v1/query/financial` | Consultar dados financeiros (read-only) |
| `GET` | `/api/v1/query/payroll` | Consultar payroll (read-only) |

---

### Analytics

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/analytics/explain` | Explicar domínio |
| `GET` | `/api/v1/analytics/audit` | Análise de auditoria |
| `GET` | `/api/v1/analytics/timeline` | Timeline da instituição |
| `GET` | `/api/v1/analytics/reports` | Definições de relatórios |

---

### KPIs

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/kpi/coverage` | KPI de cobertura |
| `GET` | `/api/v1/kpi/financial` | KPI financeiro |
| `GET` | `/api/v1/kpi/payroll` | KPI de payroll |
| `GET` | `/api/v1/kpi/operational` | KPI operacional |

---

## Endpoints Internos

### Health

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/health/ready` | Readiness check |
| `GET` | `/api/v1/health/live` | Liveness check |

---

## Schemas

### Request/Response Padrão

```json
{
  "data": {},
  "meta": {
    "timestamp": "2026-06-27T00:00:00Z",
    "version": "v1"
  }
}
```

### Erro Padrão

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": []
  }
}
```

---

## Autenticação

| Endpoint | Autenticação | Nível |
|---|---|---|
| `/api/v1/health/*` | Não | Público |
| `/api/v1/doctors/*` | Sim | Usuário |
| `/api/v1/periods/*` | Sim | Usuário |
| `/api/v1/shifts/*` | Sim | Usuário |
| `/api/v1/assignments/*` | Sim | Usuário |
| `/api/v1/coverage/*` | Sim | Usuário |
| `/api/v1/extras/*` | Sim | Usuário |
| `/api/v1/payroll/*` | Sim | Administrador |
| `/api/v1/readiness/*` | Sim | Administrador |
| `/api/v1/query/*` | Sim | Usuário |
| `/api/v1/analytics/*` | Sim | Administrador |
| `/api/v1/kpi/*` | Sim | Administrador |

---

## Validação

| Critério | Status |
|---|---|
| Todos os endpoints documentados | ✅ |
| Versionamento definido | ✅ |
| Schemas documentados | ✅ |
| Autenticação documentada | ✅ |
| Erros padronizados | ✅ |
