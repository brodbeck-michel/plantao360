from datetime import date
from pydantic import BaseModel, Field


class ShiftSummaryDTO(BaseModel):
    id: int = Field(..., description="Shift ID")
    shift_date: date = Field(..., description="Shift date")
    shift_type: str = Field(..., description="Shift type")
    status: str = Field(..., description="Shift status")

    model_config = {"from_attributes": True}
