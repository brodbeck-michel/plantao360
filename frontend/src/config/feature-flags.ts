/**
 * Feature Flags — Plantão 360
 *
 * Centralized feature flag configuration.
 * Flags are read from environment variables (VITE_*) at build time.
 *
 * Sprint: 14 — Operational MVP
 */

// ============================================================
// Feature Flags
// ============================================================

export const FEATURE_FLAGS = {
  /** MVP Mode: hides non-homologated modules from sidebar menu */
  MVP_MODE: import.meta.env.VITE_MVP_MODE !== 'false',

  /** Demo mode: uses mock data instead of real API */
  DEMO_MODE: import.meta.env.VITE_DEMO_MODE === 'true',

  /** Mock API: intercepts API calls and returns mock data */
  MOCK_API: import.meta.env.VITE_MOCK_API === 'true',

  /** Real API: connects to backend (default: true) */
  REAL_API: import.meta.env.VITE_REAL_API !== 'false',

  /** Show debug panel with query cache, feature flags, etc. */
  SHOW_DEBUG_PANEL: import.meta.env.VITE_SHOW_DEBUG_PANEL === 'true',

  /** Enable experimental UI components */
  ENABLE_EXPERIMENTAL_UI: import.meta.env.VITE_ENABLE_EXPERIMENTAL_UI === 'true',

  /** Timeline feature (enabled by default) */
  TIMELINE: import.meta.env.VITE_TIMELINE !== 'false',

  /** Health Cards on dashboard */
  HEALTH_CARDS: import.meta.env.VITE_HEALTH_CARDS !== 'false',

  /** Drag and drop for assignments (not yet implemented) */
  DRAG_AND_DROP: import.meta.env.VITE_DRAG_AND_DROP === 'true',

  /** PDF export (not yet implemented) */
  EXPORT_PDF: import.meta.env.VITE_EXPORT_PDF === 'true',

  /** Push notifications (not yet implemented) */
  NOTIFICATIONS: import.meta.env.VITE_NOTIFICATIONS === 'true',
} as const;

// ============================================================
// Types
// ============================================================

export type FeatureFlag = keyof typeof FEATURE_FLAGS;

// ============================================================
// Helpers
// ============================================================

/**
 * Check if a feature flag is enabled.
 * @param flag - The feature flag name
 * @returns boolean
 */
export function isFeatureEnabled(flag: FeatureFlag): boolean {
  return FEATURE_FLAGS[flag] === true;
}

/**
 * Get all enabled feature flags.
 * @returns Array of enabled flag names
 */
export function getEnabledFlags(): FeatureFlag[] {
  return Object.entries(FEATURE_FLAGS)
    .filter(([, value]) => value === true)
    .map(([key]) => key as FeatureFlag);
}

/**
 * Get all disabled feature flags.
 * @returns Array of disabled flag names
 */
export function getDisabledFlags(): FeatureFlag[] {
  return Object.entries(FEATURE_FLAGS)
    .filter(([, value]) => value === false)
    .map(([key]) => key as FeatureFlag);
}
