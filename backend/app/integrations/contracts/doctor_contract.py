"""
Integration Contracts — Doctor Adapter Protocol

Este módulo define o contrato para integração com sistemas de gestão de médicos.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from . import CRMValidationResult, DoctorExternalData, SyncResult


@runtime_checkable
class DoctorAdapter(Protocol):
    """Contrato para integração com sistemas de gestão de médicos."""

    async def sync_doctors(self) -> SyncResult:
        """Sincronizar médicos com sistema externo."""
        ...

    async def get_doctor(self, doctor_id: str) -> DoctorExternalData:
        """Obter dados de um médico de sistema externo."""
        ...

    async def validate_crm(self, crm: str) -> CRMValidationResult:
        """Validar CRM em sistema externo."""
        ...
