"""
External Adapter — Doctor Adapter

Este módulo contém o adaptador base para sistemas de gestão de médicos.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import CRMValidationResult, DoctorExternalData, SyncResult


class DoctorAdapterBase:
    """Adaptador base para sistemas de gestão de médicos."""

    async def sync_doctors(self) -> SyncResult:
        """Sincronizar médicos com sistema externo."""
        raise NotImplementedError("Subclasses devem implementar sync_doctors")

    async def get_doctor(self, doctor_id: str) -> DoctorExternalData:
        """Obter dados de um médico de sistema externo."""
        raise NotImplementedError("Subclasses devem implementar get_doctor")

    async def validate_crm(self, crm: str) -> CRMValidationResult:
        """Validar CRM em sistema externo."""
        raise NotImplementedError("Subclasses devem implementar validate_crm")
