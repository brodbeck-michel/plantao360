from pydantic import BaseModel, Field, model_validator


class PeriodFilterDTO(BaseModel):
    page: int = Field(1, ge=1, description="Numero da pagina")
    size: int = Field(20, ge=1, le=100, description="Itens por pagina")
    year: int | None = Field(None, description="Filtro por ano")
    month: int | None = Field(None, description="Filtro por mes")
    status: str | None = Field(None, description="Filtro por status")
    sort_by: str = Field("id", description="Campo para ordenacao")
    sort_direction: str = Field("asc", description="Direcao: asc ou desc")

    @model_validator(mode="after")
    def _validate_sort(self) -> "PeriodFilterDTO":
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "year", "month", "status", "created_at"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
        return self

    def to_filters(self) -> dict:
        filters = {}
        if self.year is not None:
            filters["year"] = self.year
        if self.month is not None:
            filters["month"] = self.month
        if self.status is not None:
            filters["status"] = self.status
        return filters
