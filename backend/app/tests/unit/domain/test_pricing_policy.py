"""Tests for PricingPolicy."""

import pytest
from datetime import date

from app.domain.remuneration.remuneration_rule import RemunerationRule
from app.domain.remuneration.pricing_policy import PricingPolicy


class TestPricingPolicy:
    def setup_method(self):
        self.rules = [
            RemunerationRule(
                rule_id="AC-001",
                fact_type="assignment_completion",
                version="1.0",
                valid_from=date(2025, 1, 1),
                valid_until=None,
                multiplier=1.0,
            ),
            RemunerationRule(
                rule_id="EX-001",
                fact_type="extra_approved",
                version="1.0",
                valid_from=date(2025, 1, 1),
                valid_until=None,
                multiplier=1.0,
            ),
            RemunerationRule(
                rule_id="AC-H01",
                fact_type="assignment_completion",
                version="1.0",
                valid_from=date(2025, 1, 1),
                valid_until=None,
                multiplier=1.5,
            ),
        ]
        self.policy = PricingPolicy(self.rules)

    def test_select_rule_for_assignment(self):
        rule = self.policy.select_rule("assignment_completion", date(2025, 6, 15))
        assert rule is not None
        assert rule.fact_type == "assignment_completion"

    def test_select_rule_for_extra(self):
        rule = self.policy.select_rule("extra_approved", date(2025, 6, 15))
        assert rule is not None
        assert rule.fact_type == "extra_approved"

    def test_select_rule_unknown_type_returns_none(self):
        rule = self.policy.select_rule("unknown_type", date(2025, 6, 15))
        assert rule is None

    def test_select_rule_no_valid_rule_returns_none(self):
        rules = [
            RemunerationRule(
                rule_id="AC-001",
                fact_type="assignment_completion",
                version="1.0",
                valid_from=date(2025, 1, 1),
                valid_until=date(2025, 6, 30),
                multiplier=1.0,
            ),
        ]
        policy = PricingPolicy(rules)
        rule = policy.select_rule("assignment_completion", date(2025, 7, 1))
        assert rule is None

    def test_get_rules_for_type(self):
        rules = self.policy.get_rules_for_type("assignment_completion")
        assert len(rules) == 2

    def test_get_all_rules(self):
        rules = self.policy.get_all_rules()
        assert len(rules) == 3
