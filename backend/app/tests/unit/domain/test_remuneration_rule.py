"""Tests for RemunerationRule."""

import pytest
from datetime import date

from app.domain.remuneration.remuneration_rule import RemunerationRule


class TestRemunerationRule:
    def test_rule_creation(self):
        rule = RemunerationRule(
            rule_id="AC-001",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=None,
            hour_rate_source="doctor",
            multiplier=1.0,
            description="Standard rule",
        )
        assert rule.rule_id == "AC-001"
        assert rule.fact_type == "assignment_completion"
        assert rule.multiplier == 1.0

    def test_rule_valid_for_date_within_range(self):
        rule = RemunerationRule(
            rule_id="AC-001",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=date(2025, 12, 31),
            multiplier=1.0,
        )
        assert rule.is_valid_for(date(2025, 6, 15)) is True

    def test_rule_valid_for_date_before_range(self):
        rule = RemunerationRule(
            rule_id="AC-001",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=date(2025, 12, 31),
            multiplier=1.0,
        )
        assert rule.is_valid_for(date(2024, 12, 31)) is False

    def test_rule_valid_for_date_after_range(self):
        rule = RemunerationRule(
            rule_id="AC-001",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=date(2025, 12, 31),
            multiplier=1.0,
        )
        assert rule.is_valid_for(date(2026, 1, 1)) is False

    def test_rule_valid_for_date_open_ended(self):
        rule = RemunerationRule(
            rule_id="AC-001",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=None,
            multiplier=1.0,
        )
        assert rule.is_valid_for(date(2099, 12, 31)) is True

    def test_rule_with_holiday_multiplier(self):
        rule = RemunerationRule(
            rule_id="AC-H01",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=None,
            multiplier=1.5,
            description="Holiday rule",
        )
        assert rule.multiplier == 1.5
