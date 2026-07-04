/**
 * Query Factories — Plantão 360
 *
 * Fábricas de queries e mutations para React Query.
 * Cada feature pode criar suas próprias queries usando estas fábricas.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { UseQueryOptions, UseMutationOptions, QueryKey } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { apiClient, AppError, mapError } from '../api/client';

// ============================================================
// Types
// ============================================================

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

// ============================================================
// Query Factory
// ============================================================

export function createQuery<TData, TParams extends Record<string, unknown> = Record<string, unknown>>(
  queryKey: QueryKey,
  endpoint: string,
  options?: Omit<UseQueryOptions<TData, AppError>, 'queryKey' | 'queryFn'>
) {
  return {
    queryKey,
    queryFn: async (): Promise<TData> => {
      try {
        const response = await apiClient.get<TData>(endpoint);
        return response.data;
      } catch (error) {
        throw mapError(error as any);
      }
    },
    ...options,
  };
}

// ============================================================
// Paginated Query Factory
// ============================================================

export function createPaginatedQuery<TData>(
  queryKey: QueryKey,
  endpoint: string,
  params?: PaginationParams,
  options?: Omit<UseQueryOptions<PaginatedResponse<TData>, AppError>, 'queryKey' | 'queryFn'>
) {
  return {
    queryKey: [...queryKey, params],
    queryFn: async (): Promise<PaginatedResponse<TData>> => {
      try {
        const response = await apiClient.get<PaginatedResponse<TData>>(endpoint, { params });
        return response.data;
      } catch (error) {
        throw mapError(error as any);
      }
    },
    ...options,
  };
}

// ============================================================
// Mutation Factory
// ============================================================

export function createMutation<TData, TVariables>(
  endpoint: string,
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'POST',
  options?: Omit<UseMutationOptions<TData, AppError, TVariables>, 'mutationFn'>
) {
  return {
    mutationFn: async (variables: TVariables): Promise<TData> => {
      try {
        let response;
        switch (method) {
          case 'POST':
            response = await apiClient.post<TData>(endpoint, variables);
            break;
          case 'PUT':
            response = await apiClient.put<TData>(endpoint, variables);
            break;
          case 'PATCH':
            response = await apiClient.patch<TData>(endpoint, variables);
            break;
          case 'DELETE':
            response = await apiClient.delete<TData>(endpoint);
            break;
        }
        return response!.data;
      } catch (error) {
        throw mapError(error as any);
      }
    },
    ...options,
  };
}

// ============================================================
// Mutation with Dynamic Endpoint
// ============================================================

export function createDynamicMutation<TData, TVariables>(
  endpointFn: (variables: TVariables) => string,
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'POST',
  options?: Omit<UseMutationOptions<TData, AppError, TVariables>, 'mutationFn'>
) {
  return {
    mutationFn: async (variables: TVariables): Promise<TData> => {
      try {
        const endpoint = endpointFn(variables);
        let response;
        switch (method) {
          case 'POST':
            response = await apiClient.post<TData>(endpoint, variables);
            break;
          case 'PUT':
            response = await apiClient.put<TData>(endpoint, variables);
            break;
          case 'PATCH':
            response = await apiClient.patch<TData>(endpoint, variables);
            break;
          case 'DELETE':
            response = await apiClient.delete<TData>(endpoint);
            break;
        }
        return response!.data;
      } catch (error) {
        throw mapError(error as any);
      }
    },
    ...options,
  };
}
