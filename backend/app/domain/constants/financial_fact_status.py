"""Financial fact status constants."""

from enum import StrEnum


class FinancialFactStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
