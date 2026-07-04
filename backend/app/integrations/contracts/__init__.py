"""
Integration Contracts — Plantão 360

Este módulo define os contratos de integração para sistemas externos.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


# ============================================================
# External Data Models (para comunicação com sistemas externos)
# ============================================================


@dataclass(frozen=True)
class HospitalData:
    id: str
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[str] = None


@dataclass(frozen=True)
class DoctorExternalData:
    id: str
    name: str
    crm: str
    specialty: str
    email: str
    hospital_id: str


@dataclass(frozen=True)
class ScheduleData:
    hospital_id: str
    date: date
    shifts: list[dict]


@dataclass(frozen=True)
class PayrollExportData:
    payroll_id: str
    competency: str
    doctors: list[dict]
    total_amount: float
    export_date: datetime


@dataclass(frozen=True)
class PayrollImportData:
    payroll_id: str
    status: str
    import_date: datetime


@dataclass(frozen=True)
class PayrollExternalStatus:
    payroll_id: str
    status: str
    last_updated: datetime


@dataclass(frozen=True)
class ExportResult:
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    export_date: datetime = None


@dataclass(frozen=True)
class SyncResult:
    success: bool
    synced_count: int = 0
    error_count: int = 0
    errors: list[str] = None


@dataclass(frozen=True)
class CRMValidationResult:
    valid: bool
    doctor_name: Optional[str] = None
    specialty: Optional[str] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class ScheduleExportData:
    period_id: str
    shifts: list[dict]
    export_date: datetime


@dataclass(frozen=True)
class ScheduleImportData:
    period_id: str
    shifts: list[dict]
    import_date: datetime


@dataclass(frozen=True)
class ConflictData:
    shift_id: str
    doctor_id: str
    conflict_type: str
    description: str


@dataclass(frozen=True)
class FinancialExportData:
    period_id: str
    doctors: list[dict]
    total_amount: float
    export_date: datetime


@dataclass(frozen=True)
class FinancialImportData:
    period_id: str
    doctors: list[dict]
    import_date: datetime


@dataclass(frozen=True)
class PaymentStatusData:
    doctor_id: str
    status: str
    last_updated: datetime


@dataclass(frozen=True)
class NotificationData:
    recipient_id: str
    recipient_type: str
    subject: str
    body: str
    notification_type: str


@dataclass(frozen=True)
class NotificationResult:
    success: bool
    notification_id: Optional[str] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class EmailData:
    to: str
    subject: str
    body: str
    is_html: bool = False


@dataclass(frozen=True)
class EmailResult:
    success: bool
    message_id: Optional[str] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class SMSData:
    phone_number: str
    message: str


@dataclass(frozen=True)
class SMSResult:
    success: bool
    message_id: Optional[str] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class ScheduleExportData:
    period_id: str
    shifts: list[dict]
    export_date: datetime


@dataclass(frozen=True)
class ScheduleImportData:
    period_id: str
    shifts: list[dict]
    import_date: datetime


@dataclass(frozen=True)
class ConflictData:
    shift_id: str
    doctor_id: str
    conflict_type: str
    description: str
