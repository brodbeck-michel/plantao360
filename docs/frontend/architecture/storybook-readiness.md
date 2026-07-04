# Storybook Readiness — Plantão 360

**Sprint:** 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
**Data:** 2026-06-27

---

## Status: ✅ Pronto para instalação (decisão adiada)

---

## Estrutura Necessária

### Diretórios
```
.storybook/
├── main.ts
├── preview.ts
├── manager.ts
└── preview-head.html
```

### Componentes Story
Cada componente compartilhado deve ter um arquivo `.stories.tsx`:

```
src/shared/components/
├── status-chip/
│   ├── status-chip.tsx
│   └── status-chip.stories.tsx
├── kpi-card/
│   ├── kpi-card.tsx
│   └── kpi-card.stories.tsx
└── ...
```

---

## Convenções de Story

### Naming
- Arquivo: `[component-name].stories.tsx`
- Default export: `ComponentName`
- Named exports: `Primary`, `Secondary`, `Disabled`, `Loading`, `Error`

### Estrutura
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { StatusChip } from './status-chip';

const meta: Meta<typeof StatusChip> = {
  title: 'Shared/StatusChip',
  component: StatusChip,
  tags: ['autodocs'],
  argTypes: {
    status: {
      control: 'select',
      options: ['active', 'inactive', 'pending', 'approved', 'rejected', 'completed', 'in-progress'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof StatusChip>;

export const Primary: Story = {
  args: {
    status: 'active',
  },
};
```

---

## Decision Points

| Feature | Decision | Status |
|---|---|---|
| Storybook Installation | Adiado | ⏳ |
| Storybook Addons | Adiado | ⏳ |
| Storybook Theme | Adiado | ⏳ |
| Visual Testing | Adiado | ⏳ |

---

## References

- `docs/frontend/design-system-functional.md`
- `docs/frontend/screen-inventory.md`
