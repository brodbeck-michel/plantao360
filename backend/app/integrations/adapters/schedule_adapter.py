"""
External Adapter — Schedule Adapter

Este módulo contém o adaptador base para sistemas de agenda.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import ConflictData, ScheduleExportData, ScheduleImportData


class ScheduleAdapterBase:
    """Adaptador base para sistemas de agenda."""

    async def export_schedule(self, period_id: str) -> ScheduleExportData:
        """Exportar agenda para sistema externo."""
        raise NotImplementedError("Subclasses devem implementar export_schedule")

    async def import_schedule(self, file_path: str) -> ScheduleImportData:
        """Importar agenda de sistema externo."""
        raise NotImplementedError("Subclasses devem implementar import_schedule")

    async def get_schedule_conflicts(self, period_id: str) -> list[ConflictData]:
        """Obter conflitos de agenda em sistema externo."""
        raise NotImplementedError("Subclasses devem implementar get_schedule_conflicts")
