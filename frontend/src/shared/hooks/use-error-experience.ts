/**
 * useErrorExperience — Plantão 360
 *
 * Hook para exibir erros e sucessos com notistack.
 * Reutilizável por todas as features.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import { useSnackbar } from 'notistack';
import type { AppError } from '../../api/client';

// ============================================================
// Types
// ============================================================

interface UseErrorExperienceReturn {
  showError: (error: unknown, fallbackMessage?: string) => void;
  showSuccess: (message: string) => void;
  showWarning: (message: string) => void;
  showInfo: (message: string) => void;
}

// ============================================================
// Hook
// ============================================================

export function useErrorExperience(): UseErrorExperienceReturn {
  const { enqueueSnackbar } = useSnackbar();

  const showError = (error: unknown, fallbackMessage?: string) => {
    const message = getErrorMessage(error, fallbackMessage);
    enqueueSnackbar(message, { variant: 'error' });
  };

  const showSuccess = (message: string) => {
    enqueueSnackbar(message, { variant: 'success' });
  };

  const showWarning = (message: string) => {
    enqueueSnackbar(message, { variant: 'warning' });
  };

  const showInfo = (message: string) => {
    enqueueSnackbar(message, { variant: 'info' });
  };

  return { showError, showSuccess, showWarning, showInfo };
}

// ============================================================
// Helpers
// ============================================================

function getErrorMessage(error: unknown, fallback?: string): string {
  if (error && typeof error === 'object' && 'message' in error) {
    return (error as AppError).message;
  }
  if (error && typeof error === 'object' && 'response' in error) {
    const axiosError = error as { response?: { data?: { message?: string } } };
    return axiosError.response?.data?.message || fallback || 'Erro inesperado. Tente novamente.';
  }
  return fallback || 'Erro inesperado. Tente novamente.';
}
