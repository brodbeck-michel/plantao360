from datetime import datetime
from typing import Optional

from pydantic import Field, computed_field

from app.schemas.base.base_dto import BaseResponseDTO
from app.domain.constants.competency_dates import get_competency_dates


class PeriodResponseDTO(BaseResponseDTO):
    year: int = Field(..., description="Ano do periodo")
    month: int = Field(..., description="Mes do periodo")
    status: str = Field(..., description="Status do periodo (draft/closed/paid)")
    created_at: Optional[datetime] = Field(None, description="Data de criacao")
    updated_at: Optional[datetime] = Field(None, description="Data de atualizacao")

    @computed_field
    @property
    def start_date(self) -> str:
        start, _ = get_competency_dates(self.year, self.month)
        return start.isoformat()

    @computed_field
    @property
    def end_date(self) -> str:
        _, end = get_competency_dates(self.year, self.month)
        return end.isoformat()

    model_config = {"from_attributes": True}
