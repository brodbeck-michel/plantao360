/**
 * Config — Plantão 360
 *
 * Barrel export for configuration.
 *
 * Sprint: 14 — Operational MVP
 */

export { FEATURE_FLAGS, isFeatureEnabled, getEnabledFlags, getDisabledFlags } from './feature-flags';
export type { FeatureFlag } from './feature-flags';
export { featureFlags } from './feature-flag-service';
export type { IFeatureFlagService } from './feature-flag-service';
