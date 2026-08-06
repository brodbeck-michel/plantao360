export interface HourRateResult {
  tier: string;
  rate: number;
}

const BRACKETS: Array<[number, string]> = [
  [2, '1'],
  [5, '2'],
  [8, '3'],
  [10, '4'],
];

const RATES: Record<string, number> = {
  'M-1': 141.00, 'M-2': 146.88, 'M-3': 152.76, 'M-4': 158.63, 'M-5': 164.51,
  'E-1': 152.76, 'E-2': 158.63, 'E-3': 164.51, 'E-4': 170.38, 'E-5': 176.26,
};

function yearsOfCareer(careerStartDate: string, referenceDate: Date): number {
  const start = new Date(careerStartDate + 'T00:00:00');
  const diffMs = referenceDate.getTime() - start.getTime();
  return diffMs / (1000 * 60 * 60 * 24 * 365.25);
}

export function computeHourRate(hasRqe: boolean, careerStartDate: string | null | undefined, referenceDate: Date = new Date()): HourRateResult {
  const prefix = hasRqe ? 'E' : 'M';

  if (!careerStartDate) {
    const tier = `${prefix}-1`;
    return { tier, rate: RATES[tier] };
  }

  const years = yearsOfCareer(careerStartDate, referenceDate);
  let suffix = '5';
  for (const [limit, bracketSuffix] of BRACKETS) {
    if (years <= limit) {
      suffix = bracketSuffix;
      break;
    }
  }

  const tier = `${prefix}-${suffix}`;
  return { tier, rate: RATES[tier] };
}
