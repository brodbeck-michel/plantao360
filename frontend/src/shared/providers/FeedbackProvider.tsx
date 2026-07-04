/**
 * FeedbackProvider — Plantão 360
 *
 * Provider centralizado com hook useFeedback().
 * Integrates with existing ToastProvider.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { AppToast, ToastConfig } from '../components/feedback/AppToast';
import { AppConfirmation } from '../components/feedback/AppConfirmation';

// ============================================================
// Types
// ============================================================

interface ConfirmOptions {
  title: string;
  message: string;
  severity?: 'warning' | 'error' | 'info';
  confirmLabel?: string;
  cancelLabel?: string;
}

interface FeedbackContextValue {
  toast: {
    success: (message: string, options?: { duration?: number; explanation?: string }) => void;
    error: (message: string, options?: { duration?: number; errorCode?: string }) => void;
    warning: (message: string, options?: { duration?: number }) => void;
    info: (message: string, options?: { duration?: number }) => void;
  };
  confirm: (options: ConfirmOptions) => Promise<boolean>;
  dismissToast: (id: string) => void;
}

// ============================================================
// Context
// ============================================================

const FeedbackContext = createContext<FeedbackContextValue | undefined>(undefined);

// ============================================================
// Provider
// ============================================================

interface FeedbackProviderProps {
  children: ReactNode;
  defaultDuration?: number;
  maxToasts?: number;
}

export function FeedbackProvider({
  children,
  defaultDuration = 4000,
  maxToasts = 3,
}: FeedbackProviderProps) {
  const [toasts, setToasts] = useState<ToastConfig[]>([]);
  const [confirmState, setConfirmState] = useState<{
    open: boolean;
    options: ConfirmOptions;
    resolve: (value: boolean) => void;
  } | null>(null);

  const addToast = useCallback(
    (message: string, severity: ToastConfig['severity'], options?: Partial<ToastConfig>) => {
      const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
      const toast: ToastConfig = {
        id,
        message,
        severity,
        duration: options?.duration ?? defaultDuration,
        errorCode: options?.errorCode,
        explanation: options?.explanation,
        action: options?.action,
        onClose: () => {},
      };

      setToasts((prev) => {
        const updated = [...prev, toast];
        return updated.length > maxToasts ? updated.slice(-maxToasts) : updated;
      });
    },
    [defaultDuration, maxToasts]
  );

  const dismissToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const confirm = useCallback((options: ConfirmOptions): Promise<boolean> => {
    return new Promise((resolve) => {
      setConfirmState({ open: true, options, resolve });
    });
  }, []);

  const handleConfirmClose = useCallback((value: boolean) => {
    confirmState?.resolve(value);
    setConfirmState(null);
  }, [confirmState]);

  const contextValue: FeedbackContextValue = {
    toast: {
      success: (msg, opts) => addToast(msg, 'success', opts),
      error: (msg, opts) => addToast(msg, 'error', { duration: Infinity, ...opts }),
      warning: (msg, opts) => addToast(msg, 'warning', opts),
      info: (msg, opts) => addToast(msg, 'info', opts),
    },
    confirm,
    dismissToast,
  };

  return (
    <FeedbackContext.Provider value={contextValue}>
      {children}

      {/* Toasts */}
      {toasts.map((toast) => (
        <AppToast key={toast.id} {...toast} onClose={dismissToast} />
      ))}

      {/* Confirmation Dialog */}
      {confirmState && (
        <AppConfirmation
          open={confirmState.open}
          title={confirmState.options.title}
          message={confirmState.options.message}
          severity={confirmState.options.severity}
          confirmLabel={confirmState.options.confirmLabel}
          cancelLabel={confirmState.options.cancelLabel}
          onConfirm={() => handleConfirmClose(true)}
          onCancel={() => handleConfirmClose(false)}
        />
      )}
    </FeedbackContext.Provider>
  );
}

// ============================================================
// Hook
// ============================================================

export function useFeedback(): FeedbackContextValue {
  const context = useContext(FeedbackContext);
  if (!context) {
    throw new Error('useFeedback must be used within a FeedbackProvider');
  }
  return context;
}
