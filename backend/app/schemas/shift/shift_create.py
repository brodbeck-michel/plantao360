from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class ShiftCreateDTO(BaseModel):
    period_id: int = Field(..., description="Period ID")
    shift_date: date = Field(..., description="Shift date")
    shift_type: str = Field(..., description="Shift type: T1, T2, T3, R1, R2")
    scheduled_start: Optional[datetime] = Field(None, description="Scheduled start time")
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end time")
    doctor_count: Optional[int] = Field(None, ge=0, description="Number of doctors assigned")
    total_duration_minutes: Optional[int] = Field(None, ge=0, description="Total duration in minutes")
