from app.core.settings.factory import get_settings
from app.core.settings.base import BaseAppSettings
from app.core.settings.development import DevelopmentSettings
from app.core.settings.production import ProductionSettings
from app.core.settings.test import TestSettings


def test_settings_factory_returns_base():
    settings = get_settings()
    assert isinstance(settings, BaseAppSettings)


def test_settings_has_allowed_origins_list():
    settings = get_settings()
    assert isinstance(settings.allowed_origins_list, list)
    assert len(settings.allowed_origins_list) > 0


def test_development_settings_defaults():
    settings = DevelopmentSettings.model_validate({"ENVIRONMENT": "development"})
    assert settings.ENVIRONMENT == "development"
    assert settings.LOG_LEVEL == "DEBUG"


def test_production_settings_defaults():
    settings = ProductionSettings.model_validate({"ENVIRONMENT": "production"})
    assert settings.ENVIRONMENT == "production"
    assert settings.LOG_LEVEL == "WARNING"


def test_test_settings_defaults():
    settings = TestSettings()
    assert settings.ENVIRONMENT == "test"
    assert "test-secret" in settings.SECRET_KEY
