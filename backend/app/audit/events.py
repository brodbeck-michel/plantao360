"""Audit events - contratos para eventos de auditoria."""

from enum import StrEnum


class AuditAction(StrEnum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]
