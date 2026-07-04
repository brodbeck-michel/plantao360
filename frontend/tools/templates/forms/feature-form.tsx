/**
 * {{FEATURE_PASCAL}} Form — Plantão 360
 *
 * Formulário de criação/edição de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { Box, TextField, Grid, Button, CircularProgress, Alert } from '@mui/material';
import { Save, Cancel } from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';

interface {{FEATURE_PASCAL}}FormProps {
  initialData?: any;
  onSubmit: (data: any) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
  error?: string;
  mode?: 'create' | 'edit';
}

export function {{FEATURE_PASCAL}}Form({ initialData, onSubmit, onCancel, loading, error, mode = 'create' }: {{FEATURE_PASCAL}}FormProps) {
  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: initialData || { name: '' },
  });

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Controller
            name="name"
            control={control}
            rules={{ required: 'Nome é obrigatório' }}
            render={({ field }) => (
              <TextField {...field} label="Nome" fullWidth required error={!!errors.name} helperText={errors.name?.message} disabled={loading} />
            )}
          />
        </Grid>
      </Grid>
      <Box display="flex" justifyContent="flex-end" gap={1} mt={3}>
        <Button onClick={onCancel} disabled={loading} startIcon={<Cancel />}>Cancelar</Button>
        <Button type="submit" variant="contained" disabled={loading} startIcon={loading ? <CircularProgress size={16} /> : <Save />}>
          {mode === 'create' ? 'Criar' : 'Salvar'}
        </Button>
      </Box>
    </Box>
  );
}
