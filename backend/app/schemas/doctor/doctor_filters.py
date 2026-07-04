from pydantic import BaseModel, Field, model_validator


class DoctorFilterDTO(BaseModel):
    page: int = Field(1, ge=1, description="Numero da pagina")
    size: int = Field(20, ge=1, le=100, description="Itens por pagina")
    name: str | None = Field(None, description="Filtro por nome (parcial)")
    crm: str | None = Field(None, description="Filtro por CRM (parcial)")
    active: bool | None = Field(None, description="Filtro por status ativo")
    sort_by: str = Field("id", description="Campo para ordenacao")
    sort_direction: str = Field("asc", description="Direcao: asc ou desc")

    @model_validator(mode="after")
    def _validate_sort(self) -> "DoctorFilterDTO":
        if self.sort_direction not in ("asc", "desc"):
            self.sort_direction = "asc"
        allowed_sorts = {"id", "name", "crm", "hour_rate", "active", "specialty", "created_at"}
        if self.sort_by not in allowed_sorts:
            self.sort_by = "id"
        return self

    def to_filters(self) -> dict:
        filters = {}
        if self.name is not None:
            filters["name"] = self.name
        if self.crm is not None:
            filters["crm"] = self.crm
        if self.active is not None:
            filters["active"] = self.active
        return filters
