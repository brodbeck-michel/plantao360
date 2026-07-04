/**
 * DoctorProfileDrawer — Plantão 360
 *
 * Drawer lateral com perfil rápido do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import {
  Drawer, Box, Typography, IconButton, Divider, List, ListItem, ListItemText, ListItemIcon,
} from '@mui/material';
import { Close, Email, LocalHospital, Badge, CalendarToday } from '@mui/icons-material';
import { EntityAvatar } from '../../../shared/components/entity-avatar';
import { StatusChip } from '../../../shared/components/status-chip';
import { useDoctorSummary } from '../hooks/use-doctors';
import type { Doctor } from '../types/doctor-types';

// ============================================================
// Types
// ============================================================

interface DoctorProfileDrawerProps {
  open: boolean;
  doctor: Doctor;
  onClose: () => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorProfileDrawer({ open, doctor, onClose }: DoctorProfileDrawerProps) {
  const { data: summary } = useDoctorSummary(doctor.id);

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: { width: 360 },
      }}
    >
      <Box p={3}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box display="flex" alignItems="center" gap={2}>
            <EntityAvatar name={doctor.name} size="large" />
            <Box>
              <Typography variant="h6" fontWeight={600}>
                {doctor.name}
              </Typography>
              <StatusChip status={doctor.active ? 'active' : 'inactive'} />
            </Box>
          </Box>
          <IconButton onClick={onClose} aria-label="Fechar">
            <Close />
          </IconButton>
        </Box>

        <Divider sx={{ my: 2 }} />

        <List dense>
          <ListItem>
            <ListItemIcon><Badge fontSize="small" /></ListItemIcon>
            <ListItemText primary="CRM" secondary={doctor.crm} />
          </ListItem>
          <ListItem>
            <ListItemIcon><LocalHospital fontSize="small" /></ListItemIcon>
            <ListItemText primary="Especialidade" secondary={doctor.specialty} />
          </ListItem>
          <ListItem>
            <ListItemIcon><Email fontSize="small" /></ListItemIcon>
            <ListItemText primary="E-mail" secondary={doctor.email} />
          </ListItem>
          <ListItem>
            <ListItemIcon><CalendarToday fontSize="small" /></ListItemIcon>
            <ListItemText
              primary="Criado em"
              secondary={new Date(doctor.created_at).toLocaleDateString('pt-BR')}
            />
          </ListItem>
        </List>

        {summary && (
          <>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle2" fontWeight={600} mb={1}>
              Resumo
            </Typography>
            <Box display="flex" gap={2}>
              <Box textAlign="center">
                <Typography variant="h6" color="primary" fontWeight={600}>
                  {summary.total_shifts}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Plantões
                </Typography>
              </Box>
              <Box textAlign="center">
                <Typography variant="h6" color="primary" fontWeight={600}>
                  {summary.total_hours}h
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Horas
                </Typography>
              </Box>
            </Box>
          </>
        )}
      </Box>
    </Drawer>
  );
}
