/**
 * API Services Index — Plantão 360
 *
 * Barrel para serviços de API e React Query factories.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

export { queryKeys } from './query-keys';
export {
  createQuery,
  createPaginatedQuery,
  createMutation,
  createDynamicMutation,
} from './query-factory';
export type { PaginatedResponse, PaginationParams } from './query-factory';
