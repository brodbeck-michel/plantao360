/**
 * use{{FEATURE_PASCAL}}s Hook — Plantão 360
 *
 * Hooks para gerenciar {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {{ feature_camel }}Queries, {{ feature_camel }}Mutations } from '../services/{{FEATURE_NAME}}-api';
import { queryKeys } from '../../../services/query-keys';
import type { {{FEATURE_PASCAL}}Filters, {{FEATURE_PASCAL}}ListSort } from '../types/{{FEATURE_NAME}}-types';

// Query Hooks
export function use{{FEATURE_PASCAL}}sList(params?: any) {
  return useQuery({{ feature_camel }}Queries.list(params));
}

export function use{{FEATURE_PASCAL}}Detail(id: string) {
  return useQuery({{ feature_camel }}Queries.detail(id));
}

// Mutation Hooks
export function useCreate{{FEATURE_PASCAL}}() {
  const queryClient = useQueryClient();
  return useMutation({
    ...{{ feature_camel }}Mutations.create(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.{{FEATURE_NAME}}.all });
    },
  });
}

export function useUpdate{{FEATURE_PASCAL}}() {
  const queryClient = useQueryClient();
  return useMutation({
    ...{{ feature_camel }}Mutations.update(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.{{FEATURE_NAME}}.all });
    },
  });
}

export function useDelete{{FEATURE_PASCAL}}() {
  const queryClient = useQueryClient();
  return useMutation({
    ...{{ feature_camel }}Mutations.delete(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.{{FEATURE_NAME}}.all });
    },
  });
}

// State Hooks
export function use{{FEATURE_PASCAL}}Filters() {
  const [filters, setFilters] = useState<{{FEATURE_PASCAL}}Filters>({});
  const updateFilter = useCallback((partial: Partial<{{FEATURE_PASCAL}}Filters>) => {
    setFilters((prev) => ({ ...prev, ...partial }));
  }, []);
  const clearFilters = useCallback(() => { setFilters({}); }, []);
  return { filters, updateFilter, clearFilters };
}

export function use{{FEATURE_PASCAL}}Sort() {
  const [sort, setSort] = useState<{{FEATURE_PASCAL}}ListSort>({ field: 'name', direction: 'asc' });
  const updateSort = useCallback((field: string, direction: 'asc' | 'desc') => {
    setSort({ field: field as any, direction });
  }, []);
  return { sort, updateSort };
}

export function use{{FEATURE_PASCAL}}Pagination() {
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const updatePage = useCallback((newPage: number) => setPage(newPage), []);
  const updatePageSize = useCallback((newPageSize: number) => { setPageSize(newPageSize); setPage(0); }, []);
  return { page, pageSize, updatePage, updatePageSize };
}

export function use{{FEATURE_PASCAL}}Selection() {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const updateSelection = useCallback((ids: string[]) => setSelectedIds(ids), []);
  const clearSelection = useCallback(() => setSelectedIds([]), []);
  return { selectedIds, updateSelection, clearSelection };
}
