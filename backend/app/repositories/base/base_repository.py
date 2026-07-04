from typing import TypeVar, Generic, Optional, Type

from sqlalchemy.orm import Session

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def create(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        self.session.flush()
        return entity

    def update(self, entity: ModelType) -> ModelType:
        merged = self.session.merge(entity)
        self.session.flush()
        return merged

    def delete(self, id: int) -> bool:
        entity = self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.flush()
            return True
        return False

    def soft_delete(self, id: int) -> bool:
        entity = self.get_by_id(id)
        if entity:
            if hasattr(entity, "active"):
                entity.active = False
            self.session.flush()
            return True
        return False

    def exists(self, id: int) -> bool:
        return self.session.query(self.model).filter(self.model.id == id).first() is not None

    def count(self) -> int:
        return self.session.query(self.model).count()
