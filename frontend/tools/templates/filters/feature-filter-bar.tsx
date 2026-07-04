/**
 * {{FEATURE_PASCAL}} Filter Bar — Plantão 360
 *
 * Filtros de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { FilterBar, FilterField } from '../../../shared/components/filter-bar';
import type { {{FEATURE_PASCAL}}Filters } from '../types/{{FEATURE_NAME}}-types';

interface {{FEATURE_PASCAL}}FilterBarProps {
  filters: {{FEATURE_PASCAL}}Filters;
  onFilterChange: (filters: Partial<{{FEATURE_PASCAL}}Filters>) => void;
  onClear: () => void;
}

export function {{FEATURE_PASCAL}}FilterBar({ filters, onFilterChange, onClear }: {{FEATURE_PASCAL}}FilterBarProps) {
  const activeCount = [filters.name, filters.active !== undefined ? String(filters.active) : ''].filter(Boolean).length;

  const fields: FilterField[] = [
    { id: 'name', label: 'Nome', type: 'text', placeholder: 'Nome', value: filters.name || '', onChange: (v) => onFilterChange({ name: v as string }) },
    { id: 'active', label: 'Status', type: 'select', options: [{ value: '', label: 'Todos' }, { value: 'true', label: 'Ativo' }, { value: 'false', label: 'Inativo' }],
      value: filters.active !== undefined ? String(filters.active) : '', onChange: (v) => onFilterChange({ active: v === '' ? undefined : v === 'true' }) },
  ];

  return <FilterBar fields={fields} searchPlaceholder="Pesquisar..." searchValue={filters.name || ''} onSearchChange={(v) => onFilterChange({ name: v })} onClear={onClear} activeCount={activeCount} />;
}
