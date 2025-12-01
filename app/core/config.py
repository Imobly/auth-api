import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS origins - accepts comma-separated list from env or defaults to localhost
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:admin123@postgres:5432/auth_db",
    )

    DB_SSLMODE: str | None = os.getenv("DB_SSLMODE", "require")
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "auth_api")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    HOST: str = os.getenv("HOST", "0.0.0.0")
    # Render provides PORT env var; fall back to 8000 locally
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
