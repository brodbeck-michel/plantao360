/**
 * DomainExplanationPanel — Plantão 360
 *
 * Painel que exibe explicação de domínio.
 * Integra com DomainExplanation do backend.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import {
  Box, Typography, Paper, Stepper, Step, StepLabel, StepContent, Chip,
} from '@mui/material';
import { Info } from '@mui/icons-material';
import type { DomainExplanation } from '../../../types';

// ============================================================
// Types
// ============================================================

interface DomainExplanationPanelProps {
  explanation: DomainExplanation;
}

// ============================================================
// Component
// ============================================================

export function DomainExplanationPanel({ explanation }: DomainExplanationPanelProps) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Info color="info" fontSize="small" />
        <Typography variant="subtitle2" fontWeight={600}>
          Explicação do Domínio
        </Typography>
        {explanation.is_reproducible && (
          <Chip label="Reproduzível" size="small" color="success" variant="outlined" />
        )}
      </Box>
      <Stepper orientation="vertical">
        {explanation.steps.map((step) => (
          <Step key={step.order} active>
            <StepLabel
              StepIconComponent={() => (
                <Chip
                  label={step.order}
                  size="small"
                  color="primary"
                  sx={{ minWidth: 24, height: 24 }}
                />
              )}
            >
              <Typography variant="body2" fontWeight={500}>
                {step.description}
              </Typography>
            </StepLabel>
            <StepContent>
              <Typography variant="body2" color="text.secondary">
                Valor: <strong>{String(step.value)}</strong>
              </Typography>
              {step.formula && (
                <Typography variant="caption" color="text.secondary" display="block" mt={0.5}>
                  Fórmula: <code>{step.formula}</code>
                </Typography>
              )}
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Paper>
  );
}
