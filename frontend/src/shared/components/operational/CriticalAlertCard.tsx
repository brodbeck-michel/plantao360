/**
 * CriticalAlertCard — Plantão 360
 *
 * Card de alerta com severidade visual, ação rápida, pulsação.
 * Aparece apenas quando há alertas de severidade crítica.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Card, CardContent, Typography, Stack, Button } from '@mui/material';
import { Warning, Error, ArrowForward } from '@mui/icons-material';
import { tokens } from '../../../theme';

// ============================================================
// Types
// ============================================================

interface CriticalAlert {
  alert_id: string;
  title: string;
  description: string;
  severity: 'critical' | 'warning';
  action_label?: string;
  action_route?: string;
}

// ============================================================
// Props
// ============================================================

interface CriticalAlertCardProps {
  alerts: CriticalAlert[];
  onAction?: (route: string) => void;
}

// ============================================================
// Component
// ============================================================

export function CriticalAlertCard({ alerts, onAction }: CriticalAlertCardProps) {
  if (alerts.length === 0) return null;

  const criticalCount = alerts.filter((a) => a.severity === 'critical').length;

  return (
    <Card
      sx={{
        border: `1px solid ${tokens.colors.operational.criticalBorder}`,
        backgroundColor: tokens.colors.operational.criticalBg,
        animation: criticalCount > 0 ? 'pulseCritical 2s ease-in-out infinite' : 'none',
      }}
    >
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1.5 }}>
          <Error sx={{ color: tokens.colors.operational.critical, fontSize: 20 }} />
          <Typography variant="subtitle2" sx={{ fontWeight: 700, color: tokens.colors.operational.critical }}>
            ALERTAS CRÍTICOS ({alerts.length})
          </Typography>
        </Stack>

        <Stack spacing={1}>
          {alerts.map((alert) => (
            <Stack
              key={alert.alert_id}
              direction="row"
              alignItems="center"
              justifyContent="space-between"
              sx={{
                p: 1.5,
                borderRadius: tokens.borderRadius.md,
                bgcolor: alert.severity === 'critical' ? 'rgba(255,72,66,0.08)' : 'rgba(255,176,32,0.08)',
                border: `1px solid ${alert.severity === 'critical' ? tokens.colors.operational.criticalBorder : tokens.colors.operational.attentionBorder}`,
              }}
            >
              <Stack direction="row" alignItems="center" spacing={1} sx={{ minWidth: 0, flex: 1 }}>
                {alert.severity === 'critical' ? (
                  <Error sx={{ color: tokens.colors.operational.critical, fontSize: 18, flexShrink: 0 }} />
                ) : (
                  <Warning sx={{ color: tokens.colors.operational.attention, fontSize: 18, flexShrink: 0 }} />
                )}
                <Box sx={{ minWidth: 0 }}>
                  <Typography variant="body2" sx={{ fontWeight: 600, color: tokens.colors.text.primary }}>
                    {alert.title}
                  </Typography>
                  <Typography variant="caption" sx={{ color: tokens.colors.text.secondary }}>
                    {alert.description}
                  </Typography>
                </Box>
              </Stack>

              {alert.action_label && alert.action_route && (
                <Button
                  size="small"
                  endIcon={<ArrowForward sx={{ fontSize: '14px !important' }} />}
                  onClick={() => onAction?.(alert.action_route!)}
                  sx={{
                    color: alert.severity === 'critical' ? tokens.colors.operational.critical : tokens.colors.operational.attention,
                    fontWeight: 600,
                    fontSize: '0.75rem',
                    flexShrink: 0,
                    ml: 1,
                    '&:hover': {
                      bgcolor: alert.severity === 'critical' ? 'rgba(255,72,66,0.08)' : 'rgba(255,176,32,0.08)',
                    },
                  }}
                >
                  {alert.action_label}
                </Button>
              )}
            </Stack>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}
