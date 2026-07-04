from pydantic import BaseModel, Field


class DoctorSummaryDTO(BaseModel):
    id: int = Field(..., description="ID do médico")
    name: str = Field(..., description="Nome completo do médico")
    crm: str = Field(..., description="Número do CRM")
    active: bool = Field(..., description="Status ativo/inativo")

    model_config = {"from_attributes": True}
