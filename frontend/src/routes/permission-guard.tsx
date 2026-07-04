/**
 * Permission Guard — Plantão 360
 *
 * Guard de permissões para rotas protegidas.
 * Baseado na Access Matrix (Sprint 11).
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import type { Persona } from '../../types';

// ============================================================
// Types
// ============================================================

interface PermissionGuardProps {
  children: React.ReactNode;
  allowedPersonas: Persona[];
  currentPersona?: Persona;
  fallbackPath?: string;
}

// ============================================================
// Component
// ============================================================

export function PermissionGuard({
  children,
  allowedPersonas,
  currentPersona,
  fallbackPath = '/app/dashboard',
}: PermissionGuardProps) {
  if (!currentPersona || !allowedPersonas.includes(currentPersona)) {
    return <Navigate to={fallbackPath} replace />;
  }

  return <>{children}</>;
}

// ============================================================
// Persona Constants
// ============================================================

export const ALL_PERSONAS: Persona[] = [
  'coordenador',
  'medico',
  'financeiro',
  'rh',
  'auditor',
  'administrador',
  'diretor',
];

export const COORDENADOR_PERSONAS: Persona[] = ['coordenador', 'administrador'];
export const MEDICO_PERSONAS: Persona[] = ['medico', 'coordenador', 'administrador'];
export const FINANCEIRO_PERSONAS: Persona[] = ['financeiro', 'administrador', 'diretor'];
export const ADMIN_PERSONAS: Persona[] = ['administrador'];
export const AUDITOR_PERSONAS: Persona[] = ['auditor', 'administrador', 'diretor'];
