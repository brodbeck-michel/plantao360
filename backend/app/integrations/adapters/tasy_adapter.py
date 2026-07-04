"""
External Adapter — Tasy Adapter (Placeholder)

Este módulo contém o adaptador para o Tasy (ERP Hospitalar).
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
Status: FUTURO (não implementado)
"""

from __future__ import annotations

from ..contracts import HospitalData, ScheduleData
from .hospital_adapter import HospitalAdapterBase


class TasyAdapter(HospitalAdapterBase):
    """Adaptador para o Tasy (ERP Hospitalar).

    Status: FUTURO
    Implementação pendente de definição de necessidade real.
    """

    async def get_hospital(self, hospital_id: str) -> HospitalData:
        """Obter dados de um hospital via Tasy."""
        raise NotImplementedError("TasyAdapter não implementado")

    async def list_hospitals(self) -> list[HospitalData]:
        """Listar hospitais via Tasy."""
        raise NotImplementedError("TasyAdapter não implementado")

    async def get_hospital_schedule(
        self, hospital_id: str, schedule_date: "date"
    ) -> ScheduleData:
        """Obter agenda via Tasy."""
        raise NotImplementedError("TasyAdapter não implementado")
