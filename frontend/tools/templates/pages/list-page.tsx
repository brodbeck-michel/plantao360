/**
 * {{FEATURE_PASCAL}} List Page — Plantão 360
 *
 * Página de listagem de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React, { useState, useMemo } from 'react';
import { Box, Alert } from '@mui/material';
import {{FEATURE_PASCAL}}Header } from '../components/{{FEATURE_NAME}}-header';
import {{FEATURE_PASCAL}}Toolbar } from '../components/{{FEATURE_NAME}}-toolbar';
import {{FEATURE_PASCAL}}Table } from '../tables/{{FEATURE_NAME}}-table';
import {{FEATURE_PASCAL}}FilterBar } from '../filters/{{FEATURE_NAME}}-filter-bar';
import { {{FEATURE_PASCAL}}CreateDialog } from '../dialogs/{{FEATURE_NAME}}-create-dialog';
import { {{FEATURE_PASCAL}}EditDialog } from '../dialogs/{{FEATURE_NAME}}-edit-dialog';
import { {{FEATURE_PASCAL}}DeleteDialog } from '../dialogs/{{FEATURE_NAME}}-delete-dialog';
import { LoadingSpinner } from '../../../shared/components/loading-spinner';
import { EmptyState } from '../../../shared/components/empty-state';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import {
  use{{FEATURE_PASCAL}}sList, use{{FEATURE_PASCAL}}Filters, use{{FEATURE_PASCAL}}Sort,
  use{{FEATURE_PASCAL}}Pagination, use{{FEATURE_PASCAL}}Selection,
} from '../hooks/use-{{FEATURE_NAME}}s';
import type { {{FEATURE_PASCAL}} } from '../types/{{FEATURE_NAME}}-types';

export function {{FEATURE_PASCAL}}ListPage() {
  const { filters, updateFilter, clearFilters } = use{{FEATURE_PASCAL}}Filters();
  const { sort, updateSort } = use{{FEATURE_PASCAL}}Sort();
  const { page, pageSize, updatePage, updatePageSize } = use{{FEATURE_PASCAL}}Pagination();
  const { selectedIds, updateSelection } = use{{FEATURE_PASCAL}}Selection();

  const [createOpen, setCreateOpen] = useState(false);
  const [editItem, setEditItem] = useState<{{FEATURE_PASCAL}} | null>(null);
  const [deleteItem, setDeleteItem] = useState<{{FEATURE_PASCAL}} | null>(null);

  const queryParams = useMemo(() => ({
    page: page + 1, page_size: pageSize, ...filters,
    sort_by: sort.field, sort_order: sort.direction,
  }), [page, pageSize, filters, sort]);

  const { data, isLoading, error } = use{{FEATURE_PASCAL}}sList(queryParams);
  const items = data?.data || [];
  const total = data?.total || 0;

  if (error) {
    return (
      <Box p={3}>
        {{FEATURE_PASCAL}}Header />
        <Alert severity="error">Erro ao carregar dados.</Alert>
      </Box>
    );
  }

  return (
    <ErrorBoundary>
      <Box p={3}>
        {{FEATURE_PASCAL}}Header actions={
          {{FEATURE_PASCAL}}Toolbar total={total} onCreate={() => setCreateOpen(true)} selectedCount={selectedIds.length} />
        } />
        {{FEATURE_PASCAL}}FilterBar filters={filters} onFilterChange={updateFilter} onClear={clearFilters} />
        {isLoading ? (
          <LoadingSpinner message="Carregando..." />
        ) : items.length === 0 ? (
          <EmptyState title="Nenhum registro encontrado" actionLabel="Novo" onAction={() => setCreateOpen(true)} />
        ) : (
          {{FEATURE_PASCAL}}Table items={items} total={total} page={page} pageSize={pageSize}
            onPageChange={updatePage} onPageSizeChange={updatePageSize} onSortChange={updateSort}
            onEdit={setEditItem} onDelete={setDeleteItem} />
        )}
        {{FEATURE_PASCAL}}CreateDialog open={createOpen} onClose={() => setCreateOpen(false)} />
        {editItem && {{FEATURE_PASCAL}}EditDialog open={!!editItem} item={editItem} onClose={() => setEditItem(null)} />}
        {deleteItem && {{FEATURE_PASCAL}}DeleteDialog open={!!deleteItem} item={deleteItem} onClose={() => setDeleteItem(null)} />}
      </Box>
    </ErrorBoundary>
  );
}
