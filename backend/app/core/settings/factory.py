import os
from functools import lru_cache

from app.core.settings.base import BaseAppSettings
from app.core.settings.development import DevelopmentSettings
from app.core.settings.production import ProductionSettings
from app.core.settings.test import TestSettings


@lru_cache
def get_settings() -> BaseAppSettings:
    environment = os.getenv("ENVIRONMENT", "development").lower()

    settings_map = {
        "development": DevelopmentSettings,
        "production": ProductionSettings,
        "test": TestSettings,
    }

    settings_class = settings_map.get(environment, DevelopmentSettings)
    return settings_class()
