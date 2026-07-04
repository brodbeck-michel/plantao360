import React, { useState, useMemo, useRef, useEffect } from 'react';
import { Box, Popover, TextField, Typography, InputAdornment, Divider, Chip } from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { DoctorListItem } from './DoctorListItem';
import type { DoctorOption } from '../../types/operational-types';

interface DoctorStats {
  totalShifts: number;
  totalHours: number;
  assignedToday: number;
}

interface QuickAssignPopoverProps {
  open: boolean;
  anchorEl: HTMLElement | null;
  doctors: DoctorOption[];
  assignedDoctorIds: number[];
  doctorStats: Record<number, DoctorStats>;
  onSelect: (doctorId: number) => void;
  onClear: () => void;
  onClose: () => void;
  isLoading?: boolean;
}

export function QuickAssignPopover({
  open,
  anchorEl,
  doctors,
  assignedDoctorIds,
  doctorStats,
  onSelect,
  onClear,
  onClose,
  isLoading,
}: QuickAssignPopoverProps) {
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'hours' | 'shifts'>('name');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      setSearch('');
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  const filtered = useMemo(() => {
    let result = doctors;
    if (search.trim()) {
      const q = search.toLowerCase();
      result = doctors.filter(
        (d) =>
          d.name.toLowerCase().includes(q) ||
          d.crm.toLowerCase().includes(q) ||
          (d.specialty && d.specialty.toLowerCase().includes(q))
      );
    }

    result = [...result].sort((a, b) => {
      if (sortBy === 'hours') {
        const aHours = doctorStats[a.id]?.totalHours || 0;
        const bHours = doctorStats[b.id]?.totalHours || 0;
        return aHours - bHours;
      }
      if (sortBy === 'shifts') {
        const aShifts = doctorStats[a.id]?.totalShifts || 0;
        const bShifts = doctorStats[b.id]?.totalShifts || 0;
        return aShifts - bShifts;
      }
      return a.name.localeCompare(b.name);
    });

    const assigned = result.filter((d) => assignedDoctorIds.includes(d.id));
    const unassigned = result.filter((d) => !assignedDoctorIds.includes(d.id));
    return [...assigned, ...unassigned];
  }, [doctors, search, sortBy, assignedDoctorIds, doctorStats]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && filtered.length === 1) {
      onSelect(filtered[0].id);
      onClose();
    }
  };

  return (
    <Popover
      open={open}
      anchorEl={anchorEl}
      onClose={onClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      transformOrigin={{ vertical: 'top', horizontal: 'left' }}
      slotProps={{
        paper: {
          sx: {
            width: 360,
            maxHeight: 440,
            mt: 0.5,
            borderRadius: '8px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
          },
        },
      }}
    >
      <Box sx={{ p: 1.5 }}>
        <TextField
          inputRef={inputRef}
          fullWidth
          size="small"
          placeholder="Buscar por nome, CRM ou especialidade..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={handleKeyDown}
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
      <Box sx={{ px: 1.5, pb: 1, display: 'flex', gap: 0.5 }}>
        {[
          { key: 'name' as const, label: 'Nome' },
          { key: 'hours' as const, label: 'Menos horas' },
          { key: 'shifts' as const, label: 'Menos turnos' },
        ].map((opt) => (
          <Chip
            key={opt.key}
            label={opt.label}
            size="small"
            onClick={() => setSortBy(opt.key)}
            variant={sortBy === opt.key ? 'filled' : 'outlined'}
            sx={{
              fontSize: '0.6875rem',
              height: 22,
              bgcolor: sortBy === opt.key ? '#00995D' : 'transparent',
              color: sortBy === opt.key ? 'white' : '#6B7280',
              borderColor: sortBy === opt.key ? '#00995D' : '#E5E7EB',
              '&:hover': { bgcolor: sortBy === opt.key ? '#007A4D' : '#F3F4F6' },
            }}
          />
        ))}
      </Box>
      <Divider />
      <Box sx={{ maxHeight: 280, overflow: 'auto', py: 0.5 }}>
        {filtered.length === 0 ? (
          <Box sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary" fontSize="0.8125rem">
              Nenhum médico encontrado
            </Typography>
          </Box>
        ) : (
          filtered.map((doctor) => {
            const stats = doctorStats[doctor.id];
            const isAssigned = assignedDoctorIds.includes(doctor.id);
            return (
              <DoctorListItem
                key={doctor.id}
                doctor={doctor}
                isAssigned={isAssigned}
                stats={stats}
                onSelect={() => { onSelect(doctor.id); onClose(); }}
              />
            );
          })
        )}
      </Box>
      <Divider />
      <Box sx={{ p: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="caption" color="text.secondary" fontSize="0.6875rem">
          {filtered.length} médico{filtered.length !== 1 ? 's' : ''}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {assignedDoctorIds.length > 0 && (
            <Typography
              variant="caption"
              onClick={() => { onClear(); onClose(); }}
              sx={{ color: '#FF4842', cursor: 'pointer', px: 1, py: 0.5, '&:hover': { bgcolor: '#FFEBEE', borderRadius: 1 } }}
            >
              Limpar
            </Typography>
          )}
          <Typography
            variant="caption"
            onClick={onClose}
            sx={{ color: '#6B7280', cursor: 'pointer', px: 1, py: 0.5, '&:hover': { bgcolor: '#F3F4F6', borderRadius: 1 } }}
          >
            Fechar
          </Typography>
        </Box>
      </Box>
    </Popover>
  );
}
