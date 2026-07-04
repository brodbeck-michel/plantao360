/**
 * DoctorDeleteDialog — Plantão 360
 *
 * Diálogo de exclusão de médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { ConfirmDialog } from '../../../shared/components/confirm-dialog';
import { useDeleteDoctor } from '../hooks/use-doctors';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';
import type { Doctor } from '../types/doctor-types';

// ============================================================
// Types
// ============================================================

interface DoctorDeleteDialogProps {
  open: boolean;
  doctor: Doctor;
  onClose: () => void;
}

// ============================================================
// Component
// ============================================================

export function DoctorDeleteDialog({ open, doctor, onClose }: DoctorDeleteDialogProps) {
  const deleteDoctor = useDeleteDoctor();
  const { showError, showSuccess } = useErrorExperience();

  const handleConfirm = async () => {
    try {
      await deleteDoctor.mutateAsync(doctor.id);
      showSuccess('Médico excluído com sucesso');
      onClose();
    } catch (error) {
      showError(error);
    }
  };

  return (
    <ConfirmDialog
      open={open}
      title="Excluir Médico"
      message={`Tem certeza que deseja excluir o médico "${doctor.name}"? Esta ação não pode ser desfeita.`}
      confirmLabel="Excluir"
      cancelLabel="Cancelar"
      severity="error"
      onConfirm={handleConfirm}
      onCancel={onClose}
      loading={deleteDoctor.isPending}
    />
  );
}
