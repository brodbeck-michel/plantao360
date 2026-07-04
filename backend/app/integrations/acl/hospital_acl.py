"""
Anti-Corruption Layer — Hospital ACL

Este módulo traduz dados de sistemas hospitalares para o formato do domínio.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..contracts import HospitalData, ScheduleData
from ..contracts.hospital_contract import HospitalAdapter
from . import BaseACL


@dataclass(frozen=True)
class Hospital:
    """Modelo de domínio para Hospital."""

    id: str
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[str] = None


class HospitalACL(BaseACL):
    """ACL para integração com sistemas hospitalares."""

    def __init__(self, adapter: HospitalAdapter):
        self._adapter = adapter

    async def get_hospital(self, hospital_id: str) -> Hospital:
        """Obter hospital e traduzir para formato do domínio."""
        external_data = await self._adapter.get_hospital(hospital_id)
        return self._to_domain(external_data)

    async def list_hospitals(self) -> list[Hospital]:
        """Listar hospitais e traduzir para formato do domínio."""
        external_list = await self._adapter.list_hospitals()
        return [self._to_domain(data) for data in external_list]

    async def get_hospital_schedule(
        self, hospital_id: str, schedule_date: "date"
    ) -> ScheduleData:
        """Obter agenda e traduzir para formato do domínio."""
        return await self._adapter.get_hospital_schedule(hospital_id, schedule_date)

    def _to_domain(self, external_data: HospitalData) -> Hospital:
        """Traduz dados externos para formato do domínio."""
        return Hospital(
            id=external_data.id,
            name=external_data.name,
            address=external_data.address,
            phone=external_data.phone,
            email=external_data.email,
        )

    def _to_external(self, domain_data: Hospital) -> HospitalData:
        """Traduz dados do domínio para formato externo."""
        return HospitalData(
            id=domain_data.id,
            name=domain_data.name,
            address=domain_data.address,
            phone=domain_data.phone,
            email=domain_data.email,
        )
