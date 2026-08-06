import React, { useMemo, useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Box, Typography, TextField,
  MenuItem, Button, IconButton, Divider, Alert, Tooltip, useTheme,
} from '@mui/material';
import { Close as CloseIcon, Delete as DeleteIcon, Check as CheckIcon, CallSplit as SplitIcon } from '@mui/icons-material';
import { SHIFT_LABELS, SHIFT_TIMES, formatHours } from '../../types/operational-types';
import type { ShiftCellData, DoctorOption, AssignmentData } from '../../types/operational-types';
import { getFeatureAccentColors } from '../../utils/feature-accent-colors';

interface SplitShiftDialogProps {
  open: boolean;
  date: string | null;
  shiftType: string | null;
  cell: ShiftCellData | null;
  doctors: DoctorOption[];
  saving?: boolean;
  onClose: () => void;
  onCreate: (data: { shift_id: number; doctor_id: number; start_time: string; end_time: string }) => Promise<void>;
  onUpdatePart: (assignmentId: number, data: { start_time: string; end_time: string }) => Promise<void>;
  onRemove: (assignmentId: number) => Promise<void>;
}

function toMinutes(hhmm: string): number | null {
  if (!hhmm) return null;
  const [h, m] = hhmm.split(':').map((v) => parseInt(v, 10));
  if (Number.isNaN(h) || Number.isNaN(m)) return null;
  return h * 60 + m;
}

function rangeOverlaps(aStart: number, aEnd: number, bStart: number, bEnd: number): boolean {
  const aEndAdj = aEnd <= aStart ? aEnd + 24 * 60 : aEnd;
  const bEndAdj = bEnd <= bStart ? bEnd + 24 * 60 : bEnd;
  return aStart < bEndAdj && bStart < aEndAdj;
}

function durationLabel(start: string, end: string): string {
  const s = toMinutes(start);
  const e = toMinutes(end);
  if (s === null || e === null) return '—';
  let diff = e - s;
  if (diff <= 0) diff += 24 * 60;
  return formatHours(diff / 60);
}

function PartRow({ part, onSave, onRemove }: {
  part: AssignmentData;
  onSave: (id: number, data: { start_time: string; end_time: string }) => Promise<void>;
  onRemove: (id: number) => Promise<void>;
}) {
  const [start, setStart] = useState(part.start_time);
  const [end, setEnd] = useState(part.end_time);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setStart(part.start_time);
    setEnd(part.end_time);
  }, [part.start_time, part.end_time]);

  const dirty = start !== part.start_time || end !== part.end_time;

  const handleSave = async () => {
    if (!start || !end) return;
    setSaving(true);
    try {
      await onSave(part.id, { start_time: start, end_time: end });
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 0.75 }}>
      <Typography variant="body2" fontWeight={600} sx={{ flex: '0 0 auto', minWidth: 90 }} noWrap>
        {part.doctor_name}
      </Typography>
      <TextField
        size="small" type="time" value={start}
        onChange={(e) => setStart(e.target.value)}
        InputLabelProps={{ shrink: true }}
        sx={{ width: 110 }}
      />
      <Typography variant="body2" color="text.secondary">–</Typography>
      <TextField
        size="small" type="time" value={end}
        onChange={(e) => setEnd(e.target.value)}
        InputLabelProps={{ shrink: true }}
        sx={{ width: 110 }}
      />
      <Typography variant="caption" color="text.secondary" sx={{ flex: 1, textAlign: 'right' }}>
        {durationLabel(start, end)}
      </Typography>
      {dirty && (
        <Tooltip title="Salvar horário">
          <IconButton size="small" onClick={handleSave} disabled={saving} sx={{ color: '#00995D' }}>
            <CheckIcon sx={{ fontSize: 18 }} />
          </IconButton>
        </Tooltip>
      )}
      <Tooltip title="Remover">
        <IconButton size="small" onClick={() => onRemove(part.id)}>
          <DeleteIcon sx={{ fontSize: 16 }} />
        </IconButton>
      </Tooltip>
    </Box>
  );
}

