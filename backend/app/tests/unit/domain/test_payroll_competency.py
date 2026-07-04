"""Tests for payroll competency domain object."""

import pytest
from datetime import datetime

from app.domain.payroll.payroll_competency import (
    PayrollCompetency,
    PayrollVersion,
    PayrollSeal,
    PayrollExplanation,
    PayrollAuditSnapshot,
    ExplanationStep,
    AuditEntry,
)
from app.domain.payroll.governance import (
    PayrollReadiness,
    ApprovalChecklist,
    AdministrativeApproval,
    AdministrativeLock,
    ApprovalSnapshot,
    ReadinessStatus,
)
from app.domain.constants.payroll_status import PayrollStatus
from app.domain.remuneration.remuneration_result import RemunerationResult, DoctorRemuneration
from app.domain.remuneration.calculation_explanation import CalculationExplanation
from app.domain.financial.financial_snapshot_builder import FinancialSnapshotData, FinancialFactData


def _make_snapshot(facts=None):
    return FinancialSnapshotData(
        period_id=1,
        coverage_snapshot_id=1,
        facts=facts or [],
        total_facts=0,
        total_duration_minutes=0,
    )


def _make_result(period_id=1, total_value=100.0):
    return RemunerationResult(
        period_id=period_id,
        total_value=total_value,
        total_facts=1,
        doctor_results=[
            DoctorRemuneration(
                doctor_id=1,
                total_value=total_value,
                calculations=[
                    CalculationExplanation(
                        fact_id=1,
                        fact_type="assignment_completion",
                        doctor_id=1,
                        duration_minutes=60,
                        rule_id="rule_1",
                        rule_version="1.0",
                        hour_rate=100.0,
                        multiplier=1.0,
                        total_value=100.0,
                    )
                ],
            )
        ],
    )


