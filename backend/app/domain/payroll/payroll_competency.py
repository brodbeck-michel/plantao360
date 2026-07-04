"""Payroll domain objects — PayrollCompetency, PayrollVersion, PayrollSeal, PayrollExplanation, PayrollAuditSnapshot."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.constants.payroll_status import PayrollStatus
from app.domain.remuneration.remuneration_result import RemunerationResult, DoctorRemuneration
from app.domain.remuneration.remuneration_rule import RemunerationRule
from app.domain.financial.financial_snapshot_builder import FinancialSnapshotData
from app.domain.state_machines.payroll_state_machine import PayrollStateMachine
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


@dataclass
class PayrollVersion:
    """Immutable version of a payroll competency state.

    Created each time a competency is calculated or reopened.
    Never modified after creation.
    """
    version_number: int
    created_at: datetime
    financial_snapshot: FinancialSnapshotData
    remuneration_result: RemunerationResult
    rules_applied: list[RemunerationRule] = field(default_factory=list)
    created_by: str = "system"
    reopen_reason: str | None = None

    def to_dict(self) -> dict:
        return {
            "version_number": self.version_number,
            "created_at": self.created_at.isoformat(),
            "total_facts": self.financial_snapshot.total_facts,
            "total_value": self.remuneration_result.total_value,
            "total_doctors": len(self.remuneration_result.doctor_results),
            "rules_count": len(self.rules_applied),
            "created_by": self.created_by,
            "reopen_reason": self.reopen_reason,
        }


@dataclass
class PayrollSeal:
    """Immutable seal created upon approval.

    Contains complete snapshot for future reproduction.
    Cannot be modified after creation.
    """
    sealed_at: datetime
    sealed_by: str
    version_number: int
    financial_snapshot: FinancialSnapshotData
    remuneration_result: RemunerationResult
    rules_applied: list[RemunerationRule] = field(default_factory=list)
    total_value: float = 0.0
    total_doctors: int = 0
    total_facts: int = 0

    def to_dict(self) -> dict:
        return {
            "sealed_at": self.sealed_at.isoformat(),
            "sealed_by": self.sealed_by,
            "version_number": self.version_number,
            "total_value": self.total_value,
            "total_doctors": self.total_doctors,
            "total_facts": self.total_facts,
            "rules_count": len(self.rules_applied),
        }


@dataclass
class ExplanationStep:
    """A single step in payroll explanation."""
    step_number: int
    description: str
    doctor_id: int
    fact_type: str
    rule_id: str
    rule_version: str
    hour_rate: float
    multiplier: float
    duration_minutes: int
    total_value: float


@dataclass
class PayrollExplanation:
    """Explains how a payroll was calculated, step by step.

    Immutable after creation.
    """
    created_at: datetime
    steps: list[ExplanationStep] = field(default_factory=list)
    total_value: float = 0.0
    total_doctors: int = 0
    total_facts: int = 0

    def add_step(self, step: ExplanationStep) -> None:
        self.steps.append(step)
        self.total_value += step.total_value

    def to_dict(self) -> dict:
        return {
            "created_at": self.created_at.isoformat(),
            "steps_count": len(self.steps),
            "total_value": self.total_value,
            "total_doctors": self.total_doctors,
            "total_facts": self.total_facts,
            "steps": [
                {
                    "step": s.step_number,
                    "description": s.description,
                    "doctor_id": s.doctor_id,
                    "fact_type": s.fact_type,
                    "rule_id": s.rule_id,
                    "rule_version": s.rule_version,
                    "hour_rate": s.hour_rate,
                    "multiplier": s.multiplier,
                    "duration_minutes": s.duration_minutes,
                    "total_value": s.total_value,
                }
                for s in self.steps
            ],
        }


@dataclass
class AuditEntry:
    """Single audit trail entry."""
    timestamp: datetime
    action: str
    performed_by: str
    previous_status: str
    new_status: str
    details: str = ""


@dataclass
class PayrollAuditSnapshot:
    """Complete audit trail for a payroll competency.

    Append-only: entries cannot be modified after creation.
    """
    entries: list[AuditEntry] = field(default_factory=list)

    def add_entry(self, entry: AuditEntry) -> None:
        self.entries.append(entry)

    def to_dict(self) -> dict:
        return {
            "entries_count": len(self.entries),
            "entries": [
                {
                    "timestamp": e.timestamp.isoformat(),
                    "action": e.action,
                    "performed_by": e.performed_by,
                    "previous_status": e.previous_status,
                    "new_status": e.new_status,
                    "details": e.details,
                }
                for e in self.entries
            ],
        }


class PayrollCompetency(AggregateRoot):
    """Aggregate Root representing an official financial competency.

    Responsible for:
    - Lifecycle management
    - Versioning
    - Snapshots
    - Audit trail
    - Administrative governance (readiness, checklist, approval, lock)
    """

    def __init__(
        self,
        period_id: int,
        year_month: str,
        created_by: str = "system",
    ) -> None:
        super().__init__()
        self.period_id: int = period_id
        self.year_month: str = year_month
        self.status: PayrollStatus = PayrollStatus.DRAFT
        self.created_by: str = created_by
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
        self.current_version: int = 1
        self.versions: list[PayrollVersion] = []
        self.seal: PayrollSeal | None = None
        self.explanation: PayrollExplanation | None = None
        self.audit: PayrollAuditSnapshot = PayrollAuditSnapshot()
        self.reopen_count: int = 0
        self.reopen_reason: str | None = None

        # Governance fields
        self.readiness: PayrollReadiness | None = None
        self.checklist: ApprovalChecklist | None = None
        self.administrative_approval: AdministrativeApproval | None = None
        self.administrative_lock: AdministrativeLock | None = None
        self.approval_snapshot: ApprovalSnapshot | None = None

        self._state_machine = PayrollStateMachine(self)

        self.add_event("payroll.created.v1", {
            "period_id": period_id,
            "year_month": year_month,
        })

    @property
    def total_value(self) -> float:
        if self.seal:
            return self.seal.total_value
        if self.versions:
            return self.versions[-1].remuneration_result.total_value
        return 0.0

    @property
    def is_approved(self) -> bool:
        return self.status == PayrollStatus.APPROVED

    @property
    def is_locked(self) -> bool:
        return self.status == PayrollStatus.LOCKED

    @property
    def is_sealed(self) -> bool:
        return self.seal is not None

    @property
    def is_administratively_closed(self) -> bool:
        return (
            self.administrative_approval is not None
            and self.approval_snapshot is not None
        )

    def calculate(
        self,
        financial_snapshot: FinancialSnapshotData,
        remuneration_result: RemunerationResult,
        rules_applied: list[RemunerationRule] | None = None,
    ) -> None:
        """Calculate competency from financial snapshot and remuneration result."""
        self._state_machine.calculate()

        version = PayrollVersion(
            version_number=self.current_version,
            created_at=datetime.utcnow(),
            financial_snapshot=financial_snapshot,
            remuneration_result=remuneration_result,
            rules_applied=rules_applied or [],
            created_by=self.created_by,
        )
        self.versions.append(version)

        self._build_explanation(remuneration_result)
        self._record_audit("calculated", "System calculated competency")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.calculated.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "total_value": remuneration_result.total_value,
        })

    def review(self, reviewed_by: str = "system") -> None:
        """Review competency (validate calculations)."""
        self._state_machine.review()
        self._record_audit("reviewed", f"Reviewed by {reviewed_by}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.reviewed.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
        })

    def approve(self, approved_by: str = "system") -> None:
        """Approve competency — creates immutable seal."""
        self._state_machine.approve()

        if self.versions:
            latest = self.versions[-1]
            self.seal = PayrollSeal(
                sealed_at=datetime.utcnow(),
                sealed_by=approved_by,
                version_number=latest.version_number,
                financial_snapshot=latest.financial_snapshot,
                remuneration_result=latest.remuneration_result,
                rules_applied=latest.rules_applied,
                total_value=latest.remuneration_result.total_value,
                total_doctors=len(latest.remuneration_result.doctor_results),
                total_facts=latest.remuneration_result.total_facts,
            )

        self._record_audit("approved", f"Approved by {approved_by}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.approved.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "total_value": self.total_value,
        })

    def lock(self, locked_by: str = "system", justification: str = "") -> None:
        """Lock competency administratively — freezes all changes."""
        self._state_machine.lock()

        self.administrative_lock = AdministrativeLock(
            competency_id=self.aggregate_id or 0,
            year_month=self.year_month,
            version=self.current_version,
            locked_by=locked_by,
            locked_at=datetime.utcnow(),
            justification=justification,
        )

        self._record_audit("locked", f"Locked by {locked_by}: {justification}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.locked.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "locked_by": locked_by,
        })

    def unlock(self, unlocked_by: str = "system", justification: str = "") -> None:
        """Unlock competency — removes administrative lock."""
        self._state_machine.unlock()
        self.administrative_lock = None

        self._record_audit("unlocked", f"Unlocked by {unlocked_by}: {justification}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.unlocked.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "unlocked_by": unlocked_by,
        })

    def export(self, exported_by: str = "system") -> None:
        """Export competency to external system."""
        self._state_machine.export()
        self._record_audit("exported", f"Exported by {exported_by}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.exported.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
        })

    def mark_paid(self, paid_by: str = "system") -> None:
        """Mark competency as paid."""
        self._state_machine.mark_paid()
        self._record_audit("paid", f"Marked as paid by {paid_by}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.paid.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
        })

    def archive(self) -> None:
        """Archive competency (automatic after 30 days in paid)."""
        self._state_machine.archive()
        self._record_audit("archived", "System archived competency")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.archived.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
        })

    def reopen(self, reason: str, reopened_by: str = "system") -> None:
        """Reopen competency — creates new version."""
        self._state_machine.reopen()

        self.reopen_count += 1
        self.reopen_reason = reason
        self.current_version += 1
        self.seal = None
        self.explanation = None
        self.readiness = None
        self.checklist = None
        self.administrative_approval = None
        self.administrative_lock = None
        self.approval_snapshot = None

        self._record_audit("reopened", f"Reopened by {reopened_by}: {reason}")
        self.updated_at = datetime.utcnow()

        self.add_event("payroll.reopened.v1", {
            "period_id": self.period_id,
            "previous_version": self.current_version - 1,
            "new_version": self.current_version,
            "reason": reason,
        })

    # --- Governance methods ---

    def validate_readiness(self, validated_by: str = "system") -> PayrollReadiness:
        """Validate if the competency is ready for administrative closing.

        Does NOT alter state. Returns readiness assessment.
        """
        items = []

        # CLC-01: Competência calculada
        clc01_passed = self.status in {
            PayrollStatus.CALCULATED,
            PayrollStatus.REVIEWED,
        }
        items.append(ReadinessItem(
            item_id="CLC-01",
            description="Competência calculada",
            passed=clc01_passed,
            message="" if clc01_passed else "Competência não está em estado calculated ou reviewed",
        ))

        # CLC-02: Versão válida
        clc02_passed = len(self.versions) > 0
        items.append(ReadinessItem(
            item_id="CLC-02",
            description="Versão válida",
            passed=clc02_passed,
            message="" if clc02_passed else "Competência não possui versões",
        ))

        # SNF-01: Snapshot financeiro presente
        active_version = self.get_active_version()
        snf01_passed = active_version is not None and active_version.financial_snapshot is not None
        items.append(ReadinessItem(
            item_id="SNF-01",
            description="Snapshot financeiro presente",
            passed=snf01_passed,
            message="" if snf01_passed else "Snapshot financeiro não encontrado",
        ))

        # REM-01: Resultado de remuneração presente
        rem01_passed = active_version is not None and active_version.remuneration_result is not None
        items.append(ReadinessItem(
            item_id="REM-01",
            description="Resultado de remuneração presente",
            passed=rem01_passed,
            message="" if rem01_passed else "Resultado de remuneração não encontrado",
        ))

        # CON-01: Sem inconsistências críticas (placeholder — depends on external data)
        con01_passed = True
        items.append(ReadinessItem(
            item_id="CON-01",
            description="Sem inconsistências críticas",
            passed=con01_passed,
            message="",
        ))

        # AUD-01: Trail completo
        aud01_passed = len(self.audit.entries) > 0
        items.append(ReadinessItem(
            item_id="AUD-01",
            description="Trail de auditoria presente",
            passed=aud01_passed,
            message="" if aud01_passed else "Trail de auditoria vazio",
        ))

        # EXP-01: Explicação presente
        exp01_passed = self.explanation is not None
        items.append(ReadinessItem(
            item_id="EXP-01",
            description="Explicação presente",
            passed=exp01_passed,
            message="" if exp01_passed else "Explicação não encontrada",
        ))

        pending_count = sum(1 for i in items if not i.passed)
        status = ReadinessStatus.READY if pending_count == 0 else ReadinessStatus.NOT_READY

        readiness = PayrollReadiness(
            competency_id=self.aggregate_id or 0,
            year_month=self.year_month,
            version=self.current_version,
            validated_at=datetime.utcnow(),
            validated_by=validated_by,
            status=status,
            items=items,
            pending_count=pending_count,
        )

        self.readiness = readiness

        self.add_event("payroll.ready.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "status": status,
            "pending_count": pending_count,
        })

        return readiness

    def build_checklist(self, created_by: str = "system") -> ApprovalChecklist:
        """Build the approval checklist from readiness assessment."""
        if self.readiness is None:
            raise ValueError("Readiness deve ser validado antes de construir checklist")

        items = [
            ChecklistItem(
                item_id="CLC-01",
                description="Competência calculada",
                category=ChecklistCategory.CALCULO,
                required=True,
            ),
            ChecklistItem(
                item_id="CLC-02",
                description="Versão válida",
                category=ChecklistCategory.CALCULO,
                required=True,
            ),
            ChecklistItem(
                item_id="SNF-01",
                description="Snapshot financeiro íntegro",
                category=ChecklistCategory.SNAPSHOT_FINANCEIRO,
                required=True,
            ),
            ChecklistItem(
                item_id="REM-01",
                description="Remunerações válidas",
                category=ChecklistCategory.REMUNERACAO,
                required=True,
            ),
            ChecklistItem(
                item_id="CON-01",
                description="Sem inconsistências críticas",
                category=ChecklistCategory.CONSISTENCIA,
                required=True,
            ),
            ChecklistItem(
                item_id="AUD-01",
                description="Trail de auditoria completo",
                category=ChecklistCategory.AUDITORIA,
                required=True,
            ),
            ChecklistItem(
                item_id="EXP-01",
                description="Explicação presente",
                category=ChecklistCategory.EXPLICACAO,
                required=True,
            ),
        ]

        # Auto-satisfy items based on readiness
        for item in items:
            readiness_item = next(
                (r for r in self.readiness.items if r.item_id == item.item_id),
                None,
            )
            if readiness_item and readiness_item.passed:
                item.satisfy(checked_by="system", justification="Auto-validado pelo PayrollReadiness")

        checklist = ApprovalChecklist(
            competency_id=self.aggregate_id or 0,
            year_month=self.year_month,
            version=self.current_version,
            created_at=datetime.utcnow(),
            created_by=created_by,
            items=items,
        )

        self.checklist = checklist

        self.add_event("payroll.checklist.completed.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "total_items": checklist.total_items,
            "satisfied_items": checklist.satisfied_items,
        })

        return checklist

    def request_approval(
        self,
        requested_by: str = "system",
        justification: str = "",
    ) -> None:
        """Request administrative approval."""
        if self.readiness is None or not self.readiness.is_ready:
            raise ValueError("Readiness deve estar ready para solicitar aprovação")
        if self.checklist is None or not self.checklist.is_complete:
            raise ValueError("Checklist deve estar completo para solicitar aprovação")

        self._record_audit(
            "approval_requested",
            f"Approval requested by {requested_by}: {justification}",
        )

        self.add_event("payroll.approval.requested.v1", {
            "period_id": self.period_id,
            "version": self.current_version,
            "requested_by": requested_by,
        })

    def approve_administratively(
        self,
        approved_by: str = "system",
        justification: str = "",
        observations: str = "",
    ) -> AdministrativeApproval:
        """Approve competency administratively — full governance process."""
        # Validate prerequisites
        if self.readiness is None or not self.readiness.is_ready:
            raise ValueError("Readiness deve estar ready para aprovação")
        if self.checklist is None or not self.checklist.is_complete:
            raise ValueError("Checklist deve estar completo para aprovação")

        # Core approval (creates seal)
        self.approve(approved_by=approved_by)

        # Create administrative approval
        self.administrative_approval = AdministrativeApproval(
            competency_id=self.aggregate_id or 0,
            year_month=self.year_month,
            version=self.current_version,
            approved_by=approved_by,
            approved_at=datetime.utcnow(),
            justification=justification,
            observations=observations,
            checklist_version=self.current_version,
        )

        # Create approval snapshot
        self.approval_snapshot = ApprovalSnapshot(
            competency_id=self.aggregate_id or 0,
            year_month=self.year_month,
            version=self.current_version,
            snapshot_by=approved_by,
            snapshot_at=datetime.utcnow(),
            justification=justification,
            approval=self.administrative_approval,
            checklist=self.checklist,
        )

        self._record_audit(
            "administratively_approved",
            f"Administratively approved by {approved_by}: {justification}",
        )

        return self.administrative_approval

    def get_active_version(self) -> PayrollVersion | None:
        """Get the current active version."""
        if self.versions:
            return self.versions[-1]
        return None

    def get_version(self, version_number: int) -> PayrollVersion | None:
        """Get a specific version by number."""
        for v in self.versions:
            if v.version_number == version_number:
                return v
        return None

    def _build_explanation(self, result: RemunerationResult) -> None:
        """Build explanation from remuneration result."""
        self.explanation = PayrollExplanation(
            created_at=datetime.utcnow(),
            total_value=result.total_value,
            total_doctors=len(result.doctor_results),
            total_facts=result.total_facts,
        )

        step_number = 0
        for doctor_result in result.doctor_results:
            for calc in doctor_result.calculations:
                step_number += 1
                step = ExplanationStep(
                    step_number=step_number,
                    description=f"Fact {calc.fact_id} ({calc.fact_type}) for doctor {calc.doctor_id}",
                    doctor_id=calc.doctor_id,
                    fact_type=calc.fact_type,
                    rule_id=calc.rule_id,
                    rule_version=calc.rule_version,
                    hour_rate=calc.hour_rate,
                    multiplier=calc.multiplier,
                    duration_minutes=calc.duration_minutes,
                    total_value=calc.total_value,
                )
                self.explanation.add_step(step)

    def _record_audit(self, action: str, details: str) -> None:
        """Record an audit entry."""
        entry = AuditEntry(
            timestamp=datetime.utcnow(),
            action=action,
            performed_by=self.created_by,
            previous_status=self.status,
            new_status=self.status,
            details=details,
        )
        self.audit.add_entry(entry)

    def before_transition(self, from_status: str, to_status: str) -> None:
        pass

    def after_transition(self, from_status: str, to_status: str) -> None:
        pass
