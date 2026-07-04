from typing import Optional
from pydantic import BaseModel, Field


class AssignmentUpdateDTO(BaseModel):
    doctor_id: Optional[int] = Field(None, description="New doctor ID (for swap)")
    start_time: Optional[str] = Field(None, description="Start time (HH:MM)")
    end_time: Optional[str] = Field(None, description="End time (HH:MM)")
