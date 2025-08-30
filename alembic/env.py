from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.models import Base
from app.config import settings
import os

config = context.config

# Determine database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    url = DATABASE_URL
else:
    # fallback to local .env settings
    host = settings.database_hostname or "localhost"
    port = int(settings.database_port or 5432)
    user = settings.database_username or "postgres"
    password = settings.database_password or ""
    dbname = settings.database_name or "fastapi"

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

config.set_main_option("sqlalchemy.url", url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
