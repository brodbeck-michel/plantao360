from typing import Protocol, Optional

from app.models.shift_part import ShiftPart


class ShiftPartRepositoryInterface(Protocol):
    def get_by_id(self, id: int) -> Optional[ShiftPart]: ...

    def list(self, skip: int = 0, limit: int = 100) -> list[ShiftPart]: ...

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
        **filters,
    ) -> list[ShiftPart]: ...

    def count_filtered(self, **filters) -> int: ...

    def create(self, entity: ShiftPart) -> ShiftPart: ...

    def update(self, entity: ShiftPart) -> ShiftPart: ...

    def exists(self, id: int) -> bool: ...

    def count(self) -> int: ...

    def find_overlapping(
        self, doctor_id: int, start_time, end_time, exclude_id: Optional[int] = None
    ) -> list[ShiftPart]: ...

    def find_conflicting_shifts(
        self, doctor_id: int, shift_date, exclude_id: Optional[int] = None
    ) -> list[ShiftPart]: ...
