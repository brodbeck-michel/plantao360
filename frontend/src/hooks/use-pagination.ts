/**
 * usePagination Hook — Plantão 360
 *
 * Hook para paginação de tabelas.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { useState, useCallback } from 'react';

// ============================================================
// Types
// ============================================================

export interface UsePaginationReturn {
  page: number;
  pageSize: number;
  setPage: (page: number) => void;
  setPageSize: (pageSize: number) => void;
  nextPage: () => void;
  prevPage: () => void;
  reset: () => void;
  offset: number;
}

// ============================================================
// Hook
// ============================================================

export function usePagination(defaultPage = 1, defaultPageSize = 20): UsePaginationReturn {
  const [page, setPage] = useState(defaultPage);
  const [pageSize, setPageSize] = useState(defaultPageSize);

  const nextPage = useCallback(() => {
    setPage((prev) => prev + 1);
  }, []);

  const prevPage = useCallback(() => {
    setPage((prev) => Math.max(1, prev - 1));
  }, []);

  const reset = useCallback(() => {
    setPage(defaultPage);
    setPageSize(defaultPageSize);
  }, [defaultPage, defaultPageSize]);

  const offset = (page - 1) * pageSize;

  return {
    page,
    pageSize,
    setPage,
    setPageSize,
    nextPage,
    prevPage,
    reset,
    offset,
  };
}
