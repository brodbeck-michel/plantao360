import React from 'react';
import { Box, Typography } from '@mui/material';
import { SHIFT_TYPES, SHIFT_LABELS, SHIFT_TIMES } from '../../types/operational-types';

export function GridHeader() {
  return (
    <Box component="tr" sx={{ bgcolor: '#F3F4F6', borderBottom: '2px solid #E5E7EB' }}>
      <Box
        component="th"
        sx={{
          p: 1.5,
          textAlign: 'left',
          fontWeight: 600,
          fontSize: '0.8125rem',
          color: '#374151',
          width: 140,
          minWidth: 140,
          position: 'sticky',
          left: 0,
          top: 0,
          bgcolor: '#F3F4F6',
          zIndex: 3,
        }}
      >
        DATA
      </Box>
      {SHIFT_TYPES.map((st) => (
        <Box
          component="th"
          key={st}
          sx={{
            p: 1,
            textAlign: 'center',
            fontWeight: 600,
            fontSize: '0.75rem',
            color: '#374151',
            minWidth: 180,
            width: 180,
            position: 'sticky',
            top: 0,
            bgcolor: '#F3F4F6',
            zIndex: 2,
          }}
        >
          <Typography variant="caption" fontWeight={700} display="block" fontSize="0.8125rem">
            {SHIFT_LABELS[st]}
          </Typography>
          <Typography variant="caption" color="text.secondary" fontSize="0.6875rem">
            {SHIFT_TIMES[st].start}–{SHIFT_TIMES[st].end} · {SHIFT_TIMES[st].hours}H
          </Typography>
        </Box>
      ))}
      <Box component="th" sx={{ width: 40, minWidth: 40 }} />
    </Box>
  );
}
