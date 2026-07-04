"""Remuneration Rule — Defines how a financial fact is converted to value."""

from dataclasses import dataclass
from datetime import date


@dataclass
class RemunerationRule:
    """A rule that defines how to calculate remuneration for a fact type.

    Rules are immutable. To change a rule, create a new version
    with a different validity period.
    """

    rule_id: str
    fact_type: str
    version: str
    valid_from: date
    valid_until: date | None
    hour_rate_source: str = "doctor"
    multiplier: float = 1.0
    description: str = ""

    def is_valid_for(self, fact_date: date) -> bool:
        """Check if this rule is valid for a given date."""
        if fact_date < self.valid_from:
            return False
        if self.valid_until is not None and fact_date >= self.valid_until:
            return False
        return True

    def is_active(self) -> bool:
        """Check if this rule is currently active."""
        from datetime import date as date_type
        return self.is_valid_for(date_type.today())
