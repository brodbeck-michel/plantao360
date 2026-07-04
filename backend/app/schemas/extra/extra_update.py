"""Extra Update DTO."""

from pydantic import BaseModel, Field


class ExtraUpdateDTO(BaseModel):
    duration_minutes: int | None = Field(None, gt=0, description="Duração em minutos")
    justification: str | None = Field(None, min_length=1, description="Justificativa")
