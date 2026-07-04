/**
 * PageSkeleton — Plantão 360
 *
 * Generic loading skeleton for pages.
 * Provides consistent loading UX across all modules.
 *
 * Sprint: 14 — Operational MVP
 */

import { Box, Skeleton, Stack, Card, CardContent, Grid } from '@mui/material';

interface PageSkeletonProps {
  title?: boolean;
  toolbar?: boolean;
  cards?: number;
  table?: boolean;
  height?: number;
}

export function PageSkeleton({
  title = true,
  toolbar = true,
  cards = 0,
  table = true,
  height = 400,
}: PageSkeletonProps) {
  return (
    <Box>
      {/* Title + Toolbar */}
      {title && (
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
          <Skeleton variant="text" width={200} height={40} />
          {toolbar && <Skeleton variant="rectangular" width={120} height={36} sx={{ borderRadius: 1 }} />}
        </Stack>
      )}

      {/* Summary Cards */}
      {cards > 0 && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {Array.from({ length: cards }).map((_, i) => (
            <Grid size={{ xs: 12, sm: 6, md: 3 }} key={i}>
              <Card>
                <CardContent>
                  <Skeleton variant="text" width="60%" height={20} />
                  <Skeleton variant="text" width="40%" height={32} sx={{ mt: 1 }} />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Table Skeleton */}
      {table && (
        <Box sx={{ width: '100%' }}>
          <Skeleton variant="rectangular" height={56} sx={{ borderRadius: '4px 4px 0 0' }} />
          {Array.from({ length: 8 }).map((_, i) => (
            <Skeleton key={i} variant="rectangular" height={52} sx={{ borderBottom: '1px solid', borderColor: 'divider' }} />
          ))}
        </Box>
      )}

      {/* Generic Content */}
      {!table && height > 0 && (
        <Skeleton variant="rectangular" height={height} sx={{ borderRadius: 1 }} />
      )}
    </Box>
  );
}
