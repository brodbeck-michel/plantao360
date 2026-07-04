import { apiClient } from '../../../api/client';
import { queryKeys } from '../../../services/query-keys';
import { createQuery, createMutation, createPaginatedQuery } from '../../../services/query-factory';
import type { ShiftData, ShiftListParams, CreateShiftData, UpdateShiftData } from '../types/shift-types';

export const shiftQueries = {
  list: (params?: ShiftListParams) =>
    createPaginatedQuery<ShiftData>(
      queryKeys.shifts.list(params || {}),
      '/shifts',
      params
    ),
  detail: (id: string) =>
    createQuery<ShiftData>(
      queryKeys.shifts.detail(id),
      `/shifts/${id}`
    ),
};

export const shiftMutations = {
  create: () => createMutation<ShiftData, CreateShiftData>('/shifts', 'POST'),
  update: () => createMutation<ShiftData, UpdateShiftData>('/shifts', 'PUT'),
  delete: () => createMutation<any, number>('/shifts', 'DELETE'),
};

export async function fetchShifts(params?: ShiftListParams): Promise<ShiftData[]> {
  const response = await apiClient.get('/shifts', { params });
  return response.data.data?.items || response.data.data || [];
}

export async function createShift(data: CreateShiftData): Promise<ShiftData> {
  const response = await apiClient.post('/shifts', data);
  return response.data.data || response.data;
}

export async function updateShift(id: number, data: UpdateShiftData): Promise<ShiftData> {
  const response = await apiClient.put(`/shifts/${id}`, data);
  return response.data.data || response.data;
}

export async function deleteShift(id: number): Promise<void> {
  await apiClient.delete(`/shifts/${id}`);
}
