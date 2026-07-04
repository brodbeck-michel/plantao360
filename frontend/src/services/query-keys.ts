/**
 * Query Keys — Plantão 360
 *
 * Chaves padronizadas para React Query. Garantem consistência
 * e facilitam invalidação de cache.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

// ============================================================
// Base Keys
// ============================================================

export const queryKeys = {
  // Health
  health: ['health'] as const,

  // Doctors
  doctors: {
    all: ['doctors'] as const,
    lists: () => [...queryKeys.doctors.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.doctors.lists(), filters] as const,
    details: () => [...queryKeys.doctors.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.doctors.details(), id] as const,
  },

  // Periods
  periods: {
    all: ['periods'] as const,
    lists: () => [...queryKeys.periods.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.periods.lists(), filters] as const,
    details: () => [...queryKeys.periods.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.periods.details(), id] as const,
  },

  // Shifts
  shifts: {
    all: ['shifts'] as const,
    lists: () => [...queryKeys.shifts.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.shifts.lists(), filters] as const,
    details: () => [...queryKeys.shifts.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.shifts.details(), id] as const,
  },

  // Assignments
  assignments: {
    all: ['assignments'] as const,
    lists: () => [...queryKeys.assignments.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.assignments.lists(), filters] as const,
    details: () => [...queryKeys.assignments.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.assignments.details(), id] as const,
  },

  // Extras
  extras: {
    all: ['extras'] as const,
    lists: () => [...queryKeys.extras.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.extras.lists(), filters] as const,
    details: () => [...queryKeys.extras.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.extras.details(), id] as const,
  },

  // Coverage
  coverage: {
    all: ['coverage'] as const,
    lists: () => [...queryKeys.coverage.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.coverage.lists(), filters] as const,
    details: () => [...queryKeys.coverage.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.coverage.details(), id] as const,
  },

  // Payroll
  payroll: {
    all: ['payroll'] as const,
    lists: () => [...queryKeys.payroll.all, 'list'] as const,
    list: (filters: Record<string, unknown>) =>
      [...queryKeys.payroll.lists(), filters] as const,
    details: () => [...queryKeys.payroll.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.payroll.details(), id] as const,
    readiness: (id: string) =>
      [...queryKeys.payroll.all, 'readiness', id] as const,
  },

  // Query Domain
  query: {
    doctors: (filters?: Record<string, unknown>) =>
      ['query', 'doctors', filters] as const,
    coverage: (filters?: Record<string, unknown>) =>
      ['query', 'coverage', filters] as const,
    financial: (filters?: Record<string, unknown>) =>
      ['query', 'financial', filters] as const,
    payroll: (filters?: Record<string, unknown>) =>
      ['query', 'payroll', filters] as const,
    timeline: (filters?: Record<string, unknown>) =>
      ['query', 'timeline', filters] as const,
    dashboard: (filters?: Record<string, unknown>) =>
      ['query', 'dashboard', filters] as const,
  },

  // Dashboard
  dashboard: {
    all: ['dashboard'] as const,
    summary: ['dashboard', 'summary'] as const,
  },

  // KPIs
  kpi: {
    coverage: ['kpi', 'coverage'] as const,
    financial: ['kpi', 'financial'] as const,
    payroll: ['kpi', 'payroll'] as const,
    operational: ['kpi', 'operational'] as const,
  },

  // Analytics
  analytics: {
    explain: (params?: Record<string, unknown>) =>
      ['analytics', 'explain', params] as const,
    audit: (params?: Record<string, unknown>) =>
      ['analytics', 'audit', params] as const,
    timeline: (params?: Record<string, unknown>) =>
      ['analytics', 'timeline', params] as const,
    reports: ['analytics', 'reports'] as const,
  },
} as const;
