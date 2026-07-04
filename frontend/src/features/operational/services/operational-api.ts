import { apiClient } from '../../../api/client';
import { queryKeys } from '../../../services/query-keys';
import { createQuery, createMutation } from '../../../services/query-factory';
import type { WorkspaceData } from '../types/operational-types';

export const workspaceQueries = {
  detail: (periodId: string) =>
    createQuery<WorkspaceData>(
      queryKeys.periods.detail(periodId),
      `/periods/${periodId}/workspace`,
      { staleTime: 0 }
    ),
};

export const assignmentMutations = {
  create: () =>
    createMutation<any, { shift_id: number; doctor_id: number; start_time: string; end_time: string }>(
      '/assignments', 'POST'
    ),
  update: () =>
    createMutation<any, { id: number; doctor_id?: number; start_time?: string; end_time?: string }>(
      '/assignments', 'PUT'
    ),
  delete: () =>
    createMutation<any, number>(
      '/assignments', 'DELETE'
    ),
};

export async function fetchWorkspace(periodId: string): Promise<WorkspaceData> {
  const response = await apiClient.get(`/periods/${periodId}/workspace`);
  return response.data.data;
}

export async function createAssignment(data: { shift_id: number; doctor_id: number; start_time: string; end_time: string }) {
  const response = await apiClient.post('/assignments', data);
  return response.data;
}

export async function updateAssignment(id: number, data: { doctor_id?: number; start_time?: string; end_time?: string }) {
  const response = await apiClient.put(`/assignments/${id}`, data);
  return response.data;
}

export async function deleteAssignment(id: number) {
  const response = await apiClient.delete(`/assignments/${id}`);
  return response.data;
}

export async function moveAssignment(id: number, data: { target_shift_id: number; start_time?: string; end_time?: string }) {
  const response = await apiClient.put(`/assignments/${id}/move`, data);
  return response.data;
}

export async function duplicateDay(data: { source_date: string; target_date: string; period_id: number }) {
  const response = await apiClient.post('/assignments/duplicate-day', data);
  return response.data;
}

export async function duplicateWeek(data: { source_start_date: string; target_start_date: string; period_id: number }) {
  const response = await apiClient.post('/assignments/duplicate-week', data);
  return response.data;
}
