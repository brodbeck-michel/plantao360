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

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/login', data);
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  changeMyPassword: async (password: string): Promise<void> => {
    await apiClient.put('/auth/me/password', { password });
  },
};
