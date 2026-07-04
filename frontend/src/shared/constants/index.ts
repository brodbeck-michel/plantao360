/**
 * Shared Constants — Plantão 360
 *
 * Barrel export for all shared constants.
 *
 * Sprint: 14 — Operational MVP
 */

export {
  ENTITY_ICONS,
  EVENT_ICONS,
  EVENT_COLORS,
  ACTION_ICONS,
  TREND_ICONS,
  NAV_ICONS,
  ALL_ICONS,
} from './icons';

export {
  STATUS_COLORS,
  STATUS_LABELS,
  STATUS_BG_COLORS,
  getStatusColor,
  getStatusLabel,
  getStatusBgColor,
  getShiftStatusColor,
} from './status-colors';

export type {
  DoctorStatus,
  PeriodStatus,
  ShiftStatus,
  AssignmentStatus,
  ExtraStatus,
  CoverageStatus,
  PayrollStatus,
  HealthCardStatus,
  AlertSeverity,
} from './status-colors';
