"""Query Services — Read-only services for the query domain."""

from app.domain.query.doctor_analytics_query import DoctorAnalyticsQuery
from app.domain.query.coverage_analytics_query import CoverageAnalyticsQuery
from app.domain.query.financial_analytics_query import FinancialAnalyticsQuery
from app.domain.query.payroll_analytics_query import PayrollAnalyticsQuery
from app.domain.query.timeline_query import TimelineQuery

from app.domain.read_models.doctor_summary import DoctorSummary
from app.domain.read_models.coverage_summary import CoverageSummary
from app.domain.read_models.financial_summary import FinancialSummary
from app.domain.read_models.payroll_summary import PayrollSummary

from app.domain.explainability.domain_explanation import DomainExplanation
from app.domain.explainability.explanation_step import ExplanationStep
from app.domain.explainability.explanation_context import ExplanationContext

from app.domain.analytics.audit_analytics import AuditAnalytics
from app.domain.kpi.coverage_kpi import CoverageKPI
from app.domain.kpi.financial_kpi import FinancialKPI
from app.domain.kpi.payroll_kpi import PayrollKPI
from app.domain.kpi.operational_kpi import OperationalKPI

from app.domain.timeline import InstitutionTimeline, TimelineEvent

from datetime import datetime


class QueryService:
    """Read-only query service for the query domain.

    Nenhum endpoint poderá alterar estado.
    """

    def __init__(self, session):
        self._session = session

    def execute_doctor_query(self, query: DoctorAnalyticsQuery) -> list[DoctorSummary]:
        """Execute a doctor analytics query."""
        return []

    def execute_coverage_query(self, query: CoverageAnalyticsQuery) -> CoverageSummary:
        """Execute a coverage analytics query."""
        return CoverageSummary(period_id=query.period_id or 0)

    def execute_financial_query(self, query: FinancialAnalyticsQuery) -> FinancialSummary:
        """Execute a financial analytics query."""
        return FinancialSummary(period_id=query.period_id or 0)

    def execute_payroll_query(self, query: PayrollAnalyticsQuery) -> PayrollSummary | list[PayrollSummary]:
        """Execute a payroll analytics query."""
        return []

    def execute_timeline_query(self, query: TimelineQuery) -> InstitutionTimeline:
        """Execute a timeline query."""
        return InstitutionTimeline(entity_type=query.entity_type, entity_id=query.entity_id)

    def explain_remuneration(
        self,
        doctor_id: int,
        period_id: int,
        year_month: str,
    ) -> DomainExplanation:
        """Explain why a doctor received a specific remuneration value."""
        context = ExplanationContext(
            entity_type="remuneration",
            period_id=period_id,
            year_month=year_month,
            doctor_id=doctor_id,
            requested_at=datetime.utcnow(),
        )
        return DomainExplanation(
            question=f"Por que o médico {doctor_id} recebeu esse valor no período {year_month}?",
            answer="Valor calculado com base nas regras de remuneração aplicáveis aos fatos financeiros do período.",
            entity_type="remuneration",
            entity_id=doctor_id,
            context=context,
            steps=[],
            evidence=[],
            rules_applied=[],
            generated_at=datetime.utcnow(),
        )

    def explain_extra_rejection(
        self,
        extra_id: int,
        period_id: int,
    ) -> DomainExplanation:
        """Explain why an extra was rejected."""
        context = ExplanationContext(
            entity_type="extra",
            entity_id=extra_id,
            period_id=period_id,
            requested_at=datetime.utcnow(),
        )
        return DomainExplanation(
            question=f"Por que o extra {extra_id} foi rejeitado?",
            answer="Extra rejeitado de acordo com as regras de negócio aplicáveis.",
            entity_type="extra",
            entity_id=extra_id,
            context=context,
            steps=[],
            evidence=[],
            rules_applied=[],
            generated_at=datetime.utcnow(),
        )

    def explain_competency_reopen(
        self,
        payroll_id: int,
        year_month: str,
    ) -> DomainExplanation:
        """Explain why a competency was reopened."""
        context = ExplanationContext(
            entity_type="payroll",
            entity_id=payroll_id,
            year_month=year_month,
            requested_at=datetime.utcnow(),
        )
        return DomainExplanation(
            question=f"Por que a competência {year_month} foi reaberta?",
            answer="Competência reaberta de acordo com solicitação administrativa.",
            entity_type="payroll",
            entity_id=payroll_id,
            context=context,
            steps=[],
            evidence=[],
            rules_applied=[],
            generated_at=datetime.utcnow(),
        )

    def get_audit_analytics(self, year_month: str | None = None) -> AuditAnalytics:
        """Get audit analytics for a period."""
        return AuditAnalytics(generated_at=datetime.utcnow())

    def get_coverage_kpi(self, period_id: int, year_month: str) -> CoverageKPI:
        """Get coverage KPI for a period."""
        return CoverageKPI(period_id=period_id, year_month=year_month, generated_at=datetime.utcnow())

    def get_financial_kpi(self, period_id: int, year_month: str) -> FinancialKPI:
        """Get financial KPI for a period."""
        return FinancialKPI(period_id=period_id, year_month=year_month, generated_at=datetime.utcnow())

    def get_payroll_kpi(self, period_id: int, year_month: str) -> PayrollKPI:
        """Get payroll KPI for a period."""
        return PayrollKPI(period_id=period_id, year_month=year_month, generated_at=datetime.utcnow())

    def get_operational_kpi(self, period_id: int, year_month: str) -> OperationalKPI:
        """Get operational KPI for a period."""
        return OperationalKPI(period_id=period_id, year_month=year_month, generated_at=datetime.utcnow())
