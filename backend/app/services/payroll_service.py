"""Payroll service — orchestrates competency lifecycle and governance."""

from datetime import datetime

from app.database.unit_of_work import UnitOfWork
from app.repositories.payroll_repository import PayrollRepository
from app.models.payroll import Payroll
from app.schemas.payroll.payroll_create import PayrollCreateDTO
from app.schemas.payroll.payroll_response import PayrollResponseDTO
from app.schemas.payroll.payroll_filters import PayrollFilterDTO
from app.schemas.payroll.payroll_reopen import PayrollReopenDTO
from app.schemas.payroll.payroll_governance import (
    PayrollApprovalDTO,
    PayrollLockDTO,
    PayrollUnlockDTO,
    ChecklistItemUpdateDTO,
    PayrollReadinessDTO,
    ApprovalChecklistDTO,
    AdministrativeApprovalDTO,
    AdministrativeLockDTO,
    ApprovalSnapshotDTO,
    ReadinessItemDTO,
    ChecklistItemDTO,
)
from app.common.result import Success, Failure, Result
from app.common.pagination import Page
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.payroll_errors import PayrollErrorCode
from app.domain.payroll.payroll_competency import PayrollCompetency
from app.domain.payroll.governance import (
    ChecklistItemStatus,
    ReadinessStatus,
)
from app.domain.constants.payroll_status import PayrollStatus
from app.core.logging import get_logger

logger = get_logger("service.payroll")

event_dispatcher = EventDispatcher()


def _build_response(payroll: Payroll) -> PayrollResponseDTO:
    """Build response DTO from payroll model."""
    return PayrollResponseDTO(
        id=payroll.id,
        period_id=payroll.period_id,
        year_month=payroll.year_month,
        status=payroll.status,
        current_version=payroll.current_version,
        created_by=payroll.created_by,
        created_at=payroll.created_at,
        updated_at=payroll.updated_at,
        reopen_count=payroll.reopen_count,
        reopen_reason=payroll.reopen_reason,
    )


