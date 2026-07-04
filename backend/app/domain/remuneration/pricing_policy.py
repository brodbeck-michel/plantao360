"""Pricing Policy — Selects which rule to apply for a financial fact."""

from dataclasses import dataclass
from datetime import date

from app.domain.remuneration.remuneration_rule import RemunerationRule


class PricingPolicy:
    """Selects the appropriate RemunerationRule for a given financial fact.

    Does NOT calculate values. Only selects the rule.
    """

    def __init__(self, rules: list[RemunerationRule]):
        self._rules = rules

    def select_rule(self, fact_type: str, fact_date: date) -> RemunerationRule | None:
        """Select the active rule for a given fact type and date.

        If multiple rules match, returns the most recently created one.
        """
        candidates = [
            r for r in self._rules
            if r.fact_type == fact_type and r.is_valid_for(fact_date)
        ]
        if not candidates:
            return None
        return candidates[-1]

    def get_rules_for_type(self, fact_type: str) -> list[RemunerationRule]:
        """Get all rules for a given fact type."""
        return [r for r in self._rules if r.fact_type == fact_type]

    def get_all_rules(self) -> list[RemunerationRule]:
        """Get all rules."""
        return list(self._rules)
