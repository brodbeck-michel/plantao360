export interface ApiError {
  code: string;
  message: string;
  status?: number;
  details?: unknown;
  requestId?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface Doctor {
  id: string;
  name: string;
  crm: string;
  specialty: string;
  phone?: string;
  email?: string;
  doctor_type: string;
  hour_rate: number;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DoctorSummary {
  doctor_id: string;
  name: string;
  specialty: string;
  total_shifts: number;
  total_assignments: number;
  total_hours: number;
}

export interface Period {
  id: string;
  name: string;
  year: number;
  month: number;
  start_date: string;
  end_date: string;
  status: 'draft' | 'closed' | 'paid';
  created_at: string;
  updated_at: string;
}

export interface PeriodSummary {
  period_id: string;
  name: string;
  status: string;
  total_shifts: number;
  total_doctors: number;
  total_hours: number;
}

export interface Shift {
  id: string;
  period_id: string;
  doctor_id: string;
  shift_date: string;
  shift_type: string;
  start_time: string;
  end_time: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface ShiftSummary {
  shift_id: string;
  period_id: string;
  doctor_id: string;
  doctor_name: string;
  shift_date: string;
  shift_type: string;
  status: string;
  coverage_status?: string;
}

export interface Assignment {
  id: string;
  shift_id: string;
  doctor_id: string;
  assignment_type: string;
  status: 'planned' | 'confirmed' | 'started' | 'completed' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface AssignmentSummary {
  assignment_id: string;
  shift_id: string;
  doctor_id: string;
  doctor_name: string;
  assignment_type: string;
  status: string;
  created_at: string;
}

export interface Extra {
  id: string;
  shift_id: string;
  doctor_id: string;
  extra_type: string;
  duration_minutes: number;
  justification: string;
  status: 'pending' | 'approved' | 'rejected' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface Coverage {
  id: string;
  shift_id: string;
  coverage_type: string;
  status: 'pending' | 'approved' | 'rejected';
  requested_at: string;
  resolved_at?: string;
  resolved_by?: string;
}

export interface Payroll {
  id: string;
  competency: string;
  period_id: string;
  status: 'draft' | 'calculated' | 'reviewed' | 'approved' | 'exported' | 'paid' | 'archived';
  total_doctors: number;
  total_amount: number;
  created_at: string;
  updated_at: string;
  approved_at?: string;
  completed_at?: string;
}

export type DoctorStatus = 'active' | 'inactive';
export type PeriodStatus = 'draft' | 'closed' | 'paid';
export type ShiftStatus = 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
export type AssignmentStatus = 'planned' | 'confirmed' | 'started' | 'completed' | 'cancelled';
export type ExtraStatus = 'pending' | 'approved' | 'rejected' | 'cancelled';
export type CoverageStatus = 'pending' | 'approved' | 'rejected';
export type PayrollStatus = 'draft' | 'calculated' | 'reviewed' | 'approved' | 'exported' | 'paid' | 'archived';

export interface AuditEntry {
  id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  field?: string;
  old_value?: string | null;
  new_value?: string | null;
  changed_by: string;
  changed_at: string;
  metadata?: Record<string, unknown>;
}

export type Persona = 'coordenador' | 'medico' | 'financeiro' | 'rh' | 'auditor' | 'administrador' | 'diretor';

export interface UserPermissions {
  persona: Persona;
  canCreate: boolean;
  canRead: boolean;
  canUpdate: boolean;
  canDelete: boolean;
  canApprove: boolean;
  canExport: boolean;
}
