# Blueprint Library — Plantão 360

**Date:** 2026-06-27

---

## Visão Geral

Blueprints são padrões oficiais de páginas. Toda página deve seguir um Blueprint.

---

## Blueprints Oficiais

### 1. List Page
- PageHeader
- Toolbar (contador, criar, exportar)
- FilterBar (pesquisa, filtros)
- DataTable (colunas, ordenação, seleção, ações)
- Pagination
- Empty State
- Loading State
- Error State

### 2. Detail Page
- PageHeader (breadcrumb, título, ações)
- Tabs (Detalhes, Histórico, Auditoria)
- Details Panel
- History Timeline
- Audit Card

### 3. Form Page
- PageHeader
- Form (React Hook Form)
- Validation rules
- Loading state
- Error state
- Success feedback

### 4. Wizard
- Stepper
- Multiple steps
- Validation per step
- Back/Next/Submit

### 5. Dashboard
- KPI Cards
- Charts
- Alerts
- Quick actions

### 6. Settings
- Form sections
- Toggle switches
- Save button

### 7. Timeline
- EntityTimeline component
- Filters
- Pagination

### 8. Analytics
- Charts
- Filters
- Export

---

## Uso

Para criar uma nova página, copie o Blueprint correspondente:

```bash
# List Page
cp tools/templates/pages/list-page.tsx features/[feature]/pages/[feature]-list-page.tsx

# Detail Page
cp tools/templates/pages/detail-page.tsx features/[feature]/pages/[feature]-detail-page.tsx
```

---

## Referências

- `tools/templates/pages/`
- `docs/frontend/entity-page-blueprint.md`
