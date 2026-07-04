/**
 * DoctorDeactivateDialog — Plantão 360
 *
 * Diálogo de desativação de médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { ConfirmDialog } from '../../../shared/components/confirm-dialog';
import { useUpdateDoctor } from '../hooks/use-doctors';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';
import type { Doctor } from '../types/doctor-types';

// ============================================================
// Types
// ============================================================

interface DoctorDeactivateDialogProps {
  open: boolean;
  doctor: Doctor;
  onClose: () => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorDeactivateDialog({ open, doctor, onClose }: DoctorDeactivateDialogProps) {
  const updateDoctor = useUpdateDoctor();
  const { showError, showSuccess } = useErrorExperience();

  const handleConfirm = async () => {
    try {
      await updateDoctor.mutateAsync({ id: doctor.id, active: !doctor.active });
      showSuccess(doctor.active ? 'Médico desativado com sucesso' : 'Médico ativado com sucesso');
      onClose();
    } catch (error) {
      showError(error);
    }
  };

  return (
    <ConfirmDialog
      open={open}
      title={doctor.active ? 'Desativar Médico' : 'Ativar Médico'}
      message={
        doctor.active
          ? `Tem certeza que deseja desativar o médico "${doctor.name}"? Ele não poderá mais ser atribuído a plantões.`
          : `Tem certeza que deseja ativar o médico "${doctor.name}"?`
      }
      confirmLabel={doctor.active ? 'Desativar' : 'Ativar'}
      cancelLabel="Cancelar"
      severity={doctor.active ? 'warning' : 'info'}
      onConfirm={handleConfirm}
      onCancel={onClose}
      loading={updateDoctor.isPending}
    />
  );
}
