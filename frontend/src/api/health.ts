import { apiClient } from './client';

export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
  database: string;
  timestamp: string;
}

export const healthApi = {
  check: () => apiClient.get<HealthResponse>('/health'),
};
