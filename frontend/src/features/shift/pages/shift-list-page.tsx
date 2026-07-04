import React, { useState } from 'react';
import {
  Container, Typography, Box, Button, Paper, IconButton, Tooltip,
  Dialog, DialogTitle, DialogContent, DialogActions, TextField, MenuItem,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { DataTable, Column } from '../../../shared/components/data-table';
import { StatusChip } from '../../../shared/components/status-chip';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';
import { apiClient } from '../../../api/client';
import { queryClient } from '../../../providers/query-provider';
import { SHIFT_TYPES, SHIFT_LABELS, SHIFT_TIMES } from '../types/shift-types';
import type { ShiftData } from '../types/shift-types';

export function ShiftListPage() {
  const { showError, showSuccess } = useErrorExperience();
  const [shifts, setShifts] = useState<ShiftData[]>([]);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingShift, setEditingShift] = useState<ShiftData | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<ShiftData | null>(null);
  const [periodId, setPeriodId] = useState<string>('');
  const [shiftType, setShiftType] = useState('T1');
  const [shiftDate, setShiftDate] = useState('');

  const loadShifts = async () => {
    setLoading(true);
    try {
      const params: any = { page: 1, size: 100, sort_by: 'shift_date', sort_direction: 'desc' };
      if (periodId) params.period_id = parseInt(periodId);
      const response = await apiClient.get('/shifts', { params });
      const data = response.data.data?.items || response.data.data || [];
      setShifts(Array.isArray(data) ? data : []);
    } catch (error) {
      showError(error);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => { loadShifts(); }, []);

  const handleCreate = async () => {
    try {
      await apiClient.post('/shifts', {
        period_id: parseInt(periodId) || 1,
        shift_date: shiftDate,
        shift_type: shiftType,
        scheduled_start: SHIFT_TIMES[shiftType]?.start,
        scheduled_end: SHIFT_TIMES[shiftType]?.end,
      });
      showSuccess('Turno criado com sucesso');
      setDialogOpen(false);
      loadShifts();
    } catch (error) {
      showError(error);
    }
  };

  const handleDelete = async () => {
    if (!deleteConfirm) return;
    try {
      await apiClient.delete(`/shifts/${deleteConfirm.id}`);
      showSuccess('Turno excluido com sucesso');
      setDeleteConfirm(null);
      loadShifts();
    } catch (error) {
      showError(error);
    }
  };

  const columns: Column<ShiftData>[] = [
    { id: 'shift_date', label: 'Data', sortable: true, render: (row) => new Date(row.shift_date + 'T12:00:00').toLocaleDateString('pt-BR') },
    { id: 'shift_type', label: 'Tipo', sortable: true, render: (row) => <StatusChip status="info" label={SHIFT_LABELS[row.shift_type] || row.shift_type} /> },
    { id: 'status', label: 'Status', sortable: true, render: (row) => <StatusChip status={row.status as any} /> },
    { id: 'doctor_count', label: 'Vagas', render: (row) => row.doctor_count || '-' },
    {
      id: 'actions', label: 'Acoes', width: 120, render: (row) => (
        <Box display="flex" gap={0.5}>
          <Tooltip title="Editar">
            <IconButton size="small" onClick={() => { setEditingShift(row); setShiftType(row.shift_type); setShiftDate(row.shift_date); setDialogOpen(true); }}>
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Excluir">
            <IconButton size="small" onClick={() => setDeleteConfirm(row)}>
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" fontWeight={600}>Turnos</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => { setEditingShift(null); setShiftDate(''); setShiftType('T1'); setDialogOpen(true); }}>
          Novo Turno
        </Button>
      </Box>

      <Paper sx={{ mb: 2, p: 2 }}>
        <Box display="flex" gap={2} alignItems="center">
          <TextField label="Periodo ID" size="small" value={periodId} onChange={(e) => setPeriodId(e.target.value)} sx={{ width: 120 }} />
          <Button variant="outlined" onClick={loadShifts}>Filtrar</Button>
        </Box>
      </Paper>

      <DataTable columns={columns} data={shifts as any} total={shifts.length} loading={loading} sortBy="shift_date" sortOrder="desc" emptyMessage="Nenhum turno encontrado" />

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>{editingShift ? 'Editar Turno' : 'Novo Turno'}</DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={1}>
            <TextField label="Periodo ID" type="number" value={periodId} onChange={(e) => setPeriodId(e.target.value)} fullWidth />
            <TextField label="Data" type="date" value={shiftDate} onChange={(e) => setShiftDate(e.target.value)} fullWidth InputLabelProps={{ shrink: true }} />
            <TextField label="Tipo" select value={shiftType} onChange={(e) => setShiftType(e.target.value)} fullWidth>
              {SHIFT_TYPES.map((t) => <MenuItem key={t} value={t}>{SHIFT_LABELS[t]}</MenuItem>)}
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleCreate} variant="contained">{editingShift ? 'Salvar' : 'Criar'}</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={!!deleteConfirm} onClose={() => setDeleteConfirm(null)}>
        <DialogTitle>Excluir Turno?</DialogTitle>
        <DialogContent><Typography>Tem certeza?</Typography></DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirm(null)}>Cancelar</Button>
          <Button onClick={handleDelete} color="error" variant="contained">Excluir</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
