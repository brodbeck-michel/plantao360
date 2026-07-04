/**
 * OperationalHealthCard — Plantão 360
 *
 * Card de saúde operacional com progress ring, cor semântica, trend.
 * Clicável — navega para o módulo correspondente.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Card, CardContent, Typography, Stack, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { tokens } from '../../../theme';
import { OperationalLevel, getOperationalStatus } from '../../constants/status-colors';

// ============================================================
// Props
// ============================================================

interface OperationalHealthCardProps {
  title: string;
  value: string | number;
  level: OperationalLevel;
  trend?: 'up' | 'down' | 'flat';
  trendValue?: string;
  detail?: string;
  route: string;
  percentage?: number;
}

// ============================================================
// Component
// ============================================================

export function OperationalHealthCard({
  title,
  value,
  level,
  trend,
  trendValue,
  detail,
  route,
  percentage,
}: OperationalHealthCardProps) {
  const navigate = useNavigate();
  const status = getOperationalStatus(level);

  const trendIcon = trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→';
  const trendColor = trend === 'up' ? tokens.colors.operational.healthy
    : trend === 'down' ? tokens.colors.operational.critical
    : tokens.colors.text.secondary;

  return (
    <Card
      onClick={() => navigate(route)}
      role="button"
      tabIndex={0}
      aria-label={`${title}: ${value}. Clique para ver detalhes.`}
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
        '&:active': {
          transform: 'translateY(0px) scale(0.98)',
        },
        '&:focus-visible': {
          outline: `2px solid ${tokens.colors.primary.main}`,
          outlineOffset: '2px',
        },
      }}
    >
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography
              variant="caption"
              sx={{ color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}
            >
              {title}
            </Typography>
            <Typography
              variant="h4"
              sx={{
                fontSize: { xs: '1.75rem', sm: '2.25rem' },
                fontWeight: 700,
                color: tokens.colors.text.primary,
                mt: 0.5,
                fontVariantNumeric: 'tabular-nums',
              }}
            >
              {value}
            </Typography>
            {(trend || trendValue) && (
              <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                <Typography
                  variant="caption"
                  sx={{ color: trendColor, fontWeight: 700 }}
                >
                  {trendIcon} {trendValue}
                </Typography>
                {detail && (
                  <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>
                    {detail}
                  </Typography>
                )}
              </Stack>
            )}
          </Box>

          {percentage !== undefined && (
            <Box sx={{ position: 'relative', display: 'inline-flex', ml: 1.5 }}>
              <CircularProgress
                variant="determinate"
                value={percentage}
                size={56}
                thickness={4}
                sx={{
                  color: status.color,
                  '& .MuiCircularProgress-circle': {
                    strokeLinecap: 'round',
                  },
                }}
              />
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  bottom: 0,
                  right: 0,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Typography
                  variant="caption"
                  sx={{ fontWeight: 700, fontSize: '0.7rem', color: status.color }}
                >
                  {Math.round(percentage)}%
                </Typography>
              </Box>
            </Box>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}
