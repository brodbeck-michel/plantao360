/**
 * Doctor Feature Index — Plantão 360
 *
 * Barrel do módulo de Médicos (Golden Frontend Module).
 * Sprint: 13 — Golden Frontend Module
 */

// ============================================================
// Components (reutilizáveis)
// ============================================================
export { DoctorAvatar } from './components/doctor-avatar';
export { DoctorCard } from './components/doctor-card';
export { DoctorHeader } from './components/doctor-header';
export { DoctorToolbar } from './components/doctor-toolbar';

// ============================================================
// Tables (reutilizáveis)
// ============================================================
export { DoctorTable } from './tables/doctor-table';

// ============================================================
// Filters (reutilizáveis)
// ============================================================
export { DoctorFilterBar } from './filters/doctor-filter-bar';

// ============================================================
// Forms
// ============================================================
export { DoctorForm } from './forms/doctor-form';

// ============================================================
// Details
// ============================================================
export { DoctorDetailsPanel } from './details/doctor-details-panel';

// ============================================================
// History
// ============================================================
export { DoctorHistoryTimeline } from './history/doctor-history-timeline';

// ============================================================
// Audit
// ============================================================
export { DoctorAuditCard } from './audit/doctor-audit-card';

// ============================================================
// Dialogs
// ============================================================
export { DoctorCreateDialog } from './dialogs/doctor-create-dialog';
export { DoctorEditDialog } from './dialogs/doctor-edit-dialog';
export { DoctorDeleteDialog } from './dialogs/doctor-delete-dialog';
export { DoctorDeactivateDialog } from './dialogs/doctor-deactivate-dialog';

// ============================================================
// Pages
// ============================================================
export { DoctorListPage } from './pages/doctor-list-page';
export { DoctorDetailPage } from './pages/doctor-detail-page';
export { DoctorHistoryPage } from './pages/doctor-history-page';
export { DoctorAuditPage } from './pages/doctor-audit-page';
export { DoctorProfileDrawer } from './pages/doctor-profile-drawer';

// ============================================================
// Hooks
// ============================================================
export {
  useDoctorList,
  useDoctorDetail,
  useDoctorSummary,
  useCreateDoctor,
  useUpdateDoctor,
  useDeleteDoctor,
  useDoctorFilters,
  useDoctorSearch,
  useDoctorSort,
  useDoctorPagination,
  useDoctorSelection,
} from './hooks/use-doctors';

// ============================================================
// Services
// ============================================================
export {
  doctorQueries,
  doctorMutations,
  fetchDoctors,
  fetchDoctor,
  createDoctor,
  updateDoctor,
  deleteDoctor,
  deactivateDoctor,
  fetchDoctorHistory,
  fetchDoctorAudit,
} from './services/doctor-api';
export type { DoctorListParams, CreateDoctorData, UpdateDoctorData, DoctorHistory } from './services/doctor-api';

// ============================================================
// Types
// ============================================================
export type {
  Doctor,
  DoctorSummary,
  AuditEntry,
  DoctorFilters,
  DoctorListSort,
  DoctorListState,
  DoctorFormState,
  DoctorAuditEntry,
  DoctorDialogState,
  DoctorDetailTab,
} from './types/doctor-types';
