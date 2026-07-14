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

from app.domain.analytics.audit_analytics import AuditAnalytics
from app.domain.kpi.coverage_kpi import CoverageKPI
from app.domain.kpi.financial_kpi import FinancialKPI
from app.domain.kpi.payroll_kpi import PayrollKPI
from app.domain.kpi.operational_kpi import OperationalKPI

from dataclasses import dataclass, field
from datetime import datetime


# Timeline value objects — antes em domain/timeline (consumidor único: este service).
# Inlinados aqui no colapso da domain/ (spec 004, Grupo B).
@dataclass(frozen=True)
class TimelineEvent:
    """A single event in the institution timeline."""
    timestamp: str
    event_type: str
    entity_type: str
    entity_id: int
    description: str
    performed_by: str = ""
    previous_status: str = ""
    new_status: str = ""
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "description": self.description,
            "performed_by": self.performed_by,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "details": self.details,
        }


@dataclass(frozen=True)
class InstitutionTimeline:
    """Global timeline reconstructing the complete chain of events.

    Reconstrói: Shift → Assignment → Extra → Coverage → Financial Facts →
    Remuneration → Payroll → Approval → Administrative Lock
    """
    entity_type: str = ""
    entity_id: int | None = None
    events: list[TimelineEvent] = field(default_factory=list)
    total_events: int = 0
    date_range: dict = field(default_factory=dict)
    generated_at: datetime | None = None

    @property
    def is_empty(self) -> bool:
        return len(self.events) == 0

    @property
    def event_types(self) -> list[str]:
        return list(set(e.event_type for e in self.events))

    def filter_by_type(self, event_type: str) -> list[TimelineEvent]:
        return [e for e in self.events if e.event_type == event_type]

    def filter_by_entity(self, entity_type: str) -> list[TimelineEvent]:
        return [e for e in self.events if e.entity_type == entity_type]

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "events": [e.to_dict() for e in self.events],
            "total_events": self.total_events,
            "date_range": self.date_range,
            "event_types": self.event_types,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


# Explainability value objects — antes em domain/explainability (consumidor único: este service).
# Inlinados aqui no colapso da domain/ (spec 004, Grupo B).
@dataclass(frozen=True)
class ExplanationStep:
    """A single step explaining why something happened. Reproduzível e rastreável."""
    step_number: int
    description: str
    rule_applied: str
    input_value: float = 0.0
    output_value: float = 0.0
    multiplier: float = 1.0
    duration_minutes: int = 0
    evidence: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        return {
            "step_number": self.step_number,
            "description": self.description,
            "rule_applied": self.rule_applied,
            "input_value": self.input_value,
            "output_value": self.output_value,
            "multiplier": self.multiplier,
            "duration_minutes": self.duration_minutes,
            "evidence": self.evidence,
            "source": self.source,
        }


@dataclass(frozen=True)
class ExplanationContext:
    """Context providing additional information for an explanation."""
    entity_type: str = ""
    entity_id: int | None = None
    period_id: int | None = None
    year_month: str | None = None
    doctor_id: int | None = None
    version: int | None = None
    requested_by: str = ""
    requested_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "doctor_id": self.doctor_id,
            "version": self.version,
            "requested_by": self.requested_by,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
        }


@dataclass(frozen=True)
class DomainExplanation:
    """Explains why something happened using domain rules. Toda resposta é reproduzível."""
    question: str
    answer: str
    entity_type: str
    entity_id: int
    context: ExplanationContext
    steps: list[ExplanationStep] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    rules_applied: list[str] = field(default_factory=list)
    confidence: float = 1.0
    generated_at: datetime | None = None
    generated_by: str = "system"

    @property
    def is_reproducible(self) -> bool:
        return len(self.steps) > 0 and len(self.rules_applied) > 0

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.answer,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "context": self.context.to_dict(),
            "steps": [s.to_dict() for s in self.steps],
            "evidence": self.evidence,
            "rules_applied": self.rules_applied,
            "confidence": self.confidence,
            "is_reproducible": self.is_reproducible,
            "total_steps": self.total_steps,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "generated_by": self.generated_by,
        }


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
