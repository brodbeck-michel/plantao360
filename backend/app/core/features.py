from dataclasses import dataclass


@dataclass
class FeatureFlags:
    DARK_MODE: bool = True
    NOTIFICATIONS: bool = False
    EXPORT_PDF: bool = False
    ENABLE_JWT: bool = False
    ENABLE_AUDIT_LOG: bool = False
    ENABLE_BI: bool = False
    ENABLE_ANALYTICS: bool = False
    ENABLE_TASY_INTEGRATION: bool = False
    ENABLE_EXPORT_PDF: bool = False
    ENABLE_IMPORT_LEGACY: bool = False


def get_feature_flags() -> FeatureFlags:
    import os

    def _flag(name: str, default: str = "false") -> bool:
        return os.getenv(name, default).lower() == "true"

    return FeatureFlags(
        DARK_MODE=_flag("DARK_MODE", "true"),
        NOTIFICATIONS=_flag("NOTIFICATIONS"),
        EXPORT_PDF=_flag("EXPORT_PDF"),
        ENABLE_JWT=_flag("ENABLE_JWT"),
        ENABLE_AUDIT_LOG=_flag("ENABLE_AUDIT_LOG"),
        ENABLE_BI=_flag("ENABLE_BI"),
        ENABLE_ANALYTICS=_flag("ENABLE_ANALYTICS"),
        ENABLE_TASY_INTEGRATION=_flag("ENABLE_TASY_INTEGRATION"),
        ENABLE_EXPORT_PDF=_flag("ENABLE_EXPORT_PDF"),
        ENABLE_IMPORT_LEGACY=_flag("ENABLE_IMPORT_LEGACY"),
    )
