/**
 * FilterBar — Plantão 360
 *
 * Barra de filtros genérica reutilizável.
 * Sprint: 13 — Golden Frontend Module
 */

import React, { useState } from 'react';
import {
  Box, TextField, MenuItem, Button, IconButton, Chip, Collapse, InputAdornment,
} from '@mui/material';
import { FilterList, Clear, Search, ExpandMore, ExpandLess } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

export interface FilterField {
  id: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'boolean';
  options?: { value: string; label: string }[];
  placeholder?: string;
  value: string | boolean;
  onChange: (value: string | boolean) => void;
}

interface FilterBarProps {
  fields: FilterField[];
  searchPlaceholder?: string;
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  onClear?: () => void;
  activeCount?: number;
}

// ============================================================
// Component
// ============================================================

export function FilterBar({
  fields,
  searchPlaceholder = 'Pesquisar...',
  searchValue = '',
  onSearchChange,
  onClear,
  activeCount = 0,
}: FilterBarProps) {
  const [expanded, setExpanded] = useState(true);

  return (
    <Box mb={2}>
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        {onSearchChange && (
          <TextField
            size="small"
            placeholder={searchPlaceholder}
            value={searchValue}
            onChange={(e) => onSearchChange(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search fontSize="small" />
                </InputAdornment>
              ),
            }}
            sx={{ minWidth: 250 }}
            inputProps={{ 'aria-label': searchPlaceholder }}
          />
        )}
        <Button
          startIcon={<FilterList />}
          endIcon={expanded ? <ExpandLess /> : <ExpandMore />}
          onClick={() => setExpanded(!expanded)}
          aria-expanded={expanded}
          aria-controls="filter-panel"
        >
          Filtros
          {activeCount > 0 && (
            <Chip
              label={activeCount}
              size="small"
              color="primary"
              sx={{ ml: 1, height: 20, fontSize: '0.75rem' }}
            />
          )}
        </Button>
        {activeCount > 0 && onClear && (
          <Button
            startIcon={<Clear />}
            onClick={onClear}
            color="inherit"
            size="small"
          >
            Limpar
          </Button>
        )}
      </Box>
      <Collapse in={expanded}>
        <Box
          id="filter-panel"
          display="flex"
          flexWrap="wrap"
          gap={2}
          p={2}
          bgcolor="grey.50"
          borderRadius={1}
          role="region"
          aria-label="Filtros"
        >
          {fields.map((field) => (
            <TextField
              key={field.id}
              size="small"
              label={field.label}
              select={field.type === 'select'}
              type={field.type === 'date' ? 'date' : undefined}
              placeholder={field.placeholder}
              value={field.value}
              onChange={(e) => field.onChange(e.target.value)}
              InputLabelProps={field.type === 'date' ? { shrink: true } : undefined}
              sx={{ minWidth: 180 }}
              inputProps={{ 'aria-label': field.label }}
            >
              {field.type === 'select' && field.options?.map((opt) => (
                <MenuItem key={opt.value} value={opt.value}>
                  {opt.label}
                </MenuItem>
              ))}
            </TextField>
          ))}
        </Box>
      </Collapse>
    </Box>
  );
}
