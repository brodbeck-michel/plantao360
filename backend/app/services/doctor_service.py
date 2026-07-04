from typing import Optional

from app.database.unit_of_work import UnitOfWork
from app.repositories.doctor_repository import DoctorRepository
from app.models.doctor import Doctor
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.schemas.doctor.doctor_update import DoctorUpdateDTO
from app.schemas.doctor.doctor_response import DoctorResponseDTO
from app.schemas.doctor.doctor_filters import DoctorFilterDTO
from app.common.pagination import Page
from app.common.result import Success, Failure, Result
from app.common.api_response import ApiResponse, ApiErrorDetail
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.doctor_errors import DoctorErrorCode
from app.core.logging import get_logger

logger = get_logger("service.doctor")

event_dispatcher = EventDispatcher()


class DoctorService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> DoctorRepository:
        return DoctorRepository(self.uow.session)

    def list(self, filter_dto: DoctorFilterDTO) -> Page[DoctorResponseDTO]:
        skip = (filter_dto.page - 1) * filter_dto.size
        doctors = self.repo.search(
            name=filter_dto.name,
            crm=filter_dto.crm,
            active=filter_dto.active,
            skip=skip,
            limit=filter_dto.size,
            sort_by=filter_dto.sort_by,
            sort_direction=filter_dto.sort_direction,
        )
        total = self.repo.count_filtered(
            name=filter_dto.name,
            crm=filter_dto.crm,
            active=filter_dto.active,
        )
        items = [DoctorResponseDTO.model_validate(d) for d in doctors]
        return Page(
            items=items,
            page=filter_dto.page,
            size=filter_dto.size,
            total=total,
        )

    def get_by_id(self, id: int) -> Result[DoctorResponseDTO]:
        doctor = self.repo.get_by_id(id)
        if not doctor:
            return Failure(
                error=DoctorErrorCode.DOCTOR_NOT_FOUND,
                code=DoctorErrorCode.DOCTOR_NOT_FOUND,
            )
        return Success(data=DoctorResponseDTO.model_validate(doctor))

    def create(self, dto: DoctorCreateDTO) -> Result[DoctorResponseDTO]:
        if self.repo.exists_by_crm(dto.crm):
            return Failure(
                error=f"CRM {dto.crm} ja cadastrado",
                code=DoctorErrorCode.DOCTOR_ALREADY_EXISTS,
            )

        doctor = Doctor(
            name=dto.name,
            crm=dto.crm,
            hour_rate=dto.hour_rate,
            specialty=dto.specialty,
            phone=dto.phone,
            email=dto.email,
            doctor_type=dto.doctor_type,
        )
        created = self.repo.create(doctor)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.DOCTOR_CREATED_V1,
                data={"id": created.id, "name": created.name, "crm": created.crm},
            )
        )

        logger.info("doctor.created.v1", extra={"doctor_id": created.id})
        return Success(data=DoctorResponseDTO.model_validate(created))

    def update(self, id: int, dto: DoctorUpdateDTO) -> Result[DoctorResponseDTO]:
        doctor = self.repo.get_by_id(id)
        if not doctor:
            return Failure(
                error=DoctorErrorCode.DOCTOR_NOT_FOUND,
                code=DoctorErrorCode.DOCTOR_NOT_FOUND,
            )

        if dto.crm and self.repo.exists_by_crm(dto.crm, exclude_id=id):
            return Failure(
                error=f"CRM {dto.crm} ja cadastrado",
                code=DoctorErrorCode.DOCTOR_ALREADY_EXISTS,
            )

        if dto.name is not None:
            doctor.name = dto.name
        if dto.crm is not None:
            doctor.crm = dto.crm
        if dto.hour_rate is not None:
            doctor.hour_rate = dto.hour_rate
        if dto.specialty is not None:
            doctor.specialty = dto.specialty
        if dto.phone is not None:
            doctor.phone = dto.phone
        if dto.email is not None:
            doctor.email = dto.email
        if dto.doctor_type is not None:
            doctor.doctor_type = dto.doctor_type
        if dto.active is not None:
            doctor.active = dto.active

        updated = self.repo.update(doctor)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.DOCTOR_UPDATED_V1,
                data={"id": updated.id, "name": updated.name},
            )
        )

        logger.info("doctor.updated.v1", extra={"doctor_id": updated.id})
        return Success(data=DoctorResponseDTO.model_validate(updated))

    def delete(self, id: int) -> Result[bool]:
        doctor = self.repo.get_by_id(id)
        if not doctor:
            return Failure(
                error=DoctorErrorCode.DOCTOR_NOT_FOUND,
                code=DoctorErrorCode.DOCTOR_NOT_FOUND,
            )

        self.repo.soft_delete(id)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.DOCTOR_DEACTIVATED_V1,
                data={"id": id},
            )
        )

        logger.info("doctor.deactivated.v1", extra={"doctor_id": id})
        return Success(data=True)
