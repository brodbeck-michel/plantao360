"""Fixtures compartilhadas dos testes de integração.

Motivo: cada teste monta um app FastAPI e sobrescreve `get_db`, mas os endpoints são
protegidos por `Depends(get_current_user)` / `require_role(...)` (RBAC, Sprint 19). Sem
sobrescrever a auth, todos retornam 401.

A lógica de override vive em `_auth.py` (importável tanto aqui quanto por testes que montam o
app real, como `test_bootstrap`). A fixture `auth_override` apenas expõe o instalador.
"""
import pytest

from app.tests.integration._auth import install_auth_override


@pytest.fixture
def auth_override():
    """Instalador de auth para a `client` fixture: `auth_override(test_app)`."""
    return install_auth_override
