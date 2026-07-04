"""FinancialKPI — Financial performance indicators."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class FinancialKPI:
    """Financial Key Performance Indicator."""
    period_id: int
    year_month: str
    total_remuneration: float = 0.0
    cost_per_shift: float = 0.0
    cost_per_doctor: float = 0.0
    cost_per_hour: float = 0.0
    total_hours: float = 0.0
    total_shifts: int = 0
    total_doctors: int = 0
    cost_by_type: dict[str, float] = field(default_factory=dict)
    cost_by_doctor: list[dict] = field(default_factory=list)
    trend: str = "stable"
    previous_period_total: float | None = None
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Indicadores financeiros consolidados do período"

    @property
    def formula(self) -> str:
        return "cost_per_shift = total_remuneration / total_shifts"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de remunerações: R$ {self.total_remuneration:.2f}",
            f"Total de plantões: {self.total_shifts}",
            f"Total de horas: {self.total_hours:.1f}",
            f"Total de médicos: {self.total_doctors}",
        ]

    @property
    def explanation(self) -> str:
        if self.previous_period_total and self.total_remuneration > self.previous_period_total:
            pct = ((self.total_remuneration - self.previous_period_total) / self.previous_period_total) * 100
            return f"Custo aumentou {pct:.1f}% em relação ao período anterior."
        elif self.previous_period_total and self.total_remuneration < self.previous_period_total:
            pct = ((self.previous_period_total - self.total_remuneration) / self.previous_period_total) * 100
            return f"Custo diminuiu {pct:.1f}% em relação ao período anterior."
        return "Custo dentro do esperado para o período."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "total_remuneration": self.total_remuneration,
            "cost_per_shift": self.cost_per_shift,
            "cost_per_doctor": self.cost_per_doctor,
            "cost_per_hour": self.cost_per_hour,
            "total_hours": self.total_hours,
            "total_shifts": self.total_shifts,
            "total_doctors": self.total_doctors,
            "cost_by_type": self.cost_by_type,
            "cost_by_doctor": self.cost_by_doctor,
            "trend": self.trend,
            "previous_period_total": self.previous_period_total,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
