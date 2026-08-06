from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HourRateResult:
    tier: str
    rate: float


# (limite superior de anos de carreira, indice da faixa 0-4) -> sufixo do tier e valor
_BRACKETS = [
    (2, "1"),
    (5, "2"),
    (8, "3"),
    (10, "4"),
]

_RATES = {
    "M-1": 141.00, "M-2": 146.88, "M-3": 152.76, "M-4": 158.63, "M-5": 164.51,
    "E-1": 152.76, "E-2": 158.63, "E-3": 164.51, "E-4": 170.38, "E-5": 176.26,
}


def _years_of_career(career_start_date: date, reference_date: date) -> float:
    return (reference_date - career_start_date).days / 365.25


def compute_hour_rate(
    has_rqe: bool,
    career_start_date: date | None,
    reference_date: date | None = None,
) -> HourRateResult:
    reference_date = reference_date or date.today()
    prefix = "E" if has_rqe else "M"

    if career_start_date is None:
        tier = f"{prefix}-1"
        return HourRateResult(tier=tier, rate=_RATES[tier])

    years = _years_of_career(career_start_date, reference_date)
    suffix = "5"
    for limit, bracket_suffix in _BRACKETS:
        if years <= limit:
            suffix = bracket_suffix
            break

    tier = f"{prefix}-{suffix}"
    return HourRateResult(tier=tier, rate=_RATES[tier])
