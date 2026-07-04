"""
External Adapter — Senior Adapter (Placeholder)

Este módulo contém o adaptador para o Senior (ERP de Folha).
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
Status: FUTURO (não implementado)
"""

from __future__ import annotations

from ..contracts import (
    ExportResult,
    PayrollExportData,
    PayrollExternalStatus,
    PayrollImportData,
)
from ..contracts.payroll_contract import PayrollAdapter


class SeniorAdapter(PayrollAdapter):
    """Adaptador para o Senior (ERP de Folha).

    Status: FUTURO
    Implementação pendente de definição de necessidade real.
    """

    async def export_payroll(
        self, payroll_id: str, data: PayrollExportData
    ) -> ExportResult:
        """Exportar dados de folha via Senior."""
        raise NotImplementedError("SeniorAdapter não implementado")

    async def import_payroll(self, file_path: str) -> PayrollImportData:
        """Importar dados de folha via Senior."""
        raise NotImplementedError("SeniorAdapter não implementado")

    async def get_payroll_status(self, payroll_id: str) -> PayrollExternalStatus:
        """Obter status de folha via Senior."""
        raise NotImplementedError("SeniorAdapter não implementado")
