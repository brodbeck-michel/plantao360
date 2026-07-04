/**
 * App Providers — Plantão 360
 *
 * Composição de todos os providers da aplicação.
 *
 * PROVIDER ORDER (mandatory — changes require ADR):
 * ─────────────────────────────────────────────────
 * 1. ThemeProvider      — MUI theme (design tokens). Must be first.
 * 2. QueryProvider      — React Query (cache, staleTime, retry).
 * 3. ToastProvider      — Centralized notifications (depends on MUI for Alert).
 * 4. FeedbackProvider   — Unified feedback (toast + confirm + dialog).
 * 5. BrowserRouter      — Routing (rendered in main.tsx, not here).
 *
 * Sprint: 14 — Operational MVP
 * Sprint: 15 — FeedbackProvider integration
 */

import React from 'react';
import { QueryProvider } from './query-provider';
import { ThemeProvider } from './theme-provider';
import { ToastProvider } from '../shared/providers/toast-provider';
import { FeedbackProvider } from '../shared/providers/FeedbackProvider';

// ============================================================
// Provider Composition
// ============================================================

interface AppProvidersProps {
  children: React.ReactNode;
}

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <ThemeProvider>
      <QueryProvider>
        <ToastProvider>
          <FeedbackProvider>
            {children}
          </FeedbackProvider>
        </ToastProvider>
      </QueryProvider>
    </ThemeProvider>
  );
}
