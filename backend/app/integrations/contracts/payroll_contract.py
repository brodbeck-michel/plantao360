"""
Integration Contracts — Payroll Adapter Protocol

Este módulo define o contrato para integração com sistemas de folha de pagamento.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from . import (
    ExportResult,
    PayrollExportData,
    PayrollExternalStatus,
    PayrollImportData,
)


@runtime_checkable
class PayrollAdapter(Protocol):
    """Contrato para integração com sistemas de folha de pagamento."""

    async def export_payroll(
        self, payroll_id: str, data: PayrollExportData
    ) -> ExportResult:
        """Exportar dados de folha para sistema externo."""
        ...

    async def import_payroll(self, file_path: str) -> PayrollImportData:
        """Importar dados de folha de sistema externo."""
        ...

    async def get_payroll_status(self, payroll_id: str) -> PayrollExternalStatus:
        """Obter status de folha em sistema externo."""
        ...
