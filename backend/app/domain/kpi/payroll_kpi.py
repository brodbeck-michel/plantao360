"""PayrollKPI — Payroll performance indicators."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class PayrollKPI:
    """Payroll Key Performance Indicator."""
    period_id: int
    year_month: str
    total_competencies: int = 0
    approved_competencies: int = 0
    pending_competencies: int = 0
    reopened_competencies: int = 0
    average_time_to_close_days: float = 0.0
    average_time_to_approve_days: float = 0.0
    reopen_rate: float = 0.0
    approval_rate: float = 0.0
    total_versions: int = 0
    average_versions_per_competency: float = 0.0
    trend: str = "stable"
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Indicadores de desempenho do processo de folha de pagamento"

    @property
    def formula(self) -> str:
        return "reopen_rate = reopened_competencies / total_competencies * 100"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de competências: {self.total_competencies}",
            f"Aprovadas: {self.approved_competencies}",
            f"Pendentes: {self.pending_competencies}",
            f"Reabertas: {self.reopened_competencies}",
        ]

    @property
    def explanation(self) -> str:
        if self.reopen_rate > 20:
            return "Taxa de reabertura alta. Processo de validação pode precisar de melhoria."
        elif self.reopen_rate > 10:
            return "Taxa de reabertura moderada. Monitorar tendências."
        return "Taxa de reabertura dentro do esperado."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "total_competencies": self.total_competencies,
            "approved_competencies": self.approved_competencies,
            "pending_competencies": self.pending_competencies,
            "reopened_competencies": self.reopened_competencies,
            "average_time_to_close_days": self.average_time_to_close_days,
            "average_time_to_approve_days": self.average_time_to_approve_days,
            "reopen_rate": self.reopen_rate,
            "approval_rate": self.approval_rate,
            "total_versions": self.total_versions,
            "average_versions_per_competency": self.average_versions_per_competency,
            "trend": self.trend,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
