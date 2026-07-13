import React, { useState, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, CircularProgress, Typography, Snackbar, Alert, useTheme } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { useWorkspace, useAssignDoctor, useSwapDoctor, useRemoveAssignment, useMoveAssignment, useDuplicateDay, useDuplicateWeek } from '../hooks/use-workspace';
import { useWorkspaceKeyboard } from '../hooks/use-workspace-keyboard';
import { useUndoRedo } from '../hooks/use-undo-redo';
import { AssignmentGrid } from '../components/grid/AssignmentGrid';
import { CellContextMenu } from '../components/grid/CellContextMenu';
import { QuickAssignPopover } from '../components/quick-assign/QuickAssignPopover';
import { CoverageSidebar } from '../components/sidebar/CoverageSidebar';
import { WorkspaceHeader } from '../components/workspace/WorkspaceHeader';
import { WorkspaceTabs } from '../components/workspace/WorkspaceTabs';
import { SummaryTab } from '../components/tabs/SummaryTab';
import { DoctorsTab } from '../components/tabs/DoctorsTab';
import { ShiftManagementTab } from '../components/tabs/ShiftManagementTab';
import { FinancialTab } from '../components/tabs/FinancialTab';
import { ReportsTab } from '../components/tabs/ReportsTab';
import { SHIFT_TYPES, SHIFT_TIMES, MONTH_NAMES } from '../types/operational-types';
import { useAuth } from '../../../contexts/AuthContext';
import { canEdit } from '../../../rbac';
import { useBreadcrumbLabel } from '../../../contexts/BreadcrumbContext';
import type { CellPosition } from '../hooks/use-workspace-keyboard';

interface CellContext {
  date: string;
  shiftType: string;
  shiftId: number | null;
  anchorEl: HTMLElement;
  existingAssignmentIds: number[];
}

interface ContextMenuState {
  anchorEl: HTMLElement | null;
  date: string;
  shiftType: string;
  shiftId: number | null;
}

interface ToastState {
  open: boolean;
  message: string;
  severity: 'success' | 'error' | 'warning' | 'info';
}

