"""Punkt wejścia aplikacji — złożenie wszystkich elementów w jedną całość.

Aplikacja jest budowana funkcją `create_app()`, a nie w kodzie modułu.
Dzięki temu testy tworzą własną instancję (z bazą w pamięci) bez żadnych
sztuczek, a produkcyjne uruchomienie korzysta z obiektu `app` na końcu pliku.

Aplikacja jest BEZSTANOWA: nie trzyma w pamięci niczego, co byłoby potrzebne
do obsłużenia kolejnego żądania. Cały stan siedzi w bazie. Dlatego można
uruchomić dwie kopie tego samego procesu i rozdzielić między nie ruch.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sqlalchemy as sa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app import __version__
from app.config import Settings, load_settings
from app.db import check_database, create_db_engine, dispose_engine
from app.errors import register_error_handlers
from app.metrics import MetricsRegistry
from app.middleware import register_metrics_middleware
from app.routes import links, redirect, system
from app.runtime import configure_logging, install_signal_handlers, log_startup_banner

logger = logging.getLogger(__name__)

API_DESCRIPTION = """
Skracacz linków — aplikacja bazowa programu stażowego DevOps.

Zamienia długi adres na krótki kod. Wejście pod `/r/{code}` przekierowuje
pod adres docelowy i zwiększa licznik kliknięć.

Odpowiedzi błędne mają zawsze postać `{"detail": "komunikat"}`.
"""


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Cykl życia aplikacji: co się dzieje przy starcie i przy zatrzymaniu.

    Kod przed `yield` wykonuje się raz, gdy serwer wstaje. Kod po `yield` —
    gdy serwer się zatrzymuje, również po otrzymaniu sygnału SIGTERM.
    To jest miejsce na zamknięcie połączeń, żeby zatrzymanie usługi było
    czyste, a nie polegało na tym, że system w końcu ubije proces.
    """
    settings: Settings = application.state.settings
    install_signal_handlers()
    log_startup_banner(settings)
    _warn_if_database_not_ready(application)

    yield

    logger.info("Zatrzymuję aplikację %s", settings.app_name)
    dispose_engine(application.state.engine)
    logger.info("Aplikacja %s zatrzymana", settings.app_name)


def _warn_if_database_not_ready(application: FastAPI) -> None:
    """Ostrzega w logu, gdy baza nie odpowiada albo nie ma jeszcze tabel.

    Aplikacja mimo to wstaje — i tak ma być. Endpoint `/health` odpowie
    wtedy kodem 503, co jest czytelnym sygnałem dla monitoringu.
    Aplikacja, która przy niedostępnej bazie po prostu nie startuje,
    jest trudniejsza w diagnozie: nie ma jak jej o nic zapytać.
    """
    engine = application.state.engine
    if not check_database(engine):
        logger.warning(
            "Baza danych nie odpowiada — /health będzie zwracać 503 do czasu "
            "przywrócenia połączenia"
        )
        return

    try:
        if not sa.inspect(engine).has_table("links"):
            logger.warning(
                "W bazie nie ma tabeli 'links' — zapytania będą kończyć się błędem. "
                "Czy migracje zostały uruchomione?"
            )
    except SQLAlchemyError:
        logger.error("Nie udało się sprawdzić struktury bazy danych", exc_info=True)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Buduje gotową do uruchomienia aplikację FastAPI.

    Kolejność ma znaczenie: najpierw konfiguracja i logowanie (żeby wszystko
    dalsze miało gdzie logować), potem zasoby współdzielone, na końcu trasy.
    """
    settings = settings or load_settings()
    configure_logging(settings.log_level, settings.app_name)

    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=API_DESCRIPTION,
        lifespan=lifespan,
    )

    # Obiekty współdzielone przez wszystkie żądania. Trasy sięgają po nie
    # przez zależności z `dependencies.py`, nie przez zmienne globalne.
    application.state.settings = settings
    application.state.engine = create_db_engine(settings.database_url)
    application.state.metrics = MetricsRegistry(settings.app_name)

    register_error_handlers(application)
    register_metrics_middleware(application)
    _configure_cors(application, settings)

    application.include_router(system.router)
    application.include_router(links.router)
    application.include_router(redirect.router)

    return application


def _configure_cors(application: FastAPI, settings: Settings) -> None:
    """Włącza obsługę CORS wyłącznie wtedy, gdy podano listę origin-ów.

    CORS to reguła PRZEGLĄDARKI. Serwer sam z siebie nie blokuje niczego —
    to przeglądarka odmawia skryptowi dostępu do odpowiedzi, jeśli serwer
    nie potwierdził wprost, że zna dany origin. Dlatego `curl` działa
    zawsze, a ta sama odpowiedź w przeglądarce potrafi być odrzucona.

    Origin to schemat + host + port. `http://localhost:3000` i
    `http://localhost:8000` to dwa różne origin-y, mimo tego samego hosta.
    """
    if not settings.cors_enabled:
        return

    application.add_middleware(
        CORSMiddleware,
        # Wyłącznie origin-y z listy. Nigdy "*" — gwiazdka oznacza
        # „każda strona w internecie może odpytywać to API z przeglądarki
        # użytkownika”, a to rzadko jest to, o co komuś chodzi.
        allow_origins=list(settings.cors_origins),
        # To API nie używa ciasteczek ani nagłówka Authorization, więc nie
        # pozwalamy przeglądarce dołączać do żądań danych uwierzytelniających.
        allow_credentials=False,
        # Tylko metody, które API faktycznie obsługuje.
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )


# Obiekt używany przez serwer: `uvicorn app.main:app`
app = create_app()
