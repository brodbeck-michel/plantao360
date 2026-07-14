"""Query Services — Read-only services for the query domain."""


from app.domain.read_models.doctor_summary import DoctorSummary
from app.domain.read_models.coverage_summary import CoverageSummary
from app.domain.read_models.financial_summary import FinancialSummary
from app.domain.read_models.payroll_summary import PayrollSummary


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


# Query objects — antes em domain/query (consumidores: este service + rotas de API que agora
# importam daqui). Inlinados no colapso da domain/ (spec 005, Grupo D).
@dataclass(frozen=True)
class DoctorAnalyticsQuery:
    """Represents a business question about doctors."""
    doctor_id: int | None = None
    active_only: bool = True
    period_id: int | None = None
    year_month: str | None = None
    include_totals: bool = True
    include_remuneration: bool = False
    include_shifts: bool = True
    sort_by: str = "name"
    sort_direction: str = "asc"

    def to_dict(self) -> dict:
        return {
            "doctor_id": self.doctor_id,
            "active_only": self.active_only,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "include_totals": self.include_totals,
            "include_remuneration": self.include_remuneration,
            "include_shifts": self.include_shifts,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }


@dataclass(frozen=True)
class CoverageAnalyticsQuery:
    """Represents a business question about coverage."""
    period_id: int | None = None
    year_month: str | None = None
    shift_type: str | None = None
    include_inconsistencies: bool = True
    include_extras: bool = True
    include_uncovered: bool = False
    doctor_id: int | None = None
    sort_by: str = "shift_date"
    sort_direction: str = "asc"

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "shift_type": self.shift_type,
            "include_inconsistencies": self.include_inconsistencies,
            "include_extras": self.include_extras,
            "include_uncovered": self.include_uncovered,
            "doctor_id": self.doctor_id,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }


@dataclass(frozen=True)
class FinancialAnalyticsQuery:
    """Represents a business question about financial data."""
    period_id: int | None = None
    year_month: str | None = None
    doctor_id: int | None = None
    fact_type: str | None = None
    include_rules: bool = True
    include_explanations: bool = False
    include_version_comparison: bool = False
    compare_versions: list[int] = field(default_factory=list)
    sort_by: str = "total_value"
    sort_direction: str = "desc"

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "doctor_id": self.doctor_id,
            "fact_type": self.fact_type,
            "include_rules": self.include_rules,
            "include_explanations": self.include_explanations,
            "include_version_comparison": self.include_version_comparison,
            "compare_versions": self.compare_versions,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }


@dataclass(frozen=True)
class PayrollAnalyticsQuery:
    """Represents a business question about payroll competencies."""
    payroll_id: int | None = None
    period_id: int | None = None
    year_month: str | None = None
    status: str | None = None
    include_audit: bool = True
    include_versions: bool = False
    include_seal: bool = False
    include_checklist: bool = False
    include_approval: bool = False
    include_timeline: bool = False
    sort_by: str = "year_month"
    sort_direction: str = "desc"

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "status": self.status,
            "include_audit": self.include_audit,
            "include_versions": self.include_versions,
            "include_seal": self.include_seal,
            "include_checklist": self.include_checklist,
            "include_approval": self.include_approval,
            "include_timeline": self.include_timeline,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }


@dataclass(frozen=True)
class TimelineQuery:
    """Represents a business question about the timeline of an entity."""
    entity_type: str = ""
    entity_id: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    from_date: str | None = None
    to_date: str | None = None
    event_type: str | None = None
    include_events: bool = True
    include_status_changes: bool = True
    include_audit: bool = False
    include_version_changes: bool = False
    event_types: list[str] = field(default_factory=list)
    limit: int = 50
    offset: int = 0
    sort_by: str = "timestamp"
    sort_direction: str = "asc"

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "event_type": self.event_type,
            "include_events": self.include_events,
            "include_status_changes": self.include_status_changes,
            "include_audit": self.include_audit,
            "include_version_changes": self.include_version_changes,
            "event_types": self.event_types,
            "limit": self.limit,
            "offset": self.offset,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
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


# Audit analytics value objects — antes em domain/analytics (consumidor único: este service).
# Inlinados aqui no colapso da domain/ (spec 004, Grupo B).
@dataclass(frozen=True)
class ReopenedCompetency:
    """Record of a reopened competency."""
    payroll_id: int
    year_month: str
    reopened_by: str
    reopened_at: str
    reason: str
    previous_version: int
    new_version: int

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "year_month": self.year_month,
            "reopened_by": self.reopened_by,
            "reopened_at": self.reopened_at,
            "reason": self.reason,
            "previous_version": self.previous_version,
            "new_version": self.new_version,
        }


