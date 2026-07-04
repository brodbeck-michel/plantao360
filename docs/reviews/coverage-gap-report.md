# Coverage Gap Report

**Sprint:** 9
**Data:** 2026-06-26
**Atualizado por:** Sprint 9 — Payroll Aggregate & Competência Financeira

---

## Diagnóstico Atual

**Cobertura Total:** 74.53% (meta: ≥80%)
**Cobertura Sprint 8:** 75.76%
**Evolução:** -1.23 pontos (novo código de domínio adicionado sem cobertura equivalente)

---

## Módulos com Menor Cobertura

| Módulo | Cobertura | Linhas Faltantes | Prioridade |
|---|---|---|---|
| `use_cases/assignments/` | 0% | 376 | Alta |
| `repositories/interfaces/` | 0% | 66 | Média |
| `services/base/` | 0% | 10 | Média |
| `use_cases/base/` | 41% | 18 | Média |
| `domain/overlap/overlap_detector.py` | 57% | 9 | Baixa |
| `validators/shift_validator.py` | 56% | 12 | Baixa |
| `repositories/shift_part_repository.py` | 50% | 20 | Média |
| `services/extra_service.py` | 68% | 29 | Média |

---

## Progresso da Sprint 9

### Novos Testes Adicionados (74)
- `test_payroll_status.py` — 9 testes (constantes de status)
- `test_payroll_state_machine.py` — 17 testes (transições, validações, reabertura)
- `test_payroll_competency.py` — 25 testes (domínio, versões, selo, explicação, auditoria)
- `test_payroll_errors.py` — 12 testes (códigos de erro)
- `test_payroll_events.py` — 11 testes (eventos, versionamento)

### Cobertura dos Novos Módulos
- `domain/payroll/` — ~95% (todos os componentes testados)
- `domain/constants/payroll_status.py` — 100%
- `domain/state_machines/payroll_state_machine.py` — 100%
- `domain/errors/payroll_errors.py` — 100%
- `services/payroll_service.py` — ~70% (caminhos principais testados)
- `repositories/payroll_repository.py` — ~60% (CRUD básico testado)

---

## Análise da Queda de Cobertura

A cobertura caiu de 75.76% para 74.53% porque:
1. **Novo código de domínio** (~500 linhas) foi adicionado
2. **Testes focados** em domínio puro (74 testes unitários)
3. **Código de infraestrutura** (service, repository, API) não testado com cobertura equivalente
4. **Gap existente** (use_cases/assignments/ = 0%) permanece

---

## Plano para Atingir ≥80%

### Prioridade Alta (Sprint 10)
1. **Criar testes para use_cases/assignments/** — 10 arquivos, ~376 linhas
   - Testar cada use case individualmente com mocks
   - Foco: happy path + error paths
   - Esforço estimado: 2-3 horas

### Prioridade Média (Sprint 10)
2. **Testar services/payroll_service.py** — CRUD + transições
   - Mockar repository, testar lógica de serviço
   - Esforço estimado: 30 min

3. **Testar services/extra_service.py** — métodos approve/reject/cancel
   - Mockar repository, testar lógica de estado
   - Esforço estimado: 30 min

4. **Testar repositories/shift_part_repository.py** — find_overlapping
   - Usar SQLite em memória
   - Esforço estimado: 30 min

5. **Testar use_cases/base/** — base_use_case.py
   - Testar template method
   - Esforço estimado: 20 min

### Prioridade Baixa (Sprint 10+)
6. Testar `domain/overlap/overlap_detector.py`
7. Testar `validators/shift_validator.py`
8. Testar `repositories/interfaces/`

---

## Projeção

| Ação | Linhas Cobertas | Nova Cobertura |
|---|---|---|
| Testar use_cases/assignments/ | +376 | ~82% |
| Testar services/payroll_service.py | +120 | ~77% |
| Testar services/extra_service.py | +29 | ~75% |
| **Combinado** | **+525** | **~85%** |

**Conclusão:** Cobrir apenas os use_cases/assignments/ (prioridade alta) já eleva a cobertura para ~82%, atingindo a meta.

---

## Resumo de Testes por Sprint

| Sprint | Testes Adicionados | Total | Cobertura |
|---|---|---|---|
| Sprint 0-5 | 465 | 465 | N/A |
| Sprint 6 | 37 | 502 | 75% |
| Sprint 7 | 40 | 542 | 75% |
| Sprint 8 | 35 | 577 | 75.76% |
| Sprint 9 | 74 | 651 | 74.53% |
