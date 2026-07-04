/**
 * DoctorCreateDialog — Plantão 360
 *
 * Diálogo de criação de médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import { DoctorForm } from '../forms/doctor-form';
import { useCreateDoctor } from '../hooks/use-doctors';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';

// ============================================================
// Types
// ============================================================

interface DoctorCreateDialogProps {
  open: boolean;
  onClose: () => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorCreateDialog({ open, onClose }: DoctorCreateDialogProps) {
  const createDoctor = useCreateDoctor();
  const { showError, showSuccess } = useErrorExperience();

  const handleSubmit = async (data: { name: string; crm: string; specialty: string; email: string }) => {
    try {
      await createDoctor.mutateAsync(data);
      showSuccess('Médico criado com sucesso');
      onClose();
    } catch (error) {
      showError(error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth aria-labelledby="create-doctor-title">
      <DialogTitle id="create-doctor-title">Novo Médico</DialogTitle>
      <DialogContent>
        <DoctorForm
          onSubmit={handleSubmit}
          onCancel={onClose}
          loading={createDoctor.isPending}
          error={createDoctor.error?.message}
          mode="create"
        />
      </DialogContent>
    </Dialog>
  );
}
