import React, { useEffect } from 'react';
import { Box, TextField, Grid, Button, CircularProgress, Alert, MenuItem, FormControlLabel, Switch, Chip, Typography } from '@mui/material';
import { Save, Cancel } from '@mui/icons-material';
import { useForm, Controller, useWatch } from 'react-hook-form';
import type { DoctorFormState } from '../types/doctor-types';
import { computeHourRate } from '../utils/hour-rate-table';

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
  career_start_date: {
    required: 'Data de inicio de carreira e obrigatoria',
    validate: (value: string) => {
      if (!value) return true;
      return new Date(value) <= new Date() || 'Data nao pode ser no futuro';
    },
  },
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
      has_rqe: initialData?.has_rqe || false,
      career_start_date: initialData?.career_start_date || '',
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
        has_rqe: initialData.has_rqe || false,
        career_start_date: initialData.career_start_date || '',
      });
    }
  }, [initialData, reset]);

  const hasRqe = useWatch({ control, name: 'has_rqe' });
  const careerStartDate = useWatch({ control, name: 'career_start_date' });
  const preview = careerStartDate ? computeHourRate(hasRqe, careerStartDate) : null;

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
        <Grid item xs={12} sm={6}>
          <Controller name="career_start_date" control={control} rules={validationRules.career_start_date} render={({ field }) => (
            <TextField {...field} label="Início de carreira" type="date" fullWidth required error={!!errors.career_start_date} helperText={errors.career_start_date?.message} disabled={loading} InputLabelProps={{ shrink: true }} />
          )} />
        </Grid>
        <Grid item xs={12} sm={6} display="flex" alignItems="center">
          <Controller name="has_rqe" control={control} render={({ field }) => (
            <FormControlLabel
              control={<Switch checked={field.value} onChange={(e) => field.onChange(e.target.checked)} disabled={loading} />}
              label="Possui RQE"
            />
          )} />
        </Grid>
        <Grid item xs={12}>
          <Box display="flex" alignItems="center" gap={1} sx={{ p: 1.5, bgcolor: 'action.hover', borderRadius: 1 }}>
            <Typography variant="body2" color="text.secondary">Valor hora calculado:</Typography>
            {preview ? (
              <>
                <Chip label={preview.tier} size="small" color="primary" variant="outlined" />
                <Typography variant="body2" fontWeight={700}>
                  R$ {preview.rate.toFixed(2)}
                </Typography>
              </>
            ) : (
              <Typography variant="body2" color="text.secondary">preencha a data de início de carreira</Typography>
            )}
          </Box>
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
