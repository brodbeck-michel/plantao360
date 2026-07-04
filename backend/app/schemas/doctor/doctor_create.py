from pydantic import BaseModel, Field

from app.schemas.base.base_dto import BaseCreateDTO


class DoctorCreateDTO(BaseCreateDTO):
    name: str = Field(..., min_length=1, max_length=255, description="Nome completo do medico")
    crm: str = Field(..., min_length=1, max_length=20, description="Numero do CRM (4-10 digitos)")
    hour_rate: float = Field(..., gt=0, description="Valor da hora em R$")
    specialty: str = Field("Clinica Medica", max_length=100, description="Especialidade medica")
    phone: str | None = Field(None, max_length=20, description="Telefone de contato")
    email: str | None = Field(None, max_length=255, description="Email de contato")
    doctor_type: str = Field("plantonista", description="Tipo: plantonista, diarista, freelancer")
