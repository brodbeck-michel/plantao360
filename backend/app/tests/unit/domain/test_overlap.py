import pytest
from app.domain.overlap.overlap_check import OverlapCheckRequest, OverlapResult
from app.domain.overlap.conflict_detection import ConflictDetectionRequest, ConflictResult
from app.domain.overlap.overlap_detector import OverlapDetector
from datetime import time


def test_overlap_result_none():
    result = OverlapResult.none()
    assert result.has_overlap is False
    assert result.conflicting_assignment_ids == []


def test_overlap_result_found():
    result = OverlapResult.found([1, 2], "overlap detected")
    assert result.has_overlap is True
    assert len(result.conflicting_assignment_ids) == 2


def test_conflict_result_none():
    result = ConflictResult.none()
    assert result.has_conflict is False


def test_conflict_result_found():
    result = ConflictResult.found([10, 20], "conflict detected")
    assert result.has_conflict is True
    assert len(result.conflicting_shift_ids) == 2


def test_overlap_detector_no_repository():
    detector = OverlapDetector()
    request = OverlapCheckRequest(
        doctor_id=1, shift_id=1, start_time=time(8, 0), end_time=time(20, 0)
    )
    result = detector.check_overlap(request)
    assert result.has_overlap is False


def test_overlap_detector_with_mock_repository():
    mock_repo = type("MockRepo", (), {
        "find_overlapping": lambda self, **kwargs: []
    })()
    detector = OverlapDetector(repository=mock_repo)
    request = OverlapCheckRequest(
        doctor_id=1, shift_id=1, start_time=time(8, 0), end_time=time(20, 0)
    )
    result = detector.check_overlap(request)
    assert result.has_overlap is False
