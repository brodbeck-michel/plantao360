/**
 * SkeletonTable — Plantão 360
 *
 * Skeleton de tabela com rows animados.
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Skeleton, Stack } from '@mui/material';

interface SkeletonTableProps {
  rows?: number;
  columns?: number;
}

export function SkeletonTable({ rows = 5, columns = 4 }: SkeletonTableProps) {
  return (
    <Box>
      {/* Header */}
      <Stack direction="row" spacing={2} sx={{ mb: 1, px: 1 }}>
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={`h-${i}`} variant="text" height={16} sx={{ flex: i === 0 ? '0 0 120px' : 1 }} />
        ))}
      </Stack>
      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIdx) => (
        <Stack key={`r-${rowIdx}`} direction="row" spacing={2} sx={{ py: 1, px: 1, borderTop: '1px solid #E5E7EB' }}>
          {Array.from({ length: columns }).map((_, colIdx) => (
            <Skeleton key={`c-${rowIdx}-${colIdx}`} variant="text" height={20} sx={{ flex: colIdx === 0 ? '0 0 120px' : 1 }} />
          ))}
        </Stack>
      ))}
    </Box>
  );
}
