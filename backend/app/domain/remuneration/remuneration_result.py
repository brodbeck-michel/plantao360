"""Remuneration Result — Consolidated result of remuneration calculation."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.remuneration.calculation_explanation import CalculationExplanation


@dataclass
class DoctorRemuneration:
    """Remuneration for a single doctor."""
    doctor_id: int
    total_value: float
    calculations: list[CalculationExplanation] = field(default_factory=list)

    @property
    def total_hours(self) -> float:
        return sum(c.duration_minutes / 60.0 for c in self.calculations)


@dataclass
class RemunerationResult:
    """Consolidated result of remuneration calculation for a period.

    Does NOT write to database. Pure domain object.
    """

    period_id: int
    is_simulation: bool = False
    calculated_at: datetime | None = None
    doctor_results: list[DoctorRemuneration] = field(default_factory=list)
    total_value: float = 0.0
    total_facts: int = 0

    def add_doctor_result(self, doctor_result: DoctorRemuneration) -> None:
        """Add a doctor's remuneration result."""
        self.doctor_results.append(doctor_result)
        self.total_value += doctor_result.total_value
        self.total_facts += len(doctor_result.calculations)

    def get_doctor_result(self, doctor_id: int) -> DoctorRemuneration | None:
        """Get result for a specific doctor."""
        for dr in self.doctor_results:
            if dr.doctor_id == doctor_id:
                return dr
        return None

    def to_dict(self) -> dict:
        """Serialize result to dictionary."""
        return {
            "period_id": self.period_id,
            "is_simulation": self.is_simulation,
            "total_value": self.total_value,
            "total_facts": self.total_facts,
            "total_doctors": len(self.doctor_results),
            "doctors": [
                {
                    "doctor_id": dr.doctor_id,
                    "total_value": dr.total_value,
                    "total_hours": dr.total_hours,
                    "facts_count": len(dr.calculations),
                }
                for dr in self.doctor_results
            ],
        }