export function SplitShiftDialog({ open, date, shiftType, cell, doctors, saving, onClose, onCreate, onUpdatePart, onRemove }: SplitShiftDialogProps) {
  const [doctorId, setDoctorId] = useState<number | ''>('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [error, setError] = useState('');
  const theme = useTheme();
  const accent = getFeatureAccentColors(theme.palette.mode);

  useEffect(() => {
    if (open) {
      setDoctorId('');
      setError('');
      const defaults = shiftType ? SHIFT_TIMES[shiftType] : null;
      setStartTime(defaults?.start || '');
      setEndTime(defaults?.end || '');
    }
  }, [open, shiftType]);

  const existingParts = cell?.assignments || [];

  const overlapWarning = useMemo(() => {
    const s = toMinutes(startTime);
    const e = toMinutes(endTime);
    if (s === null || e === null) return null;
    for (const part of existingParts) {
      const ps = toMinutes(part.start_time);
      const pe = toMinutes(part.end_time);
      if (ps === null || pe === null) continue;
      if (rangeOverlaps(s, e, ps, pe)) {
        return `Horário sobrepõe com ${part.doctor_name} (${part.start_time}–${part.end_time})`;
      }
    }
    return null;
  }, [startTime, endTime, existingParts]);

  const dateLabel = date
    ? new Date(date + 'T12:00:00').toLocaleDateString('pt-BR', { weekday: 'short', day: '2-digit', month: 'short' })
    : '';

  const handleAdd = async () => {
    setError('');
    if (!cell?.shift_id) { setError('Turno nao encontrado'); return; }
    if (!doctorId) { setError('Selecione o medico'); return; }
    if (!startTime || !endTime) { setError('Informe inicio e fim'); return; }
    try {
      await onCreate({ shift_id: cell.shift_id, doctor_id: doctorId, start_time: startTime, end_time: endTime });
      setDoctorId('');
    } catch (err: any) {
      setError(err?.response?.data?.error?.message || 'Erro ao dividir turno');
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Box display="flex" alignItems="center" gap={1}>
            <SplitIcon sx={{ color: accent.violet.main, fontSize: 20 }} />
            <Typography variant="h6" fontWeight={700} fontSize="1.05rem">Ajuste / Divisão de Turno</Typography>
          </Box>
          <Typography variant="caption" color="text.secondary">
            {dateLabel} · {shiftType ? SHIFT_LABELS[shiftType] : ''}
          </Typography>
        </Box>
        <IconButton size="small" onClick={onClose}><CloseIcon fontSize="small" /></IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Typography variant="overline" color="text.secondary" fontWeight={700}>
          Médicos neste turno
        </Typography>
        {existingParts.length === 0 ? (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2, mt: 0.5 }}>
            Nenhum médico atribuído ainda.
          </Typography>
        ) : (
          <Box sx={{ mb: 1, mt: 0.5 }}>
            {existingParts.map((a) => (
              <PartRow key={a.id} part={a} onSave={onUpdatePart} onRemove={onRemove} />
            ))}
          </Box>
        )}

        <Divider sx={{ my: 2 }} />

        <Typography variant="overline" color="text.secondary" fontWeight={700} sx={{ display: 'block', mb: 1 }}>
          Adicionar médico com horário específico
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {!error && overlapWarning && <Alert severity="warning" sx={{ mb: 2 }}>{overlapWarning}</Alert>}

        <TextField
          fullWidth select label="Médico" value={doctorId}
          onChange={(e) => setDoctorId(Number(e.target.value))}
          sx={{ mb: 2 }}
        >
          {doctors.filter((d) => d.active).map((d) => (
            <MenuItem key={d.id} value={d.id}>{d.name} — {d.crm}</MenuItem>
          ))}
        </TextField>

        <Box display="flex" gap={2}>
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
        </Box>
        {startTime && endTime && (
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            Duração: {durationLabel(startTime, endTime)}
          </Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Fechar</Button>
        <Button
          variant="contained"
          onClick={handleAdd}
          disabled={saving || !doctorId || !startTime || !endTime}
          sx={{ bgcolor: '#7C3AED', '&:hover': { bgcolor: '#6D28D9' } }}
        >
          {saving ? 'Adicionando...' : 'Adicionar médico'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
