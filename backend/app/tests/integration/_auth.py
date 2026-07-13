"""Auth de teste compartilhada para os testes de integração.

Os endpoints são protegidos por `Depends(get_current_user)` / `require_role(...)` (RBAC).
Como `require_role` depende internamente de `get_current_user`, basta sobrescrever
`get_current_user` por um usuário ADMIN falso para destravar a auth em qualquer app de teste.
"""
from app.core.security.dependencies import get_current_user
from app.models.user import User


def fake_admin() -> User:
    """Usuário ADMIN não-persistido (id/role/active são o que a auth usa)."""
    return User(
        id=1,
        name="Test Admin",
        email="admin@test.local",
        password_hash="x",
        role="ADMIN",
        active=True,
    )


def install_auth_override(app) -> None:
    """Sobrescreve a auth de um app FastAPI de teste por um ADMIN falso."""
    app.dependency_overrides[get_current_user] = fake_admin
