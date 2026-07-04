"""
External Adapter — Notification Adapter

Este módulo contém o adaptador base para sistemas de notificação.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from ..contracts import (
    EmailData,
    EmailResult,
    NotificationData,
    NotificationResult,
    SMSData,
    SMSResult,
)


class NotificationAdapterBase:
    """Adaptador base para sistemas de notificação."""

    async def send_notification(self, notification: NotificationData) -> NotificationResult:
        """Enviar notificação."""
        raise NotImplementedError("Subclasses devem implementar send_notification")

    async def send_email(self, email: EmailData) -> EmailResult:
        """Enviar email."""
        raise NotImplementedError("Subclasses devem implementar send_email")

    async def send_sms(self, sms: SMSData) -> SMSResult:
        """Enviar SMS."""
        raise NotImplementedError("Subclasses devem implementar send_sms")
