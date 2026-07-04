from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: list[T] = field(default_factory=list)
    page: int = 1
    size: int = 20
    total: int = 0

    @property
    def pages(self) -> int:
        if self.size == 0:
            return 0
        return (self.total + self.size - 1) // self.size

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "page": self.page,
            "size": self.size,
            "total": self.total,
            "pages": self.pages,
        }
