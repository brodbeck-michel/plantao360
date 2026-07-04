from app.core.settings.base import BaseAppSettings


class TestSettings(BaseAppSettings):
    ENVIRONMENT: str = "test"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "test-secret-key-not-for-production"

    model_config = {
        "env_file": ".env.test",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
