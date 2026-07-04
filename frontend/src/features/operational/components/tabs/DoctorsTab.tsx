import React, { useState, useMemo, useCallback } from 'react';
import {
  Box, Typography, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Chip, IconButton, Tooltip, Button, Dialog,
  DialogTitle, DialogContent, DialogActions, TextField, MenuItem,
  Alert, Snackbar, InputAdornment,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import {
  Add as AddIcon, Edit as EditIcon, Block as DeactivateIcon,
  CheckCircle as ActivateIcon, Delete as DeleteIcon,
} from '@mui/icons-material';
import { apiClient } from '../../../../api/client';
import type { DoctorOption } from '../../types/operational-types';

interface DoctorStats {
  totalShifts: number;
  totalHours: number;
  assignedToday: number;
}

interface DoctorsTabProps {
  doctors: DoctorOption[];
  doctorStats: Record<number, DoctorStats>;
  periodId: string;
  onRefresh: () => void;
}

const EMPTY_FORM = {
  name: '', crm: '', specialty: 'Clinica Medica', phone: '', email: '',
  doctor_type: 'plantonista', hour_rate: 0, active: true,
};

function getStatusColor(stats?: DoctorStats): 'success' | 'warning' | 'error' | 'default' {
  if (!stats) return 'default';
  if (stats.totalHours >= 240) return 'error';
  if (stats.totalHours >= 180) return 'warning';
  return 'success';
}

function getStatusLabel(stats?: DoctorStats): string {
  if (!stats) return 'Sem dados';
  if (stats.totalHours >= 240) return 'Carga alta';
  if (stats.totalHours >= 180) return 'Carga moderada';
  return 'Disponivel';
}

export function DoctorsTab({ doctors, doctorStats, periodId, onRefresh }: DoctorsTabProps) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingDoctor, setEditingDoctor] = useState<DoctorOption | null>(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const [confirmDeactivate, setConfirmDeactivate] = useState<DoctorOption | null>(null);

  const [search, setSearch] = useState('');

  const sorted = useMemo(() => {
    let result = [...doctors];
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter((d) =>
        d.name.toLowerCase().includes(q) ||
        d.crm.toLowerCase().includes(q) ||
        (d.specialty && d.specialty.toLowerCase().includes(q)) ||
        ((d as any).phone && (d as any).phone.toLowerCase().includes(q))
      );
    }
    return result.sort((a, b) => {
      const statsA = doctorStats[a.id];
      const statsB = doctorStats[b.id];
      return (statsB?.totalHours || 0) - (statsA?.totalHours || 0);
    });
  }, [doctors, doctorStats, search]);

  const openCreate = useCallback(() => {
    setEditingDoctor(null);
    setForm(EMPTY_FORM);
    setError('');
    setDialogOpen(true);
  }, []);

  const openEdit = useCallback((doctor: DoctorOption) => {
    setEditingDoctor(doctor);
    setForm({
      name: doctor.name,
      crm: doctor.crm,
      specialty: doctor.specialty || 'Clinica Medica',
      phone: (doctor as any).phone || '',
      email: (doctor as any).email || '',
      doctor_type: (doctor as any).doctor_type || 'plantonista',
      hour_rate: doctor.hour_rate,
      active: doctor.active,
    });
    setError('');
    setDialogOpen(true);
  }, []);

  const handleSave = useCallback(async () => {
    if (!form.name.trim()) { setError('Nome e obrigatorio'); return; }
    if (!form.crm.trim()) { setError('CRM e obrigatorio'); return; }
    setSaving(true);
    setError('');
    try {
      if (editingDoctor) {
        await apiClient.put(`/doctors/${editingDoctor.id}`, {
          name: form.name,
          crm: form.crm,
          specialty: form.specialty,
          phone: form.phone || null,
          email: form.email || null,
          doctor_type: form.doctor_type,
          hour_rate: form.hour_rate,
        });
        setToast({ open: true, message: 'Medico atualizado com sucesso', severity: 'success' });
      } else {
        await apiClient.post('/doctors', {
          name: form.name,
          crm: form.crm,
          specialty: form.specialty,
          phone: form.phone || null,
          email: form.email || null,
          doctor_type: form.doctor_type,
          hour_rate: form.hour_rate,
        });
        setToast({ open: true, message: 'Medico criado com sucesso', severity: 'success' });
      }
      setDialogOpen(false);
      onRefresh();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || err?.message || 'Erro ao salvar medico';
      setError(msg);
    }
    setSaving(false);
  }, [form, editingDoctor, onRefresh]);

  const handleDeactivate = useCallback(async () => {
    if (!confirmDeactivate) return;
    try {
      await apiClient.put(`/doctors/${confirmDeactivate.id}`, { active: false });
      setToast({ open: true, message: 'Medico inativado', severity: 'success' });
      setConfirmDeactivate(null);
      onRefresh();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao inativar';
      setToast({ open: true, message: msg, severity: 'error' });
    }
  }, [confirmDeactivate, onRefresh]);

  const handleActivate = useCallback(async (doctor: DoctorOption) => {
    try {
      await apiClient.put(`/doctors/${doctor.id}`, { active: true });
      setToast({ open: true, message: 'Medico reativado', severity: 'success' });
      onRefresh();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao reativar';
      setToast({ open: true, message: msg, severity: 'error' });
    }
  }, [onRefresh]);

  return (
    <Box sx={{ p: 3, overflow: 'auto', flex: 1 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3} gap={2}>
        <Typography variant="h6" fontWeight={700} sx={{ flexShrink: 0 }}>
          Medicos da Competencia
        </Typography>
        <Box display="flex" gap={1} alignItems="center" sx={{ flex: 1, maxWidth: 400 }}>
          <TextField
            size="small"
            placeholder="Pesquisar por nome, CRM, especialidade ou telefone..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            fullWidth
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ fontSize: 18, color: '#9CA3AF' }} />
                </InputAdornment>
              ),
            }}
            sx={{ '& .MuiOutlinedInput-root': { fontSize: '0.8125rem' } }}
          />
        </Box>
        <Button
          variant="contained"
          size="small"
          startIcon={<AddIcon />}
          onClick={openCreate}
          sx={{ bgcolor: '#00995D', '&:hover': { bgcolor: '#007A4D' }, flexShrink: 0 }}
        >
          Novo Medico
        </Button>
      </Box>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Nome</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>CRM</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Especialidade</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Tipo</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Telefone</TableCell>
              <TableCell align="center" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Plantoes</TableCell>
              <TableCell align="center" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Horas</TableCell>
              <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Vlr/Hora</TableCell>
              <TableCell align="center" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Status</TableCell>
              <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Acoes</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sorted.map((doctor) => {
              const stats = doctorStats[doctor.id];
              return (
                <TableRow key={doctor.id} hover sx={{ opacity: doctor.active ? 1 : 0.5 }}>
                  <TableCell sx={{ fontSize: '0.8125rem', fontWeight: 500 }}>{doctor.name}</TableCell>
                  <TableCell sx={{ fontSize: '0.8125rem', color: 'text.secondary' }}>{doctor.crm}</TableCell>
                  <TableCell sx={{ fontSize: '0.8125rem', color: 'text.secondary' }}>{doctor.specialty}</TableCell>
                  <TableCell sx={{ fontSize: '0.8125rem', color: 'text.secondary' }}>{(doctor as any).doctor_type || 'plantonista'}</TableCell>
                  <TableCell sx={{ fontSize: '0.8125rem', color: 'text.secondary' }}>{(doctor as any).phone || '-'}</TableCell>
                  <TableCell align="center" sx={{ fontSize: '0.8125rem', fontWeight: 500 }}>
                    {stats?.totalShifts || 0}
                  </TableCell>
                  <TableCell align="center" sx={{ fontSize: '0.8125rem', fontWeight: 500 }}>
                    {stats ? `${stats.totalHours.toFixed(0)}h` : '0h'}
                  </TableCell>
                  <TableCell align="right" sx={{ fontSize: '0.8125rem' }}>
                    R$ {doctor.hour_rate.toFixed(2)}
                  </TableCell>
                  <TableCell align="center">
                    <Chip
                      label={doctor.active ? getStatusLabel(stats) : 'Inativo'}
                      size="small"
                      color={doctor.active ? getStatusColor(stats) : 'default'}
                      variant="outlined"
                      sx={{ fontSize: '0.6875rem' }}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="Editar">
                      <IconButton size="small" onClick={() => openEdit(doctor)}>
                        <EditIcon sx={{ fontSize: 16 }} />
                      </IconButton>
                    </Tooltip>
                    {doctor.active ? (
                      <Tooltip title="Inativar">
                        <IconButton size="small" onClick={() => setConfirmDeactivate(doctor)} sx={{ color: '#FFB020' }}>
                          <DeactivateIcon sx={{ fontSize: 16 }} />
                        </IconButton>
                      </Tooltip>
                    ) : (
                      <Tooltip title="Reativar">
                        <IconButton size="small" onClick={() => handleActivate(doctor)} sx={{ color: '#00B87A' }}>
                          <ActivateIcon sx={{ fontSize: 16 }} />
                        </IconButton>
                      </Tooltip>
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingDoctor ? 'Editar Medico' : 'Novo Medico'}</DialogTitle>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <TextField fullWidth label="Nome" value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} sx={{ mt: 1, mb: 2 }} />
          <TextField fullWidth label="CRM" value={form.crm} onChange={(e) => setForm((p) => ({ ...p, crm: e.target.value }))} sx={{ mb: 2 }} />
          <TextField fullWidth select label="Especialidade" value={form.specialty} onChange={(e) => setForm((p) => ({ ...p, specialty: e.target.value }))} sx={{ mb: 2 }}>
            {['Clinica Medica', 'Pediatria', 'Obstetricia', 'Cirurgia', 'Ortopedia', 'Anestesiologia', 'Radiologia', 'Dermatologia', 'Urologia', 'Infectologia', 'Patologia', 'Neurologia', 'Cardiologia', 'Gastroenterologia', 'Pneumologia'].map((s) => (
              <MenuItem key={s} value={s}>{s}</MenuItem>
            ))}
          </TextField>
          <TextField fullWidth select label="Tipo" value={form.doctor_type} onChange={(e) => setForm((p) => ({ ...p, doctor_type: e.target.value }))} sx={{ mb: 2 }}>
            <MenuItem value="plantonista">Plantonista</MenuItem>
            <MenuItem value="residente">Residente</MenuItem>
            <MenuItem value="staff">Staff</MenuItem>
          </TextField>
          <TextField fullWidth label="Telefone" value={form.phone} onChange={(e) => setForm((p) => ({ ...p, phone: e.target.value }))} sx={{ mb: 2 }} />
          <TextField fullWidth label="Email" value={form.email} onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))} sx={{ mb: 2 }} />
          <TextField fullWidth type="number" label="Valor Hora (R$)" value={form.hour_rate} onChange={(e) => setForm((p) => ({ ...p, hour_rate: parseFloat(e.target.value) || 0 }))} sx={{ mb: 2 }} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleSave} variant="contained" disabled={saving} sx={{ bgcolor: '#00995D' }}>
            {saving ? 'Salvando...' : 'Salvar'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={!!confirmDeactivate} onClose={() => setConfirmDeactivate(null)} maxWidth="xs">
        <DialogTitle>Inativar Medico</DialogTitle>
        <DialogContent>
          <Typography>Tem certeza que deseja inativar {confirmDeactivate?.name}?</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            O medico nao sera mais exibido nas listagens de atribuicao.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDeactivate(null)}>Cancelar</Button>
          <Button onClick={handleDeactivate} variant="contained" color="warning">Inativar</Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={toast.open} autoHideDuration={3000} onClose={() => setToast((p) => ({ ...p, open: false }))} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert onClose={() => setToast((p) => ({ ...p, open: false }))} severity={toast.severity} variant="filled">{toast.message}</Alert>
      </Snackbar>
    </Box>
  );
}
