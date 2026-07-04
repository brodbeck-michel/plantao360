from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.domain.constants.shift_status import ShiftStatus


class ShiftUpdateDTO(BaseModel):
    shift_date: Optional[date] = Field(None, description="Shift date")
    shift_type: Optional[str] = Field(None, description="Shift type: T1, T2, T3, R1, R2")
    scheduled_start: Optional[datetime] = Field(None, description="Scheduled start time")
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end time")
    doctor_count: Optional[int] = Field(None, ge=0, description="Number of doctors assigned")
    total_duration_minutes: Optional[int] = Field(None, ge=0, description="Total duration in minutes")
    status: Optional[str] = Field(None, description="Shift status")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None and v not in ShiftStatus.values():
            raise ValueError(f"Invalid status: {v}. Must be one of: {', '.join(ShiftStatus.values())}")
        return v
