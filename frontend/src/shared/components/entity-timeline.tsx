/**
 * EntityTimeline — Plantão 360
 *
 * Timeline genérica para histórico de mudanças.
 * Reutilizável por qualquer feature.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Typography, Box, Stack } from '@mui/material';

// ============================================================
// Types
// ============================================================

export interface TimelineEvent {
  id: string;
  date: string;
  title: string;
  description?: string;
  user?: string;
  type?: 'create' | 'update' | 'delete' | 'status' | 'system';
}

interface EntityTimelineProps {
  events: TimelineEvent[];
  emptyMessage?: string;
}

// ============================================================
// Helpers
// ============================================================

const typeColorMap: Record<string, 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info' | 'grey'> = {
  create: 'success',
  update: 'info',
  delete: 'error',
  status: 'warning',
  system: 'grey',
};

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// ============================================================
// Component
// ============================================================

export function EntityTimeline({ events, emptyMessage = 'Nenhum evento registrado' }: EntityTimelineProps) {
  if (events.length === 0) {
    return (
      <Box py={4} textAlign="center">
        <Typography variant="body2" color="text.secondary">
          {emptyMessage}
        </Typography>
      </Box>
    );
  }

  return (
    <Stack spacing={2} pl={1}>
      {events.map((event) => (
        <Box key={event.id} display="flex" gap={2}>
          <Box
            sx={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              bgcolor: `${typeColorMap[event.type || 'system']}.main`,
              mt: 0.5,
              flexShrink: 0,
            }}
          />
          <Box>
            <Typography variant="subtitle2" fontWeight={600}>
              {event.title}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {formatDate(event.date)}
              {event.user && ` — ${event.user}`}
            </Typography>
            {event.description && (
              <Typography variant="body2" color="text.secondary" mt={0.5}>
                {event.description}
              </Typography>
            )}
          </Box>
        </Box>
      ))}
    </Stack>
  );
}
