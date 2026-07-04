"""Tests for RemunerationResult and RemunerationEngine."""

import pytest
from datetime import date

from app.domain.remuneration.remuneration_rule import RemunerationRule
from app.domain.remuneration.pricing_policy import PricingPolicy
from app.domain.remuneration.remuneration_engine import RemunerationEngine
from app.domain.remuneration.remuneration_result import RemunerationResult, DoctorRemuneration
from app.domain.remuneration.calculation_explanation import CalculationExplanation
from app.domain.financial.financial_snapshot_builder import FinancialFactData


class TestRemunerationResult:
    def test_empty_result(self):
        result = RemunerationResult(period_id=1)
        assert result.total_value == 0.0
        assert result.total_facts == 0
        assert len(result.doctor_results) == 0

    def test_add_doctor_result(self):
        result = RemunerationResult(period_id=1)
        dr = DoctorRemuneration(doctor_id=1, total_value=1200.0)
        result.add_doctor_result(dr)

        assert result.total_value == 1200.0
        assert result.total_facts == 0
        assert len(result.doctor_results) == 1

    def test_get_doctor_result(self):
        result = RemunerationResult(period_id=1)
        dr = DoctorRemuneration(doctor_id=1, total_value=1200.0)
        result.add_doctor_result(dr)

        found = result.get_doctor_result(1)
        assert found is not None
        assert found.total_value == 1200.0

    def test_get_doctor_result_not_found(self):
        result = RemunerationResult(period_id=1)
        found = result.get_doctor_result(999)
        assert found is None

    def test_to_dict(self):
        result = RemunerationResult(period_id=1, is_simulation=True)
        dr = DoctorRemuneration(doctor_id=1, total_value=1200.0)
        result.add_doctor_result(dr)

        d = result.to_dict()
        assert d["period_id"] == 1
        assert d["is_simulation"] is True
        assert d["total_value"] == 1200.0
        assert d["total_doctors"] == 1


class TestRemunerationEngine:
    def setup_method(self):
        rules = [
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
        ]
        self.policy = PricingPolicy(rules)
        self.engine = RemunerationEngine(self.policy)

    def test_calculate_empty_facts(self):
        result = self.engine.calculate(
            period_id=1,
            facts=[],
            doctor_rates={},
        )
        assert result.total_value == 0.0
        assert result.total_facts == 0

    def test_calculate_single_assignment(self):
        facts = [
            FinancialFactData(
                period_id=1,
                doctor_id=1,
                fact_type="assignment_completion",
                duration_minutes=480,
                source_event="assignment.completed.v1",
                source_id=1,
            ),
        ]
        doctor_rates = {1: 150.0}

        result = self.engine.calculate(
            period_id=1,
            facts=facts,
            doctor_rates=doctor_rates,
        )

        assert result.total_value == 1200.0
        assert result.total_facts == 1
        assert len(result.doctor_results) == 1

    def test_calculate_multiple_facts_same_doctor(self):
        facts = [
            FinancialFactData(
                period_id=1, doctor_id=1,
                fact_type="assignment_completion",
                duration_minutes=480,
                source_event="assignment.completed.v1", source_id=1,
            ),
            FinancialFactData(
                period_id=1, doctor_id=1,
                fact_type="extra_approved",
                duration_minutes=60,
                source_event="extra.approved.v1", source_id=1,
            ),
        ]
        doctor_rates = {1: 150.0}

        result = self.engine.calculate(
            period_id=1, facts=facts, doctor_rates=doctor_rates,
        )

        assert result.total_value == 1350.0
        assert result.total_facts == 2

    def test_calculate_multiple_doctors(self):
        facts = [
            FinancialFactData(
                period_id=1, doctor_id=1,
                fact_type="assignment_completion",
                duration_minutes=480,
                source_event="assignment.completed.v1", source_id=1,
            ),
            FinancialFactData(
                period_id=1, doctor_id=2,
                fact_type="assignment_completion",
                duration_minutes=480,
                source_event="assignment.completed.v1", source_id=2,
            ),
        ]
        doctor_rates = {1: 150.0, 2: 200.0}

        result = self.engine.calculate(
            period_id=1, facts=facts, doctor_rates=doctor_rates,
        )

        assert result.total_value == 2800.0
        assert len(result.doctor_results) == 2

    def test_calculate_simulation(self):
        facts = [
            FinancialFactData(
                period_id=1, doctor_id=1,
                fact_type="assignment_completion",
                duration_minutes=480,
                source_event="assignment.completed.v1", source_id=1,
            ),
        ]
        doctor_rates = {1: 150.0}

        result = self.engine.calculate(
            period_id=1, facts=facts, doctor_rates=doctor_rates,
            is_simulation=True,
        )

        assert result.is_simulation is True

    def test_calculate_unknown_fact_type_skipped(self):
        facts = [
            FinancialFactData(
                period_id=1, doctor_id=1,
                fact_type="unknown_type",
                duration_minutes=480,
                source_event="unknown.v1", source_id=1,
            ),
        ]
        doctor_rates = {1: 150.0}

        result = self.engine.calculate(
            period_id=1, facts=facts, doctor_rates=doctor_rates,
        )

        assert result.total_value == 0.0
        assert result.total_facts == 0

    def test_doctor_result_total_hours(self):
        facts = [
            FinancialFactData(
                period_id=1, doctor_id=1,
                fact_type="assignment_completion",
                duration_minutes=480,
                source_event="assignment.completed.v1", source_id=1,
            ),
        ]
        doctor_rates = {1: 150.0}

        result = self.engine.calculate(
            period_id=1, facts=facts, doctor_rates=doctor_rates,
        )

        dr = result.get_doctor_result(1)
        assert dr.total_hours == 8.0
