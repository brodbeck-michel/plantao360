import React, { forwardRef } from 'react';
import { Box, Table, TableBody, TableContainer, Paper } from '@mui/material';
import { GridHeader } from './GridHeader';
import { AssignmentRow } from './AssignmentRow';
import type { DayData } from '../../types/operational-types';
import type { CellPosition } from '../../hooks/use-workspace-keyboard';

interface AssignmentGridProps {
  days: DayData[];
  activeCell: CellPosition | null;
  onOpenCell: (date: string, shiftType: string, shiftId: number | null, anchorEl: HTMLElement) => void;
  onRemove: (assignmentId: number) => void;
  onContextMenu: (e: React.MouseEvent, date: string, shiftType: string, shiftId: number | null) => void;
  onDrop?: (sourceAssignmentId: number, sourceDoctorId: number, targetDate: string, targetShiftType: string, targetShiftId: number | null) => void;
  sameDayConflicts: Map<string, boolean>;
}

export const AssignmentGrid = forwardRef<HTMLDivElement, AssignmentGridProps>(
  ({ days, activeCell, onOpenCell, onRemove, onContextMenu, onDrop, sameDayConflicts }, ref) => {
    return (
      <Paper ref={ref} variant="outlined" sx={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <TableContainer sx={{ flex: 1, overflow: 'auto' }}>
          <Table
            size="small"
            sx={{
              tableLayout: 'fixed',
              minWidth: 1040,
              '& th, & td': { px: 0, py: 0 },
            }}
          >
            <TableBody>
              <GridHeader />
              {days.map((day, idx) => (
                <AssignmentRow
                  key={day.date}
                  day={day}
                  dayIndex={idx}
                  activeCell={activeCell}
                  onOpenCell={onOpenCell}
                  onRemove={onRemove}
                  onContextMenu={onContextMenu}
                  onDrop={onDrop}
                  sameDayConflicts={sameDayConflicts}
                />
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    );
  }
);

AssignmentGrid.displayName = 'AssignmentGrid';
