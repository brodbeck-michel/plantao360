from typing import Protocol, Optional

from app.models.doctor import Doctor


class DoctorRepositoryInterface(Protocol):
    def get_by_id(self, id: int) -> Optional[Doctor]: ...

    def get_by_crm(self, crm: str) -> Optional[Doctor]: ...

    def exists_by_crm(self, crm: str, exclude_id: int | None = None) -> bool: ...

    def list(self, skip: int = 0, limit: int = 100) -> list[Doctor]: ...

    def search(
        self,
        name: str | None = None,
        crm: str | None = None,
        active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
    ) -> list[Doctor]: ...

    def count_filtered(
        self,
        name: str | None = None,
        crm: str | None = None,
        active: bool | None = None,
    ) -> int: ...

    def create(self, entity: Doctor) -> Doctor: ...

    def update(self, entity: Doctor) -> Doctor: ...

    def soft_delete(self, id: int) -> bool: ...

    def exists(self, id: int) -> bool: ...

    def count(self) -> int: ...
