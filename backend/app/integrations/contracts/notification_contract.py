"""
Integration Contracts — Notification Adapter Protocol

Este módulo define o contrato para integração com sistemas de notificação.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from . import EmailData, EmailResult, NotificationData, NotificationResult, SMSData, SMSResult


@runtime_checkable
class NotificationAdapter(Protocol):
    """Contrato para integração com sistemas de notificação."""

    async def send_notification(self, notification: NotificationData) -> NotificationResult:
        """Enviar notificação."""
        ...

    async def send_email(self, email: EmailData) -> EmailResult:
        """Enviar email."""
        ...

    async def send_sms(self, sms: SMSData) -> SMSResult:
        """Enviar SMS."""
        ...