@dataclass(frozen=True)
class ApprovalRecord:
    """Record of an approval."""
    payroll_id: int
    year_month: str
    approved_by: str
    approved_at: str
    version: int
    checklist_complete: bool

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "year_month": self.year_month,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "version": self.version,
            "checklist_complete": self.checklist_complete,
        }


@dataclass(frozen=True)
class AuditAnalytics:
    """Audit analytics results."""
    total_competencies: int = 0
    reopened_competencies: list[ReopenedCompetency] = field(default_factory=list)
    reopen_count: int = 0
    reopen_rate: float = 0.0
    approvals: list[ApprovalRecord] = field(default_factory=list)
    average_time_to_close_days: float = 0.0
    average_time_to_approve_days: float = 0.0
    segregation_violations: int = 0
    changes_after_lock: int = 0
    audit_trail_integrity: bool = True
    generated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "total_competencies": self.total_competencies,
            "reopened_competencies": [r.to_dict() for r in self.reopened_competencies],
            "reopen_count": self.reopen_count,
            "reopen_rate": self.reopen_rate,
            "approvals": [a.to_dict() for a in self.approvals],
            "average_time_to_close_days": self.average_time_to_close_days,
            "average_time_to_approve_days": self.average_time_to_approve_days,
            "segregation_violations": self.segregation_violations,
            "changes_after_lock": self.changes_after_lock,
            "audit_trail_integrity": self.audit_trail_integrity,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


# KPI value objects — antes em domain/kpi (consumidor único: este service).
# Inlinados aqui no colapso da domain/ (spec 004, Grupo B).
@dataclass(frozen=True)
class CoverageKPI:
    """Coverage Key Performance Indicator."""
    period_id: int
    year_month: str
    coverage_rate: float = 0.0
    total_shifts: int = 0
    covered_shifts: int = 0
    uncovered_shifts: int = 0
    coverage_by_type: dict[str, float] = field(default_factory=dict)
    coverage_by_day: list[dict] = field(default_factory=list)
    trend: str = "stable"
    previous_period_rate: float | None = None
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Percentual de plantões com ao menos um médico atribuído"

    @property
    def formula(self) -> str:
        return "covered_shifts / total_shifts * 100"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de plantões: {self.total_shifts}",
            f"Plantões cobertos: {self.covered_shifts}",
            f"Plantões descobertos: {self.uncovered_shifts}",
        ]

    @property
    def explanation(self) -> str:
        if self.coverage_rate >= 90:
            return "Cobertura adequada. A maioria dos plantões possui médicos atribuídos."
        elif self.coverage_rate >= 70:
            return "Cobertura parcial. Alguns plantões precisam de atenção."
        else:
            return "Cobertura insuficiente. Ação urgente necessária para evitar descobertos."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "coverage_rate": self.coverage_rate,
            "total_shifts": self.total_shifts,
            "covered_shifts": self.covered_shifts,
            "uncovered_shifts": self.uncovered_shifts,
            "coverage_by_type": self.coverage_by_type,
            "coverage_by_day": self.coverage_by_day,
            "trend": self.trend,
            "previous_period_rate": self.previous_period_rate,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


@dataclass(frozen=True)
class FinancialKPI:
    """Financial Key Performance Indicator."""
    period_id: int
    year_month: str
    total_remuneration: float = 0.0
    cost_per_shift: float = 0.0
    cost_per_doctor: float = 0.0
    cost_per_hour: float = 0.0
    total_hours: float = 0.0
    total_shifts: int = 0
    total_doctors: int = 0
    cost_by_type: dict[str, float] = field(default_factory=dict)
    cost_by_doctor: list[dict] = field(default_factory=list)
    trend: str = "stable"
    previous_period_total: float | None = None
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Indicadores financeiros consolidados do período"

    @property
    def formula(self) -> str:
        return "cost_per_shift = total_remuneration / total_shifts"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de remunerações: R$ {self.total_remuneration:.2f}",
            f"Total de plantões: {self.total_shifts}",
            f"Total de horas: {self.total_hours:.1f}",
            f"Total de médicos: {self.total_doctors}",
        ]

    @property
    def explanation(self) -> str:
        if self.previous_period_total and self.total_remuneration > self.previous_period_total:
            pct = ((self.total_remuneration - self.previous_period_total) / self.previous_period_total) * 100
            return f"Custo aumentou {pct:.1f}% em relação ao período anterior."
        elif self.previous_period_total and self.total_remuneration < self.previous_period_total:
            pct = ((self.previous_period_total - self.total_remuneration) / self.previous_period_total) * 100
            return f"Custo diminuiu {pct:.1f}% em relação ao período anterior."
        return "Custo dentro do esperado para o período."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "total_remuneration": self.total_remuneration,
            "cost_per_shift": self.cost_per_shift,
            "cost_per_doctor": self.cost_per_doctor,
            "cost_per_hour": self.cost_per_hour,
            "total_hours": self.total_hours,
            "total_shifts": self.total_shifts,
            "total_doctors": self.total_doctors,
            "cost_by_type": self.cost_by_type,
            "cost_by_doctor": self.cost_by_doctor,
            "trend": self.trend,
            "previous_period_total": self.previous_period_total,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


