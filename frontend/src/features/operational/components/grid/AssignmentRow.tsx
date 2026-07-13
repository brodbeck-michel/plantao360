import React, { useState, useCallback } from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import { AssignmentCell } from './AssignmentCell';
import { SHIFT_TYPES } from '../../types/operational-types';
import type { DayData } from '../../types/operational-types';
import type { CellPosition } from '../../hooks/use-workspace-keyboard';

interface AssignmentRowProps {
  day: DayData;
  dayIndex: number;
  activeCell: CellPosition | null;
  onOpenCell: (date: string, shiftType: string, shiftId: number | null, anchorEl: HTMLElement) => void;
  onRemove: (assignmentId: number) => void;
  onContextMenu: (e: React.MouseEvent, date: string, shiftType: string, shiftId: number | null) => void;
  onDrop?: (sourceAssignmentId: number, sourceDoctorId: number, targetDate: string, targetShiftType: string, targetShiftId: number | null) => void;
  sameDayConflicts: Map<string, boolean>;
}

export function AssignmentRow({ day, dayIndex, activeCell, onOpenCell, onRemove, onContextMenu, onDrop, sameDayConflicts }: AssignmentRowProps) {
  const theme = useTheme();
  const dayNum = new Date(day.date + 'T12:00:00').getDate();
  const isWeekend = day.day_of_week === 'Sab' || day.day_of_week === 'Dom';
  const [dragOverShift, setDragOverShift] = useState<string | null>(null);
  const weekendBg = theme.palette.mode === 'dark' ? theme.palette.primary.main + '14' : '#F0FDF4';
  const weekdayBg = theme.palette.mode === 'dark' ? theme.palette.background.paper : '#F9FAFB';

  const handleDragOver = useCallback((shiftType: string) => {
    setDragOverShift(shiftType);
  }, []);

  const handleDrop = useCallback((shiftType: string, shiftId: number | null) => {
    return (e: React.DragEvent) => {
      e.preventDefault();
      setDragOverShift(null);
      try {
        const data = JSON.parse(e.dataTransfer.getData('application/json'));
        if (data.assignmentId && onDrop) {
          onDrop(data.assignmentId, data.doctorId, day.date, shiftType, shiftId);
        }
      } catch {}
    };
  }, [day.date, onDrop]);

  const handleDragLeave = useCallback(() => {
    setDragOverShift(null);
  }, []);

  return (
    <Box component="tr" sx={{ borderBottom: `1px solid ${theme.palette.divider}` }} onDragLeave={handleDragLeave}>
      <Box
        component="td"
        sx={{
          p: 1.5,
          fontWeight: isWeekend ? 700 : 500,
          fontSize: '0.8125rem',
          color: isWeekend ? theme.palette.primary.main : theme.palette.text.secondary,
          bgcolor: isWeekend ? weekendBg : weekdayBg,
          borderBottom: `1px solid ${theme.palette.divider}`,
          position: 'sticky',
          left: 0,
          zIndex: 1,
          whiteSpace: 'nowrap',
          minWidth: 140,
          outline: activeCell?.dayIndex === dayIndex ? `2px solid ${theme.palette.primary.main}` : 'none',
          outlineOffset: -2,
        }}
      >
        <Typography variant="caption" fontWeight={600} display="block">
          {day.day_of_week} {dayNum}/{String(day.date.split('-')[1]).padStart(2, '0')}
        </Typography>
      </Box>
      {SHIFT_TYPES.map((st) => {
        const cell = day.shifts[st];
        const isActive = activeCell?.dayIndex === dayIndex && activeCell?.shiftType === st;
        const isConflict = sameDayConflicts.get(`${day.date}-${st}`) || false;
        return (
          <AssignmentCell
            key={st}
            cell={cell}
            onOpen={(e) => onOpenCell(day.date, st, cell.shift_id, e)}
            onRemove={onRemove}
            isWeekend={isWeekend}
            isActive={isActive}
            isSameDayConflict={isConflict}
            date={day.date}
            shiftType={st}
            onContextMenu={(e) => onContextMenu(e, day.date, st, cell.shift_id)}
            onDrop={handleDrop(st, cell.shift_id)}
            onDragOver={() => handleDragOver(st)}
            isDragOver={dragOverShift === st}
          />
        );
      })}
      <Box component="td" sx={{ width: 40, minWidth: 40, borderBottom: `1px solid ${theme.palette.divider}` }} />
    </Box>
  );
}
