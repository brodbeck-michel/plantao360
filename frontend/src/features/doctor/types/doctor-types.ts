import type { Doctor, DoctorSummary, AuditEntry } from '../../../types';

export type { Doctor, DoctorSummary, AuditEntry };

export interface DoctorFilters {
  name?: string;
  crm?: string;
  specialty?: string;
  active?: boolean;
}

export interface DoctorListSort {
  field: 'name' | 'crm' | 'specialty' | 'created_at';
  direction: 'asc' | 'desc';
}

export interface DoctorListState {
  filters: DoctorFilters;
  sort: DoctorListSort;
  page: number;
  pageSize: number;
}

export interface DoctorFormState {
  name: string;
  crm: string;
  specialty: string;
  email: string;
  phone: string;
  doctor_type: string;
  hour_rate: number;
}

export interface DoctorHistory {
  id: string;
  doctor_id: string;
  event_type: 'created' | 'updated' | 'deactivated' | 'activated' | 'deleted';
  description: string;
  user?: string;
  created_at: string;
}

export interface DoctorAuditEntry {
  id: string;
  field: string;
  old_value: string | null;
  new_value: string | null;
  changed_by: string;
  changed_at: string;
}

export interface DoctorDialogState {
  create: boolean;
  edit: boolean;
  delete: boolean;
  deactivate: boolean;
  selectedDoctor: Doctor | null;
}

export type DoctorDetailTab = 'details' | 'history' | 'audit';
