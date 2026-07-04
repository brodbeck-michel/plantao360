/**
 * ProgressOverlay — Plantão 360
 *
 * Overlay translúcido com progresso para operações longas.
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { tokens } from '../../../theme';

interface ProgressOverlayProps {
  visible: boolean;
  message?: string;
}

export function ProgressOverlay({ visible, message }: ProgressOverlayProps) {
  if (!visible) return null;

  return (
    <Box
      sx={{
        position: 'fixed',
        inset: 0,
        bgcolor: 'rgba(255,255,255,0.7)',
        backdropFilter: 'blur(4px)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: tokens.zIndex.modal,
        animation: 'fadeIn 200ms ease-out',
      }}
      role="progressbar"
      aria-busy="true"
      aria-label={message || 'Carregando'}
    >
      <CircularProgress size={48} sx={{ color: tokens.colors.primary.main }} />
      {message && (
        <Typography variant="body2" sx={{ mt: 2, color: tokens.colors.text.secondary, fontWeight: 500 }}>
          {message}
        </Typography>
      )}
    </Box>
  );
}
