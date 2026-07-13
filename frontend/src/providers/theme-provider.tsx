/**
 * Theme Provider — Plantão 360
 *
 * Provider do MUI Theme para toda a aplicação.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React, { useMemo } from 'react';
import { ThemeProvider as MuiThemeProvider, CssBaseline } from '@mui/material';
import { getTheme } from '../theme';
import { ColorModeProvider, useColorMode } from '../contexts/ColorModeContext';

// ============================================================
// Provider Component
// ============================================================

interface ThemeProviderProps {
  children: React.ReactNode;
}

function MuiThemeBridge({ children }: { children: React.ReactNode }) {
  const { mode } = useColorMode();
  const theme = useMemo(() => getTheme(mode), [mode]);

  return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </MuiThemeProvider>
  );
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  return (
    <ColorModeProvider>
      <MuiThemeBridge>{children}</MuiThemeBridge>
    </ColorModeProvider>
  );
}
