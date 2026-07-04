export interface PeriodData {
  id: number;
  year: number;
  month: number;
  status: 'draft' | 'closed' | 'paid';
  created_at: string;
  updated_at: string;
}

export interface PeriodListParams {
  page?: number;
  size?: number;
  year?: number;
  month?: number;
  status?: string;
  sort_by?: string;
  sort_direction?: 'asc' | 'desc';
}

export interface CreatePeriodData {
  year: number;
  month: number;
}

export interface UpdatePeriodData {
  year?: number;
  month?: number;
}

export const MONTH_NAMES = [
  'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
];

export const STATUS_LABELS: Record<string, string> = {
  draft: 'Rascunho',
  closed: 'Fechado',
  paid: 'Pago',
};
