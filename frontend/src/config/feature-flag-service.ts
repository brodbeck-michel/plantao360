/**
 * FeatureFlagService — Plantão 360
 *
 * Encapsulates feature flag access behind a service interface.
 * Components depend on this service, not on the underlying implementation.
 *
 * Sprint: 14 — Operational MVP
 */

import { FEATURE_FLAGS, type FeatureFlag } from './feature-flags';

// ============================================================
// Service Interface
// ============================================================

export interface IFeatureFlagService {
  isEnabled(flag: FeatureFlag): boolean;
  getEnabled(): FeatureFlag[];
  getDisabled(): FeatureFlag[];
  getAll(): Record<FeatureFlag, boolean>;
}

// ============================================================
// Service Implementation
// ============================================================

class FeatureFlagServiceImpl implements IFeatureFlagService {
  /**
   * Check if a feature flag is enabled.
   * @param flag - The feature flag name
   * @returns boolean
   */
  isEnabled(flag: FeatureFlag): boolean {
    return FEATURE_FLAGS[flag] === true;
  }

  /**
   * Get all enabled feature flags.
   * @returns Array of enabled flag names
   */
  getEnabled(): FeatureFlag[] {
    return Object.entries(FEATURE_FLAGS)
      .filter(([, value]) => value === true)
      .map(([key]) => key as FeatureFlag);
  }

  /**
   * Get all disabled feature flags.
   * @returns Array of disabled flag names
   */
  getDisabled(): FeatureFlag[] {
    return Object.entries(FEATURE_FLAGS)
      .filter(([, value]) => value === false)
      .map(([key]) => key as FeatureFlag);
  }

  /**
   * Get all feature flags with their values.
   * @returns Record of flag names to boolean values
   */
  getAll(): Record<FeatureFlag, boolean> {
    return { ...FEATURE_FLAGS };
  }
}

// ============================================================
// Singleton Export
// ============================================================

/**
 * Feature flag service instance.
 *
 * Usage:
 * ```tsx
 * import { featureFlags } from '@/config';
 *
 * if (featureFlags.isEnabled('DEMO_MODE')) {
 *   // Use mock data
 * }
 * ```
 */
export const featureFlags: IFeatureFlagService = new FeatureFlagServiceImpl();

// ============================================================
// React Hook
// ============================================================

/**
 * React hook for accessing the feature flag service.
 *
 * Usage:
 * ```tsx
 * const featureFlags = useFeatureFlagService();
 * if (featureFlags.isEnabled('DEMO_MODE')) {
 *   // Use mock data
 * }
 * ```
 */
export function useFeatureFlagService(): IFeatureFlagService {
  return featureFlags;
}