@dataclass(frozen=True)
class PayrollKPI:
    """Payroll Key Performance Indicator."""
    period_id: int
    year_month: str
    total_competencies: int = 0
    approved_competencies: int = 0
    pending_competencies: int = 0
    reopened_competencies: int = 0
    average_time_to_close_days: float = 0.0
    average_time_to_approve_days: float = 0.0
    reopen_rate: float = 0.0
    approval_rate: float = 0.0
    total_versions: int = 0
    average_versions_per_competency: float = 0.0
    trend: str = "stable"
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Indicadores de desempenho do processo de folha de pagamento"

    @property
    def formula(self) -> str:
        return "reopen_rate = reopened_competencies / total_competencies * 100"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de competências: {self.total_competencies}",
            f"Aprovadas: {self.approved_competencies}",
            f"Pendentes: {self.pending_competencies}",
            f"Reabertas: {self.reopened_competencies}",
        ]

    @property
    def explanation(self) -> str:
        if self.reopen_rate > 20:
            return "Taxa de reabertura alta. Processo de validação pode precisar de melhoria."
        elif self.reopen_rate > 10:
            return "Taxa de reabertura moderada. Monitorar tendências."
        return "Taxa de reabertura dentro do esperado."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "total_competencies": self.total_competencies,
            "approved_competencies": self.approved_competencies,
            "pending_competencies": self.pending_competencies,
            "reopened_competencies": self.reopened_competencies,
            "average_time_to_close_days": self.average_time_to_close_days,
            "average_time_to_approve_days": self.average_time_to_approve_days,
            "reopen_rate": self.reopen_rate,
            "approval_rate": self.approval_rate,
            "total_versions": self.total_versions,
            "average_versions_per_competency": self.average_versions_per_competency,
            "trend": self.trend,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


@dataclass(frozen=True)
class OperationalKPI:
    """Operational Key Performance Indicator."""
    period_id: int
    year_month: str
    total_shifts: int = 0
    total_doctors: int = 0
    total_hours: float = 0.0
    total_extras: int = 0
    extras_approved: int = 0
    extras_rejected: int = 0
    extras_pending: int = 0
    extra_approval_rate: float = 0.0
    doctors_per_shift: float = 0.0
    hours_per_doctor: float = 0.0
    average_assignment_duration: float = 0.0
    utilization_rate: float = 0.0
    trend: str = "stable"
    generated_at: datetime | None = None

    @property
    def definition(self) -> str:
        return "Indicadores de desempenho operacional da instituição"

    @property
    def formula(self) -> str:
        return "doctors_per_shift = total_doctors / total_shifts"

    @property
    def evidence(self) -> list[str]:
        return [
            f"Total de plantões: {self.total_shifts}",
            f"Total de médicos: {self.total_doctors}",
            f"Total de horas: {self.total_hours:.1f}",
            f"Total de extras: {self.total_extras}",
        ]

    @property
    def explanation(self) -> str:
        if self.extra_approval_rate > 80:
            return "Taxa de aprovação de extras alta. Processo de solicitação bem definido."
        elif self.extra_approval_rate > 50:
            return "Taxa de aprovação de extras moderada. Revisar critérios de aprovação."
        return "Taxa de aprovação de extras baixa. Verificar processos de solicitação."

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "total_shifts": self.total_shifts,
            "total_doctors": self.total_doctors,
            "total_hours": self.total_hours,
            "total_extras": self.total_extras,
            "extras_approved": self.extras_approved,
            "extras_rejected": self.extras_rejected,
            "extras_pending": self.extras_pending,
            "extra_approval_rate": self.extra_approval_rate,
            "doctors_per_shift": self.doctors_per_shift,
            "hours_per_doctor": self.hours_per_doctor,
            "average_assignment_duration": self.average_assignment_duration,
            "utilization_rate": self.utilization_rate,
            "trend": self.trend,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "explanation": self.explanation,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
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
