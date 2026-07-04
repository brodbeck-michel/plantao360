/**
 * AppToast — Plantão 360
 *
 * Toast padronizado com 4 variantes: success, error, warning, info.
 * Integra com o ToastProvider existente.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Snackbar, Alert, AlertColor, Typography, Box } from '@mui/material';
import { Info } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

export interface ToastConfig {
  id: string;
  message: string;
  severity: AlertColor;
  duration: number;
  errorCode?: string;
  explanation?: string;
  action?: { label: string; onClick: () => void };
  onClose: (id: string) => void;
}

// ============================================================
// Component
// ============================================================

export function AppToast({
  id,
  message,
  severity,
  duration,
  errorCode,
  explanation,
  action,
  onClose,
}: ToastConfig) {
  return (
    <Snackbar
      open
      autoHideDuration={duration}
      onClose={() => onClose(id)}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      sx={{ zIndex: 1400 }}
    >
      <Alert
        onClose={() => onClose(id)}
        severity={severity}
        variant="filled"
        action={action ? (
          <Typography
            variant="body2"
            sx={{ color: '#fff', fontWeight: 600, cursor: 'pointer', textDecoration: 'underline' }}
            onClick={action.onClick}
          >
            {action.label}
          </Typography>
        ) : undefined}
        sx={{
          width: '100%',
          minWidth: 300,
          maxWidth: 500,
          borderRadius: '12px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
        }}
      >
        <Typography variant="body2" fontWeight={500}>
          {message}
        </Typography>
        {errorCode && (
          <Typography variant="caption" sx={{ opacity: 0.85, display: 'block', mt: 0.5 }}>
            Código: {errorCode}
          </Typography>
        )}
        {explanation && (
          <Box sx={{ mt: 1, p: 1, bgcolor: 'rgba(255,255,255,0.15)', borderRadius: 1 }}>
            <Box display="flex" alignItems="center" gap={0.5} mb={0.5}>
              <Info fontSize="small" />
              <Typography variant="caption" fontWeight={600}>
                Explicação
              </Typography>
            </Box>
            <Typography variant="caption" display="block">
              {explanation}
            </Typography>
          </Box>
        )}
      </Alert>
    </Snackbar>
  );
}
