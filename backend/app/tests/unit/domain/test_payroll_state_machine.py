"""Tests for payroll state machine."""

import pytest

from app.domain.payroll.payroll_competency import PayrollCompetency
from app.domain.constants.payroll_status import PayrollStatus
from app.domain.state_machines.payroll_state_machine import PayrollStateMachine
from app.domain.remuneration.remuneration_result import RemunerationResult, DoctorRemuneration
from app.domain.remuneration.calculation_explanation import CalculationExplanation
from app.domain.financial.financial_snapshot_builder import FinancialSnapshotData


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


class TestPayrollStateMachine:
    def test_calculate_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.DRAFT, PayrollStatus.CALCULATED)

    def test_review_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.CALCULATED, PayrollStatus.REVIEWED)

    def test_approve_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.REVIEWED, PayrollStatus.APPROVED)

    def test_lock_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.APPROVED, PayrollStatus.LOCKED)

    def test_unlock_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.LOCKED, PayrollStatus.APPROVED)

    def test_export_from_approved(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.APPROVED, PayrollStatus.EXPORTED)

    def test_export_from_locked(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.LOCKED, PayrollStatus.EXPORTED)

    def test_paid_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.EXPORTED, PayrollStatus.PAID)

    def test_archive_transition(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.PAID, PayrollStatus.ARCHIVED)

    def test_reopen_from_locked(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert sm.can_transition(PayrollStatus.LOCKED, PayrollStatus.DRAFT)

    def test_reopen_from_archived_fails(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert not sm.can_transition(PayrollStatus.ARCHIVED, PayrollStatus.DRAFT)

    def test_invalid_transition_calculate_to_approved(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert not sm.can_transition(PayrollStatus.CALCULATED, PayrollStatus.APPROVED)

    def test_invalid_transition_draft_to_approved(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        assert not sm.can_transition(PayrollStatus.DRAFT, PayrollStatus.APPROVED)

    def test_get_allowed_transitions(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        sm = PayrollStateMachine(pc)
        allowed = sm.get_allowed_transitions(PayrollStatus.APPROVED)
        assert PayrollStatus.LOCKED in allowed
        assert PayrollStatus.EXPORTED in allowed
        assert PayrollStatus.DRAFT in allowed

    def test_full_lifecycle_with_lock(self):
        pc = PayrollCompetency(period_id=1, year_month="202606")
        pc.calculate(_make_snapshot(), _make_result())
        assert pc.status == PayrollStatus.CALCULATED

        pc.review()
        assert pc.status == PayrollStatus.REVIEWED

        pc.approve()
        assert pc.status == PayrollStatus.APPROVED

        pc.lock(locked_by="admin", justification="Test")
        assert pc.status == PayrollStatus.LOCKED

        pc.unlock(unlocked_by="director", justification="Authorized")
        assert pc.status == PayrollStatus.APPROVED

        pc.export()
        assert pc.status == PayrollStatus.EXPORTED

        pc.mark_paid()
        assert pc.status == PayrollStatus.PAID

        pc.archive()
        assert pc.status == PayrollStatus.ARCHIVED
