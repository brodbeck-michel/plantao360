from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class ShiftFilterDTO(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Items per page")
    period_id: Optional[int] = Field(None, description="Filter by period ID")
    shift_date: Optional[date] = Field(None, description="Filter by shift date")
    shift_type: Optional[str] = Field(None, description="Filter by shift type")
    status: Optional[str] = Field(None, description="Filter by status")
    sort_by: str = Field("id", description="Sort field")
    sort_direction: str = Field("asc", description="Sort direction: asc or desc")

    @model_validator(mode="after")
    def _validate_sort(self) -> "ShiftFilterDTO":
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "shift_date", "shift_type", "status", "period_id", "created_at"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
        return self

    def to_filters(self) -> dict:
        filters = {}
        if self.period_id is not None:
            filters["period_id"] = self.period_id
        if self.shift_date is not None:
            filters["shift_date"] = self.shift_date
        if self.shift_type is not None:
            filters["shift_type"] = self.shift_type
        if self.status is not None:
            filters["status"] = self.status
        return filters
