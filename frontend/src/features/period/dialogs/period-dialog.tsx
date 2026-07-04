import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, MenuItem, Box } from '@mui/material';
import { useCreatePeriod, useUpdatePeriod } from '../hooks/use-periods';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';
import { MONTH_NAMES } from '../types/period-types';

interface PeriodDialogProps {
  open: boolean;
  onClose: () => void;
  mode: 'create' | 'edit';
  initialData?: { id: number; year: number; month: number };
}

export function PeriodDialog({ open, onClose, mode, initialData }: PeriodDialogProps) {
  const [year, setYear] = useState(initialData?.year || new Date().getFullYear());
  const [month, setMonth] = useState(initialData?.month || new Date().getMonth() + 1);
  const createPeriod = useCreatePeriod();
  const updatePeriod = useUpdatePeriod();
  const { showError, showSuccess } = useErrorExperience();

  useEffect(() => {
    if (initialData) {
      setYear(initialData.year);
      setMonth(initialData.month);
    }
  }, [initialData]);

  const handleSubmit = async () => {
    try {
      if (mode === 'create') {
        await createPeriod.mutateAsync({ year, month });
        showSuccess('Competencia criada com sucesso');
      } else if (initialData) {
        await updatePeriod.mutateAsync({ id: initialData.id, year, month });
        showSuccess('Competencia atualizada com sucesso');
      }
      onClose();
    } catch (error) {
      showError(error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle>{mode === 'create' ? 'Nova Competencia' : 'Editar Competencia'}</DialogTitle>
      <DialogContent>
        <Box display="flex" flexDirection="column" gap={2} mt={1}>
          <TextField
            label="Ano"
            type="number"
            value={year}
            onChange={(e) => setYear(parseInt(e.target.value))}
            fullWidth
            inputProps={{ min: 2000, max: 2100 }}
          />
          <TextField
            label="Mes"
            select
            value={month}
            onChange={(e) => setMonth(parseInt(e.target.value))}
            fullWidth
          >
            {MONTH_NAMES.map((name, idx) => (
              <MenuItem key={idx + 1} value={idx + 1}>{name}</MenuItem>
            ))}
          </TextField>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button onClick={handleSubmit} variant="contained" disabled={createPeriod.isPending || updatePeriod.isPending}>
          {mode === 'create' ? 'Criar' : 'Salvar'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
