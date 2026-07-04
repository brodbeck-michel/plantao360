from dataclasses import dataclass


@dataclass
class PaginationQuery:
    page: int = 1
    size: int = 20

    def __post_init__(self) -> None:
        if self.page < 1:
            self.page = 1
        if self.size < 1:
            self.size = 1
        if self.size > 100:
            self.size = 100

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size
