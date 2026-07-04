from app.core.config import get_settings
from app.core.features import get_feature_flags


def test_settings_loads():
    settings = get_settings()
    assert settings.APP_NAME == "Plantao360"
    assert settings.ENVIRONMENT in ("development", "production", "test")


def test_settings_has_required_fields():
    settings = get_settings()
    assert hasattr(settings, "DATABASE_URL")
    assert hasattr(settings, "SECRET_KEY")
    assert hasattr(settings, "LOG_LEVEL")
    assert hasattr(settings, "ALLOWED_ORIGINS")


def test_feature_flags_loads():
    flags = get_feature_flags()
    assert hasattr(flags, "ENABLE_JWT")
    assert hasattr(flags, "ENABLE_AUDIT_LOG")
    assert hasattr(flags, "ENABLE_BI")
    assert hasattr(flags, "ENABLE_ANALYTICS")
    assert hasattr(flags, "ENABLE_TASY_INTEGRATION")
    assert hasattr(flags, "ENABLE_EXPORT_PDF")
    assert hasattr(flags, "ENABLE_IMPORT_LEGACY")
