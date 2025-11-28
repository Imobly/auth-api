import os
from typing import List

from pydantic_settings import BaseSettings


def _split_csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Allow overriding CORS origins via env var comma-separated list
    CORS_ORIGINS: List[str] = _split_csv(
        os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
    )

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
