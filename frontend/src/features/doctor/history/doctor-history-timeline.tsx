/**
 * DoctorHistoryTimeline — Plantão 360
 *
 * Timeline de histórico do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { EntityTimeline, TimelineEvent } from '../../../shared/components/entity-timeline';

// ============================================================
// Types
// ============================================================

interface DoctorHistoryTimelineProps {
  events: TimelineEvent[];
}

// ============================================================
// Component
// ============================================================

export function DoctorHistoryTimeline({ events }: DoctorHistoryTimelineProps) {
  return (
    <Paper variant="outlined" sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h6" fontWeight={600}>
          Histórico
        </Typography>
        <Typography variant="body2" color="text.secondary">
          ({events.length} eventos)
        </Typography>
      </Box>
      <EntityTimeline events={events} emptyMessage="Nenhum evento registrado" />
    </Paper>
  );
}
