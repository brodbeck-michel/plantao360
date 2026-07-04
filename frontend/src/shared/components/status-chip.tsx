/**
 * StatusChip Component — Plantão 360
 *
 * Componente para exibir status com cores consistentes.
 * Consome tokens visuais de shared/constants/status-colors.
 * Segue UX-006 (consistência visual) e Design System (indicadores).
 *
 * Sprint: 14 — Operational MVP
 */

import React from 'react';
import { Chip, ChipProps } from '@mui/material';
import { STATUS_COLORS, STATUS_LABELS, getShiftStatusColor } from '../constants/status-colors';

// ============================================================
// Types
// ============================================================

type StatusType =
  | 'active' | 'inactive'
  | 'draft' | 'closed' | 'paid'
  | 'scheduled' | 'in_progress' | 'completed' | 'cancelled'
  | 'planned' | 'confirmed' | 'started'
  | 'pending' | 'approved' | 'rejected'
  | 'calculated' | 'reviewed' | 'exported' | 'archived'
  | 'healthy' | 'warning' | 'critical' | 'info' | 'default';

const SHIFT_STATUSES = new Set(['draft', 'scheduled', 'in_progress', 'completed', 'cancelled']);

interface StatusChipProps extends Omit<ChipProps, 'color' | 'label'> {
  status: StatusType;
  label?: string;
}

// ============================================================
// Component
// ============================================================

/**
 * StatusChip — displays a status with consistent color and label.
 *
 * Uses centralized STATUS_COLORS and STATUS_LABELS from shared/constants.
 * Components should NEVER use raw colors — always consume via StatusChip.
 *
 * @example
 * <StatusChip status="active" />
 * <StatusChip status="draft" label="Rascunho" />
 * <StatusChip status="completed" variant="outlined" />
 */
export function StatusChip({ status, label, ...props }: StatusChipProps) {
  const isShift = SHIFT_STATUSES.has(status);

  if (isShift) {
    return (
      <Chip
        label={label || STATUS_LABELS[status] || status}
        size="small"
        sx={{
          backgroundColor: getShiftStatusColor(status),
          color: '#fff',
          fontWeight: 600,
        }}
        {...props}
      />
    );
  }

  return (
    <Chip
      color={STATUS_COLORS[status] || 'default'}
      label={label || STATUS_LABELS[status] || status}
      size="small"
      {...props}
    />
  );
}
