from pydantic import BaseModel


class BaseCreateDTO(BaseModel):
    pass


class BaseUpdateDTO(BaseModel):
    pass


class BaseResponseDTO(BaseModel):
    id: int

    model_config = {"from_attributes": True}


class BaseFilterDTO(BaseModel):
    page: int = 1
    size: int = 20

    def __post_init__(self) -> None:
        if self.page < 1:
            self.page = 1
        if self.size < 1:
            self.size = 1
        if self.size > 100:
            self.size = 100


class BaseListDTO(BaseModel):
    items: list[BaseResponseDTO]
    page: int
    size: int
    total: int
    pages: int
