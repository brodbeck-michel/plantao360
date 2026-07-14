"""Tests for Query Domain — Read Models, Query Objects, Projections, Explainability, KPIs, Timeline."""

import pytest
from datetime import datetime

from app.services.query_service import (
    DoctorSummary,
    CoverageSummary,
    FinancialSummary,
    PayrollSummary,
)

from app.services.query_service import (
    DoctorAnalyticsQuery,
    CoverageAnalyticsQuery,
    FinancialAnalyticsQuery,
    PayrollAnalyticsQuery,
    TimelineQuery,
)

from app.services.query_service import DomainExplanation, ExplanationStep, ExplanationContext

from app.services.query_service import AuditAnalytics, ReopenedCompetency, ApprovalRecord

from app.services.query_service import CoverageKPI, FinancialKPI, PayrollKPI, OperationalKPI

from app.services.query_service import InstitutionTimeline, TimelineEvent


class TestReadModels:
    def test_doctor_summary(self):
        ds = DoctorSummary(
            doctor_id=1, name="Dr. João", crm="12345",
            hour_rate=100.0, active=True, total_shifts=10,
        )
        assert ds.doctor_id == 1
        assert ds.total_shifts == 10
        d = ds.to_dict()
        assert d["name"] == "Dr. João"

    def test_coverage_summary(self):
        cs = CoverageSummary(period_id=1, total_shifts=30, coverage_rate=85.0)
        assert cs.period_id == 1
        assert cs.coverage_rate == 85.0
        d = cs.to_dict()
        assert d["total_shifts"] == 30

    def test_financial_summary(self):
        fs = FinancialSummary(period_id=1, total_facts=50, total_value=10000.0)
        assert fs.total_facts == 50
        d = fs.to_dict()
        assert d["total_value"] == 10000.0

    def test_payroll_summary(self):
        ps = PayrollSummary(
            payroll_id=1, period_id=1, year_month="202606",
            status="approved", current_version=1,
        )
        assert ps.status == "approved"
        d = ps.to_dict()
        assert d["year_month"] == "202606"


class TestQueryObjects:
    def test_doctor_query(self):
        q = DoctorAnalyticsQuery(doctor_id=1, active_only=True)
        assert q.doctor_id == 1
        d = q.to_dict()
        assert d["active_only"] is True

    def test_coverage_query(self):
        q = CoverageAnalyticsQuery(period_id=1, year_month="202606")
        assert q.period_id == 1
        d = q.to_dict()
        assert d["year_month"] == "202606"

    def test_financial_query(self):
        q = FinancialAnalyticsQuery(period_id=1, doctor_id=1)
        assert q.doctor_id == 1
        d = q.to_dict()
        assert d["include_rules"] is True

    def test_payroll_query(self):
        q = PayrollAnalyticsQuery(payroll_id=1, status="approved")
        assert q.status == "approved"
        d = q.to_dict()
        assert d["include_audit"] is True

    def test_timeline_query(self):
        q = TimelineQuery(entity_type="payroll", entity_id=1)
        assert q.entity_type == "payroll"
        d = q.to_dict()
        assert d["include_events"] is True


class TestExplainability:
    def test_explanation_step(self):
        step = ExplanationStep(
            step_number=1,
            description="Aplicação da regra de plantão noturno",
            rule_applied="RN-01",
            input_value=100.0,
            output_value=150.0,
            multiplier=1.5,
        )
        assert step.step_number == 1
        d = step.to_dict()
        assert d["multiplier"] == 1.5

    def test_explanation_context(self):
        ctx = ExplanationContext(
            entity_type="remuneration",
            period_id=1,
            year_month="202606",
            doctor_id=1,
        )
        assert ctx.entity_type == "remuneration"
        d = ctx.to_dict()
        assert d["doctor_id"] == 1

    def test_domain_explanation(self):
        step = ExplanationStep(
            step_number=1,
            description="Test",
            rule_applied="RN-01",
        )
        ctx = ExplanationContext(entity_type="remuneration", period_id=1)
        exp = DomainExplanation(
            question="Por que?",
            answer="Porque sim.",
            entity_type="remuneration",
            entity_id=1,
            context=ctx,
            steps=[step],
            rules_applied=["RN-01"],
        )
        assert exp.is_reproducible
        assert exp.total_steps == 1
        d = exp.to_dict()
        assert d["confidence"] == 1.0

    def test_explanation_not_reproducible_without_steps(self):
        ctx = ExplanationContext(entity_type="remuneration")
        exp = DomainExplanation(
            question="Por que?",
            answer="Resposta.",
            entity_type="remuneration",
            entity_id=1,
            context=ctx,
        )
        assert not exp.is_reproducible


