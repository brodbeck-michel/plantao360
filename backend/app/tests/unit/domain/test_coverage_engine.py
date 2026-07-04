"""Tests for Coverage Engine."""

import pytest
from dataclasses import dataclass

from app.domain.coverage.coverage_engine import CoverageEngine, CoverageResult
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.constants.extra_status import ExtraStatus


@dataclass
class FakeShift:
    id: int
    status: str
    shift_parts: list
    shift_extras: list


@dataclass
class FakeAssignment:
    id: int
    doctor_id: int
    status: str
    duration_minutes: int | None


@dataclass
class FakeExtra:
    id: int
    doctor_id: int
    status: str
    duration_minutes: int


class TestCoverageEngine:
    def setup_method(self):
        self.engine = CoverageEngine()

    def test_consolidate_shift_completed_assignment(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.COMPLETED, duration_minutes=480)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 1
        assert result.facts[0].fact_type == "assignment_completion"
        assert result.facts[0].duration_minutes == 480
        assert result.facts[0].doctor_id == 1

    def test_consolidate_shift_approved_extra(self):
        extra = FakeExtra(id=1, doctor_id=1, status=ExtraStatus.APPROVED, duration_minutes=60)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[], shift_extras=[extra])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 1
        assert result.facts[0].fact_type == "extra_approved"
        assert result.facts[0].duration_minutes == 60

    def test_consolidate_shift_rejected_extra_not_included(self):
        extra = FakeExtra(id=1, doctor_id=1, status=ExtraStatus.REJECTED, duration_minutes=60)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[], shift_extras=[extra])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_pending_extra_not_included(self):
        extra = FakeExtra(id=1, doctor_id=1, status=ExtraStatus.PENDING, duration_minutes=60)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[], shift_extras=[extra])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_cancelled_extra_not_included(self):
        extra = FakeExtra(id=1, doctor_id=1, status=ExtraStatus.CANCELLED, duration_minutes=60)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[], shift_extras=[extra])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_planned_assignment_not_included(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.PLANNED, duration_minutes=480)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_confirmed_assignment_not_included(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.CONFIRMED, duration_minutes=480)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_started_assignment_not_included(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.STARTED, duration_minutes=480)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_cancelled_assignment_not_included(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.CANCELLED, duration_minutes=480)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0

    def test_consolidate_shift_completed_assignment_on_cancelled_shift(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.COMPLETED, duration_minutes=480)
        shift = FakeShift(id=1, status=ShiftStatus.CANCELLED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0
        assert result.total_inconsistencies == 1
        assert result.inconsistencies[0].inconsistency_type == "completed_assignment_on_cancelled_shift"

    def test_consolidate_shift_mixed_facts(self):
        a1 = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.COMPLETED, duration_minutes=480)
        a2 = FakeAssignment(id=2, doctor_id=2, status=AssignmentStatus.COMPLETED, duration_minutes=480)
        e1 = FakeExtra(id=1, doctor_id=1, status=ExtraStatus.APPROVED, duration_minutes=60)
        e2 = FakeExtra(id=2, doctor_id=2, status=ExtraStatus.REJECTED, duration_minutes=30)

        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[a1, a2], shift_extras=[e1, e2])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 3
        assert result.total_duration_minutes == 1020

    def test_consolidate_period(self):
        a1 = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.COMPLETED, duration_minutes=480)
        s1 = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[a1], shift_extras=[])
        s2 = FakeShift(id=2, status=ShiftStatus.COMPLETED, shift_parts=[], shift_extras=[])

        results = self.engine.consolidate_period([s1, s2])

        assert len(results) == 2
        assert results[0].total_facts == 1
        assert results[1].total_facts == 0

    def test_consolidate_shift_empty(self):
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0
        assert result.total_inconsistencies == 0
        assert result.total_duration_minutes == 0

    def test_coverage_result_properties(self):
        result = CoverageResult(shift_id=1)
        assert result.total_facts == 0
        assert result.total_duration_minutes == 0

    def test_consolidate_shift_assignment_without_duration(self):
        assignment = FakeAssignment(id=1, doctor_id=1, status=AssignmentStatus.COMPLETED, duration_minutes=None)
        shift = FakeShift(id=1, status=ShiftStatus.COMPLETED, shift_parts=[assignment], shift_extras=[])

        result = self.engine.consolidate_shift(shift)

        assert result.total_facts == 0
