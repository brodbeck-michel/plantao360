from enum import StrEnum


class PeriodStatus(StrEnum):
    DRAFT = "draft"
    CLOSED = "closed"
    PAID = "paid"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.name) for item in cls]
