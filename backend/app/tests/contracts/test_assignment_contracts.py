from app.domain.errors.assignment_errors import AssignmentErrorCode


def test_assignment_error_codes_are_strings():
    for code in AssignmentErrorCode:
        assert isinstance(code.value, str)


def test_assignment_required_error_codes_exist():
    assert hasattr(AssignmentErrorCode, "ASSIGNMENT_NOT_FOUND")
    assert hasattr(AssignmentErrorCode, "ASSIGNMENT_IMMUTABLE")
    assert hasattr(AssignmentErrorCode, "ASSIGNMENT_INVALID_TRANSITION")
    assert hasattr(AssignmentErrorCode, "ASSIGNMENT_CANNOT_BE_CANCELLED")
    assert hasattr(AssignmentErrorCode, "ASSIGNMENT_OVERLAP")
