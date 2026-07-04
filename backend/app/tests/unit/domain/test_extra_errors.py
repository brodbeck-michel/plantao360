"""Tests for Extra error codes."""

from app.domain.errors.extra_errors import ExtraErrorCode


class TestExtraErrorCodes:
    def test_all_codes_are_strings(self):
        for code in ExtraErrorCode:
            assert isinstance(code, str)

    def test_not_found_code(self):
        assert ExtraErrorCode.EXTRA_NOT_FOUND == "extra.not_found"

    def test_duration_invalid_code(self):
        assert ExtraErrorCode.EXTRA_DURATION_INVALID == "extra.duration_invalid"

    def test_justification_required_code(self):
        assert ExtraErrorCode.EXTRA_JUSTIFICATION_REQUIRED == "extra.justification_required"

    def test_has_required_codes(self):
        required = [
            "extra.not_found",
            "extra.duration_invalid",
            "extra.justification_required",
            "extra.shift_not_found",
            "extra.doctor_not_found",
            "extra.period_closed",
            "extra.period_paid",
            "extra.shift_cancelled",
            "extra.invalid_transition",
            "extra.not_editable",
            "extra.max_duration_exceeded",
        ]
        for code in required:
            assert code in [e.value for e in ExtraErrorCode], f"Missing {code}"
