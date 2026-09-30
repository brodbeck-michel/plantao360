"""PLANTAOPA-5: horas dos turnos cadastrados contam pela hora cheia."""
import pytest

from app.services.workspace_service import WorkspaceService


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("13:00", "18:59", 6.0),
        ("08:00", "13:59", 6.0),
        ("07:00", "19:00", 12.0),
        ("19:00", "06:59", 12.0),
        ("07:00", "07:00", 24.0),
        ("20:00", "23:00", 3.0),
        ("", "", 0.0),
    ],
)
def test_calc_hours_hora_cheia(start, end, expected):
    service = WorkspaceService.__new__(WorkspaceService)
    assert service._calc_hours(start, end) == expected
