/**
 * DashboardPage — Plantão 360
 *
 * Centro de Operações Hospitalares.
 * Responde à pergunta: "Situação operacional em <30 segundos?"
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Stack, List, ListItem, ListItemAvatar,
  ListItemText, Avatar, Divider, Tooltip, Skeleton,
} from '@mui/material';
import {
  Refresh as RefreshIcon, EventNote as EventNoteIcon, AccessTime as AccessTimeIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { queryKeys } from '../../../services/query-keys';
import { useFeatureFlagService } from '../../../config/feature-flag-service';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import { tokens } from '../../../theme';
import { getOperationalLevel } from '../../../shared/constants/status-colors';
import {
  OperationalHealthCard, CoverageCard, CompetencyCard, CriticalAlertCard,
  UpcomingActionCard, InstitutionStatusBar, OperationalMetricsPanel,
  OperationalEmptyState,
} from '../../../shared/components/operational';
import { SkeletonCard } from '../../../shared/components/loading/SkeletonCard';
import { AutoRefreshIndicator } from '../../../shared/components/loading/AutoRefreshIndicator';
import { ContentTransition } from '../../../shared/components/loading/ContentTransition';
import { apiClient } from '../../../api/client';

// ============================================================
// API
// ============================================================

async function fetchDashboard() {
  const response = await apiClient.get('/query/dashboard');
  return response.data.data ?? response.data;
}

// ============================================================
// Helpers
// ============================================================

function severityToLevel(severity: string): 'healthy' | 'attention' | 'critical' | 'informative' {
  return getOperationalLevel(severity);
}

// ============================================================
// Main Component
// ============================================================

function DashboardPageContent() {
  const featureFlags = useFeatureFlagService();
  const isDemoMode = featureFlags.isEnabled('DEMO_MODE');
  const navigate = useNavigate();
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());

  const {
    data: dashboard,
    isLoading,
    error,
    refetch,
    isFetching,
  } = useQuery({
    queryKey: queryKeys.dashboard.summary,
    queryFn: fetchDashboard,
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
        <Typography variant="h6" sx={{ color: tokens.colors.error.main, mb: 1 }}>
          Erro ao carregar dashboard
        </Typography>
        <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>
          Verifique se o backend está rodando.
        </Typography>
      </Card>
    );
  }

  // Map API data
  const healthCards = dashboard?.health_cards || [];
  const kpis = dashboard?.kpis || {};
  const activities = dashboard?.recent_activities || [];
  const alerts = dashboard?.operational_alerts || [];
  const upcomingActions = dashboard?.upcoming_actions || [];
  const currentPeriod = dashboard?.current_period;

  // Derive operational state
  const criticalAlerts = alerts.filter((a: any) => a.severity === 'critical' || a.severity === 'high');
  const operationalState = criticalAlerts.length > 0 ? 'critical' : kpis.coverage_rate < 90 ? 'attention' : 'healthy';

  // Map health cards to operational cards
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

  // Map upcoming actions
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
      {/* Header Operacional */}
      <ContentTransition visible={!isLoading}>
        <InstitutionStatusBar
          competency={currentPeriod?.name}
          coverage={kpis.coverage_rate}
          lastSync={lastRefresh.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
          operationalState={operationalState as 'healthy' | 'attention' | 'critical'}
        />
      </ContentTransition>

      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <AutoRefreshIndicator lastRefresh={lastRefresh} isRefreshing={isFetching} />
      </Box>

      {/* Alertas Críticos */}
      {!isLoading && criticalAlerts.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <CriticalAlertCard
            alerts={criticalAlerts.map((a: any) => ({
              alert_id: a.alert_id || `alert-${Math.random()}`,
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

      {/* Health Cards — 4 Operational Cards clicáveis */}
      <Grid container spacing={2} sx={{ mt: 2 }}>
        {(isLoading ? Array.from({ length: 4 }) : cardLevels).map((card: any, index: number) => (
          <Grid size={{ xs: 12, sm: 6, md: 3 }} key={card?.card_id || index}
            sx={{ animation: `fadeInUp 300ms ease-out ${index * 50}ms both` }}>
            {isLoading ? (
              <SkeletonCard />
            ) : (
              <OperationalHealthCard
                title={card.label}
                value={card.value}
                level={card.level}
                trend={card.trend_direction}
                trendValue={card.detail}
                detail={card.detail}
                route={card.route}
                percentage={card.percentage}
              />
            )}
          </Grid>
        ))}
      </Grid>

      {/* Grid Variado — Health Cards + Próximas Ações */}
      <Grid container spacing={2} sx={{ mt: 2 }}>
        {/* Resumo Operacional */}
        <Grid size={{ xs: 12, md: 8 }}>
          <ContentTransition visible={!isLoading}>
            <Card>
              <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600, color: tokens.colors.text.primary, mb: 1.5 }}>
                  RESUMO OPERACIONAL
                </Typography>
                {isLoading ? (
                  <Stack spacing={1}>
                    {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} variant="text" height={24} />)}
                  </Stack>
                ) : (
                  <Stack spacing={1}>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>Total de Plantões</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{kpis.total_shifts || 0}</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>Cobertura</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{kpis.coverage_rate ? `${kpis.coverage_rate}%` : '0%'}</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>Médicos Ativos</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{kpis.active_doctors || 0}</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" sx={{ color: tokens.colors.text.secondary }}>Total de Horas</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{kpis.total_hours || 0}h</Typography>
                    </Stack>
                  </Stack>
                )}
              </CardContent>
            </Card>
          </ContentTransition>
        </Grid>

        {/* Próximas Ações */}
        <Grid size={{ xs: 12, md: 4 }}>
          <ContentTransition visible={!isLoading}>
            {isLoading ? (
              <SkeletonCard height={200} />
            ) : (
              <UpcomingActionCard
                actions={mappedActions}
                onAction={(route) => navigate(route)}
              />
            )}
          </ContentTransition>
        </Grid>
      </Grid>

      {/* Últimos Eventos */}
      {!isLoading && activities.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <ContentTransition visible={!isLoading}>
            <Card>
              <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600, color: tokens.colors.text.primary, mb: 1.5 }}>
                  ÚLTIMOS EVENTOS
                </Typography>
                <List dense disablePadding>
                  {activities.slice(0, 5).map((activity: any, index: number) => (
                    <ListItem key={activity.activity_id || index} sx={{ px: 0, py: 0.5 }}>
                      <ListItemAvatar sx={{ minWidth: 40 }}>
                        <Avatar sx={{
                          width: 28, height: 28,
                          bgcolor: activity.severity === 'critical' ? tokens.colors.operational.critical
                            : activity.severity === 'warning' ? tokens.colors.operational.attention
                            : tokens.colors.primary.main + '15',
                          color: activity.severity === 'critical' ? tokens.colors.operational.critical
                            : activity.severity === 'warning' ? tokens.colors.operational.attention
                            : tokens.colors.primary.main,
                        }}>
                          <EventNoteIcon sx={{ fontSize: 14 }} />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={activity.description}
                        secondary={activity.timestamp}
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 500 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </ContentTransition>
        </Box>
      )}

      {/* Painel de Métricas Operacionais */}
      {!isLoading && (
        <Box sx={{ mt: 2 }}>
          <ContentTransition visible={!isLoading}>
            <OperationalMetricsPanel
              coverage={{
                percentage: kpis.coverage_rate || 0,
                level: getOperationalLevel(kpis.coverage_rate >= 90 ? 'healthy' : kpis.coverage_rate >= 70 ? 'warning' : 'critical'),
                covered: Math.round((kpis.coverage_rate || 0) * (kpis.total_shifts || 180) / 100),
                total: kpis.total_shifts || 180,
              }}
              doctors={{
                active: kpis.active_doctors || 0,
                total: (kpis.active_doctors || 0) + 1,
                inactive: 1,
                level: 'healthy',
              }}
              shifts={{
                total: kpis.total_shifts || 0,
                distribution: [
                  { label: 'T1', count: 22, color: tokens.colors.info.main },
                  { label: 'T2', count: 20, color: tokens.colors.info.main },
                  { label: 'T3', count: 18, color: '#5A2FA0' },
                  { label: 'R1', count: 15, color: tokens.colors.primary.main },
                  { label: 'R2', count: 13, color: tokens.colors.primary.main },
                ],
                uncovered: criticalAlerts.length,
                level: criticalAlerts.length > 0 ? 'critical' : 'healthy',
              }}
              competency={{
                name: currentPeriod?.name || '—',
                progress: 62,
                level: 'healthy',
                daysElapsed: 19,
                totalDays: 30,
              }}
              extras={{
                pending: 5,
                approved: 7,
                payrollStatus: 'Pendente',
                level: 'attention',
              }}
            />
          </ContentTransition>
        </Box>
      )}

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
