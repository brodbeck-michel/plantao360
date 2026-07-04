import React, { useEffect } from 'react';
import { Box, TextField, Grid, Button, CircularProgress, Alert, MenuItem } from '@mui/material';
import { Save, Cancel } from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import type { DoctorFormState } from '../types/doctor-types';

interface DoctorFormProps {
  initialData?: Partial<DoctorFormState>;
  onSubmit: (data: DoctorFormState) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
  error?: string;
  mode?: 'create' | 'edit';
}

const validationRules = {
  name: { required: 'Nome e obrigatorio', minLength: { value: 3, message: 'Nome deve ter no minimo 3 caracteres' } },
  crm: { required: 'CRM e obrigatorio', pattern: { value: /^[0-9]{4,6}$/, message: 'CRM deve ter entre 4 e 6 digitos' } },
  specialty: { required: 'Especialidade e obrigatoria' },
  hour_rate: { required: 'Valor hora e obrigatorio', min: { value: 0.01, message: 'Valor deve ser maior que zero' } },
};

const DOCTOR_TYPES = [
  { value: 'plantonista', label: 'Plantonista' },
  { value: 'diarista', label: 'Diarista' },
  { value: 'freelancer', label: 'Freelancer' },
];

export function DoctorForm({ initialData, onSubmit, onCancel, loading = false, error, mode = 'create' }: DoctorFormProps) {
  const { control, handleSubmit, reset, formState: { errors, isDirty } } = useForm<DoctorFormState>({
    defaultValues: {
      name: initialData?.name || '',
      crm: initialData?.crm || '',
      specialty: initialData?.specialty || 'Clinica Medica',
      email: initialData?.email || '',
      phone: initialData?.phone || '',
      doctor_type: initialData?.doctor_type || 'plantonista',
      hour_rate: initialData?.hour_rate || 150,
    },
  });

  useEffect(() => {
    if (initialData) {
      reset({
        name: initialData.name || '',
        crm: initialData.crm || '',
        specialty: initialData.specialty || 'Clinica Medica',
        email: initialData.email || '',
        phone: initialData.phone || '',
        doctor_type: initialData.doctor_type || 'plantonista',
        hour_rate: initialData.hour_rate || 150,
      });
    }
  }, [initialData, reset]);

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Controller name="name" control={control} rules={validationRules.name} render={({ field }) => (
            <TextField {...field} label="Nome" fullWidth required error={!!errors.name} helperText={errors.name?.message} disabled={loading} autoFocus />
          )} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller name="crm" control={control} rules={validationRules.crm} render={({ field }) => (
            <TextField {...field} label="CRM" fullWidth required error={!!errors.crm} helperText={errors.crm?.message} disabled={loading} placeholder="Ex: 12345" />
          )} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller name="specialty" control={control} rules={validationRules.specialty} render={({ field }) => (
            <TextField {...field} label="Especialidade" fullWidth required error={!!errors.specialty} helperText={errors.specialty?.message} disabled={loading} />
          )} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller name="hour_rate" control={control} rules={validationRules.hour_rate} render={({ field }) => (
            <TextField {...field} label="Valor Hora (R$)" type="number" fullWidth required error={!!errors.hour_rate} helperText={errors.hour_rate?.message} disabled={loading} inputProps={{ min: 0, step: 0.01 }} />
          )} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller name="doctor_type" control={control} render={({ field }) => (
            <TextField {...field} label="Tipo" select fullWidth disabled={loading}>
              {DOCTOR_TYPES.map((t) => <MenuItem key={t.value} value={t.value}>{t.label}</MenuItem>)}
            </TextField>
          )} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller name="phone" control={control} render={({ field }) => (
            <TextField {...field} label="Telefone" fullWidth disabled={loading} placeholder="(27) 99999-0000" />
          )} />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller name="email" control={control} render={({ field }) => (
            <TextField {...field} label="E-mail" type="email" fullWidth disabled={loading} />
          )} />
        </Grid>
      </Grid>
      <Box display="flex" justifyContent="flex-end" gap={1} mt={3}>
        <Button onClick={onCancel} disabled={loading} startIcon={<Cancel />}>Cancelar</Button>
        <Button type="submit" variant="contained" disabled={loading || (mode === 'edit' && !isDirty)} startIcon={loading ? <CircularProgress size={16} /> : <Save />}>
          {mode === 'create' ? 'Criar' : 'Salvar'}
        </Button>
      </Box>
    </Box>
  );
}
