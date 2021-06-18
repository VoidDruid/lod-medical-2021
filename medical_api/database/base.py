from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from common import to_snake
from settings import database_settings


ASYNC_DRIVER_NAME = "postgresql+asyncpg"
SYNC_DRIVER_NAME = "postgresql"


def make_sync_session_factory(
    database_url: str = database_settings.full_url_sync,
) -> sessionmaker:
    sessionmaker_kwargs = {
        "autocommit": False,
        "autoflush": False,
        "bind": create_engine(database_url),
    }
    return sessionmaker(**sessionmaker_kwargs)


def make_async_session_factory(
    database_url: str = database_settings.full_url_async,
) -> sessionmaker:
    sessionmaker_kwargs = {
        "autocommit": False,
        "autoflush": False,
        "bind": create_async_engine(database_url),
        "class_": AsyncSession,
    }
    return sessionmaker(**sessionmaker_kwargs)


def make_sync_scoped_session_factory(
    database_url: str = database_settings.full_url_sync,
) -> scoped_session:
    session_factory = make_sync_session_factory(database_url)
    return scoped_session(session_factory)


def make_async_scoped_session_factory(
    database_url: str = database_settings.full_url_async,
) -> scoped_session:
    session_factory = make_async_session_factory(database_url)
    return scoped_session(session_factory)


sync_session = make_sync_session_factory()
async_session = make_async_scoped_session_factory()

metadata = MetaData(schema=database_settings.db_schema)


@as_declarative(metadata=metadata)
class Base:
    @declared_attr
    def __tablename__(  # pylint: disable=no-self-argument
        cls,  # noqa:N805
    ) -> str:
        return to_snake(cls.__name__)  # type: ignore  # pylint: disable=no-member
