from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.database import DATABASE_URL, Base
from app.models.marker import Marker
from app.models.trip import Trip
from app.models.user import User

config = context.config

config.set_main_option("sqlalchemy.url", f"{DATABASE_URL}?async_fallback=True")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

__all_models__ = [Trip, User, Marker]

EXISTING_TABLES_NAMESPACE = (
    "auth_",
    "authtoken_",
    "core_",
    "django_",
    "spatial_",
)


def include_object(obj, name, type_, reflected, compare_to):
    """Ignore all Django's tables."""

    if type_ == "table" and name.startswith(EXISTING_TABLES_NAMESPACE):
        return False
    return True


def run_migrations_offline():
    """Run migrations in 'offline' mode."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
