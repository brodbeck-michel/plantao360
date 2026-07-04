"""Tests for Financial Snapshot Builder."""

import pytest

from app.domain.financial.financial_snapshot_builder import (
    FinancialSnapshotBuilder,
    FinancialFactData,
    FinancialSnapshotData,
)
from app.domain.coverage.coverage_engine import CoverageResult, CoverageFact
from app.domain.constants.financial_fact_status import FinancialFactStatus


class TestFinancialSnapshotBuilder:
    def setup_method(self):
        self.builder = FinancialSnapshotBuilder()

    def test_build_empty_coverage(self):
        result = CoverageResult(shift_id=1)
        snapshot = self.builder.build(
            period_id=1,
            coverage_snapshot_id=1,
            coverage_results=[result],
        )

        assert snapshot.total_facts == 0
        assert snapshot.total_duration_minutes == 0
        assert len(snapshot.facts) == 0

    def test_build_with_assignment_fact(self):
        fact = CoverageFact(
            doctor_id=1,
            fact_type="assignment_completion",
            duration_minutes=480,
            source_event="assignment.completed.v1",
            source_id=1,
        )
        result = CoverageResult(shift_id=1, facts=[fact])

        snapshot = self.builder.build(
            period_id=1,
            coverage_snapshot_id=1,
            coverage_results=[result],
        )

        assert snapshot.total_facts == 1
        assert snapshot.total_duration_minutes == 480
        assert snapshot.facts[0].fact_type == "assignment_completion"
        assert snapshot.facts[0].doctor_id == 1
        assert snapshot.facts[0].period_id == 1

    def test_build_with_extra_fact(self):
        fact = CoverageFact(
            doctor_id=2,
            fact_type="extra_approved",
            duration_minutes=60,
            source_event="extra.approved.v1",
            source_id=1,
        )
        result = CoverageResult(shift_id=1, facts=[fact])

        snapshot = self.builder.build(
            period_id=1,
            coverage_snapshot_id=1,
            coverage_results=[result],
        )

        assert snapshot.total_facts == 1
        assert snapshot.facts[0].fact_type == "extra_approved"

    def test_build_with_multiple_results(self):
        fact1 = CoverageFact(
            doctor_id=1,
            fact_type="assignment_completion",
            duration_minutes=480,
            source_event="assignment.completed.v1",
            source_id=1,
        )
        fact2 = CoverageFact(
            doctor_id=2,
            fact_type="extra_approved",
            duration_minutes=60,
            source_event="extra.approved.v1",
            source_id=1,
        )
        result1 = CoverageResult(shift_id=1, facts=[fact1])
        result2 = CoverageResult(shift_id=2, facts=[fact2])

        snapshot = self.builder.build(
            period_id=1,
            coverage_snapshot_id=1,
            coverage_results=[result1, result2],
        )

        assert snapshot.total_facts == 2
        assert snapshot.total_duration_minutes == 540

    def test_build_default_status_is_active(self):
        snapshot = self.builder.build(
            period_id=1,
            coverage_snapshot_id=1,
            coverage_results=[],
        )

        assert snapshot.facts == []

    def test_financial_fact_data_defaults(self):
        fact = FinancialFactData(
            period_id=1,
            doctor_id=1,
            fact_type="assignment_completion",
            duration_minutes=480,
            source_event="assignment.completed.v1",
            source_id=1,
        )

        assert fact.status == FinancialFactStatus.ACTIVE
