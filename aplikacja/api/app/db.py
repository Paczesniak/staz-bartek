"""Połączenie z bazą danych — tworzenie silnika, kontrola stanu, sprzątanie.

Aplikacja rozmawia z bazą przez jeden obiekt `Engine` (pula połączeń),
tworzony raz przy starcie i zamykany przy zatrzymaniu procesu.

Cały kod SQL w tej aplikacji jest przenośny. Jedyne miejsce, które w ogóle
patrzy na rodzaj bazy, to `_connect_options()` — i dotyczy ono wyłącznie
sposobu, w jaki sterownik SQLite pilnuje wątków, a nie tego, jak wygląda SQL.
"""

from __future__ import annotations

import logging

import sqlalchemy as sa
from sqlalchemy.engine import URL, Engine, make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)


def create_db_engine(database_url: str) -> Engine:
    """Tworzy silnik SQLAlchemy dla podanego adresu bazy.

    `pool_pre_ping=True` sprawia, że przed użyciem połączenia z puli
    SQLAlchemy sprawdza, czy ono jeszcze żyje. Bez tego restart bazy
    zostawia w puli martwe połączenia i pierwsze żądania po restarcie
    kończą się błędem.
    """
    url = make_url(database_url)
    engine = sa.create_engine(
        url,
        pool_pre_ping=True,
        future=True,
        **_connect_options(url),
    )
    logger.debug("Utworzono silnik bazy danych: %s", safe_database_url(database_url))
    return engine


def _connect_options(url: URL) -> dict[str, object]:
    """Zwraca opcje sterownika zależne od rodzaju bazy.

    UWAGA — to jedyne miejsce w aplikacji, które rozróżnia bazy, i dotyczy
    wyłącznie zachowania sterownika, nie SQL-a:

    * `check_same_thread=False` — sterownik `sqlite3` domyślnie zabrania
      używać połączenia w innym wątku niż ten, który je otworzył.
      FastAPI obsługuje żądania w puli wątków, więc bez tej opcji
      część żądań kończyłaby się błędem sterownika.
    * `StaticPool` dla bazy w pamięci — baza `sqlite://` żyje wyłącznie
      wewnątrz jednego połączenia. Gdyby pula otwierała kolejne, każde
      widziałoby własną, pustą bazę. Używane w testach.

    Dla PostgreSQL i innych baz zwracamy pusty słownik, czyli domyślne
    zachowanie SQLAlchemy — podmiana DATABASE_URL nie wymaga zmian w kodzie.
    """
    if url.get_backend_name() != "sqlite":
        return {}

    options: dict[str, object] = {"connect_args": {"check_same_thread": False}}
    if not url.database or url.database == ":memory:":
        options["poolclass"] = StaticPool
    return options


def check_database(engine: Engine) -> bool:
    """Sprawdza, czy baza odpowiada. Zwraca True/False, nie rzuca wyjątkiem.

    To jest sonda dla `/health` i dla metryki `linkbox_up`, więc jej zadaniem
    jest dać odpowiedź, a nie wywrócić żądanie. Błąd trafia do logu z pełną
    treścią (`exc_info`) — do klienta idzie tylko informacja „error”,
    bez szczegółów, które zdradzałyby budowę bazy.
    """
    try:
        with engine.connect() as connection:
            connection.execute(sa.text("SELECT 1"))
        return True
    except SQLAlchemyError:
        logger.error("Baza danych nie odpowiada na zapytanie kontrolne", exc_info=True)
        return False


def dispose_engine(engine: Engine) -> None:
    """Zamyka wszystkie połączenia z puli.

    Wołane przy zatrzymywaniu aplikacji (również po SIGTERM), żeby baza
    nie zostawała z wiszącymi sesjami po stronie serwera.
    """
    engine.dispose()
    logger.info("Zamknięto połączenia z bazą danych")


def backend_name(database_url: str) -> str:
    """Zwraca nazwę silnika bazy (np. `sqlite`, `postgresql`) do logów i metryk."""
    return make_url(database_url).get_backend_name()


def safe_database_url(database_url: str) -> str:
    """Zwraca adres bazy z ukrytym hasłem — wersja bezpieczna do logowania.

    Adres PostgreSQL potrafi zawierać hasło (`postgresql://user:haslo@host/db`).
    Logi lądują w journalu, w Dockerze i prędzej czy później w systemie
    zbierania logów — hasło nie ma prawa się tam znaleźć.
    """
    return make_url(database_url).render_as_string(hide_password=True)
