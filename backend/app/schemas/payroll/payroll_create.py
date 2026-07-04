"""Payroll create DTO."""

from pydantic import BaseModel, Field


class PayrollCreateDTO(BaseModel):
    period_id: int = Field(..., description="Period ID to calculate payroll for")
    year_month: str = Field(..., min_length=6, max_length=6, description="Year-month format YYYYMM")
    created_by: str = Field(default="system", max_length=100)
