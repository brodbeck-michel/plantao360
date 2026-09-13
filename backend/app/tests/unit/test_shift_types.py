from app.domain.constants.shift_types import ShiftType


def test_shift_type_values():
    values = ShiftType.values()
    assert values == ["T1", "T2", "T3", "R1", "R2", "R3"]


def test_shift_type_choices():
    choices = ShiftType.choices()
    assert len(choices) == 6
    assert ("T1", "T1") in choices
    assert ("R2", "R2") in choices
    assert ("R3", "R3") in choices


def test_shift_type_members():
    assert ShiftType.T1 == "T1"
    assert ShiftType.T2 == "T2"
    assert ShiftType.T3 == "T3"
    assert ShiftType.R1 == "R1"
    assert ShiftType.R2 == "R2"
    assert ShiftType.R3 == "R3"


def test_shift_type_is_str_enum():
    assert issubclass(ShiftType, str)
