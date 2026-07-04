"""Snapshot status constants."""

from enum import StrEnum


class SnapshotStatus(StrEnum):
    ACTIVE = "active"
    INVALIDATED = "invalidated"
