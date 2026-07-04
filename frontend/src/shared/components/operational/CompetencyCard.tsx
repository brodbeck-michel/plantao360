/**
 * CompetencyCard — Plantão 360
 *
 * Card da competência atual com status, período, progresso.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Card, CardContent, Typography, Stack, LinearProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { CalendarMonth } from '@mui/icons-material';
import { tokens } from '../../../theme';
import { OperationalLevel, getOperationalStatus } from '../../constants/status-colors';

// ============================================================
// Props
// ============================================================

interface CompetencyCardProps {
  name: string;
  level: OperationalLevel;
  startDate: string;
  endDate: string;
  progress?: number;
  route?: string;
}

// ============================================================
// Component
// ============================================================

export function CompetencyCard({
  name,
  level,
  startDate,
  endDate,
  progress,
  route = '/app/periods',
}: CompetencyCardProps) {
  const navigate = useNavigate();
  const status = getOperationalStatus(level);

  return (
    <Card
      onClick={() => navigate(route)}
      role="button"
      tabIndex={0}
      aria-label={`Competência ${name}. Período: ${startDate} a ${endDate}. Clique para ver detalhes.`}
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
        <Stack direction="row" alignItems="center" spacing={0.75}>
          <CalendarMonth sx={{ fontSize: 18, color: tokens.colors.text.secondary }} />
          <Typography
            variant="caption"
            sx={{ color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}
          >
            COMPETÊNCIA
          </Typography>
        </Stack>

        <Typography sx={{ fontSize: '1.5rem', fontWeight: 700, color: tokens.colors.text.primary, mt: 0.5 }}>
          {name}
        </Typography>

        <Typography variant="caption" sx={{ color: tokens.colors.text.muted, display: 'block', mt: 0.5 }}>
          {startDate} — {endDate}
        </Typography>

        {progress !== undefined && (
          <LinearProgress
            variant="determinate"
            value={progress}
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
        )}

        <Box
          sx={{
            mt: 1,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 0.5,
            px: 1,
            py: 0.25,
            borderRadius: tokens.borderRadius.sm,
            bgcolor: `${status.color}15`,
            border: `1px solid ${status.color}30`,
          }}
        >
          <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: status.color }} />
          <Typography variant="caption" sx={{ fontWeight: 600, color: status.color }}>
            {status.label}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}
