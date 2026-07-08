import { apiClient } from './client';

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  active: boolean;
  last_login: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface CreateUserRequest {
  name: string;
  email: string;
  password: string;
  role: string;
}

export interface UpdateUserRequest {
  name?: string;
  email?: string;
  role?: string;
  active?: boolean;
}

export interface ChangePasswordRequest {
  password: string;
}

export const usersApi = {
  list: async (): Promise<User[]> => {
    const response = await apiClient.get('/users');
    return response.data;
  },

  get: async (id: number): Promise<User> => {
    const response = await apiClient.get(`/users/${id}`);
    return response.data;
  },

  create: async (data: CreateUserRequest): Promise<User> => {
    const response = await apiClient.post('/users', data);
    return response.data;
  },

  update: async (id: number, data: UpdateUserRequest): Promise<User> => {
    const response = await apiClient.put(`/users/${id}`, data);
    return response.data;
  },

  activate: async (id: number): Promise<User> => {
    const response = await apiClient.post(`/users/${id}/activate`);
    return response.data;
  },

  deactivate: async (id: number): Promise<User> => {
    const response = await apiClient.post(`/users/${id}/deactivate`);
    return response.data;
  },

  changePassword: async (id: number, password: string): Promise<void> => {
    await apiClient.post(`/users/${id}/password`, { password });
  },
};
