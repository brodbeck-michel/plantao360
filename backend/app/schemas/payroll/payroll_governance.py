"""Governance DTOs — PayrollReadiness, ApprovalChecklist, AdministrativeApproval, AdministrativeLock, ApprovalSnapshot."""

from datetime import datetime
from pydantic import BaseModel, Field


class ReadinessItemDTO(BaseModel):
    item_id: str
    description: str
    passed: bool
    message: str = ""


class PayrollReadinessDTO(BaseModel):
    competency_id: int
    year_month: str
    version: int
    validated_at: datetime
    validated_by: str
    status: str
    items: list[ReadinessItemDTO]
    pending_count: int


class ChecklistItemDTO(BaseModel):
    item_id: str
    description: str
    category: str
    required: bool = True
    status: str = "pending"
    justification: str = ""
    checked_by: str = ""
    checked_at: datetime | None = None


class ApprovalChecklistDTO(BaseModel):
    competency_id: int
    year_month: str
    version: int
    created_at: datetime
    created_by: str
    items: list[ChecklistItemDTO]
    total_items: int
    satisfied_items: int
    completed: bool
    completed_at: datetime | None = None
    completed_by: str = ""


class AdministrativeApprovalDTO(BaseModel):
    competency_id: int
    year_month: str
    version: int
    approved_by: str
    approved_at: datetime
    justification: str
    observations: str = ""
    checklist_version: int = 0


class AdministrativeLockDTO(BaseModel):
    competency_id: int
    year_month: str
    version: int
    locked_by: str
    locked_at: datetime
    justification: str = ""


class ApprovalSnapshotDTO(BaseModel):
    competency_id: int
    year_month: str
    version: int
    snapshot_by: str
    snapshot_at: datetime
    justification: str
    approval: AdministrativeApprovalDTO
    lock: AdministrativeLockDTO | None = None
    checklist: ApprovalChecklistDTO | None = None


class PayrollApprovalDTO(BaseModel):
    approved_by: str = Field(default="system", max_length=100)
    justification: str = Field(..., min_length=1, max_length=500, description="Justificativa da aprovação")
    observations: str = Field(default="", max_length=1000)


class PayrollLockDTO(BaseModel):
    locked_by: str = Field(default="system", max_length=100)
    justification: str = Field(default="", max_length=500)


class PayrollUnlockDTO(BaseModel):
    unlocked_by: str = Field(default="system", max_length=100)
    justification: str = Field(..., min_length=10, max_length=500)


class ChecklistItemUpdateDTO(BaseModel):
    item_id: str
    status: str = Field(..., description="satisfied | not_satisfied | waived")
    justification: str = Field(default="", max_length=500)
    checked_by: str = Field(default="system", max_length=100)
