# Doctor Feature Review — Sprint 13

**Date:** 2026-06-27
**Status:** ✅ Audit Complete

---

## 1. Componentes Duplicados?

**Não.** Os componentes existentes são:
- `DoctorAvatar` — Específico de Doctor (não reutilizável)
- `DoctorCard` — Específico de Doctor (pode ser generalizado depois)
- `StatusChip` — Shared (já existe, reutilizável)
- `KPICard` — Shared (já existe, reutilizável)
- `ConfirmDialog` — Shared (já existe, reutilizável)
- `EmptyState` — Shared (já existe, reutilizável)
- `PageHeader` — Shared (já existe, reutilizável)

**Ação:** Manter DoctorAvatar e DoctorCard dentro da feature. StatusChip, KPICard, ConfirmDialog, EmptyState, PageHeader já estão em shared.

---

## 2. APIs Não Utilizadas?

**Não.** O `doctor-api.ts` expõe:
- `doctorQueries.list()` — Usado por useDoctorList
- `doctorQueries.detail()` — Usado por useDoctorDetail
- `doctorQueries.summary()` — Não usado ainda
- `doctorMutations.create()` — Usado por useCreateDoctor
- `doctorMutations.update()` — Usado por useUpdateDoctor
- `doctorMutations.delete()` — Usado por useDeleteDoctor

**Ação:** `doctorQueries.summary()` será usado pela DoctorProfileDrawer.

---

## 3. Endpoints Sem Interface?

**Sim.** Faltam:
- `GET /doctors/{id}/history` — Histórico de mudanças
- `GET /doctors/{id}/audit` — Auditoria
- `PATCH /doctors/{id}/deactivate` — Desativação

**Ação:** Adicionar ao doctor-api.ts.

---

## 4. Informação Desnecessária?

**Não.** Todos os tipos e funções são necessários.

---

## 5. Informação Faltando?

**Sim.** Faltam:
- Tipos para histórico e auditoria
- Hooks para histórico e auditoria
- Páginas (List, Detail, Create, Edit, History, Audit)
- Componentes de tabela, filtros, diálogos
- Form Engine
- Table Engine
- Filter Engine

**Ação:** Criar todas as ETAPAs 1-17.

---

## Conclusão

A feature Doctor está no estágio inicial (Sprint 12). Para se tornar o Golden Frontend Module, precisa de:
- Estrutura completa (ETAPA 1)
- 7 páginas (ETAPA 2)
- 10+ componentes (ETAPA 4)
- 9 hooks (ETAPA 5)
- Form Engine (ETAPA 6)
- Table Engine (ETAPA 7)
- Filter Engine (ETAPA 8)
- 6 diálogos (ETAPA 9)
- Error Experience (ETAPA 10)
- Accessibility (ETAPA 11)
- Responsiveness (ETAPA 12)
- Performance (ETAPA 13)
- Testes (ETAPA 14)
- Documentação (ETAPA 15)
- Review (ETAPA 16)
- ADR-027 (ETAPA 17)
