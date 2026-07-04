/**
 * EmptyState Component — Plantão 360
 *
 * Estado vazio para quando não há dados.
 * Segue UX-008 (empty states devem explicar o que é e como preencher).
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Inbox } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
}

// ============================================================
// Component
// ============================================================

export function EmptyState({
  title = 'Nenhum registro encontrado',
  description = 'Não há dados para exibir. Crie um novo registro para começar.',
  actionLabel,
  onAction,
  icon,
}: EmptyStateProps) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      py={8}
      px={4}
    >
      {icon || <Inbox sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />}
      <Typography variant="h6" gutterBottom textAlign="center">
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary" textAlign="center" mb={3}>
        {description}
      </Typography>
      {actionLabel && onAction && (
        <Button variant="contained" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </Box>
  );
}
