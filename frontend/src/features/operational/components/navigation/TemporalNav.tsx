import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { NavigateBefore as PrevIcon, NavigateNext as NextIcon } from '@mui/icons-material';
import { IconButton } from '@mui/material';
import type { PeriodInfo } from '../../types/operational-types';
import { MONTH_NAMES, getCompetencyLabel } from '../../types/operational-types';

interface TemporalNavProps {
  period: PeriodInfo;
  onNavigate: (offset: number) => void;
}

export function TemporalNav({ period, onNavigate }: TemporalNavProps) {
  const label = `${MONTH_NAMES[period.month - 1]} ${period.year}`;

  return (
    <Box display="flex" alignItems="center" gap={1}>
      <IconButton size="small" onClick={() => onNavigate(-1)}>
        <PrevIcon fontSize="small" />
      </IconButton>
      <Box textAlign="center">
        <Typography variant="body2" fontWeight={600} fontSize="0.875rem">
          {label}
        </Typography>
        <Typography variant="caption" color="text.secondary" fontSize="0.6875rem">
          {getCompetencyLabel(period.year, period.month)}
        </Typography>
      </Box>
      <IconButton size="small" onClick={() => onNavigate(1)}>
        <NextIcon fontSize="small" />
      </IconButton>
    </Box>
  );
}
