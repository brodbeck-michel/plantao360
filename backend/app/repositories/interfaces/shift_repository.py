from typing import Protocol, Optional

from app.models.shift import Shift


class ShiftRepositoryInterface(Protocol):
    def get_by_id(self, id: int) -> Optional[Shift]: ...

    def list(self, skip: int = 0, limit: int = 100) -> list[Shift]: ...

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
        **filters,
    ) -> list[Shift]: ...

    def count_filtered(self, **filters) -> int: ...

    def create(self, entity: Shift) -> Shift: ...

    def update(self, entity: Shift) -> Shift: ...

    def soft_delete(self, id: int) -> bool: ...

    def exists(self, id: int) -> bool: ...

    def count(self) -> int: ...
