# Technical Debt Report

**Generated:** 2026-06-26 17:12

**Files Scanned:** 281

---

## Summary

| Type | Count |
|------|-------|
| TODOs | 37 |
| FIXMEs | 0 |
| Deprecated | 0 |
| Unused Imports | 26 |
| **Total** | **63** |

---

## Items

| File | Line | Type | Message |
|------|------|------|---------|
| app\audit\__init__.py | 3 | TODO | Implementar modelos de audit log |
| app\audit\__init__.py | 4 | TODO | Criar service de auditoria |
| app\audit\__init__.py | 5 | TODO | Integrar com SQLAlchemy events |
| app\audit\__init__.py | 6 | TODO | Adicionar middleware de auditoria |
| app\audit\models.py | 10 | TODO | Implementar com SQLAlchemy |
| app\audit\service.py | 8 | TODO | Implementar service de auditoria |
| app\audit\service.py | 23 | TODO | Persistir no banco de dados |
| app\audit\service.py | 24 | TODO | Enviar para fila de eventos (futuro) |
| app\core\security\dependencies.py | 15 | TODO | Implementar get_current_user com JWT |
| app\core\security\dependencies.py | 18 | TODO | Verificar token JWT no header Authorization |
| app\core\security\dependencies.py | 19 | TODO | Decodificar e validar token |
| app\core\security\dependencies.py | 20 | TODO | Retornar payload do usuário |
| app\core\security\dependencies.py | 24 | TODO | Implementar require_role |
| app\core\security\dependencies.py | 27 | TODO | Criar dependência que verifica se o usuário tem a role necessária |
| app\core\security\dependencies.py | 31 | TODO | Implementar require_permission |
| app\core\security\dependencies.py | 34 | TODO | Criar dependência que verifica se o usuário tem a permissão necessária |
| app\core\security\permissions.py | 11 | TODO | Mapear permissões por recurso |
| app\core\security\permissions.py | 12 | TODO | Criar decorator para verificação de permissão |
| app\core\security\permissions.py | 13 | TODO | Integrar com dependência do FastAPI |
| app\core\security\roles.py | 12 | TODO | Implementar hierarquia de permissões |
| app\core\security\roles.py | 13 | TODO | Criar mapeamento Role → Permissions |
| app\core\security\roles.py | 14 | TODO | Integrar com JWT claims |
| app\observability\__init__.py | 3 | TODO | Implementar OpenTelemetry quando necessário |
| app\observability\__init__.py | 4 | TODO | Adicionar tracing distribuído |
| app\observability\__init__.py | 5 | TODO | Integrar com Jaeger ou Zipkin para visualização de traces |
| app\observability\__init__.py | 6 | TODO | Adicionar métricas customizadas de negócio |
| app\observability\instrumentation.py | 9 | TODO | Instrumentar FastAPI automaticamente |
| app\observability\instrumentation.py | 10 | TODO | Instrumentar SQLAlchemy automaticamente |
| app\observability\instrumentation.py | 11 | TODO | Adicionar hooks de spans customizados |
| app\observability\metrics.py | 8 | TODO | Criar counter de requests |
| app\observability\metrics.py | 9 | TODO | Criar histogram de latência |
| app\observability\metrics.py | 10 | TODO | Criar gauge de conexões ativas |
| app\observability\metrics.py | 11 | TODO | Criar métricas de negócio (plantões criados, escalas geradas) |
| app\observability\tracing.py | 11 | TODO | Criar tracer provider |
| app\observability\tracing.py | 12 | TODO | Configurar exportador OTLP |
| app\observability\tracing.py | 13 | TODO | Adicionar instrumentação automática para FastAPI |
| app\observability\tracing.py | 14 | TODO | Adicionar instrumentação automática para SQLAlchemy |
| app\common\responses.py | 1 | UNUSED_IMPORT | Potentially unused import: field |
| app\database\unit_of_work.py | 1 | UNUSED_IMPORT | Potentially unused import: Generator |
| app\domain\base\aggregate_root.py | 1 | UNUSED_IMPORT | Potentially unused import: annotations |
| app\domain\calendar\business_calendar.py | 1 | UNUSED_IMPORT | Potentially unused import: annotations |
| app\domain\events\event_collector.py | 1 | UNUSED_IMPORT | Potentially unused import: annotations |
| app\domain\metrics\period_metrics.py | 1 | UNUSED_IMPORT | Potentially unused import: field |
| app\domain\rules\shift_rules.py | 1 | UNUSED_IMPORT | Potentially unused import: datetime |
| app\domain\transitions\period_transition.py | 1 | UNUSED_IMPORT | Potentially unused import: field |
| app\domain\value_objects\shift_time_range.py | 1 | UNUSED_IMPORT | Potentially unused import: timedelta |
| app\repositories\base\interfaces.py | 1 | UNUSED_IMPORT | Potentially unused import: Generic |
| app\repositories\shift_repository.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\schemas\assignment\assignment_create.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\schemas\base\__init__.py | 1 | UNUSED_IMPORT | Potentially unused import: ( |
| app\schemas\doctor\doctor_create.py | 1 | UNUSED_IMPORT | Potentially unused import: BaseModel |
| app\schemas\doctor\doctor_detail.py | 1 | UNUSED_IMPORT | Potentially unused import: BaseModel |
| app\schemas\doctor\doctor_response.py | 1 | UNUSED_IMPORT | Potentially unused import: BaseModel |
| app\schemas\doctor\doctor_update.py | 1 | UNUSED_IMPORT | Potentially unused import: BaseModel |
| app\schemas\shift\__init__.py | 1 | UNUSED_IMPORT | Potentially unused import: BaseModel |
| app\schemas\shift\__init__.py | 1 | UNUSED_IMPORT | Potentially unused import: Field |
| app\services\assignment_service.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\services\base\base_service.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\services\doctor_service.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\services\period_service.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\services\shift_service.py | 1 | UNUSED_IMPORT | Potentially unused import: Optional |
| app\use_cases\periods\base_period_use_case.py | 1 | UNUSED_IMPORT | Potentially unused import: Success |
| app\validators\shift_validator.py | 1 | UNUSED_IMPORT | Potentially unused import: time |


---

## By File

### app\audit\__init__.py

- Line 3: [TODO] Implementar modelos de audit log
- Line 4: [TODO] Criar service de auditoria
- Line 5: [TODO] Integrar com SQLAlchemy events
- Line 6: [TODO] Adicionar middleware de auditoria

### app\audit\models.py

- Line 10: [TODO] Implementar com SQLAlchemy

### app\audit\service.py

- Line 8: [TODO] Implementar service de auditoria
- Line 23: [TODO] Persistir no banco de dados
- Line 24: [TODO] Enviar para fila de eventos (futuro)

### app\common\responses.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: field

### app\core\security\dependencies.py

- Line 15: [TODO] Implementar get_current_user com JWT
- Line 18: [TODO] Verificar token JWT no header Authorization
- Line 19: [TODO] Decodificar e validar token
- Line 20: [TODO] Retornar payload do usuário
- Line 24: [TODO] Implementar require_role
- Line 27: [TODO] Criar dependência que verifica se o usuário tem a role necessária
- Line 31: [TODO] Implementar require_permission
- Line 34: [TODO] Criar dependência que verifica se o usuário tem a permissão necessária

### app\core\security\permissions.py

- Line 11: [TODO] Mapear permissões por recurso
- Line 12: [TODO] Criar decorator para verificação de permissão
- Line 13: [TODO] Integrar com dependência do FastAPI

### app\core\security\roles.py

- Line 12: [TODO] Implementar hierarquia de permissões
- Line 13: [TODO] Criar mapeamento Role → Permissions
- Line 14: [TODO] Integrar com JWT claims

### app\database\unit_of_work.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Generator

### app\domain\base\aggregate_root.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: annotations

### app\domain\calendar\business_calendar.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: annotations

### app\domain\events\event_collector.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: annotations

### app\domain\metrics\period_metrics.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: field

### app\domain\rules\shift_rules.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: datetime

### app\domain\transitions\period_transition.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: field

### app\domain\value_objects\shift_time_range.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: timedelta

### app\observability\__init__.py

- Line 3: [TODO] Implementar OpenTelemetry quando necessário
- Line 4: [TODO] Adicionar tracing distribuído
- Line 5: [TODO] Integrar com Jaeger ou Zipkin para visualização de traces
- Line 6: [TODO] Adicionar métricas customizadas de negócio

### app\observability\instrumentation.py

- Line 9: [TODO] Instrumentar FastAPI automaticamente
- Line 10: [TODO] Instrumentar SQLAlchemy automaticamente
- Line 11: [TODO] Adicionar hooks de spans customizados

### app\observability\metrics.py

- Line 8: [TODO] Criar counter de requests
- Line 9: [TODO] Criar histogram de latência
- Line 10: [TODO] Criar gauge de conexões ativas
- Line 11: [TODO] Criar métricas de negócio (plantões criados, escalas geradas)

### app\observability\tracing.py

- Line 11: [TODO] Criar tracer provider
- Line 12: [TODO] Configurar exportador OTLP
- Line 13: [TODO] Adicionar instrumentação automática para FastAPI
- Line 14: [TODO] Adicionar instrumentação automática para SQLAlchemy

### app\repositories\base\interfaces.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Generic

### app\repositories\shift_repository.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\schemas\assignment\assignment_create.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\schemas\base\__init__.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: (

### app\schemas\doctor\doctor_create.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: BaseModel

### app\schemas\doctor\doctor_detail.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: BaseModel

### app\schemas\doctor\doctor_response.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: BaseModel

### app\schemas\doctor\doctor_update.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: BaseModel

### app\schemas\shift\__init__.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: BaseModel
- Line 1: [UNUSED_IMPORT] Potentially unused import: Field

### app\services\assignment_service.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\services\base\base_service.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\services\doctor_service.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\services\period_service.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\services\shift_service.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Optional

### app\use_cases\periods\base_period_use_case.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: Success

### app\validators\shift_validator.py

- Line 1: [UNUSED_IMPORT] Potentially unused import: time

