"""Coverage Engine — Consolida fatos operacionais em fatos financeiros."""

from dataclasses import dataclass, field
from datetime import datetime

from app.models.shift import Shift
from app.models.shift_part import ShiftPart
from app.models.shift_extra import ShiftExtra
from app.models.doctor import Doctor
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.constants.extra_status import ExtraStatus
from app.domain.constants.inconsistency_type import InconsistencyType


@dataclass
class CoverageFact:
    """Represents a consolidated coverage fact."""
    doctor_id: int
    fact_type: str
    duration_minutes: int
    source_event: str
    source_id: int


@dataclass
class CoverageInconsistency:
    """Represents an inconsistency detected during consolidation."""
    inconsistency_type: str
    entity_type: str
    entity_id: int
    details: str


@dataclass
class CoverageResult:
    """Result of coverage consolidation for a single shift."""
    shift_id: int
    facts: list[CoverageFact] = field(default_factory=list)
    inconsistencies: list[CoverageInconsistency] = field(default_factory=list)

    @property
    def total_facts(self) -> int:
        return len(self.facts)

    @property
    def total_inconsistencies(self) -> int:
        return len(self.inconsistencies)

    @property
    def total_duration_minutes(self) -> int:
        return sum(f.duration_minutes for f in self.facts)


class CoverageEngine:
    """Consolidates operational facts into financial facts.

    The Coverage Engine does NOT calculate values.
    It only identifies, validates, and registers eligible operational facts.
    """

    def consolidate_shift(self, shift: Shift) -> CoverageResult:
        """Consolidate coverage for a single shift."""
        result = CoverageResult(shift_id=shift.id)

        for assignment in shift.shift_parts:
            self._process_assignment(assignment, shift, result)

        for extra in shift.shift_extras:
            self._process_extra(extra, shift, result)

        return result

    def _process_assignment(
        self, assignment: ShiftPart, shift: Shift, result: CoverageResult
    ) -> None:
        """Process a single assignment for coverage consolidation."""
        if assignment.status != AssignmentStatus.COMPLETED:
            return

        if shift.status == ShiftStatus.CANCELLED:
            result.inconsistencies.append(
                CoverageInconsistency(
                    inconsistency_type=InconsistencyType.COMPLETED_ASSIGNMENT_ON_CANCELLED_SHIFT,
                    entity_type="assignment",
                    entity_id=assignment.id,
                    details=(
                        f"Assignment {assignment.id} is completed but Shift "
                        f"{shift.id} is cancelled"
                    ),
                )
            )
            return

        if assignment.duration_minutes and assignment.duration_minutes > 0:
            result.facts.append(
                CoverageFact(
                    doctor_id=assignment.doctor_id,
                    fact_type="assignment_completion",
                    duration_minutes=assignment.duration_minutes,
                    source_event="assignment.completed.v1",
                    source_id=assignment.id,
                )
            )

    def _process_extra(
        self, extra: ShiftExtra, shift: Shift, result: CoverageResult
    ) -> None:
        """Process a single extra for coverage consolidation."""
        if extra.status == ExtraStatus.APPROVED:
            result.facts.append(
                CoverageFact(
                    doctor_id=extra.doctor_id,
                    fact_type="extra_approved",
                    duration_minutes=extra.duration_minutes,
                    source_event="extra.approved.v1",
                    source_id=extra.id,
                )
            )
        elif extra.status == ExtraStatus.REJECTED:
            pass
        elif extra.status == ExtraStatus.PENDING:
            pass
        elif extra.status == ExtraStatus.CANCELLED:
            pass

    def consolidate_period(self, shifts: list[Shift]) -> list[CoverageResult]:
        """Consolidate coverage for all shifts in a period."""
        results = []
        for shift in shifts:
            result = self.consolidate_shift(shift)
            results.append(result)
        return results
