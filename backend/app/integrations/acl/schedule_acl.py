"""
Anti-Corruption Layer — Schedule ACL

Este módulo traduz dados de sistemas de agenda para o formato do domínio.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import ConflictData, ScheduleExportData, ScheduleImportData
from ..contracts.schedule_contract import ScheduleAdapter
from . import BaseACL


class ScheduleACL(BaseACL):
    """ACL para integração com sistemas de agenda."""

    def __init__(self, adapter: ScheduleAdapter):
        self._adapter = adapter

    async def export_schedule(self, period_id: str) -> ScheduleExportData:
        """Exportar agenda para sistema externo."""
        return await self._adapter.export_schedule(period_id)

    async def import_schedule(self, file_path: str) -> ScheduleImportData:
        """Importar agenda de sistema externo."""
        return await self._adapter.import_schedule(file_path)

    async def get_schedule_conflicts(self, period_id: str) -> list[ConflictData]:
        """Obter conflitos de agenda em sistema externo."""
        return await self._adapter.get_schedule_conflicts(period_id)

    def _to_domain(self, external_data: ScheduleImportData) -> ScheduleExportData:
        """Traduz dados externos para formato do domínio."""
        return ScheduleExportData(
            period_id=external_data.period_id,
            shifts=external_data.shifts,
            export_date=external_data.import_date,
        )

    def _to_external(self, domain_data: ScheduleExportData) -> ScheduleImportData:
        """Traduz dados do domínio para formato externo."""
        return ScheduleImportData(
            period_id=domain_data.period_id,
            shifts=domain_data.shifts,
            import_date=domain_data.export_date,
        )
