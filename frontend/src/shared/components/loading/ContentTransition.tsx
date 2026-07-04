/**
 * ContentTransition — Plantão 360
 *
 * Wrapper com fade transition para evitar flickering.
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box } from '@mui/material';

interface ContentTransitionProps {
  visible: boolean;
  children: React.ReactNode;
}

export function ContentTransition({ visible, children }: ContentTransitionProps) {
  return (
    <Box
      sx={{
        opacity: visible ? 1 : 0,
        transition: 'opacity 300ms cubic-bezier(0.4, 0, 0.2, 1)',
      }}
    >
      {children}
    </Box>
  );
}
