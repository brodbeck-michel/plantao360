"""Inconsistency type constants."""

from enum import StrEnum


class InconsistencyType(StrEnum):
    EXTRA_WITHOUT_ASSIGNMENT = "extra_without_assignment"
    EXTRA_AFTER_CLOSURE = "extra_after_closure"
    INACTIVE_DOCTOR_ASSIGNMENT = "inactive_doctor_assignment"
    COMPLETED_ASSIGNMENT_ON_CANCELLED_SHIFT = "completed_assignment_on_cancelled_shift"
    OVERLAPPING_ASSIGNMENTS = "overlapping_assignments"
    INCOMPLETE_ASSIGNMENT_AT_CLOSURE = "incomplete_assignment_at_closure"
    MODIFICATION_AFTER_PAYMENT = "modification_after_payment"
    ZERO_HOUR_RATE = "zero_hour_rate"
