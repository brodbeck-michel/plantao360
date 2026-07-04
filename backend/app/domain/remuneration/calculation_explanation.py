"""Calculation Explanation — Full audit trail for a single calculation."""

from dataclasses import dataclass, field


@dataclass
class ExplanationStep:
    """A single step in the calculation explanation."""
    step_number: int
    description: str
    input_value: float
    output_value: float
    details: str = ""


@dataclass
class CalculationExplanation:
    """Complete and immutable explanation of how a calculation was executed.

    This is the central element for auditability.
    """

    fact_id: int
    fact_type: str
    doctor_id: int
    duration_minutes: int
    rule_id: str
    rule_version: str
    hour_rate: float
    multiplier: float
    steps: list[ExplanationStep] = field(default_factory=list)
    total_value: float = 0.0

    def add_step(
        self, description: str, input_value: float,
        output_value: float, details: str = ""
    ) -> None:
        """Add a step to the explanation."""
        step = ExplanationStep(
            step_number=len(self.steps) + 1,
            description=description,
            input_value=input_value,
            output_value=output_value,
            details=details,
        )
        self.steps.append(step)

    def to_dict(self) -> dict:
        """Serialize explanation to dictionary."""
        return {
            "fact_id": self.fact_id,
            "fact_type": self.fact_type,
            "doctor_id": self.doctor_id,
            "duration_minutes": self.duration_minutes,
            "duration_hours": self.duration_minutes / 60.0,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "hour_rate": self.hour_rate,
            "multiplier": self.multiplier,
            "steps": [
                {
                    "step": s.step_number,
                    "description": s.description,
                    "input": s.input_value,
                    "output": s.output_value,
                    "details": s.details,
                }
                for s in self.steps
            ],
            "total_value": self.total_value,
        }
