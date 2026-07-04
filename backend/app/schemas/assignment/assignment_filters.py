from typing import Optional
from pydantic import BaseModel, Field, model_validator


class AssignmentFilterDTO(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Items per page")
    shift_id: Optional[int] = Field(None, description="Filter by shift ID")
    doctor_id: Optional[int] = Field(None, description="Filter by doctor ID")
    status: Optional[str] = Field(None, description="Filter by status")
    sort_by: str = Field("id", description="Sort field")
    sort_direction: str = Field("asc", description="Sort direction: asc or desc")

    @model_validator(mode="after")
    def _validate_sort(self) -> "AssignmentFilterDTO":
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "shift_id", "doctor_id", "status", "created_at"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
        return self

    def to_filters(self) -> dict:
        filters = {}
        if self.shift_id is not None:
            filters["shift_id"] = self.shift_id
        if self.doctor_id is not None:
            filters["doctor_id"] = self.doctor_id
        if self.status is not None:
            filters["status"] = self.status
        return filters
