"""Tests for financial domain constants."""

from app.domain.constants.financial_fact_type import FinancialFactType
from app.domain.constants.financial_fact_status import FinancialFactStatus
from app.domain.constants.snapshot_status import SnapshotStatus
from app.domain.constants.inconsistency_type import InconsistencyType


class TestFinancialFactType:
    def test_assignment_completion(self):
        assert FinancialFactType.ASSIGNMENT_COMPLETION == "assignment_completion"

    def test_extra_approved(self):
        assert FinancialFactType.EXTRA_APPROVED == "extra_approved"

    def test_has_two_types(self):
        assert len(FinancialFactType) == 2


class TestFinancialFactStatus:
    def test_active(self):
        assert FinancialFactStatus.ACTIVE == "active"

    def test_revoked(self):
        assert FinancialFactStatus.REVOKED == "revoked"

    def test_has_two_statuses(self):
        assert len(FinancialFactStatus) == 2


class TestSnapshotStatus:
    def test_active(self):
        assert SnapshotStatus.ACTIVE == "active"

    def test_invalidated(self):
        assert SnapshotStatus.INVALIDATED == "invalidated"

    def test_has_two_statuses(self):
        assert len(SnapshotStatus) == 2


class TestInconsistencyType:
    def test_extra_without_assignment(self):
        assert InconsistencyType.EXTRA_WITHOUT_ASSIGNMENT == "extra_without_assignment"

    def test_completed_assignment_on_cancelled_shift(self):
        assert InconsistencyType.COMPLETED_ASSIGNMENT_ON_CANCELLED_SHIFT == "completed_assignment_on_cancelled_shift"

    def test_overlapping_assignments(self):
        assert InconsistencyType.OVERLAPPING_ASSIGNMENTS == "overlapping_assignments"

    def test_has_eight_types(self):
        assert len(InconsistencyType) == 8