class PayrollService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> PayrollRepository:
        return PayrollRepository(self.uow.session)

    def list(self, filter_dto: PayrollFilterDTO) -> Page[PayrollResponseDTO]:
        skip = (filter_dto.page - 1) * filter_dto.size
        items = self.repo.list(
            skip=skip,
            limit=filter_dto.size,
            period_id=filter_dto.period_id,
            year_month=filter_dto.year_month,
            status=filter_dto.status,
            sort_by=filter_dto.sort_by,
            sort_direction=filter_dto.sort_direction,
        )
        total = self.repo.count(
            period_id=filter_dto.period_id,
            year_month=filter_dto.year_month,
            status=filter_dto.status,
        )
        dtos = [_build_response(p) for p in items]
        return Page(
            items=dtos,
            page=filter_dto.page,
            size=filter_dto.size,
            total=total,
        )

    def get_by_id(self, payroll_id: int) -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )
        return Success(data=_build_response(entity))

    def create(self, dto: PayrollCreateDTO) -> Result[PayrollResponseDTO]:
        existing = self.repo.get_by_period(dto.period_id)
        if existing:
            return Failure(
                error=PayrollErrorCode.PAYROLL_ALREADY_EXISTS,
                code=PayrollErrorCode.PAYROLL_ALREADY_EXISTS,
            )

        now = datetime.utcnow()
        entity = Payroll(
            period_id=dto.period_id,
            year_month=dto.year_month,
            created_by=dto.created_by,
            created_at=now,
            updated_at=now,
        )
        created = self.repo.create(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_CREATED_V1,
                data={"id": created.id, "period_id": created.period_id},
            )
        )

        logger.info("payroll.created.v1", extra={"payroll_id": created.id})
        return Success(data=_build_response(created))

    def review(self, payroll_id: int, reviewed_by: str = "system") -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.CALCULATED:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        entity.status = PayrollStatus.REVIEWED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_REVIEWED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("payroll.reviewed.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def approve(self, payroll_id: int, approved_by: str = "system") -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.REVIEWED:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        entity.status = PayrollStatus.APPROVED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_APPROVED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("payroll.approved.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def export(self, payroll_id: int, exported_by: str = "system") -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status not in {PayrollStatus.APPROVED, PayrollStatus.LOCKED}:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        entity.status = PayrollStatus.EXPORTED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_EXPORTED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("payroll.exported.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def mark_paid(self, payroll_id: int, paid_by: str = "system") -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.EXPORTED:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        entity.status = PayrollStatus.PAID
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_PAID_V1,
                data={"id": updated.id},
            )
        )

        logger.info("payroll.paid.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def archive(self, payroll_id: int) -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.PAID:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        entity.status = PayrollStatus.ARCHIVED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_ARCHIVED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("payroll.archived.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def reopen(self, payroll_id: int, dto: PayrollReopenDTO) -> Result[PayrollResponseDTO]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        reopenable = {
            PayrollStatus.CALCULATED,
            PayrollStatus.REVIEWED,
            PayrollStatus.APPROVED,
            PayrollStatus.LOCKED,
            PayrollStatus.EXPORTED,
            PayrollStatus.PAID,
        }
        if entity.status not in reopenable:
            return Failure(
                error=PayrollErrorCode.PAYROLL_REOPEN_FAILED,
                code=PayrollErrorCode.PAYROLL_REOPEN_FAILED,
            )

        entity.status = PayrollStatus.DRAFT
        entity.reopen_count += 1
        entity.reopen_reason = dto.reason
        entity.current_version += 1
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_REOPENED_V1,
                data={
                    "id": updated.id,
                    "previous_version": updated.current_version - 1,
                    "new_version": updated.current_version,
                    "reason": dto.reason,
                },
            )
        )

        logger.info("payroll.reopened.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def delete(self, payroll_id: int) -> Result[bool]:
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.DRAFT:
            return Failure(
                error=PayrollErrorCode.PAYROLL_IMMUTABLE,
                code=PayrollErrorCode.PAYROLL_IMMUTABLE,
            )

        self.uow.session.delete(entity)
        self.uow.session.flush()
        logger.info("payroll.deleted", extra={"payroll_id": payroll_id})
        return Success(data=True)

    # --- Governance methods ---

    def validate_readiness(self, payroll_id: int, validated_by: str = "system") -> Result[PayrollReadinessDTO]:
        """Validate if a competency is ready for administrative closing."""
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status not in {PayrollStatus.CALCULATED, PayrollStatus.REVIEWED}:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        # Build domain object and validate readiness
        domain = PayrollCompetency(
            period_id=entity.period_id,
            year_month=entity.year_month,
            created_by=entity.created_by,
        )
        domain.status = PayrollStatus(entity.status)
        domain.current_version = entity.current_version

        readiness = domain.validate_readiness(validated_by=validated_by)

        # Map to DTO
        items_dto = [
            ReadinessItemDTO(
                item_id=i.item_id,
                description=i.description,
                passed=i.passed,
                message=i.message,
            )
            for i in readiness.items
        ]

        dto = PayrollReadinessDTO(
            competency_id=entity.id,
            year_month=entity.year_month,
            version=entity.current_version,
            validated_at=readiness.validated_at,
            validated_by=readiness.validated_by,
            status=readiness.status,
            items=items_dto,
            pending_count=readiness.pending_count,
        )

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_READY_V1,
                data={
                    "id": entity.id,
                    "status": readiness.status,
                    "pending_count": readiness.pending_count,
                },
            )
        )

        logger.info("payroll.ready.v1", extra={"payroll_id": entity.id})
        return Success(data=dto)

    def lock(self, payroll_id: int, dto: PayrollLockDTO) -> Result[PayrollResponseDTO]:
        """Lock competency administratively."""
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.APPROVED:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        entity.status = PayrollStatus.LOCKED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_LOCKED_V1,
                data={
                    "id": updated.id,
                    "locked_by": dto.locked_by,
                },
            )
        )

        logger.info("payroll.locked.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def unlock(self, payroll_id: int, dto: PayrollUnlockDTO) -> Result[PayrollResponseDTO]:
        """Unlock competency — removes administrative lock."""
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.LOCKED:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_LOCKED,
                code=PayrollErrorCode.PAYROLL_NOT_LOCKED,
            )

        entity.status = PayrollStatus.APPROVED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_UNLOCKED_V1,
                data={
                    "id": updated.id,
                    "unlocked_by": dto.unlocked_by,
                },
            )
        )

        logger.info("payroll.unlocked.v1", extra={"payroll_id": updated.id})
        return Success(data=_build_response(updated))

    def approve_administratively(
        self,
        payroll_id: int,
        dto: PayrollApprovalDTO,
    ) -> Result[AdministrativeApprovalDTO]:
        """Approve competency administratively — full governance process."""
        entity = self.repo.get_by_id(payroll_id)
        if not entity:
            return Failure(
                error=PayrollErrorCode.PAYROLL_NOT_FOUND,
                code=PayrollErrorCode.PAYROLL_NOT_FOUND,
            )

        if entity.status != PayrollStatus.REVIEWED:
            return Failure(
                error=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
                code=PayrollErrorCode.PAYROLL_INVALID_TRANSITION,
            )

        # Update status
        entity.status = PayrollStatus.APPROVED
        entity.updated_at = datetime.utcnow()
        updated = self.repo.update(entity)

        # Create approval DTO
        approval_dto = AdministrativeApprovalDTO(
            competency_id=updated.id,
            year_month=updated.year_month,
            version=updated.current_version,
            approved_by=dto.approved_by,
            approved_at=datetime.utcnow(),
            justification=dto.justification,
            observations=dto.observations,
            checklist_version=updated.current_version,
        )

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PAYROLL_APPROVED_V1,
                data={
                    "id": updated.id,
                    "approved_by": dto.approved_by,
                    "justification": dto.justification,
                },
            )
        )

        logger.info("payroll.approved.v1", extra={"payroll_id": updated.id})
        return Success(data=approval_dto)
