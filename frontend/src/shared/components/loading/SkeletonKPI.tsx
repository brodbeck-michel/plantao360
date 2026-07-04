/**
 * SkeletonKPI — Plantão 360
 *
 * Skeleton para KPI com shimmer animation.
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Skeleton } from '@mui/material';

export function SkeletonKPI() {
  return (
    <Box sx={{ p: 2.5 }}>
      <Skeleton variant="text" width="50%" height={14} sx={{ mb: 1 }} />
      <Skeleton variant="text" width="35%" height={40} sx={{ mb: 1 }} />
      <Skeleton variant="text" width="60%" height={14} />
    </Box>
  );
}
