from pydantic import Field

from app.schemas.base.base_dto import BaseCreateDTO


class PeriodCreateDTO(BaseCreateDTO):
    year: int = Field(..., ge=2000, le=2100, description="Ano do periodo (2000-2100)")
    month: int = Field(..., ge=1, le=12, description="Mes do periodo (1-12)")
