# Capability Matrix — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

A Capability Matrix documenta todas as capacidades do Plantão 360 e seu status de implementação.

---

## Capacidades por Contexto

### 1. Doctor Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Criar médico | ✅ | Sim |
| Atualizar médico | ✅ | Sim |
| Desativar médico | ✅ | Sim |
| Listar médicos | ✅ | Sim |
| Obter médico por ID | ✅ | Sim |
| Sincronizar médicos (externo) | 🔮 | Não (futuro) |
| Validar CRM (externo) | 🔮 | Não (futuro) |

---

### 2. Period Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Criar período | ✅ | Sim |
| Atualizar período | ✅ | Sim |
| Fechar período | ✅ | Sim |
| Reabrir período | ✅ | Sim |
| Listar períodos | ✅ | Sim |
| Obter período por ID | ✅ | Sim |

---

### 3. Shift Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Criar plantão | ✅ | Sim |
| Atualizar plantão | ✅ | Sim |
| Cancelar plantão | ✅ | Sim |
| Listar plantões | ✅ | Sim |
| Obter plantão por ID | ✅ | Sim |
| Exportar agenda (externo) | 🔮 | Não (futuro) |
| Importar agenda (externo) | 🔮 | Não (futuro) |

---

### 4. Assignment Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Criar atribuição | ✅ | Sim |
| Atualizar atribuição | ✅ | Sim |
| Cancelar atribuição | ✅ | Sim |
| Listar atribuições | ✅ | Sim |
| Obter atribuição por ID | ✅ | Sim |

---

### 5. Coverage Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Solicitar cobertura | ✅ | Sim |
| Aprovar cobertura | ✅ | Sim |
| Rejeitar cobertura | ✅ | Sim |
| Listar coberturas | ✅ | Sim |
| Obter cobertura por ID | ✅ | Sim |

---

### 6. Financial Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Calcular dados financeiros | ✅ | Sim |
| Aprovar dados financeiros | ✅ | Sim |
| Listar dados financeiros | ✅ | Sim |
| Exportar dados financeiros (externo) | 🔮 | Não (futuro) |
| Importar dados financeiros (externo) | 🔮 | Não (futuro) |
| Obter status de pagamento (externo) | 🔮 | Não (futuro) |

---

### 7. Payroll Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Criar competência | ✅ | Sim |
| Aprovar competência | ✅ | Sim |
| Rejeitar competência | ✅ | Sim |
| Processar competência | ✅ | Sim |
| Completar competência | ✅ | Sim |
| Bloquear competência | ✅ | Sim |
| Listar competências | ✅ | Sim |
| Obter competência por ID | ✅ | Sim |
| Exportar folha (externo) | 🔮 | Não (futuro) |
| Importar folha (externo) | 🔮 | Não (futuro) |
| Obter status de folha (externo) | 🔮 | Não (futuro) |

---

### 8. Analytics Context

| Capacidade | Status | Implementada? |
|---|---|---|
| Explicar domínio | ✅ | Sim |
| Análise de auditoria | ✅ | Sim |
| Timeline da instituição | ✅ | Sim |
| Definições de relatórios | ✅ | Sim |
| KPI de cobertura | ✅ | Sim |
| KPI financeiro | ✅ | Sim |
| KPI de payroll | ✅ | Sim |
| KPI operacional | ✅ | Sim |

---

## Resumo por Status

| Status | Quantidade | Porcentagem |
|---|---|---|
| ✅ Implementado | 45 | 80% |
| 🔮 Futuro | 11 | 20% |
| **Total** | **56** | **100%** |

---

## Capacidades Futuras (Sprint 11+)

| Capacidade | Contexto | Prioridade |
|---|---|---|
| Sincronizar médicos | Doctor | Alta |
| Validar CRM | Doctor | Alta |
| Exportar agenda | Shift | Média |
| Importar agenda | Shift | Média |
| Exportar dados financeiros | Financial | Média |
| Importar dados financeiros | Financial | Média |
| Obter status de pagamento | Financial | Média |
| Exportar folha | Payroll | Alta |
| Importar folha | Payroll | Alta |
| Obter status de folha | Payroll | Alta |

---

## Validação

| Critério | Status |
|---|---|
| Todas as capacidades documentadas | ✅ |
| Status de implementação definido | ✅ |
| Capacidades futuras priorizadas | ✅ |
| Resumo calculado | ✅ |
