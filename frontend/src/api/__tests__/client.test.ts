/**
 * API Client Test — Plantão 360
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createApiClient, mapErrorToMessage } from 'src/api/client';

// Mock axios
vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() },
      },
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    })),
  },
}));

describe('API Client', () => {
  it('creates client with default config', () => {
    const client = createApiClient();
    expect(client).toBeDefined();
  });

  it('creates client with custom base URL', () => {
    const client = createApiClient({ baseURL: 'https://custom.api.com' });
    expect(client).toBeDefined();
  });
});

describe('Error Mapper', () => {
  it('maps network error', () => {
    const error = {
      code: 'ERR_NETWORK',
      message: 'Network Error',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Erro de conexão. Verifique sua internet.');
  });

  it('maps timeout error', () => {
    const error = {
      code: 'ECONNABORTED',
      message: 'timeout',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Tempo limite excedido. Tente novamente.');
  });

  it('maps 401 error', () => {
    const error = {
      response: { status: 401 },
      message: 'Unauthorized',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Sessão expirada. Faça login novamente.');
  });

  it('maps 403 error', () => {
    const error = {
      response: { status: 403 },
      message: 'Forbidden',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Acesso negado. Você não tem permissão.');
  });

  it('maps 404 error', () => {
    const error = {
      response: { status: 404 },
      message: 'Not Found',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Recurso não encontrado.');
  });

  it('maps 500 error', () => {
    const error = {
      response: { status: 500 },
      message: 'Internal Server Error',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Erro interno do servidor.');
  });

  it('maps unknown error', () => {
    const error = {
      message: 'Unknown error',
    };
    const result = mapErrorToMessage(error);
    expect(result).toBe('Erro inesperado. Tente novamente.');
  });
});
