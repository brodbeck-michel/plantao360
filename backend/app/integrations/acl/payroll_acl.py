"""
Anti-Corruption Layer — Payroll ACL

Este módulo traduz dados de sistemas de folha para o formato do domínio.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..contracts import (
    ExportResult,
    PayrollExportData,
    PayrollExternalStatus,
    PayrollImportData,
)
from ..contracts.payroll_contract import PayrollAdapter
from . import BaseACL


@dataclass(frozen=True)
class PayrollExport:
    """Modelo de domínio para exportação de folha."""

    payroll_id: str
    competency: str
    doctors: list[dict]
    total_amount: float
    export_date: "datetime"


class PayrollACL(BaseACL):
    """ACL para integração com sistemas de folha de pagamento."""

    def __init__(self, adapter: PayrollAdapter):
        self._adapter = adapter

    async def export_payroll(
        self, payroll_id: str, data: PayrollExportData
    ) -> ExportResult:
        """Exportar dados de folha para sistema externo."""
        return await self._adapter.export_payroll(payroll_id, data)

    async def import_payroll(self, file_path: str) -> PayrollImportData:
        """Importar dados de folha de sistema externo."""
        return await self._adapter.import_payroll(file_path)

    async def get_payroll_status(self, payroll_id: str) -> PayrollExternalStatus:
        """Obter status de folha em sistema externo."""
        return await self._adapter.get_payroll_status(payroll_id)

    def _to_domain(self, external_data: PayrollImportData) -> PayrollExport:
        """Traduz dados externos para formato do domínio."""
        return PayrollExport(
            payroll_id=external_data.payroll_id,
            competency="",
            doctors=[],
            total_amount=0.0,
            export_date=external_data.import_date,
        )

    def _to_external(self, domain_data: PayrollExport) -> PayrollExportData:
        """Traduz dados do domínio para formato externo."""
        return PayrollExportData(
            payroll_id=domain_data.payroll_id,
            competency=domain_data.competency,
            doctors=domain_data.doctors,
            total_amount=domain_data.total_amount,
            export_date=domain_data.export_date,
        )
