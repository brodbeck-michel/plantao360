"""
External Adapter — Financial Adapter

Este módulo contém o adaptador base para sistemas financeiros.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import FinancialExportData, FinancialImportData, PaymentStatusData


class FinancialAdapterBase:
    """Adaptador base para sistemas financeiros."""

    async def export_financial(self, period_id: str) -> FinancialExportData:
        """Exportar dados financeiros para sistema externo."""
        raise NotImplementedError("Subclasses devem implementar export_financial")

    async def import_financial(self, file_path: str) -> FinancialImportData:
        """Importar dados financeiros de sistema externo."""
        raise NotImplementedError("Subclasses devem implementar import_financial")

    async def get_payment_status(self, doctor_id: str) -> PaymentStatusData:
        """Obter status de pagamento em sistema externo."""
        raise NotImplementedError("Subclasses devem implementar get_payment_status")
