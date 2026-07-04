"""
Integration Contracts — Hospital Adapter Protocol

Este módulo define o contrato para integração com sistemas hospitalares.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from . import HospitalData, ScheduleData


@runtime_checkable
class HospitalAdapter(Protocol):
    """Contrato para integração com sistemas hospitalares."""

    async def get_hospital(self, hospital_id: str) -> HospitalData:
        """Obter dados de um hospital."""
        ...

    async def list_hospitals(self) -> list[HospitalData]:
        """Listar todos os hospitais."""
        ...

    async def get_hospital_schedule(
        self, hospital_id: str, date: "date"
    ) -> ScheduleData:
        """Obter agenda de um hospital."""
        ...
