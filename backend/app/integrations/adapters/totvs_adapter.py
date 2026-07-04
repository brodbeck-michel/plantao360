"""
External Adapter — TOTVS Adapter (Placeholder)

Este módulo contém o adaptador para o TOTVS (ERP).
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
Status: FUTURO (não implementado)
"""

from __future__ import annotations

from ..contracts import FinancialExportData, FinancialImportData, PaymentStatusData
from ..contracts.financial_contract import FinancialAdapter


class TOTVSAdapter(FinancialAdapter):
    """Adaptador para o TOTVS (ERP).

    Status: FUTURO
    Implementação pendente de definição de necessidade real.
    """

    async def export_financial(self, period_id: str) -> FinancialExportData:
        """Exportar dados financeiros via TOTVS."""
        raise NotImplementedError("TOTVSAdapter não implementado")

    async def import_financial(self, file_path: str) -> FinancialImportData:
        """Importar dados financeiros via TOTVS."""
        raise NotImplementedError("TOTVSAdapter não implementado")

    async def get_payment_status(self, doctor_id: str) -> PaymentStatusData:
        """Obter status de pagamento via TOTVS."""
        raise NotImplementedError("TOTVSAdapter não implementado")
