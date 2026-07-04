from pydantic import BaseModel, Field


class PeriodQueryDTO(BaseModel):
    search: str | None = Field(None, description="Busca geral")
    year: int | None = Field(None, description="Filtro por ano")
    month: int | None = Field(None, description="Filtro por mes")
    status: str | None = Field(None, description="Filtro por status")
    page: int = Field(1, ge=1, description="Numero da pagina")
    size: int = Field(20, ge=1, le=100, description="Itens por pagina")
    sort_by: str = Field("id", description="Campo para ordenacao")
    sort_direction: str = Field("asc", description="Direcao: asc ou desc")

    def __post_init__(self) -> None:
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "year", "month", "status", "active"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
