"""
Anti-Corruption Layer — Notification ACL

Este módulo traduz dados de sistemas de notificação para o formato do domínio.
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
from ..contracts.notification_contract import NotificationAdapter
from . import BaseACL


class NotificationACL(BaseACL):
    """ACL para integração com sistemas de notificação."""

    def __init__(self, adapter: NotificationAdapter):
        self._adapter = adapter

    async def send_notification(self, notification: NotificationData) -> NotificationResult:
        """Enviar notificação."""
        return await self._adapter.send_notification(notification)

    async def send_email(self, email: EmailData) -> EmailResult:
        """Enviar email."""
        return await self._adapter.send_email(email)

    async def send_sms(self, sms: SMSData) -> SMSResult:
        """Enviar SMS."""
        return await self._adapter.send_sms(sms)

    def _to_domain(self, external_data: NotificationResult) -> NotificationData:
        """Traduz dados externos para formato do domínio."""
        return NotificationData(
            recipient_id="",
            recipient_type="",
            subject="",
            body="",
            notification_type="",
        )

    def _to_external(self, domain_data: NotificationData) -> NotificationResult:
        """Traduz dados do domínio para formato externo."""
        return NotificationResult(
            success=True,
            notification_id=None,
            error_message=None,
        )
