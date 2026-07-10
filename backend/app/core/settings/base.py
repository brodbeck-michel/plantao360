from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    APP_NAME: str = "Plantao360"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./plantao360.db"
    SECRET_KEY: str = "change-me-in-production-use-a-real-secret"
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Bootstrap admin (criado no startup quando não há usuários).
    # Em produção, ProductionSettings valida e recusa a senha padrão.
    ADMIN_EMAIL: str = "admin@plantao360.local"
    ADMIN_PASSWORD: str = "admin123"

    ENABLE_JWT: bool = False
    ENABLE_AUDIT_LOG: bool = False
    ENABLE_BI: bool = False
    ENABLE_ANALYTICS: bool = False
    ENABLE_TASY_INTEGRATION: bool = False
    DEMO_MODE: bool = False

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = {
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }
