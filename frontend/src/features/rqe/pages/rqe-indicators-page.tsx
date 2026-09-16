/**
 * RqeIndicatorsPage — Plantão 360
 *
 * Indicador de horas de plantão cobertas por médicos com RQE (PLANTAOPA-3).
 *
 * Responde: "do total de horas realizadas na competência, quanto % foi coberto
 * por médico com RQE?". Não confundir com o card da dashboard, que conta médicos
 * (cabeças) — aqui a métrica é ponderada por hora.
 */

import { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Stack, Grid, TextField, MenuItem, Skeleton,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip,
  ToggleButton, ToggleButtonGroup, Tooltip, useTheme, Alert,
} from '@mui/material';
import {
  BarChart as BarChartIcon, TableRows as TableRowsIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../api/client';
import { tokens, darkTokens } from '../../../theme';
import { ErrorBoundary } from '../../../shared/components/error-boundary';

// ============================================================
// API
// ============================================================

interface RqeDoctorHours {
  doctor_id: number;
  name: string;
  crm: string;
  has_rqe: boolean;
  total_hours: number;
  shift_hours: number;
  extra_hours: number;
  shift_count: number;
}

interface RqeHoursIndicator {
  period_id: number;
  year: number;
  month: number;
  period_name: string;
  period_status: string;
  total_hours: number;
  hours_with_rqe: number;
  hours_without_rqe: number;
  pct_with_rqe: number;
  pct_without_rqe: number;
  doctors_total: number;
  doctors_with_rqe: number;
  doctors_without_rqe: number;
  doctors: RqeDoctorHours[];
}

async function fetchRqeHours(periodId: number | null): Promise<RqeHoursIndicator> {
  const url = periodId
    ? `/query/indicators/rqe-hours?period_id=${periodId}`
    : '/query/indicators/rqe-hours';
  const response = await apiClient.get(url);
  return response.data.data ?? response.data;
}

interface PeriodOption {
  id: number;
  year: number;
  month: number;
}

async function fetchPeriods(): Promise<PeriodOption[]> {
  const response = await apiClient.get('/periods?size=100&sort_by=id&sort_direction=desc');
  return response.data.data?.items ?? [];
}

function periodLabel(p: PeriodOption): string {
  const label = new Date(p.year, p.month - 1, 1).toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
  return label.charAt(0).toUpperCase() + label.slice(1);
}

function formatHours(hours: number): string {
  return `${Math.round(hours)}h`;
}

function formatPct(pct: number): string {
  return `${pct.toFixed(1).replace('.', ',')}%`;
}

// ============================================================
// Bloco 1 — Resumo
// ============================================================

function StatTile({ value, label, color }: { value: string; label: string; color?: string }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;

  return (
    <Card variant="outlined" sx={{ height: '100%' }}>
      <CardContent sx={{ textAlign: 'center', py: 2 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, color: color || colors.text.primary }}>
          {value}
        </Typography>
        <Typography variant="caption" sx={{ color: colors.text.secondary, letterSpacing: 0.5 }}>
          {label}
        </Typography>
      </CardContent>
    </Card>
  );
}

function SummaryBlock({ data, loading }: { data?: RqeHoursIndicator; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;

  if (loading) {
    return <Skeleton variant="rounded" height={140} sx={{ mb: 2 }} />;
  }

  const pct = data?.pct_with_rqe ?? 0;
  const hasHours = (data?.total_hours ?? 0) > 0;

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="overline" sx={{ color: colors.text.secondary, fontWeight: 700 }}>
          HORAS COBERTAS POR MÉDICOS COM RQE
        </Typography>
        <Grid container spacing={2} alignItems="center" sx={{ mt: 0 }}>
          <Grid item xs={12} md={4}>
            <Typography variant="h2" sx={{ fontWeight: 800, color: colors.primary.dark, lineHeight: 1.1 }}>
              {formatPct(pct)}
            </Typography>
            <Typography variant="body2" sx={{ color: colors.text.secondary }}>
              {hasHours ? (
                <>
                  <strong>{formatHours(data!.hours_with_rqe)}</strong> das{' '}
                  <strong>{formatHours(data!.total_hours)}</strong> horas trabalhadas na competência
                  foram cobertas por médicos com RQE.
                </>
              ) : (
                'Nenhuma hora lançada nesta competência.'
              )}
            </Typography>
          </Grid>
          <Grid item xs={6} sm={3} md={2}>
            <StatTile value={formatHours(data?.total_hours ?? 0)} label="TOTAL DE HORAS" />
          </Grid>
          <Grid item xs={6} sm={3} md={2}>
            <StatTile value={String(data?.doctors_total ?? 0)} label="MÉDICOS NA COMPETÊNCIA" />
          </Grid>
          <Grid item xs={6} sm={3} md={2}>
            <StatTile value={String(data?.doctors_with_rqe ?? 0)} label="COM RQE" />
          </Grid>
          <Grid item xs={6} sm={3} md={2}>
            <StatTile
              value={String(data?.doctors_without_rqe ?? 0)}
              label="SEM RQE"
              color={colors.info.main}
            />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

// ============================================================
// Bloco 2 — Distribuição dos plantões por RQE
// ============================================================

function LegendDot({ color, label }: { color: string; label: string }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;

  return (
    <Stack direction="row" alignItems="center" gap={0.75}>
      <Box sx={{ width: 12, height: 12, borderRadius: '3px', bgcolor: color }} />
      <Typography variant="caption" sx={{ color: colors.text.secondary, fontWeight: 600 }}>
        {label}
      </Typography>
    </Stack>
  );
}

function DistributionBlock({ data, loading }: { data?: RqeHoursIndicator; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const withColor = colors.primary.dark;
  const withoutColor = colors.info.main;

  if (loading) {
    return <Skeleton variant="rounded" height={160} sx={{ mb: 2 }} />;
  }

  const total = data?.total_hours ?? 0;
  const pctWith = data?.pct_with_rqe ?? 0;
  const pctWithout = data?.pct_without_rqe ?? 0;

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Stack direction="row" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={1}>
          <Typography variant="subtitle1" sx={{ fontWeight: 700, color: colors.text.primary }}>
            Distribuição dos plantões por RQE
          </Typography>
          <Typography variant="caption" sx={{ color: colors.text.secondary }}>
            {formatHours(total)} · {data?.period_name}
          </Typography>
        </Stack>

        <Stack direction="row" gap={2} sx={{ mt: 1.5, mb: 1 }}>
          <LegendDot color={withColor} label="Com RQE" />
          <LegendDot color={withoutColor} label="Sem RQE" />
        </Stack>

        {total > 0 ? (
          <>
            <Box
              role="img"
              aria-label={`Com RQE ${formatPct(pctWith)}, sem RQE ${formatPct(pctWithout)}`}
              sx={{ display: 'flex', height: 36, borderRadius: 1, overflow: 'hidden' }}
            >
              {pctWith > 0 && (
                <Tooltip title={`Com RQE: ${formatHours(data!.hours_with_rqe)}`}>
                  <Box sx={{
                    width: `${pctWith}%`, bgcolor: withColor, display: 'flex',
                    alignItems: 'center', justifyContent: 'center',
                  }}>
                    <Typography variant="caption" sx={{ color: '#FFF', fontWeight: 700 }}>
                      {pctWith >= 8 ? formatPct(pctWith) : ''}
                    </Typography>
                  </Box>
                </Tooltip>
              )}
              {pctWithout > 0 && (
                <Tooltip title={`Sem RQE: ${formatHours(data!.hours_without_rqe)}`}>
                  <Box sx={{
                    width: `${pctWithout}%`, bgcolor: withoutColor, display: 'flex',
                    alignItems: 'center', justifyContent: 'center',
                  }}>
                    <Typography variant="caption" sx={{ color: '#FFF', fontWeight: 700 }}>
                      {pctWithout >= 8 ? formatPct(pctWithout) : ''}
                    </Typography>
                  </Box>
                </Tooltip>
              )}
            </Box>
            <Stack direction="row" gap={2} flexWrap="wrap" sx={{ mt: 1 }}>
              <Typography variant="caption" sx={{ color: colors.text.secondary }}>
                <strong>Com RQE:</strong> {formatPct(pctWith)} · {formatHours(data!.hours_with_rqe)} ·{' '}
                {data!.doctors_with_rqe} médicos
              </Typography>
              <Typography variant="caption" sx={{ color: colors.text.secondary }}>
                <strong>Sem RQE:</strong> {formatPct(pctWithout)} · {formatHours(data!.hours_without_rqe)} ·{' '}
                {data!.doctors_without_rqe} médicos
              </Typography>
            </Stack>
          </>
        ) : (
          <Typography variant="body2" sx={{ color: colors.text.secondary, py: 2 }}>
            Sem horas lançadas para distribuir nesta competência.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Bloco 3 — Levantamento por médico
// ============================================================

function DoctorBreakdownBlock({ data, loading }: { data?: RqeHoursIndicator; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const [view, setView] = useState<'chart' | 'table'>('chart');

  const withColor = colors.primary.dark;
  const withoutColor = colors.info.main;

  if (loading) {
    return <Skeleton variant="rounded" height={320} />;
  }

  const doctors = data?.doctors ?? [];
  const maxHours = doctors.length > 0 ? doctors[0].total_hours : 0;

  return (
    <Card>
      <CardContent>
        <Stack direction="row" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={1}>
          <Stack direction="row" alignItems="baseline" gap={1} flexWrap="wrap">
            <Typography variant="subtitle1" sx={{ fontWeight: 700, color: colors.text.primary }}>
              Levantamento por médico
            </Typography>
            <Typography variant="caption" sx={{ color: colors.text.secondary }}>
              {doctors.length} médicos com registro · ordenado por horas
            </Typography>
          </Stack>
          <ToggleButtonGroup
            size="small"
            exclusive
            value={view}
            onChange={(_, v) => v && setView(v)}
          >
            <ToggleButton value="chart" aria-label="Ver gráfico">
              <BarChartIcon fontSize="small" sx={{ mr: 0.5 }} /> Gráfico
            </ToggleButton>
            <ToggleButton value="table" aria-label="Ver tabela">
              <TableRowsIcon fontSize="small" sx={{ mr: 0.5 }} /> Tabela
            </ToggleButton>
          </ToggleButtonGroup>
        </Stack>

        <Stack direction="row" gap={2} sx={{ mt: 1.5, mb: 1.5 }}>
          <LegendDot color={withColor} label="Com RQE" />
          <LegendDot color={withoutColor} label="Sem RQE" />
        </Stack>

        {doctors.length === 0 ? (
          <Typography variant="body2" sx={{ color: colors.text.secondary, py: 2 }}>
            Nenhum médico com horas lançadas nesta competência.
          </Typography>
        ) : view === 'chart' ? (
          <Stack gap={0.75}>
            {doctors.map((d) => (
              <Stack key={d.doctor_id} direction="row" alignItems="center" gap={1}>
                <Typography
                  variant="caption"
                  sx={{ width: 190, flexShrink: 0, color: colors.text.primary, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}
                  title={`${d.name} — ${d.has_rqe ? 'com RQE' : 'sem RQE'}`}
                >
                  {d.name}
                </Typography>
                <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                  <Tooltip title={`${d.has_rqe ? 'Com RQE' : 'Sem RQE'} · ${formatHours(d.total_hours)} (${formatHours(d.extra_hours)} de extras)`}>
                    <Box sx={{
                      width: maxHours > 0 ? `${Math.max((d.total_hours / maxHours) * 100, 1)}%` : '1%',
                      height: 16,
                      borderRadius: '3px',
                      bgcolor: d.has_rqe ? withColor : withoutColor,
                    }} />
                  </Tooltip>
                </Box>
                <Typography variant="caption" sx={{ width: 52, flexShrink: 0, textAlign: 'right', color: colors.text.secondary }}>
                  {formatHours(d.total_hours)}
                </Typography>
              </Stack>
            ))}
          </Stack>
        ) : (
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 700 }}>Médico</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>CRM</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>RQE</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700 }}>Plantões</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700 }}>Horas de escala</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700 }}>Horas extras</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700 }}>Total</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {doctors.map((d) => (
                  <TableRow key={d.doctor_id} hover>
                    <TableCell>{d.name}</TableCell>
                    <TableCell>{d.crm}</TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={d.has_rqe ? 'Sim' : 'Não'}
                        sx={{
                          fontWeight: 700,
                          bgcolor: d.has_rqe ? colors.operational.healthyBg : colors.operational.informativeBg,
                          color: d.has_rqe ? colors.primary.dark : colors.info.main,
                        }}
                      />
                    </TableCell>
                    <TableCell align="right">{d.shift_count}</TableCell>
                    <TableCell align="right">{formatHours(d.shift_hours)}</TableCell>
                    <TableCell align="right">{formatHours(d.extra_hours)}</TableCell>
                    <TableCell align="right" sx={{ fontWeight: 700 }}>{formatHours(d.total_hours)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Página
// ============================================================

function RqeIndicatorsPageContent() {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const [selectedPeriodId, setSelectedPeriodId] = useState<number | null>(null);

  const { data: periods = [] } = useQuery({
    queryKey: ['periods', 'selector'],
    queryFn: fetchPeriods,
    staleTime: 5 * 60 * 1000,
  });

  const { data, isLoading, isError } = useQuery({
    queryKey: ['indicators', 'rqe-hours', selectedPeriodId],
    queryFn: () => fetchRqeHours(selectedPeriodId),
  });

  return (
    <Box>
      <Stack direction="row" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={1.5} mb={2}>
        <Stack>
          <Typography variant="h5" sx={{ fontWeight: 700, color: colors.text.primary }}>
            Indicadores RQE
          </Typography>
          <Typography variant="caption" sx={{ color: colors.text.secondary }}>
            Percentual de horas de plantão cobertas por médicos com RQE
          </Typography>
        </Stack>
        <TextField
          select
          size="small"
          label="Competência"
          value={selectedPeriodId ?? ''}
          onChange={(e) => setSelectedPeriodId(e.target.value === '' ? null : Number(e.target.value))}
          sx={{ minWidth: 220 }}
          InputLabelProps={{ shrink: true }}
          SelectProps={{ displayEmpty: true }}
        >
          <MenuItem value="">Atual (automática)</MenuItem>
          {periods.map((p) => (
            <MenuItem key={p.id} value={p.id}>{periodLabel(p)}</MenuItem>
          ))}
        </TextField>
      </Stack>

      {isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Não foi possível carregar o indicador de RQE.
        </Alert>
      )}

      <SummaryBlock data={data} loading={isLoading} />
      <DistributionBlock data={data} loading={isLoading} />
      <DoctorBreakdownBlock data={data} loading={isLoading} />

      <Typography variant="caption" sx={{ display: 'block', mt: 2, color: colors.text.secondary }}>
        Horas contabilizadas: plantões não cancelados + horas extras aprovadas. O RQE considerado é
        o do cadastro atual do médico. Por isso o total pode diferir do total exibido na dashboard,
        que também soma extras pendentes e plantões cancelados.
      </Typography>
    </Box>
  );
}

export default function RqeIndicatorsPage() {
  return (
    <ErrorBoundary>
      <RqeIndicatorsPageContent />
    </ErrorBoundary>
  );
}
