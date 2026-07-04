from app.domain.overlap.overlap_check import OverlapCheckRequest, OverlapResult
from app.domain.overlap.conflict_detection import ConflictDetectionRequest, ConflictResult


class OverlapDetector:
    def __init__(self, repository=None) -> None:
        self._repository = repository

    def check_overlap(self, request: OverlapCheckRequest) -> OverlapResult:
        if self._repository is None:
            return OverlapResult.none()
        overlapping = self._repository.find_overlapping(
            doctor_id=request.doctor_id,
            start_time=request.start_time,
            end_time=request.end_time,
            exclude_id=request.exclude_assignment_id,
        )
        if overlapping:
            ids = [a.id for a in overlapping]
            return OverlapResult.found(
                assignment_ids=ids,
                message=f"Doctor {request.doctor_id} has {len(ids)} overlapping assignment(s)",
            )
        return OverlapResult.none()

    def detect_conflicts(self, request: ConflictDetectionRequest) -> ConflictResult:
        if self._repository is None:
            return ConflictResult.none()
        conflicts = self._repository.find_conflicting_shifts(
            doctor_id=request.doctor_id,
            shift_date=request.shift_date,
            exclude_id=request.exclude_assignment_id,
        )
        if conflicts:
            ids = [s.id for s in conflicts]
            return ConflictResult.found(
                shift_ids=ids,
                message=f"Doctor {request.doctor_id} has {len(ids)} conflicting shift(s)",
            )
        return ConflictResult.none()
