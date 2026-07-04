from app.common.result import Success, Failure
from app.common.pagination import Page
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.list")


class ListAssignments(BaseAssignmentUseCase):
    def validate(self, **kwargs) -> Failure | None:
        return None

    def execute(self, **kwargs) -> Success:
        shift_id = kwargs.get("shift_id")
        doctor_id = kwargs.get("doctor_id")
        status = kwargs.get("status")
        page = kwargs.get("page", 1)
        size = kwargs.get("size", 20)

        skip = (page - 1) * size

        filters = {}
        if shift_id:
            filters["shift_id"] = shift_id
        if doctor_id:
            filters["doctor_id"] = doctor_id
        if status:
            filters["status"] = status

        items = self.repo.search(skip=skip, limit=size, **filters)
        total = self.repo.count_filtered(**filters)

        dtos = []
        for item in items:
            dtos.append({
                "id": item.id,
                "shift_id": item.shift_id,
                "doctor_id": item.doctor_id,
                "start_time": str(item.start_time),
                "end_time": str(item.end_time),
                "status": item.status,
                "duration_minutes": item.duration_minutes,
            })

        page_result = Page(items=dtos, page=page, size=size, total=total)
        return Success(data=page_result.to_dict())
