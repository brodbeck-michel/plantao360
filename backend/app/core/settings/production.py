from app.core.settings.base import BaseAppSettings


class ProductionSettings(BaseAppSettings):
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "WARNING"
    DATABASE_URL: str = "postgresql+psycopg2://user:pass@localhost:5432/plantao360"

    model_config = {
        "env_file": ".env.production",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
