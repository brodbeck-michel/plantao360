from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ApiResponse(Generic[T]):
    def __init__(
        self,
        success: bool = True,
        data: T | None = None,
        meta: dict[str, Any] | None = None,
        errors: list[str] | None = None,
        error: ApiErrorDetail | None = None,
    ):
        self.success = success
        self.data = data
        self.meta = meta or {}
        self.errors = errors or []
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "success": self.success,
            "data": self.data,
            "meta": self.meta,
            "errors": self.errors,
        }
        if self.error:
            result["error"] = self.error.model_dump()
        return result

    @classmethod
    def ok(cls, data: T, meta: dict[str, Any] | None = None) -> "ApiResponse[T]":
        return cls(success=True, data=data, meta=meta)

    @classmethod
    def fail(
        cls,
        errors: list[str] | None = None,
        error: ApiErrorDetail | None = None,
        meta: dict[str, Any] | None = None,
    ) -> "ApiResponse":
        return cls(success=False, errors=errors or [], error=error, meta=meta)

    @classmethod
    def fail_with_code(
        cls,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
        meta: dict[str, Any] | None = None,
    ) -> "ApiResponse":
        error = ApiErrorDetail(code=code, message=message, details=details)
        return cls(success=False, error=error, meta=meta)
