from enum import Enum


class Roles(str, Enum):
    ADMIN = "ADMIN"
    COORDENADOR = "COORDENADOR"
    FINANCEIRO = "FINANCEIRO"
    MEDICO = "MEDICO"
    CONSULTA = "CONSULTA"


# TODO: Implementar hierarquia de permissões
# TODO: Criar mapeamento Role → Permissions
# TODO: Integrar com JWT claims
