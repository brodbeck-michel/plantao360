"""Remuneration Calculator — Executes calculation rules on financial facts."""

from dataclasses import dataclass

from app.domain.remuneration.remuneration_rule import RemunerationRule
from app.domain.remuneration.calculation_explanation import CalculationExplanation


@dataclass
class CalculationInput:
    """Input for a single calculation."""
    fact_id: int
    fact_type: str
    doctor_id: int
    duration_minutes: int
    hour_rate: float
    fact_date: str


@dataclass
class CalculationOutput:
    """Output of a single calculation."""
    fact_id: int
    doctor_id: int
    value: float
    explanation: CalculationExplanation


class RemunerationCalculator:
    """Executes calculation rules on financial facts.

    Does NOT access database. Works only on domain objects.
    """

    def calculate(self, fact: CalculationInput, rule: RemunerationRule) -> CalculationOutput:
        """Calculate remuneration for a single fact using a rule.

        Args:
            fact: The financial fact to calculate
            rule: The rule to apply

        Returns:
            CalculationOutput with value and explanation
        """
        duration_hours = fact.duration_minutes / 60.0

        explanation = CalculationExplanation(
            fact_id=fact.fact_id,
            fact_type=fact.fact_type,
            doctor_id=fact.doctor_id,
            duration_minutes=fact.duration_minutes,
            rule_id=rule.rule_id,
            rule_version=rule.version,
            hour_rate=fact.hour_rate,
            multiplier=rule.multiplier,
        )

        explanation.add_step(
            description="Conversão de minutos para horas",
            input_value=float(fact.duration_minutes),
            output_value=duration_hours,
            details=f"{fact.duration_minutes} min ÷ 60 = {duration_hours:.2f} h",
        )

        explanation.add_step(
            description="Aplicação do valor hora",
            input_value=duration_hours,
            output_value=fact.hour_rate * duration_hours,
            details=f"{duration_hours:.2f} h × R$ {fact.hour_rate:.2f}/h = R$ {fact.hour_rate * duration_hours:.2f}",
        )

        value_before_multiplier = fact.hour_rate * duration_hours

        explanation.add_step(
            description="Aplicação do multiplicador",
            input_value=rule.multiplier,
            output_value=value_before_multiplier * rule.multiplier,
            details=f"R$ {value_before_multiplier:.2f} × {rule.multiplier} = R$ {value_before_multiplier * rule.multiplier:.2f}",
        )

        final_value = value_before_multiplier * rule.multiplier

        explanation.add_step(
            description="Valor final",
            input_value=final_value,
            output_value=final_value,
            details=f"R$ {final_value:.2f}",
        )

        explanation.total_value = final_value

        return CalculationOutput(
            fact_id=fact.fact_id,
            doctor_id=fact.doctor_id,
            value=final_value,
            explanation=explanation,
        )
