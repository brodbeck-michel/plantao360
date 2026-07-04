/**
 * KPICard Component — Plantão 360
 *
 * Componente para exibir KPIs no dashboard.
 * Segue UX-005 (indicadores explicáveis) e Design System (KPICard).
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'flat';
  trendValue?: string;
  icon?: React.ReactNode;
  onClick?: () => void;
}

// ============================================================
// Component
// ============================================================

export function KPICard({
  title,
  value,
  subtitle,
  trend,
  trendValue,
  icon,
  onClick,
}: KPICardProps) {
  const trendIcon = {
    up: <TrendingUp color="success" fontSize="small" />,
    down: <TrendingDown color="error" fontSize="small" />,
    flat: <TrendingFlat color="action" fontSize="small" />,
  };

  return (
    <Card
      onClick={onClick}
      sx={{
        cursor: onClick ? 'pointer' : 'default',
        '&:hover': onClick ? { boxShadow: 2 } : {},
        height: '100%',
      }}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" component="div" fontWeight={600}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
            {trend && trendValue && (
              <Box display="flex" alignItems="center" gap={0.5} mt={1}>
                {trendIcon[trend]}
                <Typography variant="caption" color={trend === 'up' ? 'success.main' : trend === 'down' ? 'error.main' : 'text.secondary'}>
                  {trendValue}
                </Typography>
              </Box>
            )}
          </Box>
          {icon && (
            <Box color="primary.main"Clone>
              {icon}
            </Box>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}
