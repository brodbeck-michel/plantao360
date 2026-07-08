/**
 * API Client — Plantão 360
 *
 * Camada de abstração HTTP. Nenhum componente deve importar Axios diretamente.
 * Todos os acessos à API devem passar por este módulo.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';

// ============================================================
// Types
// ============================================================

export interface ApiClientConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export interface RequestContext {
  requestId: string;
  timestamp: number;
}

// ============================================================
// Request ID Generator
// ============================================================

let requestCounter = 0;

function generateRequestId(): string {
  requestCounter += 1;
  return `req_${Date.now()}_${requestCounter}`;
}

// ============================================================
// API Client Factory
// ============================================================

export function createApiClient(config: ApiClientConfig): AxiosInstance {
  const client = axios.create({
    baseURL: config.baseURL,
    timeout: config.timeout ?? 30000,
    headers: {
      'Content-Type': 'application/json',
      ...config.headers,
    },
  });

  // Request Interceptor
  client.interceptors.request.use(
    (requestConfig: InternalAxiosRequestConfig) => {
      const requestId = generateRequestId();
      const context: RequestContext = {
        requestId,
        timestamp: Date.now(),
      };

      // Attach request ID to headers
      requestConfig.headers['X-Request-ID'] = requestId;

      // Attach JWT token if present
      const token = localStorage.getItem('plantao360.token');
      if (token) {
        requestConfig.headers['Authorization'] = `Bearer ${token}`;
      }

      // Store context for response interceptor
      (requestConfig as any).__context = context;

      return requestConfig;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response Interceptor
  client.interceptors.response.use(
    (response) => {
      return response;
    },
    (error: AxiosError) => {
      // Auto-logout on 401
      if (error.response?.status === 401) {
        localStorage.removeItem('plantao360.token');
        window.location.href = '/login';
      }
      const mappedError = mapError(error);
      return Promise.reject(mappedError);
    }
  );

  return client;
}

// ============================================================
// Error Mapper
// ============================================================

export interface AppError {
  code: string;
  message: string;
  status?: number;
  details?: unknown;
  requestId?: string;
}

export function mapError(error: AxiosError): AppError {
  const status = error.response?.status;
  const data = error.response?.data as any;

  // Network error
  if (!error.response) {
    return {
      code: 'NETWORK_ERROR',
      message: 'Não foi possível conectar ao servidor. Verifique sua conexão.',
      status: undefined,
      details: error.message,
    };
  }

  // Server error with custom message
  if (data?.message) {
    return {
      code: data.code || 'SERVER_ERROR',
      message: data.message,
      status,
      details: data.details,
      requestId: error.config?.headers?.['X-Request-ID'] as string,
    };
  }

  // Default error mapping by status
  const statusMessages: Record<number, string> = {
    400: 'Dados inválidos. Verifique as informações e tente novamente.',
    401: 'Sessão expirada. Faça login novamente.',
    403: 'Você não tem permissão para esta ação.',
    404: 'Recurso não encontrado.',
    409: 'Conflito de dados. Verifique as informações.',
    422: 'Dados não processados. Verifique os campos.',
    429: 'Muitas requisições. Aguarde um momento e tente novamente.',
    500: 'Erro interno do servidor. Contate o suporte.',
    502: 'Serviço temporariamente indisponível.',
    503: 'Serviço indisponível. Tente novamente em alguns minutos.',
  };

  return {
    code: 'HTTP_ERROR',
    message: statusMessages[status || 500] || 'Ocorreu um erro inesperado.',
    status,
    details: data,
    requestId: error.config?.headers?.['X-Request-ID'] as string,
  };
}

// ============================================================
// Default Client Instance
// ============================================================

export const apiClient = createApiClient({
  baseURL: '/api/v1',
  timeout: 30000,
});
