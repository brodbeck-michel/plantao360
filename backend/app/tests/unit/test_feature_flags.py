from app.core.features import FeatureFlags, get_feature_flags


def test_feature_flags_all_fields():
    flags = get_feature_flags()
    assert hasattr(flags, "ENABLE_JWT")
    assert hasattr(flags, "ENABLE_AUDIT_LOG")
    assert hasattr(flags, "ENABLE_BI")
    assert hasattr(flags, "ENABLE_ANALYTICS")
    assert hasattr(flags, "ENABLE_TASY_INTEGRATION")
    assert hasattr(flags, "ENABLE_EXPORT_PDF")
    assert hasattr(flags, "ENABLE_IMPORT_LEGACY")
    assert hasattr(flags, "DARK_MODE")
    assert hasattr(flags, "NOTIFICATIONS")
    assert hasattr(flags, "EXPORT_PDF")


def test_feature_flags_are_booleans():
    flags = get_feature_flags()
    assert isinstance(flags.ENABLE_JWT, bool)
    assert isinstance(flags.ENABLE_EXPORT_PDF, bool)
    assert isinstance(flags.ENABLE_IMPORT_LEGACY, bool)


def test_feature_flags_class_defaults():
    flags = FeatureFlags()
    assert flags.ENABLE_JWT is False
    assert flags.ENABLE_EXPORT_PDF is False
    assert flags.ENABLE_IMPORT_LEGACY is False
