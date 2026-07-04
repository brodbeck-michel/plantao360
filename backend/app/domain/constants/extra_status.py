"""Extra status constants."""

from enum import StrEnum


class ExtraStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
