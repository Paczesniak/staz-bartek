"""Konfiguracja środowiska Alembica.

Ten plik odpowiada na dwa pytania:

1. **Z jaką bazą się połączyć?** — z tą samą, z którą łączy się aplikacja,
   czyli spod zmiennej środowiskowej DATABASE_URL. Adres nie jest wpisany
   w `alembic.ini`, żeby istniało dokładnie jedno miejsce, które o nim decyduje.
2. **Jak ma wyglądać baza docelowo?** — tak, jak opisuje `app/models.py`.
   To pozwala Alembicowi porównywać stan bazy z opisem w kodzie.
"""

from __future__ import annotations

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.config import load_settings
from app.db import safe_database_url
from app.models import metadata

config = context.config

# Nazwa loggera zaczyna się od "alembic", więc podlega ustawieniom
# z sekcji [logger_alembic] w alembic.ini.
logger = logging.getLogger("alembic.env")

# Logowanie Alembica wg sekcji [loggers] w alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adres bazy wstrzykiwany z konfiguracji aplikacji (zmienna DATABASE_URL).
DATABASE_URL = load_settings().database_url
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Wzorzec struktury bazy — na jego podstawie działa `alembic revision --autogenerate`.
target_metadata = metadata


def run_migrations_offline() -> None:
    """Tryb offline: zamiast wykonywać SQL, wypisuje go na ekran.

    Przydatne, gdy migracje wykonuje ktoś inny (administrator bazy)
    albo gdy chce się po prostu zobaczyć, co dana migracja zrobi.
    Uruchomienie: `alembic upgrade head --sql`.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Tryb zwykły: łączy się z bazą i wykonuje migracje."""
    logger.info("Łączę się z bazą: %s", safe_database_url(DATABASE_URL))

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # `compare_type=True` sprawia, że autogeneracja zauważa zmianę
            # typu kolumny, a nie tylko dodanie lub usunięcie kolumny.
            compare_type=True,
            # Wymagane, żeby zmiany kolumn działały również na SQLite,
            # który nie potrafi zwykłego ALTER TABLE i musi przepisać tabelę.
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
