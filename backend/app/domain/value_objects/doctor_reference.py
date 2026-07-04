from dataclasses import dataclass


@dataclass(frozen=True)
class DoctorReference:
    doctor_id: int
    doctor_name: str = ""
    crm: str = ""

    def __post_init__(self) -> None:
        if self.doctor_id <= 0:
            raise ValueError(f"Invalid doctor_id: {self.doctor_id}")
