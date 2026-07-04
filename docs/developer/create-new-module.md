# Guia: Criar Novo Módulo (usando Doctors como template)

**Data:** 2026-06-25

---

## Passo a Passo

### 1. Model

Criar `app/models/{module}.py`:

```python
from sqlalchemy import String, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from app.models.base_mixins import TimestampMixin, SoftDeleteMixin

class Period(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "periods"
    __table_args__ = (
        Index("ix_periods_name", "name", unique=True),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
```

Registrar em `app/models/__init__.py`.

---

### 2. DTOs (7 arquivos)

Criar `app/schemas/{module}/`:

| Arquivo | Conteúdo |
|---------|----------|
| `{module}_create.py` | `BaseCreateDTO` + campos obrigatórios |
| `{module}_update.py` | `BaseUpdateDTO` + campos opcionais |
| `{module}_response.py` | `BaseResponseDTO` + todos os campos |
| `{module}_summary.py` | `BaseModel` + id, nome, campos essenciais |
| `{module}_detail.py` | `BaseResponseDTO` + campos + relações |
| `{module}_filters.py` | `BaseModel` + page, size, sort, filtros |
| `{module}_query.py` | `BaseModel` + search + filtros avançados |

Registrar em `__init__.py`.

---

### 3. Repository Interface

Criar `app/repositories/interfaces/{module}_repository.py`:

```python
from typing import Protocol, Optional
from app.models.{module} import {Model}

class {Module}RepositoryInterface(Protocol):
    def get_by_id(self, id: int) -> Optional[{Model}]: ...
    def create(self, entity: {Model}) -> {Model}: ...
    def update(self, entity: {Model}) -> {Model}: ...
    def soft_delete(self, id: int) -> bool: ...
    def exists(self, id: int) -> bool: ...
    def count(self) -> int: ...
```

---

### 4. Repository Implementation

Criar `app/repositories/{module}_repository.py`:

```python
from app.models.{module} import {Model}
from app.repositories.base.base_repository import BaseRepository

class {Module}Repository(BaseRepository[{Model}]):
    def __init__(self, session):
        super().__init__({Model}, session)
```

---

### 5. Specifications

Criar `app/repositories/specifications/{module}_specifications.py`:

```python
from app.repositories.specifications.base_specification import BaseSpecification

class NameContains(BaseSpecification):
    def __init__(self, name: str):
        self.name = name
    def is_satisfied_by(self, query):
        return query.filter({Model}.name.ilike(f"%{self.name}%"))
```

---

### 6. Error Codes

Criar `app/domain/errors/{module}_errors.py`:

```python
from enum import StrEnum

class {Module}ErrorCode(StrEnum):
    {MODULE}_NOT_FOUND = "{MODULE}_NOT_FOUND"
    {MODULE}_ALREADY_EXISTS = "{MODULE}_ALREADY_EXISTS"
```

---

### 7. Validator Rules

Criar `app/validators/rules/`:

```python
def validate_{rule}(value) -> list[str]:
    errors = []
    if not value:
        errors.append("Campo obrigatório")
    return errors
```

Criar `app/validators/{module}_validator.py`:

```python
class {Module}Validator(BaseValidator):
    def _validate(self, data, result):
        # Orquestra regras
        for error in validate_{rule}(data.field):
            result.add_error(error)
```

---

### 8. Mapper

Criar `app/mappers/{module}_mapper.py`:

```python
from app.mappers.base_mapper import BaseMapper

class {Module}Mapper(BaseMapper[{Model}, {CreateDTO}, {ResponseDTO}]):
    def __init__(self):
        super().__init__({Model}, {CreateDTO}, {ResponseDTO})
```

---

### 9. Service

Criar `app/services/{module}_service.py`:

```python
class {Module}Service:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> {Module}Repository:
        return {Module}Repository(self.uow.session)

    def list(self, filter_dto) -> Page: ...
    def get_by_id(self, id) -> Result: ...
    def create(self, dto) -> Result: ...
    def update(self, id, dto) -> Result: ...
    def delete(self, id) -> Result: ...
```

---

### 10. Router

Criar `app/api/routes/{module}s.py`:

```python
router = APIRouter(prefix="/{module}s", tags=["{Modules}"])

@router.get("/")
def list_{module}s(...): ...

@router.get("/{id}")
def get_{module}(...): ...

@router.post("/", status_code=201)
def create_{module}(...): ...

@router.put("/{id}")
def update_{module}(...): ...

@router.delete("/{id}")
def delete_{module}(...): ...
```

Registrar em `app/api/app.py`.

---

### 11. Tests

Criar:

- `tests/unit/test_{module}_model.py`
- `tests/unit/test_{module}_repository.py`
- `tests/unit/test_{module}_service.py`
- `tests/unit/test_{module}_mapper.py`
- `tests/unit/test_{module}_validator.py`
- `tests/integration/test_{module}s_api.py`
- `tests/contracts/test_{module}_contracts.py`

---

### 12. Documentação

Criar `docs/modules/{module}-module.md`.

---

## Checklist Obrigatório

- [ ] Model com TimestampMixin + SoftDeleteMixin
- [ ] 7 DTOs especializados
- [ ] Repository Interface (Protocol)
- [ ] Repository Implementation (BaseRepository)
- [ ] Specifications (NameContains, etc)
- [ ] Error Codes (StrEnum)
- [ ] Validator com Rules
- [ ] Mapper (BaseMapper)
- [ ] Service (via UoW)
- [ ] Router com ApiResponse + Headers
- [ ] Eventos versionados (v1)
- [ ] AuditContext
- [ ] Unit tests (5+)
- [ ] Integration tests (5+)
- [ ] Contract tests (5+)
- [ ] Documentation
