/**
 * DoctorEditDialog — Plantão 360
 *
 * Diálogo de edição de médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Dialog, DialogTitle, DialogContent } from '@mui/material';
import { DoctorForm } from '../forms/doctor-form';
import { useUpdateDoctor } from '../hooks/use-doctors';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';
import type { Doctor } from '../types/doctor-types';

// ============================================================
// Types
// ============================================================

interface DoctorEditDialogProps {
  open: boolean;
  doctor: Doctor;
  onClose: () => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorEditDialog({ open, doctor, onClose }: DoctorEditDialogProps) {
  const updateDoctor = useUpdateDoctor();
  const { showError, showSuccess } = useErrorExperience();

  const handleSubmit = async (data: { name: string; crm: string; specialty: string; email: string }) => {
    try {
      await updateDoctor.mutateAsync({ id: doctor.id, ...data });
      showSuccess('Médico atualizado com sucesso');
      onClose();
    } catch (error) {
      showError(error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth aria-labelledby="edit-doctor-title">
      <DialogTitle id="edit-doctor-title">Editar Médico</DialogTitle>
      <DialogContent>
        <DoctorForm
          initialData={doctor}
          onSubmit={handleSubmit}
          onCancel={onClose}
          loading={updateDoctor.isPending}
          error={updateDoctor.error?.message}
          mode="edit"
        />
      </DialogContent>
    </Dialog>
  );
}
