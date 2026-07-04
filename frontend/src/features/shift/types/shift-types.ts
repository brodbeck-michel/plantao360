export interface ShiftData {
  id: number;
  period_id: number;
  shift_date: string;
  shift_type: string;
  status: string;
  scheduled_start: string | null;
  scheduled_end: string | null;
  total_duration_minutes: number | null;
  doctor_count: number | null;
  created_at: string;
  updated_at: string;
}

export interface ShiftListParams {
  page?: number;
  size?: number;
  period_id?: number;
  shift_type?: string;
  status?: string;
  sort_by?: string;
  sort_direction?: 'asc' | 'desc';
}

export interface CreateShiftData {
  period_id: number;
  shift_date: string;
  shift_type: string;
  scheduled_start?: string;
  scheduled_end?: string;
  total_duration_minutes?: number;
  doctor_count?: number;
}

export interface UpdateShiftData {
  shift_date?: string;
  shift_type?: string;
  status?: string;
  scheduled_start?: string;
  scheduled_end?: string;
  total_duration_minutes?: number;
  doctor_count?: number;
}

export const SHIFT_TYPES = ['T1', 'T2', 'T3', 'R1', 'R2'] as const;
export type ShiftType = typeof SHIFT_TYPES[number];

export const SHIFT_LABELS: Record<string, string> = {
  T1: 'T1 TITULAR MANHA',
  T2: 'T2 TITULAR TARDE',
  T3: 'T3 TITULAR NOITE',
  R1: 'R1 REFORCO MANHA',
  R2: 'R2 REFORCO TARDE',
};

export const SHIFT_TIMES: Record<string, { start: string; end: string; hours: number }> = {
  T1: { start: '07:00', end: '19:00', hours: 12 },
  T2: { start: '19:00', end: '07:00', hours: 12 },
  T3: { start: '19:00', end: '07:00', hours: 12 },
  R1: { start: '07:00', end: '13:00', hours: 6 },
  R2: { start: '13:00', end: '19:00', hours: 6 },
};
