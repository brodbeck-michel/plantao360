from pydantic import model_validator

from app.core.settings.base import BaseAppSettings


# Valores de exemplo/placeholder que NUNCA podem ir para produção.
INSECURE_SECRET_KEYS = {
    "",
    "change-me-in-production-use-a-real-secret",
    "change-this-to-a-real-secret-in-production",
}
INSECURE_ADMIN_PASSWORDS = {
    "",
    "admin123",
    "admin",
    "password",
    "changeme",
}


class ProductionSettings(BaseAppSettings):
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "WARNING"
    DATABASE_URL: str = "postgresql+psycopg2://user:pass@localhost:5432/plantao360"

    model_config = {
        "env_file": ".env.production",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @model_validator(mode="after")
    def _validate_production_secrets(self) -> "ProductionSettings":
        """Falha rápido se segredos padrão/fracos forem usados em produção.

        Rodar a aplicação com o SECRET_KEY de exemplo permitiria forjar tokens
        JWT; um admin com senha padrão é acesso total conhecido. Melhor não subir.
        """
        errors: list[str] = []

        if self.SECRET_KEY in INSECURE_SECRET_KEYS or len(self.SECRET_KEY) < 32:
            errors.append(
                "SECRET_KEY inseguro ou ausente. Defina um valor aleatório com "
                ">= 32 caracteres no .env.production. Gere um com: "
                'python -c "import secrets; print(secrets.token_urlsafe(48))"'
            )

        if self.ADMIN_PASSWORD in INSECURE_ADMIN_PASSWORDS or len(self.ADMIN_PASSWORD) < 8:
            errors.append(
                "ADMIN_PASSWORD inseguro ou ausente. Defina ADMIN_PASSWORD no "
                ".env.production com >= 8 caracteres e diferente dos valores padrão."
            )

        if errors:
            raise ValueError(
                "Configuração de produção insegura — startup abortado:\n  - "
                + "\n  - ".join(errors)
            )
        return self
