/**
 * SkeletonCard — Plantão 360
 *
 * Skeleton com shape de card operacional.
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Card, CardContent, Skeleton, Stack } from '@mui/material';
import { tokens } from '../../../theme';

interface SkeletonCardProps {
  height?: number;
}

export function SkeletonCard({ height = 120 }: SkeletonCardProps) {
  return (
    <Card sx={{ height }}>
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <Skeleton variant="text" width="40%" height={14} sx={{ mb: 1 }} />
        <Skeleton variant="text" width="60%" height={32} sx={{ mb: 1 }} />
        <Skeleton variant="text" width="30%" height={14} />
      </CardContent>
    </Card>
  );
}
