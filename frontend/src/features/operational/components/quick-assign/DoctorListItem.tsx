import React from 'react';
import { Box, Typography, Tooltip } from '@mui/material';
import type { DoctorOption } from '../../types/operational-types';

interface DoctorStats {
  totalShifts: number;
  totalHours: number;
  assignedToday: number;
}

interface DoctorListItemProps {
  doctor: DoctorOption;
  isAssigned: boolean;
  stats?: DoctorStats;
  onSelect: () => void;
}

function getStatusLabel(stats?: DoctorStats): { label: string; color: string } {
  if (!stats) return { label: 'Disponível', color: '#00995D' };
  if (stats.totalHours >= 240) return { label: 'Carga alta', color: '#FF4842' };
  if (stats.assignedToday > 0) return { label: 'Em outro turno', color: '#FFB020' };
  return { label: 'Disponível', color: '#00995D' };
}

export function DoctorListItem({ doctor, isAssigned, stats, onSelect }: DoctorListItemProps) {
  const status = getStatusLabel(stats);

  return (
    <Box
      onClick={onSelect}
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        px: 2,
        py: 1,
        cursor: 'pointer',
        transition: 'background-color 100ms',
        '&:hover': { bgcolor: '#F3F4F6' },
        ...(isAssigned && { bgcolor: '#E6F7EF' }),
      }}
    >
      <Box sx={{ flex: 1, minWidth: 0 }}>
        <Box display="flex" alignItems="center" gap={0.5}>
          <Typography
            variant="body2"
            fontWeight={isAssigned ? 600 : 400}
            fontSize="0.8125rem"
            noWrap
            sx={{ color: isAssigned ? '#065F46' : '#1F2937' }}
          >
            {doctor.name}
          </Typography>
          {isAssigned && (
            <Typography variant="caption" color="#00995D" fontWeight={600} fontSize="0.625rem" sx={{ ml: 0.5 }}>
              escalado
            </Typography>
          )}
        </Box>
        <Typography variant="caption" color="text.secondary" fontSize="0.6875rem">
          CRM {doctor.crm} · {doctor.specialty}
        </Typography>
        {stats && (
          <Box display="flex" gap={1} mt={0.25}>
            <Typography variant="caption" color="text.secondary" fontSize="0.625rem">
              {stats.totalShifts} plantões · {stats.totalHours.toFixed(0)}h
            </Typography>
            <Tooltip title={status.label} arrow>
              <Typography variant="caption" fontWeight={600} fontSize="0.625rem" color={status.color}>
                {status.label}
              </Typography>
            </Tooltip>
          </Box>
        )}
      </Box>
    </Box>
  );
}