class TestPayrollCompetency:
    def test_create(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        assert pc.period_id == 1
        assert pc.year_month == "202606"
        assert pc.status == PayrollStatus.DRAFT
        assert pc.current_version == 1
        assert pc.reopen_count == 0
        assert pc.total_value == 0.0
        assert not pc.is_approved
        assert not pc.is_locked
        assert not pc.is_sealed
        assert not pc.is_administratively_closed

    def test_calculate(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        snapshot = _make_snapshot()
        result = _make_result()
        pc.calculate(snapshot, result)
        assert pc.status == PayrollStatus.CALCULATED
        assert len(pc.versions) == 1
        assert pc.total_value == 100.0
        assert pc.explanation is not None

    def test_review(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        assert pc.status == PayrollStatus.REVIEWED

    def test_approve_creates_seal(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        assert pc.status == PayrollStatus.APPROVED
        assert pc.seal is not None
        assert pc.is_sealed
        assert pc.is_approved
        assert pc.seal.total_value == 100.0

    def test_lock(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.lock(locked_by="admin", justification="Bloqueio para auditoria")
        assert pc.status == PayrollStatus.LOCKED
        assert pc.is_locked
        assert pc.administrative_lock is not None
        assert pc.administrative_lock.locked_by == "admin"

    def test_unlock(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.lock(locked_by="admin", justification="Test")
        pc.unlock(unlocked_by="director", justification="Desbloqueio autorizado")
        assert pc.status == PayrollStatus.APPROVED
        assert not pc.is_locked
        assert pc.administrative_lock is None

    def test_export(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.export()
        assert pc.status == PayrollStatus.EXPORTED

    def test_export_from_locked(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.lock(locked_by="admin", justification="Test")
        pc.export()
        assert pc.status == PayrollStatus.EXPORTED

    def test_mark_paid(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.export()
        pc.mark_paid()
        assert pc.status == PayrollStatus.PAID

    def test_archive(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.export()
        pc.mark_paid()
        pc.archive()
        assert pc.status == PayrollStatus.ARCHIVED

    def test_reopen_from_approved(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.reopen(reason="Error correction")
        assert pc.status == PayrollStatus.DRAFT
        assert pc.reopen_count == 1
        assert pc.current_version == 2
        assert pc.seal is None

    def test_reopen_from_locked(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.lock(locked_by="admin", justification="Test")
        pc.reopen(reason="Correction needed")
        assert pc.status == PayrollStatus.DRAFT
        assert pc.reopen_count == 1
        assert pc.current_version == 2
        assert pc.seal is None
        assert pc.administrative_lock is None
        assert pc.administrative_approval is None

    def test_reopen_generates_new_version(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        pc.reopen(reason="Correction")
        assert pc.current_version == 2
        pc.calculate(_make_snapshot(), _make_result(total_value=200.0))
        assert len(pc.versions) == 2
        assert pc.total_value == 200.0

    def test_get_active_version(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        assert pc.get_active_version() is None
        pc.calculate(_make_snapshot(), _make_result())
        v = pc.get_active_version()
        assert v is not None
        assert v.version_number == 1

    def test_get_version(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        v = pc.get_version(1)
        assert v is not None
        assert v.version_number == 1
        assert pc.get_version(99) is None

    def test_events_generated(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        events = [e["name"] for e in pc.pending_events]
        assert "payroll.created.v1" in events

    def test_events_after_calculate(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        events = [e["name"] for e in pc.pending_events]
        assert "payroll.calculated.v1" in events

    def test_invalid_transition_fails(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        with pytest.raises(ValueError, match="Cannot transition"):
            pc.review()

    def test_reopen_requires_valid_status(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        with pytest.raises(ValueError, match="Cannot reopen"):
            pc.reopen(reason="test")


class TestPayrollCompetencyGovernance:
    def test_validate_readiness_calculated(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        readiness = pc.validate_readiness(validated_by="admin")
        assert readiness.status == ReadinessStatus.READY
        assert readiness.pending_count == 0
        assert pc.readiness is not None

    def test_validate_readiness_draft_fails(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        readiness = pc.validate_readiness(validated_by="admin")
        assert readiness.status == ReadinessStatus.NOT_READY
        assert readiness.pending_count > 0

    def test_build_checklist(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.validate_readiness(validated_by="admin")
        checklist = pc.build_checklist(created_by="admin")
        assert checklist is not None
        assert checklist.total_items > 0
        assert pc.checklist is not None

    def test_build_checklist_without_readiness_fails(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        with pytest.raises(ValueError, match="Readiness deve ser validado"):
            pc.build_checklist(created_by="admin")

    def test_approve_administratively(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.validate_readiness(validated_by="admin")
        pc.build_checklist(created_by="admin")
        approval = pc.approve_administratively(
            approved_by="admin",
            justification="Dados validados e conferidos",
        )
        assert pc.status == PayrollStatus.APPROVED
        assert pc.is_administratively_closed
        assert pc.administrative_approval is not None
        assert pc.approval_snapshot is not None
        assert pc.seal is not None

    def test_approve_administratively_without_readiness_fails(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        with pytest.raises(ValueError, match="Readiness deve estar ready"):
            pc.approve_administratively(
                approved_by="admin",
                justification="Test",
            )

    def test_lock_unlock_cycle(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        pc.review()
        pc.approve()
        assert pc.status == PayrollStatus.APPROVED

        pc.lock(locked_by="admin", justification="Auditoria")
        assert pc.status == PayrollStatus.LOCKED
        assert pc.is_locked

        pc.unlock(unlocked_by="director", justification="Autorizado")
        assert pc.status == PayrollStatus.APPROVED
        assert not pc.is_locked


class TestPayrollVersion:
    def test_version_creation(self):
        v = PayrollVersion(
            version_number=1,
            created_at=datetime.utcnow(),
            financial_snapshot=_make_snapshot(),
            remuneration_result=_make_result(),
        )
        assert v.version_number == 1
        assert v.remuneration_result.total_value == 100.0

    def test_version_to_dict(self):
        v = PayrollVersion(
            version_number=1,
            created_at=datetime.utcnow(),
            financial_snapshot=_make_snapshot(),
            remuneration_result=_make_result(),
        )
        d = v.to_dict()
        assert d["version_number"] == 1
        assert d["total_value"] == 100.0
        assert d["total_doctors"] == 1


class TestPayrollSeal:
    def test_seal_creation(self):
        s = PayrollSeal(
            sealed_at=datetime.utcnow(),
            sealed_by="admin",
            version_number=1,
            financial_snapshot=_make_snapshot(),
            remuneration_result=_make_result(),
            total_value=100.0,
            total_doctors=1,
            total_facts=1,
        )
        assert s.sealed_by == "admin"
        assert s.total_value == 100.0

    def test_seal_to_dict(self):
        s = PayrollSeal(
            sealed_at=datetime.utcnow(),
            sealed_by="admin",
            version_number=1,
            financial_snapshot=_make_snapshot(),
            remuneration_result=_make_result(),
            total_value=100.0,
            total_doctors=1,
            total_facts=1,
        )
        d = s.to_dict()
        assert d["sealed_by"] == "admin"
        assert d["total_value"] == 100.0


class TestPayrollExplanation:
    def test_explanation_creation(self):
        e = PayrollExplanation(created_at=datetime.utcnow())
        assert len(e.steps) == 0
        assert e.total_value == 0.0

    def test_explanation_add_step(self):
        e = PayrollExplanation(created_at=datetime.utcnow())
        step = ExplanationStep(
            step_number=1,
            description="Test step",
            doctor_id=1,
            fact_type="assignment_completion",
            rule_id="rule_1",
            rule_version="1.0",
            hour_rate=100.0,
            multiplier=1.0,
            duration_minutes=60,
            total_value=100.0,
        )
        e.add_step(step)
        assert len(e.steps) == 1
        assert e.total_value == 100.0

    def test_explanation_to_dict(self):
        e = PayrollExplanation(created_at=datetime.utcnow())
        d = e.to_dict()
        assert "steps" in d
        assert "total_value" in d


class TestPayrollAuditSnapshot:
    def test_audit_creation(self):
        a = PayrollAuditSnapshot()
        assert len(a.entries) == 0

    def test_audit_add_entry(self):
        a = PayrollAuditSnapshot()
        entry = AuditEntry(
            timestamp=datetime.utcnow(),
            action="created",
            performed_by="system",
            previous_status="draft",
            new_status="draft",
            details="Test",
        )
        a.add_entry(entry)
        assert len(a.entries) == 1

    def test_audit_to_dict(self):
        a = PayrollAuditSnapshot()
        d = a.to_dict()
        assert "entries" in d
        assert "entries_count" in d
