# Auditoria Funcional — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27
**Status:** CONCLUÍDA

---

## Perguntas de Auditoria

### 1. Existe alguma operação sem suporte?

**Resposta:** Não.

Todas as operações identificadas no domínio possuem suporte via endpoints:

| Operação | Endpoint | Suporte |
|---|---|---|
| CRUD de Médicos | `/api/v1/doctors` | ✅ |
| CRUD de Períodos | `/api/v1/periods` | ✅ |
| CRUD de Plantões | `/api/v1/shifts` | ✅ |
| CRUD de Atribuições | `/api/v1/assignments` | ✅ |
| CRUD de Coberturas | `/api/v1/coverage` | ✅ |
| CRUD de Extras | `/api/v1/extras` | ✅ |
| CRUD de Payroll | `/api/v1/payroll` | ✅ |
| Fechar Período | `POST /api/v1/periods/{id}/close` | ✅ |
| Reabrir Período | `POST /api/v1/periods/{id}/reopen` | ✅ |
| Aprovar Payroll | `POST /api/v1/payroll/{id}/approve` | ✅ |
| Rejeitar Payroll | `POST /api/v1/payroll/{id}/reject` | ✅ |
| Processar Payroll | `POST /api/v1/payroll/{id}/process` | ✅ |
| Completar Payroll | `POST /api/v1/payroll/{id}/complete` | ✅ |
| Bloquear Payroll | `POST /api/v1/payroll/{id}/lock` | ✅ |
| Aprovar Cobertura | `POST /api/v1/coverage/{id}/approve` | ✅ |
| Rejeitar Cobertura | `POST /api/v1/coverage/{id}/reject` | ✅ |
| Consultar Readiness | `GET /api/v1/readiness/payroll` | ✅ |
| Consultar Queries | `GET /api/v1/query/*` | ✅ |
| Consultar Analytics | `GET /api/v1/analytics/*` | ✅ |
| Consultar KPIs | `GET /api/v1/kpi/*` | ✅ |

**Conclusão:** Nenhuma operação sem suporte.

---

### 2. Existem APIs inutilizadas?

**Resposta:** Não.

Todas as 60 endpoints são utilizáveis e possuem uso documentado:

| Categoria | Endpoints | Uso |
|---|---|---|
| Doctors | 5 | CRUD completo |
| Periods | 6 | CRUD + close/reopen |
| Shifts | 5 | CRUD + cancel |
| Assignments | 5 | CRUD + cancel |
| Coverage | 6 | CRUD + approve/reject |
| Extras | 5 | CRUD |
| Payroll | 9 | CRUD + governance |
| Readiness | 1 | Verificação |
| Query | 7 | Consultas read-only |
| Analytics | 4 | Análises |
| KPIs | 4 | Indicadores |
| Health | 3 | Infraestrutura |

**Conclusão:** Nenhuma API inutilizada.

---

### 3. Existem jornadas incompletas?

**Resposta:** Sim, identificadas as seguintes lacunas:

| Jornada | Status | Lacuna |
|---|---|---|
| Gerenciar Médicos | ✅ Completa | — |
| Gerenciar Períodos | ✅ Completa | — |
| Gerenciar Plantões | ✅ Completa | — |
| Gerenciar Atribuições | ✅ Completa | — |
| Gerenciar Coberturas | ✅ Completa | — |
| Gerenciar Extras | ⚠️ Parcial | Jornada não documentada em user-journeys.md |
| Gerenciar Payroll | ✅ Completa | — |
| Visualizar Analytics | ✅ Completa | — |
| **Gerenciar Extras** | ❌ Ausente | Não documentada |
| **Consultar Relatórios** | ❌ Ausente | Não documentada |
| **Exportar Dados** | ❌ Ausente | Não documentada |

**Ação necessária:** Documentar jornadas faltantes nesta sprint.

---

### 4. Existe alguma regra impossível de executar?

**Resposta:** Não.

Todas as regras de negócio são executáveis via endpoints disponíveis:

| Regra | Execução | Viável? |
|---|---|---|
| Fechar período apenas em status DRAFT | `POST /api/v1/periods/{id}/close` | ✅ |
| Aprovar payroll com checklist completo | `POST /api/v1/payroll/{id}/approve` | ✅ |
| Bloquear payroll após aprovação | `POST /api/v1/payroll/{id}/lock` | ✅ |
| Cancelar plantão apenas em SCHEDULED | `DELETE /api/v1/shifts/{id}` | ✅ |
| Aprovar cobertura apenas em PENDING | `POST /api/v1/coverage/{id}/approve` | ✅ |

**Conclusão:** Nenhuma regra impossível de executar.

---

### 5. Existe alguma operação excessivamente complexa?

**Resposta:** Sim, identificadas:

| Operação | Complexidade | Motivo |
|---|---|---|
| Aprovar Payroll | Alta | Requer checklist, readiness, snapshot |
| Processar Payroll | Alta | Consolida dados financeiros |
| Fechar Período | Média | Validações de estado |
| Consolidar Cobertura | Média | Múltiplas fontes de dados |

**Ação necessária:** Simplificar UX para operações complexas (documentado nesta sprint).

---

## Resumo da Auditoria

| Pergunta | Resultado | Ação |
|---|---|---|
| Operação sem suporte? | Não | Nenhuma |
| APIs inutilizadas? | Não | Nenhuma |
| Jornadas incompletas? | Sim | Documentar faltantes |
| Regras impossíveis? | Não | Nenhuma |
| Operações complexas? | Sim | Simplificar UX |

---

## Conclusão

A auditoria funcional identificou:
- **3 jornadas faltantes** (Extras, Relatórios, Exportação)
- **2 operações de alta complexidade** que precisam de UX simplificada

Nenhuma lacuna crítica foi encontrada que impeça a implementação do Frontend.
