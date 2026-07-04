/**
 * Entity Icons — Plantão 360
 *
 * Centralized MUI icon mapping per entity, event type, and action.
 * Single source of truth for all modules.
 *
 * Sprint: 14 — Operational MVP
 */

import {
  // Entity icons
  LocalHospital,
  CalendarMonth,
  EventNote,
  PersonAdd,
  HealthAndSafety,
  AddCircle,
  Receipt,
  People,
  Dashboard,
  Timeline,
  Description,
  Insights,
  Assignment,
  AttachMoney,
  // Status icons
  Warning,
  CheckCircle,
  Error,
  Info,
  Schedule,
  Cancel,
  // Action icons
  Edit,
  Delete,
  Search,
  FilterList,
  Refresh,
  Settings,
  Notifications,
  Save,
  Close,
  OpenInNew,
  ContentCopy,
  Archive,
  Unarchive,
  Download,
  Upload,
  Print,
  Share,
  CloudDownload,
  CloudUpload,
  // Trend icons
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  // Navigation icons
  Menu,
  ChevronLeft,
  ChevronRight,
  ExpandMore,
  ExpandLess,
  ArrowBack,
  ArrowForward,
  Help,
  HelpOutline,
  LightMode,
  DarkMode,
  Brightness6,
  Logout,
  Person,
  AccountCircle,
} from '@mui/icons-material';

// ============================================================
// Entity Icons
// ============================================================

export const ENTITY_ICONS = {
  doctor: LocalHospital,
  period: CalendarMonth,
  shift: EventNote,
  assignment: PersonAdd,
  extra: AddCircle,
  coverage: HealthAndSafety,
  payroll: Receipt,
  dashboard: Dashboard,
  timeline: Timeline,
  report: Description,
  analytics: Insights,
  people: People,
  notification: Notifications,
  settings: Settings,
  assignment_alt: Assignment,
  financial: AttachMoney,
} as const;

// ============================================================
// Event Type Icons
// ============================================================

export const EVENT_ICONS = {
  create: CheckCircle,
  update: Edit,
  delete: Delete,
  status: Info,
  system: Settings,
  warning: Warning,
  error: Error,
  success: CheckCircle,
  info: Info,
  schedule: Schedule,
  cancel: Cancel,
  search: Search,
  filter: FilterList,
  refresh: Refresh,
} as const;

// ============================================================
// Event Type Colors
// ============================================================

export const EVENT_COLORS = {
  create: 'success',
  update: 'info',
  delete: 'error',
  status: 'warning',
  system: 'grey',
  warning: 'warning',
  error: 'error',
  success: 'success',
  info: 'info',
  schedule: 'info',
  cancel: 'error',
} as const;

// ============================================================
// Action Icons — CRUD + Operations
// ============================================================

export const ACTION_ICONS = {
  create: AddCircle,
  edit: Edit,
  delete: Delete,
  save: Save,
  cancel: Cancel,
  close: Close,
  refresh: Refresh,
  search: Search,
  filter: FilterList,
  open: OpenInNew,
  copy: ContentCopy,
  archive: Archive,
  unarchive: Unarchive,
  download: Download,
  upload: Upload,
  print: Print,
  share: Share,
  cloud_download: CloudDownload,
  cloud_upload: CloudUpload,
  export: Download,
  import: Upload,
} as const;

// ============================================================
// Trend Icons
// ============================================================

export const TREND_ICONS = {
  up: TrendingUp,
  down: TrendingDown,
  flat: TrendingFlat,
} as const;

// ============================================================
// Navigation Icons
// ============================================================

export const NAV_ICONS = {
  menu: Menu,
  chevron_left: ChevronLeft,
  chevron_right: ChevronRight,
  expand_more: ExpandMore,
  expand_less: ExpandLess,
  arrow_back: ArrowBack,
  arrow_forward: ArrowForward,
  help: Help,
  help_outline: HelpOutline,
  light_mode: LightMode,
  dark_mode: DarkMode,
  brightness: Brightness6,
  logout: Logout,
  person: Person,
  account: AccountCircle,
} as const;

// ============================================================
// Combined Export
// ============================================================

export const ALL_ICONS = {
  ...ENTITY_ICONS,
  ...EVENT_ICONS,
  ...ACTION_ICONS,
  ...TREND_ICONS,
  ...NAV_ICONS,
} as const;
