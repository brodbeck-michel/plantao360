from dataclasses import dataclass


@dataclass(frozen=True)
class ShiftReference:
    shift_id: int
    shift_date: str = ""
    shift_type: str = ""

    def __post_init__(self) -> None:
        if self.shift_id <= 0:
            raise ValueError(f"Invalid shift_id: {self.shift_id}")
