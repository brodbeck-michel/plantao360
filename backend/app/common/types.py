from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]
Headers: TypeAlias = dict[str, str]
QueryParams: TypeAlias = dict[str, str | int | float | bool | None]

UUIDStr = str
RequestID = UUIDStr
CorrelationID = UUIDStr
AuditID = UUIDStr
EventID = UUIDStr
