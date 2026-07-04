from app.core.settings.base import BaseAppSettings


class DevelopmentSettings(BaseAppSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///./plantao360.db"

    model_config = {
        "env_file": ".env.development",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
