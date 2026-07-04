"""OperationalKPI — Operational performance indicators."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class OperationalKPI:
    """Operational Key Performance Indicator."""
    period_id: int
    year_month: str
    total_shifts: int = 0
    total_doctors: int = 0
    total_hours: float = 0.0
    total_extras: int = 0
    extras_approved: int = 0
    extras_rejected: int = 0
    extras_pending: int = 0
    extra_approval_rate: float = 0.0
    doctors_per_shift: float = 0.0
    hours_per_doctor: float = 0.0
    average_assignment_duration: float = 0.0
    utilization_rate: float = 0.0
    trend: str = "stable"
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Indicadores de desempenho operacional da instituição"

    @property
    def formula(self) -> str:
        return "doctors_per_shift = total_doctors / total_shifts"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de plantões: {self.total_shifts}",
            f"Total de médicos: {self.total_doctors}",
            f"Total de horas: {self.total_hours:.1f}",
            f"Total de extras: {self.total_extras}",
        ]

    @property
    def explanation(self) -> str:
        if self.extra_approval_rate > 80:
            return "Taxa de aprovação de extras alta. Processo de solicitação bem definido."
        elif self.extra_approval_rate > 50:
            return "Taxa de aprovação de extras moderada. Revisar critérios de aprovação."
        return "Taxa de aprovação de extras baixa. Verificar processos de solicitação."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "total_shifts": self.total_shifts,
            "total_doctors": self.total_doctors,
            "total_hours": self.total_hours,
            "total_extras": self.total_extras,
            "extras_approved": self.extras_approved,
            "extras_rejected": self.extras_rejected,
            "extras_pending": self.extras_pending,
            "extra_approval_rate": self.extra_approval_rate,
            "doctors_per_shift": self.doctors_per_shift,
            "hours_per_doctor": self.hours_per_doctor,
            "average_assignment_duration": self.average_assignment_duration,
            "utilization_rate": self.utilization_rate,
            "trend": self.trend,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
