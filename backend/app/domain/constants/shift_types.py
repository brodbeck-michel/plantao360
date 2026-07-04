from enum import StrEnum


class ShiftType(StrEnum):
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    R1 = "R1"
    R2 = "R2"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.name) for item in cls]
