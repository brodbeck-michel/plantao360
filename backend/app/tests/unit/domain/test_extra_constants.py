"""Tests for Extra status constants."""

from app.domain.constants.extra_status import ExtraStatus


class TestExtraStatus:
    def test_all_statuses_exist(self):
        assert ExtraStatus.PENDING == "pending"
        assert ExtraStatus.APPROVED == "approved"
        assert ExtraStatus.REJECTED == "rejected"
        assert ExtraStatus.CANCELLED == "cancelled"

    def test_has_four_statuses(self):
        assert len(ExtraStatus) == 4
