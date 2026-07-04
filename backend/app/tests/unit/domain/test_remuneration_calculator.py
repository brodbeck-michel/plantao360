"""Tests for RemunerationCalculator."""

import pytest

from app.domain.remuneration.remuneration_rule import RemunerationRule
from app.domain.remuneration.remuneration_calculator import (
    RemunerationCalculator,
    CalculationInput,
)
from datetime import date


class TestRemunerationCalculator:
    def setup_method(self):
        self.calculator = RemunerationCalculator()
        self.rule = RemunerationRule(
            rule_id="AC-001",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=None,
            multiplier=1.0,
        )

    def test_calculate_basic(self):
        fact = CalculationInput(
            fact_id=1,
            fact_type="assignment_completion",
            doctor_id=1,
            duration_minutes=480,
            hour_rate=150.0,
            fact_date="2025-06-15",
        )

        output = self.calculator.calculate(fact, self.rule)

        assert output.value == 1200.0
        assert output.doctor_id == 1
        assert output.explanation.total_value == 1200.0

    def test_calculate_with_multiplier(self):
        rule = RemunerationRule(
            rule_id="AC-H01",
            fact_type="assignment_completion",
            version="1.0",
            valid_from=date(2025, 1, 1),
            valid_until=None,
            multiplier=1.5,
        )
        fact = CalculationInput(
            fact_id=1,
            fact_type="assignment_completion",
            doctor_id=1,
            duration_minutes=480,
            hour_rate=150.0,
            fact_date="2025-06-15",
        )

        output = self.calculator.calculate(fact, rule)

        assert output.value == 1800.0

    def test_calculate_short_duration(self):
        fact = CalculationInput(
            fact_id=1,
            fact_type="extra_approved",
            doctor_id=1,
            duration_minutes=60,
            hour_rate=150.0,
            fact_date="2025-06-15",
        )

        output = self.calculator.calculate(fact, self.rule)

        assert output.value == 150.0

    def test_calculate_explanation_has_steps(self):
        fact = CalculationInput(
            fact_id=1,
            fact_type="assignment_completion",
            doctor_id=1,
            duration_minutes=480,
            hour_rate=150.0,
            fact_date="2025-06-15",
        )

        output = self.calculator.calculate(fact, self.rule)

        assert len(output.explanation.steps) == 4
        assert output.explanation.rule_id == "AC-001"

    def test_calculate_zero_duration(self):
        fact = CalculationInput(
            fact_id=1,
            fact_type="assignment_completion",
            doctor_id=1,
            duration_minutes=0,
            hour_rate=150.0,
            fact_date="2025-06-15",
        )

        output = self.calculator.calculate(fact, self.rule)

        assert output.value == 0.0
