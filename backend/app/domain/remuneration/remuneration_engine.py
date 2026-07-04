"""Remuneration Engine — Orchestrates calculation of remuneration from financial facts."""

from datetime import datetime

from app.domain.remuneration.pricing_policy import PricingPolicy
from app.domain.remuneration.remuneration_calculator import (
    RemunerationCalculator,
    CalculationInput,
)
from app.domain.remuneration.remuneration_result import (
    RemunerationResult,
    DoctorRemuneration,
)
from app.domain.financial.financial_snapshot_builder import FinancialFactData


class RemunerationEngine:
    """Orchestrates remuneration calculation.

    Does NOT access database. Works only on domain objects.
    Receives FinancialSnapshot data and PricingPolicy.
    Returns RemunerationResult.
    """

    def __init__(self, policy: PricingPolicy):
        self._policy = policy
        self._calculator = RemunerationCalculator()

    def calculate(
        self,
        period_id: int,
        facts: list[FinancialFactData],
        doctor_rates: dict[int, float],
        is_simulation: bool = False,
    ) -> RemunerationResult:
        """Calculate remuneration for a period.

        Args:
            period_id: The period to calculate for
            facts: List of financial facts
            doctor_rates: Map of doctor_id -> hour_rate
            is_simulation: If True, result is not persisted

        Returns:
            RemunerationResult with all calculations
        """
        result = RemunerationResult(
            period_id=period_id,
            is_simulation=is_simulation,
            calculated_at=datetime.utcnow(),
        )

        doctor_facts: dict[int, list[FinancialFactData]] = {}
        for fact in facts:
            if fact.doctor_id not in doctor_facts:
                doctor_facts[fact.doctor_id] = []
            doctor_facts[fact.doctor_id].append(fact)

        for doctor_id, doctor_facts_list in doctor_facts.items():
            doctor_result = self._calculate_doctor(
                doctor_id, doctor_facts_list, doctor_rates.get(doctor_id, 0.0)
            )
            result.add_doctor_result(doctor_result)

        return result

    def _calculate_doctor(
        self,
        doctor_id: int,
        facts: list[FinancialFactData],
        hour_rate: float,
    ) -> DoctorRemuneration:
        """Calculate remuneration for a single doctor."""
        calculations = []
        total_value = 0.0

        for fact in facts:
            from datetime import datetime as dt
            fact_date = dt.utcnow().date()

            rule = self._policy.select_rule(fact.fact_type, fact_date)
            if rule is None:
                continue

            calculation_input = CalculationInput(
                fact_id=0,
                fact_type=fact.fact_type,
                doctor_id=doctor_id,
                duration_minutes=fact.duration_minutes,
                hour_rate=hour_rate,
                fact_date=fact_date.isoformat(),
            )

            output = self._calculator.calculate(calculation_input, rule)
            calculations.append(output.explanation)
            total_value += output.value

        return DoctorRemuneration(
            doctor_id=doctor_id,
            total_value=total_value,
            calculations=calculations,
        )
