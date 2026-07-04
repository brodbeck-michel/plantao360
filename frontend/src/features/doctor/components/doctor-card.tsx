/**
 * Doctor Card Component — Plantão 360
 *
 * Card de resumo para médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { DoctorAvatar } from './doctor-avatar';
import type { Doctor } from '../types/doctor-types';
import { ROUTES } from '../../../routes/routes';

// ============================================================
// Types
// ============================================================

interface DoctorCardProps {
  doctor: Doctor;
}

// ============================================================
// Component
// ============================================================

export function DoctorCard({ doctor }: DoctorCardProps) {
  const navigate = useNavigate();

  return (
    <Card
      onClick={() => navigate(`${ROUTES.DOCTORS}/${doctor.id}`)}
      sx={{ cursor: 'pointer', '&:hover': { boxShadow: 2 } }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" gap={2}>
          <DoctorAvatar name={doctor.name} size="large" />
          <Box flex={1}>
            <Typography variant="h6" fontWeight={600}>
              {doctor.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              CRM: {doctor.crm}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {doctor.specialty}
            </Typography>
          </Box>
          <Chip
            label={doctor.active ? 'Ativo' : 'Inativo'}
            color={doctor.active ? 'success' : 'default'}
            size="small"
          />
        </Box>
      </CardContent>
    </Card>
  );
}
