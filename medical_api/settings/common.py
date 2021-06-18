import os

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, Field
from sqlalchemy.engine.url import make_url


class Settings(BaseSettings):
    DEBUG: bool = False
    APP_NAME: str = "Medical API"
    APP_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = (
        "{level} {time:YYYY-MM-DD HH:mm:ss} {name}:{function}-{message} | {extra}"
    )


class DatabaseSettings(BaseSettings):
    username: str = Field(
        ...,
        description="Имя пользователя для подключения к БД",
    )
    password: str = Field(
        ...,
        description="Пароль для подключения к БД",
    )
    url: AnyUrl = Field(
        ...,
        description="URL (DSN) путь для подключения к базе данных",
    )
    db_schema: str = Field(
        ...,
        description="Название схемы БД",
    )
    db_name: str = Field(..., description="Имя БД")

    @property
    def full_url_async(self) -> str:
        """
        URL (DSN) путь для подключения к базе данных вместе
        с username и password с указанием асинхронного драйвера
        """
        url = make_url(self.url + self.db_name)
        url = url.set(
            drivername="postgresql+asyncpg",
            username=self.username,
            password=self.password,
        )
        return str(url)

    @property
    def full_url_sync(self) -> str:
        """ "
        URL (DSN) путь для подключения к базе данных вместе
        с username и password с указанием синхронного драйвера
        """
        url = make_url(self.url + self.db_name)
        url = url.set(
            drivername="postgresql",
            username=self.username,
            password=self.password,
        )
        return str(url)

    class Config:
        env_prefix = "database_"
        env_file_encoding = "utf8"
        env_file = os.getenv("DATABASE_ENV_FILE", "./.env.local")
        extra = "ignore"


settings = Settings()
database_settings = DatabaseSettings()

# For convinience
DEBUG = settings.DEBUG
APP_NAME = settings.APP_NAME
APP_VERSION = settings.APP_VERSION
