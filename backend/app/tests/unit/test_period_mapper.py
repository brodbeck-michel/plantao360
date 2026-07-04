from app.mappers.period_mapper import PeriodMapper
from app.schemas.period.period_create import PeriodCreateDTO
from app.models.period import Period
from app.domain.constants.period_status import PeriodStatus


def test_mapper_to_response():
    mapper = PeriodMapper()
    period = Period(id=1, year=2026, month=6, status=PeriodStatus.DRAFT)
    dto = mapper.to_response(period)
    assert dto.id == 1
    assert dto.year == 2026
    assert dto.month == 6
    assert dto.status == "draft"


def test_mapper_to_model():
    mapper = PeriodMapper()
    dto = PeriodCreateDTO(year=2026, month=6)
    model = mapper.to_model(dto)
    assert model.year == 2026
    assert model.month == 6


def test_mapper_to_response_list():
    mapper = PeriodMapper()
    periods = [
        Period(id=1, year=2026, month=6, status=PeriodStatus.DRAFT),
        Period(id=2, year=2026, month=7, status=PeriodStatus.CLOSED),
    ]
    dtos = mapper.to_response_list(periods)
    assert len(dtos) == 2
    assert dtos[0].year == 2026
    assert dtos[1].year == 2026


def test_mapper_to_summary():
    mapper = PeriodMapper()
    period = Period(id=1, year=2026, month=6, status=PeriodStatus.DRAFT)
    summary = mapper.to_summary(period)
    assert summary["id"] == 1
    assert summary["year"] == 2026
    assert summary["month"] == 6
    assert summary["status"] == "draft"
