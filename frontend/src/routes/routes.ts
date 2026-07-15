/**
 * App Routes — Plantão 360
 *
 * Definição centralizada de todas as rotas da aplicação.
 * Baseado no Navigation Map (Sprint 11).
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

// ============================================================
// Route Constants
// ============================================================

export const ROUTES = {
  // Public
  HOME: '/',
  LOGIN: '/login',
  HEALTH: '/health',

  // App
  DASHBOARD: '/app/dashboard',
  WORKSPACE: '/app/workspace',

  // Doctors
  DOCTORS: '/app/doctors',
  DOCTOR_NEW: '/app/doctors/new',
  DOCTOR_DETAIL: '/app/doctors/:id',
  DOCTOR_EDIT: '/app/doctors/:id/edit',

  // Periods
  PERIODS: '/app/periods',
  PERIOD_NEW: '/app/periods/new',
  PERIOD_DETAIL: '/app/periods/:id',
  PERIOD_EDIT: '/app/periods/:id/edit',

  // Shifts
  SHIFTS: '/app/shifts',
  SHIFT_NEW: '/app/shifts/new',
  SHIFT_DETAIL: '/app/shifts/:id',
  SHIFT_EDIT: '/app/shifts/:id/edit',
  SHIFT_CALENDAR: '/app/shifts/calendar',

  // Assignments
  ASSIGNMENTS: '/app/assignments',
  ASSIGNMENT_NEW: '/app/assignments/new',
  ASSIGNMENT_DETAIL: '/app/assignments/:id',
  ASSIGNMENT_EDIT: '/app/assignments/:id/edit',

  // Coverage
  COVERAGE: '/app/coverage',

  // Extras
  EXTRAS: '/app/extras',
  EXTRA_NEW: '/app/extras/new',
  EXTRA_DETAIL: '/app/extras/:id',
  EXTRA_EDIT: '/app/extras/:id/edit',

  // Payroll (rota SPA viva no menu Financeiro; backend de payroll foi removido — spec 006)
  PAYROLL: '/app/payroll',

  // Analytics
  ANALYTICS: '/app/analytics',
  TIMELINE: '/app/analytics/timeline',
  REPORTS: '/app/analytics/reports',

  // Users (Admin only)
  USERS: '/app/users',
} as const;

// ============================================================
// Navigation Items
// ============================================================

export interface NavItem {
  label: string;
  path: string;
  icon: string;
  children?: NavItem[];
  roles?: string[];
}

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: ROUTES.DASHBOARD, icon: 'Dashboard' },
  {
    label: 'Operacional',
    path: '',
    icon: 'Assignment',
    children: [
      { label: 'Workspace', path: ROUTES.WORKSPACE, icon: 'Dashboard' },
      { label: 'Competencias', path: ROUTES.PERIODS, icon: 'CalendarMonth' },
      { label: 'Plantoes', path: ROUTES.SHIFTS, icon: 'EventNote' },
      { label: 'Cobertura', path: ROUTES.COVERAGE, icon: 'HealthAndSafety' },
      { label: 'Extras', path: ROUTES.EXTRAS, icon: 'AddCircle' },
    ],
  },
  {
    label: 'Gestão de Pessoal',
    path: '',
    icon: 'People',
    children: [
      { label: 'Médicos', path: ROUTES.DOCTORS, icon: 'LocalHospital' },
    ],
  },
  {
    label: 'Financeiro',
    path: '',
    icon: 'AttachMoney',
    roles: ['ADMIN', 'COORDENADOR', 'FINANCEIRO'],
    children: [
      { label: 'Payroll', path: ROUTES.PAYROLL, icon: 'Receipt' },
    ],
  },
  {
    label: 'Analytics',
    path: '',
    icon: 'Analytics',
    children: [
      { label: 'Dashboard', path: ROUTES.ANALYTICS, icon: 'Insights' },
      { label: 'Timeline', path: ROUTES.TIMELINE, icon: 'Timeline' },
      { label: 'Relatorios', path: ROUTES.REPORTS, icon: 'Description' },
    ],
  },
  {
    label: 'Sistema',
    path: '',
    icon: 'Settings',
    roles: ['ADMIN'],
    children: [
      { label: 'Usuarios', path: ROUTES.USERS, icon: 'People' },
    ],
  },
];
