/**
 * {{FEATURE_PASCAL}} Table — Plantão 360
 *
 * Tabela de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Link } from '@mui/material';
import { DataTable, Column } from '../../../shared/components/data-table';
import { StatusChip } from '../../../shared/components/status-chip';
import { EntityAvatar } from '../../../shared/components/entity-avatar';
import { ActionsMenu, ActionItem } from '../../../shared/components/actions-menu';
import { Edit, Delete, Visibility } from '@mui/icons-material';
import type { {{FEATURE_PASCAL}} } from '../types/{{FEATURE_NAME}}-types';
import { ROUTES } from '../../../routes/routes';

interface {{FEATURE_PASCAL}}TableProps {
  items: {{FEATURE_PASCAL}}[];
  total: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  onSortChange?: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
  onEdit: (item: {{FEATURE_PASCAL}}) => void;
  onDelete: (item: {{FEATURE_PASCAL}}) => void;
}

export function {{FEATURE_PASCAL}}Table({ items, total, page, pageSize, onPageChange, onPageSizeChange, onSortChange, onEdit, onDelete }: {{FEATURE_PASCAL}}TableProps) {
  const navigate = useNavigate();

  const columns: Column<any>[] = [
    {
      id: 'name', label: 'Nome', sortable: true,
      render: (row) => (
        <Box display="flex" alignItems="center" gap={1.5}>
          <EntityAvatar name={row.name} size="small" />
          <Link component="button" variant="body2" fontWeight={600}
            onClick={() => navigate(`${ROUTES.{{FEATURE_NAME.upper()}}}/${row.id}`)}>
            {row.name}
          </Link>
        </Box>
      ),
    },
    {
      id: 'active', label: 'Status', sortable: true, align: 'center', width: 100,
      render: (row) => <StatusChip status={row.active ? 'active' : 'inactive'} />,
    },
    {
      id: 'actions', label: '', align: 'right', width: 50,
      render: (row) => (
        <ActionsMenu actions={[
          { id: 'view', label: 'Visualizar', icon: <Visibility fontSize="small" />, onClick: () => navigate(`${ROUTES.{{FEATURE_NAME.upper()}}}/${row.id}`) },
          { id: 'edit', label: 'Editar', icon: <Edit fontSize="small" />, onClick: () => onEdit(row) },
          { id: 'delete', label: 'Excluir', icon: <Delete fontSize="small" />, onClick: () => onDelete(row), color: 'error', divider: true },
        ]} />
      ),
    },
  ];

  return (
    <DataTable columns={columns} data={items} total={total} page={page} pageSize={pageSize}
      onPageChange={onPageChange} onPageSizeChange={onPageSizeChange} onSortChange={onSortChange}
      emptyMessage="Nenhum registro encontrado" />
  );
}
