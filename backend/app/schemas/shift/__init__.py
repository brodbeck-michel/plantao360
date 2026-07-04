from pydantic import BaseModel, Field

from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_update import ShiftUpdateDTO
from app.schemas.shift.shift_response import ShiftResponseDTO
from app.schemas.shift.shift_summary import ShiftSummaryDTO
from app.schemas.shift.shift_filters import ShiftFilterDTO
from app.schemas.shift.shift_query import ShiftQueryDTO

__all__ = [
    "ShiftCreateDTO",
    "ShiftUpdateDTO",
    "ShiftResponseDTO",
    "ShiftSummaryDTO",
    "ShiftFilterDTO",
    "ShiftQueryDTO",
]
