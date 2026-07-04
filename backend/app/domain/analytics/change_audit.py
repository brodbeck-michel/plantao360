"""ChangeAudit — Audit data for changes."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ChangeAudit:
    """Audit data for changes made to entities."""
    entity_type: str
    entity_id: int
    change_type: str
    changed_by: str
    changed_at: str
    previous_status: str
    new_status: str
    details: str = ""
    is_after_lock: bool = False
    is_after_approval: bool = False

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "change_type": self.change_type,
            "changed_by": self.changed_by,
            "changed_at": self.changed_at,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "details": self.details,
            "is_after_lock": self.is_after_lock,
            "is_after_approval": self.is_after_approval,
        }