export default function WorkspacePage() {
  const theme = useTheme();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const periodId = id || '1';
  const { user } = useAuth();
  const canModify = canEdit(user?.role, 'workspace');

  const { data: workspace, isLoading, refetch } = useWorkspace(periodId);

  useBreadcrumbLabel(
    workspace?.period ? `${MONTH_NAMES[workspace.period.month - 1]} ${workspace.period.year}` : undefined
  );

  const { data: periodsData } = useQuery({
    queryKey: ['periods', 'list'],
    queryFn: async () => {
      const resp = await import('../../../api/client').then(m => m.apiClient.get('/periods?size=100&sort_by=id&sort_direction=desc'));
      return resp.data.data?.items || [];
    },
    staleTime: 60000,
  });

  const handleNavigatePeriod = useCallback((offset: number) => {
    if (!periodsData || periodsData.length === 0) return;
    const currentIndex = periodsData.findIndex((p: any) => String(p.id) === periodId);
    if (currentIndex === -1) return;
    const targetIndex = currentIndex - offset;
    if (targetIndex < 0 || targetIndex >= periodsData.length) return;
    navigate(`/app/periods/${periodsData[targetIndex].id}`);
  }, [periodsData, periodId, navigate]);

  const assignDoctor = useAssignDoctor(periodId);
  const swapDoctor = useSwapDoctor(periodId);
  const removeAssignment = useRemoveAssignment(periodId);
  const moveAssignment = useMoveAssignment(periodId);
  const duplicateDayMut = useDuplicateDay(periodId);
  const duplicateWeekMut = useDuplicateWeek(periodId);

  const [activeTab, setActiveTab] = useState(0);
  const [activeCell, setActiveCell] = useState<CellPosition | null>(null);
  const [cellContext, setCellContext] = useState<CellContext | null>(null);
  const [toast, setToast] = useState<ToastState>({ open: false, message: '', severity: 'success' });
  const [confirmDialog, setConfirmDialog] = useState<{ open: boolean; message: string; onConfirm: () => void } | null>(null);
  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const [clipboard, setClipboard] = useState<{ doctorId: number; doctorName: string } | null>(null);
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'error' | 'idle'>('idle');
  const [lastSaveTime, setLastSaveTime] = useState<string>('');

  const undoRedo = useUndoRedo({ onStatusChange: setSaveStatus });

  const showToast = useCallback((message: string, severity: 'success' | 'error' | 'warning' | 'info' = 'success') => {
    setToast({ open: true, message, severity });
  }, []);

  const isMutating = assignDoctor.isPending || swapDoctor.isPending || removeAssignment.isPending || moveAssignment.isPending || duplicateDayMut.isPending || duplicateWeekMut.isPending;

  const doctorStats = useMemo(() => {
    if (!workspace) return {};
    const stats: Record<number, { totalShifts: number; totalHours: number; assignedToday: number }> = {};
    workspace.doctors.forEach((d) => { stats[d.id] = { totalShifts: 0, totalHours: 0, assignedToday: 0 }; });
    workspace.days.forEach((day) => {
      SHIFT_TYPES.forEach((st) => {
        day.shifts[st].assignments.forEach((a) => {
          if (stats[a.doctor_id]) {
            stats[a.doctor_id].totalShifts += 1;
            const parts_s = a.start_time.split(':');
            const parts_e = a.end_time.split(':');
            let startMin = parseInt(parts_s[0]) * 60 + parseInt(parts_s[1]);
            let endMin = parseInt(parts_e[0]) * 60 + parseInt(parts_e[1]);
            if (endMin <= startMin) endMin += 24 * 60;
            stats[a.doctor_id].totalHours += (endMin - startMin) / 60;
          }
        });
      });
    });
    return stats;
  }, [workspace]);

  const sameDayConflicts = useMemo(() => {
    if (!workspace) return new Map<string, boolean>();
    const map = new Map<string, boolean>();
    workspace.days.forEach((day) => {
      const doctorOccurrences = new Map<number, string[]>();
      SHIFT_TYPES.forEach((st) => {
        day.shifts[st].assignments.forEach((a) => {
          const existing = doctorOccurrences.get(a.doctor_id) || [];
          existing.push(st);
          doctorOccurrences.set(a.doctor_id, existing);
        });
      });
      doctorOccurrences.forEach((types, _doctorId) => {
        if (types.length > 1) {
          types.forEach((st) => map.set(`${day.date}-${st}`, true));
        }
      });
    });
    return map;
  }, [workspace]);

  const conflicts = useMemo(() => {
    if (!workspace) return [];
    const result: Array<{ doctorName: string; date: string; shiftType: string }> = [];
    const doctorShifts = new Map<number, { date: string; shiftType: string }[]>();
    workspace.days.forEach((day) => {
      SHIFT_TYPES.forEach((st) => {
        day.shifts[st].assignments.forEach((a) => {
          const existing = doctorShifts.get(a.doctor_id) || [];
          existing.push({ date: day.date, shiftType: st });
          doctorShifts.set(a.doctor_id, existing);
        });
      });
    });
    doctorShifts.forEach((shifts, doctorId) => {
      const dateGroups = new Map<string, string[]>();
      shifts.forEach((s) => {
        const existing = dateGroups.get(s.date) || [];
        existing.push(s.shiftType);
        dateGroups.set(s.date, existing);
      });
      dateGroups.forEach((types, date) => {
        if (types.length > 1) {
          const doctor = workspace.doctors.find((d) => d.id === doctorId);
          result.push({ doctorName: doctor?.name || `Medico #${doctorId}`, date, shiftType: types.join(', ') });
        }
      });
    });
    return result;
  }, [workspace]);

  const markSaved = useCallback(() => {
    setSaveStatus('saved');
    setLastSaveTime(new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }));
  }, []);

  const handleOpenCell = useCallback((date: string, shiftType: string, shiftId: number | null, anchorEl: HTMLElement) => {
    if (!workspace) return;
    const day = workspace.days.find((d) => d.date === date);
    const cell = day?.shifts[shiftType];
    const existingIds = cell?.assignments.map((a) => a.doctor_id) || [];
    setCellContext({ date, shiftType, shiftId, anchorEl, existingAssignmentIds: existingIds });
  }, [workspace]);

  const executeAssign = useCallback(async (doctorId: number) => {
    if (!cellContext || !workspace) return;
    const prevAssignments = workspace.days.find((d) => d.date === cellContext.date)?.shifts[cellContext.shiftType]?.assignments || [];
    const prevDoctorId = prevAssignments[0]?.doctor_id;
    try {
      if (prevAssignments.length > 0) {
        await swapDoctor.mutateAsync({ assignment_id: prevAssignments[0].id, doctor_id: doctorId });
        const doctorName = workspace.doctors.find((d) => d.id === doctorId)?.name || `Medico #${doctorId}`;
        undoRedo.push(
          `Trocar para ${doctorName}`,
          async () => { await swapDoctor.mutateAsync({ assignment_id: prevAssignments[0].id, doctor_id: prevDoctorId }); refetch(); },
          async () => { await swapDoctor.mutateAsync({ assignment_id: prevAssignments[0].id, doctor_id: doctorId }); refetch(); },
        );
      } else {
        if (cellContext.shiftId == null) { showToast('Turno nao encontrado no sistema', 'error'); return; }
        const result = await assignDoctor.mutateAsync({ shift_id: cellContext.shiftId, doctor_id: doctorId, shift_type: cellContext.shiftType });
        const doctorName = workspace.doctors.find((d) => d.id === doctorId)?.name || `Medico #${doctorId}`;
        undoRedo.push(
          `Atribuir ${doctorName}`,
          async () => { await removeAssignment.mutateAsync(result.id); refetch(); },
          async () => { await assignDoctor.mutateAsync({ shift_id: cellContext.shiftId, doctor_id: doctorId, shift_type: cellContext.shiftType }); refetch(); },
        );
      }
      showToast('Medico atribuido com sucesso');
      markSaved();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || err?.message || 'Erro ao atribuir medico';
      showToast(msg, 'error');
      setSaveStatus('error');
    }
    setCellContext(null);
  }, [cellContext, workspace, assignDoctor, swapDoctor, removeAssignment, showToast, undoRedo, refetch, markSaved]);

  const handleAssign = useCallback(async (doctorId: number) => {
    if (!canModify) return;
    if (!cellContext || !workspace) return;
    const existingAssignments = workspace.days.find((d) => d.date === cellContext.date)?.shifts[cellContext.shiftType]?.assignments || [];
    if (existingAssignments.find((a) => a.doctor_id === doctorId)) {
      showToast('Medico ja escalado neste turno', 'warning');
      setCellContext(null);
      return;
    }
    const doctorOnSameDay = workspace.days.find((d) => d.date === cellContext.date)?.shifts;
    if (doctorOnSameDay) {
      for (const st of SHIFT_TYPES) {
        const cell = doctorOnSameDay[st];
        if (st !== cellContext.shiftType) {
          const conflict = cell.assignments.find((a) => a.doctor_id === doctorId);
          if (conflict) {
            const doctor = workspace.doctors.find((d) => d.id === doctorId);
            setConfirmDialog({
              open: true,
              message: `${doctor?.name || 'Medico'} ja possui plantao no turno ${st} neste dia. Deseja atribuir mesmo assim?`,
              onConfirm: async () => { setConfirmDialog(null); await executeAssign(doctorId); },
            });
            return;
          }
        }
      }
    }
    await executeAssign(doctorId);
  }, [cellContext, workspace, showToast, executeAssign]);

  const handleRemove = useCallback(async (assignmentId: number) => {
    if (!canModify) return;
    const assignment = workspace?.days.flatMap((d) => SHIFT_TYPES.map((st) => ({ ...d.shifts[st], date: d.date, shiftType: st }))).flatMap((c) => c.assignments).find((a) => a.id === assignmentId);
    try {
      await removeAssignment.mutateAsync(assignmentId);
      if (assignment) {
        undoRedo.push(
          `Remover ${assignment.doctor_name}`,
          async () => { await assignDoctor.mutateAsync({ shift_id: assignment.shift_id, doctor_id: assignment.doctor_id, shift_type: assignment.shift_type }); refetch(); },
          async () => { await removeAssignment.mutateAsync(assignmentId); refetch(); },
        );
      }
      showToast('Atribuicao removida');
      markSaved();
    } catch {
      showToast('Erro ao remover atribuicao', 'error');
      setSaveStatus('error');
    }
  }, [workspace, removeAssignment, assignDoctor, showToast, undoRedo, refetch, markSaved]);

  const handleRemoveActive = useCallback(async () => {
    if (!activeCell || !workspace) return;
    const day = workspace.days[activeCell.dayIndex];
    if (!day) return;
    const cell = day.shifts[activeCell.shiftType];
    if (cell.assignments.length > 0) {
      await handleRemove(cell.assignments[0].id);
    }
  }, [activeCell, workspace, handleRemove]);

  const handleClear = useCallback(async () => {
    if (!canModify) return;
    if (!cellContext || !workspace) return;
    const existingAssignments = workspace.days.find((d) => d.date === cellContext.date)?.shifts[cellContext.shiftType]?.assignments || [];
    try {
      for (const a of existingAssignments) { await removeAssignment.mutateAsync(a.id); }
      showToast('Turno limpo');
      markSaved();
    } catch {
      showToast('Erro ao limpar turno', 'error');
      setSaveStatus('error');
    }
    setCellContext(null);
  }, [cellContext, workspace, removeAssignment, showToast, markSaved]);

  const handleContextMenu = useCallback((e: React.MouseEvent, date: string, shiftType: string, shiftId: number | null) => {
    e.preventDefault();
    setContextMenu({ anchorEl: e.currentTarget as HTMLElement, date, shiftType, shiftId });
  }, []);

  const handleCopyDoctor = useCallback(() => {
    if (!contextMenu || !workspace) return;
    const day = workspace.days.find((d) => d.date === contextMenu.date);
    const cell = day?.shifts[contextMenu.shiftType];
    if (cell?.assignments[0]) {
      setClipboard({ doctorId: cell.assignments[0].doctor_id, doctorName: cell.assignments[0].doctor_name });
      showToast(`Copiado: ${cell.assignments[0].doctor_name}`, 'info');
    }
  }, [contextMenu, workspace, showToast]);

  const handleCopyActive = useCallback(() => {
    if (!activeCell || !workspace) return;
    const day = workspace.days[activeCell.dayIndex];
    if (!day) return;
    const cell = day.shifts[activeCell.shiftType];
    if (cell.assignments[0]) {
      setClipboard({ doctorId: cell.assignments[0].doctor_id, doctorName: cell.assignments[0].doctor_name });
      showToast(`Copiado: ${cell.assignments[0].doctor_name}`, 'info');
    }
  }, [activeCell, workspace, showToast]);

  const handlePaste = useCallback(async (targetDate?: string, targetShift?: string) => {
    if (!canModify) return;
    const date = targetDate || contextMenu?.date;
    const shift = targetShift || contextMenu?.shiftType;
    if (!date || !shift || !clipboard || !workspace) return;

    const day = workspace.days.find((d) => d.date === date);
    const cell = day?.shifts[shift];
    if (cell) {
      try {
        const existingAssignment = cell.assignments[0];
        if (existingAssignment) {
          await swapDoctor.mutateAsync({ assignment_id: existingAssignment.id, doctor_id: clipboard.doctorId });
        } else {
          if (cell.shift_id == null) { showToast('Turno nao encontrado', 'error'); return; }
          await assignDoctor.mutateAsync({ shift_id: cell.shift_id, doctor_id: clipboard.doctorId, shift_type: shift });
        }
        showToast(`Colado: ${clipboard.doctorName}`);
        markSaved();
      } catch (err: any) {
        const msg = err?.response?.data?.error?.message || 'Erro ao colar medico';
        showToast(msg, 'error');
      }
    }
    setContextMenu(null);
  }, [contextMenu, clipboard, workspace, swapDoctor, assignDoctor, showToast, markSaved]);

  const handlePasteActive = useCallback(async () => {
    if (!activeCell || !workspace || !clipboard) return;
    const day = workspace.days[activeCell.dayIndex];
    if (!day) return;
    await handlePaste(day.date, activeCell.shiftType);
  }, [activeCell, workspace, clipboard, handlePaste]);

  const handleDuplicateDay = useCallback(async () => {
    if (!canModify) return;
    if (!contextMenu || !workspace) return;
    const sourceDate = contextMenu.date;
    const nextDay = new Date(sourceDate + 'T12:00:00');
    nextDay.setDate(nextDay.getDate() + 1);
    const targetDate = nextDay.toISOString().split('T')[0];

    const hasShiftInRange = workspace.days.some((d) => d.date === targetDate);
    if (!hasShiftInRange) {
      showToast('Data de destino fora da competencia', 'warning');
      setContextMenu(null);
      return;
    }

    try {
      await duplicateDayMut.mutateAsync({ source_date: sourceDate, target_date: targetDate });
      showToast(`Dia duplicado: ${sourceDate} -> ${targetDate}`);
      markSaved();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao duplicar dia';
      showToast(msg, 'error');
    }
    setContextMenu(null);
  }, [contextMenu, workspace, duplicateDayMut, showToast, markSaved]);

  const handleDuplicateWeek = useCallback(async () => {
    if (!canModify) return;
    if (!contextMenu || !workspace) return;
    const sourceDate = new Date(contextMenu.date + 'T12:00:00');
    const dayOfWeek = sourceDate.getDay();
    const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
    const sourceMonday = new Date(sourceDate);
    sourceMonday.setDate(sourceMonday.getDate() + mondayOffset);
    const targetMonday = new Date(sourceMonday);
    targetMonday.setDate(targetMonday.getDate() + 7);

    const sourceStart = sourceMonday.toISOString().split('T')[0];
    const targetStart = targetMonday.toISOString().split('T')[0];

    try {
      await duplicateWeekMut.mutateAsync({ source_start_date: sourceStart, target_start_date: targetStart });
      showToast(`Semana duplicada: ${sourceStart} -> ${targetStart}`);
      markSaved();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao duplicar semana';
      showToast(msg, 'error');
    }
    setContextMenu(null);
  }, [contextMenu, workspace, duplicateWeekMut, showToast, markSaved]);

  const handleDrop = useCallback(async (sourceAssignmentId: number, _sourceDoctorId: number, targetDate: string, targetShiftType: string, targetShiftId: number | null) => {
    if (!canModify) return;
    if (!workspace) return;
    const assignment = workspace.days.flatMap((d) => SHIFT_TYPES.map((st) => ({ ...d.shifts[st], date: d.date, shiftType: st }))).flatMap((c) => c.assignments).find((a) => a.id === sourceAssignmentId);
    if (!assignment) return;

    if (assignment.date === targetDate && assignment.shiftType === targetShiftType) return;

    const targetDay = workspace.days.find((d) => d.date === targetDate);
    const targetCell = targetDay?.shifts[targetShiftType];
    if (targetCell?.assignments.length) {
      showToast('Turno destino ja possui medico', 'warning');
      return;
    }

    try {
      await moveAssignment.mutateAsync({
        assignment_id: sourceAssignmentId,
        target_shift_id: targetShiftId,
        start_time: SHIFT_TIMES[targetShiftType]?.start,
        end_time: SHIFT_TIMES[targetShiftType]?.end,
      });
      showToast('Medico movido com sucesso');
      markSaved();
    } catch (err: any) {
      const msg = err?.response?.data?.error?.message || 'Erro ao mover medico';
      showToast(msg, 'error');
    }
  }, [workspace, moveAssignment, showToast, markSaved]);

  const handlePeriodAction = useCallback(async (action: 'close' | 'reopen' | 'duplicate' | 'delete' | 'copy-from') => {
    if (!canModify) return;
    try {
      if (action === 'close') {
        await fetch(`/api/v1/periods/${periodId}/close`, { method: 'POST' });
        showToast('Competencia fechada com sucesso');
      } else if (action === 'reopen') {
        await fetch(`/api/v1/periods/${periodId}/reopen`, { method: 'POST' });
        showToast('Competencia reaberta com sucesso');
      } else if (action === 'duplicate') {
        const resp = await fetch(`/api/v1/periods/${periodId}/duplicate`, { method: 'POST' });
        const result = await resp.json();
        if (result.success !== false) {
          showToast('Competencia duplicada com sucesso');
          navigate(`/app/periods/${result.data?.id || periodId}`);
        } else {
          showToast(result.error?.message || 'Erro ao duplicar', 'error');
        }
      } else if (action === 'delete') {
        await fetch(`/api/v1/periods/${periodId}`, { method: 'DELETE' });
        showToast('Competencia excluida');
        navigate('/app/periods');
      } else if (action === 'copy-from') {
        const resp = await fetch(`/api/v1/periods`);
        const periodsData = await resp.json();
        const periods = periodsData.data?.items || [];
        const sorted = periods.sort((a: any, b: any) => {
          if (a.year !== b.year) return b.year - a.year;
          return b.month - a.month;
        });
        const prevPeriod = sorted.find((p: any) => p.id !== parseInt(periodId));
        if (!prevPeriod) {
          showToast('Nenhum periodo anterior encontrado', 'warning');
          return;
        }
        await fetch(`/api/v1/periods/${periodId}/copy-from/${prevPeriod.id}`, { method: 'POST' });
        showToast('Dados copiados do periodo anterior');
      }
      refetch();
    } catch (err: any) {
      const msg = err?.message || 'Erro ao executar acao';
      showToast(msg, 'error');
    }
  }, [periodId, refetch, showToast, navigate]);

  const { gridRef } = useWorkspaceKeyboard({
    days: workspace?.days || [],
    activeCell,
    setActiveCell,
    onOpenCell: handleOpenCell,
    onRemoveActive: handleRemoveActive,
    onCopy: handleCopyActive,
    onPaste: handlePasteActive,
    isPopoverOpen: !!cellContext,
    onClosePopover: () => setCellContext(null),
    onUndo: undoRedo.undo,
    onRedo: undoRedo.redo,
  });

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <Box sx={{ height: 48, mb: 2 }}><CircularProgress size={20} /></Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            {Array.from({ length: 5 }).map((_, i) => (
              <Box key={i} sx={{ height: 44, mb: 0.5, bgcolor: theme.palette.action.hover, borderRadius: 1 }} />
            ))}
          </Box>
          <Box sx={{ width: 240 }}>
            {Array.from({ length: 4 }).map((_, i) => (
              <Box key={i} sx={{ height: 60, mb: 1, bgcolor: theme.palette.action.hover, borderRadius: 1 }} />
            ))}
          </Box>
        </Box>
      </Box>
    );
  }

  if (!workspace) {
    return (
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="60vh" gap={2}>
        <Typography variant="h6" color="text.secondary">Competencia nao encontrada</Typography>
        <Typography variant="body2" color="text.secondary">Verifique se o ID da competencia e valido.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 120px)' }}>
      <WorkspaceHeader
        period={workspace.period}
        summary={workspace.summary}
        onNavigate={handleNavigatePeriod}
        onRefresh={() => refetch()}
        onPeriodAction={handlePeriodAction}
        canModify={canModify}
      />
      <WorkspaceTabs activeTab={activeTab} onTabChange={setActiveTab} />

      {activeTab === 0 && (
        <Box sx={{ display: 'flex', gap: 2, flex: 1, overflow: 'hidden' }}>
          <Box sx={{ flex: 1, overflow: 'auto' }}>
            <AssignmentGrid ref={gridRef} days={workspace.days} activeCell={activeCell} onOpenCell={handleOpenCell} onRemove={handleRemove} onContextMenu={handleContextMenu} onDrop={handleDrop} sameDayConflicts={sameDayConflicts} />
          </Box>
          <CoverageSidebar summary={workspace.summary} conflicts={conflicts} pastActions={undoRedo.pastActions} futureActions={undoRedo.futureActions} onUndoAction={undoRedo.undo} onRedoAction={undoRedo.redo} saveStatus={saveStatus} lastSaveTime={lastSaveTime} />
        </Box>
      )}
      {activeTab === 1 && <SummaryTab summary={workspace.summary} days={workspace.days} doctors={workspace.doctors} />}
      {activeTab === 2 && <DoctorsTab doctors={workspace.doctors} doctorStats={doctorStats} periodId={periodId} onRefresh={() => refetch()} />}
      {activeTab === 3 && <ShiftManagementTab period={workspace.period} onShiftCreated={() => refetch()} onShiftUpdated={() => refetch()} onShiftDeleted={() => refetch()} canModify={canModify} />}
      {activeTab === 4 && <FinancialTab days={workspace.days} doctors={workspace.doctors} />}
      {activeTab === 5 && <ReportsTab period={workspace.period} summary={workspace.summary} days={workspace.days} doctors={workspace.doctors} />}

      <QuickAssignPopover open={!!cellContext} anchorEl={cellContext?.anchorEl || null} doctors={workspace.doctors} assignedDoctorIds={cellContext?.existingAssignmentIds || []} doctorStats={doctorStats} onSelect={handleAssign} onClear={handleClear} onClose={() => setCellContext(null)} isLoading={isMutating} />
      <CellContextMenu open={!!contextMenu} anchorEl={contextMenu?.anchorEl || null} onClose={() => setContextMenu(null)} onCopyDoctor={handleCopyDoctor} onPaste={() => handlePaste()} onClearCell={handleClear} onDuplicateDay={handleDuplicateDay} onDuplicateWeek={handleDuplicateWeek} hasClipboardData={!!clipboard} hasAssignments={!!contextMenu && (() => { const day = workspace.days.find((d) => d.date === contextMenu.date); return (day?.shifts[contextMenu.shiftType]?.assignments.length || 0) > 0; })()} canModify={canModify} />

      <Snackbar open={toast.open} autoHideDuration={3000} onClose={() => setToast((prev) => ({ ...prev, open: false }))} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert onClose={() => setToast((prev) => ({ ...prev, open: false }))} severity={toast.severity} variant="filled" sx={{ width: '100%' }}>{toast.message}</Alert>
      </Snackbar>

      {confirmDialog && (
        <Box sx={{ position: 'fixed', inset: 0, bgcolor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1300 }} onClick={() => setConfirmDialog(null)}>
          <Box sx={{ bgcolor: theme.palette.background.paper, borderRadius: 2, p: 3, maxWidth: 400, width: '90%' }} onClick={(e) => e.stopPropagation()}>
            <Typography variant="body1" mb={2}>{confirmDialog.message}</Typography>
            <Box display="flex" justifyContent="flex-end" gap={1}>
              <Box onClick={() => setConfirmDialog(null)} sx={{ px: 2, py: 1, borderRadius: 1, cursor: 'pointer', bgcolor: theme.palette.action.hover, fontSize: '0.875rem', fontWeight: 500 }}>Cancelar</Box>
              <Box onClick={confirmDialog.onConfirm} sx={{ px: 2, py: 1, borderRadius: 1, cursor: 'pointer', bgcolor: theme.palette.primary.main, color: theme.palette.primary.contrastText, fontSize: '0.875rem', fontWeight: 500 }}>Confirmar</Box>
            </Box>
          </Box>
        </Box>
      )}
    </Box>
  );
}
