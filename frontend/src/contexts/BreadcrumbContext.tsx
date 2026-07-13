/**
 * BreadcrumbContext — Plantão 360
 *
 * Permite que páginas de detalhe (competência, médico, etc.) registrem
 * o nome real da entidade exibida, para que o breadcrumb do MainLayout
 * mostre "Julho 2026" / "Dra. Ana" em vez de "Detalhes #<id>".
 */

import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';

interface BreadcrumbContextValue {
  labels: Record<string, string>;
  setLabel: (path: string, label: string) => void;
  clearLabel: (path: string) => void;
}

const BreadcrumbContext = createContext<BreadcrumbContextValue | undefined>(undefined);

export function BreadcrumbProvider({ children }: { children: React.ReactNode }) {
  const [labels, setLabels] = useState<Record<string, string>>({});

  const setLabel = useCallback((path: string, label: string) => {
    setLabels((prev) => (prev[path] === label ? prev : { ...prev, [path]: label }));
  }, []);

  const clearLabel = useCallback((path: string) => {
    setLabels((prev) => {
      if (!(path in prev)) return prev;
      const next = { ...prev };
      delete next[path];
      return next;
    });
  }, []);

  const value = useMemo(() => ({ labels, setLabel, clearLabel }), [labels, setLabel, clearLabel]);

  return <BreadcrumbContext.Provider value={value}>{children}</BreadcrumbContext.Provider>;
}

function useBreadcrumbContext() {
  const ctx = useContext(BreadcrumbContext);
  if (!ctx) throw new Error('useBreadcrumbContext deve ser usado dentro de BreadcrumbProvider');
  return ctx;
}

/** Consumido pelo MainLayout para resolver o label da rota atual. */
export function useBreadcrumbLabels() {
  return useBreadcrumbContext().labels;
}

/** Chamado pelas páginas de detalhe para registrar o nome real da entidade. */
export function useBreadcrumbLabel(label: string | undefined | null) {
  const { setLabel, clearLabel } = useBreadcrumbContext();
  const { pathname } = useLocation();
  const pathRef = useRef(pathname);
  pathRef.current = pathname;

  useEffect(() => {
    if (label) setLabel(pathRef.current, label);
    return () => clearLabel(pathRef.current);
  }, [label, setLabel, clearLabel]);
}
