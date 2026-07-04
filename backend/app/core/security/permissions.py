from enum import Enum


class Permissions(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


# TODO: Mapear permissões por recurso
# TODO: Criar decorator para verificação de permissão
# TODO: Integrar com dependência do FastAPI
