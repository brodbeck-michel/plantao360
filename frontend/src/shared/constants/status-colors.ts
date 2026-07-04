/**
 * Status Colors — Plantão 360
 *
 * Unified status → color mapping.
 * Single source of truth for all modules.
 *
 * Sprint: 14 — Operational MVP
 */

import { ChipProps } from '@mui/material';

// ============================================================
// Status Types
// ============================================================

export type DoctorStatus = 'active' | 'inactive';
export type PeriodStatus = 'draft' | 'closed' | 'paid';
export type ShiftStatus = 'draft' | 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
export type AssignmentStatus = 'planned' | 'confirmed' | 'started' | 'completed' | 'cancelled';
export type ExtraStatus = 'pending' | 'approved' | 'rejected' | 'cancelled';
export type CoverageStatus = 'pending' | 'approved' | 'rejected';
export type PayrollStatus = 'draft' | 'calculated' | 'reviewed' | 'approved' | 'exported' | 'paid' | 'archived';
export type HealthCardStatus = 'healthy' | 'warning' | 'critical' | 'info' | 'default';
export type AlertSeverity = 'low' | 'medium' | 'high' | 'critical';

// ============================================================
// Status → Color Mapping
// ============================================================

export const STATUS_COLORS: Record<string, ChipProps['color']> = {
  // Doctor
  active: 'success',
  inactive: 'default',

  // Period
  closed: 'info',
  paid: 'success',

  // Shift
  draft: 'default',
  scheduled: 'warning',
  in_progress: 'success',
  completed: 'info',
  cancelled: 'error',

  // Assignment
  planned: 'default',
  confirmed: 'info',
  started: 'warning',

  // Extra
  pending: 'warning',
  approved: 'success',
  rejected: 'error',

  // Coverage
  // pending: 'warning', (already defined)
  // approved: 'success', (already defined)
  // rejected: 'error', (already defined)

  // Payroll
  calculated: 'info',
  reviewed: 'info',
  exported: 'success',
  archived: 'default',

  // Health Card
  healthy: 'success',
  // warning: 'warning', (already defined)
  critical: 'error',
  // info: 'info', (already defined)
  // default: 'default', (already defined)

  // Alert Severity
  low: 'info',
  medium: 'warning',
  // high: 'error', (already defined)
  // critical: 'error', (already defined)
};

// ============================================================
// Status → Label Mapping (Portuguese)
// ============================================================

export const STATUS_LABELS: Record<string, string> = {
  // Doctor
  active: 'Ativo',
  inactive: 'Inativo',

  // Period
  closed: 'Fechado',
  paid: 'Pago',

  // Shift
  draft: 'Rascunho',
  scheduled: 'Agendado',
  in_progress: 'Em Andamento',
  completed: 'Concluído',
  cancelled: 'Cancelado',

  // Assignment
  planned: 'Planejado',
  confirmed: 'Confirmado',
  started: 'Iniciado',

  // Extra
  pending: 'Pendente',
  approved: 'Aprovado',
  rejected: 'Rejeitado',

  // Payroll
  calculated: 'Calculado',
  reviewed: 'Revisado',
  exported: 'Exportado',
  archived: 'Arquivado',

  // Health Card
  healthy: 'Saudável',
  warning: 'Atenção',
  critical: 'Crítico',
  info: 'Informativo',
  default: 'Padrão',

  // Alert Severity
  low: 'Baixa',
  medium: 'Média',
  high: 'Alta',
  critical_severity: 'Crítica',
};

// ============================================================
// Status → Background Color (for badges)
// ============================================================

export const STATUS_BG_COLORS: Record<string, string> = {
  active: '#E8F5E9',
  inactive: '#F5F5F5',
  draft: '#F3F4F6',
  closed: '#E3F2FD',
  paid: '#E8F5E9',
  scheduled: '#FEF3C7',
  in_progress: '#D1FAE5',
  completed: '#DBEAFE',
  cancelled: '#FEE2E2',
  planned: '#F5F5F5',
  confirmed: '#E3F2FD',
  started: '#FFF3E0',
  pending: '#FFF3E0',
  approved: '#E8F5E9',
  rejected: '#FFEBEE',
  calculated: '#E3F2FD',
  reviewed: '#E3F2FD',
  exported: '#E8F5E9',
  archived: '#F5F5F5',
  healthy: '#E8F5E9',
  warning: '#FFF3E0',
  critical: '#FFEBEE',
  info: '#E3F2FD',
  default: '#F5F5F5',
};

