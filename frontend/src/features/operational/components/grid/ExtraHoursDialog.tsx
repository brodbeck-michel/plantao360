import React, { useMemo, useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Box, Typography, TextField,
  MenuItem, Button, IconButton, Divider, Alert, Tooltip, useTheme,
} from '@mui/material';
import { Close as CloseIcon, Delete as DeleteIcon, MoreTime as MoreTimeIcon } from '@mui/icons-material';
import { SHIFT_TYPES, SHIFT_LABELS, formatHours } from '../../types/operational-types';
import type { DayData } from '../../types/operational-types';
import { getFeatureAccentColors } from '../../utils/feature-accent-colors';

interface ExtraHoursDialogProps {
  open: boolean;
  date: string | null;
  day: DayData | null;
  saving?: boolean;
  onClose: () => void;
  onCreate: (data: { shift_id: number; doctor_id: number; duration_minutes: number; justification: string }) => Promise<void>;
  onDelete: (extraId: number) => Promise<void>;
}

interface DoctorShiftOption {
  key: string;
  shiftId: number;
  doctorId: number;
  doctorName: string;
  shiftType: string;
}

function toMinutes(hhmm: string): number | null {
  if (!hhmm) return null;
  const [h, m] = hhmm.split(':').map((v) => parseInt(v, 10));
  if (Number.isNaN(h) || Number.isNaN(m)) return null;
  return h * 60 + m;
}

export function ExtraHoursDialog({ open, date, day, saving, onClose, onCreate, onDelete }: ExtraHoursDialogProps) {
  const [selectedKey, setSelectedKey] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [justification, setJustification] = useState('');
  const [error, setError] = useState('');
  const theme = useTheme();
  const accent = getFeatureAccentColors(theme.palette.mode);

  useEffect(() => {
    if (open) {
      setSelectedKey('');
      setStartTime('');
      setEndTime('');
      setJustification('');
      setError('');
    }
  }, [open]);

  const doctorOptions: DoctorShiftOption[] = useMemo(() => {
    if (!day) return [];
    const options: DoctorShiftOption[] = [];
    SHIFT_TYPES.forEach((st) => {
      const cell = day.shifts[st];
      if (!cell?.shift_id) return;
      cell.assignments.forEach((a) => {
        options.push({
          key: `${a.doctor_id}-${cell.shift_id}`,
          shiftId: cell.shift_id as number,
          doctorId: a.doctor_id,
          doctorName: a.doctor_name,
          shiftType: st,
        });
      });
    });
    return options;
  }, [day]);

  const existingExtras = useMemo(() => {
    if (!day) return [];
    return SHIFT_TYPES.flatMap((st) => day.shifts[st]?.extras || []);
  }, [day]);

  const durationMinutes = useMemo(() => {
    const s = toMinutes(startTime);
    const e = toMinutes(endTime);
    if (s === null || e === null) return null;
    let diff = e - s;
    if (diff <= 0) diff += 24 * 60;
    return diff;
  }, [startTime, endTime]);

  const dateLabel = date
    ? new Date(date + 'T12:00:00').toLocaleDateString('pt-BR', { weekday: 'short', day: '2-digit', month: 'short' })
    : '';

  const handleAdd = async () => {
    setError('');
    const option = doctorOptions.find((o) => o.key === selectedKey);
    if (!option) { setError('Selecione o medico'); return; }
    if (!durationMinutes || durationMinutes <= 0) { setError('Informe um horario de inicio e fim validos'); return; }
    if (!justification.trim()) { setError('Justificativa e obrigatoria'); return; }
    try {
      await onCreate({
        shift_id: option.shiftId,
        doctor_id: option.doctorId,
        duration_minutes: durationMinutes,
        justification: justification.trim(),
      });
      setSelectedKey('');
      setStartTime('');
      setEndTime('');
      setJustification('');
    } catch (err: any) {
      setError(err?.response?.data?.error?.message || 'Erro ao adicionar hora extra');
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Box display="flex" alignItems="center" gap={1}>
            <MoreTimeIcon sx={{ color: accent.amber.main, fontSize: 20 }} />
            <Typography variant="h6" fontWeight={700} fontSize="1.05rem">Horário Extra</Typography>
          </Box>
          <Typography variant="caption" color="text.secondary">{dateLabel}</Typography>
        </Box>
        <IconButton size="small" onClick={onClose}><CloseIcon fontSize="small" /></IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Typography variant="overline" color="text.secondary" fontWeight={700}>
          Horas extras registradas neste dia
        </Typography>
        {existingExtras.length === 0 ? (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2, mt: 0.5 }}>
            Nenhuma hora extra registrada neste dia.
          </Typography>
        ) : (
          <Box sx={{ mb: 2, mt: 0.5 }}>
            {existingExtras.map((ex) => (
              <Box key={ex.id} sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', py: 0.75 }}>
                <Box>
                  <Typography variant="body2" fontWeight={600}>
                    {ex.doctor_name} · {formatHours(ex.duration_minutes / 60)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">{ex.justification}</Typography>
                </Box>
                <Tooltip title="Remover">
                  <IconButton size="small" onClick={() => onDelete(ex.id)}>
                    <DeleteIcon sx={{ fontSize: 16 }} />
                  </IconButton>
                </Tooltip>
              </Box>
            ))}
          </Box>
        )}

        <Divider sx={{ mb: 2 }} />

        <Typography variant="overline" color="text.secondary" fontWeight={700} sx={{ display: 'block', mb: 1 }}>
          Adicionar hora extra
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

        <TextField
          fullWidth select label="Médico" value={selectedKey}
          onChange={(e) => setSelectedKey(e.target.value)}
          sx={{ mb: 2 }}
          disabled={doctorOptions.length === 0}
          helperText={doctorOptions.length === 0 ? 'Nenhum médico escalado neste dia' : ' '}
        >
          {doctorOptions.map((o) => (
            <MenuItem key={o.key} value={o.key}>
              {o.doctorName} — {SHIFT_LABELS[o.shiftType]}
            </MenuItem>
          ))}
        </TextField>

        <Box display="flex" gap={2} sx={{ mb: 2 }}>
          <TextField
            label="Início" type="time" value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            InputLabelProps={{ shrink: true }}
            sx={{ flex: 1 }}
          />
          <TextField
            label="Fim" type="time" value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            InputLabelProps={{ shrink: true }}
            sx={{ flex: 1 }}
          />
          <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', bgcolor: accent.amber.bg, borderRadius: 1 }}>
            <Typography variant="caption" color="text.secondary">Duração</Typography>
            <Typography variant="body2" fontWeight={700} color="text.primary">
              {durationMinutes ? formatHours(durationMinutes / 60) : '—'}
            </Typography>
          </Box>
        </Box>

        <TextField
          fullWidth multiline minRows={2} label="Justificativa"
          placeholder="Descreva o motivo do horário extra (obrigatório)..."
          value={justification}
          onChange={(e) => setJustification(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Fechar</Button>
        <Button
          variant="contained"
          onClick={handleAdd}
          disabled={saving || !selectedKey || !durationMinutes || !justification.trim()}
          sx={{ bgcolor: '#B45309', '&:hover': { bgcolor: '#92400E' } }}
        >
          {saving ? 'Adicionando...' : 'Adicionar hora extra'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
