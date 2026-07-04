"""DomainExplanation — Explains why something happened using domain rules."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.explainability.explanation_step import ExplanationStep
from app.domain.explainability.explanation_context import ExplanationContext


@dataclass(frozen=True)
class DomainExplanation:
    """Explains why something happened using domain rules.

    Toda resposta é reproduzível. Usa as mesmas regras do domínio operacional.
    """
    question: str
    answer: str
    entity_type: str
    entity_id: int
    context: ExplanationContext
    steps: list[ExplanationStep] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    rules_applied: list[str] = field(default_factory=list)
    confidence: float = 1.0
    generated_at: datetime | None = None
    generated_by: str = "system"

    @property
    def is_reproducible(self) -> bool:
        return len(self.steps) > 0 and len(self.rules_applied) > 0

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.answer,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "context": self.context.to_dict(),
            "steps": [s.to_dict() for s in self.steps],
            "evidence": self.evidence,
            "rules_applied": self.rules_applied,
            "confidence": self.confidence,
            "is_reproducible": self.is_reproducible,
            "total_steps": self.total_steps,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "generated_by": self.generated_by,
        }
