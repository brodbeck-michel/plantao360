/**
 * UpcomingActionCard — Plantão 360
 *
 * Card de próxima ação com prioridade e botão de ação.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Card, CardContent, Typography, Stack, Button, Chip } from '@mui/material';
import { ArrowForward, Schedule } from '@mui/icons-material';
import { tokens } from '../../../theme';

// ============================================================
// Types
// ============================================================

interface UpcomingAction {
  action_id: string;
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  action_label?: string;
  action_route?: string;
}

// ============================================================
// Props
// ============================================================

interface UpcomingActionCardProps {
  actions: UpcomingAction[];
  onAction?: (route: string) => void;
}

// ============================================================
// Helpers
// ============================================================

const PRIORITY_CONFIG = {
  high: { color: tokens.colors.operational.critical, label: 'Urgente', bg: tokens.colors.operational.criticalBg },
  medium: { color: tokens.colors.operational.attention, label: 'Pendente', bg: tokens.colors.operational.attentionBg },
  low: { color: tokens.colors.informative, label: 'Baixa', bg: tokens.colors.informativeBg },
};

// ============================================================
// Component
// ============================================================

export function UpcomingActionCard({ actions, onAction }: UpcomingActionCardProps) {
  if (actions.length === 0) {
    return (
      <Card>
        <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
          <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1.5 }}>
            <Schedule sx={{ color: tokens.colors.text.secondary, fontSize: 20 }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 600, color: tokens.colors.text.secondary }}>
              PRÓXIMAS AÇÕES
            </Typography>
          </Stack>
          <Typography variant="body2" sx={{ color: tokens.colors.text.muted, textAlign: 'center', py: 2 }}>
            Nenhuma ação pendente
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1.5 }}>
          <Schedule sx={{ color: tokens.colors.primary.main, fontSize: 20 }} />
          <Typography variant="subtitle2" sx={{ fontWeight: 600, color: tokens.colors.text.primary }}>
            PRÓXIMAS AÇÕES
          </Typography>
        </Stack>

        <Stack spacing={1}>
          {actions.map((action) => {
            const config = PRIORITY_CONFIG[action.priority];
            return (
              <Stack
                key={action.action_id}
                direction="row"
                alignItems="center"
                justifyContent="space-between"
                sx={{
                  p: 1.5,
                  borderRadius: tokens.borderRadius.md,
                  bgcolor: config.bg,
                  border: `1px solid ${config.color}20`,
                }}
              >
                <Stack direction="row" alignItems="center" spacing={1} sx={{ minWidth: 0, flex: 1 }}>
                  <Chip
                    label={config.label}
                    size="small"
                    sx={{
                      bgcolor: config.color,
                      color: '#fff',
                      fontWeight: 600,
                      fontSize: '0.65rem',
                      height: 20,
                      flexShrink: 0,
                    }}
                  />
                  <Box sx={{ minWidth: 0 }}>
                    <Typography variant="body2" sx={{ fontWeight: 600, color: tokens.colors.text.primary }}>
                      {action.title}
                    </Typography>
                    {action.description && (
                      <Typography variant="caption" sx={{ color: tokens.colors.text.secondary }}>
                        {action.description}
                      </Typography>
                    )}
                  </Box>
                </Stack>

                {action.action_label && action.action_route && (
                  <Button
                    size="small"
                    endIcon={<ArrowForward sx={{ fontSize: '14px !important' }} />}
                    onClick={() => onAction?.(action.action_route!)}
                    sx={{
                      color: config.color,
                      fontWeight: 600,
                      fontSize: '0.75rem',
                      flexShrink: 0,
                      ml: 1,
                    }}
                  >
                    {action.action_label}
                  </Button>
                )}
              </Stack>
            );
          })}
        </Stack>
      </CardContent>
    </Card>
  );
}
