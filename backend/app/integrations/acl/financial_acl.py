"""
Anti-Corruption Layer — Financial ACL

Este módulo traduz dados de sistemas financeiros para o formato do domínio.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import FinancialExportData, FinancialImportData, PaymentStatusData
from ..contracts.financial_contract import FinancialAdapter
from . import BaseACL


class FinancialACL(BaseACL):
    """ACL para integração com sistemas financeiros."""

    def __init__(self, adapter: FinancialAdapter):
        self._adapter = adapter

    async def export_financial(self, period_id: str) -> FinancialExportData:
        """Exportar dados financeiros para sistema externo."""
        return await self._adapter.export_financial(period_id)

    async def import_financial(self, file_path: str) -> FinancialImportData:
        """Importar dados financeiros de sistema externo."""
        return await self._adapter.import_financial(file_path)

    async def get_payment_status(self, doctor_id: str) -> PaymentStatusData:
        """Obter status de pagamento em sistema externo."""
        return await self._adapter.get_payment_status(doctor_id)

    def _to_domain(self, external_data: FinancialImportData) -> FinancialExportData:
        """Traduz dados externos para formato do domínio."""
        return FinancialExportData(
            period_id=external_data.period_id,
            doctors=external_data.doctors,
            total_amount=0.0,
            export_date=external_data.import_date,
        )

    def _to_external(self, domain_data: FinancialExportData) -> FinancialImportData:
        """Traduz dados do domínio para formato externo."""
        return FinancialImportData(
            period_id=domain_data.period_id,
            doctors=domain_data.doctors,
            import_date=domain_data.export_date,
        )
