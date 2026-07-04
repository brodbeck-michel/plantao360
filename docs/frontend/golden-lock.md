# Frontend Golden Lock — Plantão 360

**Date:** 2026-06-27
**Status:** ✅ LOCKED

---

## Visão Geral

O Frontend Golden Lock congela oficialmente todos os padrões arquiteturais do Frontend. Nenhuma Feature poderá criar novos padrões. Toda evolução deverá ocorrer através da Plataforma.

---

## Padrões Congelados

### 1. Feature Structure
```
features/[feature]/
├── api/              # (reservado)
├── components/       # Componentes reutilizáveis da feature
├── dialogs/          # Diálogos de ação
├── details/          # Painéis de detalhes
├── filters/          # Filtros reutilizáveis
├── forms/            # Formulários
├── hooks/            # Hooks de negócio
├── history/          # Timeline de histórico
├── audit/            # Card de auditoria
├── pages/            # Páginas completas
├── services/         # API e mutations
├── tables/           # Tabelas
├── types/            # Tipos
├── utils/            # Utilitários
├── manifest/         # Manifest da feature
├── tests/            # Testes
└── index.ts          # Barrel file
```

### 2. Pages
- ListPage — Listagem com filtros, tabela, paginação
- DetailPage — Detalhes com tabs
- HistoryPage — Timeline de histórico
- AuditPage — Card de auditoria

### 3. Components
- EntityAvatar — Avatar genérico
- StatusChip — Badge de status
- KPICard — Card de KPI
- ConfirmDialog — Diálogo de confirmação
- EmptyState — Estado vazio
- PageHeader — Cabeçalho de página
- LoadingSpinner — Loading indicator
- ErrorBoundary — Error boundary
- DataTable — Tabela genérica
- FilterBar — Filtros genéricos
- ActionsMenu — Menu de ações
- EntityTimeline — Timeline genérica
- DomainExplanationPanel — Explicação de domínio

### 4. Hooks
- Query: useEntityList, useEntityDetail, useEntitySummary
- Mutation: useCreateEntity, useUpdateEntity, useDeleteEntity
- State: useEntityFilters, useEntitySort, useEntityPagination, useEntitySelection

### 5. API Layer
- apiClient com interceptors
- Query factories
- Mutation factories
- Error mapper
- barrel files

### 6. Dialog Pattern
- Create, Edit, Delete, Deactivate
- ConfirmDialog para ações destrutivas
- Loading state
- Error handling
- Success feedback

### 7. Table Pattern
- DataTable genérico
- Column definition pattern
- Sorting, pagination, selection
- Loading, empty, error states

### 8. Filter Pattern
- FilterBar genérico
- FilterField definition pattern
- Search, select, date, boolean
- Active count, clear filters

### 9. Form Pattern
- React Hook Form
- Controller pattern
- Validation rules centralizadas
- Loading, error, dirty state

### 10. Routing
- ROUTES constants
- NAV_ITEMS constants
- PermissionGuard
- Lazy loading

### 11. Accessibility
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- Contrast adequado

### 12. UX
- Empty states explicativos
- Loading states claros
- Error states com retry
- Success feedback
- Confirmation dialogs

---

## Processo de Evolução

### Para alterar um padrão:
1. Criar ADR documentando a mudança
2. Atualizar Golden Module (Doctor)
3. Atualizar Templates
4. Atualizar Validators
5. Atualizar Documentação
6. Só então implementar

### Para criar nova feature:
1. Usar Feature Generator
2. Seguir Templates
3. Criar Manifest
4. Rodar Validators
5. Aprovar Review

---

## Referências

- `features/doctor/` — Golden Frontend Module
- `shared/components/` — Componentes reutilizáveis
- `docs/frontend/entity-page-blueprint.md`
- `docs/adr/ADR-027-golden-frontend-module.md`
