# ADR-027: Golden Frontend Module

**Date:** 2026-06-27
**Status:** Accepted
**Sprint:** 13

---

## Context

O Plantão 360 precisa de uma referência arquitetural obrigatória para todas as futuras features do Frontend. O módulo Doctor foi selecionado como Golden Frontend Module por ser a feature mais representativa do sistema.

---

## Decision

Declaramos o **Doctor Module** como o Golden Frontend Module com os seguintes padrões:

### 1. Feature Structure
```
features/[feature]/
├── components/     # Componentes reutilizáveis da feature
├── dialogs/        # Diálogos de ação
├── details/        # Painéis de detalhes
├── filters/        # Filtros reutilizáveis
├── forms/          # Formulários
├── hooks/          # Hooks de negócio
├── history/        # Timeline de histórico
├── audit/          # Card de auditoria
├── pages/          # Páginas completas
├── services/       # API e mutations
├── tables/         # Tabelas
├── types/          # Tipos
├── utils/          # Utilitários
├── manifest/       # Manifest da feature
├── tests/          # Testes
└── index.ts        # Barrel file
```

### 2. Shared Components
Componentes reutilizáveis ficam em `shared/components/`:
- EntityAvatar
- StatusChip
- ConfirmDialog
- EmptyState
- PageHeader
- LoadingSpinner
- ErrorBoundary
- DataTable
- FilterBar
- ActionsMenu
- EntityTimeline
- DomainExplanationPanel

### 3. Hook Pattern
- **Query Hooks:** `useEntityList`, `useEntityDetail`, `useEntitySummary`
- **Mutation Hooks:** `useCreateEntity`, `useUpdateEntity`, `useDeleteEntity`
- **State Hooks:** `useEntityFilters`, `useEntitySort`, `useEntityPagination`, `useEntitySelection`
- Nunca misturar leitura com mutação

### 4. Form Engine
- React Hook Form para validação
- Controller pattern
- Validation rules centralizadas
- Loading, error, dirty state
- Reset e submit padronizados

### 5. Table Engine
- DataTable genérico
- Column definition pattern
- Sorting, pagination, selection
- Loading, empty, error states
- Actions menu por linha

### 6. Filter Engine
- FilterBar genérico
- FilterField definition pattern
- Search, select, date, boolean
- Active count
- Clear filters

### 7. Dialog Pattern
- Create, Edit, Delete, Deactivate
- ConfirmDialog para ações destrutivas
- Loading state
- Error handling
- Success feedback

### 8. Error Experience
- DomainExplanation para erros de negócio
- Snackbar para feedback
- ErrorBoundary para erros de renderização

### 9. Accessibility
- ARIA labels em todos os elementos interativos
- Keyboard navigation
- Focus management
- Screen reader support
- Contrast adequate

### 10. Performance
- Lazy loading de páginas
- React Query com cache
- Memoização onde justificável
- Code splitting por feature

---

## Consequences

### Positivas
1. **Consistência** — Todas as features seguem mesmo padrão
2. **Velocidade** — Copiar e renomear para nova feature
3. **Manutenibilidade** — Mudanças em um padrão afetam todas as features
4. **Testabilidade** — Padrão definido para testes
5. **Acessibilidade** — Padrão definido para a11y

### Negativas
1. **Rigidez** — Pode não se adequar a features muito simples
2. **Boilerplate** — Mais arquivos por feature
3. **Curva de aprendizado** — Equipe precisa conhecer o padrão

---

## Implementation

### Arquivos Criados
- `features/doctor/` — Golden Frontend Module completo
- `shared/components/` — 12 componentes reutilizáveis
- `docs/frontend/entity-page-blueprint.md`
- `docs/frontend/doctor-frontend-guide.md`
- `docs/frontend/testing-guide.md`
- `docs/frontend/accessibility-guide.md`
- `docs/frontend/reviews/golden-module-review.md`

---

## References

- `features/doctor/` — Golden Frontend Module
- `shared/components/` — Componentes reutilizáveis
- `docs/frontend/entity-page-blueprint.md`
- `docs/frontend/doctor-frontend-guide.md`
- `docs/frontend/reviews/golden-module-review.md`
