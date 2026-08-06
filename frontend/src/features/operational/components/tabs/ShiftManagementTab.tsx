import React from 'react';
import { Box, Typography, Paper, Chip, Stack, useTheme } from '@mui/material';
import { CallSplit as SplitIcon, MoreTime as ExtraTimeIcon } from '@mui/icons-material';
import { SHIFT_LABELS, SHIFT_TIMES } from '../../types/operational-types';
import type { PeriodInfo } from '../../types/operational-types';
import { getFeatureAccentColors } from '../../utils/feature-accent-colors';

interface ShiftManagementTabProps {
  period: PeriodInfo;
}

const TITULAR_SHIFTS = ['T1', 'T2', 'T3'] as const;
const REFORCO_SHIFTS = ['R1', 'R2'] as const;

const SHIFT_PERIOD_LABEL: Record<string, string> = {
  T1: 'Manhã',
  T2: 'Tarde',
  T3: 'Noite',
  R1: 'Manhã',
  R2: 'Tarde',
};

const SHIFT_PERIOD_COLOR: Record<string, string> = {
  Manhã: '#0EA5E9',
  Tarde: '#F59E0B',
  Noite: '#6366F1',
};

function ShiftDefinitionRow({ code }: { code: string }) {
  const times = SHIFT_TIMES[code];
  const periodLabel = SHIFT_PERIOD_LABEL[code];
  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 2,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="h6" fontWeight={700} sx={{ minWidth: 32 }}>
          {code}
        </Typography>
        <Box>
          <Chip
            label={periodLabel}
            size="small"
            sx={{
              backgroundColor: SHIFT_PERIOD_COLOR[periodLabel],
              color: '#fff',
              fontWeight: 600,
              fontSize: '0.6875rem',
              mb: 0.5,
            }}
          />
          <Typography variant="body2" color="text.secondary">
            {times?.start} → {times?.end}
            {code === 'T3' && <Typography component="span" variant="caption" color="text.secondary"> *</Typography>}
          </Typography>
        </Box>
      </Box>
      <Typography variant="h6" fontWeight={700} color="text.secondary">
        {times?.hours}h
      </Typography>
    </Paper>
  );
}

export function ShiftManagementTab(_props: ShiftManagementTabProps) {
  const theme = useTheme();
  const accent = getFeatureAccentColors(theme.palette.mode);

  return (
    <Box sx={{ p: 3, overflow: 'auto', flex: 1 }}>
      <Typography variant="h6" fontWeight={700} mb={3}>
        Turnos
      </Typography>

      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
          gap: 3,
        }}
      >
        <Box>
          <Typography variant="overline" color="text.secondary" fontWeight={700}>
            {SHIFT_LABELS.T1.split(' ').slice(1).join(' ')} — 24H
          </Typography>
          <Stack spacing={1.5} mt={1}>
            {TITULAR_SHIFTS.map((code) => (
              <ShiftDefinitionRow key={code} code={code} />
            ))}
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            * Noite vira madrugada do dia seguinte
          </Typography>
        </Box>

        <Box>
          <Typography variant="overline" color="text.secondary" fontWeight={700}>
            {SHIFT_LABELS.R1.split(' ').slice(1).join(' ')} — 9H ÀS 21H
          </Typography>
          <Stack spacing={1.5} mt={1}>
            {REFORCO_SHIFTS.map((code) => (
              <ShiftDefinitionRow key={code} code={code} />
            ))}
          </Stack>

          <Typography variant="overline" color="text.secondary" fontWeight={700} sx={{ display: 'block', mt: 3 }}>
            Recursos Especiais
          </Typography>
          <Stack spacing={1.5} mt={1}>
            <Paper variant="outlined" sx={{ p: 2, display: 'flex', alignItems: 'flex-start', gap: 1.5, bgcolor: accent.violet.bg }}>
              <SplitIcon sx={{ color: accent.violet.main, mt: 0.25 }} fontSize="small" />
              <Box>
                <Typography variant="body2" fontWeight={700} color="text.primary">Ajuste / Divisão de turno</Typography>
                <Typography variant="caption" color="text.secondary">
                  Divide um turno entre dois médicos com horários e horas exatas
                </Typography>
              </Box>
            </Paper>
            <Paper variant="outlined" sx={{ p: 2, display: 'flex', alignItems: 'flex-start', gap: 1.5, bgcolor: accent.amber.bg }}>
              <ExtraTimeIcon sx={{ color: accent.amber.main, mt: 0.25 }} fontSize="small" />
              <Box>
                <Typography variant="body2" fontWeight={700} color="text.primary">Horário Extra</Typography>
                <Typography variant="caption" color="text.secondary">
                  Registra horas extras fora do turno padrão com justificativa obrigatória
                </Typography>
              </Box>
            </Paper>
          </Stack>
        </Box>
      </Box>
    </Box>
  );
}
