/**
 * AutoRefreshIndicator — Plantão 360
 *
 * Indicador discreto de auto-refresh no header.
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React, { useState, useEffect } from 'react';
import { Stack, Typography } from '@mui/material';
import SyncIcon from '@mui/icons-material/Sync';
import { tokens } from '../../../theme';

interface AutoRefreshIndicatorProps {
  lastRefresh: Date | null;
  intervalMs?: number;
  isRefreshing?: boolean;
}

export function AutoRefreshIndicator({
  lastRefresh,
  intervalMs = 30000,
  isRefreshing = false,
}: AutoRefreshIndicatorProps) {
  const [elapsed, setElapsed] = useState('');

  useEffect(() => {
    if (!lastRefresh) return;

    const update = () => {
      const diff = Math.floor((Date.now() - lastRefresh.getTime()) / 1000);
      if (diff < 60) setElapsed(`${diff}s`);
      else if (diff < 3600) setElapsed(`${Math.floor(diff / 60)}m`);
      else setElapsed(`${Math.floor(diff / 3600)}h`);
    };

    update();
    const timer = setInterval(update, 5000);
    return () => clearInterval(timer);
  }, [lastRefresh]);

  if (!lastRefresh) return null;

  return (
    <Stack
      direction="row"
      alignItems="center"
      spacing={0.5}
      role="status"
      aria-label={`Última atualização: ${elapsed}`}
    >
      <SyncIcon
        sx={{
          fontSize: 14,
          color: tokens.colors.text.muted,
          animation: isRefreshing ? 'spin 1s linear infinite' : 'none',
        }}
      />
      <Typography variant="caption" sx={{ color: tokens.colors.text.muted }}>
        {isRefreshing ? 'Atualizando...' : `Atualizado há ${elapsed}`}
      </Typography>
    </Stack>
  );
}
