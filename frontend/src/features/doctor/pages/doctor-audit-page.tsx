/**
 * DoctorAuditPage — Plantão 360
 *
 * Página de auditoria do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { DoctorHeader } from '../components/doctor-header';
import { DoctorAuditCard } from '../audit/doctor-audit-card';
import { LoadingSpinner } from '../../../shared/components/loading-spinner';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import { useDoctorDetail } from '../hooks/use-doctors';
import { ROUTES } from '../../../routes/routes';

// ============================================================
// Component
// ============================================================

export function DoctorAuditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: doctor, isLoading } = useDoctorDetail(id!);

  if (isLoading) {
    return <LoadingSpinner message="Carregando auditoria..." />;
  }

  return (
    <ErrorBoundary>
      <Box p={3}>
        <DoctorHeader
          subtitle={`Auditoria de ${doctor?.name || 'Médico'}`}
          actions={
            <Button
              startIcon={<ArrowBack />}
              onClick={() => navigate(`${ROUTES.DOCTORS}/${id}`)}
              variant="outlined"
              size="small"
            >
              Voltar
            </Button>
          }
        />
        <DoctorAuditCard entries={[]} />
      </Box>
    </ErrorBoundary>
  );
}
