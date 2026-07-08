/**
 * DoctorTable — Plantão 360
 *
 * Tabela específica de médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Link } from '@mui/material';
import { DataTable, Column } from '../../../shared/components/data-table';
import { StatusChip } from '../../../shared/components/status-chip';
import { EntityAvatar } from '../../../shared/components/entity-avatar';
import { ActionsMenu, ActionItem } from '../../../shared/components/actions-menu';
import { Edit, Delete, Visibility, Block } from '@mui/icons-material';
import type { Doctor } from '../types/doctor-types';
import { ROUTES } from '../../../routes/routes';
import { useAuth } from '../../../contexts/AuthContext';
import { canEdit } from '../../../rbac';

// ============================================================
// Types
// ============================================================

interface DoctorTableProps {
  doctors: Doctor[];
  total: number;
  page: number;
  pageSize: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  loading?: boolean;
  selectable?: boolean;
  selectedIds?: string[];
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  onSortChange?: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
  onSelectionChange?: (ids: string[]) => void;
  onEdit: (doctor: Doctor) => void;
  onDelete: (doctor: Doctor) => void;
  onDeactivate: (doctor: Doctor) => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorTable({
  doctors,
  total,
  page,
  pageSize,
  sortBy,
  sortOrder,
  loading,
  selectable,
  selectedIds,
  onPageChange,
  onPageSizeChange,
  onSortChange,
  onSelectionChange,
  onEdit,
  onDelete,
  onDeactivate,
}: DoctorTableProps) {
  const navigate = useNavigate();
  const { user } = useAuth();
  const canModify = canEdit(user?.role, 'medicos');

  const getActions = (doctor: Doctor): ActionItem[] => {
    const actions: ActionItem[] = [
      {
        id: 'view',
        label: 'Visualizar',
        icon: <Visibility fontSize="small" />,
        onClick: () => navigate(`${ROUTES.DOCTORS}/${doctor.id}`),
      },
    ];
    if (canModify) {
      actions.push(
        {
          id: 'edit',
          label: 'Editar',
          icon: <Edit fontSize="small" />,
          onClick: () => onEdit(doctor),
        },
        {
          id: 'deactivate',
          label: doctor.active ? 'Desativar' : 'Ativar',
          icon: <Block fontSize="small" />,
          onClick: () => onDeactivate(doctor),
          divider: true,
        },
        {
          id: 'delete',
          label: 'Excluir',
          icon: <Delete fontSize="small" />,
          onClick: () => onDelete(doctor),
          color: 'error',
        },
      );
    }
    return actions;
  };

  const columns: Column<Doctor>[] = [
    {
      id: 'name',
      label: 'Nome',
      sortable: true,
      render: (row) => (
        <Box display="flex" alignItems="center" gap={1.5}>
          <EntityAvatar name={row.name} size="small" />
          <Link
            component="button"
            variant="body2"
            fontWeight={600}
            onClick={() => navigate(`${ROUTES.DOCTORS}/${row.id}`)}
            sx={{ textDecoration: 'none', cursor: 'pointer' }}
          >
            {row.name}
          </Link>
        </Box>
      ),
    },
    {
      id: 'crm',
      label: 'CRM',
      sortable: true,
      width: 120,
      render: (row) => (
        <Typography variant="body2" fontFamily="monospace">
          {row.crm}
        </Typography>
      ),
    },
    {
      id: 'specialty',
      label: 'Especialidade',
      sortable: true,
      render: (row) => row.specialty,
    },
    {
      id: 'email',
      label: 'E-mail',
      render: (row) => row.email,
    },
    {
      id: 'active',
      label: 'Status',
      sortable: true,
      align: 'center',
      width: 100,
      render: (row) => <StatusChip status={row.active ? 'active' : 'inactive'} />,
    },
    {
      id: 'actions',
      label: '',
      align: 'right',
      width: 50,
      render: (row) => <ActionsMenu actions={getActions(row)} ariaLabel={`Ações de ${row.name}`} />,
    },
  ];

  return (
    <DataTable
      columns={columns}
      data={doctors as unknown as Record<string, unknown>[]}
      total={total}
      page={page}
      pageSize={pageSize}
      sortBy={sortBy}
      sortOrder={sortOrder}
      loading={loading}
      selectable={selectable}
      selectedIds={selectedIds}
      onPageChange={onPageChange}
      onPageSizeChange={onPageSizeChange}
      onSortChange={onSortChange}
      onSelectionChange={onSelectionChange}
      emptyMessage="Nenhum médico encontrado"
    />
  );
}
