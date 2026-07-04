from dataclasses import dataclass


@dataclass
class SortField:
    field: str
    direction: str = "asc"

    def __post_init__(self) -> None:
        if self.direction not in ("asc", "desc"):
            self.direction = "asc"
