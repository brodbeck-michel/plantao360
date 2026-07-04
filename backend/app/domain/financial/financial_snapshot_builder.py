"""Financial domain — Snapshot and Fact builders."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.coverage.coverage_engine import CoverageResult, CoverageFact
from app.domain.constants.financial_fact_type import FinancialFactType
from app.domain.constants.financial_fact_status import FinancialFactStatus


@dataclass
class FinancialFactData:
    """Data for a single financial fact."""
    period_id: int
    doctor_id: int
    fact_type: str
    duration_minutes: int
    source_event: str
    source_id: int
    status: str = FinancialFactStatus.ACTIVE


@dataclass
class FinancialSnapshotData:
    """Data for a financial snapshot."""
    period_id: int
    coverage_snapshot_id: int
    facts: list[FinancialFactData] = field(default_factory=list)
    total_facts: int = 0
    total_duration_minutes: int = 0


class FinancialSnapshotBuilder:
    """Builds FinancialSnapshot from CoverageResults.

    Does NOT calculate values. Only consolidates rights.
    """

    def build(
        self,
        period_id: int,
        coverage_snapshot_id: int,
        coverage_results: list[CoverageResult],
    ) -> FinancialSnapshotData:
        """Build a FinancialSnapshot from coverage results."""
        facts = []

        for result in coverage_results:
            for coverage_fact in result.facts:
                fact = FinancialFactData(
                    period_id=period_id,
                    doctor_id=coverage_fact.doctor_id,
                    fact_type=coverage_fact.fact_type,
                    duration_minutes=coverage_fact.duration_minutes,
                    source_event=coverage_fact.source_event,
                    source_id=coverage_fact.source_id,
                )
                facts.append(fact)

        total_duration = sum(f.duration_minutes for f in facts)

        return FinancialSnapshotData(
            period_id=period_id,
            coverage_snapshot_id=coverage_snapshot_id,
            facts=facts,
            total_facts=len(facts),
            total_duration_minutes=total_duration,
        )
