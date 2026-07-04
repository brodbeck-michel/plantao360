"""Tests for payroll status constants."""

from app.domain.constants.payroll_status import PayrollStatus


class TestPayrollStatus:
    def test_draft_value(self):
        assert PayrollStatus.DRAFT == "draft"

    def test_calculated_value(self):
        assert PayrollStatus.CALCULATED == "calculated"

    def test_reviewed_value(self):
        assert PayrollStatus.REVIEWED == "reviewed"

    def test_approved_value(self):
        assert PayrollStatus.APPROVED == "approved"

    def test_exported_value(self):
        assert PayrollStatus.EXPORTED == "exported"

    def test_paid_value(self):
        assert PayrollStatus.PAID == "paid"

    def test_archived_value(self):
        assert PayrollStatus.ARCHIVED == "archived"

    def test_all_statuses(self):
        assert len(PayrollStatus.values()) == 8

    def test_values_method(self):
        values = PayrollStatus.values()
        assert "draft" in values
        assert "calculated" in values
        assert "reviewed" in values
        assert "approved" in values
        assert "exported" in values
        assert "paid" in values
        assert "archived" in values
