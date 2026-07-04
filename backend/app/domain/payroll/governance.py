"""Governance domain objects — PayrollReadiness, ApprovalChecklist, AdministrativeApproval, AdministrativeLock, ApprovalSnapshot."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class ChecklistItemStatus(StrEnum):
    PENDING = "pending"
    SATISFIED = "satisfied"
    NOT_SATISFIED = "not_satisfied"
    WAIVED = "waived"


class ChecklistCategory(StrEnum):
    CALCULO = "calculo"
    SNAPSHOT_FINANCEIRO = "snapshot_financeiro"
    REMUNERACAO = "remuneracao"
    CONSISTENCIA = "consistencia"
    AUDITORIA = "auditoria"
    EXPLICACAO = "explicacao"


class ReadinessStatus(StrEnum):
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass
class ChecklistItem:
    """A single item in the approval checklist."""
    item_id: str
    description: str
    category: ChecklistCategory
    required: bool = True
    status: ChecklistItemStatus = ChecklistItemStatus.PENDING
    justification: str = ""
    checked_by: str = ""
    checked_at: datetime | None = None

    def satisfy(self, checked_by: str, justification: str = "") -> None:
        self.status = ChecklistItemStatus.SATISFIED
        self.checked_by = checked_by
        self.checked_at = datetime.utcnow()
        if justification:
            self.justification = justification

    def waive(self, checked_by: str, justification: str) -> None:
        if len(justification) < 10:
            raise ValueError("Justificativa deve ter mínimo de 10 caracteres")
        self.status = ChecklistItemStatus.WAIVED
        self.checked_by = checked_by
        self.checked_at = datetime.utcnow()
        self.justification = justification

    def fail(self, checked_by: str, justification: str = "") -> None:
        self.status = ChecklistItemStatus.NOT_SATISFIED
        self.checked_by = checked_by
        self.checked_at = datetime.utcnow()
        if justification:
            self.justification = justification

    @property
    def is_resolved(self) -> bool:
        return self.status in {
            ChecklistItemStatus.SATISFIED,
            ChecklistItemStatus.WAIVED,
        }

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "description": self.description,
            "category": self.category,
            "required": self.required,
            "status": self.status,
            "justification": self.justification,
            "checked_by": self.checked_by,
            "checked_at": self.checked_at.isoformat() if self.checked_at else None,
        }


@dataclass
class ReadinessItem:
    """A single readiness check result."""
    item_id: str
    description: str
    passed: bool
    message: str = ""

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "description": self.description,
            "passed": self.passed,
            "message": self.message,
        }


@dataclass
class PayrollReadiness:
    """Validates if a competency is ready for administrative closing.

    Does NOT alter state. Read-only validation component.
    """
    competency_id: int
    year_month: str
    version: int
    validated_at: datetime
    validated_by: str
    status: ReadinessStatus
    items: list[ReadinessItem] = field(default_factory=list)
    pending_count: int = 0

    @property
    def is_ready(self) -> bool:
        return self.status == ReadinessStatus.READY

    def add_item(self, item: ReadinessItem) -> None:
        self.items.append(item)
        if not item.passed:
            self.pending_count += 1

    def to_dict(self) -> dict:
        return {
            "competency_id": self.competency_id,
            "year_month": self.year_month,
            "version": self.version,
            "validated_at": self.validated_at.isoformat(),
            "validated_by": self.validated_by,
            "status": self.status,
            "items": [i.to_dict() for i in self.items],
            "pending_count": self.pending_count,
        }


@dataclass
class ApprovalChecklist:
    """Represents all criteria required before approval.

    Each item must be satisfied or waived before approval is allowed.
    """
    competency_id: int
    year_month: str
    version: int
    created_at: datetime
    created_by: str
    items: list[ChecklistItem] = field(default_factory=list)
    completed: bool = False
    completed_at: datetime | None = None
    completed_by: str = ""

    @property
    def total_items(self) -> int:
        return len(self.items)

    @property
    def satisfied_items(self) -> int:
        return sum(1 for i in self.items if i.is_resolved)

    @property
    def required_items(self) -> list[ChecklistItem]:
        return [i for i in self.items if i.required]

    @property
    def all_required_satisfied(self) -> bool:
        return all(i.is_resolved for i in self.required_items)

    @property
    def is_complete(self) -> bool:
        return self.all_required_satisfied and self.total_items > 0

    def get_item(self, item_id: str) -> ChecklistItem | None:
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def complete(self, completed_by: str) -> None:
        if not self.is_complete:
            unsatisfied = [
                i.item_id for i in self.required_items if not i.is_resolved
            ]
            raise ValueError(
                f"Checklist incompleto. Itens pendentes: {unsatisfied}"
            )
        self.completed = True
        self.completed_at = datetime.utcnow()
        self.completed_by = completed_by

    def to_dict(self) -> dict:
        return {
            "competency_id": self.competency_id,
            "year_month": self.year_month,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "items": [i.to_dict() for i in self.items],
            "total_items": self.total_items,
            "satisfied_items": self.satisfied_items,
            "completed": self.completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "completed_by": self.completed_by,
        }


@dataclass
class AdministrativeApproval:
    """Represents the administrative act of approval.

    Immutable after creation. Contains responsible, date, justification, version.
    """
    competency_id: int
    year_month: str
    version: int
    approved_by: str
    approved_at: datetime
    justification: str
    observations: str = ""
    checklist_version: int = 0

    def to_dict(self) -> dict:
        return {
            "competency_id": self.competency_id,
            "year_month": self.year_month,
            "version": self.version,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat(),
            "justification": self.justification,
            "observations": self.observations,
            "checklist_version": self.checklist_version,
        }


@dataclass
class AdministrativeLock:
    """Freezes the competency administratively.

    After created, no administrative alteration may occur.
    """
    competency_id: int
    year_month: str
    version: int
    locked_by: str
    locked_at: datetime
    justification: str = ""

    def to_dict(self) -> dict:
        return {
            "competency_id": self.competency_id,
            "year_month": self.year_month,
            "version": self.version,
            "locked_by": self.locked_by,
            "locked_at": self.locked_at.isoformat(),
            "justification": self.justification,
        }


@dataclass
class ApprovalSnapshot:
    """Freezes the complete state at approval time.

    Contains: version, user, timestamp, justification, checklist used.
    Immutable after creation.
    """
    competency_id: int
    year_month: str
    version: int
    snapshot_by: str
    snapshot_at: datetime
    justification: str
    approval: AdministrativeApproval
    lock: AdministrativeLock | None = None
    checklist: ApprovalChecklist | None = None

    def to_dict(self) -> dict:
        return {
            "competency_id": self.competency_id,
            "year_month": self.year_month,
            "version": self.version,
            "snapshot_by": self.snapshot_by,
            "snapshot_at": self.snapshot_at.isoformat(),
            "justification": self.justification,
            "approval": self.approval.to_dict(),
            "lock": self.lock.to_dict() if self.lock else None,
            "checklist": self.checklist.to_dict() if self.checklist else None,
        }
