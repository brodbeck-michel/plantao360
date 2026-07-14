from enum import StrEnum


class BusinessRuleCode(StrEnum):
    RN_01_SHIFT_REQUIRES_DOCTOR = "RN_01"
    RN_02_SPLIT_MUST_CLOSE_PERIOD = "RN_02"
    RN_03_NO_OVERLAPPING = "RN_03"
    RN_04_EXTRA_REQUIRES_JUSTIFICATION = "RN_04"
    RN_05_CLOSED_PERIOD_IMMUTABLE = "RN_05"
    RN_06_DOCTOR_SOFT_DELETE = "RN_06"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def labels(cls) -> list[tuple[str, str]]:
        return [(item.value, item.name) for item in cls]
