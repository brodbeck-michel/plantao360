/**
 * DoctorListPage — Plantão 360
 *
 * Página de listagem de médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React, { useState, useMemo } from 'react';
import { Box, Snackbar, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { DoctorHeader } from '../components/doctor-header';
import { DoctorToolbar } from '../components/doctor-toolbar';
import { DoctorFilterBar } from '../filters/doctor-filter-bar';
import { DoctorTable } from '../tables/doctor-table';
import { DoctorCreateDialog } from '../dialogs/doctor-create-dialog';
import { DoctorEditDialog } from '../dialogs/doctor-edit-dialog';
import { DoctorDeleteDialog } from '../dialogs/doctor-delete-dialog';
import { DoctorDeactivateDialog } from '../dialogs/doctor-deactivate-dialog';
import { LoadingSpinner } from '../../../shared/components/loading-spinner';
import { EmptyState } from '../../../shared/components/empty-state';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import {
  useDoctorList, useDoctorFilters, useDoctorSort, useDoctorPagination, useDoctorSelection,
} from '../hooks/use-doctors';
import type { Doctor } from '../types/doctor-types';
import { ROUTES } from '../../../routes/routes';

// ============================================================
// Component
// ============================================================

export function DoctorListPage() {
  const navigate = useNavigate();
  const { filters, updateFilter, clearFilters } = useDoctorFilters();
  const { sort, updateSort } = useDoctorSort();
  const { page, pageSize, updatePage, updatePageSize } = useDoctorPagination();
  const { selectedIds, updateSelection, clearSelection } = useDoctorSelection();

  const [createOpen, setCreateOpen] = useState(false);
  const [editDoctor, setEditDoctor] = useState<Doctor | null>(null);
  const [deleteDoctor, setDeleteDoctor] = useState<Doctor | null>(null);
  const [deactivateDoctor, setDeactivateDoctor] = useState<Doctor | null>(null);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false, message: '', severity: 'success',
  });

  const queryParams = useMemo(() => ({
    page: page + 1,
    page_size: pageSize,
    name: filters.name,
    crm: filters.crm,
    specialty: filters.specialty,
    active: filters.active,
    sort_by: sort.field,
    sort_order: sort.direction,
  }), [page, pageSize, filters, sort]);

  const { data, isLoading, error } = useDoctorList(queryParams);

  const doctors = data?.data || [];
  const total = data?.total || 0;

  if (error) {
    return (
      <Box p={3}>
        <DoctorHeader />
        <Alert severity="error" role="alert">
          Erro ao carregar médicos. Tente novamente.
        </Alert>
      </Box>
    );
  }

  return (
    <ErrorBoundary>
      <Box p={3}>
        <DoctorHeader
          actions={
            <DoctorToolbar
              total={total}
              onCreate={() => setCreateOpen(true)}
              selectedCount={selectedIds.length}
            />
          }
        />

        <DoctorFilterBar
          filters={filters}
          onFilterChange={updateFilter}
          onClear={clearFilters}
        />

        {isLoading ? (
          <LoadingSpinner message="Carregando médicos..." />
        ) : doctors.length === 0 ? (
          <EmptyState
            title="Nenhum médico encontrado"
            description="Crie um novo médico para começar."
            actionLabel="Novo Médico"
            onAction={() => setCreateOpen(true)}
          />
        ) : (
          <DoctorTable
            doctors={doctors}
            total={total}
            page={page}
            pageSize={pageSize}
            sortBy={sort.field}
            sortOrder={sort.direction}
            selectable
            selectedIds={selectedIds}
            onPageChange={updatePage}
            onPageSizeChange={updatePageSize}
            onSortChange={updateSort}
            onSelectionChange={updateSelection}
            onEdit={(doctor) => setEditDoctor(doctor)}
            onDelete={(doctor) => setDeleteDoctor(doctor)}
            onDeactivate={(doctor) => setDeactivateDoctor(doctor)}
          />
        )}

        {/* Dialogs */}
        <DoctorCreateDialog open={createOpen} onClose={() => setCreateOpen(false)} />
        {editDoctor && (
          <DoctorEditDialog open={!!editDoctor} doctor={editDoctor} onClose={() => setEditDoctor(null)} />
        )}
        {deleteDoctor && (
          <DoctorDeleteDialog open={!!deleteDoctor} doctor={deleteDoctor} onClose={() => setDeleteDoctor(null)} />
        )}
        {deactivateDoctor && (
          <DoctorDeactivateDialog open={!!deactivateDoctor} doctor={deactivateDoctor} onClose={() => setDeactivateDoctor(null)} />
        )}

        {/* Snackbar */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert severity={snackbar.severity} onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}>
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </ErrorBoundary>
  );
}
