import { apiClient } from '../../../api/client';
import { queryKeys } from '../../../services/query-keys';
import { createQuery, createMutation, createPaginatedQuery } from '../../../services/query-factory';
import type { UseQueryOptions } from '@tanstack/react-query';
import type { AppError } from '../../../api/client';
import type { Doctor, DoctorSummary, AuditEntry } from '../../../types';

export interface DoctorListParams {
  page?: number;
  page_size?: number;
  name?: string;
  crm?: string;
  active?: boolean;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface CreateDoctorData {
  name: string;
  crm: string;
  specialty: string;
  email: string;
  phone?: string;
  doctor_type?: string;
  hour_rate: number;
}

export interface UpdateDoctorData {
  id: string;
  name?: string;
  crm?: string;
  specialty?: string;
  email?: string;
  phone?: string;
  doctor_type?: string;
  hour_rate?: number;
  active?: boolean;
}

export const doctorQueries = {
  list: (params?: DoctorListParams) =>
    createPaginatedQuery<Doctor>(
      queryKeys.doctors.list(params || {}),
      '/doctors',
      params
    ),
  detail: (id: string, options?: Omit<UseQueryOptions<Doctor, AppError>, 'queryKey' | 'queryFn'>) =>
    createQuery<Doctor>(
      queryKeys.doctors.detail(id),
      `/doctors/${id}`,
      options
    ),
};

export const doctorMutations = {
  create: () => createMutation<Doctor, CreateDoctorData>('/doctors', 'POST'),
  update: () => createMutation<Doctor, Omit<UpdateDoctorData, 'id'>>('/doctors', 'PUT'),
  delete: () => createMutation<void, string>('/doctors', 'DELETE'),
};

export async function fetchDoctors(params?: DoctorListParams): Promise<Doctor[]> {
  const response = await apiClient.get('/doctors', { params });
  return response.data.data || response.data;
}

export async function fetchDoctor(id: string): Promise<Doctor> {
  const response = await apiClient.get(`/doctors/${id}`);
  return response.data;
}

export async function createDoctor(data: CreateDoctorData): Promise<Doctor> {
  const response = await apiClient.post('/doctors', data);
  return response.data;
}

export async function updateDoctor(id: string, data: Omit<UpdateDoctorData, 'id'>): Promise<Doctor> {
  const response = await apiClient.put(`/doctors/${id}`, data);
  return response.data;
}

export async function deleteDoctor(id: string): Promise<void> {
  await apiClient.delete(`/doctors/${id}`);
}
