from app.models.doctor import Doctor
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.schemas.doctor.doctor_response import DoctorResponseDTO
from app.mappers.base_mapper import BaseMapper


class DoctorMapper(BaseMapper[Doctor, DoctorCreateDTO, DoctorResponseDTO]):
    def __init__(self):
        super().__init__(Doctor, DoctorCreateDTO, DoctorResponseDTO)
