from pydantic import BaseModel, Field

from app.schemas.base.base_dto import BaseUpdateDTO


class DoctorUpdateDTO(BaseUpdateDTO):
    name: str | None = Field(None, min_length=1, max_length=255, description="Nome completo do medico")
    crm: str | None = Field(None, min_length=1, max_length=20, description="Numero do CRM (4-10 digitos)")
    hour_rate: float | None = Field(None, gt=0, description="Valor da hora em R$")
    specialty: str | None = Field(None, max_length=100, description="Especialidade medica")
    phone: str | None = Field(None, max_length=20, description="Telefone de contato")
    email: str | None = Field(None, max_length=255, description="Email de contato")
    doctor_type: str | None = Field(None, description="Tipo: plantonista, diarista, freelancer")
    active: bool | None = Field(None, description="Status ativo/inativo")
