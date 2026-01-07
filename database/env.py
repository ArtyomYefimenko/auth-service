"""
Provide configurations of Alembic.
"""
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

config = context.config

assert config.config_file_name
fileConfig(config.config_file_name)

from auth_service.core.config import settings
db_url_escaped = settings.async_database_url.replace('%', '%%')
config.set_main_option('sqlalchemy.url', db_url_escaped)

from auth_service.models import *

from auth_service.core.database import ModelBaseDeclarative
target_metadata = ModelBaseDeclarative.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable here as well.
    By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option('sqlalchemy.url')

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            'paramstyle': 'named',
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(connection):
    """
    Run migrations.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """
    Run migrations asynchronously.
    """
    connectable = async_engine_from_config(
        configuration=config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(fn=run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context.
    """
    connectable = config.attributes.get("connection", None)

    if connectable is None:
        asyncio.run(run_async_migrations())

    else:
        run_migrations(connectable)


if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()
