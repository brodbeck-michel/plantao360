/**
 * DataTable — Plantão 360
 *
 * Tabela genérica reutilizável.
 * Sprint: 13 — Golden Frontend Module
 */

import React, { useState } from 'react';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  TableSortLabel, TablePagination, Paper, Box, Checkbox,
  CircularProgress, Typography,
} from '@mui/material';

// ============================================================
// Types
// ============================================================

export interface Column<T> {
  id: string;
  label: string;
  sortable?: boolean;
  width?: number | string;
  align?: 'left' | 'center' | 'right';
  render: (row: T) => React.ReactNode;
}

export interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  total?: number;
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  loading?: boolean;
  selectable?: boolean;
  selectedIds?: string[];
  getRowId?: (row: T) => string;
  onPageChange?: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
  onSortChange?: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
  onSelectionChange?: (ids: string[]) => void;
  emptyMessage?: string;
}

// ============================================================
// Component
// ============================================================

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  total = 0,
  page = 0,
  pageSize = 10,
  sortBy,
  sortOrder = 'asc',
  loading = false,
  selectable = false,
  selectedIds = [],
  getRowId = (row: T) => row.id as string,
  onPageChange,
  onPageSizeChange,
  onSortChange,
  onSelectionChange,
  emptyMessage = 'Nenhum registro encontrado',
}: DataTableProps<T>) {
  const handleSort = (columnId: string) => {
    if (!onSortChange) return;
    const isCurrentSort = sortBy === columnId;
    onSortChange(columnId, isCurrentSort && sortOrder === 'asc' ? 'desc' : 'asc');
  };

  const handleSelectAll = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!onSelectionChange) return;
    if (event.target.checked) {
      onSelectionChange(data.map((row) => getRowId(row)));
    } else {
      onSelectionChange([]);
    }
  };

  const handleSelectRow = (id: string) => {
    if (!onSelectionChange) return;
    if (selectedIds.includes(id)) {
      onSelectionChange(selectedIds.filter((i) => i !== id));
    } else {
      onSelectionChange([...selectedIds, id]);
    }
  };

  const allSelected = data.length > 0 && selectedIds.length === data.length;
  const someSelected = selectedIds.length > 0 && selectedIds.length < data.length;

  return (
    <Paper variant="outlined">
      <TableContainer>
        <Table size="medium">
          <TableHead>
            <TableRow>
              {selectable && (
                <TableCell padding="checkbox">
                  <Checkbox
                    checked={allSelected}
                    indeterminate={someSelected}
                    onChange={handleSelectAll}
                    inputProps={{ 'aria-label': 'Selecionar todos' }}
                  />
                </TableCell>
              )}
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align || 'left'}
                  width={column.width}
                  sortDirection={sortBy === column.id ? sortOrder : false}
                >
                  {column.sortable ? (
                    <TableSortLabel
                      active={sortBy === column.id}
                      direction={sortBy === column.id ? sortOrder : 'asc'}
                      onClick={() => handleSort(column.id)}
                    >
                      {column.label}
                    </TableSortLabel>
                  ) : (
                    column.label
                  )}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={columns.length + (selectable ? 1 : 0)} align="center" sx={{ py: 8 }}>
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : data.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length + (selectable ? 1 : 0)} align="center" sx={{ py: 8 }}>
                  <Typography variant="body2" color="text.secondary">
                    {emptyMessage}
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              data.map((row) => {
                const id = getRowId(row);
                const isSelected = selectedIds.includes(id);
                return (
                  <TableRow
                    key={id}
                    hover
                    selected={isSelected}
                    role="row"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === ' ' || e.key === 'Enter') {
                        e.preventDefault();
                        handleSelectRow(id);
                      }
                    }}
                  >
                    {selectable && (
                      <TableCell padding="checkbox">
                        <Checkbox
                          checked={isSelected}
                          onChange={() => handleSelectRow(id)}
                          inputProps={{ 'aria-label': `Selecionar linha ${id}` }}
                        />
                      </TableCell>
                    )}
                    {columns.map((column) => (
                      <TableCell key={column.id} align={column.align || 'left'}>
                        {column.render(row)}
                      </TableCell>
                    ))}
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={total}
        page={page}
        rowsPerPage={pageSize}
        rowsPerPageOptions={[5, 10, 25, 50]}
        onPageChange={(_, newPage) => onPageChange?.(newPage)}
        onRowsPerPageChange={(event) => onPageSizeChange?.(parseInt(event.target.value, 10))}
        labelRowsPerPage="Linhas por página"
        labelDisplayedRows={({ from, to, count }) =>
          `${from}-${to} de ${count !== -1 ? count : `mais de ${to}`}`
        }
      />
    </Paper>
  );
}
