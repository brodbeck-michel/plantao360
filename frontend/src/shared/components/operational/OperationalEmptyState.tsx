/**
 * OperationalEmptyState — Plantão 360
 *
 * Empty state contextual com ilustração SVG, explicação operacional,
 * ação recomendada e pré-requisitos.
 *
 * Sprint: 15 — UX Foundation & Operational Experience
 */

import React from 'react';
import { Box, Typography, Stack, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  EventNote,
  LocalHospital,
  CheckCircle,
  RocketLaunch,
} from '@mui/icons-material';
import { tokens } from '../../../theme';

// ============================================================
// Types
// ============================================================

type EmptyContext = 'shifts' | 'doctors' | 'alerts' | 'dashboard' | 'periods' | 'assignments' | 'extras';

interface EmptyConfig {
  title: string;
  description: string;
  actionLabel?: string;
  actionRoute?: string;
  prereq?: string;
  icon: React.ReactNode;
}

// ============================================================
// Configs
// ============================================================

const EMPTY_CONFIGS: Record<EmptyContext, EmptyConfig> = {
  shifts: {
    title: 'Nenhum plantão nesta competência',
    description: 'Crie plantões para começar a distribuição da escala do Pronto Socorro.',
    actionLabel: 'Criar Plantão',
    actionRoute: '/app/shifts/new',
    prereq: 'Certifique-se de que existe uma competência aberta.',
    icon: <EventNote sx={{ fontSize: 48, color: tokens.colors.primary.main }} />,
  },
  doctors: {
    title: 'Nenhum médico cadastrado',
    description: 'Cadastre médicos para montar as escalas de plantão.',
    actionLabel: 'Cadastrar Médico',
    actionRoute: '/app/doctors/new',
    icon: <LocalHospital sx={{ fontSize: 48, color: tokens.colors.primary.main }} />,
  },
  alerts: {
    title: 'Tudo sob controle',
    description: 'Não há alertas operacionais. A operação está saudável.',
    icon: <CheckCircle sx={{ fontSize: 48, color: tokens.colors.operational.healthy }} />,
  },
  dashboard: {
    title: 'Seu centro de operações está pronto',
    description: 'Configure a primeira competência para ativar o dashboard.',
    actionLabel: 'Criar Competência',
    actionRoute: '/app/periods/new',
    icon: <RocketLaunch sx={{ fontSize: 48, color: tokens.colors.primary.main }} />,
  },
  periods: {
    title: 'Nenhuma competência encontrada',
    description: 'Crie uma competência para começar a organizar os plantões.',
    actionLabel: 'Criar Competência',
    actionRoute: '/app/periods/new',
    icon: <EventNote sx={{ fontSize: 48, color: tokens.colors.primary.main }} />,
  },
  assignments: {
    title: 'Nenhuma atribuição realizada',
    description: 'Atribua médicos aos plantões para iniciar a escala.',
    actionLabel: 'Criar Atribuição',
    actionRoute: '/app/assignments/new',
    prereq: 'É necessário ter plantões criados.',
    icon: <EventNote sx={{ fontSize: 48, color: tokens.colors.primary.main }} />,
  },
  extras: {
    title: 'Nenhum horário extra registrado',
    description: 'Registre horas extras quando necessário.',
    icon: <EventNote sx={{ fontSize: 48, color: tokens.colors.primary.main }} />,
  },
};

// ============================================================
// Props
// ============================================================

interface OperationalEmptyStateProps {
  context: EmptyContext;
  customTitle?: string;
  customDescription?: string;
}

// ============================================================
// Component
// ============================================================

export function OperationalEmptyState({
  context,
  customTitle,
  customDescription,
}: OperationalEmptyStateProps) {
  const navigate = useNavigate();
  const config = EMPTY_CONFIGS[context];

  return (
    <Stack
      alignItems="center"
      justifyContent="center"
      sx={{ py: 6, px: 3, textAlign: 'center' }}
    >
      {/* Icon */}
      <Box
        sx={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          bgcolor: tokens.colors.primary.main + '10',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 2,
        }}
      >
        {config.icon}
      </Box>

      {/* Title */}
      <Typography variant="h6" sx={{ fontWeight: 600, color: tokens.colors.text.primary, mb: 0.5 }}>
        {customTitle || config.title}
      </Typography>

      {/* Description */}
      <Typography variant="body2" sx={{ color: tokens.colors.text.secondary, maxWidth: 400, mb: 2 }}>
        {customDescription || config.description}
      </Typography>

      {/* Prerequisite */}
      {config.prereq && (
        <Typography variant="caption" sx={{ color: tokens.colors.text.muted, fontStyle: 'italic', mb: 2 }}>
          {config.prereq}
        </Typography>
      )}

      {/* Action */}
      {config.actionLabel && config.actionRoute && (
        <Button
          variant="contained"
          onClick={() => navigate(config.actionRoute!)}
          sx={{
            bgcolor: tokens.colors.primary.main,
            color: tokens.colors.primary.contrastText,
            fontWeight: 600,
            px: 3,
            '&:hover': {
              bgcolor: tokens.colors.primary.dark,
            },
          }}
        >
          {config.actionLabel}
        </Button>
      )}
    </Stack>
  );
}
