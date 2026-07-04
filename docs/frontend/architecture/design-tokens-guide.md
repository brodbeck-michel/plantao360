# Design Tokens Guide — Plantão 360

**Sprint:** 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
**Data:** 2026-06-27

---

## Estrutura de Tokens

### Colors
```typescript
const colors = {
  primary: {
    50: '#E3F2FD',
    100: '#BBDEFB',
    200: '#90CAF9',
    300: '#64B5F6',
    400: '#42A5F5',
    500: '#1565C0',  // Primary
    600: '#1565C0',
    700: '#1565C0',
    800: '#1565C0',
    900: '#1565C0',
  },
  success: '#2E7D32',
  warning: '#F57F17',
  error: '#C62828',
  info: '#0288D1',
  background: {
    default: '#FFFFFF',
    paper: '#FAFAFA',
  },
  text: {
    primary: '#212121',
    secondary: '#757575',
  },
};
```

### Spacing
```typescript
const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  xxl: '48px',
};
```

### Border Radius
```typescript
const borderRadius = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  full: '9999px',
};
```

### Elevation
```typescript
const elevation = {
  sm: '0 1px 2px rgba(0,0,0,0.05)',
  md: '0 4px 6px rgba(0,0,0,0.1)',
  lg: '0 10px 15px rgba(0,0,0,0.1)',
  xl: '0 20px 25px rgba(0,0,0,0.15)',
};
```

### Typography
```typescript
const typography = {
  fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  h1: { fontSize: '2.5rem', fontWeight: 700 },
  h2: { fontSize: '2rem', fontWeight: 600 },
  h3: { fontSize: '1.5rem', fontWeight: 600 },
  body1: { fontSize: '1rem', fontWeight: 400 },
  body2: { fontSize: '0.875rem', fontWeight: 400 },
  caption: { fontSize: '0.75rem', fontWeight: 400 },
};
```

### Breakpoints
```typescript
const breakpoints = {
  xs: '0px',
  sm: '600px',
  md: '960px',
  lg: '1280px',
  xl: '1920px',
};
```

---

## Uso

### Theme
```typescript
import { theme } from 'src/theme';

// MUI component
<Box sx={{ p: theme.spacing.md }}>
  <Typography color={theme.colors.primary[500]}>
    Text
  </Typography>
</Box>
```

### MUI Theme
```typescript
import { createTheme } from '@mui/material/styles';
import { theme } from 'src/theme';

const muiTheme = createTheme({
  palette: {
    primary: { main: theme.colors.primary[500] },
    success: { main: theme.colors.success },
    warning: { main: theme.colors.warning },
    error: { main: theme.colors.error },
    info: { main: theme.colors.info },
  },
  typography: {
    fontFamily: theme.typography.fontFamily,
  },
});
```

---

## Referências

- `frontend/src/theme/index.ts`
- `docs/frontend/design-system-functional.md`
