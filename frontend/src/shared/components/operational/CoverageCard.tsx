/**
 * CoverageCard — Plantão 360
 *
 * Card de cobertura com barra de progresso visual e percentual.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Card, CardContent, Typography, Stack, LinearProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { tokens } from '../../../theme';
import { OperationalLevel, getOperationalStatus } from '../../constants/status-colors';

// ============================================================
// Props
// ============================================================

interface CoverageCardProps {
  percentage: number;
  level: OperationalLevel;
  coveredShifts: number;
  totalShifts: number;
  route?: string;
}

// ============================================================
// Component
// ============================================================

export function CoverageCard({
  percentage,
  level,
  coveredShifts,
  totalShifts,
  route = '/app/coverage',
}: CoverageCardProps) {
  const navigate = useNavigate();
  const status = getOperationalStatus(level);

  return (
    <Card
      onClick={() => navigate(route)}
      role="button"
      tabIndex={0}
      aria-label={`Cobertura: ${percentage}%. ${coveredShifts} de ${totalShifts} plantões cobertos. Clique para ver detalhes.`}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          navigate(route);
        }
      }}
      sx={{
        cursor: 'pointer',
        border: `1px solid ${status.border}`,
        borderBottom: `3px solid ${status.color}`,
        transition: 'all 200ms cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: tokens.elevation.md,
        },
        '&:active': { transform: 'translateY(0) scale(0.98)' },
        '&:focus-visible': {
          outline: `2px solid ${tokens.colors.primary.main}`,
          outlineOffset: '2px',
        },
      }}
    >
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <Typography
          variant="caption"
          sx={{ color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}
        >
          COBERTURA
        </Typography>

        <Stack direction="row" alignItems="baseline" spacing={1} sx={{ mt: 0.5 }}>
          <Typography
            sx={{ fontSize: '2rem', fontWeight: 700, color: status.color, fontVariantNumeric: 'tabular-nums' }}
          >
            {percentage}%
          </Typography>
          <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>
            {coveredShifts}/{totalShifts} plantões
          </Typography>
        </Stack>

        <LinearProgress
          variant="determinate"
          value={percentage}
          sx={{
            mt: 1.5,
            height: 6,
            borderRadius: 3,
            bgcolor: `${status.color}20`,
            '& .MuiLinearProgress-bar': {
              bgcolor: status.color,
              borderRadius: 3,
            },
          }}
        />
      </CardContent>
    </Card>
  );
}
