/**
 * OperationalMetricsPanel — Plantão 360
 *
 * Painel reutilizável com métricas em 5 categorias:
 * Cobertura, Médicos Ativos, Plantões, Competência, Extras/Payroll.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Card, CardContent, Typography, Stack, LinearProgress, Divider } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { tokens } from '../../../theme';
import { OperationalLevel, getOperationalStatus } from '../../constants/status-colors';

// ============================================================
// Types
// ============================================================

interface ShiftDistribution {
  label: string;
  count: number;
  color?: string;
}

interface OperationalMetricsPanelProps {
  coverage: { percentage: number; level: OperationalLevel; covered: number; total: number };
  doctors: { active: number; total: number; inactive: number; level: OperationalLevel };
  shifts: { total: number; distribution: ShiftDistribution[]; uncovered: number; level: OperationalLevel };
  competency: { name: string; progress: number; level: OperationalLevel; daysElapsed: number; totalDays: number };
  extras: { pending: number; approved: number; payrollStatus: string; level: OperationalLevel };
}

// ============================================================
// Component
// ============================================================

export function OperationalMetricsPanel({
  coverage,
  doctors,
  shifts,
  competency,
  extras,
}: OperationalMetricsPanelProps) {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="subtitle2" sx={{ fontWeight: 600, color: tokens.colors.text.primary, mb: 1.5 }}>
        PAINEL DE MÉTRICAS
      </Typography>

      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
          gap: 2,
        }}
      >
        {/* Coverage */}
        <Card
          onClick={() => navigate('/app/coverage')}
          sx={{ cursor: 'pointer', '&:hover': { boxShadow: tokens.elevation.sm } }}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              COBERTURA
            </Typography>
            <Stack direction="row" alignItems="baseline" spacing={1} sx={{ mt: 0.5, mb: 1 }}>
              <Typography sx={{ fontSize: '1.5rem', fontWeight: 700, color: getOperationalStatus(coverage.level).color }}>
                {coverage.percentage}%
              </Typography>
              <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>
                {coverage.covered}/{coverage.total} plantões
              </Typography>
            </Stack>
            <LinearProgress
              variant="determinate"
              value={coverage.percentage}
              sx={{ height: 4, borderRadius: 2, bgcolor: `${getOperationalStatus(coverage.level).color}20`, '& .MuiLinearProgress-bar': { bgcolor: getOperationalStatus(coverage.level).color, borderRadius: 2 } }}
            />
          </CardContent>
        </Card>

        {/* Doctors */}
        <Card
          onClick={() => navigate('/app/doctors')}
          sx={{ cursor: 'pointer', '&:hover': { boxShadow: tokens.elevation.sm } }}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              MÉDICOS
            </Typography>
            <Stack direction="row" alignItems="baseline" spacing={1} sx={{ mt: 0.5 }}>
              <Typography sx={{ fontSize: '1.5rem', fontWeight: 700, color: tokens.colors.text.primary }}>
                {doctors.active}
              </Typography>
              <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>
                de {doctors.total} ativos
              </Typography>
            </Stack>
            {doctors.inactive > 0 && (
              <Typography variant="caption" sx={{ color: tokens.colors.operational.attention, fontWeight: 600, display: 'block', mt: 0.5 }}>
                {doctors.inactive} inativo{doctors.inactive > 1 ? 's' : ''}
              </Typography>
            )}
          </CardContent>
        </Card>

        {/* Shifts Distribution */}
        <Card
          onClick={() => navigate('/app/shifts')}
          sx={{ cursor: 'pointer', '&:hover': { boxShadow: tokens.elevation.sm } }}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              PLANTÕES
            </Typography>
            <Typography sx={{ fontSize: '1.5rem', fontWeight: 700, color: tokens.colors.text.primary, mt: 0.5 }}>
              {shifts.total}
            </Typography>
            <Stack direction="row" spacing={1.5} sx={{ mt: 1, flexWrap: 'wrap', gap: 0.5 }}>
              {shifts.distribution.map((d) => (
                <Typography key={d.label} variant="caption" sx={{ color: d.color || tokens.colors.text.secondary }}>
                  {d.label}: <strong>{d.count}</strong>
                </Typography>
              ))}
            </Stack>
            {shifts.uncovered > 0 && (
              <Typography variant="caption" sx={{ color: tokens.colors.operational.critical, fontWeight: 600, display: 'block', mt: 0.75 }}>
                {shifts.uncovered} sem médico
              </Typography>
            )}
          </CardContent>
        </Card>

        {/* Competency */}
        <Card
          onClick={() => navigate('/app/periods')}
          sx={{ cursor: 'pointer', '&:hover': { boxShadow: tokens.elevation.sm } }}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              COMPETÊNCIA
            </Typography>
            <Typography sx={{ fontSize: '1.25rem', fontWeight: 700, color: tokens.colors.text.primary, mt: 0.5 }}>
              {competency.name}
            </Typography>
            <LinearProgress
              variant="determinate"
              value={competency.progress}
              sx={{ height: 4, borderRadius: 2, mt: 1, bgcolor: `${getOperationalStatus(competency.level).color}20`, '& .MuiLinearProgress-bar': { bgcolor: getOperationalStatus(competency.level).color, borderRadius: 2 } }}
            />
            <Typography variant="caption" sx={{ color: tokens.colors.text.muted, display: 'block', mt: 0.5 }}>
              {competency.daysElapsed} de {competency.totalDays} dias
            </Typography>
          </CardContent>
        </Card>

        {/* Extras/Payroll (full width) */}
        <Card
          onClick={() => navigate('/app/extras')}
          sx={{ cursor: 'pointer', gridColumn: { xs: '1', md: '1 / -1' }, '&:hover': { boxShadow: tokens.elevation.sm } }}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.secondary, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              EXTRAS / PAYROLL
            </Typography>
            <Stack direction="row" spacing={3} sx={{ mt: 0.5, flexWrap: 'wrap', gap: 1 }}>
              <Box>
                <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>
                  Extras pendentes: <strong style={{ color: extras.pending > 0 ? tokens.colors.operational.attention : tokens.colors.text.primary }}>{extras.pending}</strong>
                </Typography>
              </Box>
              <Box>
                <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>
                  Extras aprovados: <strong>{extras.approved}</strong>
                </Typography>
              </Box>
              <Box>
                <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>
                  Payroll: <strong style={{ color: extras.payrollStatus === 'Pendente' ? tokens.colors.operational.attention : tokens.colors.text.primary }}>{extras.payrollStatus}</strong>
                </Typography>
              </Box>
            </Stack>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}
