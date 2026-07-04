from dataclasses import dataclass


@dataclass
class SortingQuery:
    field: str = "id"
    direction: str = "asc"

    def __post_init__(self) -> None:
        if self.direction not in ("asc", "desc"):
            self.direction = "asc"
