# Component Guidelines — Plantão 360

**Sprint:** 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
**Data:** 2026-06-27

---

## Estrutura de Componentes

### Component Structure
```typescript
/**
 * [Component Name] — Plantão 360
 *
 * [Descrição]
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
// External imports

// ============================================================
// Types
// ============================================================

interface ComponentProps {
  // Props
}

// ============================================================
// Helpers (if needed)
// ============================================================

function helperFunction() {
  // Pure functions
}

// ============================================================
// Component
// ============================================================

export function ComponentName({ prop1, prop2 }: ComponentProps) {
  // Hooks
  // Handlers
  // Render
  return (
    // JSX
  );
}
```

---

## Regras

### Naming
- **Component:** PascalCase (`DoctorCard`)
- **File:** kebab-case (`doctor-card.tsx`)
- **Props interface:** `ComponentNameProps` (`DoctorCardProps`)

### Imports
1. React (if needed)
2. External libraries (MUI, React Router, etc.)
3. Internal shared components
4. Types
5. Hooks

### Structure
1. Types interface
2. Helpers (pure functions)
3. Component

### Exports
- Named exports only
- Barrel file (`index.ts`) for public API

### Accessibility
- Use semantic HTML
- Include `aria-label` for interactive elements
- Support keyboard navigation
- Maintain focus management

### Performance
- Use `React.memo` for expensive renders
- Avoid inline objects/functions in JSX
- Use `useMemo` for expensive computations
- Use `useCallback` for event handlers passed to children

---

## Common Components

| Component | Description | Location |
|---|---|---|
| StatusChip | Status badge | `shared/components/` |
| KPICard | KPI metric card | `shared/components/` |
| ConfirmDialog | Confirmation modal | `shared/components/` |
| EmptyState | Empty state placeholder | `shared/components/` |
| PageHeader | Page header with title | `shared/components/` |
| LoadingSpinner | Loading indicator | `shared/components/` |
| ErrorBoundary | Error boundary wrapper | `shared/components/` |

---

## References

- `docs/frontend/design-system-functional.md`
- `docs/frontend/ux-rules.md`
- `frontend/src/shared/components/`
