from app.common.result import Success, Failure
from app.common.api_response import ApiResponse
from app.common.pagination import Page
from app.common.query import PaginationQuery, SortingQuery
from app.common.filters import FilterOperator
from app.validators.base_validator import BaseValidator, ValidationResult
from app.events.event_dispatcher import EventDispatcher, Event


def test_result_pattern_integration():
    def create_doctor(name: str) -> Success | Failure:
        if not name:
            return Failure(error="Nome obrigatório", code="VALIDATION_ERROR")
        return Success(data={"name": name})

    result = create_doctor("Dr. Test")
    assert result.is_success
    result2 = create_doctor("")
    assert result2.is_failure


def test_api_response_integration():
    def format_response(data):
        return ApiResponse.ok(data=data).to_dict()

    resp = format_response({"id": 1, "name": "Dr. Test"})
    assert resp["success"] is True
    assert resp["data"]["name"] == "Dr. Test"


def test_pagination_integration():
    items = [{"id": i} for i in range(25)]
    page = Page(items=items[:10], page=1, size=10, total=25)
    assert page.pages == 3
    assert page.has_next is True


def test_query_objects_integration():
    pq = PaginationQuery(page=2, size=10)
    assert pq.offset == 10
    sq = SortingQuery(field="name", direction="desc")
    assert sq.direction == "desc"


def test_event_dispatcher_integration():
    dispatcher = EventDispatcher()
    events = []
    dispatcher.register("doctor.created", lambda e: events.append(e.data))
    dispatcher.dispatch(Event(name="doctor.created", data={"id": 1}))
    assert len(events) == 1
    assert events[0]["id"] == 1


def test_validator_integration():
    class DoctorValidator(BaseValidator):
        def _validate(self, data, result: ValidationResult):
            if not data.get("name"):
                result.add_error("Nome obrigatório")

    v = DoctorValidator()
    result = v.validate({"name": ""})
    assert result.is_valid is False
    assert "Nome obrigatório" in result.errors
