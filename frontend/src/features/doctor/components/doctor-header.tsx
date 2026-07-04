/**
 * DoctorHeader — Plantão 360
 *
 * Cabeçalho da página de médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { PageHeader } from '../../../shared/components/page-header';
import { ROUTES } from '../../../routes/routes';

// ============================================================
// Types
// ============================================================

interface DoctorHeaderProps {
  subtitle?: string;
  actions?: React.ReactNode;
}

// ============================================================
// Component
// ============================================================

export function DoctorHeader({ subtitle, actions }: DoctorHeaderProps) {
  return (
    <PageHeader
      title="Médicos"
      subtitle={subtitle || 'Gestão de médicos do sistema'}
      breadcrumbs={[
        { label: 'Home', path: ROUTES.DASHBOARD },
        { label: 'Médicos' },
      ]}
      actions={actions}
    />
  );
}
