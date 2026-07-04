/**
 * ComingSoonPage — Plantão 360
 *
 * Standardized placeholder for features not yet implemented.
 * Preserves navigation without creating incomplete screens.
 *
 * Sprint: 14 — Operational MVP
 */

import React from 'react';
import { Box, Container, Typography, Paper, Chip } from '@mui/material';
import { Construction } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

interface ComingSoonPageProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  estimatedSprint?: string;
}

// ============================================================
// Component
// ============================================================

/**
 * ComingSoonPage — displays a standardized "coming soon" message.
 *
 * Used for routes that are defined but not yet implemented.
 * Keeps navigation functional while indicating future features.
 *
 * @example
 * <ComingSoonPage title="Financeiro" estimatedSprint="Sprint 16" />
 */
export function ComingSoonPage({
  title,
  description,
  icon,
  estimatedSprint,
}: ComingSoonPageProps) {
  return (
    <Container maxWidth="md">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="60vh"
        textAlign="center"
      >
        <Paper
          elevation={0}
          sx={{
            p: 6,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 3,
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 2,
          }}
        >
          {icon || (
            <Construction
              sx={{ fontSize: 64, color: 'text.disabled' }}
            />
          )}

          <Typography variant="h4" fontWeight={600} color="text.primary">
            {title}
          </Typography>

          <Typography variant="body1" color="text.secondary" maxWidth={400}>
            {description || 'Esta funcionalidade está em desenvolvimento e estará disponível em breve.'}
          </Typography>

          {estimatedSprint && (
            <Chip
              label={`Previsto: ${estimatedSprint}`}
              color="primary"
              variant="outlined"
              size="small"
            />
          )}

          <Typography variant="caption" color="text.disabled" mt={2}>
            Plantão 360 — Sistema de Gestão de Plantões Médicos
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}
