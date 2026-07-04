/**
 * {{FEATURE_PASCAL}} Toolbar — Plantão 360
 *
 * Toolbar da página de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import { Add, FileDownload } from '@mui/icons-material';

interface {{FEATURE_PASCAL}}ToolbarProps {
  total: number;
  onCreate: () => void;
  onExport?: () => void;
  selectedCount?: number;
}

export function {{FEATURE_PASCAL}}Toolbar({ total, onCreate, onExport, selectedCount = 0 }: {{FEATURE_PASCAL}}ToolbarProps) {
  return (
    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
      <Box display="flex" alignItems="center" gap={2}>
        <Typography variant="body2" color="text.secondary">
          {total} {total === 1 ? 'registro' : 'registros'}
          {selectedCount > 0 && ` (${selectedCount} selecionados)`}
        </Typography>
      </Box>
      <Box display="flex" gap={1}>
        {onExport && (
          <Button startIcon={<FileDownload />} onClick={onExport} variant="outlined" size="small">
            Exportar
          </Button>
        )}
        <Button startIcon={<Add />} onClick={onCreate} variant="contained" size="small">
          Novo
        </Button>
      </Box>
    </Box>
  );
}
