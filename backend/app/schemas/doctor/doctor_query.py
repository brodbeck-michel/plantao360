from pydantic import BaseModel, Field


class DoctorQueryDTO(BaseModel):
    search: str | None = Field(None, description="Busca geral (nome ou CRM)")
    name: str | None = Field(None, description="Filtro por nome")
    crm: str | None = Field(None, description="Filtro por CRM")
    active: bool | None = Field(None, description="Filtro por status")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Itens por página")
    sort_by: str = Field("id", description="Campo para ordenação")
    sort_direction: str = Field("asc", description="Direção: asc ou desc")

    def __post_init__(self) -> None:
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "name", "crm", "hour_rate", "active"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
