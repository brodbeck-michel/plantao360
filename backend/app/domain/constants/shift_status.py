from enum import StrEnum


class ShiftStatus(StrEnum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.name) for item in cls]
