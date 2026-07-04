"""Payroll Reopen DTO."""

from pydantic import BaseModel, Field


class PayrollReopenDTO(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500, description="Reason for reopening")
    reopened_by: str = Field(default="system", max_length=100)
