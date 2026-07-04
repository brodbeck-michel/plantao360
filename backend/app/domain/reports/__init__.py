"""Report Definitions — Contracts for query output."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ReportField:
    """A single field in a report definition."""
    name: str
    label: str
    field_type: str
    required: bool = True
    description: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "label": self.label,
            "field_type": self.field_type,
            "required": self.required,
            "description": self.description,
            "source": self.source,
        }


@dataclass(frozen=True)
class ReportFilter:
    """A single filter in a report definition."""
    name: str
    label: str
    filter_type: str
    required: bool = False
    default_value: str = ""
    options: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "label": self.label,
            "filter_type": self.filter_type,
            "required": self.required,
            "default_value": self.default_value,
            "options": self.options,
        }


@dataclass(frozen=True)
class ReportDefinition:
    """Contract for a report. Defines what data is available.

    Não gera PDF, Excel ou gráficos. Apenas contrato.
    """
    name: str
    description: str
    objective: str
    fields: list[ReportField] = field(default_factory=list)
    filters: list[ReportFilter] = field(default_factory=list)
    sort_by: str = ""
    sort_direction: str = "asc"
    permissions: list[str] = field(default_factory=list)
    data_source: str = ""
    version: str = "1.0"
    created_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "objective": self.objective,
            "fields": [f.to_dict() for f in self.fields],
            "filters": [f.to_dict() for f in self.filters],
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
            "permissions": self.permissions,
            "data_source": self.data_source,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
