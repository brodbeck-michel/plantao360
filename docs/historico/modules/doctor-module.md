# Módulo Médicos — Golden Module

**Data:** 2026-06-24

---

## Estrutura

```
app/
├── schemas/doctor/doctor_dto.py    # DTOs
├── repositories/doctor_repository.py  # Repository
├── services/doctor_service.py      # Service
├── mappers/doctor_mapper.py        # Mapper
├── validators/doctor_validator.py  # Validator
├── api/routes/doctors.py           # Router
└── tests/
    ├── unit/test_doctor_*.py       # Unit tests
    ├── integration/test_doctors_api.py  # Integration tests
    └── contracts/test_patterns_integration.py  # Contract tests
```

---

## DTOs

```python
# Create
DoctorCreateDTO(name, crm, hour_rate)

# Update
DoctorUpdateDTO(name?, crm?, hour_rate?)

# Response
DoctorResponseDTO(id, name, crm, hour_rate, active)

# Filter
DoctorFilterDTO(page, size, name?, crm?, active?, sort_by, sort_direction)
```

---

## Repository

```python
repo = DoctorRepository(session)

# Métodos base (herdados)
repo.get_by_id(id)
repo.list(skip, limit)
repo.create(entity)
repo.update(entity)
repo.delete(id)
repo.exists(id)
repo.count()

# Métodos customizados
repo.get_by_crm(crm)
repo.exists_by_crm(crm, exclude_id?)
repo.search(name?, crm?, active?, skip, limit, sort_by, sort_direction)
repo.count_filtered(name?, crm?, active?)
repo.soft_delete(id)
```

---

## Service

```python
service = DoctorService(uow)

# List com paginação e filtros
page = service.list(filter_dto)  # Page[DoctorResponseDTO]

# Get by ID
result = service.get_by_id(id)  # Result[DoctorResponseDTO]

# Create
result = service.create(dto)  # Result[DoctorResponseDTO]

# Update
result = service.update(id, dto)  # Result[DoctorResponseDTO]

# Soft Delete
result = service.delete(id)  # Result[bool]
```

---

## Mapper

```python
mapper = DoctorMapper()

dto = mapper.to_dto(doctor_model)
model = mapper.to_model(doctor_dto)
dtos = mapper.to_dto_list([doctor1, doctor2])
```

---

## Validator

```python
validator = DoctorValidator()
result = validator.validate(dto)
if not result.is_valid:
    print(result.errors)
```

---

## Router

```
GET    /api/v1/doctors/           # List
GET    /api/v1/doctors/{id}       # Get
POST   /api/v1/doctors/           # Create
PUT    /api/v1/doctors/{id}       # Update
DELETE /api/v1/doctors/{id}       # Soft Delete
```

---

## Response Format

```json
{
    "success": true,
    "data": { "id": 1, "name": "Dr. João", "crm": "12345", "hour_rate": 150.0, "active": true },
    "meta": {},
    "errors": []
}
```

---

## Testes

| Camada | Arquivo | Testes |
|--------|---------|--------|
| Model | test_doctor_model.py | 1 |
| Repository | test_doctor_repository.py | 11 |
| Service | test_doctor_service.py | 10 |
| Mapper | test_doctor_mapper.py | 3 |
| Validator | test_doctor_validator.py | 7 |
| Integration | test_doctors_api.py | 8 |
| Contracts | test_patterns_integration.py | 6 |

**Total: 46 testes**

---

## Checklist para Novos Módulos

- [ ] Model com TimestampMixin e/ou SoftDeleteMixin
- [ ] DTOs (Create, Update, Response, Filter)
- [ ] Repository com métodos customizados
- [ ] Service com CRUD via UoW
- [ ] Mapper (Model ↔ DTO)
- [ ] Validator com regras específicas
- [ ] Router com ApiResponse
- [ ] Unit tests (Repository, Service, Mapper, Validator)
- [ ] Integration tests (Router)
- [ ] Contract tests (patterns)
