import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { periodQueries, periodMutations } from '../services/period-api';
import { queryKeys } from '../../../services/query-keys';
import type { PeriodListParams, CreatePeriodData, UpdatePeriodData } from '../types/period-types';

export function usePeriodList(params?: PeriodListParams) {
  return useQuery({
    ...periodQueries.list(params),
    select: (data) => {
      if (data && (data as any).data) {
        return (data as any).data;
      }
      return data;
    },
  });
}

export function usePeriodDetail(id: string) {
  return useQuery({
    ...periodQueries.detail(id),
    select: (data) => {
      if (data && (data as any).data) {
        return (data as any).data;
      }
      return data;
    },
  });
}

export function useCreatePeriod() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreatePeriodData) => periodMutations.create().mutationFn(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.periods.all });
    },
  });
}

export function useUpdatePeriod() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { id: number } & UpdatePeriodData) =>
      periodMutations.update().mutationFn(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.periods.all });
    },
  });
}

export function useDeletePeriod() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => periodMutations.delete().mutationFn(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.periods.all });
    },
  });
}

export function useClosePeriod() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => periodMutations.close().mutationFn(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.periods.all });
    },
  });
}

export function useReopenPeriod() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => periodMutations.reopen().mutationFn(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.periods.all });
    },
  });
}

export function useDuplicatePeriod() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => periodMutations.duplicate().mutationFn(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.periods.all });
    },
  });
}

export function usePeriodFilters() {
  const [filters, setFilters] = useState<PeriodListParams>({});
  const updateFilter = useCallback((partial: Partial<PeriodListParams>) => {
    setFilters((prev) => ({ ...prev, ...partial }));
  }, []);
  const clearFilters = useCallback(() => setFilters({}), []);
  return { filters, updateFilter, clearFilters };
}