// ============================================================
// Operational Status — 4-Level System (Sprint 15)
// ============================================================

export type OperationalLevel = 'healthy' | 'attention' | 'critical' | 'informative';

export const OPERATIONAL_STATUS: Record<OperationalLevel, {
  color: string;
  bg: string;
  border: string;
  label: string;
  icon: string;
}> = {
  healthy: {
    color: '#00B87A',
    bg: '#E6F7EF',
    border: '#A7F3D0',
    label: 'Saudável',
    icon: 'CheckCircle',
  },
  attention: {
    color: '#FFB020',
    bg: '#FFF8E1',
    border: '#FDE68A',
    label: 'Atenção',
    icon: 'Warning',
  },
  critical: {
    color: '#FF4842',
    bg: '#FFEBEE',
    border: '#FECACA',
    label: 'Crítico',
    icon: 'Error',
  },
  informative: {
    color: '#1B6FE0',
    bg: '#EFF6FF',
    border: '#BFDBFE',
    label: 'Informativo',
    icon: 'Info',
  },
};

/** Map domain statuses to operational levels */
export const STATUS_TO_OPERATIONAL: Record<string, OperationalLevel> = {
  // Doctor
  active: 'healthy',
  inactive: 'informative',
  // Period
  closed: 'healthy',
  paid: 'healthy',
  // Shift
  draft: 'informative',
  scheduled: 'attention',
  in_progress: 'healthy',
  completed: 'healthy',
  cancelled: 'critical',
  // Assignment
  planned: 'informative',
  confirmed: 'healthy',
  started: 'attention',
  // Extra
  pending: 'attention',
  approved: 'healthy',
  rejected: 'critical',
  // Payroll
  calculated: 'informative',
  reviewed: 'informative',
  exported: 'healthy',
  archived: 'informative',
  // Health Card
  healthy: 'healthy',
  warning: 'attention',
  critical: 'critical',
  info: 'informative',
  default: 'informative',
  // Alert Severity
  low: 'informative',
  medium: 'attention',
  high: 'critical',
  critical_severity: 'critical',
};

/**
 * Get the operational level for a domain status.
 */
export function getOperationalLevel(status: string): OperationalLevel {
  return STATUS_TO_OPERATIONAL[status] || 'informative';
}

/**
 * Get operational status display properties.
 */
export function getOperationalStatus(level: OperationalLevel) {
  return OPERATIONAL_STATUS[level];
}

// ============================================================
// Helpers
// ============================================================

/**
 * Get the color for a status.
 * @param status - The status string
 * @returns MUI ChipProps color
 */
export function getStatusColor(status: string): ChipProps['color'] {
  return STATUS_COLORS[status] || 'default';
}

/**
 * Get the label for a status.
 * @param status - The status string
 * @returns Portuguese label
 */
export function getStatusLabel(status: string): string {
  return STATUS_LABELS[status] || status;
}

/**
 * Get the background color for a status.
 * @param status - The status string
 * @returns CSS color string
 */
export function getStatusBgColor(status: string): string {
  return STATUS_BG_COLORS[status] || '#F5F5F5';
}

const SHIFT_STATUS_HEX: Record<string, string> = {
  draft: '#9CA3AF',
  scheduled: '#F59E0B',
  in_progress: '#10B981',
  completed: '#3B82F6',
  cancelled: '#EF4444',
};

/**
 * Get the hex color for a shift status.
 * @param status - The shift status string
 * @returns CSS hex color string
 */
export function getShiftStatusColor(status: string): string {
  return SHIFT_STATUS_HEX[status] || '#9CA3AF';
}
