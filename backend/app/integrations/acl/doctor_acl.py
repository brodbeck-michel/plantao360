"""
Anti-Corruption Layer — Doctor ACL

Este módulo traduz dados de sistemas de médicos para o formato do domínio.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from dataclasses import dataclass

from ..contracts import CRMValidationResult, DoctorExternalData, SyncResult
from ..contracts.doctor_contract import DoctorAdapter
from . import BaseACL


@dataclass(frozen=True)
class DoctorExternal:
    """Modelo de domínio para dados externos de médico."""

    id: str
    name: str
    crm: str
    specialty: str
    email: str
    hospital_id: str


class DoctorACL(BaseACL):
    """ACL para integração com sistemas de gestão de médicos."""

    def __init__(self, adapter: DoctorAdapter):
        self._adapter = adapter

    async def sync_doctors(self) -> SyncResult:
        """Sincronizar médicos com sistema externo."""
        return await self._adapter.sync_doctors()

    async def get_doctor(self, doctor_id: str) -> DoctorExternal:
        """Obter dados de um médico de sistema externo."""
        external_data = await self._adapter.get_doctor(doctor_id)
        return self._to_domain(external_data)

    async def validate_crm(self, crm: str) -> CRMValidationResult:
        """Validar CRM em sistema externo."""
        return await self._adapter.validate_crm(crm)

    def _to_domain(self, external_data: DoctorExternalData) -> DoctorExternal:
        """Traduz dados externos para formato do domínio."""
        return DoctorExternal(
            id=external_data.id,
            name=external_data.name,
            crm=external_data.crm,
            specialty=external_data.specialty,
            email=external_data.email,
            hospital_id=external_data.hospital_id,
        )

    def _to_external(self, domain_data: DoctorExternal) -> DoctorExternalData:
        """Traduz dados do domínio para formato externo."""
        return DoctorExternalData(
            id=domain_data.id,
            name=domain_data.name,
            crm=domain_data.crm,
            specialty=domain_data.specialty,
            email=domain_data.email,
            hospital_id=domain_data.hospital_id,
        )
