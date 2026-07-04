"""CoverageKPI — Coverage performance indicators."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CoverageKPI:
    """Coverage Key Performance Indicator.

    Cada KPI contém: definição, fórmula, evidências e explicação.
    """
    period_id: int
    year_month: str
    coverage_rate: float = 0.0
    total_shifts: int = 0
    covered_shifts: int = 0
    uncovered_shifts: int = 0
    coverage_by_type: dict[str, float] = field(default_factory=dict)
    coverage_by_day: list[dict] = field(default_factory=list)
    trend: str = "stable"
    previous_period_rate: float | None = None
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Percentual de plantões com ao menos um médico atribuído"

    @property
    def formula(self) -> str:
        return "covered_shifts / total_shifts * 100"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de plantões: {self.total_shifts}",
            f"Plantões cobertos: {self.covered_shifts}",
            f"Plantões descobertos: {self.uncovered_shifts}",
        ]

    @property
    def explanation(self) -> str:
        if self.coverage_rate >= 90:
            return "Cobertura adequada. A maioria dos plantões possui médicos atribuídos."
        elif self.coverage_rate >= 70:
            return "Cobertura parcial. Alguns plantões precisam de atenção."
        else:
            return "Cobertura insuficiente. Ação urgente necessária para evitar descobertos."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "coverage_rate": self.coverage_rate,
            "total_shifts": self.total_shifts,
            "covered_shifts": self.covered_shifts,
            "uncovered_shifts": self.uncovered_shifts,
            "coverage_by_type": self.coverage_by_type,
            "coverage_by_day": self.coverage_by_day,
            "trend": self.trend,
            "previous_period_rate": self.previous_period_rate,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
