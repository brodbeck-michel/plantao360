/**
 * App Layout — Plantão 360
 *
 * Layout principal da aplicação com menu lateral e AppBar.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Collapse,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  CalendarMonth,
  EventNote,
  PersonAdd,
  HealthAndSafety,
  AddCircle,
  People,
  LocalHospital,
  Receipt,
  Analytics,
  Timeline,
  Description,
  ExpandLess,
  ExpandMore,
  AccountCircle,
  AttachMoney,
} from '@mui/icons-material';
import { ROUTES, NAV_ITEMS, NavItem } from '../routes/routes';

// ============================================================
// Constants
// ============================================================

const DRAWER_WIDTH = 260;
const DRAWER_COLLAPSED_WIDTH = 64;

// ============================================================
// Icon Map
// ============================================================

const iconMap: Record<string, React.ReactNode> = {
  Dashboard: <Dashboard />,
  CalendarMonth: <CalendarMonth />,
  EventNote: <EventNote />,
  PersonAdd: <PersonAdd />,
  HealthAndSafety: <HealthAndSafety />,
  AddCircle: <AddCircle />,
  People: <People />,
  LocalHospital: <LocalHospital />,
  Receipt: <Receipt />,
  Analytics: <Analytics />,
  Timeline: <Timeline />,
  Description: <Description />,
  AttachMoney: <AttachMoney />,
};

// ============================================================
// NavItem Component
// ============================================================

function NavItemComponent({ item, depth = 0 }: { item: NavItem; depth?: number }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const isActive = location.pathname === item.path;
  const hasChildren = item.children && item.children.length > 0;

  const handleClick = () => {
    if (hasChildren) {
      setOpen(!open);
    } else if (item.path) {
      navigate(item.path);
    }
  };

  return (
    <>
      <ListItemButton
        onClick={handleClick}
        selected={isActive}
        sx={{ pl: depth * 2 + 2 }}
      >
        <ListItemIcon>{iconMap[item.icon]}</ListItemIcon>
        <ListItemText primary={item.label} />
        {hasChildren && (open ? <ExpandLess /> : <ExpandMore />)}
      </ListItemButton>
      {hasChildren && (
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {item.children!.map((child) => (
              <NavItemComponent key={child.path} item={child} depth={depth + 1} />
            ))}
          </List>
        </Collapse>
      )}
    </>
  );
}

// ============================================================
// Layout Component
// ============================================================

export function AppLayout() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const drawerContent = (
    <Box>
      <Toolbar>
        <Typography variant="h6" noWrap fontWeight={700} color="primary">
          Plantão 360
        </Typography>
      </Toolbar>
      <List>
        {NAV_ITEMS.map((item) => (
          <NavItemComponent key={item.path || item.label} item={item} />
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* AppBar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          ml: { md: `${DRAWER_WIDTH}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ flexGrow: 1 }} />
          <IconButton color="inherit" onClick={handleMenuOpen}>
            <AccountCircle />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleMenuClose}>Meu Perfil</MenuItem>
            <MenuItem onClick={handleMenuClose}>Sair</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            '& .MuiDrawer-paper': { width: DRAWER_WIDTH },
          }}
        >
          {drawerContent}
        </Drawer>
      ) : (
        <Drawer
          variant="permanent"
          sx={{
            width: DRAWER_WIDTH,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: DRAWER_WIDTH,
              boxSizing: 'border-box',
            },
          }}
        >
          {drawerContent}
        </Drawer>
      )}

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          ml: { md: `${DRAWER_WIDTH}px` },
          mt: '64px',
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
}
