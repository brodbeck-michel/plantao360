"""Extra Create DTO."""

from pydantic import BaseModel, Field


class ExtraCreateDTO(BaseModel):
    shift_id: int = Field(..., description="ID do Plantão")
    doctor_id: int = Field(..., description="ID do Médico")
    duration_minutes: int = Field(..., gt=0, description="Duração em minutos")
    justification: str = Field(..., min_length=1, description="Justificativa do Extra")
