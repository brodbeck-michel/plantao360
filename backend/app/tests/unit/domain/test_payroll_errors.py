"""Tests for payroll error codes."""

from app.domain.errors.payroll_errors import PayrollErrorCode


class TestPayrollErrors:
    def test_payroll_not_found(self):
        assert PayrollErrorCode.PAYROLL_NOT_FOUND == "payroll_not_found"

    def test_payroll_already_exists(self):
        assert PayrollErrorCode.PAYROLL_ALREADY_EXISTS == "payroll_already_exists"

    def test_payroll_immutable(self):
        assert PayrollErrorCode.PAYROLL_IMMUTABLE == "payroll_immutable"

    def test_payroll_invalid_transition(self):
        assert PayrollErrorCode.PAYROLL_INVALID_TRANSITION == "payroll_invalid_transition"

    def test_payroll_requires_seal(self):
        assert PayrollErrorCode.PAYROLL_REQUIRES_SEAL == "payroll_requires_seal"

    def test_payroll_requires_version(self):
        assert PayrollErrorCode.PAYROLL_REQUIRES_VERSION == "payroll_requires_version"

    def test_payroll_requires_snapshot(self):
        assert PayrollErrorCode.PAYROLL_REQUIRES_SNAPSHOT == "payroll_requires_snapshot"

    def test_payroll_requires_review(self):
        assert PayrollErrorCode.PAYROLL_REQUIRES_REVIEW == "payroll_requires_review"

    def test_payroll_requires_approval(self):
        assert PayrollErrorCode.PAYROLL_REQUIRES_APPROVAL == "payroll_requires_approval"

    def test_payroll_reopen_failed(self):
        assert PayrollErrorCode.PAYROLL_REOPEN_FAILED == "payroll_reopen_failed"

    def test_payroll_archive_failed(self):
        assert PayrollErrorCode.PAYROLL_ARCHIVE_FAILED == "payroll_archive_failed"

    def test_total_error_count(self):
        assert len(PayrollErrorCode) == 19
