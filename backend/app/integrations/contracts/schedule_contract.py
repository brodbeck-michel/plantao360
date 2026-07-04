"""
Integration Contracts — Schedule Adapter Protocol

Este módulo define o contrato para integração com sistemas de agenda.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from . import ConflictData, ExportResult, ScheduleExportData, ScheduleImportData


@runtime_checkable
class ScheduleAdapter(Protocol):
    """Contrato para integração com sistemas de agenda."""

    async def export_schedule(self, period_id: str) -> ScheduleExportData:
        """Exportar agenda para sistema externo."""
        ...

    async def import_schedule(self, file_path: str) -> ScheduleImportData:
        """Importar agenda de sistema externo."""
        ...

    async def get_schedule_conflicts(self, period_id: str) -> list[ConflictData]:
        """Obter conflitos de agenda em sistema externo."""
        ...
