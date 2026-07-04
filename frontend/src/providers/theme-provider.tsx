/**
 * Theme Provider — Plantão 360
 *
 * Provider do MUI Theme para toda a aplicação.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { ThemeProvider as MuiThemeProvider, CssBaseline } from '@mui/material';
import { theme } from '../theme';

// ============================================================
// Provider Component
// ============================================================

interface ThemeProviderProps {
  children: React.ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </MuiThemeProvider>
  );
}
