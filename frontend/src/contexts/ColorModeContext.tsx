/**
 * ColorModeContext — Plantão 360
 *
 * Estado do modo de tema (claro/escuro), com persistência em localStorage
 * e fallback para a preferência do sistema operacional.
 */

import React, { createContext, useCallback, useContext, useMemo, useState } from 'react';
import type { ColorMode } from '../theme';

const STORAGE_KEY = 'color_mode';

function getInitialMode(): ColorMode {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === 'light' || stored === 'dark') return stored;
  if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) return 'dark';
  return 'light';
}

interface ColorModeContextValue {
  mode: ColorMode;
  toggleColorMode: () => void;
}

const ColorModeContext = createContext<ColorModeContextValue | undefined>(undefined);

export function ColorModeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = useState<ColorMode>(getInitialMode);

  const toggleColorMode = useCallback(() => {
    setMode((prev) => {
      const next = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem(STORAGE_KEY, next);
      return next;
    });
  }, []);

  const value = useMemo(() => ({ mode, toggleColorMode }), [mode, toggleColorMode]);

  return <ColorModeContext.Provider value={value}>{children}</ColorModeContext.Provider>;
}

export function useColorMode() {
  const ctx = useContext(ColorModeContext);
  if (!ctx) throw new Error('useColorMode deve ser usado dentro de ColorModeProvider');
  return ctx;
}
