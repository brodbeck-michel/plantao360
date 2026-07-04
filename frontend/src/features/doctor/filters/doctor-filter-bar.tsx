/**
 * DoctorFilterBar — Plantão 360
 *
 * Filtros reutilizáveis para médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { FilterBar, FilterField } from '../../../shared/components/filter-bar';
import type { DoctorFilters } from '../types/doctor-types';

// ============================================================
// Types
// ============================================================

interface DoctorFilterBarProps {
  filters: DoctorFilters;
  onFilterChange: (filters: Partial<DoctorFilters>) => void;
  onClear: () => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorFilterBar({ filters, onFilterChange, onClear }: DoctorFilterBarProps) {
  const activeCount = [
    filters.name,
    filters.crm,
    filters.specialty,
    filters.active !== undefined ? String(filters.active) : '',
  ].filter(Boolean).length;

  const fields: FilterField[] = [
    {
      id: 'name',
      label: 'Nome',
      type: 'text',
      placeholder: 'Nome do médico',
      value: filters.name || '',
      onChange: (value) => onFilterChange({ name: value as string }),
    },
    {
      id: 'crm',
      label: 'CRM',
      type: 'text',
      placeholder: 'Número do CRM',
      value: filters.crm || '',
      onChange: (value) => onFilterChange({ crm: value as string }),
    },
    {
      id: 'specialty',
      label: 'Especialidade',
      type: 'text',
      placeholder: 'Especialidade',
      value: filters.specialty || '',
      onChange: (value) => onFilterChange({ specialty: value as string }),
    },
    {
      id: 'active',
      label: 'Status',
      type: 'select',
      options: [
        { value: '', label: 'Todos' },
        { value: 'true', label: 'Ativo' },
        { value: 'false', label: 'Inativo' },
      ],
      value: filters.active !== undefined ? String(filters.active) : '',
      onChange: (value) => onFilterChange({
        active: value === '' ? undefined : value === 'true',
      }),
    },
  ];

  return (
    <FilterBar
      fields={fields}
      searchPlaceholder="Pesquisar médicos..."
      searchValue={filters.name || ''}
      onSearchChange={(value) => onFilterChange({ name: value })}
      onClear={onClear}
      activeCount={activeCount}
    />
  );
}
