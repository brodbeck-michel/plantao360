from datetime import date

from pydantic import BaseModel, Field, field_validator

from app.schemas.base.base_dto import BaseUpdateDTO


class DoctorUpdateDTO(BaseUpdateDTO):
    name: str | None = Field(None, min_length=1, max_length=255, description="Nome completo do medico")
    crm: str | None = Field(None, min_length=1, max_length=20, description="Numero do CRM (4-10 digitos)")
    has_rqe: bool | None = Field(None, description="Possui RQE (Registro de Qualificacao de Especialista)")
    career_start_date: date | None = Field(None, description="Data de inicio de carreira")
    specialty: str | None = Field(None, max_length=100, description="Especialidade medica")
    phone: str | None = Field(None, max_length=20, description="Telefone de contato")
    email: str | None = Field(None, max_length=255, description="Email de contato")
    doctor_type: str | None = Field(None, description="Tipo: plantonista, diarista, freelancer")
    active: bool | None = Field(None, description="Status ativo/inativo")

    @field_validator("career_start_date")
    @classmethod
    def _validate_career_start_date(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("career_start_date nao pode ser no futuro")
        return value
