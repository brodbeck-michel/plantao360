from typing import TypeVar, Generic, Type

from pydantic import BaseModel

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateDTOType = TypeVar("CreateDTOType", bound=BaseModel)
ResponseDTOType = TypeVar("ResponseDTOType", bound=BaseModel)


class BaseMapper(Generic[ModelType, CreateDTOType, ResponseDTOType]):
    def __init__(
        self,
        model_class: Type[ModelType],
        create_dto_class: Type[CreateDTOType],
        response_dto_class: Type[ResponseDTOType],
    ):
        self.model_class = model_class
        self.create_dto_class = create_dto_class
        self.response_dto_class = response_dto_class

    def to_model(self, dto: CreateDTOType) -> ModelType:
        return self.model_class(**dto.model_dump())

    def to_response(self, model: ModelType) -> ResponseDTOType:
        return self.response_dto_class.model_validate(model)

    def update_model(self, model: ModelType, dto: BaseModel) -> ModelType:
        update_data = dto.model_dump(exclude_unset=True)
        for field_name, value in update_data.items():
            setattr(model, field_name, value)
        return model

    def to_summary(self, model: ModelType) -> dict:
        return {
            "id": model.id,
            "name": getattr(model, "name", None),
            "crm": getattr(model, "crm", None),
            "active": getattr(model, "active", None),
        }

    def to_response_list(self, models: list[ModelType]) -> list[ResponseDTOType]:
        return [self.to_response(m) for m in models]
