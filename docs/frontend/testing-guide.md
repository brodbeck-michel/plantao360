# Testing Guide — Plantão 360

**Sprint:** 13 — Golden Frontend Module
**Data:** 2026-06-27

---

## Estrutura de Testes

```
features/doctor/tests/
├── doctor-avatar.test.tsx        # Component test
├── doctor-card.test.tsx          # Component test
├── doctor-table.test.tsx         # Component test
├── doctor-form.test.tsx          # Component test
├── use-doctors.test.ts           # Hook test
├── doctor-api.test.ts            # Service test
├── doctor-list-page.test.tsx     # Page test
├── doctor-detail-page.test.tsx   # Page test
└── doctor-accessibility.test.tsx # A11y test
```

---

## Tipos de Testes

### 1. Component Tests
```tsx
import { render, screen } from '@testing-library/react';
import { DoctorCard } from '../components/doctor-card';

describe('DoctorCard', () => {
  it('renders doctor name', () => {
    render(<DoctorCard doctor={mockDoctor} />);
    expect(screen.getByText('Dr. João')).toBeInTheDocument();
  });
});
```

### 2. Hook Tests
```tsx
import { renderHook, act } from '@testing-library/react';
import { useDoctorFilters } from '../hooks/use-doctors';

describe('useDoctorFilters', () => {
  it('updates filter', () => {
    const { result } = renderHook(() => useDoctorFilters());
    act(() => {
      result.current.updateFilter({ name: 'João' });
    });
    expect(result.current.filters.name).toBe('João');
  });
});
```

### 3. Page Tests
```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { DoctorListPage } from '../pages/doctor-list-page';

describe('DoctorListPage', () => {
  it('renders list', async () => {
    render(<DoctorListPage />);
    await waitFor(() => {
      expect(screen.getByText('Médicos')).toBeInTheDocument();
    });
  });
});
```

### 4. Accessibility Tests
```tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { DoctorCard } from '../components/doctor-card';

expect.extend(toHaveNoViolations);

describe('DoctorCard a11y', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<DoctorCard doctor={mockDoctor} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});
```

### 5. Contract Tests
```tsx
import { doctorQueries } from '../services/doctor-api';

describe('Doctor API Contract', () => {
  it('list query returns correct shape', () => {
    const query = doctorQueries.list({});
    expect(query.queryKey).toEqual(['doctors', 'list', {}]);
  });
});
```

### 6. Snapshot Tests
```tsx
import { render } from '@testing-library/react';
import { DoctorCard } from '../components/doctor-card';

describe('DoctorCard', () => {
  it('matches snapshot', () => {
    const { container } = render(<DoctorCard doctor={mockDoctor} />);
    expect(container).toMatchSnapshot();
  });
});
```

---

## Commands

```bash
# Run all tests
npx vitest run

# Run specific test file
npx vitest run features/doctor/tests/doctor-card.test.tsx

# Run with coverage
npx vitest run --coverage

# Watch mode
npx vitest
```

---

## Referências

- `frontend/vitest.config.ts`
- `frontend/src/test/setup.ts`
