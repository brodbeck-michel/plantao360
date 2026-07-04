from enum import StrEnum


class AssignmentStatus(StrEnum):
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.name) for item in cls]
