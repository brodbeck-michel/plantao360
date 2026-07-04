/**
 * Theme — Plantão 360
 *
 * Design tokens e tema MUI para toda a aplicação.
 * Identidade visual: Unimed Tubarão (#00995D).
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import { createTheme, responsiveFontSizes } from '@mui/material/styles';
import { ptBR } from '@mui/material/locale';

// ============================================================
// Design Tokens v2
// ============================================================

export const tokens = {
  colors: {
    // ── Unimed Brand ──────────────────────────────────────────
    primary: {
      main: '#00995D',
      light: '#00B87A',
      dark: '#007A47',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#0A1628',
      light: '#1E293B',
      dark: '#020817',
      contrastText: '#FFFFFF',
    },

    // ── Semantic Operational ──────────────────────────────────
    operational: {
      healthy: '#00B87A',
      healthyBg: '#E6F7EF',
      healthyBorder: '#A7F3D0',
      attention: '#FFB020',
      attentionBg: '#FFF8E1',
      attentionBorder: '#FDE68A',
      critical: '#FF4842',
      criticalBg: '#FFEBEE',
      criticalBorder: '#FECACA',
      informative: '#1B6FE0',
      informativeBg: '#EFF6FF',
      informativeBorder: '#BFDBFE',
    },

    // ── MUI Semantic ──────────────────────────────────────────
    success: {
      main: '#00B87A',
      light: '#A7F3D0',
      dark: '#007A47',
    },
    warning: {
      main: '#FFB020',
      light: '#FDE68A',
      dark: '#D97706',
    },
    error: {
      main: '#FF4842',
      light: '#FECACA',
      dark: '#DC2626',
    },
    info: {
      main: '#1B6FE0',
      light: '#BFDBFE',
      dark: '#1E40AF',
    },

    // ── Neutrals ──────────────────────────────────────────────
    grey: {
      50: '#F7F8FA',
      100: '#F1F3F5',
      200: '#E5E7EB',
      300: '#D1D5DB',
      400: '#9CA3AF',
      500: '#6B7280',
      600: '#4B5563',
      700: '#374151',
      800: '#1F2937',
      900: '#111827',
    },
    background: {
      default: '#F7F8FA',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#1A1A2E',
      secondary: '#6B7280',
      muted: '#9CA3AF',
    },
  },

  // ── Spacing ───────────────────────────────────────────────
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
  },

  // ── Border Radius ─────────────────────────────────────────
  borderRadius: {
    none: '0px',
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    chip: '24px',
    full: '9999px',
  },

  // ── Elevation (with color tinting) ────────────────────────
  elevation: {
    none: 'none',
    sm: '0 1px 3px rgba(0,153,93,0.06), 0 1px 2px rgba(0,0,0,0.04)',
    md: '0 4px 6px rgba(0,153,93,0.07), 0 2px 4px rgba(0,0,0,0.04)',
    lg: '0 10px 15px rgba(0,153,93,0.08), 0 4px 6px rgba(0,0,0,0.04)',
    xl: '0 20px 25px rgba(0,153,93,0.10), 0 8px 10px rgba(0,0,0,0.04)',
    glow: '0 0 20px rgba(0,153,93,0.15)',
  },

  // ── Typography ────────────────────────────────────────────
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontSize: '2.5rem', fontWeight: 700, lineHeight: 1.2 },
    h2: { fontSize: '2rem', fontWeight: 600, lineHeight: 1.3 },
    h3: { fontSize: '1.5rem', fontWeight: 600, lineHeight: 1.3 },
    h4: { fontSize: '1.25rem', fontWeight: 600, lineHeight: 1.4 },
    h5: { fontSize: '1rem', fontWeight: 600, lineHeight: 1.4 },
    h6: { fontSize: '0.875rem', fontWeight: 600, lineHeight: 1.4 },
    body1: { fontSize: '1rem', fontWeight: 400, lineHeight: 1.6 },
    body2: { fontSize: '0.875rem', fontWeight: 400, lineHeight: 1.5 },
    caption: { fontSize: '0.75rem', fontWeight: 400, lineHeight: 1.4 },
    kpi: { fontSize: '2.5rem', fontWeight: 700, lineHeight: 1.0, fontVariantNumeric: 'tabular-nums' },
  },

  // ── Breakpoints ───────────────────────────────────────────
  breakpoints: {
    mobile: 768,
    tablet: 1024,
    desktop: 1280,
  },

  // ── Transitions ───────────────────────────────────────────
  transition: {
    fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
    normal: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
    slow: '500ms cubic-bezier(0.4, 0, 0.2, 1)',
  },

  // ── Z-Index Scale ─────────────────────────────────────────
  zIndex: {
    sidebar: 1200,
    appBar: 1100,
    dropdown: 1100,
    modal: 1300,
    toast: 1400,
    tooltip: 1500,
  },
} as const;

// ============================================================
// Dark Mode Tokens (prepared, not applied)
// ============================================================

export const darkTokens = {
  colors: {
    primary: tokens.colors.primary,
    secondary: { main: '#94A3B8', light: '#CBD5E1', dark: '#64748B', contrastText: '#0F172A' },
    background: { default: '#0F172A', paper: '#1E293B' },
    text: { primary: '#F1F5F9', secondary: '#94A3B8' },
    grey: {
      50: '#1E293B', 100: '#334155', 200: '#475569', 300: '#64748B',
      400: '#94A3B8', 500: '#CBD5E1', 600: '#E2E8F0', 700: '#F1F5F9',
      800: '#F8FAFC', 900: '#FFFFFF',
    },
  },
  elevation: {
    none: 'none',
    sm: '0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)',
    md: '0 4px 6px rgba(0,0,0,0.35), 0 2px 4px rgba(0,0,0,0.2)',
    lg: '0 10px 15px rgba(0,0,0,0.4), 0 4px 6px rgba(0,0,0,0.2)',
    xl: '0 20px 25px rgba(0,0,0,0.45), 0 8px 10px rgba(0,0,0,0.2)',
  },
} as const;

// ============================================================
// MUI Theme
// ============================================================

let theme = createTheme({
  palette: {
    primary: tokens.colors.primary,
    secondary: tokens.colors.secondary,
    success: tokens.colors.success,
    warning: tokens.colors.warning,
    error: tokens.colors.error,
    info: tokens.colors.info,
    grey: tokens.colors.grey,
    background: tokens.colors.background,
    text: tokens.colors.text,
  },
  typography: {
    fontFamily: tokens.typography.fontFamily,
    h1: tokens.typography.h1,
    h2: tokens.typography.h2,
    h3: tokens.typography.h3,
    h4: tokens.typography.h4,
    h5: tokens.typography.h5,
    h6: tokens.typography.h6,
    body1: tokens.typography.body1,
    body2: tokens.typography.body2,
    caption: tokens.typography.caption,
  },
  shape: {
    borderRadius: 8,
  },
  spacing: 8,
  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
          padding: '8px 16px',
          transition: tokens.transition.fast,
          '&:hover': {
            transform: 'translateY(-1px)',
          },
          '&:active': {
            transform: 'translateY(0px) scale(0.98)',
          },
        },
      },
    },
    MuiCard: {
      defaultProps: {
        elevation: 0,
      },
      styleOverrides: {
        root: {
          border: '1px solid #E5E7EB',
          borderRadius: 12,
          transition: tokens.transition.normal,
          '&:hover': {
            boxShadow: tokens.elevation.sm,
            borderColor: '#D1D5DB',
          },
        },
      },
    },
    MuiChip: {
      defaultProps: {
        variant: 'filled',
      },
      styleOverrides: {
        root: {
          borderRadius: 24,
          fontWeight: 600,
          fontSize: '0.75rem',
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
        size: 'small',
      },
    },
    MuiFormControl: {
      defaultProps: {
        variant: 'outlined',
        size: 'small',
      },
    },
    MuiSkeleton: {
      defaultProps: {
        animation: 'wave',
      },
    },
  },
}, ptBR);

theme = responsiveFontSizes(theme);

export { theme };
export default theme;
