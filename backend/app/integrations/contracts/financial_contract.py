"""
Integration Contracts — Financial Adapter Protocol

Este módulo define o contrato para integração com sistemas financeiros.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from . import ExportResult, FinancialExportData, FinancialImportData, PaymentStatusData


@runtime_checkable
class FinancialAdapter(Protocol):
    """Contrato para integração com sistemas financeiros."""

    async def export_financial(self, period_id: str) -> FinancialExportData:
        """Exportar dados financeiros para sistema externo."""
        ...

    async def import_financial(self, file_path: str) -> FinancialImportData:
        """Importar dados financeiros de sistema externo."""
        ...

    async def get_payment_status(self, doctor_id: str) -> PaymentStatusData:
        """Obter status de pagamento em sistema externo."""
        ...
