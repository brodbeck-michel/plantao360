from dataclasses import dataclass

from app.domain.constants.period_status import PeriodStatus


@dataclass(frozen=True)
class PeriodContract:
    period_id: int
    year: int
    month: int
    status: PeriodStatus

    def can_be_queried(self) -> bool:
        return True

    def can_be_validated(self) -> bool:
        return True

    def can_be_closed_by_external(self) -> bool:
        return False

    def can_status_be_changed_by_external(self) -> bool:
        return False

    def can_be_reopened_by_external(self) -> bool:
        return False

    def can_dates_be_modified_by_external(self) -> bool:
        return False

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year": self.year,
            "month": self.month,
            "status": self.status,
            "permissions": {
                "query": self.can_be_queried(),
                "validate": self.can_be_validated(),
                "close": self.can_be_closed_by_external(),
                "change_status": self.can_status_be_changed_by_external(),
                "reopen": self.can_be_reopened_by_external(),
                "modify_dates": self.can_dates_be_modified_by_external(),
            },
        }
