from typing import Any

from pydantic import model_validator, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8")

    secret_key: str
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    mysql_dsn: MySQLDsn

    @model_validator(mode="before")
    @classmethod
    def create_mysql_dsn(cls, data: Any):
        user = data["db_user"]
        password = data["db_password"]
        name = data["db_name"]
        host = data["db_host"]
        data["mysql_dsn"] = MySQLDsn(
            f"mysql+asyncmy://{user}:{password}@{host}:5432/{name}?charset=utf8mb4"
        )
        return data


settings = Settings()  # type: ignore
