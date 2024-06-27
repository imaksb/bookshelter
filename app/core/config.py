import secrets
from typing import Literal
from sqlalchemy.engine.url import URL
from pydantic import computed_field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "IOwHcoGQChEJgA0X27sI5VutIr3Kt_7Sf2dJIdlmUNU" # secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 * 2
    ALGORITHM: str = "HS256"

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["development", "production"] = "development"

    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "development":
            return f"http://{self.DOMAIN}:8000"
        return f"https://{self.DOMAIN}"

    DB_NAME: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    RESET_PASSWORD_TOKEN_EXPIRE_HOURS: int = 24
    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME
        )


settings = Settings()
