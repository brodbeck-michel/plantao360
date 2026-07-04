import React, { useState } from 'react';
import { Box, Typography, Paper, LinearProgress, Badge, Tabs, Tab } from '@mui/material';
import {
  People as PeopleIcon,
  EventNote as EventNoteIcon,
  AccessTime as AccessTimeIcon,
  HealthAndSafety as HealthIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
  History as HistoryIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import { HistoryPanel } from '../workspace/HistoryPanel';
import type { WorkspaceSummary } from '../../types/operational-types';
import type { HistoryAction } from '../../hooks/use-undo-redo';

interface ConflictItem {
  doctorName: string;
  date: string;
  shiftType: string;
}

interface CoverageSidebarProps {
  summary: WorkspaceSummary;
  conflicts?: ConflictItem[];
  pastActions?: HistoryAction[];
  futureActions?: HistoryAction[];
  onUndoAction?: (actionId: string) => void;
  onRedoAction?: (actionId: string) => void;
  saveStatus?: 'saved' | 'saving' | 'error' | 'idle';
  lastSaveTime?: string;
}

export function CoverageSidebar({
  summary,
  conflicts = [],
  pastActions = [],
  futureActions = [],
  onUndoAction,
  onRedoAction,
  saveStatus,
  lastSaveTime,
}: CoverageSidebarProps) {
  const [sidebarTab, setSidebarTab] = useState(0);
  const coverageColor = summary.coverage_rate >= 90 ? '#00B87A' : summary.coverage_rate >= 50 ? '#FFB020' : '#FF4842';

  return (
    <Paper
      variant="outlined"
      sx={{
        width: 260,
        minWidth: 260,
        display: 'flex',
        flexDirection: 'column',
        borderRadius: '8px',
        overflow: 'hidden',
      }}
    >
      <Tabs
        value={sidebarTab}
        onChange={(_, v) => setSidebarTab(v)}
        variant="fullWidth"
        sx={{
          minHeight: 36,
          borderBottom: '1px solid #E5E7EB',
          '& .MuiTab-root': { minHeight: 36, py: 0, fontSize: '0.75rem', fontWeight: 600 },
        }}
      >
        <Tab icon={<SpeedIcon sx={{ fontSize: 14 }} />} iconPosition="start" label="Resumo" />
        <Tab
          icon={
            <Badge
              badgeContent={pastActions.length + futureActions.length}
              color="info"
              sx={{ '& .MuiBadge-badge': { fontSize: '0.5625rem', height: 14, minWidth: 14 } }}
            >
              <HistoryIcon sx={{ fontSize: 14 }} />
            </Badge>
          }
          iconPosition="start"
          label="Histórico"
        />
      </Tabs>

      {sidebarTab === 0 && (
        <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 2, flex: 1 }}>
          <Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
              <Box display="flex" alignItems="center" gap={0.5}>
                <HealthIcon sx={{ fontSize: 14, color: coverageColor }} />
                <Typography variant="caption" fontWeight={600} fontSize="0.75rem">
                  Cobertura
                </Typography>
              </Box>
              <Typography variant="caption" fontWeight={700} fontSize="0.8125rem" color={coverageColor}>
                {summary.coverage_rate}%
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={summary.coverage_rate}
              sx={{
                height: 6,
                borderRadius: 3,
                bgcolor: '#F3F4F6',
                '& .MuiLinearProgress-bar': {
                  bgcolor: coverageColor,
                  borderRadius: 3,
                },
              }}
            />
          </Box>

          <Box display="flex" alignItems="center" gap={1}>
            <EventNoteIcon sx={{ fontSize: 16, color: '#6B7280' }} />
            <Box>
              <Typography variant="caption" display="block" color="text.secondary" fontSize="0.6875rem">
                Turnos
              </Typography>
              <Typography variant="body2" fontWeight={600} fontSize="0.8125rem">
                {summary.filled_shifts}/{summary.total_shifts}
              </Typography>
            </Box>
          </Box>

          <Box display="flex" alignItems="center" gap={1}>
            <AccessTimeIcon sx={{ fontSize: 16, color: '#6B7280' }} />
            <Box>
              <Typography variant="caption" display="block" color="text.secondary" fontSize="0.6875rem">
                Horas
              </Typography>
              <Typography variant="body2" fontWeight={600} fontSize="0.8125rem">
                {summary.total_hours}h
              </Typography>
            </Box>
          </Box>

          <Box display="flex" alignItems="center" gap={1}>
            <PeopleIcon sx={{ fontSize: 16, color: '#6B7280' }} />
            <Box>
              <Typography variant="caption" display="block" color="text.secondary" fontSize="0.6875rem">
                Médicos Ativos
              </Typography>
              <Typography variant="body2" fontWeight={600} fontSize="0.8125rem">
                {summary.total_doctors}
              </Typography>
            </Box>
          </Box>

          {conflicts.length > 0 && (
            <Box display="flex" alignItems="center" gap={1}>
              <Badge badgeContent={conflicts.length} color="warning" sx={{ '& .MuiBadge-badge': { fontSize: '0.625rem' } }}>
                <WarningIcon sx={{ fontSize: 16, color: '#FFB020' }} />
              </Badge>
              <Box>
                <Typography variant="caption" display="block" color="text.secondary" fontSize="0.6875rem">
                  Conflitos
                </Typography>
                <Typography variant="body2" fontWeight={600} fontSize="0.8125rem" color="#FFB020">
                  {conflicts.length} pendente{conflicts.length > 1 ? 's' : ''}
                </Typography>
              </Box>
            </Box>
          )}

          {saveStatus && (
            <Box sx={{ mt: 'auto', pt: 1, borderTop: '1px solid #E5E7EB' }}>
              <Box display="flex" alignItems="center" gap={0.5}>
                <ScheduleIcon sx={{ fontSize: 12, color: '#9CA3AF' }} />
                <Typography variant="caption" color="text.secondary" fontSize="0.6875rem">
                  {saveStatus === 'saving' ? 'Salvando...' : saveStatus === 'saved' ? `Salvo ${lastSaveTime || ''}` : 'Erro ao salvar'}
                </Typography>
              </Box>
            </Box>
          )}
        </Box>
      )}

      {sidebarTab === 1 && (
        <HistoryPanel
          pastActions={pastActions}
          futureActions={futureActions}
          onUndo={onUndoAction || (() => {})}
          onRedo={onRedoAction || (() => {})}
        />
      )}
    </Paper>
  );
}
