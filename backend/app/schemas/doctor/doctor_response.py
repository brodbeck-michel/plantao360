from pydantic import BaseModel, Field

from app.schemas.base.base_dto import BaseResponseDTO


class DoctorResponseDTO(BaseResponseDTO):
    name: str = Field(..., description="Nome completo do medico")
    crm: str = Field(..., description="Numero do CRM")
    hour_rate: float = Field(..., description="Valor da hora em R$")
    specialty: str = Field(..., description="Especialidade medica")
    phone: str | None = Field(None, description="Telefone de contato")
    email: str | None = Field(None, description="Email de contato")
    doctor_type: str = Field(..., description="Tipo do medico")
    active: bool = Field(..., description="Status ativo/inativo")

    model_config = {"from_attributes": True}
