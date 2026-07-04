from app.models.shift import Shift
from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_response import ShiftResponseDTO
from app.mappers.base_mapper import BaseMapper


class ShiftMapper(BaseMapper[Shift, ShiftCreateDTO, ShiftResponseDTO]):
    def __init__(self):
        super().__init__(Shift, ShiftCreateDTO, ShiftResponseDTO)
