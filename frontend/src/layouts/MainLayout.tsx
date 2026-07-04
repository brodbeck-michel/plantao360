/**
 * MainLayout — Plantao 360
 * Collapsible sidebar with pin/unpin, hover expand, localStorage persistence.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar, Box, Drawer, IconButton, List, ListItemButton, ListItemIcon,
  ListItemText, Toolbar, Typography, Badge, Avatar, Tooltip, Divider,
  Chip, InputBase, Breadcrumbs, Link, useTheme, Skeleton, Stack,
} from '@mui/material';
import {
  Menu as MenuIcon, Search as SearchIcon, Notifications as NotificationsIcon,
  Help as HelpIcon, LightMode as LightModeIcon, DarkMode as DarkModeIcon,
  Dashboard as DashboardIcon, Assignment as AssignmentIcon,
  CalendarMonth as CalendarMonthIcon, EventNote as EventNoteIcon,
  PersonAdd as PersonAddIcon, HealthAndSafety as HealthAndSafetyIcon,
  AddCircle as AddCircleIcon, People as PeopleIcon,
  LocalHospital as LocalHospitalIcon, Receipt as ReceiptIcon,
  Insights as InsightsIcon, Timeline as TimelineIcon,
  Description as DescriptionIcon, AttachMoney as AttachMoneyIcon,
  ChevronRight as ChevronRightIcon, ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon, Sync as SyncIcon, Circle as CircleIcon,
  PushPin as PinIcon, PushPinOutlined as PinOutlinedIcon,
  ChevronLeft as ChevronLeftIcon, ChevronRight as ChevronRightIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { ROUTES, NAV_ITEMS, type NavItem } from '../routes/routes';
import { FEATURE_FLAGS } from '../config';
import { tokens } from '../theme';

const DRAWER_WIDTH = 280;
const DRAWER_COLLAPSED_WIDTH = 64;

const iconMap: Record<string, React.ReactNode> = {
  Dashboard: <DashboardIcon />, Assignment: <AssignmentIcon />,
  CalendarMonth: <CalendarMonthIcon />, EventNote: <EventNoteIcon />,
  PersonAdd: <PersonAddIcon />, HealthAndSafety: <HealthAndSafetyIcon />,
  AddCircle: <AddCircleIcon />, People: <PeopleIcon />,
  LocalHospital: <LocalHospitalIcon />, Receipt: <ReceiptIcon />,
  Insights: <InsightsIcon />, Timeline: <TimelineIcon />,
  Description: <DescriptionIcon />, AttachMoney: <AttachMoneyIcon />,
};

const segmentLabelMap: Record<string, string> = {
  dashboard: 'Dashboard', doctors: 'Medicos', periods: 'Competencias',
  shifts: 'Plantoes', assignments: 'Distribuicao', coverage: 'Cobertura',
  extras: 'Extras', payroll: 'Financeiro', analytics: 'Analytics',
};

async function fetchDashboardContext() {
  const response = await fetch('/api/v1/query/dashboard?include_health_cards=false&include_recent_activities=false&include_operational_alerts=false&include_upcoming_actions=false');
  if (!response.ok) return null;
  const json = await response.json();
  return json.data ?? json;
}

function SidebarOperationalContext({ collapsed }: { collapsed: boolean }) {
  const { data, isLoading } = useQuery({
    queryKey: ['dashboard', 'context'],
    queryFn: fetchDashboardContext,
    refetchInterval: 60000,
    staleTime: 30000,
  });

  if (collapsed) return null;

  if (isLoading) {
    return (
      <Box sx={{ px: 2, py: 1.5 }}>
        <Skeleton variant="text" width="70%" height={16} />
        <Skeleton variant="text" width="50%" height={14} sx={{ mt: 0.5 }} />
      </Box>
    );
  }

  if (!data?.current_period) return null;

  const period = data.current_period;
  const kpis = data.kpis || {};
  const coverage = kpis.coverage_rate || 0;
  const alertCount = data.operational_alerts?.length || 0;
  const statusLevel = alertCount > 0 ? 'critical' : coverage < 90 ? 'attention' : 'healthy';
  const statusCfg = {
    healthy: { color: tokens.colors.operational.healthy, label: 'Operacao Normal', bg: tokens.colors.operational.healthyBg },
    attention: { color: tokens.colors.operational.attention, label: 'Atencao', bg: tokens.colors.operational.attentionBg },
    critical: { color: tokens.colors.operational.critical, label: 'Critico', bg: tokens.colors.operational.criticalBg },
  }[statusLevel];

  return (
    <Box sx={{ px: 2, py: 1.5 }}>
      <Stack direction="row" alignItems="center" spacing={0.75} sx={{ mb: 1.5 }}>
        <LocalHospitalIcon sx={{ fontSize: 16, color: tokens.colors.primary.main }} />
        <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.primary }}>
          PS Unimed Tubarao
        </Typography>
      </Stack>
      <Box sx={{
        display: 'flex', alignItems: 'center', gap: 0.75, p: 1,
        borderRadius: tokens.borderRadius.md, bgcolor: statusCfg.bg,
        border: `1px solid ${statusCfg.color}30`, mb: 1.5,
      }}>
        <CircleIcon sx={{ fontSize: 8, color: statusCfg.color }} />
        <Typography variant="caption" sx={{ fontWeight: 600, color: statusCfg.color, flex: 1 }}>
          {statusCfg.label}
        </Typography>
        {alertCount > 0 && (
          <Chip label={alertCount} size="small" sx={{
            height: 18, fontSize: '0.6rem', fontWeight: 700,
            bgcolor: tokens.colors.operational.critical, color: '#fff', minWidth: 24,
          }} />
        )}
      </Box>
      <Stack spacing={0.75}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>Competencia</Typography>
          <Typography variant="caption" sx={{ fontWeight: 600, color: tokens.colors.text.primary }}>{period.name}</Typography>
        </Stack>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>Cobertura</Typography>
          <Typography variant="caption" sx={{ fontWeight: 600, color: coverage < 90 ? tokens.colors.operational.attention : tokens.colors.text.primary }}>
            {coverage}%
          </Typography>
        </Stack>
      </Stack>
      <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1.5, pt: 1, borderTop: `1px solid ${tokens.colors.grey[200]}` }}>
        <SyncIcon sx={{ fontSize: 12, color: tokens.colors.text.muted }} />
        <Typography variant="caption" sx={{ color: tokens.colors.text.muted, fontSize: '0.65rem' }}>
          Sync: {new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
        </Typography>
      </Stack>
    </Box>
  );
}

export default function MainLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    Operacional: true, 'Gestao de Pessoal': false, Financeiro: false, Analytics: false,
  });
  const [collapsed, setCollapsed] = useState(() => {
    return localStorage.getItem('sidebar_collapsed') === 'true';
  });
  const [pinned, setPinned] = useState(() => {
    return localStorage.getItem('sidebar_pinned') === 'true';
  });
  const [hoverExpanded, setHoverExpanded] = useState(false);
  const hoverTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();

  const isExpanded = !collapsed || hoverExpanded;
  const currentWidth = isExpanded ? DRAWER_WIDTH : DRAWER_COLLAPSED_WIDTH;

  const visibleNavItems = FEATURE_FLAGS.MVP_MODE
    ? NAV_ITEMS.reduce<NavItem[]>((acc, item) => {
        if (item.path === ROUTES.DASHBOARD) {
          acc.push(item);
        } else if (item.label === 'Operacional' && item.children) {
          acc.push({
            ...item,
            children: item.children.filter((c) =>
              c.path === ROUTES.WORKSPACE || c.path === ROUTES.PERIODS
            ),
          });
        }
        return acc;
      }, [])
    : NAV_ITEMS;

  const handleToggleCollapse = useCallback(() => {
    const newCollapsed = !collapsed;
    setCollapsed(newCollapsed);
    localStorage.setItem('sidebar_collapsed', String(newCollapsed));
    if (newCollapsed) {
      setHoverExpanded(false);
      setPinned(false);
      localStorage.setItem('sidebar_pinned', 'false');
    }
  }, [collapsed]);

  const handleTogglePin = useCallback(() => {
    const newPinned = !pinned;
    setPinned(newPinned);
    localStorage.setItem('sidebar_pinned', String(newPinned));
    if (newPinned && collapsed) {
      setCollapsed(false);
      localStorage.setItem('sidebar_collapsed', 'false');
    } else if (!newPinned && !collapsed) {
      setCollapsed(true);
      localStorage.setItem('sidebar_collapsed', 'true');
    }
  }, [pinned, collapsed]);

  const handleMouseEnter = useCallback(() => {
    if (!pinned && collapsed) {
      if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current);
      hoverTimerRef.current = setTimeout(() => setHoverExpanded(true), 200);
    }
  }, [pinned, collapsed]);

  const handleMouseLeave = useCallback(() => {
    if (!pinned) {
      if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current);
      hoverTimerRef.current = setTimeout(() => setHoverExpanded(false), 300);
    }
  }, [pinned]);

  useEffect(() => {
    return () => { if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current); };
  }, []);

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);
  const toggleSection = (label: string) => setExpandedSections((prev) => ({ ...prev, [label]: !prev[label] }));
  const isActive = (path: string) => location.pathname === path;
  const isChildActive = (children?: NavItem[]) => children?.some((c) => location.pathname === c.path) ?? false;

  useEffect(() => {
    const expanded: Record<string, boolean> = { Operacional: true, 'Gestao de Pessoal': false, Financeiro: false, Analytics: false };
    NAV_ITEMS.forEach((item) => {
      if (item.children?.some((child) => location.pathname === child.path)) expanded[item.label] = true;
    });
    setExpandedSections(expanded);
  }, [location.pathname]);

  const drawerContent = (
    <Box
      sx={{ display: 'flex', flexDirection: 'column', height: '100%', width: currentWidth, transition: 'width 200ms ease' }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <Toolbar sx={{ px: isExpanded ? 2 : 1, minHeight: '56px !important', justifyContent: isExpanded ? 'flex-start' : 'center' }}>
        {isExpanded ? (
          <Box display="flex" alignItems="center" gap={1} sx={{ flex: 1 }}>
            <Box sx={{
              width: 40, height: 36, borderRadius: tokens.borderRadius.md,
              display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
              overflow: 'hidden',
            }}>
              <img src="/logo.png" alt="Unimed Tubarão" style={{ height: 36, objectFit: 'contain' }} />
            </Box>
            <Box sx={{ overflow: 'hidden' }}>
              <Typography variant="subtitle1" fontWeight={700} sx={{ color: tokens.colors.primary.dark, whiteSpace: 'nowrap' }}>
                Plantao 360
              </Typography>
              <Typography variant="caption" sx={{ color: tokens.colors.text.muted, fontSize: '0.65rem', whiteSpace: 'nowrap' }}>
                PS Unimed Tubarao
              </Typography>
            </Box>
          </Box>
        ) : (
          <Tooltip title="Plantao 360" placement="right">
            <Box sx={{
              width: 40, height: 36, borderRadius: tokens.borderRadius.md,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              overflow: 'hidden',
            }}>
              <img src="/logo.png" alt="Unimed Tubarão" style={{ height: 36, objectFit: 'contain' }} />
            </Box>
          </Tooltip>
        )}
      </Toolbar>
      <Divider sx={{ borderColor: tokens.colors.grey[200] }} />
      <SidebarOperationalContext collapsed={!isExpanded} />
      <Divider sx={{ borderColor: tokens.colors.grey[200] }} />

      <Box sx={{ px: 0.5, mt: 0.5, display: 'flex', justifyContent: 'center', gap: 0.5 }}>
        {isExpanded ? (
          <>
            <Tooltip title={pinned ? 'Desafixar sidebar' : 'Fixar sidebar'} placement="right">
              <IconButton size="small" onClick={handleTogglePin} sx={{ color: tokens.colors.text.muted, '&:hover': { color: tokens.colors.primary.main } }}>
                {pinned ? <PinIcon sx={{ fontSize: 18 }} /> : <PinOutlinedIcon sx={{ fontSize: 18 }} />}
              </IconButton>
            </Tooltip>
            <Tooltip title="Recolher sidebar" placement="right">
              <IconButton size="small" onClick={handleToggleCollapse} sx={{ color: tokens.colors.text.muted, '&:hover': { color: tokens.colors.primary.main } }}>
                <ChevronLeftIcon sx={{ fontSize: 18 }} />
              </IconButton>
            </Tooltip>
          </>
        ) : (
          <Tooltip title="Expandir sidebar" placement="right">
            <IconButton size="small" onClick={handleToggleCollapse} sx={{ color: tokens.colors.text.muted, '&:hover': { color: tokens.colors.primary.main } }}>
              <ChevronRightIcon sx={{ fontSize: 18 }} />
            </IconButton>
          </Tooltip>
        )}
      </Box>

      <List component="nav" sx={{ px: isExpanded ? 1 : 0.5, flex: 1, overflowY: 'auto', overflowX: 'hidden' }}>
        {visibleNavItems.map((item) => {
          if (!item.children || item.children.length === 0) {
            const active = isActive(item.path);
            const btn = (
              <ListItemButton key={item.label} selected={active} disabled={item.path === ''}
                onClick={() => { if (item.path) { navigate(item.path); setMobileOpen(false); } }}
                sx={{ borderRadius: tokens.borderRadius.md, mb: 0.5, position: 'relative', transition: 'all 150ms ease',
                  justifyContent: isExpanded ? 'flex-start' : 'center', px: isExpanded ? undefined : 1.5,
                  '&:hover': { bgcolor: tokens.colors.primary.main + '08' },
                  '&.Mui-selected': { bgcolor: tokens.colors.primary.main + '12',
                    '&::before': { content: '""', position: 'absolute', left: 0, top: '20%', bottom: '20%', width: 3, borderRadius: '0 3px 3px 0', bgcolor: tokens.colors.primary.main },
                  },
                }}>
                <ListItemIcon sx={{ minWidth: isExpanded ? 40 : 0, justifyContent: 'center', color: active ? tokens.colors.primary.main : tokens.colors.text.secondary }}>
                  {iconMap[item.icon] || <DashboardIcon />}
                </ListItemIcon>
                {isExpanded && <ListItemText primary={item.label} primaryTypographyProps={{ fontWeight: active ? 600 : 400, fontSize: '0.875rem' }} />}
              </ListItemButton>
            );
            return isExpanded ? btn : (
              <Tooltip key={item.label} title={item.label} placement="right">{btn}</Tooltip>
            );
          }
          const isSecExpanded = isExpanded ? (expandedSections[item.label] ?? false) : false;
          const sectionActive = isChildActive(item.children);
          const sectionBtn = (
            <ListItemButton key={item.label} selected={sectionActive} onClick={() => { if (isExpanded) toggleSection(item.label); else { navigate(item.children?.find(c => c.path)?.path || ''); } }}
              sx={{ borderRadius: tokens.borderRadius.md, mb: 0.5, transition: 'all 150ms ease',
                justifyContent: isExpanded ? 'flex-start' : 'center', px: isExpanded ? undefined : 1.5,
                '&:hover': { bgcolor: tokens.colors.primary.main + '08' },
              }}>
              <ListItemIcon sx={{ minWidth: isExpanded ? 40 : 0, justifyContent: 'center', color: sectionActive ? tokens.colors.primary.main : tokens.colors.text.secondary }}>
                {iconMap[item.icon] || <DashboardIcon />}
              </ListItemIcon>
              {isExpanded && (
                <>
                  <ListItemText primary={item.label} primaryTypographyProps={{ fontWeight: sectionActive ? 600 : 400, fontSize: '0.875rem' }} />
                  {isSecExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                </>
              )}
            </ListItemButton>
          );

          return (
            <Box key={item.label}>
              {isExpanded ? sectionBtn : (
                <Tooltip title={item.label} placement="right">{sectionBtn}</Tooltip>
              )}
              {isSecExpanded && isExpanded && (
                <List component="div" disablePadding sx={{ pl: 2 }}>
                  {item.children.map((child) => {
                    const childActive = isActive(child.path);
                    return (
                      <ListItemButton key={child.label} selected={childActive} disabled={child.path === ''}
                        onClick={() => { if (child.path) { navigate(child.path); setMobileOpen(false); } }}
                        sx={{ borderRadius: tokens.borderRadius.md, mb: 0.25, transition: 'all 150ms ease',
                          '&:hover': { bgcolor: tokens.colors.primary.main + '08' },
                          '&.Mui-selected': { bgcolor: tokens.colors.primary.main + '12',
                            '&::before': { content: '""', position: 'absolute', left: 0, top: '20%', bottom: '20%', width: 3, borderRadius: '0 3px 3px 0', bgcolor: tokens.colors.primary.main },
                          },
                        }}>
                        <ListItemText primary={
                          <Box display="flex" alignItems="center" gap={1}>
                            <Typography variant="body2" fontWeight={childActive ? 600 : 400} fontSize="0.8125rem">
                              {child.label}
                            </Typography>
                          </Box>
                        } />
                      </ListItemButton>
                    );
                  })}
                </List>
              )}
            </Box>
          );
        })}
      </List>
    </Box>
  );

  const getBreadcrumbs = () => {
    const segments = location.pathname.split('/').filter(Boolean);
    const crumbs: Array<{ label: string; path: string }> = [];
    if (segments[0] === 'app') {
      crumbs.push({ label: 'Inicio', path: ROUTES.DASHBOARD });
      if (segments[1]) {
        const label = segmentLabelMap[segments[1]] || segments[1];
        if (segments.length > 2 && segments[2] !== 'new') {
          crumbs.push({ label, path: `/${segments[0]}/${segments[1]}` });
          const last = segments[segments.length - 1];
          crumbs.push({ label: last === 'edit' ? 'Editar' : `Detalhes #${segments[2]}`, path: location.pathname });
        } else {
          crumbs.push({ label, path: `/${segments.slice(0, 2).join('/')}` });
        }
      }
    }
    return crumbs;
  };

  const breadcrumbs = getBreadcrumbs();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{
        width: { sm: `calc(100% - ${currentWidth}px)` }, ml: { sm: `${currentWidth}px` },
        bgcolor: tokens.colors.background.paper, color: tokens.colors.text.primary,
        borderBottom: `1px solid ${tokens.colors.grey[200]}`, boxShadow: 'none',
        transition: 'width 200ms ease, margin 200ms ease',
      }}>
        <Toolbar sx={{ minHeight: '56px !important' }}>
          <IconButton color="inherit" edge="start" onClick={handleDrawerToggle} sx={{ mr: 2, display: { sm: 'none' } }}>
            <MenuIcon />
          </IconButton>
          {isExpanded && (
            <Tooltip title="Pesquisar (Ctrl+K)">
              <Box sx={{
                display: 'flex', alignItems: 'center', bgcolor: tokens.colors.grey[50],
                borderRadius: tokens.borderRadius.md, px: 1.5, py: 0.5, minWidth: 200,
                maxWidth: 400, flex: 1, border: `1px solid ${tokens.colors.grey[200]}`,
                cursor: 'pointer', transition: 'all 150ms ease',
                '&:hover': { borderColor: tokens.colors.primary.main + '40', bgcolor: '#fff' },
              }}>
                <SearchIcon sx={{ color: tokens.colors.text.muted, mr: 1, fontSize: 20 }} />
                <InputBase placeholder="Pesquisar..." sx={{ flex: 1, fontSize: '0.875rem', color: tokens.colors.text.muted }} disabled />
                <Chip label="Ctrl+K" size="small" sx={{ height: 20, fontSize: '0.6rem', bgcolor: tokens.colors.grey[100], color: tokens.colors.text.muted, fontWeight: 600 }} />
              </Box>
            </Tooltip>
          )}
          <Box sx={{ flexGrow: 1 }} />
          <Box display="flex" alignItems="center" gap={0.5}>
            <Tooltip title="Notificacoes">
              <IconButton color="inherit" sx={{ color: tokens.colors.text.secondary }}>
                <Badge badgeContent={3} color="error" max={99}><NotificationsIcon fontSize="small" /></Badge>
              </IconButton>
            </Tooltip>
            <Tooltip title="Ajuda">
              <IconButton color="inherit" sx={{ color: tokens.colors.text.secondary }}><HelpIcon fontSize="small" /></IconButton>
            </Tooltip>
            <Tooltip title="Alternar tema">
              <IconButton color="inherit" sx={{ color: tokens.colors.text.secondary }}>
                {theme.palette.mode === 'dark' ? <LightModeIcon fontSize="small" /> : <DarkModeIcon fontSize="small" />}
              </IconButton>
            </Tooltip>
            <Tooltip title="Perfil">
              <IconButton color="inherit" sx={{ color: tokens.colors.text.secondary }}>
                <Avatar sx={{ width: 32, height: 32, bgcolor: tokens.colors.primary.main, color: '#fff', fontSize: '0.875rem', fontWeight: 600 }}>CO</Avatar>
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      <Box component="nav" sx={{ width: { sm: currentWidth }, flexShrink: { sm: 0 }, transition: 'width 200ms ease' }}>
        <Drawer variant="temporary" open={mobileOpen} onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH } }}>
          {drawerContent}
        </Drawer>
        <Drawer variant="permanent" sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: currentWidth, borderRight: `1px solid ${tokens.colors.grey[200]}`, transition: 'width 200ms ease', overflowX: 'hidden' },
        }} open>
          {drawerContent}
        </Drawer>
      </Box>

      <Box component="main" sx={{
        flexGrow: 1, width: { sm: `calc(100% - ${currentWidth}px)` },
        bgcolor: tokens.colors.background.default, minHeight: '100vh',
        transition: 'width 200ms ease',
      }}>
        <Toolbar />
        {breadcrumbs.length > 1 && (
          <Box sx={{ px: 3, pt: 2, pb: 0 }}>
            <Breadcrumbs separator={<ChevronRightIcon fontSize="small" />} sx={{ fontSize: '0.8rem' }}>
              {breadcrumbs.map((crumb, index) => {
                const isLast = index === breadcrumbs.length - 1;
                return isLast ? (
                  <Typography key={crumb.path} color="text.primary" fontWeight={500}>{crumb.label}</Typography>
                ) : (
                  <Link key={crumb.path} component="button" variant="body2"
                    onClick={() => navigate(crumb.path)}
                    sx={{ textDecoration: 'none', cursor: 'pointer' }}>
                    {crumb.label}
                  </Link>
                );
              })}
            </Breadcrumbs>
          </Box>
        )}
        <Box sx={{ p: 3 }}><Outlet /></Box>
      </Box>
    </Box>
  );
}
