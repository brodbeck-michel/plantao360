/**
 * {{FEATURE_PASCAL}} Header — Plantão 360
 *
 * Cabeçalho da página de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { PageHeader } from '../../../shared/components/page-header';
import { ROUTES } from '../../../routes/routes';

interface {{FEATURE_PASCAL}}HeaderProps {
  subtitle?: string;
  actions?: React.ReactNode;
}

export function {{FEATURE_PASCAL}}Header({ subtitle, actions }: {{FEATURE_PASCAL}}HeaderProps) {
  return (
    <PageHeader
      title="{{FEATURE_PASCAL}}"
      subtitle={subtitle || 'Gestão de {{FEATURE_NAME}} do sistema'}
      breadcrumbs={[
        { label: 'Home', path: ROUTES.DASHBOARD },
        { label: '{{FEATURE_PASCAL}}' },
      ]}
      actions={actions}
    />
  );
}
