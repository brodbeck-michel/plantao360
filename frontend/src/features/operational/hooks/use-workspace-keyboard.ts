import { useCallback, useEffect, useRef } from 'react';
import { SHIFT_TYPES } from '../types/operational-types';
import type { DayData } from '../types/operational-types';

export interface CellPosition {
  dayIndex: number;
  shiftType: string;
}

interface UseWorkspaceKeyboardProps {
  days: DayData[];
  activeCell: CellPosition | null;
  setActiveCell: (pos: CellPosition | null) => void;
  onOpenCell: (date: string, shiftType: string, shiftId: number | null, anchorEl: HTMLElement) => void;
  onRemoveActive?: () => void;
  onCopy?: () => void;
  onPaste?: () => void;
  onDoubleCell?: (date: string, shiftType: string, shiftId: number | null) => void;
  isPopoverOpen: boolean;
  onClosePopover: () => void;
  onUndo?: () => void;
  onRedo?: () => void;
}

export function useWorkspaceKeyboard({
  days,
  activeCell,
  setActiveCell,
  onOpenCell,
  onRemoveActive,
  onCopy,
  onPaste,
  onDoubleCell,
  isPopoverOpen,
  onClosePopover,
  onUndo,
  onRedo,
}: UseWorkspaceKeyboardProps) {
  const gridRef = useRef<HTMLDivElement>(null);

  const getCellElement = useCallback((pos: CellPosition): HTMLElement | null => {
    const day = days[pos.dayIndex];
    if (!day) return null;
    return gridRef.current?.querySelector(
      `[data-date="${day.date}"][data-shift="${pos.shiftType}"]`
    ) as HTMLElement | null;
  }, [days, gridRef]);

  const moveActiveCell = useCallback((rowDelta: number, colDelta: number) => {
    if (!activeCell) {
      if (days.length > 0) {
        setActiveCell({ dayIndex: 0, shiftType: SHIFT_TYPES[0] });
      }
      return;
    }
    const currentColIdx = SHIFT_TYPES.indexOf(activeCell.shiftType as typeof SHIFT_TYPES[number]);
    let newDayIdx = activeCell.dayIndex + rowDelta;
    let newColIdx = currentColIdx + colDelta;

    if (newColIdx < 0) { newColIdx = SHIFT_TYPES.length - 1; newDayIdx -= 1; }
    if (newColIdx >= SHIFT_TYPES.length) { newColIdx = 0; newDayIdx += 1; }
    newDayIdx = Math.max(0, Math.min(days.length - 1, newDayIdx));
    newColIdx = Math.max(0, Math.min(SHIFT_TYPES.length - 1, newColIdx));

    const newPos = { dayIndex: newDayIdx, shiftType: SHIFT_TYPES[newColIdx] };
    setActiveCell(newPos);
    const el = gridRef.current?.querySelector(
      `[data-date="${days[newDayIdx]?.date}"][data-shift="${SHIFT_TYPES[newColIdx]}"]`
    ) as HTMLElement | null;
    el?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }, [activeCell, days, setActiveCell, gridRef]);

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    const target = e.target as HTMLElement;
    const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable;

    if (e.ctrlKey || e.metaKey) {
      if (e.key === 'z' && !e.shiftKey) { e.preventDefault(); onUndo?.(); return; }
      if ((e.key === 'z' && e.shiftKey) || e.key === 'y') { e.preventDefault(); onRedo?.(); return; }
      if (e.key === 'c' && activeCell && !isInput) { e.preventDefault(); onCopy?.(); return; }
      if (e.key === 'v' && activeCell && !isInput) { e.preventDefault(); onPaste?.(); return; }
      return;
    }

    if (isPopoverOpen) {
      if (e.key === 'Escape') { e.preventDefault(); onClosePopover(); return; }
      return;
    }

    if (isInput) return;

    switch (e.key) {
      case 'ArrowUp': e.preventDefault(); moveActiveCell(-1, 0); break;
      case 'ArrowDown': e.preventDefault(); moveActiveCell(1, 0); break;
      case 'ArrowLeft': e.preventDefault(); moveActiveCell(0, -1); break;
      case 'ArrowRight': e.preventDefault(); moveActiveCell(0, 1); break;
      case 'Tab':
        e.preventDefault();
        if (e.shiftKey) moveActiveCell(0, -1);
        else moveActiveCell(0, 1);
        break;
      case 'Enter':
        e.preventDefault();
        if (activeCell) {
          const day = days[activeCell.dayIndex];
          if (day) {
            const cell = day.shifts[activeCell.shiftType];
            const el = getCellElement(activeCell);
            if (el) onOpenCell(day.date, activeCell.shiftType, cell.shift_id, el);
          }
        }
        break;
      case 'Delete':
      case 'Backspace':
        e.preventDefault();
        if (activeCell) onRemoveActive?.();
        break;
      case 'Home':
        e.preventDefault();
        if (activeCell) setActiveCell({ ...activeCell, shiftType: SHIFT_TYPES[0] });
        break;
      case 'End':
        e.preventDefault();
        if (activeCell) setActiveCell({ ...activeCell, shiftType: SHIFT_TYPES[SHIFT_TYPES.length - 1] });
        break;
      case 'PageUp':
        e.preventDefault();
        moveActiveCell(-7, 0);
        break;
      case 'PageDown':
        e.preventDefault();
        moveActiveCell(7, 0);
        break;
      default:
        break;
    }
  }, [activeCell, days, isPopoverOpen, moveActiveCell, onOpenCell, onRemoveActive, onCopy, onPaste, onClosePopover, getCellElement, onUndo, onRedo, setActiveCell]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  return { gridRef };
}
