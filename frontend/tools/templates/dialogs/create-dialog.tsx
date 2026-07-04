/**
 * {{FEATURE_PASCAL}} Create Dialog — Plantão 360
 *
 * Diálogo de criação de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { Dialog, DialogTitle, DialogContent } from '@mui/material';
import {{FEATURE_PASCAL}}Form } from '../forms/{{FEATURE_NAME}}-form';
import { useCreate{{FEATURE_PASCAL}} } from '../hooks/use-{{FEATURE_NAME}}s';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';

interface {{FEATURE_PASCAL}}CreateDialogProps {
  open: boolean;
  onClose: () => void;
}

export function {{FEATURE_PASCAL}}CreateDialog({ open, onClose }: {{FEATURE_PASCAL}}CreateDialogProps) {
  const createItem = useCreate{{FEATURE_PASCAL}}();
  const { showError, showSuccess } = useErrorExperience();

  const handleSubmit = async (data: any) => {
    try {
      await createItem.mutateAsync(data);
      showSuccess('Registro criado com sucesso');
      onClose();
    } catch (error) {
      showError(error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Novo {{FEATURE_PASCAL}}</DialogTitle>
      <DialogContent>
        {{FEATURE_PASCAL}}Form onSubmit={handleSubmit} onCancel={onClose} loading={createItem.isPending} mode="create" />
      </DialogContent>
    </Dialog>
  );
}
