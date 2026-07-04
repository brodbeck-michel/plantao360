export interface AssignmentData {
  id: number;
  shift_id: number;
  shift_type: string;
  doctor_id: number;
  doctor_name: string;
  start_time: string;
  end_time: string;
  status: string;
}

export interface ShiftCellData {
  shift_id: number | null;
  shift_type: string;
  assignments: AssignmentData[];
}

export interface DayData {
  date: string;
  day_of_week: string;
  shifts: Record<string, ShiftCellData>;
}

export interface DoctorOption {
  id: number;
  name: string;
  crm: string;
  hour_rate: number;
  specialty: string;
  active: boolean;
}

export interface WorkspaceSummary {
  total_shifts: number;
  filled_shifts: number;
  coverage_rate: number;
  total_doctors: number;
  total_hours: number;
}

export interface PeriodInfo {
  id: number;
  year: number;
  month: number;
  status: string;
  start_date: string;
  end_date: string;
}

export interface WorkspaceData {
  period: PeriodInfo;
  days: DayData[];
  doctors: DoctorOption[];
  summary: WorkspaceSummary;
}

export const SHIFT_TYPES = ['T1', 'T2', 'T3', 'R1', 'R2'] as const;

export const SHIFT_LABELS: Record<string, string> = {
  T1: 'T1 TITULAR MANHÃ',
  T2: 'T2 TITULAR TARDE',
  T3: 'T3 TITULAR NOITE',
  R1: 'R1 REFORÇO MANHÃ',
  R2: 'R2 REFORÇO TARDE',
};

export const SHIFT_TIMES: Record<string, { start: string; end: string; hours: number }> = {
  T1: { start: '07:00', end: '12:59', hours: 6 },
  T2: { start: '13:00', end: '18:59', hours: 6 },
  T3: { start: '19:00', end: '06:59', hours: 12 },
  R1: { start: '09:00', end: '14:59', hours: 6 },
  R2: { start: '15:00', end: '21:00', hours: 6 },
};

export const MONTH_NAMES = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
];

export function getCompetencyLabel(year: number, month: number): string {
  const nextMonth = month === 12 ? 1 : month + 1;
  const nextYear = month === 12 ? year + 1 : year;
  return `26/${String(month).padStart(2, '0')}/${year} – 25/${String(nextMonth).padStart(2, '0')}/${nextYear}`;
}

export function formatHours(hours: number): string {
  return `${Math.floor(hours)}h${hours % 1 > 0 ? ` ${Math.round((hours % 1) * 60)}min` : ''}`;
}
