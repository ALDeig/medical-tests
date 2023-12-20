from typing import Any

from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8")

    secret_key: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_dsn: PostgresDsn

    @model_validator(mode="before")
    @classmethod
    def create_postgres_dsn(cls, data: Any):
        user = data["postgres_user"]
        password = data["postgres_password"]
        name = data["postgres_db"]
        host = data["postgres_host"]
        data["postgres_dsn"] = PostgresDsn(
            f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}"
        )
        return data


settings = Settings()  # type: ignore
