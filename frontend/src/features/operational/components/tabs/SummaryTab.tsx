import React from 'react';
import { Box, Typography, Paper, LinearProgress } from '@mui/material';
import {
  EventNote as EventNoteIcon,
  AccessTime as AccessTimeIcon,
  People as PeopleIcon,
  HealthAndSafety as HealthIcon,
} from '@mui/icons-material';
import { SHIFT_TYPES, SHIFT_LABELS, SHIFT_TIMES, MONTH_NAMES } from '../../types/operational-types';
import type { WorkspaceSummary, DayData, DoctorOption } from '../../types/operational-types';

interface SummaryTabProps {
  summary: WorkspaceSummary;
  days: DayData[];
  doctors: DoctorOption[];
}

interface KpiCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  color: string;
}

function KpiCard({ icon, label, value, color }: KpiCardProps) {
  return (
    <Paper variant="outlined" sx={{ p: 2, flex: 1, minWidth: 160 }}>
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        {icon}
        <Typography variant="caption" color="text.secondary" fontSize="0.75rem">
          {label}
        </Typography>
      </Box>
      <Typography variant="h5" fontWeight={700} color={color}>
        {value}
      </Typography>
    </Paper>
  );
}

export function SummaryTab({ summary, days, doctors }: SummaryTabProps) {
  const shiftDistribution = SHIFT_TYPES.map((st) => {
    let count = 0;
    days.forEach((day) => {
      count += day.shifts[st]?.assignments.length || 0;
    });
    return { type: st, label: SHIFT_LABELS[st], count, hours: count * SHIFT_TIMES[st].hours };
  });

  const totalAssigned = shiftDistribution.reduce((sum, s) => sum + s.count, 0);

  return (
    <Box sx={{ p: 3, overflow: 'auto', flex: 1 }}>
      <Typography variant="h6" fontWeight={700} mb={3}>
        Resumo da Competência
      </Typography>

      <Box display="flex" gap={2} mb={4}>
        <KpiCard
          icon={<HealthIcon sx={{ fontSize: 18, color: summary.coverage_rate >= 90 ? '#00B87A' : '#FFB020' }} />}
          label="Cobertura"
          value={`${summary.coverage_rate}%`}
          color={summary.coverage_rate >= 90 ? '#00B87A' : '#FFB020'}
        />
        <KpiCard
          icon={<EventNoteIcon sx={{ fontSize: 18, color: '#6B7280' }} />}
          label="Turnos Atribuídos"
          value={`${summary.filled_shifts}/${summary.total_shifts}`}
          color="#1F2937"
        />
        <KpiCard
          icon={<AccessTimeIcon sx={{ fontSize: 18, color: '#6B7280' }} />}
          label="Horas Totais"
          value={`${summary.total_hours}h`}
          color="#1F2937"
        />
        <KpiCard
          icon={<PeopleIcon sx={{ fontSize: 18, color: '#6B7280' }} />}
          label="Médicos Ativos"
          value={summary.total_doctors}
          color="#1F2937"
        />
      </Box>

      <Typography variant="subtitle1" fontWeight={600} mb={2}>
        Distribuição por Turno
      </Typography>
      <Box display="flex" flexDirection="column" gap={1.5}>
        {shiftDistribution.map((s) => {
          const pct = totalAssigned > 0 ? Math.round((s.count / totalAssigned) * 100) : 0;
          return (
            <Paper key={s.type} variant="outlined" sx={{ p: 1.5 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
                <Typography variant="body2" fontWeight={500} fontSize="0.8125rem">
                  {s.label}
                </Typography>
                <Typography variant="caption" color="text.secondary" fontSize="0.75rem">
                  {s.count} atribuições · {s.hours}h
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={pct}
                sx={{
                  height: 4,
                  borderRadius: 2,
                  bgcolor: '#F3F4F6',
                  '& .MuiLinearProgress-bar': { bgcolor: '#00995D', borderRadius: 2 },
                }}
              />
            </Paper>
          );
        })}
      </Box>
    </Box>
  );
}
