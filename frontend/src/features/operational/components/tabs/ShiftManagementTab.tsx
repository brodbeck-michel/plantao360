import React, { useState, useMemo, useEffect, useCallback } from 'react';
import {
  Box, Typography, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, IconButton, Tooltip, Chip, Button, Dialog,
  DialogTitle, DialogContent, DialogActions, TextField, MenuItem, Alert,
} from '@mui/material';
import {
  Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon,
} from '@mui/icons-material';
import { SHIFT_TYPES, SHIFT_LABELS, SHIFT_TIMES } from '../../types/operational-types';
import { apiClient } from '../../../../api/client';
import { getShiftStatusColor, getStatusLabel } from '../../../../shared/constants/status-colors';
import type { PeriodInfo } from '../../types/operational-types';

interface ShiftRecord {
  id: number;
  period_id: number;
  shift_date: string;
  shift_type: string;
  status: string;
  scheduled_start: string | null;
  scheduled_end: string | null;
  doctor_count: number | null;
  total_duration_minutes: number | null;
}

interface ShiftManagementTabProps {
  period: PeriodInfo;
  onShiftCreated?: () => void;
  onShiftUpdated?: () => void;
  onShiftDeleted?: () => void;
  canModify?: boolean;
}

const EMPTY_FORM = { shift_date: '', shift_type: 'T1', doctor_count: 1, total_duration_minutes: 360 };

