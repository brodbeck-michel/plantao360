/**
 * useApi Hook — Plantão 360
 *
 * Hook para requisições API com loading, error e retry.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { useState, useCallback } from 'react';
import { apiClient, AppError, mapError } from '../api/client';

// ============================================================
// Types
// ============================================================

export interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: AppError | null;
}

export interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: any[]) => Promise<T | null>;
  reset: () => void;
}

// ============================================================
// Hook
// ============================================================

export function useApi<T>(
  apiFn: (...args: any[]) => Promise<T>
): UseApiReturn<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(
    async (...args: any[]): Promise<T | null> => {
      setState({ data: null, loading: true, error: null });
      try {
        const result = await apiFn(...args);
        setState({ data: result, loading: false, error: null });
        return result;
      } catch (error) {
        const appError = mapError(error as any);
        setState({ data: null, loading: false, error: appError });
        return null;
      }
    },
    [apiFn]
  );

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return { ...state, execute, reset };
}
