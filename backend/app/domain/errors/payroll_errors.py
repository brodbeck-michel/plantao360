"""Payroll error codes."""

from enum import StrEnum


class PayrollErrorCode(StrEnum):
    PAYROLL_NOT_FOUND = "payroll_not_found"
    PAYROLL_ALREADY_EXISTS = "payroll_already_exists"
    PAYROLL_IMMUTABLE = "payroll_immutable"
    PAYROLL_INVALID_TRANSITION = "payroll_invalid_transition"
    PAYROLL_REQUIRES_SEAL = "payroll_requires_seal"
    PAYROLL_REQUIRES_VERSION = "payroll_requires_version"
    PAYROLL_REQUIRES_SNAPSHOT = "payroll_requires_snapshot"
    PAYROLL_REQUIRES_REVIEW = "payroll_requires_review"
    PAYROLL_REQUIRES_APPROVAL = "payroll_requires_approval"
    PAYROLL_REOPEN_FAILED = "payroll_reopen_failed"
    PAYROLL_ARCHIVE_FAILED = "payroll_archive_failed"
    PAYROLL_NOT_READY = "payroll_not_ready"
    PAYROLL_CHECKLIST_INCOMPLETE = "payroll_checklist_incomplete"
    PAYROLL_ALREADY_LOCKED = "payroll_already_locked"
    PAYROLL_NOT_LOCKED = "payroll_not_locked"
    PAYROLL_LOCK_FAILED = "payroll_lock_failed"
    PAYROLL_UNLOCK_FAILED = "payroll_unlock_failed"
    PAYROLL_SEGREGATION_VIOLATION = "payroll_segregation_violation"
    PAYROLL_APPROVAL_FAILED = "payroll_approval_failed"
