/**
 * useDoctors — Plantão 360
 *
 * Hooks para gerenciar médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { doctorQueries, doctorMutations } from '../services/doctor-api';
import { queryKeys } from '../../../services/query-keys';
import type { DoctorListParams, CreateDoctorData, UpdateDoctorData } from '../services/doctor-api';
import type { DoctorFilters, DoctorListSort } from '../types/doctor-types';

// ============================================================
// Query Hooks — Separados de Mutations
// ============================================================

export function useDoctorList(params?: DoctorListParams) {
  return useQuery(doctorQueries.list(params));
}

export function useDoctorDetail(id: string) {
  return useQuery(doctorQueries.detail(id));
}

export function useDoctorSummary(id: string) {
  return useQuery(doctorQueries.summary(id));
}

// ============================================================
// Mutation Hooks
// ============================================================

export function useCreateDoctor() {
  const queryClient = useQueryClient();

  return useMutation({
    ...doctorMutations.create(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.doctors.all });
    },
  });
}

export function useUpdateDoctor() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateDoctorData) => {
      const { id, ...rest } = data;
      return doctorMutations.update().mutationFn(rest);
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.doctors.all });
      queryClient.invalidateQueries({ queryKey: queryKeys.doctors.detail(variables.id) });
    },
  });
}

export function useDeleteDoctor() {
  const queryClient = useQueryClient();

  return useMutation({
    ...doctorMutations.delete(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.doctors.all });
    },
  });
}

// ============================================================
// Composite Hooks — Filters, Search, History, Audit
// ============================================================

export function useDoctorFilters() {
  const [filters, setFilters] = useState<DoctorFilters>({});

  const updateFilter = useCallback((partial: Partial<DoctorFilters>) => {
    setFilters((prev) => ({ ...prev, ...partial }));
  }, []);

  const clearFilters = useCallback(() => {
    setFilters({});
  }, []);

  return { filters, updateFilter, clearFilters };
}

export function useDoctorSearch() {
  const [search, setSearch] = useState('');

  const updateSearch = useCallback((value: string) => {
    setSearch(value);
  }, []);

  return { search, updateSearch };
}

export function useDoctorSort() {
  const [sort, setSort] = useState<DoctorListSort>({ field: 'name', direction: 'asc' });

  const updateSort = useCallback((field: string, direction: 'asc' | 'desc') => {
    setSort({ field: field as DoctorListSort['field'], direction });
  }, []);

  return { sort, updateSort };
}

export function useDoctorPagination() {
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);

  const updatePage = useCallback((newPage: number) => {
    setPage(newPage);
  }, []);

  const updatePageSize = useCallback((newPageSize: number) => {
    setPageSize(newPageSize);
    setPage(0);
  }, []);

  return { page, pageSize, updatePage, updatePageSize };
}

export function useDoctorSelection() {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const updateSelection = useCallback((ids: string[]) => {
    setSelectedIds(ids);
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedIds([]);
  }, []);

  return { selectedIds, updateSelection, clearSelection };
}
