"""Tests for payroll governance domain objects."""

import pytest
from datetime import datetime

from app.domain.payroll.governance import (
    PayrollReadiness,
    ApprovalChecklist,
    AdministrativeApproval,
    AdministrativeLock,
    ApprovalSnapshot,
    ChecklistItem,
    ChecklistItemStatus,
    ChecklistCategory,
    ReadinessStatus,
    ReadinessItem,
)


class TestChecklistItem:
    def test_create(self):
        item = ChecklistItem(
            item_id="CLC-01",
            description="Competência calculada",
            category=ChecklistCategory.CALCULO,
        )
        assert item.item_id == "CLC-01"
        assert item.status == ChecklistItemStatus.PENDING
        assert not item.is_resolved

    def test_satisfy(self):
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        item.satisfy(checked_by="admin", justification="Auto-validado")
        assert item.status == ChecklistItemStatus.SATISFIED
        assert item.is_resolved
        assert item.checked_by == "admin"

    def test_waive(self):
        item = ChecklistItem(
            item_id="OPT-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
            required=False,
        )
        item.waive(checked_by="admin", justification="Item não aplicável neste contexto")
        assert item.status == ChecklistItemStatus.WAIVED
        assert item.is_resolved

    def test_waive_requires_justification(self):
        item = ChecklistItem(
            item_id="OPT-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        with pytest.raises(ValueError, match="mínimo de 10 caracteres"):
            item.waive(checked_by="admin", justification="Short")

    def test_fail(self):
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        item.fail(checked_by="admin", justification="Não atendido")
        assert item.status == ChecklistItemStatus.NOT_SATISFIED
        assert not item.is_resolved

    def test_to_dict(self):
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        d = item.to_dict()
        assert d["item_id"] == "CLC-01"
        assert d["status"] == "pending"


class TestReadinessItem:
    def test_create(self):
        item = ReadinessItem(
            item_id="CLC-01",
            description="Test",
            passed=True,
        )
        assert item.passed

    def test_to_dict(self):
        item = ReadinessItem(
            item_id="CLC-01",
            description="Test",
            passed=False,
            message="Not ready",
        )
        d = item.to_dict()
        assert not d["passed"]
        assert d["message"] == "Not ready"


class TestPayrollReadiness:
    def test_create(self):
        readiness = PayrollReadiness(
            competency_id=1,
            year_month="202606",
            version=1,
            validated_at=datetime.utcnow(),
            validated_by="system",
            status=ReadinessStatus.READY,
        )
        assert readiness.is_ready
        assert readiness.pending_count == 0

    def test_not_ready(self):
        readiness = PayrollReadiness(
            competency_id=1,
            year_month="202606",
            version=1,
            validated_at=datetime.utcnow(),
            validated_by="system",
            status=ReadinessStatus.NOT_READY,
            pending_count=2,
        )
        assert not readiness.is_ready
        assert readiness.pending_count == 2

    def test_add_item(self):
        readiness = PayrollReadiness(
            competency_id=1,
            year_month="202606",
            version=1,
            validated_at=datetime.utcnow(),
            validated_by="system",
            status=ReadinessStatus.NOT_READY,
        )
        item = ReadinessItem(item_id="CLC-01", description="Test", passed=False)
        readiness.add_item(item)
        assert readiness.pending_count == 1

    def test_to_dict(self):
        readiness = PayrollReadiness(
            competency_id=1,
            year_month="202606",
            version=1,
            validated_at=datetime.utcnow(),
            validated_by="system",
            status=ReadinessStatus.READY,
        )
        d = readiness.to_dict()
        assert d["status"] == "ready"
        assert d["competency_id"] == 1


class TestApprovalChecklist:
    def test_create(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        assert checklist.total_items == 0
        assert not checklist.is_complete

    def test_add_items_and_complete(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        item.satisfy(checked_by="admin")
        checklist.items.append(item)

        assert checklist.total_items == 1
        assert checklist.satisfied_items == 1
        assert checklist.all_required_satisfied
        assert checklist.is_complete

    def test_incomplete_checklist(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        checklist.items.append(item)

        assert not checklist.is_complete

    def test_complete_checklist(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        item.satisfy(checked_by="admin")
        checklist.items.append(item)

        checklist.complete(completed_by="admin")
        assert checklist.completed
        assert checklist.completed_by == "admin"

    def test_complete_incomplete_checklist_fails(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        checklist.items.append(item)

        with pytest.raises(ValueError, match="Checklist incompleto"):
            checklist.complete(completed_by="admin")

    def test_get_item(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        item = ChecklistItem(
            item_id="CLC-01",
            description="Test",
            category=ChecklistCategory.CALCULO,
        )
        checklist.items.append(item)

        found = checklist.get_item("CLC-01")
        assert found is not None
        assert found.item_id == "CLC-01"
        assert checklist.get_item("NOT_FOUND") is None

    def test_to_dict(self):
        checklist = ApprovalChecklist(
            competency_id=1,
            year_month="202606",
            version=1,
            created_at=datetime.utcnow(),
            created_by="system",
        )
        d = checklist.to_dict()
        assert d["competency_id"] == 1
        assert d["total_items"] == 0


class TestAdministrativeApproval:
    def test_create(self):
        approval = AdministrativeApproval(
            competency_id=1,
            year_month="202606",
            version=1,
            approved_by="admin",
            approved_at=datetime.utcnow(),
            justification="Dados validados",
        )
        assert approval.approved_by == "admin"
        assert approval.justification == "Dados validados"

    def test_to_dict(self):
        approval = AdministrativeApproval(
            competency_id=1,
            year_month="202606",
            version=1,
            approved_by="admin",
            approved_at=datetime.utcnow(),
            justification="Test",
        )
        d = approval.to_dict()
        assert d["approved_by"] == "admin"


class TestAdministrativeLock:
    def test_create(self):
        lock = AdministrativeLock(
            competency_id=1,
            year_month="202606",
            version=1,
            locked_by="admin",
            locked_at=datetime.utcnow(),
            justification="Bloqueio para auditoria",
        )
        assert lock.locked_by == "admin"

    def test_to_dict(self):
        lock = AdministrativeLock(
            competency_id=1,
            year_month="202606",
            version=1,
            locked_by="admin",
            locked_at=datetime.utcnow(),
        )
        d = lock.to_dict()
        assert d["locked_by"] == "admin"


class TestApprovalSnapshot:
    def test_create(self):
        approval = AdministrativeApproval(
            competency_id=1,
            year_month="202606",
            version=1,
            approved_by="admin",
            approved_at=datetime.utcnow(),
            justification="Test",
        )
        snapshot = ApprovalSnapshot(
            competency_id=1,
            year_month="202606",
            version=1,
            snapshot_by="admin",
            snapshot_at=datetime.utcnow(),
            justification="Test",
            approval=approval,
        )
        assert snapshot.version == 1
        assert snapshot.approval == approval

    def test_to_dict(self):
        approval = AdministrativeApproval(
            competency_id=1,
            year_month="202606",
            version=1,
            approved_by="admin",
            approved_at=datetime.utcnow(),
            justification="Test",
        )
        snapshot = ApprovalSnapshot(
            competency_id=1,
            year_month="202606",
            version=1,
            snapshot_by="admin",
            snapshot_at=datetime.utcnow(),
            justification="Test",
            approval=approval,
        )
        d = snapshot.to_dict()
        assert d["version"] == 1
        assert d["approval"]["approved_by"] == "admin"
