/**
 * OperationalStatusBadge — Plantão 360
 *
 * 4-level operational status badge: healthy, attention, critical, informative.
 * Single source of truth for all status displays.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Chip, ChipProps, Tooltip } from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error,
  Info,
} from '@mui/icons-material';
import {
  OperationalLevel,
  getOperationalStatus,
} from '../../constants/status-colors';

// ============================================================
// Props
// ============================================================

interface OperationalStatusBadgeProps {
  level: OperationalLevel;
  label?: string;
  size?: ChipProps['size'];
  showIcon?: boolean;
  tooltip?: string;
  sx?: ChipProps['sx'];
}

// ============================================================
// Icon Map
// ============================================================

const ICON_MAP: Record<OperationalLevel, React.ReactNode> = {
  healthy: <CheckCircle fontSize="small" />,
  attention: <Warning fontSize="small" />,
  critical: <Error fontSize="small" />,
  informative: <Info fontSize="small" />,
};

// ============================================================
// Component
// ============================================================

export function OperationalStatusBadge({
  level,
  label,
  size = 'small',
  showIcon = true,
  tooltip,
  sx,
}: OperationalStatusBadgeProps) {
  const status = getOperationalStatus(level);
  const displayLabel = label || status.label;

  const chip = (
    <Chip
      icon={showIcon ? ICON_MAP[level] as React.ReactElement : undefined}
      label={displayLabel}
      size={size}
      sx={{
        bgcolor: status.bg,
        color: status.color,
        border: `1px solid ${status.border}`,
        fontWeight: 600,
        '& .MuiChip-icon': {
          color: status.color,
        },
        ...sx,
      }}
      aria-label={`Status: ${displayLabel}`}
      role="status"
    />
  );

  if (tooltip) {
    return (
      <Tooltip title={tooltip} arrow>
        {chip}
      </Tooltip>
    );
  }

  return chip;
}
