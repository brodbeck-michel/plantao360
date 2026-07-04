/**
 * AppConfirmation — Plantão 360
 *
 * Confirmação com explicação de impacto e severidade visual.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Typography, Stack, Button } from '@mui/material';
import { Warning, Error, Info } from '@mui/icons-material';
import { tokens } from '../../../theme';

// ============================================================
// Types
// ============================================================

interface AppConfirmationProps {
  open: boolean;
  title: string;
  message: string;
  severity?: 'warning' | 'error' | 'info';
  confirmLabel?: string;
  cancelLabel?: string;
  loading?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

// ============================================================
// Helpers
// ============================================================

const SEVERITY_CONFIG = {
  warning: { icon: Warning, color: tokens.colors.warning.main, bg: tokens.colors.warning.light + '40' },
  error: { icon: Error, color: tokens.colors.error.main, bg: tokens.colors.error.light + '40' },
  info: { icon: Info, color: tokens.colors.info.main, bg: tokens.colors.info.light + '40' },
};

// ============================================================
// Component
// ============================================================

export function AppConfirmation({
  open,
  title,
  message,
  severity = 'warning',
  confirmLabel = 'Confirmar',
  cancelLabel = 'Cancelar',
  loading = false,
  onConfirm,
  onCancel,
}: AppConfirmationProps) {
  const config = SEVERITY_CONFIG[severity];
  const Icon = config.icon;

  return (
    <Dialog
      open={open}
      onClose={onCancel}
      maxWidth="xs"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: tokens.borderRadius.lg,
          boxShadow: tokens.elevation.xl,
        },
      }}
    >
      <DialogContent sx={{ pt: 3 }}>
        <Stack alignItems="center" spacing={1.5}>
          <Stack
            alignItems="center"
            justifyContent="center"
            sx={{
              width: 56,
              height: 56,
              borderRadius: '50%',
              bgcolor: config.bg,
            }}
          >
            <Icon sx={{ color: config.color, fontSize: 28 }} />
          </Stack>
          <Typography variant="h6" sx={{ fontWeight: 600, textAlign: 'center' }}>
            {title}
          </Typography>
          <Typography variant="body2" sx={{ color: tokens.colors.text.secondary, textAlign: 'center' }}>
            {message}
          </Typography>
        </Stack>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 2.5, pt: 1.5, gap: 1, justifyContent: 'center' }}>
        <Button
          variant="outlined"
          onClick={onCancel}
          disabled={loading}
          sx={{
            borderColor: tokens.colors.grey[300],
            color: tokens.colors.text.secondary,
            fontWeight: 600,
          }}
        >
          {cancelLabel}
        </Button>
        <Button
          variant="contained"
          onClick={onConfirm}
          disabled={loading}
          sx={{
            bgcolor: config.color,
            color: '#fff',
            fontWeight: 600,
            '&:hover': { bgcolor: config.color, opacity: 0.9 },
          }}
        >
          {loading ? 'Processando...' : confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
