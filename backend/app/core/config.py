from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "Restaurant ERP Pro"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = (
        "Enterprise Restaurant ERP & POS System"
    )
    APP_ENV: str = "development"

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "CHANGE_ME"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/restaurant_erp"
    )

    REDIS_URL: str = "redis://localhost:6379/0"

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    DEFAULT_LANGUAGE: str = "ar"
    DEFAULT_CURRENCY: str = "EGP"
    DEFAULT_TIMEZONE: str = "Africa/Cairo"

    COMPANY_NAME: str = "Restaurant ERP Pro"

    PASSWORD_MIN_LENGTH: int = 8

    MAX_LOGIN_ATTEMPTS: int = 5

    LOCKOUT_MINUTES: int = 15

    LOG_LEVEL: str = "INFO"

    DEBUG: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
