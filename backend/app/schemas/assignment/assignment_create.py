from typing import Optional
from pydantic import BaseModel, Field


class AssignmentCreateDTO(BaseModel):
    shift_id: int = Field(..., description="Shift ID")
    doctor_id: int = Field(..., description="Doctor ID")
    start_time: str = Field(..., description="Start time (HH:MM)")
    end_time: str = Field(..., description="End time (HH:MM)")
