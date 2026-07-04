/**
 * LoadingSpinner — Plantão 360
 *
 * Indicador de loading padronizado.
 * Suporta delay para evitar flickering em carregamentos rápidos.
 *
 * Sprint: 13 — Golden Frontend Module
 * Sprint: 15 — Anti-flickering delay
 */

import React, { useState, useEffect } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

// ============================================================
// Types
// ============================================================

interface LoadingSpinnerProps {
  message?: string;
  fullScreen?: boolean;
  size?: number;
  /** Delay in ms before showing spinner (default: 300ms — anti-flickering) */
  delay?: number;
}

// ============================================================
// Component
// ============================================================

export function LoadingSpinner({ message, fullScreen = false, size = 40, delay = 300 }: LoadingSpinnerProps) {
  const [visible, setVisible] = useState(delay === 0);

  useEffect(() => {
    if (delay === 0) return;
    const timer = setTimeout(() => setVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);

  if (!visible) return null;

  const content = (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      gap={2}
      py={fullScreen ? 0 : 4}
      height={fullScreen ? '100vh' : 'auto'}
      sx={{ animation: 'fadeIn 200ms ease-out' }}
    >
      <CircularProgress size={size} />
      {message && (
        <Typography variant="body2" color="text.secondary">
          {message}
        </Typography>
      )}
    </Box>
  );

  if (fullScreen) {
    return (
      <Box position="fixed" inset={0} bgcolor="background.default" zIndex={9999}>
        {content}
      </Box>
    );
  }

  return content;
}
