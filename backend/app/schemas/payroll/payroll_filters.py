"""Payroll filters DTO."""

from pydantic import BaseModel, Field


class PayrollFilterDTO(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    period_id: int | None = None
    year_month: str | None = None
    status: str | None = None
    sort_by: str = Field(default="created_at")
    sort_direction: str = Field(default="desc")
