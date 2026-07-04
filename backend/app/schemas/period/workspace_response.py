from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class AssignmentData(BaseModel):
    id: int
    shift_id: int
    shift_type: str
    doctor_id: int
    doctor_name: str
    start_time: str
    end_time: str
    status: str

    model_config = {"from_attributes": True}


class ShiftCellData(BaseModel):
    shift_id: int
    shift_type: str
    assignments: list[AssignmentData] = Field(default_factory=list)


class DayData(BaseModel):
    date: str
    day_of_week: str
    shifts: dict[str, ShiftCellData] = Field(default_factory=dict)


class DoctorOption(BaseModel):
    id: int
    name: str
    crm: str
    hour_rate: float
    specialty: str = ""
    active: bool = True

    model_config = {"from_attributes": True}


class PeriodInfo(BaseModel):
    id: int
    year: int
    month: int
    status: str
    start_date: str = ""
    end_date: str = ""

    model_config = {"from_attributes": True}


class WorkspaceSummary(BaseModel):
    total_shifts: int = 0
    filled_shifts: int = 0
    coverage_rate: float = 0.0
    total_doctors: int = 0
    total_hours: float = 0.0


class WorkspaceData(BaseModel):
    period: PeriodInfo
    days: list[DayData] = Field(default_factory=list)
    doctors: list[DoctorOption] = Field(default_factory=list)
    summary: WorkspaceSummary = Field(default_factory=WorkspaceSummary)
