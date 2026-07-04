from app.schemas.period.period_response import PeriodResponseDTO
from app.common.pagination import Page
from app.common.result import Success, Failure
from app.common.api_response import ApiResponse
from app.domain.errors.period_errors import PeriodErrorCode


class TestPeriodResponseContract:
    def test_success_response_structure(self):
        response = ApiResponse.ok(data={"id": 1})
        result = response.to_dict()
        assert result["success"] is True
        assert result["data"]["id"] == 1
        assert result["errors"] == []

    def test_error_response_structure(self):
        response = ApiResponse.fail_with_code(
            code=PeriodErrorCode.PERIOD_NOT_FOUND,
            message="Not found",
        )
        result = response.to_dict()
        assert result["success"] is False
        assert result["error"]["code"] == "PERIOD_NOT_FOUND"


class TestPeriodErrorContract:
    def test_error_codes_are_strings(self):
        for code in PeriodErrorCode:
            assert isinstance(code.value, str)
            assert code.value == code.value.upper()

    def test_required_error_codes_exist(self):
        assert hasattr(PeriodErrorCode, "PERIOD_NOT_FOUND")
        assert hasattr(PeriodErrorCode, "PERIOD_ALREADY_EXISTS")
        assert hasattr(PeriodErrorCode, "PERIOD_ALREADY_CLOSED")
        assert hasattr(PeriodErrorCode, "PERIOD_IMMUTABLE")
        assert hasattr(PeriodErrorCode, "PERIOD_CANNOT_BE_REOPENED")
