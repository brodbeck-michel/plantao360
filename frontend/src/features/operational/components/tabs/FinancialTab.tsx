import React, { useMemo } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Divider } from '@mui/material';
import { AttachMoney as MoneyIcon } from '@mui/icons-material';
import { SHIFT_TYPES, SHIFT_TIMES } from '../../types/operational-types';
import type { DayData, DoctorOption } from '../../types/operational-types';

interface FinancialTabProps {
  days: DayData[];
  doctors: DoctorOption[];
}

export function FinancialTab({ days, doctors }: FinancialTabProps) {
  const doctorFinancials = useMemo(() => {
    const map: Record<number, { name: string; crm: string; totalHours: number; totalValue: number; shiftCount: number; hourRate: number }> = {};
    doctors.forEach((d) => {
      map[d.id] = { name: d.name, crm: d.crm, totalHours: 0, totalValue: 0, shiftCount: 0, hourRate: d.hour_rate };
    });
    days.forEach((day) => {
      SHIFT_TYPES.forEach((st) => {
        day.shifts[st].assignments.forEach((a) => {
          const doc = map[a.doctor_id];
          if (doc) {
            const parts_s = a.start_time.split(':');
            const parts_e = a.end_time.split(':');
            let startMin = parseInt(parts_s[0]) * 60 + parseInt(parts_s[1]);
            let endMin = parseInt(parts_e[0]) * 60 + parseInt(parts_e[1]);
            if (endMin <= startMin) endMin += 24 * 60;
            const hours = (endMin - startMin) / 60;
            doc.totalHours += hours;
            doc.totalValue += hours * doc.hourRate;
            doc.shiftCount += 1;
          }
        });
      });
    });
    return Object.values(map).filter((d) => d.shiftCount > 0).sort((a, b) => b.totalValue - a.totalValue);
  }, [days, doctors]);

  const grandTotal = doctorFinancials.reduce((sum, d) => sum + d.totalValue, 0);
  const grandHours = doctorFinancials.reduce((sum, d) => sum + d.totalHours, 0);

  return (
    <Box sx={{ p: 3, overflow: 'auto', flex: 1 }}>
      <Box display="flex" alignItems="center" gap={1} mb={3}>
        <MoneyIcon sx={{ color: '#00995D' }} />
        <Typography variant="h6" fontWeight={700}>Financeiro</Typography>
      </Box>

      <Box display="flex" gap={2} mb={3}>
        <Paper variant="outlined" sx={{ p: 2, flex: 1 }}>
          <Typography variant="caption" color="text.secondary">Total Horas</Typography>
          <Typography variant="h5" fontWeight={700}>{grandHours.toFixed(1)}h</Typography>
        </Paper>
        <Paper variant="outlined" sx={{ p: 2, flex: 1 }}>
          <Typography variant="caption" color="text.secondary">Total Geral</Typography>
          <Typography variant="h5" fontWeight={700} color="#00995D">R$ {grandTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</Typography>
        </Paper>
      </Box>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Medico</TableCell>
              <TableCell sx={{ fontWeight: 600, fontSize: '0.75rem' }}>CRM</TableCell>
              <TableCell align="center" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Plantoes</TableCell>
              <TableCell align="center" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Horas</TableCell>
              <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Valor/Hora</TableCell>
              <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.75rem' }}>Total</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {doctorFinancials.map((d) => (
              <TableRow key={d.name} hover>
                <TableCell sx={{ fontSize: '0.8125rem', fontWeight: 500 }}>{d.name}</TableCell>
                <TableCell sx={{ fontSize: '0.8125rem', color: 'text.secondary' }}>{d.crm}</TableCell>
                <TableCell align="center" sx={{ fontSize: '0.8125rem' }}>{d.shiftCount}</TableCell>
                <TableCell align="center" sx={{ fontSize: '0.8125rem' }}>{d.totalHours.toFixed(1)}h</TableCell>
                <TableCell align="right" sx={{ fontSize: '0.8125rem' }}>R$ {d.hourRate.toFixed(2)}</TableCell>
                <TableCell align="right" sx={{ fontSize: '0.8125rem', fontWeight: 600, color: '#00995D' }}>
                  R$ {d.totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </TableCell>
              </TableRow>
            ))}
            {doctorFinancials.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 4, color: 'text.secondary' }}>
                  Nenhum dado financeiro disponivel
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
