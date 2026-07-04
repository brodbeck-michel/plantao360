import { apiClient } from '../../../api/client';
import { queryKeys } from '../../../services/query-keys';
import { createQuery, createMutation, createDynamicMutation, createPaginatedQuery } from '../../../services/query-factory';
import type { UseQueryOptions } from '@tanstack/react-query';
import type { AppError } from '../../../api/client';
import type { PeriodData, PeriodListParams, CreatePeriodData, UpdatePeriodData } from '../types/period-types';

export const periodQueries = {
  list: (params?: PeriodListParams) =>
    createPaginatedQuery<PeriodData>(
      queryKeys.periods.list(params || {}),
      '/periods',
      params
    ),

  detail: (id: string, options?: Omit<UseQueryOptions<{ data: PeriodData }, AppError>, 'queryKey' | 'queryFn'>) =>
    createQuery<{ data: PeriodData }>(
      queryKeys.periods.detail(id),
      `/periods/${id}`,
      options
    ),

  workspace: (id: string) =>
    createQuery<any>(
      [...queryKeys.periods.detail(id), 'workspace'],
      `/periods/${id}/workspace`
    ),
};

export const periodMutations = {
  create: () =>
    createMutation<PeriodData, CreatePeriodData>('/periods', 'POST'),

  update: () =>
    createDynamicMutation<PeriodData, { id: number } & UpdatePeriodData>(
      (data) => `/periods/${data.id}`,
      'PATCH'
    ),

  delete: () =>
    createDynamicMutation<any, number>(
      (id) => `/periods/${id}`,
      'DELETE'
    ),

  close: () =>
    createDynamicMutation<PeriodData, number>(
      (id) => `/periods/${id}/close`,
      'POST'
    ),

  reopen: () =>
    createDynamicMutation<PeriodData, number>(
      (id) => `/periods/${id}/reopen`,
      'POST'
    ),

  duplicate: () =>
    createDynamicMutation<any, number>(
      (id) => `/periods/${id}/duplicate`,
      'POST'
    ),

  copyFrom: () =>
    createDynamicMutation<any, { periodId: number; sourcePeriodId: number }>(
      (data) => `/periods/${data.periodId}/copy-from/${data.sourcePeriodId}`,
      'POST'
    ),
};

export async function fetchPeriods(params?: PeriodListParams): Promise<PeriodData[]> {
  const response = await apiClient.get('/periods', { params });
  return response.data.data?.items || response.data.data || [];
}

export async function fetchPeriod(id: number): Promise<PeriodData> {
  const response = await apiClient.get(`/periods/${id}`);
  return response.data.data || response.data;
}

export async function createPeriod(data: CreatePeriodData): Promise<PeriodData> {
  const response = await apiClient.post('/periods', data);
  return response.data.data || response.data;
}

export async function updatePeriod(id: number, data: UpdatePeriodData): Promise<PeriodData> {
  const response = await apiClient.patch(`/periods/${id}`, data);
  return response.data.data || response.data;
}

export async function deletePeriod(id: number): Promise<void> {
  await apiClient.delete(`/periods/${id}`);
}

export async function closePeriod(id: number): Promise<PeriodData> {
  const response = await apiClient.post(`/periods/${id}/close`);
  return response.data.data || response.data;
}

export async function reopenPeriod(id: number): Promise<PeriodData> {
  const response = await apiClient.post(`/periods/${id}/reopen`);
  return response.data.data || response.data;
}

export async function duplicatePeriod(id: number): Promise<any> {
  const response = await apiClient.post(`/periods/${id}/duplicate`);
  return response.data.data || response.data;
}

export async function copyFromPeriod(periodId: number, sourcePeriodId: number): Promise<any> {
  const response = await apiClient.post(`/periods/${periodId}/copy-from/${sourcePeriodId}`);
  return response.data.data || response.data;
}

export async function fetchWorkspace(periodId: number): Promise<any> {
  const response = await apiClient.get(`/periods/${periodId}/workspace`);
  return response.data.data || response.data;
}
