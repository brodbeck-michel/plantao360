/**
 * PageHeader Component — Plantão 360
 *
 * Cabeçalho padrão para todas as telas.
 * Segue UX-006 (consistência visual).
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { Box, Typography, Breadcrumbs, Link, Chip } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

// ============================================================
// Types
// ============================================================

interface BreadcrumbItem {
  label: string;
  path?: string;
}

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: BreadcrumbItem[];
  actions?: React.ReactNode;
  status?: string;
}

// ============================================================
// Component
// ============================================================

export function PageHeader({
  title,
  subtitle,
  breadcrumbs,
  actions,
  status,
}: PageHeaderProps) {
  return (
    <Box mb={3}>
      {breadcrumbs && breadcrumbs.length > 0 && (
        <Breadcrumbs sx={{ mb: 1 }}>
          {breadcrumbs.map((item, index) =>
            item.path ? (
              <Link
                key={index}
                component={RouterLink}
                to={item.path}
                color="inherit"
              >
                {item.label}
              </Link>
            ) : (
              <Typography key={index} color="text.primary">
                {item.label}
              </Typography>
            )
          )}
        </Breadcrumbs>
      )}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="h4" component="h1" fontWeight={600}>
              {title}
            </Typography>
            {status && <Chip label={status} size="small" />}
          </Box>
          {subtitle && (
            <Typography variant="body2" color="text.secondary" mt={0.5}>
              {subtitle}
            </Typography>
          )}
        </Box>
        {actions && <Box>{actions}</Box>}
      </Box>
    </Box>
  );
}
