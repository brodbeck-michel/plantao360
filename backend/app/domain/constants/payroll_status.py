"""Payroll status constants."""

from enum import StrEnum


class PayrollStatus(StrEnum):
    DRAFT = "draft"
    CALCULATED = "calculated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    LOCKED = "locked"
    EXPORTED = "exported"
    PAID = "paid"
    ARCHIVED = "archived"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]