class TestAuditAnalytics:
    def test_reopened_competency(self):
        rc = ReopenedCompetency(
            payroll_id=1, year_month="202606",
            reopened_by="admin", reopened_at="2026-06-27T10:00:00",
            reason="Error correction", previous_version=1, new_version=2,
        )
        assert rc.payroll_id == 1
        d = rc.to_dict()
        assert d["new_version"] == 2

    def test_approval_record(self):
        ar = ApprovalRecord(
            payroll_id=1, year_month="202606",
            approved_by="admin", approved_at="2026-06-27T10:00:00",
            version=1, checklist_complete=True,
        )
        assert ar.checklist_complete
        d = ar.to_dict()
        assert d["approved_by"] == "admin"

    def test_audit_analytics(self):
        aa = AuditAnalytics(
            total_competencies=10,
            reopen_count=2,
            reopen_rate=20.0,
        )
        assert aa.total_competencies == 10
        d = aa.to_dict()
        assert d["reopen_rate"] == 20.0


class TestKPIs:
    def test_coverage_kpi(self):
        kpi = CoverageKPI(
            period_id=1, year_month="202606",
            coverage_rate=85.0, total_shifts=30,
            covered_shifts=25, uncovered_shifts=5,
        )
        assert kpi.coverage_rate == 85.0
        d = kpi.to_dict()
        assert d["formula"] == "covered_shifts / total_shifts * 100"
        assert len(d["evidence"]) == 3

    def test_financial_kpi(self):
        kpi = FinancialKPI(
            period_id=1, year_month="202606",
            total_remuneration=50000.0,
            total_shifts=30,
            cost_per_shift=1666.67,
        )
        assert kpi.total_remuneration == 50000.0
        d = kpi.to_dict()
        assert "cost_per_shift" in d

    def test_payroll_kpi(self):
        kpi = PayrollKPI(
            period_id=1, year_month="202606",
            total_competencies=5,
            approved_competencies=4,
            reopened_competencies=1,
            reopen_rate=20.0,
        )
        assert kpi.reopen_rate == 20.0
        d = kpi.to_dict()
        assert "explanation" in d

    def test_operational_kpi(self):
        kpi = OperationalKPI(
            period_id=1, year_month="202606",
            total_shifts=30,
            total_doctors=10,
            total_extras=5,
            extras_approved=4,
            extra_approval_rate=80.0,
        )
        assert kpi.extra_approval_rate == 80.0
        d = kpi.to_dict()
        assert d["formula"] == "doctors_per_shift = total_doctors / total_shifts"


class TestTimeline:
    def test_timeline_event(self):
        event = TimelineEvent(
            timestamp="2026-06-27T10:00:00",
            event_type="shift.created",
            entity_type="shift",
            entity_id=1,
            description="Plantão criado",
        )
        assert event.event_type == "shift.created"
        d = event.to_dict()
        assert d["entity_type"] == "shift"

    def test_institution_timeline(self):
        event = TimelineEvent(
            timestamp="2026-06-27T10:00:00",
            event_type="shift.created",
            entity_type="shift",
            entity_id=1,
            description="Test",
        )
        tl = InstitutionTimeline(
            entity_type="shift",
            entity_id=1,
            events=[event],
            total_events=1,
        )
        assert not tl.is_empty
        assert tl.total_events == 1
        assert "shift.created" in tl.event_types
        d = tl.to_dict()
        assert len(d["events"]) == 1

    def test_empty_timeline(self):
        tl = InstitutionTimeline()
        assert tl.is_empty

    def test_filter_by_type(self):
        events = [
            TimelineEvent(timestamp="t1", event_type="shift.created", entity_type="shift", entity_id=1, description=""),
            TimelineEvent(timestamp="t2", event_type="assignment.created", entity_type="assignment", entity_id=1, description=""),
            TimelineEvent(timestamp="t3", event_type="shift.created", entity_type="shift", entity_id=2, description=""),
        ]
        tl = InstitutionTimeline(events=events)
        filtered = tl.filter_by_type("shift.created")
        assert len(filtered) == 2
