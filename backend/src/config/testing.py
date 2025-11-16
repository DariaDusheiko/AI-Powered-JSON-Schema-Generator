from typing import Literal
from pydantic import Field, AmqpDsn, PostgresDsn, RedisDsn
from dataclasses import dataclass

from backend.src.config.base import BaseConfig, Enviroment


class ApplicationConfig(BaseConfig):
    port: int = Field(alias="APP_PORT")
    host: str = Field(alias="APP_HOST")
    path_prefix: str = Field(alias="PATH_PREFIX")

    secret_key: str = Field(alias="ACCESS_TOKEN_SECRET_KEY")
    algorithm: str = Field(alias="ACCESS_TOKEN_ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    reload: bool = Field(alias="RELOAD_APP")


class DatabaseConfig(BaseConfig):
    user: str = Field(alias="DATABASE_USERNAME")
    name: str = Field(alias="DATABASE_NAME")
    password: str = Field(alias="DATABASE_PASSWORD")
    port: int = Field(alias="DATABASE_PORT")
    host: str = Field(alias="DATABASE_HOST")

    @property
    def dsn(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                host=self.host,
                port=self.port,
                path=self.name,
                password=self.password,
            )
        )



class DevelopmentConfig:
    app = ApplicationConfig()
    database = DatabaseConfig()

    env: Literal[Enviroment.TEST] = Enviroment.TEST