"""
Security dependencies para FastAPI.

TODO: Implementar quando JWT estiver habilitado:
- get_current_user
- require_role
- require_permission
"""

from typing import Any

from fastapi import Depends, Request


# TODO: Implementar get_current_user com JWT
async def get_current_user(request: Request) -> dict[str, Any] | None:
    """Retorna o usuário atual da requisição."""
    # TODO: Verificar token JWT no header Authorization
    # TODO: Decodificar e validar token
    # TODO: Retornar payload do usuário
    return getattr(request.state, "user", None)


# TODO: Implementar require_role
def require_role(*roles):
    """Factory de dependência para verificação de role."""
    # TODO: Criar dependência que verifica se o usuário tem a role necessária
    pass


# TODO: Implementar require_permission
def require_permission(permission: str):
    """Factory de dependência para verificação de permissão."""
    # TODO: Criar dependência que verifica se o usuário tem a permissão necessária
    pass
