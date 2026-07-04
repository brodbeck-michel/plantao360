"""Extra error codes."""

from enum import StrEnum


class ExtraErrorCode(StrEnum):
    EXTRA_NOT_FOUND = "extra.not_found"
    EXTRA_DURATION_INVALID = "extra.duration_invalid"
    EXTRA_JUSTIFICATION_REQUIRED = "extra.justification_required"
    EXTRA_SHIFT_NOT_FOUND = "extra.shift_not_found"
    EXTRA_DOCTOR_NOT_FOUND = "extra.doctor_not_found"
    EXTRA_PERIOD_CLOSED = "extra.period_closed"
    EXTRA_PERIOD_PAID = "extra.period_paid"
    EXTRA_SHIFT_CANCELLED = "extra.shift_cancelled"
    EXTRA_INVALID_TRANSITION = "extra.invalid_transition"
    EXTRA_NOT_EDITABLE = "extra.not_editable"
    EXTRA_MAX_DURATION_EXCEEDED = "extra.max_duration_exceeded"
