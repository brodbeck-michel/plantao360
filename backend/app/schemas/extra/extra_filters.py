"""Extra Filter DTO."""

from pydantic import BaseModel, Field


class ExtraFilterDTO(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)
    shift_id: int | None = None
    doctor_id: int | None = None
    status: str | None = None
