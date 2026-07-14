from datetime import time as time_type

from app.database.unit_of_work import UnitOfWork
from app.repositories.shift_part_repository import ShiftPartRepository
from app.repositories.shift_repository import ShiftRepository
from app.repositories.doctor_repository import DoctorRepository
from app.models.shift_part import ShiftPart
from app.models.shift import Shift
from app.schemas.assignment.assignment_create import AssignmentCreateDTO
from app.schemas.assignment.assignment_update import AssignmentUpdateDTO
from app.schemas.assignment.assignment_response import AssignmentResponseDTO
from app.schemas.assignment.assignment_filters import AssignmentFilterDTO
from app.common.pagination import Page
from app.common.result import Success, Failure, Result
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.constants.shift_status import ShiftStatus
from app.core.logging import get_logger

logger = get_logger("service.assignment")
event_dispatcher = EventDispatcher()


# AssignmentRules — antes em domain/rules/assignment_rules (consumidor único: este service).
# Inlinada no colapso da domain/ (spec 005, Grupo D). Regras de transição preservadas.
class AssignmentRules:
    def __init__(self, assignment) -> None:
        self._assignment = assignment

    def validate_can_confirm(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status != AssignmentStatus.PLANNED:
            errors.append(f"Cannot confirm assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_start(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status != AssignmentStatus.CONFIRMED:
            errors.append(f"Cannot start assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_complete(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status != AssignmentStatus.STARTED:
            errors.append(f"Cannot complete assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_cancel(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status not in (AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED):
            errors.append(f"Cannot cancel assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_change_doctor(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status not in (AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED):
            errors.append(f"Cannot change doctor in status '{self._assignment.status}'")
        return errors

    def validate_can_change_time(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status not in (AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED):
            errors.append(f"Cannot change time in status '{self._assignment.status}'")
        return errors

    def validate_time_range(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.start_time and self._assignment.end_time:
            if self._assignment.end_time <= self._assignment.start_time:
                errors.append("end_time must be after start_time")
        return errors


# AssignmentStateMachine — antes em domain/state_machines (consumidor único: este service).
# Inlinada no colapso da domain/ (spec 005, Grupo D). Transições e efeitos preservados.
class AssignmentStateMachine:
    def __init__(self, aggregate) -> None:
        self._aggregate = aggregate

    def confirm(self) -> None:
        self._transition(AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED)

    def start(self) -> None:
        self._transition(AssignmentStatus.CONFIRMED, AssignmentStatus.STARTED)

    def complete(self) -> None:
        self._transition(AssignmentStatus.STARTED, AssignmentStatus.COMPLETED)

    def cancel(self) -> None:
        current = self._aggregate.status
        allowed = {AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED}
        if current not in allowed:
            raise ValueError(f"Cannot cancel assignment in status '{current}'")
        self._transition(current, AssignmentStatus.CANCELLED)

    def _transition(self, from_status: str, to_status: str) -> None:
        current = self._aggregate.status
        if current != from_status:
            raise ValueError(
                f"Cannot transition from '{current}' to '{to_status}': "
                f"expected '{from_status}'"
            )
        self._aggregate.before_transition(current, to_status)
        self._aggregate.status = to_status
        self._aggregate.after_transition(current, to_status)


class AssignmentService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> ShiftPartRepository:
        return ShiftPartRepository(self.uow.session)

    @property
    def shift_repo(self) -> ShiftRepository:
        return ShiftRepository(self.uow.session)

    @property
    def doctor_repo(self) -> DoctorRepository:
        return DoctorRepository(self.uow.session)

    def _count_active_assignments(self, shift_id: int) -> int:
        active = self.repo.search(shift_id=shift_id, status=AssignmentStatus.PLANNED)
        active += self.repo.search(shift_id=shift_id, status=AssignmentStatus.CONFIRMED)
        active += self.repo.search(shift_id=shift_id, status=AssignmentStatus.STARTED)
        active += self.repo.search(shift_id=shift_id, status=AssignmentStatus.COMPLETED)
        return len(active)

    def recalculate_shift_status(self, shift_id: int) -> None:
        shift = self.shift_repo.get_by_id(shift_id)
        if not shift or shift.status == ShiftStatus.CANCELLED:
            return
        active_count = self._count_active_assignments(shift_id)
        if active_count == 0 and shift.status != ShiftStatus.DRAFT:
            shift.status = ShiftStatus.DRAFT
            self.shift_repo.update(shift)
        elif active_count > 0 and shift.status == ShiftStatus.DRAFT:
            shift.status = ShiftStatus.SCHEDULED
            self.shift_repo.update(shift)

    def list(self, filter_dto: AssignmentFilterDTO) -> Page[AssignmentResponseDTO]:
        skip = (filter_dto.page - 1) * filter_dto.size
        items = self.repo.search(
            skip=skip,
            limit=filter_dto.size,
            sort_by=filter_dto.sort_by,
            sort_direction=filter_dto.sort_direction,
            **filter_dto.to_filters(),
        )
        total = self.repo.count_filtered(**filter_dto.to_filters())
        dtos = [AssignmentResponseDTO.model_validate(d) for d in items]
        return Page(items=dtos, page=filter_dto.page, size=filter_dto.size, total=total)

    def get_by_id(self, id: int) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )
        return Success(data=AssignmentResponseDTO.model_validate(entity))

    def create(self, dto: AssignmentCreateDTO) -> Result[AssignmentResponseDTO]:
        shift = self.shift_repo.get_by_id(dto.shift_id)
        if not shift:
            return Failure(
                error="Turno nao encontrado",
                code=AssignmentErrorCode.ASSIGNMENT_SHIFT_NOT_FOUND,
            )

        if shift.status == ShiftStatus.CANCELLED:
            return Failure(
                error="Não é possível atribuir médicos. Este turno está cancelado. Reative o turno ou altere o status antes de realizar novas atribuições.",
                code=AssignmentErrorCode.ASSIGNMENT_SHIFT_NOT_FOUND,
            )

        doctor = self.doctor_repo.get_by_id(dto.doctor_id)
        if not doctor:
            return Failure(
                error="Medico nao encontrado",
                code=AssignmentErrorCode.ASSIGNMENT_DOCTOR_NOT_FOUND,
            )

        if not doctor.active:
            return Failure(
                error="Medico esta inativo",
                code=AssignmentErrorCode.ASSIGNMENT_DOCTOR_NOT_FOUND,
            )

        start_time = dto.start_time
        end_time = dto.end_time
        if isinstance(start_time, str):
            parts = start_time.split(":")
            start_time = time_type(int(parts[0]), int(parts[1]))
        if isinstance(end_time, str):
            parts = end_time.split(":")
            end_time = time_type(int(parts[0]), int(parts[1]))

        same_date = self.repo.find_same_date_assignments(
            doctor_id=dto.doctor_id,
            shift_date=shift.shift_date,
        )
        for existing in same_date:
            existing_end = existing.end_time
            existing_start = existing.start_time
            e_start = start_time
            e_end = end_time
            if existing_end <= existing_start:
                existing_end_minutes = existing_end.hour * 60 + existing_end.minute + 24 * 60
            else:
                existing_end_minutes = existing_end.hour * 60 + existing_end.minute
            if e_end <= e_start:
                e_end_minutes = e_end.hour * 60 + e_end.minute + 24 * 60
            else:
                e_end_minutes = e_end.hour * 60 + e_end.minute
            existing_start_minutes = existing_start.hour * 60 + existing_start.minute
            e_start_minutes = e_start.hour * 60 + e_start.minute
            if existing_start_minutes < e_end_minutes and existing_end_minutes > e_start_minutes:
                return Failure(
                    error="Medico ja possui atribuicao neste horario",
                    code=AssignmentErrorCode.ASSIGNMENT_OVERLAP,
                )

        entity = ShiftPart(
            shift_id=dto.shift_id,
            doctor_id=dto.doctor_id,
            start_time=start_time,
            end_time=end_time,
            status=AssignmentStatus.PLANNED,
        )
        created = self.repo.create(entity)

        if shift.status == ShiftStatus.DRAFT:
            shift.status = ShiftStatus.SCHEDULED
            self.shift_repo.update(shift)

        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_CREATED_V1, data={"id": created.id})
        )
        logger.info("assignment.created.v1", extra={"assignment_id": created.id})
        return Success(data=AssignmentResponseDTO.model_validate(created))

    def update(self, id: int, dto: AssignmentUpdateDTO) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )

        if dto.doctor_id is not None:
            doctor = self.doctor_repo.get_by_id(dto.doctor_id)
            if not doctor:
                return Failure(
                    error="Medico nao encontrado",
                    code=AssignmentErrorCode.ASSIGNMENT_DOCTOR_NOT_FOUND,
                )
            entity.doctor_id = dto.doctor_id

        if dto.start_time:
            parts = dto.start_time.split(":")
            entity.start_time = time_type(int(parts[0]), int(parts[1]))
        if dto.end_time:
            parts = dto.end_time.split(":")
            entity.end_time = time_type(int(parts[0]), int(parts[1]))

        updated = self.repo.update(entity)
        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_UPDATED_V1, data={"id": updated.id})
        )
        logger.info("assignment.updated.v1", extra={"assignment_id": updated.id})
        return Success(data=AssignmentResponseDTO.model_validate(updated))

    def confirm(self, id: int) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )
        rules = AssignmentRules(entity)
        errors = rules.validate_can_confirm()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_INVALID_TRANSITION)

        sm = AssignmentStateMachine(entity)
        sm.confirm()
        updated = self.repo.update(entity)
        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_CONFIRMED_V1, data={"id": updated.id})
        )
        logger.info("assignment.confirmed.v1", extra={"assignment_id": updated.id})
        return Success(data=AssignmentResponseDTO.model_validate(updated))

    def start(self, id: int) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )
        rules = AssignmentRules(entity)
        errors = rules.validate_can_start()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_INVALID_TRANSITION)

        sm = AssignmentStateMachine(entity)
        sm.start()
        updated = self.repo.update(entity)
        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_STARTED_V1, data={"id": updated.id})
        )
        logger.info("assignment.started.v1", extra={"assignment_id": updated.id})
        return Success(data=AssignmentResponseDTO.model_validate(updated))

    def complete(self, id: int) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )
        rules = AssignmentRules(entity)
        errors = rules.validate_can_complete()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_INVALID_TRANSITION)

        sm = AssignmentStateMachine(entity)
        sm.complete()

        if entity.start_time and entity.end_time:
            from datetime import datetime
            start_dt = datetime(2000, 1, 1, entity.start_time.hour, entity.start_time.minute)
            end_dt = datetime(2000, 1, 1, entity.end_time.hour, entity.end_time.minute)
            entity.duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

        updated = self.repo.update(entity)
        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_COMPLETED_V1, data={"id": updated.id})
        )
        logger.info("assignment.completed.v1", extra={"assignment_id": updated.id})
        return Success(data=AssignmentResponseDTO.model_validate(updated))

    def cancel(self, id: int) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )
        rules = AssignmentRules(entity)
        errors = rules.validate_can_cancel()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_CANNOT_BE_CANCELLED)

        sm = AssignmentStateMachine(entity)
        sm.cancel()
        updated = self.repo.update(entity)
        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_CANCELLED_V1, data={"id": updated.id})
        )
        logger.info("assignment.cancelled.v1", extra={"assignment_id": updated.id})
        return Success(data=AssignmentResponseDTO.model_validate(updated))

    def remove(self, id: int) -> Result[AssignmentResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )
        if entity.status == AssignmentStatus.STARTED:
            return Failure(
                error="Cannot remove a started assignment",
                code=AssignmentErrorCode.ASSIGNMENT_IMMUTABLE,
            )

        entity.status = AssignmentStatus.CANCELLED
        updated = self.repo.update(entity)

        self.recalculate_shift_status(entity.shift_id)

        event_dispatcher.dispatch(
            Event(name=DomainEventName.ASSIGNMENT_REMOVED_V1, data={"id": id})
        )
        logger.info("assignment.removed.v1", extra={"assignment_id": id})
        return Success(data=AssignmentResponseDTO.model_validate(updated))
