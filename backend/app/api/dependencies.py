from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.session import get_db
from app.core.config import get_settings
from app.core.features import get_feature_flags, FeatureFlags
from app.core.security.dependencies import get_current_user


def get_database(db: Session = Depends(get_db)) -> Session:
    """Dependência para injeção de sessão do banco."""
    return db


def get_config():
    """Dependência para configuração."""
    return get_settings()


def get_flags() -> FeatureFlags:
    """Dependência para feature flags."""
    return get_feature_flags()
