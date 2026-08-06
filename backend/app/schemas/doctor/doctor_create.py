from datetime import date

from pydantic import BaseModel, Field, field_validator

from app.schemas.base.base_dto import BaseCreateDTO


class DoctorCreateDTO(BaseCreateDTO):
    name: str = Field(..., min_length=1, max_length=255, description="Nome completo do medico")
    crm: str = Field(..., min_length=1, max_length=20, description="Numero do CRM (4-10 digitos)")
    has_rqe: bool = Field(False, description="Possui RQE (Registro de Qualificacao de Especialista)")
    career_start_date: date = Field(..., description="Data de inicio de carreira")
    specialty: str = Field("Clinica Medica", max_length=100, description="Especialidade medica")
    phone: str | None = Field(None, max_length=20, description="Telefone de contato")
    email: str | None = Field(None, max_length=255, description="Email de contato")
    doctor_type: str = Field("plantonista", description="Tipo: plantonista, diarista, freelancer")

    @field_validator("career_start_date")
    @classmethod
    def _validate_career_start_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("career_start_date nao pode ser no futuro")
        return value
