from dataclasses import dataclass


@dataclass(frozen=True)
class CoverageCheckResult:
    is_covered: bool
    current_doctors: int
    min_required: int
    message: str = ""

    @classmethod
    def covered(cls, current: int, minimum: int) -> "CoverageCheckResult":
        return cls(
            is_covered=True,
            current_doctors=current,
            min_required=minimum,
            message=f"Coverage OK: {current}/{minimum} doctors",
        )

    @classmethod
    def not_covered(cls, current: int, minimum: int) -> "CoverageCheckResult":
        return cls(
            is_covered=False,
            current_doctors=current,
            min_required=minimum,
            message=f"Coverage insufficient: {current}/{minimum} doctors",
        )


class CoveragePolicy:
    def __init__(self, min_doctors: int = 1) -> None:
        self._min_doctors = min_doctors

    def has_minimum_coverage(self, doctor_count: int) -> CoverageCheckResult:
        if doctor_count >= self._min_doctors:
            return CoverageCheckResult.covered(doctor_count, self._min_doctors)
        return CoverageCheckResult.not_covered(doctor_count, self._min_doctors)

    def has_sufficient_doctors(
        self, current_count: int, adding: int = 0, removing: int = 0
    ) -> CoverageCheckResult:
        projected = current_count + adding - removing
        if projected >= self._min_doctors:
            return CoverageCheckResult.covered(projected, self._min_doctors)
        return CoverageCheckResult.not_covered(projected, self._min_doctors)

    def would_removal_leave_uncovered(
        self, current_count: int
    ) -> CoverageCheckResult:
        projected = current_count - 1
        if projected >= self._min_doctors:
            return CoverageCheckResult.covered(projected, self._min_doctors)
        return CoverageCheckResult.not_covered(projected, self._min_doctors)
