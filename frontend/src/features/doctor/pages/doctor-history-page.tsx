/**
 * DoctorHistoryPage — Plantão 360
 *
 * Página de histórico do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { DoctorHeader } from '../components/doctor-header';
import { DoctorHistoryTimeline } from '../history/doctor-history-timeline';
import { LoadingSpinner } from '../../../shared/components/loading-spinner';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import { useDoctorDetail } from '../hooks/use-doctors';
import { ROUTES } from '../../../routes/routes';

// ============================================================
// Component
// ============================================================

export function DoctorHistoryPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: doctor, isLoading } = useDoctorDetail(id!);

  if (isLoading) {
    return <LoadingSpinner message="Carregando histórico..." />;
  }

  return (
    <ErrorBoundary>
      <Box p={3}>
        <DoctorHeader
          subtitle={`Histórico de ${doctor?.name || 'Médico'}`}
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
        <DoctorHistoryTimeline events={[]} />
      </Box>
    </ErrorBoundary>
  );
}
