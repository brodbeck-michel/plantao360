"""DTO de filtros para consulta de auditoria."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AuditFilterDTO(BaseModel):
    """Filtros para consulta da trilha de auditoria."""

    page: int = Field(1, ge=1, description="Número da página (1-based)")
    size: int = Field(20, ge=1, le=100, description="Itens por página")
    user_id: Optional[int] = Field(None, description="Filtrar por user_id do autor")
    resource: Optional[str] = Field(None, description="Tipo de recurso (assignment, shift_extra, doctor, user, period)")
    resource_id: Optional[int] = Field(None, description="ID do recurso específico")
    period_id: Optional[int] = Field(None, description="Filtrar por competência relacionada")
    start_date: Optional[datetime] = Field(None, description="Filtrar eventos a partir desta data (UTC)")
    end_date: Optional[datetime] = Field(None, description="Filtrar eventos até esta data (UTC)")
