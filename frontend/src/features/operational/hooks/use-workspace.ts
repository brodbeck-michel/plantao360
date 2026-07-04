import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '../../../services/query-keys';
import { fetchWorkspace, createAssignment, updateAssignment, deleteAssignment, moveAssignment, duplicateDay, duplicateWeek } from '../services/operational-api';
import { SHIFT_TIMES } from '../types/operational-types';

export function useWorkspace(periodId: string | undefined) {
  return useQuery({
    queryKey: queryKeys.periods.detail(periodId || ''),
    queryFn: () => fetchWorkspace(periodId!),
    enabled: !!periodId,
    staleTime: 0,
  });
}

export function useAssignDoctor(periodId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { shift_id: number; doctor_id: number; shift_type: string }) => {
      const times = SHIFT_TIMES[data.shift_type];
      return createAssignment({
        shift_id: data.shift_id,
        doctor_id: data.doctor_id,
        start_time: times.start,
        end_time: times.end,
      });
    },
    onSuccess: () => {
      if (periodId) {
        queryClient.invalidateQueries({ queryKey: queryKeys.periods.detail(periodId) });
      }
    },
  });
}

export function useSwapDoctor(periodId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { assignment_id: number; doctor_id: number }) =>
      updateAssignment(data.assignment_id, { doctor_id: data.doctor_id }),
    onSuccess: () => {
      if (periodId) {
        queryClient.invalidateQueries({ queryKey: queryKeys.periods.detail(periodId) });
      }
    },
  });
}

export function useRemoveAssignment(periodId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (assignmentId: number) => deleteAssignment(assignmentId),
    onSuccess: () => {
      if (periodId) {
        queryClient.invalidateQueries({ queryKey: queryKeys.periods.detail(periodId) });
      }
    },
  });
}

export function useMoveAssignment(periodId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { assignment_id: number; target_shift_id: number; start_time?: string; end_time?: string }) =>
      moveAssignment(data.assignment_id, { target_shift_id: data.target_shift_id, start_time: data.start_time, end_time: data.end_time }),
    onSuccess: () => {
      if (periodId) {
        queryClient.invalidateQueries({ queryKey: queryKeys.periods.detail(periodId) });
      }
    },
  });
}

export function useDuplicateDay(periodId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { source_date: string; target_date: string }) =>
      duplicateDay({ source_date: data.source_date, target_date: data.target_date, period_id: parseInt(periodId || '0') }),
    onSuccess: () => {
      if (periodId) {
        queryClient.invalidateQueries({ queryKey: queryKeys.periods.detail(periodId) });
      }
    },
  });
}

export function useDuplicateWeek(periodId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { source_start_date: string; target_start_date: string }) =>
      duplicateWeek({ source_start_date: data.source_start_date, target_start_date: data.target_start_date, period_id: parseInt(periodId || '0') }),
    onSuccess: () => {
      if (periodId) {
        queryClient.invalidateQueries({ queryKey: queryKeys.periods.detail(periodId) });
      }
    },
  });
}
