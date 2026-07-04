/**
 * AppDialog — Plantão 360
 *
 * Dialog genérico com estilos operacionais.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Typography,
  Stack,
} from '@mui/material';
import { Close } from '@mui/icons-material';
import { tokens } from '../../../theme';

// ============================================================
// Types
// ============================================================

interface AppDialogProps {
  open: boolean;
  title: string;
  subtitle?: string;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg';
  onClose: () => void;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

// ============================================================
// Component
// ============================================================

export function AppDialog({
  open,
  title,
  subtitle,
  maxWidth = 'sm',
  onClose,
  actions,
  children,
}: AppDialogProps) {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth={maxWidth}
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: tokens.borderRadius.lg,
          boxShadow: tokens.elevation.xl,
        },
      }}
    >
      <DialogTitle sx={{ pb: subtitle ? 1 : 2, pr: 6 }}>
        <Stack>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="body2" sx={{ color: tokens.colors.text.secondary, mt: 0.5 }}>
              {subtitle}
            </Typography>
          )}
        </Stack>
        <IconButton
          onClick={onClose}
          size="small"
          aria-label="Fechar"
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: tokens.colors.text.muted,
          }}
        >
          <Close fontSize="small" />
        </IconButton>
      </DialogTitle>

      <DialogContent sx={{ pt: 0 }}>{children}</DialogContent>

      {actions && (
        <DialogActions sx={{ px: 3, pb: 2.5, pt: 1.5, gap: 1 }}>{actions}</DialogActions>
      )}
    </Dialog>
  );
}
