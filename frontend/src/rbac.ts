/**
 * RBAC Permission Matrix — Plantão 360
 * Maps user roles (from backend) to module access.
 */

export type BackendRole = 'ADMIN' | 'COORDENADOR' | 'FINANCEIRO' | 'MEDICO' | 'CONSULTA';

export type ModuleKey =
  | 'dashboard'
  | 'workspace'
  | 'competencias'
  | 'turnos'
  | 'medicos'
  | 'financeiro'
  | 'relatorios'
  | 'usuarios';

type AccessLevel = 'full' | 'view' | 'none';

const MATRIX: Record<BackendRole, Record<ModuleKey, AccessLevel>> = {
  ADMIN: {
    dashboard: 'full',
    workspace: 'full',
    competencias: 'full',
    turnos: 'full',
    medicos: 'full',
    financeiro: 'full',
    relatorios: 'full',
    usuarios: 'full',
  },
  COORDENADOR: {
    dashboard: 'full',
    workspace: 'full',
    competencias: 'full',
    turnos: 'full',
    medicos: 'full',
    financeiro: 'view',
    relatorios: 'full',
    usuarios: 'none',
  },
  FINANCEIRO: {
    dashboard: 'full',
    workspace: 'none',
    competencias: 'none',
    turnos: 'none',
    medicos: 'view',
    financeiro: 'full',
    relatorios: 'full',
    usuarios: 'none',
  },
  MEDICO: {
    dashboard: 'full',
    workspace: 'full',
    competencias: 'view',
    turnos: 'view',
    medicos: 'view',
    financeiro: 'none',
    relatorios: 'view',
    usuarios: 'none',
  },
  CONSULTA: {
    dashboard: 'full',
    workspace: 'view',
    competencias: 'view',
    turnos: 'view',
    medicos: 'view',
    financeiro: 'none',
    relatorios: 'view',
    usuarios: 'none',
  },
};

export function getModuleAccess(role: BackendRole, module: ModuleKey): AccessLevel {
  return MATRIX[role]?.[module] ?? 'none';
}

export function canAccess(role: BackendRole, module: ModuleKey): boolean {
  return getModuleAccess(role, module) !== 'none';
}

export function canEdit(role: BackendRole, module: ModuleKey): boolean {
  return getModuleAccess(role, module) === 'full';
}

export function canView(role: BackendRole, module: ModuleKey): boolean {
  return getModuleAccess(role, module) !== 'none';
}
