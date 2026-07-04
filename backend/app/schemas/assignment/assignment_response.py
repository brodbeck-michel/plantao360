from datetime import time
from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator


class AssignmentResponseDTO(BaseModel):
    id: int = Field(..., description="Assignment ID")
    shift_id: int = Field(..., description="Shift ID")
    doctor_id: int = Field(..., description="Doctor ID")
    start_time: Any = Field(..., description="Start time")
    end_time: Any = Field(..., description="End time")
    status: str = Field(..., description="Assignment status")
    duration_minutes: Optional[int] = Field(None, description="Duration in minutes")

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def serialize_time(cls, v: Any) -> str:
        if isinstance(v, time):
            return v.strftime("%H:%M")
        return str(v)

    model_config = {"from_attributes": True}
