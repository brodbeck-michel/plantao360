"""
External Adapter — Payroll Adapter

Este módulo contém o adaptador base para sistemas de folha de pagamento.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import (
    ExportResult,
    PayrollExportData,
    PayrollExternalStatus,
    PayrollImportData,
)


class PayrollAdapterBase:
    """Adaptador base para sistemas de folha de pagamento."""

    async def export_payroll(
        self, payroll_id: str, data: PayrollExportData
    ) -> ExportResult:
        """Exportar dados de folha para sistema externo."""
        raise NotImplementedError("Subclasses devem implementar export_payroll")

    async def import_payroll(self, file_path: str) -> PayrollImportData:
        """Importar dados de folha de sistema externo."""
        raise NotImplementedError("Subclasses devem implementar import_payroll")

    async def get_payroll_status(self, payroll_id: str) -> PayrollExternalStatus:
        """Obter status de folha em sistema externo."""
        raise NotImplementedError("Subclasses devem implementar get_payroll_status")
