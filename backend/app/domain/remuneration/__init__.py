"""Remuneration domain — Rule, Result, Explanation (data classes usadas por payroll).

O motor de cálculo (Calculator/Engine/PricingPolicy) era prod=0 e foi removido no colapso da
domain/ (spec 004, Grupo A); a fórmula útil ficou registrada em docs/backlog-melhorias.md (B-06).
"""

from app.domain.remuneration.remuneration_rule import RemunerationRule
from app.domain.remuneration.remuneration_result import (
    RemunerationResult,
    DoctorRemuneration,
)
from app.domain.remuneration.calculation_explanation import (
    CalculationExplanation,
    ExplanationStep,
)

__all__ = [
    "RemunerationRule",
    "RemunerationResult",
    "DoctorRemuneration",
    "CalculationExplanation",
    "ExplanationStep",
]
