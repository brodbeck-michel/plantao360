from typing import Optional
from pydantic import BaseModel, Field


class ShiftQueryDTO(BaseModel):
    search: Optional[str] = Field(None, description="General search")
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Items per page")
    sort_by: str = Field("id", description="Sort field")
    sort_direction: str = Field("asc", description="Sort direction: asc or desc")

    def __post_init__(self) -> None:
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "shift_date", "shift_type", "status", "period_id"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
