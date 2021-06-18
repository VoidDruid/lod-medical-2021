from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine import Connectable, Engine

from database.base import metadata as target_metadata
from settings import database_settings


config = context.config
config.set_main_option("sqlalchemy.url", database_settings.full_url_async)

fileConfig(config.config_file_name)  # setting up loggers


def make_tables_list(config_):
    if not config_:
        return []
    tables_ = config_.get("tables", "")
    return tables_.split(",")


exclude_tables = make_tables_list(config.get_section("alembic:exclude"))
reflected_tables = make_tables_list(config.get_section("alembic:reflected"))


def include_object(object_, name, type_, reflected, compare_to):
    if type_ == "table" and name in exclude_tables:
        return False
    if type_.endswith("_constraint") and any(
        map(lambda table: name.startswith(table), reflected_tables)
    ):
        return False
    return True


def run_migrations_offline() -> None:  # pragma: no cover
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=database_settings.full_url_sync,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=database_settings.db_schema,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connectable) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=database_settings.db_schema,
        include_schemas=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online_sync(engine: Engine) -> None:
    with engine.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():  # pragma: no cover
    run_migrations_offline()
else:
    engine = create_engine(database_settings.full_url_sync, echo=True)
    run_migrations_online_sync(engine)
