import React, { useCallback } from 'react';
import { Box, Typography, IconButton, Tooltip } from '@mui/material';
import { Add as AddIcon, Close as CloseIcon, DragIndicator as DragIcon } from '@mui/icons-material';
import type { ShiftCellData } from '../../types/operational-types';

interface AssignmentCellProps {
  cell: ShiftCellData;
  onOpen: (event: HTMLElement) => void;
  onRemove: (assignmentId: number) => void;
  isWeekend: boolean;
  isActive: boolean;
  isSameDayConflict: boolean;
  date: string;
  shiftType: string;
  onContextMenu: (e: React.MouseEvent) => void;
  onDragStart?: (e: React.DragEvent, assignmentId: number, doctorId: number) => void;
  onDragOver?: (e: React.DragEvent) => void;
  onDrop?: (e: React.DragEvent) => void;
  isDragOver?: boolean;
}

export function AssignmentCell({
  cell,
  onOpen,
  onRemove,
  isWeekend,
  isActive,
  isSameDayConflict,
  date,
  shiftType,
  onContextMenu,
  onDragStart,
  onDragOver,
  onDrop,
  isDragOver,
}: AssignmentCellProps) {
  const hasAssignments = cell.assignments.length > 0;

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    onDragOver?.(e);
  }, [onDragOver]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    onDrop?.(e);
  }, [onDrop]);

  const handleDoubleClick = useCallback(() => {
    const el = document.querySelector(`[data-date="${date}"][data-shift="${shiftType}"]`) as HTMLElement;
    if (el) onOpen(el);
  }, [date, shiftType, onOpen]);

  return (
    <Box
      component="td"
      data-date={date}
      data-shift={shiftType}
      onClick={(e) => onOpen(e.currentTarget)}
      onDoubleClick={handleDoubleClick}
      onContextMenu={onContextMenu}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      sx={{
        p: 0.5,
        minHeight: 44,
        borderRight: '1px solid #E5E7EB',
        bgcolor: isDragOver ? '#D4F5E4' : isWeekend ? '#FAFBFC' : '#FFFFFF',
        cursor: 'pointer',
        transition: 'background-color 150ms, box-shadow 150ms',
        outline: isActive ? '2px solid #00995D' : 'none',
        outlineOffset: -2,
        boxShadow: isActive ? '0 0 0 1px rgba(0,153,93,0.3)' : isDragOver ? '0 0 0 2px #00995D' : 'none',
        '&:hover': {
          bgcolor: isActive ? '#D4F5E4' : isDragOver ? '#D4F5E4' : '#E6F7EF',
        },
        verticalAlign: 'middle',
      }}
    >
      {hasAssignments ? (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.25 }}>
          {cell.assignments.map((a) => (
            <Box
              key={a.id}
              draggable
              onDragStart={(e) => {
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('application/json', JSON.stringify({
                  assignmentId: a.id,
                  doctorId: a.doctor_id,
                  sourceDate: date,
                  sourceShift: shiftType,
                }));
                onDragStart?.(e, a.id, a.doctor_id);
              }}
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                bgcolor: isSameDayConflict ? '#FEF3C7' : '#E6F7EF',
                border: `1px solid ${isSameDayConflict ? '#FCD34D' : '#A7F3D0'}`,
                borderRadius: '4px',
                px: 0.75,
                py: 0.25,
                cursor: 'grab',
                '&:active': { cursor: 'grabbing' },
                '&:hover': { boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
              }}
            >
              <DragIcon sx={{ fontSize: 12, color: '#9CA3AF', mr: 0.5, flexShrink: 0 }} />
              <Tooltip title={`${a.doctor_name} (${a.start_time}–${a.end_time})`} arrow>
                <Typography
                  variant="caption"
                  fontWeight={500}
                  fontSize="0.8125rem"
                  color={isSameDayConflict ? '#92400E' : '#065F46'}
                  noWrap
                  sx={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis' }}
                >
                  {a.doctor_name}
                </Typography>
              </Tooltip>
              <IconButton
                size="small"
                onClick={(e) => {
                  e.stopPropagation();
                  onRemove(a.id);
                }}
                sx={{
                  ml: 0.5,
                  p: 0,
                  color: '#9CA3AF',
                  '&:hover': { color: '#FF4842', bgcolor: '#FFEBEE' },
                }}
              >
                <CloseIcon sx={{ fontSize: 14 }} />
              </IconButton>
            </Box>
          ))}
        </Box>
      ) : (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            minHeight: 36,
            color: '#9CA3AF',
            fontSize: '0.8125rem',
            '&:hover': { color: '#00995D' },
          }}
        >
          <AddIcon sx={{ fontSize: 16, opacity: 0.5 }} />
          <Typography variant="caption" ml={0.5} fontSize="0.75rem">
            vazio
          </Typography>
        </Box>
      )}
    </Box>
  );
}
