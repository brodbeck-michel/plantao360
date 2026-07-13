/**
 * DoctorDetailPage — Plantão 360
 *
 * Página de detalhes do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Grid, Tabs, Tab, Button, Snackbar, Alert } from '@mui/material';
import { Edit, ArrowBack } from '@mui/icons-material';
import { DoctorHeader } from '../components/doctor-header';
import { DoctorDetailsPanel } from '../details/doctor-details-panel';
import { DoctorHistoryTimeline } from '../history/doctor-history-timeline';
import { DoctorAuditCard } from '../audit/doctor-audit-card';
import { DoctorEditDialog } from '../dialogs/doctor-edit-dialog';
import { DoctorDeleteDialog } from '../dialogs/doctor-delete-dialog';
import { DoctorDeactivateDialog } from '../dialogs/doctor-deactivate-dialog';
import { LoadingSpinner } from '../../../shared/components/loading-spinner';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import { useDoctorDetail, useDoctorSummary } from '../hooks/use-doctors';
import { ROUTES } from '../../../routes/routes';
import { useAuth } from '../../../contexts/AuthContext';
import { canEdit } from '../../../rbac';
import { useBreadcrumbLabel } from '../../../contexts/BreadcrumbContext';

// ============================================================
// Types
// ============================================================

interface TabPanelProps {
  children: React.ReactNode;
  value: number;
  index: number;
}

function TabPanel({ children, value, index }: TabPanelProps) {
  return value === index ? <Box role="tabpanel">{children}</Box> : null;
}

// ============================================================
// Component
// ============================================================

export function DoctorDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const canModify = canEdit(user?.role, 'medicos');
  const [tab, setTab] = useState(0);
  const [editOpen, setEditOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deactivateOpen, setDeactivateOpen] = useState(false);

  const { data: doctor, isLoading: doctorLoading } = useDoctorDetail(id!);
  const { data: summary, isLoading: summaryLoading } = useDoctorSummary(id!);

  useBreadcrumbLabel(doctor?.name);

  const isLoading = doctorLoading || summaryLoading;

  if (isLoading) {
    return <LoadingSpinner message="Carregando médico..." />;
  }

  if (!doctor) {
    return (
      <Box p={3}>
        <DoctorHeader />
        <Alert severity="error" role="alert">
          Médico não encontrado.
        </Alert>
      </Box>
    );
  }

  return (
    <ErrorBoundary>
      <Box p={3}>
        <DoctorHeader
          subtitle={`${doctor.name} — ${doctor.specialty}`}
          actions={
            <Box display="flex" gap={1}>
              <Button
                startIcon={<ArrowBack />}
                onClick={() => navigate(ROUTES.DOCTORS)}
                variant="outlined"
                size="small"
              >
                Voltar
              </Button>
              {canModify && (
                <Button
                  startIcon={<Edit />}
                  onClick={() => setEditOpen(true)}
                  variant="outlined"
                  size="small"
                >
                  Editar
                </Button>
              )}
            </Box>
          }
        />

        <Box mb={3}>
          <Tabs value={tab} onChange={(_, newValue) => setTab(newValue)}>
            <Tab label="Detalhes" />
            <Tab label="Histórico" />
            <Tab label="Auditoria" />
          </Tabs>
        </Box>

        <TabPanel value={tab} index={0}>
          <DoctorDetailsPanel doctor={doctor} summary={summary} />
        </TabPanel>

        <TabPanel value={tab} index={1}>
          <DoctorHistoryTimeline events={[]} />
        </TabPanel>

        <TabPanel value={tab} index={2}>
          <DoctorAuditCard entries={[]} />
        </TabPanel>

        {/* Dialogs */}
        {editOpen && (
          <DoctorEditDialog open={editOpen} doctor={doctor} onClose={() => setEditOpen(false)} />
        )}
        <DoctorDeleteDialog open={deleteOpen} doctor={doctor} onClose={() => setDeleteOpen(false)} />
        <DoctorDeactivateDialog open={deactivateOpen} doctor={doctor} onClose={() => setDeactivateOpen(false)} />
      </Box>
    </ErrorBoundary>
  );
}
