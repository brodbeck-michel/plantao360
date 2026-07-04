/**
 * ToastProvider — Plantão 360
 *
 * Centralized toast/snackbar notification system.
 * Provides consistent feedback across all modules.
 * Supports ErrorCode and DomainExplanation from backend.
 *
 * Sprint: 14 — Operational MVP
 */

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Snackbar, Alert, AlertColor, Box, Typography } from '@mui/material';
import { Info } from '@mui/icons-material';

// ============================================================
// Types — Backend Error Integration
// ============================================================

/** Backend ErrorCode pattern */
export interface ErrorCode {
  code: string;
  message: string;
  details?: unknown;
}

/** Backend DomainExplanation pattern */
export interface DomainExplanation {
  question: string;
  answer: string;
  entity_type: string;
  entity_id: number;
  steps?: Array<{
    order: number;
    description: string;
    value: unknown;
    formula?: string;
  }>;
}

/** Toast options for advanced usage */
export interface ToastOptions {
  duration?: number;
  errorCode?: ErrorCode;
  explanation?: DomainExplanation;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// ============================================================
// Types — Toast
// ============================================================

interface Toast {
  id: string;
  message: string;
  severity: AlertColor;
  duration?: number;
  errorCode?: ErrorCode;
  explanation?: DomainExplanation;
}

interface ToastContextValue {
  success: (message: string, options?: ToastOptions) => void;
  error: (message: string, options?: ToastOptions) => void;
  warning: (message: string, options?: ToastOptions) => void;
  info: (message: string, options?: ToastOptions) => void;
  /** Show a toast from an ErrorCode (auto-maps severity) */
  fromErrorCode: (error: ErrorCode, options?: ToastOptions) => void;
  /** Show a toast from a DomainExplanation */
  fromExplanation: (explanation: DomainExplanation, options?: ToastOptions) => void;
}

// ============================================================
// Context
// ============================================================

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

// ============================================================
// Helpers
// ============================================================

/** Map backend error codes to toast severity */
function getSeverityFromErrorCode(code: string): AlertColor {
  if (code.includes('NOT_FOUND')) return 'warning';
  if (code.includes('ALREADY_EXISTS') || code.includes('CONFLICT')) return 'warning';
  if (code.includes('VALIDATION') || code.includes('INVALID')) return 'error';
  if (code.includes('UNAUTHORIZED') || code.includes('FORBIDDEN')) return 'error';
  if (code.includes('IMMUTABLE')) return 'warning';
  return 'error';
}

/** Map backend error codes to user-friendly messages */
function getMessageFromErrorCode(error: ErrorCode): string {
  const messageMap: Record<string, string> = {
    DOCTOR_NOT_FOUND: 'Médico não encontrado',
    DOCTOR_ALREADY_EXISTS: 'Já existe um médico com este CRM',
    PERIOD_NOT_FOUND: 'Competência não encontrada',
    PERIOD_ALREADY_EXISTS: 'Já existe uma competência para este período',
    PERIOD_ALREADY_CLOSED: 'Esta competência já está fechada',
    PERIOD_IMMUTABLE: 'Esta competência não pode ser alterada',
    PERIOD_CANNOT_BE_REOPENED: 'Esta competência não pode ser reaberta',
    SHIFT_NOT_FOUND: 'Plantão não encontrado',
    SHIFT_ALREADY_EXISTS: 'Já existe um plantão para esta data e tipo',
    NETWORK_ERROR: 'Erro de conexão. Verifique sua internet.',
    HTTP_500: 'Erro interno do servidor. Contate o suporte.',
  };
  return messageMap[error.code] || error.message || 'Ocorreu um erro inesperado';
}

// ============================================================
// Provider
// ============================================================

interface ToastProviderProps {
  children: ReactNode;
  defaultDuration?: number;
  maxToasts?: number;
}

export function ToastProvider({
  children,
  defaultDuration = 4000,
  maxToasts = 3,
}: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback(
    (message: string, severity: AlertColor, options?: ToastOptions) => {
      const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
      const newToast: Toast = {
        id,
        message,
        severity,
        duration: options?.duration ?? defaultDuration,
        errorCode: options?.errorCode,
        explanation: options?.explanation,
      };

      setToasts((prev) => {
        const updated = [...prev, newToast];
        if (updated.length > maxToasts) {
          return updated.slice(-maxToasts);
        }
        return updated;
      });
    },
    [defaultDuration, maxToasts]
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const contextValue: ToastContextValue = {
    success: (message, options) => addToast(message, 'success', options),
    error: (message, options) => addToast(message, 'error', options),
    warning: (message, options) => addToast(message, 'warning', options),
    info: (message, options) => addToast(message, 'info', options),

    fromErrorCode: (error, options) => {
      const severity = getSeverityFromErrorCode(error.code);
      const message = getMessageFromErrorCode(error);
      addToast(message, severity, { ...options, errorCode: error });
    },

    fromExplanation: (explanation, options) => {
      const message = explanation.answer || explanation.question;
      addToast(message, 'info', { ...options, explanation });
    },
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      {toasts.map((toast, index) => (
        <Snackbar
          key={toast.id}
          open
          autoHideDuration={toast.duration}
          onClose={() => removeToast(toast.id)}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          sx={{ bottom: `${(index * 70) + 24}px !important` }}
        >
          <Alert
            onClose={() => removeToast(toast.id)}
            severity={toast.severity}
            variant="filled"
            sx={{ width: '100%', minWidth: 300, maxWidth: 500 }}
          >
            <Typography variant="body2" fontWeight={500}>
              {toast.message}
            </Typography>
            {toast.errorCode && (
              <Typography variant="caption" sx={{ opacity: 0.85, display: 'block', mt: 0.5 }}>
                Código: {toast.errorCode.code}
              </Typography>
            )}
            {toast.explanation && (
              <Box sx={{ mt: 1, p: 1, bgcolor: 'rgba(255,255,255,0.15)', borderRadius: 1 }}>
                <Box display="flex" alignItems="center" gap={0.5} mb={0.5}>
                  <Info fontSize="small" />
                  <Typography variant="caption" fontWeight={600}>
                    Explicação do Domínio
                  </Typography>
                </Box>
                <Typography variant="caption" display="block">
                  {toast.explanation.answer}
                </Typography>
              </Box>
            )}
          </Alert>
        </Snackbar>
      ))}
    </ToastContext.Provider>
  );
}

// ============================================================
// Hook
// ============================================================

/**
 * Hook to access the toast notification system.
 *
 * Usage:
 * ```tsx
 * const toast = useToast();
 *
 * // Simple
 * toast.success('Plantão criado com sucesso');
 *
 * // With ErrorCode
 * toast.fromErrorCode({ code: 'PERIOD_ALREADY_EXISTS', message: '...' });
 *
 * // With DomainExplanation
 * toast.fromExplanation({ question: '...', answer: '...', entity_type: 'period', entity_id: 1 });
 * ```
 */
export function useToast(): ToastContextValue {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}
