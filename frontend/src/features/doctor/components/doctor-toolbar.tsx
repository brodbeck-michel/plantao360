/**
 * DoctorToolbar — Plantão 360
 *
 * Toolbar da página de médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import { Add, FileDownload } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

interface DoctorToolbarProps {
  total: number;
  onCreate: () => void;
  onExport?: () => void;
  selectedCount?: number;
}

// ============================================================
// Component
// ============================================================

export function DoctorToolbar({ total, onCreate, onExport, selectedCount = 0 }: DoctorToolbarProps) {
  return (
    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
      <Box display="flex" alignItems="center" gap={2}>
        <Typography variant="body2" color="text.secondary">
          {total} {total === 1 ? 'médico' : 'médicos'}
          {selectedCount > 0 && ` (${selectedCount} selecionados)`}
        </Typography>
      </Box>
      <Box display="flex" gap={1}>
        {onExport && (
          <Button
            startIcon={<FileDownload />}
            onClick={onExport}
            variant="outlined"
            size="small"
            aria-label="Exportar"
          >
            Exportar
          </Button>
        )}
        <Button
          startIcon={<Add />}
          onClick={onCreate}
          variant="contained"
          size="small"
          aria-label="Novo médico"
        >
          Novo Médico
        </Button>
      </Box>
    </Box>
  );
}
