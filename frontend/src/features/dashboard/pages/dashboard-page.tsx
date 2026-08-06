/**
 * DashboardPage — Plantão 360
 *
 * Centro de Operações Hospitalares.
 * Responde à pergunta: "Situação operacional em <30 segundos?"
 *
 * Layout: header verde institucional (MainLayout) + grid de indicadores estratégicos.
 * Identidade visual: Manual da Marca Unimed (verde #00995D, verde escuro #004E4C).
 */

import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Stack, List, ListItem, ListItemAvatar,
  ListItemText, Avatar, Skeleton, TextField, MenuItem, LinearProgress,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip, Tooltip, useTheme,
} from '@mui/material';
import {
  EventNote as EventNoteIcon,
  VerifiedUser as VerifiedUserIcon, EmojiEvents as EmojiEventsIcon,
  AttachMoney as AttachMoneyIcon, TrendingUp as TrendingUpIcon, TrendingDown as TrendingDownIcon,
  BarChart as BarChartIcon, Circle as CircleIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { queryKeys } from '../../../services/query-keys';
import { useFeatureFlagService } from '../../../config/feature-flag-service';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import { tokens, darkTokens } from '../../../theme';
import { getOperationalLevel } from '../../../shared/constants/status-colors';
import {
  OperationalHealthCard, CriticalAlertCard, UpcomingActionCard, OperationalEmptyState,
} from '../../../shared/components/operational';
import { SkeletonCard } from '../../../shared/components/loading/SkeletonCard';
import { AutoRefreshIndicator } from '../../../shared/components/loading/AutoRefreshIndicator';
import { ContentTransition } from '../../../shared/components/loading/ContentTransition';
import { apiClient } from '../../../api/client';

// ============================================================
// API
// ============================================================

async function fetchDashboard(periodId: number | null) {
  // B-03: sem periodId o backend usa a competência atual (comportamento anterior).
  const url = periodId ? `/query/dashboard?period_id=${periodId}` : '/query/dashboard';
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

// ============================================================
// Types
// ============================================================

function severityToLevel(severity: string): 'healthy' | 'attention' | 'critical' | 'informative' {
  return getOperationalLevel(severity);
}

interface RqeStats {
  with_rqe: number;
  without_rqe: number;
  total: number;
  pct_with_rqe: number;
}

interface DoctorRankingEntry {
  doctor_id: number;
  name: string;
  crm: string;
  has_rqe: boolean;
  hour_rate_tier: string;
  hour_rate: number;
  total_hours: number;
  shift_count: number;
  extra_hours: number;
  total_value: number;
}

interface FinancialTrendPoint {
  period_id: number;
  period_name: string;
  year: number;
  month: number;
  total_hours: number;
  total_value: number;
  shift_count: number;
}

interface ShiftTypeBreakdownEntry {
  shift_type: string;
  total_hours: number;
  total_value: number;
  shift_count: number;
  doctor_count: number;
}

interface FinancialData {
  current_total_value: number;
  current_total_hours: number;
  previous_total_value: number;
  variation_pct: number;
  avg_value_per_hour: number;
  extras_value: number;
  regular_value: number;
  trend: FinancialTrendPoint[];
  shift_type_breakdown: ShiftTypeBreakdownEntry[];
}

function formatCurrency(value: number): string {
  return `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatCurrencyCompact(value: number): string {
  if (value >= 1_000_000) return `R$ ${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `R$ ${(value / 1_000).toFixed(0)}k`;
  return formatCurrency(value);
}

const SHIFT_TYPE_LABELS: Record<string, string> = {
  T1: 'Titular 07h–19h',
  T2: 'Titular 19h–07h',
  T3: 'Titular 24h',
  R1: 'Reforço 09h–21h',
  R2: 'Reforço 09h–21h',
};

// ============================================================
// Seção — título padrão
// ============================================================

function SectionTitle({ icon, children }: { icon: React.ReactNode; children: React.ReactNode }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  return (
    <Stack direction="row" alignItems="center" gap={1} mb={1.5}>
      {icon}
      <Typography variant="subtitle2" sx={{ fontWeight: 700, color: colors.text.primary, letterSpacing: '0.04em' }}>
        {children}
      </Typography>
    </Stack>
  );
}

// ============================================================
// RQE Card
// ============================================================

function RqeStatsCard({ stats, loading }: { stats: RqeStats | undefined; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const withRqe = stats?.with_rqe || 0;
  const withoutRqe = stats?.without_rqe || 0;
  const total = stats?.total || 0;
  const pct = stats?.pct_with_rqe || 0;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <SectionTitle icon={<VerifiedUserIcon sx={{ fontSize: 20, color: colors.primary.main }} />}>
          MÉDICOS COM RQE
        </SectionTitle>
        {loading ? (
          <Skeleton variant="rectangular" height={100} />
        ) : (
          <>
            <Stack direction="row" alignItems="baseline" gap={1} mb={0.75} flexWrap="wrap">
              <Typography variant="h4" sx={{ fontWeight: 700, color: colors.primary.main }}>
                {pct.toFixed(0)}%
              </Typography>
              <Typography variant="body2" sx={{ color: colors.text.secondary }}>
                dos médicos ativos possuem RQE
              </Typography>
            </Stack>
            <LinearProgress
              variant="determinate"
              value={pct}
              sx={{
                height: 8,
                borderRadius: 4,
                mb: 2,
                bgcolor: colors.grey[200],
                '& .MuiLinearProgress-bar': { bgcolor: colors.primary.main, borderRadius: 4 },
              }}
            />
            <Stack direction="row" justifyContent="space-between">
              <Stack alignItems="flex-start">
                <Typography variant="h6" sx={{ fontWeight: 700, color: colors.text.primary }}>{withRqe}</Typography>
                <Typography variant="caption" sx={{ color: colors.text.secondary }}>Com RQE</Typography>
              </Stack>
              <Stack alignItems="flex-start">
                <Typography variant="h6" sx={{ fontWeight: 700, color: colors.text.primary }}>{withoutRqe}</Typography>
                <Typography variant="caption" sx={{ color: colors.text.secondary }}>Sem RQE</Typography>
              </Stack>
              <Stack alignItems="flex-start">
                <Typography variant="h6" sx={{ fontWeight: 700, color: colors.text.primary }}>{total}</Typography>
                <Typography variant="caption" sx={{ color: colors.text.secondary }}>Total ativos</Typography>
              </Stack>
            </Stack>
          </>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Resumo Operacional (compacto)
// ============================================================

function OperationalSummaryCard({ kpis, loading }: { kpis: any; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const rows = [
    { label: 'Total de Plantões', value: `${kpis.total_shifts || 0}` },
    { label: 'Plantões distribuídos', value: `${kpis.assigned_shifts || 0}` },
    { label: 'Médicos Ativos', value: `${kpis.active_doctors || 0}` },
    { label: 'Total de Horas', value: `${kpis.total_hours || 0}h` },
    { label: 'Extras pendentes', value: `${kpis.pending_extras || 0}` },
  ];
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <SectionTitle icon={<EventNoteIcon sx={{ fontSize: 20, color: colors.primary.main }} />}>
          RESUMO OPERACIONAL
        </SectionTitle>
        {loading ? (
          <Stack spacing={1}>
            {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} variant="text" height={24} />)}
          </Stack>
        ) : (
          <Stack spacing={1.25}>
            {rows.map((row) => (
              <Stack key={row.label} direction="row" justifyContent="space-between">
                <Typography variant="body2" sx={{ color: colors.text.secondary }}>{row.label}</Typography>
                <Typography variant="body2" sx={{ fontWeight: 700, color: colors.text.primary }}>{row.value}</Typography>
              </Stack>
            ))}
          </Stack>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Ranking de médicos por horas trabalhadas
// ============================================================

function DoctorRankingCard({ ranking, loading }: { ranking: DoctorRankingEntry[] | undefined; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const entries = ranking || [];
  const maxHours = entries.length > 0 ? Math.max(...entries.map((e) => e.total_hours)) : 0;

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 }, display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0 }}>
        <SectionTitle icon={<EmojiEventsIcon sx={{ fontSize: 20, color: '#F47920' }} />}>
          RANKING DE MÉDICOS POR HORAS TRABALHADAS
        </SectionTitle>
        {loading ? (
          <Stack spacing={1}>
            {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} variant="text" height={32} />)}
          </Stack>
        ) : entries.length === 0 ? (
          <Typography variant="body2" sx={{ color: colors.text.secondary, py: 2, textAlign: 'center' }}>
            Nenhum plantão registrado nesta competência ainda.
          </Typography>
        ) : (
          <TableContainer sx={{ flex: 1, minHeight: 0, maxHeight: 420 }}>
            <Table size="small" stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 700, fontSize: '0.75rem', width: 40 }}>#</TableCell>
                  <TableCell sx={{ fontWeight: 700, fontSize: '0.75rem' }}>Médico</TableCell>
                  <TableCell sx={{ fontWeight: 700, fontSize: '0.75rem', width: 70 }}>RQE</TableCell>
                  <TableCell sx={{ fontWeight: 700, fontSize: '0.75rem', minWidth: 160 }}>Horas</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700, fontSize: '0.75rem', width: 90 }}>Plantões</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, fontSize: '0.75rem', width: 130 }}>Valor Total</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {entries.map((d, idx) => (
                  <TableRow key={d.doctor_id} hover>
                    <TableCell sx={{ fontSize: '0.8125rem', color: colors.text.secondary }}>{idx + 1}º</TableCell>
                    <TableCell sx={{ fontSize: '0.8125rem', fontWeight: 600 }}>
                      {d.name}
                      <Typography variant="caption" display="block" sx={{ color: colors.text.secondary }}>
                        {d.crm} · {d.hour_rate_tier}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={d.has_rqe ? 'Sim' : 'Não'}
                        size="small"
                        sx={{
                          fontSize: '0.6875rem',
                          height: 20,
                          fontWeight: 600,
                          bgcolor: d.has_rqe ? colors.operational.healthyBg : colors.grey[100],
                          color: d.has_rqe
                            ? (theme.palette.mode === 'dark' ? colors.operational.healthy : colors.primary.dark)
                            : colors.text.secondary,
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Stack direction="row" alignItems="center" gap={1}>
                        <Box sx={{ flex: 1, minWidth: 60 }}>
                          <LinearProgress
                            variant="determinate"
                            value={maxHours > 0 ? (d.total_hours / maxHours) * 100 : 0}
                            sx={{
                              height: 6,
                              borderRadius: 3,
                              bgcolor: colors.grey[200],
                              '& .MuiLinearProgress-bar': { bgcolor: colors.primary.main, borderRadius: 3 },
                            }}
                          />
                        </Box>
                        <Typography variant="body2" sx={{ fontWeight: 700, minWidth: 44, fontVariantNumeric: 'tabular-nums' }}>
                          {d.total_hours.toFixed(0)}h
                        </Typography>
                      </Stack>
                    </TableCell>
                    <TableCell align="center" sx={{ fontSize: '0.8125rem' }}>{d.shift_count}</TableCell>
                    <TableCell align="right" sx={{ fontSize: '0.8125rem', fontWeight: 700, color: colors.primary.main, fontVariantNumeric: 'tabular-nums' }}>
                      {formatCurrency(d.total_value)}
                    </TableCell>
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
// Faturamento — Resumo
// ============================================================

function FinancialSummaryCard({ financial, loading }: { financial: FinancialData | undefined; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const value = financial?.current_total_value || 0;
  const hours = financial?.current_total_hours || 0;
  const variation = financial?.variation_pct || 0;
  const avgHour = financial?.avg_value_per_hour || 0;
  const extrasValue = financial?.extras_value || 0;
  const regularValue = financial?.regular_value || 0;
  const extrasPct = value > 0 ? (extrasValue / value) * 100 : 0;
  const isUp = variation >= 0;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <SectionTitle icon={<AttachMoneyIcon sx={{ fontSize: 20, color: colors.primary.main }} />}>
          FATURAMENTO DA COMPETÊNCIA
        </SectionTitle>
        {loading ? (
          <Skeleton variant="rectangular" height={140} />
        ) : (
          <>
            <Stack direction="row" alignItems="baseline" gap={1} flexWrap="wrap">
              <Typography variant="h4" sx={{ fontWeight: 700, color: colors.text.primary, fontVariantNumeric: 'tabular-nums' }}>
                {formatCurrency(value)}
              </Typography>
              {financial && financial.previous_total_value > 0 && (
                <Stack direction="row" alignItems="center" gap={0.25} sx={{ color: isUp ? colors.operational.healthy : colors.operational.critical }}>
                  {isUp ? <TrendingUpIcon sx={{ fontSize: 16 }} /> : <TrendingDownIcon sx={{ fontSize: 16 }} />}
                  <Typography variant="body2" sx={{ fontWeight: 700 }}>
                    {isUp ? '+' : ''}{variation.toFixed(1)}%
                  </Typography>
                </Stack>
              )}
            </Stack>
            <Typography variant="caption" sx={{ color: colors.text.secondary, display: 'block', mb: 2 }}>
              vs. competência anterior · {hours.toFixed(0)}h trabalhadas
            </Typography>

            <Box sx={{ mb: 2 }}>
              <Typography variant="caption" sx={{ color: colors.text.secondary }}>Custo médio / hora</Typography>
              <Typography variant="h6" sx={{ fontWeight: 700, color: colors.text.primary }}>
                {formatCurrency(avgHour)}
              </Typography>
            </Box>

            <Typography variant="caption" sx={{ color: colors.text.secondary, fontWeight: 700 }}>
              REGULAR vs. HORAS EXTRAS
            </Typography>
            <Box sx={{ display: 'flex', height: 10, borderRadius: 1, overflow: 'hidden', mt: 0.75, mb: 0.75, bgcolor: colors.grey[200] }}>
              <Box sx={{ width: `${100 - extrasPct}%`, bgcolor: colors.primary.main }} />
              <Box sx={{ width: `${extrasPct}%`, bgcolor: '#F47920' }} />
            </Box>
            <Stack direction="row" justifyContent="space-between">
              <Typography variant="caption" sx={{ color: colors.text.secondary }}>
                Regular: <strong style={{ color: colors.text.primary }}>{formatCurrencyCompact(regularValue)}</strong>
              </Typography>
              <Typography variant="caption" sx={{ color: colors.text.secondary }}>
                Extras: <strong style={{ color: colors.text.primary }}>{formatCurrencyCompact(extrasValue)}</strong>
              </Typography>
            </Stack>
          </>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Faturamento — Valores pagos ao longo do tempo
// ============================================================

function FinancialTrendCard({ trend, loading }: { trend: FinancialTrendPoint[] | undefined; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const points = trend || [];
  const maxValue = points.length > 0 ? Math.max(...points.map((p) => p.total_value)) : 0;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <SectionTitle icon={<TrendingUpIcon sx={{ fontSize: 20, color: colors.primary.main }} />}>
          VALORES PAGOS AO LONGO DO TEMPO
        </SectionTitle>
        {loading ? (
          <Skeleton variant="rectangular" height={200} />
        ) : points.length === 0 ? (
          <Typography variant="body2" sx={{ color: colors.text.secondary, py: 2, textAlign: 'center' }}>
            Sem histórico de competências suficiente.
          </Typography>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'flex-end', gap: 1.5, height: 210, px: 0.5 }}>
            {points.map((p, idx) => {
              const heightPct = maxValue > 0 ? Math.max((p.total_value / maxValue) * 100, 3) : 3;
              const isLast = idx === points.length - 1;
              return (
                <Tooltip
                  key={p.period_id}
                  title={`${p.period_name}: ${formatCurrency(p.total_value)} (${p.total_hours.toFixed(0)}h, ${p.shift_count} plantões)`}
                  arrow
                >
                  <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end', cursor: 'default' }}>
                    <Typography variant="caption" sx={{ fontWeight: 700, color: colors.text.primary, mb: 0.5, fontSize: '0.6875rem', whiteSpace: 'nowrap' }}>
                      {formatCurrencyCompact(p.total_value)}
                    </Typography>
                    <Box
                      sx={{
                        width: '100%',
                        maxWidth: 64,
                        height: `${heightPct}%`,
                        minHeight: 4,
                        borderRadius: '4px 4px 0 0',
                        bgcolor: isLast ? colors.primary.main : colors.primary.main + '99',
                        transition: 'height 300ms ease-out',
                      }}
                    />
                    <Typography variant="caption" sx={{ color: colors.text.secondary, mt: 0.75, fontSize: '0.6875rem', textAlign: 'center', whiteSpace: 'nowrap' }}>
                      {p.period_name.slice(0, 3)}/{String(p.year).slice(2)}
                    </Typography>
                  </Box>
                </Tooltip>
              );
            })}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Faturamento — Valores por turno
// ============================================================

function ShiftTypeBreakdownCard({ breakdown, loading }: { breakdown: ShiftTypeBreakdownEntry[] | undefined; loading: boolean }) {
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const rows = breakdown || [];
  const maxValue = rows.length > 0 ? Math.max(...rows.map((r) => r.total_value)) : 0;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <SectionTitle icon={<BarChartIcon sx={{ fontSize: 20, color: colors.primary.main }} />}>
          VALORES POR TURNO
        </SectionTitle>
        {loading ? (
          <Stack spacing={1.5}>
            {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} variant="text" height={28} />)}
          </Stack>
        ) : rows.length === 0 ? (
          <Typography variant="body2" sx={{ color: colors.text.secondary, py: 2, textAlign: 'center' }}>
            Sem plantões distribuídos nesta competência.
          </Typography>
        ) : (
          <Stack spacing={1.75}>
            {rows.map((r) => (
              <Box key={r.shift_type}>
                <Stack direction="row" justifyContent="space-between" alignItems="baseline" mb={0.5}>
                  <Typography variant="body2" sx={{ fontWeight: 700, color: colors.text.primary }}>
                    {r.shift_type}
                    <Typography component="span" variant="caption" sx={{ color: colors.text.secondary, ml: 0.75, fontWeight: 400 }}>
                      {SHIFT_TYPE_LABELS[r.shift_type] || ''} · {r.shift_count} plantões · {r.doctor_count} médicos
                    </Typography>
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 700, color: colors.text.primary, fontVariantNumeric: 'tabular-nums' }}>
                    {formatCurrency(r.total_value)}
                  </Typography>
                </Stack>
                <LinearProgress
                  variant="determinate"
                  value={maxValue > 0 ? (r.total_value / maxValue) * 100 : 0}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    bgcolor: colors.grey[200],
                    '& .MuiLinearProgress-bar': { bgcolor: colors.primary.main, borderRadius: 4 },
                  }}
                />
              </Box>
            ))}
          </Stack>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// Main Component
// ============================================================

function DashboardPageContent() {
  const featureFlags = useFeatureFlagService();
  const isDemoMode = featureFlags.isEnabled('DEMO_MODE');
  const navigate = useNavigate();
  const theme = useTheme();
  const colors = theme.palette.mode === 'dark' ? darkTokens.colors : tokens.colors;
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());
  // B-03: null = competência automática (mais recente não paga), como antes.
  const [selectedPeriodId, setSelectedPeriodId] = useState<number | null>(null);

  const { data: periods = [] } = useQuery({
    queryKey: ['periods', 'dashboard-selector'],
    queryFn: fetchPeriods,
    staleTime: 5 * 60 * 1000,
  });

  const {
    data: dashboard,
    isLoading,
    error,
    isFetching,
  } = useQuery({
    queryKey: [...queryKeys.dashboard.summary, selectedPeriodId ?? 'auto'],
    queryFn: () => fetchDashboard(selectedPeriodId),
    refetchInterval: isDemoMode ? false : 30000,
  });

  useEffect(() => {
    if (!isFetching && dashboard) {
      setLastRefresh(new Date());
    }
  }, [isFetching, dashboard]);

  if (error) {
    return (
      <Card sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ color: colors.error.main, mb: 1 }}>
          Erro ao carregar dashboard
        </Typography>
        <Typography variant="body2" sx={{ color: colors.text.secondary }}>
          Verifique se o backend está rodando.
        </Typography>
      </Card>
    );
  }

  // Map API data
  const kpis = dashboard?.kpis || {};
  const healthCards = dashboard?.health_cards || [];
  const activities = dashboard?.recent_activities || [];
  const alerts = dashboard?.operational_alerts || [];
  const upcomingActions = dashboard?.upcoming_actions || [];

  const criticalAlerts = alerts.filter((a: any) => a.severity === 'critical' || a.severity === 'high');
  const operationalState = criticalAlerts.length > 0 ? 'critical' : kpis.coverage_rate < 90 ? 'attention' : 'healthy';
  const stateConfig = {
    healthy: { color: colors.operational.healthy, label: 'Operação Normal', bg: colors.operational.healthyBg },
    attention: { color: colors.operational.attention, label: 'Atenção', bg: colors.operational.attentionBg },
    critical: { color: colors.operational.critical, label: 'Crítico', bg: colors.operational.criticalBg },
  }[operationalState as 'healthy' | 'attention' | 'critical'];

  const cardRoutes: Record<string, string> = {
    coverage: '/app/coverage',
    doctors: '/app/doctors',
    shifts: '/app/shifts',
    hours: '/app/payroll',
  };

  const cardLevels = healthCards.map((card: any) => ({
    ...card,
    level: severityToLevel(card.status || 'info'),
    route: cardRoutes[card.card_id] || '/app/dashboard',
    percentage: card.card_id === 'coverage' ? (parseFloat(card.value) || 0) : undefined,
  }));

  const mappedActions = upcomingActions.map((action: any, idx: number) => ({
    action_id: action.action_id || `action-${idx}`,
    title: action.title || action.description,
    description: action.description !== action.title ? action.description : undefined,
    priority: idx === 0 ? 'high' as const : idx < 3 ? 'medium' as const : 'low' as const,
    action_label: 'Ver',
    action_route: action.route || '/app/dashboard',
  }));

  return (
    <Box>
      {/* Barra de controle: estado operacional + seletor de competência */}
      <Stack direction="row" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={1.5} mb={2}>
        <Stack direction="row" alignItems="center" gap={1.5}>
          <Typography variant="h5" sx={{ fontWeight: 700, color: colors.text.primary }}>
            Dashboard Operacional
          </Typography>
          {!isLoading && (
            <Chip
              icon={<CircleIcon sx={{ fontSize: 10, color: `${stateConfig.color} !important` }} />}
              label={stateConfig.label}
              size="small"
              sx={{
                bgcolor: stateConfig.bg,
                color: stateConfig.color,
                fontWeight: 700,
                border: `1px solid ${stateConfig.color}30`,
              }}
            />
          )}
        </Stack>
        <Stack direction="row" alignItems="center" gap={2}>
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
          <AutoRefreshIndicator lastRefresh={lastRefresh} isRefreshing={isFetching} />
        </Stack>
      </Stack>

      {/* Alertas Críticos */}
      {!isLoading && criticalAlerts.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <CriticalAlertCard
            alerts={criticalAlerts.map((a: any, idx: number) => ({
              alert_id: a.alert_id || `alert-${idx}`,
              title: a.title,
              description: a.description,
              severity: a.severity === 'critical' || a.severity === 'high' ? 'critical' : 'warning',
              action_label: 'Resolver',
              action_route: '/app/shifts',
            }))}
            onAction={(route) => navigate(route)}
          />
        </Box>
      )}

      {/* Health Cards */}
      <Grid container spacing={2}>
        {(isLoading ? Array.from({ length: 4 }) : cardLevels).map((card: any, index: number) => (
          <Grid item xs={12} sm={6} lg={3} key={card?.card_id || index}
            sx={{ animation: `fadeInUp 300ms ease-out ${index * 50}ms both` }}>
            {isLoading ? (
              <SkeletonCard />
            ) : (
              <OperationalHealthCard
                title={card.label}
                value={card.value}
                level={card.level}
                trend={card.trend_direction}
                detail={card.detail}
                route={card.route}
                percentage={card.percentage}
              />
            )}
          </Grid>
        ))}
      </Grid>

      {/* Ranking + coluna lateral (RQE + Resumo) */}
      <Grid container spacing={2} sx={{ mt: 0 }}>
        <Grid item xs={12} lg={8}>
          <ContentTransition visible={!isLoading}>
            <DoctorRankingCard ranking={dashboard?.doctor_ranking} loading={isLoading} />
          </ContentTransition>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Stack spacing={2} sx={{ height: '100%' }}>
            <ContentTransition visible={!isLoading}>
              <RqeStatsCard stats={dashboard?.rqe_stats} loading={isLoading} />
            </ContentTransition>
            <ContentTransition visible={!isLoading}>
              <OperationalSummaryCard kpis={kpis} loading={isLoading} />
            </ContentTransition>
          </Stack>
        </Grid>
      </Grid>

      {/* Faturamento */}
      <Grid container spacing={2} sx={{ mt: 0 }}>
        <Grid item xs={12} md={6} lg={4}>
          <ContentTransition visible={!isLoading}>
            <FinancialSummaryCard financial={dashboard?.financial} loading={isLoading} />
          </ContentTransition>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <ContentTransition visible={!isLoading}>
            <FinancialTrendCard trend={dashboard?.financial?.trend} loading={isLoading} />
          </ContentTransition>
        </Grid>
        <Grid item xs={12} md={12} lg={4}>
          <ContentTransition visible={!isLoading}>
            <ShiftTypeBreakdownCard breakdown={dashboard?.financial?.shift_type_breakdown} loading={isLoading} />
          </ContentTransition>
        </Grid>
      </Grid>

      {/* Últimos Eventos + Próximas Ações */}
      <Grid container spacing={2} sx={{ mt: 0, mb: 1 }}>
        {!isLoading && activities.length > 0 && (
          <Grid item xs={12} lg={mappedActions.length > 0 ? 8 : 12}>
            <ContentTransition visible={!isLoading}>
              <Card sx={{ height: '100%' }}>
                <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
                  <SectionTitle icon={<EventNoteIcon sx={{ fontSize: 20, color: colors.primary.main }} />}>
                    ÚLTIMOS EVENTOS
                  </SectionTitle>
                  <List dense disablePadding>
                    {activities.slice(0, 5).map((activity: any, index: number) => (
                      <ListItem key={activity.activity_id || index} sx={{ px: 0, py: 0.5 }}>
                        <ListItemAvatar sx={{ minWidth: 40 }}>
                          <Avatar sx={{
                            width: 28, height: 28,
                            bgcolor: colors.operational.healthyBg,
                            color: colors.primary.main,
                          }}>
                            <EventNoteIcon sx={{ fontSize: 14 }} />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={activity.description}
                          secondary={activity.timestamp ? new Date(activity.timestamp).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''}
                          primaryTypographyProps={{ variant: 'body2', fontWeight: 500 }}
                          secondaryTypographyProps={{ variant: 'caption' }}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </ContentTransition>
          </Grid>
        )}
        {!isLoading && mappedActions.length > 0 && (
          <Grid item xs={12} lg={activities.length > 0 ? 4 : 12}>
            <ContentTransition visible={!isLoading}>
              <UpcomingActionCard
                actions={mappedActions}
                onAction={(route) => navigate(route)}
              />
            </ContentTransition>
          </Grid>
        )}
      </Grid>

      {/* Empty State quando não há dados */}
      {!isLoading && !dashboard && (
        <OperationalEmptyState context="dashboard" />
      )}
    </Box>
  );
}

export default function DashboardPage() {
  return (
    <ErrorBoundary>
      <DashboardPageContent />
    </ErrorBoundary>
  );
}
