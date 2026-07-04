from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class ShiftResponseDTO(BaseModel):
    id: int = Field(..., description="Shift ID")
    period_id: int = Field(..., description="Period ID")
    shift_date: date = Field(..., description="Shift date")
    shift_type: str = Field(..., description="Shift type")
    status: str = Field(..., description="Shift status")
    scheduled_start: Optional[datetime] = Field(None, description="Scheduled start")
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end")
    actual_start: Optional[datetime] = Field(None, description="Actual start")
    actual_end: Optional[datetime] = Field(None, description="Actual end")
    total_duration_minutes: Optional[int] = Field(None, description="Total duration in minutes")
    doctor_count: Optional[int] = Field(None, description="Number of doctors assigned")
    created_at: Optional[datetime] = Field(None, description="Created at")
    updated_at: Optional[datetime] = Field(None, description="Updated at")

    model_config = {"from_attributes": True}
