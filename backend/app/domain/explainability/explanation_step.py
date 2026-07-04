"""ExplanationStep — A single step in a domain explanation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExplanationStep:
    """A single step explaining why something happened.

    Cada passo é reproduzível e rastreável.
    """
    step_number: int
    description: str
    rule_applied: str
    input_value: float = 0.0
    output_value: float = 0.0
    multiplier: float = 1.0
    duration_minutes: int = 0
    evidence: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        return {
            "step_number": self.step_number,
            "description": self.description,
            "rule_applied": self.rule_applied,
            "input_value": self.input_value,
            "output_value": self.output_value,
            "multiplier": self.multiplier,
            "duration_minutes": self.duration_minutes,
            "evidence": self.evidence,
            "source": self.source,
        }
