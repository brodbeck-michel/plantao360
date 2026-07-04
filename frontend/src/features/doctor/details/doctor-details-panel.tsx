/**
 * DoctorDetailsPanel — Plantão 360
 *
 * Painel de detalhes do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Paper, Grid, Typography, Box, Divider } from '@mui/material';
import { EntityAvatar } from '../../../shared/components/entity-avatar';
import { StatusChip } from '../../../shared/components/status-chip';
import type { Doctor, DoctorSummary } from '../types/doctor-types';

// ============================================================
// Types
// ============================================================

interface DoctorDetailsPanelProps {
  doctor: Doctor;
  summary?: DoctorSummary;
}

// ============================================================
// Component
// ============================================================

export function DoctorDetailsPanel({ doctor, summary }: DoctorDetailsPanelProps) {
  return (
    <Paper variant="outlined" sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <EntityAvatar name={doctor.name} size="large" />
        <Box>
          <Typography variant="h5" fontWeight={600}>
            {doctor.name}
          </Typography>
          <Box display="flex" alignItems="center" gap={1} mt={0.5}>
            <Typography variant="body2" color="text.secondary">
              CRM: {doctor.crm}
            </Typography>
            <StatusChip status={doctor.active ? 'active' : 'inactive'} />
          </Box>
        </Box>
      </Box>

      <Divider sx={{ my: 2 }} />

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <Typography variant="caption" color="text.secondary" gutterBottom>
            Especialidade
          </Typography>
          <Typography variant="body1" fontWeight={500}>
            {doctor.specialty}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="caption" color="text.secondary" gutterBottom>
            E-mail
          </Typography>
          <Typography variant="body1" fontWeight={500}>
            {doctor.email}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="caption" color="text.secondary" gutterBottom>
            Criado em
          </Typography>
          <Typography variant="body1" fontWeight={500}>
            {new Date(doctor.created_at).toLocaleDateString('pt-BR')}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="caption" color="text.secondary" gutterBottom>
            Atualizado em
          </Typography>
          <Typography variant="body1" fontWeight={500}>
            {new Date(doctor.updated_at).toLocaleDateString('pt-BR')}
          </Typography>
        </Grid>
      </Grid>

      {summary && (
        <>
          <Divider sx={{ my: 2 }} />
          <Typography variant="subtitle2" fontWeight={600} mb={1}>
            Resumo
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Typography variant="h6" color="primary" fontWeight={600}>
                {summary.total_shifts}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Plantões
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="h6" color="primary" fontWeight={600}>
                {summary.total_assignments}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Atribuições
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="h6" color="primary" fontWeight={600}>
                {summary.total_hours}h
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Horas
              </Typography>
            </Grid>
          </Grid>
        </>
      )}
    </Paper>
  );
}
