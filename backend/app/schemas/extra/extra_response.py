"""Extra Response DTO."""

from datetime import datetime
from pydantic import BaseModel


class ExtraResponseDTO(BaseModel):
    id: int
    shift_id: int
    doctor_id: int
    duration_minutes: int
    justification: str
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
