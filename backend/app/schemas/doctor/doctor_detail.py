from datetime import date

from pydantic import BaseModel, Field

from app.schemas.base.base_dto import BaseResponseDTO


class DoctorDetailDTO(BaseResponseDTO):
    name: str = Field(..., description="Nome completo do médico")
    crm: str = Field(..., description="Número do CRM")
    has_rqe: bool = Field(..., description="Possui RQE")
    career_start_date: date | None = Field(None, description="Data de inicio de carreira")
    hour_rate: float = Field(..., description="Valor da hora em R$ (calculado)")
    hour_rate_tier: str = Field(..., description="Faixa de valorizacao (ex: M-3, E-2)")
    active: bool = Field(..., description="Status ativo/inativo")
    total_shifts: int = Field(0, description="Total de plantões realizados")
    total_extras: int = Field(0, description="Total de plantões extras")

    model_config = {"from_attributes": True}
