/**
 * InstitutionStatusBar — Plantão 360
 *
 * Barra de status geral do hospital no topo do Dashboard.
 * Mostra: hospital, competência, cobertura, última atualização, estado operacional.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Stack, Typography, Chip, Tooltip } from '@mui/material';
import {
  LocalHospital,
  CalendarMonth,
  HealthAndSafety,
  Sync,
  Circle,
} from '@mui/icons-material';
import { tokens } from '../../../theme';

// ============================================================
// Props
// ============================================================

interface InstitutionStatusBarProps {
  hospital?: string;
  competency?: string;
  coverage?: number;
  lastSync?: string;
  operationalState: 'healthy' | 'attention' | 'critical';
}

// ============================================================
// Helpers
// ============================================================

const STATE_CONFIG = {
  healthy: { color: tokens.colors.operational.healthy, label: 'Operação Normal', bg: tokens.colors.operational.healthyBg },
  attention: { color: tokens.colors.operational.attention, label: 'Atenção', bg: tokens.colors.operational.attentionBg },
  critical: { color: tokens.colors.operational.critical, label: 'Crítico', bg: tokens.colors.operational.criticalBg },
};

// ============================================================
// Component
// ============================================================

export function InstitutionStatusBar({
  hospital = 'PS Unimed Tubarão',
  competency,
  coverage,
  lastSync,
  operationalState,
}: InstitutionStatusBarProps) {
  const stateConfig = STATE_CONFIG[operationalState];

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 2,
        flexWrap: 'wrap',
        p: 1.5,
        px: 2,
        borderRadius: tokens.borderRadius.lg,
        bgcolor: tokens.colors.background.paper,
        border: `1px solid ${stateConfig.color}30`,
        borderLeft: `4px solid ${stateConfig.color}`,
      }}
      role="status"
      aria-label={`Estado operacional: ${stateConfig.label}`}
    >
      {/* Hospital */}
      <Stack direction="row" alignItems="center" spacing={0.75}>
        <LocalHospital sx={{ fontSize: 18, color: tokens.colors.primary.main }} />
        <Typography variant="body2" sx={{ fontWeight: 600, color: tokens.colors.text.primary }}>
          {hospital}
        </Typography>
      </Stack>

      <Box sx={{ width: 1, height: 24, bgcolor: tokens.colors.grey[200], flexShrink: 0 }} />

      {/* Competency */}
      {competency && (
        <Stack direction="row" alignItems="center" spacing={0.75}>
          <CalendarMonth sx={{ fontSize: 16, color: tokens.colors.text.secondary }} />
          <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>
            Competência: <strong>{competency}</strong>
          </Typography>
        </Stack>
      )}

      {/* Coverage */}
      {coverage !== undefined && (
        <Stack direction="row" alignItems="center" spacing={0.75}>
          <HealthAndSafety sx={{ fontSize: 16, color: tokens.colors.text.secondary }} />
          <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>
            Cobertura: <strong>{coverage}%</strong>
          </Typography>
        </Stack>
      )}

      <Box sx={{ flex: 1 }} />

      {/* Last Sync */}
      {lastSync && (
        <Tooltip title="Última sincronização de dados">
          <Stack direction="row" alignItems="center" spacing={0.5}>
            <Sync sx={{ fontSize: 14, color: tokens.colors.text.muted }} />
            <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>
              {lastSync}
            </Typography>
          </Stack>
        </Tooltip>
      )}

      {/* Operational State */}
      <Chip
        icon={<Circle sx={{ fontSize: 10, color: `${stateConfig.color} !important` }} />}
        label={stateConfig.label}
        size="small"
        sx={{
          bgcolor: stateConfig.bg,
          color: stateConfig.color,
          fontWeight: 600,
          border: `1px solid ${stateConfig.color}30`,
          '& .MuiChip-icon': {
            color: stateConfig.color,
          },
        }}
      />
    </Box>
  );
}
