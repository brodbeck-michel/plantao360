"""
External Adapter — Hospital Adapter

Este módulo contém o adaptador base para sistemas hospitalares.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from datetime import date

from ..contracts import HospitalData, ScheduleData


class HospitalAdapterBase:
    """Adaptador base para sistemas hospitalares."""

    async def get_hospital(self, hospital_id: str) -> HospitalData:
        """Obter dados de um hospital."""
        raise NotImplementedError("Subclasses devem implementar get_hospital")

    async def list_hospitals(self) -> list[HospitalData]:
        """Listar todos os hospitais."""
        raise NotImplementedError("Subclasses devem implementar list_hospitals")

    async def get_hospital_schedule(
        self, hospital_id: str, schedule_date: date
    ) -> ScheduleData:
        """Obter agenda de um hospital."""
        raise NotImplementedError("Subclasses devem implementar get_hospital_schedule")
