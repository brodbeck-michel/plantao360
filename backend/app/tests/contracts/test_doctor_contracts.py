"""Contract tests — Doctor module."""

from app.common.result import Success, Failure
from app.common.api_response import ApiResponse, ApiErrorDetail
from app.common.pagination import Page
from app.common.query import PaginationQuery, SortingQuery
from app.common.filters import FilterOperator
from app.validators.base_validator import BaseValidator, ValidationResult
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.doctor_errors import DoctorErrorCode


class TestResponseContract:
    def test_success_response_structure(self):
        resp = ApiResponse.ok(data={"id": 1}, meta={"total": 1})
        d = resp.to_dict()
        assert d["success"] is True
        assert d["data"] == {"id": 1}
        assert d["meta"] == {"total": 1}
        assert "error" not in d or d.get("error") is None

    def test_error_response_structure(self):
        resp = ApiResponse.fail_with_code(
            code=DoctorErrorCode.DOCTOR_NOT_FOUND,
            message="Médico não encontrado",
        )
        d = resp.to_dict()
        assert d["success"] is False
        assert d["error"]["code"] == "DOCTOR_NOT_FOUND"
        assert d["error"]["message"] == "Médico não encontrado"

    def test_legacy_error_response(self):
        resp = ApiResponse.fail(errors=["old style error"])
        d = resp.to_dict()
        assert d["success"] is False
        assert "old style error" in d["errors"]


class TestPaginationContract:
    def test_page_defaults(self):
        page = Page[int]()
        assert page.page == 1
        assert page.size == 20
        assert page.total == 0
        assert page.pages == 0

    def test_page_calculation(self):
        page = Page[int](items=[1, 2, 3], page=1, size=10, total=25)
        assert page.pages == 3
        assert page.has_next is True
        assert page.has_previous is False

    def test_page_last(self):
        page = Page[int](items=[1], page=3, size=10, total=25)
        assert page.has_next is False
        assert page.has_previous is True

    def test_page_to_dict(self):
        page = Page[int](items=[1, 2], page=1, size=10, total=2)
        d = page.to_dict()
        assert "items" in d
        assert "page" in d
        assert "size" in d
        assert "total" in d
        assert "pages" in d


class TestErrorContract:
    def test_doctor_error_codes(self):
        assert DoctorErrorCode.DOCTOR_ALREADY_EXISTS == "DOCTOR_ALREADY_EXISTS"
        assert DoctorErrorCode.DOCTOR_NOT_FOUND == "DOCTOR_NOT_FOUND"
        assert DoctorErrorCode.DOCTOR_INACTIVE == "DOCTOR_INACTIVE"
        assert DoctorErrorCode.INVALID_CRM == "INVALID_CRM"
        assert DoctorErrorCode.INVALID_HOUR_RATE == "INVALID_HOUR_RATE"
        assert DoctorErrorCode.INVALID_NAME == "INVALID_NAME"


class TestFilterContract:
    def test_pagination_query(self):
        pq = PaginationQuery(page=2, size=10)
        assert pq.offset == 10

    def test_sorting_query(self):
        sq = SortingQuery(field="name", direction="desc")
        assert sq.direction == "desc"

    def test_filter_operators(self):
        assert FilterOperator.CONTAINS == "contains"
        assert FilterOperator.EQUALS == "equals"
        assert FilterOperator.BETWEEN == "between"
        assert FilterOperator.IN == "in"


class TestEventVersioningContract:
    def test_doctor_events_are_versioned(self):
        assert DomainEventName.DOCTOR_CREATED_V1 == "doctor.created.v1"
        assert DomainEventName.DOCTOR_UPDATED_V1 == "doctor.updated.v1"
        assert DomainEventName.DOCTOR_DEACTIVATED_V1 == "doctor.deactivated.v1"

    def test_event_dispatcher_with_versioned_events(self):
        dispatcher = EventDispatcher()
        events = []
        dispatcher.register("doctor.created.v1", lambda e: events.append(e.data))
        dispatcher.dispatch(Event(name="doctor.created.v1", data={"id": 1}))
        assert len(events) == 1
        assert events[0]["id"] == 1
