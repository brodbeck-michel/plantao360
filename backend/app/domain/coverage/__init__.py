"""Coverage domain — CoverageEngine and related types."""

from app.domain.coverage.coverage_engine import (
    CoverageEngine,
    CoverageFact,
    CoverageInconsistency,
    CoverageResult,
)

__all__ = [
    "CoverageEngine",
    "CoverageFact",
    "CoverageInconsistency",
    "CoverageResult",
]
