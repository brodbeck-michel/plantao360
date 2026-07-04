"""
Tests — Integration Architecture — Plantão 360

Testes para a arquitetura de integração, ACL e adaptadores.
Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

import pytest
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from unittest.mock import AsyncMock, MagicMock

from app.integrations.contracts import (
    CRMValidationResult,
    DoctorExternalData,
    EmailData,
    EmailResult,
    ExportResult,
    FinancialExportData,
    FinancialImportData,
    HospitalData,
    NotificationData,
    NotificationResult,
    PaymentStatusData,
    PayrollExportData,
    PayrollExternalStatus,
    PayrollImportData,
    SMSData,
    SMSResult,
    ScheduleData,
    ScheduleExportData,
    ScheduleImportData,
    SyncResult,
    ConflictData,
)
from app.integrations.contracts.hospital_contract import HospitalAdapter
from app.integrations.contracts.payroll_contract import PayrollAdapter
from app.integrations.contracts.doctor_contract import DoctorAdapter
from app.integrations.contracts.schedule_contract import ScheduleAdapter
from app.integrations.contracts.financial_contract import FinancialAdapter
from app.integrations.contracts.notification_contract import NotificationAdapter
from app.integrations.acl.hospital_acl import HospitalACL, Hospital
from app.integrations.acl.payroll_acl import PayrollACL, PayrollExport
from app.integrations.acl.doctor_acl import DoctorACL, DoctorExternal
from app.integrations.acl.schedule_acl import ScheduleACL
from app.integrations.acl.financial_acl import FinancialACL
from app.integrations.acl.notification_acl import NotificationACL


# ============================================================
# Tests — Contracts
# ============================================================


class TestContracts:
    """Testes para contratos de integração."""

    def test_hospital_data_creation(self):
        """Testa criação de HospitalData."""
        data = HospitalData(
            id="h1",
            name="Hospital Test",
            address="Rua Test, 123",
            phone="123456789",
            email="test@hospital.com",
        )
        assert data.id == "h1"
        assert data.name == "Hospital Test"
        assert data.address == "Rua Test, 123"
        assert data.phone == "123456789"
        assert data.email == "test@hospital.com"

    def test_hospital_data_immutable(self):
        """Testa que HospitalData é imutável."""
        data = HospitalData(id="h1", name="Test", address="Address")
        with pytest.raises(AttributeError):
            data.id = "h2"

    def test_doctor_external_data_creation(self):
        """Testa criação de DoctorExternalData."""
        data = DoctorExternalData(
            id="d1",
            name="Dr. Test",
            crm="12345",
            specialty="Cardiology",
            email="doctor@test.com",
            hospital_id="h1",
        )
        assert data.id == "d1"
        assert data.name == "Dr. Test"
        assert data.crm == "12345"

    def test_payroll_export_data_creation(self):
        """Testa criação de PayrollExportData."""
        data = PayrollExportData(
            payroll_id="p1",
            competency="2026-06",
            doctors=[{"id": "d1", "name": "Dr. Test"}],
            total_amount=10000.0,
            export_date=datetime.now(),
        )
        assert data.payroll_id == "p1"
        assert data.competency == "2026-06"
        assert data.total_amount == 10000.0

    def test_export_result_creation(self):
        """Testa criação de ExportResult."""
        result = ExportResult(
            success=True,
            file_path="/path/to/file.csv",
            error_message=None,
            export_date=datetime.now(),
        )
        assert result.success is True
        assert result.file_path == "/path/to/file.csv"

    def test_sync_result_creation(self):
        """Testa criação de SyncResult."""
        result = SyncResult(
            success=True,
            synced_count=10,
            error_count=0,
            errors=[],
        )
        assert result.success is True
        assert result.synced_count == 10

    def test_crm_validation_result_creation(self):
        """Testa criação de CRMValidationResult."""
        result = CRMValidationResult(
            valid=True,
            doctor_name="Dr. Test",
            specialty="Cardiology",
            error_message=None,
        )
        assert result.valid is True
        assert result.doctor_name == "Dr. Test"


# ============================================================
# Tests — ACLs (Sync Delegation Tests)
# ============================================================


class TestHospitalACL:
    """Testes para HospitalACL."""

    def test_to_domain(self):
        """Testa tradução de dados externos para domínio."""
        adapter = MagicMock()
        acl = HospitalACL(adapter)
        external_data = HospitalData(
            id="h1", name="Test", address="Address"
        )
        hospital = acl._to_domain(external_data)
        assert isinstance(hospital, Hospital)
        assert hospital.id == "h1"

    def test_to_external(self):
        """Testa tradução de dados do domínio para externo."""
        adapter = MagicMock()
        acl = HospitalACL(adapter)
        domain_data = Hospital(id="h1", name="Test", address="Address")
        external_data = acl._to_external(domain_data)
        assert isinstance(external_data, HospitalData)
        assert external_data.id == "h1"


class TestPayrollACL:
    """Testes para PayrollACL."""

    def test_to_domain(self):
        """Testa tradução de dados externos para domínio."""
        adapter = MagicMock()
        acl = PayrollACL(adapter)
        external_data = PayrollImportData(
            payroll_id="p1", status="imported", import_date=datetime.now()
        )
        export = acl._to_domain(external_data)
        assert isinstance(export, PayrollExport)
        assert export.payroll_id == "p1"

    def test_to_external(self):
        """Testa tradução de dados do domínio para externo."""
        adapter = MagicMock()
        acl = PayrollACL(adapter)
        domain_data = PayrollExport(
            payroll_id="p1",
            competency="2026-06",
            doctors=[],
            total_amount=0.0,
            export_date=datetime.now(),
        )
        external_data = acl._to_external(domain_data)
        assert isinstance(external_data, PayrollExportData)
        assert external_data.payroll_id == "p1"


class TestDoctorACL:
    """Testes para DoctorACL."""

    def test_to_domain(self):
        """Testa tradução de dados externos para domínio."""
        adapter = MagicMock()
        acl = DoctorACL(adapter)
        external_data = DoctorExternalData(
            id="d1",
            name="Dr. Test",
            crm="12345",
            specialty="Cardiology",
            email="doctor@test.com",
            hospital_id="h1",
        )
        doctor = acl._to_domain(external_data)
        assert isinstance(doctor, DoctorExternal)
        assert doctor.id == "d1"

    def test_to_external(self):
        """Testa tradução de dados do domínio para externo."""
        adapter = MagicMock()
        acl = DoctorACL(adapter)
        domain_data = DoctorExternal(
            id="d1",
            name="Dr. Test",
            crm="12345",
            specialty="Cardiology",
            email="doctor@test.com",
            hospital_id="h1",
        )
        external_data = acl._to_external(domain_data)
        assert isinstance(external_data, DoctorExternalData)
        assert external_data.id == "d1"


class TestScheduleACL:
    """Testes para ScheduleACL."""

    def test_to_domain(self):
        """Testa tradução de dados externos para domínio."""
        adapter = MagicMock()
        acl = ScheduleACL(adapter)
        external_data = ScheduleImportData(
            period_id="per1", shifts=[], import_date=datetime.now()
        )
        export = acl._to_domain(external_data)
        assert isinstance(export, ScheduleExportData)
        assert export.period_id == "per1"

    def test_to_external(self):
        """Testa tradução de dados do domínio para externo."""
        adapter = MagicMock()
        acl = ScheduleACL(adapter)
        domain_data = ScheduleExportData(
            period_id="per1", shifts=[], export_date=datetime.now()
        )
        external_data = acl._to_external(domain_data)
        assert isinstance(external_data, ScheduleImportData)
        assert external_data.period_id == "per1"


class TestFinancialACL:
    """Testes para FinancialACL."""

    def test_to_domain(self):
        """Testa tradução de dados externos para domínio."""
        adapter = MagicMock()
        acl = FinancialACL(adapter)
        external_data = FinancialImportData(
            period_id="per1", doctors=[], import_date=datetime.now()
        )
        export = acl._to_domain(external_data)
        assert isinstance(export, FinancialExportData)
        assert export.period_id == "per1"

    def test_to_external(self):
        """Testa tradução de dados do domínio para externo."""
        adapter = MagicMock()
        acl = FinancialACL(adapter)
        domain_data = FinancialExportData(
            period_id="per1", doctors=[], total_amount=0.0, export_date=datetime.now()
        )
        external_data = acl._to_external(domain_data)
        assert isinstance(external_data, FinancialImportData)
        assert external_data.period_id == "per1"


class TestNotificationACL:
    """Testes para NotificationACL."""

    def test_to_domain(self):
        """Testa tradução de dados externos para domínio."""
        adapter = MagicMock()
        acl = NotificationACL(adapter)
        external_data = NotificationResult(
            success=True, notification_id="n1"
        )
        notification = acl._to_domain(external_data)
        assert isinstance(notification, NotificationData)

    def test_to_external(self):
        """Testa tradução de dados do domínio para externo."""
        adapter = MagicMock()
        acl = NotificationACL(adapter)
        domain_data = NotificationData(
            recipient_id="d1",
            recipient_type="doctor",
            subject="Test",
            body="Test body",
            notification_type="email",
        )
        external_data = acl._to_external(domain_data)
        assert isinstance(external_data, NotificationResult)
        assert external_data.success is True


# ============================================================
# Tests — Protocol Compliance
# ============================================================


class TestProtocolCompliance:
    """Testes para conformidade com Protocolos."""

    def test_hospital_adapter_protocol(self):
        """Testa que HospitalAdapterBase implementa HospitalAdapter."""
        from app.integrations.adapters.hospital_adapter import HospitalAdapterBase

        assert issubclass(HospitalAdapterBase, HospitalAdapter)

    def test_payroll_adapter_protocol(self):
        """Testa que PayrollAdapterBase implementa PayrollAdapter."""
        from app.integrations.adapters.payroll_adapter import PayrollAdapterBase

        assert issubclass(PayrollAdapterBase, PayrollAdapter)

    def test_doctor_adapter_protocol(self):
        """Testa que DoctorAdapterBase implementa DoctorAdapter."""
        from app.integrations.adapters.doctor_adapter import DoctorAdapterBase

        assert issubclass(DoctorAdapterBase, DoctorAdapter)

    def test_schedule_adapter_protocol(self):
        """Testa que ScheduleAdapterBase implementa ScheduleAdapter."""
        from app.integrations.adapters.schedule_adapter import ScheduleAdapterBase

        assert issubclass(ScheduleAdapterBase, ScheduleAdapter)

    def test_financial_adapter_protocol(self):
        """Testa que FinancialAdapterBase implementa FinancialAdapter."""
        from app.integrations.adapters.financial_adapter import FinancialAdapterBase

        assert issubclass(FinancialAdapterBase, FinancialAdapter)

    def test_notification_adapter_protocol(self):
        """Testa que NotificationAdapterBase implementa NotificationAdapter."""
        from app.integrations.adapters.notification_adapter import NotificationAdapterBase

        assert issubclass(NotificationAdapterBase, NotificationAdapter)
