from app.schemas.shift.shift_response import ShiftResponseDTO
from app.common.pagination import Page
from app.common.result import Success, Failure
from app.common.api_response import ApiResponse
from app.domain.errors.shift_errors import ShiftErrorCode


class TestShiftResponseContract:
    def test_success_response_structure(self):
        response = ApiResponse.ok(data={"id": 1})
        result = response.to_dict()
        assert result["success"] is True
        assert result["data"]["id"] == 1
        assert result["errors"] == []

    def test_error_response_structure(self):
        response = ApiResponse.fail_with_code(
            code=ShiftErrorCode.SHIFT_NOT_FOUND,
            message="Not found",
        )
        result = response.to_dict()
        assert result["success"] is False
        assert result["error"]["code"] == "SHIFT_NOT_FOUND"


class TestShiftErrorContract:
    def test_error_codes_are_strings(self):
        for code in ShiftErrorCode:
            assert isinstance(code.value, str)
            assert code.value == code.value.upper()

    def test_required_error_codes_exist(self):
        assert hasattr(ShiftErrorCode, "SHIFT_NOT_FOUND")
        assert hasattr(ShiftErrorCode, "SHIFT_ALREADY_EXISTS")
