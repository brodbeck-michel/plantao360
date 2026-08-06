export interface FeatureAccentColors {
  violet: { main: string; bg: string };
  amber: { main: string; bg: string };
}

export function getFeatureAccentColors(mode: 'light' | 'dark'): FeatureAccentColors {
  if (mode === 'dark') {
    return {
      violet: { main: '#A78BFA', bg: 'rgba(167,139,250,0.16)' },
      amber: { main: '#FBBF24', bg: 'rgba(251,191,36,0.16)' },
    };
  }
  return {
    violet: { main: '#7C3AED', bg: '#F5F3FF' },
    amber: { main: '#B45309', bg: '#FFFBEB' },
  };
}
