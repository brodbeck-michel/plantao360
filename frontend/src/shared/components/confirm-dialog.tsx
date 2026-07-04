/**
 * ConfirmDialog Component — Plantão 360
 *
 * Diálogo de confirmação para ações destrutivas.
 * Segue UX-002 (confirmação de ações destrutivas) e UX-020 (ConfirmDialog).
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from '@mui/material';

// ============================================================
// Types
// ============================================================

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  severity?: 'warning' | 'error';
  onConfirm: () => void;
  onCancel: () => void;
  loading?: boolean;
}

// ============================================================
// Component
// ============================================================

export function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = 'Confirmar',
  cancelLabel = 'Cancelar',
  severity = 'warning',
  onConfirm,
  onCancel,
  loading = false,
}: ConfirmDialogProps) {
  return (
    <Dialog open={open} onClose={onCancel} maxWidth="sm" fullWidth>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{message}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onCancel} disabled={loading}>
          {cancelLabel}
        </Button>
        <Button
          onClick={onConfirm}
          color={severity === 'error' ? 'error' : 'warning'}
          variant="contained"
          disabled={loading}
        >
          {confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
