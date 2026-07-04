"""
External Adapter — SAP Adapter (Placeholder)

Este módulo contém o adaptador para o SAP (ERP).
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
Status: FUTURO (não implementado)
"""

from __future__ import annotations

from ..contracts import FinancialExportData, FinancialImportData, PaymentStatusData
from ..contracts.financial_contract import FinancialAdapter


class SAPAdapter(FinancialAdapter):
    """Adaptador para o SAP (ERP).

    Status: FUTURO
    Implementação pendente de definição de necessidade real.
    """

    async def export_financial(self, period_id: str) -> FinancialExportData:
        """Exportar dados financeiros via SAP."""
        raise NotImplementedError("SAPAdapter não implementado")

    async def import_financial(self, file_path: str) -> FinancialImportData:
        """Importar dados financeiros via SAP."""
        raise NotImplementedError("SAPAdapter não implementado")

    async def get_payment_status(self, doctor_id: str) -> PaymentStatusData:
        """Obter status de pagamento via SAP."""
        raise NotImplementedError("SAPAdapter não implementado")
