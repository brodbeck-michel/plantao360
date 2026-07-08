/**
 * API Services — Plantão 360
 *
 * Módulo barrel para todos os serviços de API.
 * Cada feature possui seu próprio serviço que consome o API Client.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

export { apiClient, createApiClient, mapError } from './client';
export type { ApiClientConfig, AppError, RequestContext } from './client';
export { usersApi } from './users';
