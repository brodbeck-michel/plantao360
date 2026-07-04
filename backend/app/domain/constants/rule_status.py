"""Remuneration rule status constants."""

from enum import StrEnum


class RuleStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUPERSEDED = "superseded"
