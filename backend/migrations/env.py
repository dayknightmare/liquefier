from src.application.spi.db_interface import Base
from sqlalchemy import engine_from_config
from logging.config import fileConfig
from src.adapters.spi.db.db import Db
from sqlalchemy import pool
from alembic import context
import importlib
import os


files = list(os.walk("src/models/"))[0]
db = Db()

for i in files[2]:
    if not i.endswith(".py"):
        continue

    importlib.import_module("src.models." + i.split(".")[0])

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option(
    "sqlalchemy.url",
    db.get_db().db_url,
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()
