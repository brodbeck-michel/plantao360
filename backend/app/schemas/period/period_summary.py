from pydantic import BaseModel, Field


class PeriodSummaryDTO(BaseModel):
    id: int = Field(..., description="ID do periodo")
    year: int = Field(..., description="Ano do periodo")
    month: int = Field(..., description="Mes do periodo")
    status: str = Field(..., description="Status do periodo")

    model_config = {"from_attributes": True}