export function ShiftManagementTab({ period, onShiftCreated, onShiftUpdated, onShiftDeleted, canModify = false }: ShiftManagementTabProps) {
  const [shifts, setShifts] = useState<ShiftRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialog, setEditDialog] = useState<ShiftRecord | null>(null);
  const [newShift, setNewShift] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);

  const loadShifts = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const resp = await apiClient.get(`/shifts?period_id=${period.id}&size=100`);
      setShifts(resp.data.data?.items || []);
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao carregar turnos';
      setError(msg);
    }
    setLoading(false);
  }, [period.id]);

  useEffect(() => { loadShifts(); }, [loadShifts]);

  const handleCreate = useCallback(async () => {
    if (!newShift.shift_date) { setError('Data e obrigatoria'); return; }
    setSaving(true);
    setError('');
    try {
      await apiClient.post('/shifts', {
        period_id: period.id,
        shift_date: newShift.shift_date,
        shift_type: newShift.shift_type,
        doctor_count: newShift.doctor_count,
        total_duration_minutes: newShift.total_duration_minutes,
      });
      setCreateDialogOpen(false);
      setNewShift(EMPTY_FORM);
      loadShifts();
      onShiftCreated?.();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao criar turno';
      setError(msg);
    }
    setSaving(false);
  }, [newShift, period.id, loadShifts, onShiftCreated]);

  const handleEdit = useCallback(async () => {
    if (!editDialog) return;
    setSaving(true);
    setError('');
    try {
      await apiClient.put(`/shifts/${editDialog.id}`, {
        shift_date: editDialog.shift_date,
        shift_type: editDialog.shift_type,
        doctor_count: editDialog.doctor_count,
        total_duration_minutes: editDialog.total_duration_minutes,
        status: editDialog.status,
      });
      setEditDialog(null);
      loadShifts();
      onShiftUpdated?.();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao editar turno';
      setError(msg);
    }
    setSaving(false);
  }, [editDialog, loadShifts, onShiftUpdated]);

  const handleDelete = useCallback(async (shiftId: number) => {
    try {
      await apiClient.delete(`/shifts/${shiftId}`);
      loadShifts();
      onShiftDeleted?.();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao excluir turno';
      setError(msg);
    }
  }, [loadShifts, onShiftDeleted]);


  const grouped = useMemo(() => {
    const byDate: Record<string, ShiftRecord[]> = {};
    shifts.forEach((s) => {
      if (!byDate[s.shift_date]) byDate[s.shift_date] = [];
      byDate[s.shift_date].push(s);
    });
    return Object.entries(byDate).sort(([a], [b]) => a.localeCompare(b));
  }, [shifts]);

  return (
    <Box sx={{ p: 3, overflow: 'auto', flex: 1 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6" fontWeight={700}>
          Gestao de Turnos
        </Typography>
        {canModify && (
          <Button
            variant="contained"
            size="small"
            startIcon={<AddIcon />}
            onClick={() => { setNewShift(EMPTY_FORM); setCreateDialogOpen(true); setError(''); }}
            sx={{ bgcolor: '#00995D', '&:hover': { bgcolor: '#007A4D' } }}
          >
            Novo Turno
          </Button>
        )}
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Data</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Tipo</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Horario</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Status</TableCell>
              <TableCell align="center" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Vagas</TableCell>
              <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Acoes</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {grouped.map(([date, dateShifts]) => (
              dateShifts.map((s, idx) => (
                <TableRow key={s.id} hover>
                  {idx === 0 && (
                    <TableCell
                      rowSpan={dateShifts.length}
                      sx={{ fontWeight: 500, fontSize: '0.8125rem', borderRight: '1px solid #E5E7EB' }}
                    >
                      {new Date(date + 'T12:00:00').toLocaleDateString('pt-BR', { weekday: 'short', day: '2-digit', month: '2-digit' })}
                    </TableCell>
                  )}
                  <TableCell>
                    <Chip label={SHIFT_LABELS[s.shift_type] || s.shift_type} size="small" variant="outlined" sx={{ fontSize: '0.6875rem' }} />
                  </TableCell>
                  <TableCell sx={{ fontSize: '0.8125rem', color: 'text.secondary' }}>
                    {SHIFT_TIMES[s.shift_type]?.start || '?'} – {SHIFT_TIMES[s.shift_type]?.end || '?'}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={getStatusLabel(s.status)}
                      size="small"
                      sx={{
                        backgroundColor: getShiftStatusColor(s.status),
                        color: '#fff',
                        fontWeight: 600,
                        fontSize: '0.6875rem',
                      }}
                    />
                  </TableCell>
                  <TableCell align="center" sx={{ fontSize: '0.8125rem', fontWeight: 500 }}>
                    {s.doctor_count || 0}
                  </TableCell>
                  <TableCell align="right">
                    {canModify && (
                      <>
                        <Tooltip title="Editar">
                          <IconButton size="small" onClick={() => { setEditDialog(s); setError(''); }}>
                            <EditIcon sx={{ fontSize: 16 }} />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Remover">
                          <IconButton size="small" onClick={() => handleDelete(s.id)} sx={{ color: '#FF4842' }}>
                            <DeleteIcon sx={{ fontSize: 16 }} />
                          </IconButton>
                        </Tooltip>
                      </>
                    )}
                  </TableCell>
                </TableRow>
              ))
            ))}
            {grouped.length === 0 && !loading && (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 4, color: 'text.secondary' }}>
                  Nenhum turno encontrado. Clique em "Novo Turno" para criar.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Novo Turno</DialogTitle>
        <DialogContent>
          <TextField fullWidth type="date" label="Data" value={newShift.shift_date}
            onChange={(e) => setNewShift((p) => ({ ...p, shift_date: e.target.value }))}
            sx={{ mt: 1, mb: 2 }} InputLabelProps={{ shrink: true }} />
          <TextField fullWidth select label="Tipo de Turno" value={newShift.shift_type}
            onChange={(e) => setNewShift((p) => ({ ...p, shift_type: e.target.value }))} sx={{ mb: 2 }}>
            {SHIFT_TYPES.map((st) => (
              <MenuItem key={st} value={st}>{SHIFT_LABELS[st]}</MenuItem>
            ))}
          </TextField>
          <TextField fullWidth type="number" label="Vagas" value={newShift.doctor_count}
            onChange={(e) => setNewShift((p) => ({ ...p, doctor_count: parseInt(e.target.value) || 1 }))} sx={{ mb: 2 }} />
          <TextField fullWidth type="number" label="Duracao (minutos)" value={newShift.total_duration_minutes}
            onChange={(e) => setNewShift((p) => ({ ...p, total_duration_minutes: parseInt(e.target.value) || 0 }))} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleCreate} variant="contained" disabled={saving} sx={{ bgcolor: '#00995D' }}>
            {saving ? 'Criando...' : 'Criar'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={!!editDialog} onClose={() => setEditDialog(null)} maxWidth="xs" fullWidth>
        <DialogTitle>Editar Turno</DialogTitle>
        <DialogContent>
          {editDialog && (
            <>
              <TextField fullWidth type="date" label="Data" value={editDialog.shift_date}
                onChange={(e) => setEditDialog((p) => p ? { ...p, shift_date: e.target.value } : null)}
                sx={{ mt: 1, mb: 2 }} InputLabelProps={{ shrink: true }} />
              <TextField fullWidth select label="Tipo de Turno" value={editDialog.shift_type}
                onChange={(e) => setEditDialog((p) => p ? { ...p, shift_type: e.target.value } : null)} sx={{ mb: 2 }}>
                {SHIFT_TYPES.map((st) => (
                  <MenuItem key={st} value={st}>{SHIFT_LABELS[st]}</MenuItem>
                ))}
              </TextField>
              <TextField fullWidth type="number" label="Vagas" value={editDialog.doctor_count || 0}
                onChange={(e) => setEditDialog((p) => p ? { ...p, doctor_count: parseInt(e.target.value) || 0 } : null)} sx={{ mb: 2 }} />
              <TextField fullWidth type="number" label="Duracao (minutos)" value={editDialog.total_duration_minutes || 0}
                onChange={(e) => setEditDialog((p) => p ? { ...p, total_duration_minutes: parseInt(e.target.value) || 0 } : null)} sx={{ mb: 2 }} />
              <TextField fullWidth select label="Status" value={editDialog.status}
                onChange={(e) => setEditDialog((p) => p ? { ...p, status: e.target.value } : null)}>
                <MenuItem value="draft">Rascunho</MenuItem>
                <MenuItem value="scheduled">Agendado</MenuItem>
                <MenuItem value="in_progress">Em andamento</MenuItem>
                <MenuItem value="completed">Concluido</MenuItem>
                <MenuItem value="cancelled">Cancelado</MenuItem>
              </TextField>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialog(null)}>Cancelar</Button>
          <Button onClick={handleEdit} variant="contained" disabled={saving} sx={{ bgcolor: '#00995D' }}>
            {saving ? 'Salvando...' : 'Salvar'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
