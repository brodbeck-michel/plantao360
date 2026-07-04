"""Payroll response DTO."""

from datetime import datetime
from pydantic import BaseModel, Field


class PayrollVersionDTO(BaseModel):
    version_number: int
    created_at: datetime
    total_facts: int
    total_value: float
    total_doctors: int
    rules_count: int
    created_by: str
    reopen_reason: str | None = None


class PayrollSealDTO(BaseModel):
    sealed_at: datetime
    sealed_by: str
    version_number: int
    total_value: float
    total_doctors: int
    total_facts: int
    rules_count: int


class PayrollExplanationDTO(BaseModel):
    created_at: datetime
    steps_count: int
    total_value: float
    total_doctors: int
    total_facts: int


class PayrollAuditEntryDTO(BaseModel):
    timestamp: datetime
    action: str
    performed_by: str
    previous_status: str
    new_status: str
    details: str


class PayrollAuditDTO(BaseModel):
    entries_count: int
    entries: list[PayrollAuditEntryDTO]


class PayrollResponseDTO(BaseModel):
    id: int
    period_id: int
    year_month: str
    status: str
    current_version: int
    created_by: str
    created_at: datetime
    updated_at: datetime
    reopen_count: int
    reopen_reason: str | None = None
    total_value: float = 0.0
    seal: PayrollSealDTO | None = None
    explanation: PayrollExplanationDTO | None = None
    audit: PayrollAuditDTO | None = None
    versions: list[PayrollVersionDTO] = []

    model_config = {"from_attributes": True}
