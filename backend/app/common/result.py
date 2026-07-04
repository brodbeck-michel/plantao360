from typing import TypeVar, Generic

T = TypeVar("T")


class Success(Generic[T]):
    def __init__(self, data: T):
        self.data = data
        self.is_success = True
        self.is_failure = False

    def __repr__(self) -> str:
        return f"<Success data={self.data!r}>"


class Failure:
    def __init__(self, error: str, code: str | None = None):
        self.error = error
        self.code = code
        self.is_success = False
        self.is_failure = True

    def __repr__(self) -> str:
        return f"<Failure error={self.error!r}>"


Result = Success[T] | Failure
