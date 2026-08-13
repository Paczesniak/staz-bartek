"""Sprawy procesu: logowanie na stdout i reakcja na sygnały systemowe.

To warstwa „aplikacja jako proces w systemie”, a nie „aplikacja jako API”.
Dwie rzeczy, które są tu ważne w codziennej eksploatacji:

1. Logi idą na **stdout**, nie do pliku. Proces nie decyduje, gdzie trafi
   jego log — decyduje o tym to, co go uruchomiło (systemd, kontener,
   zwykły terminal).
2. Aplikacja reaguje na **SIGTERM**, czyli grzeczne „skończ pracę”.
   Bez tego zatrzymanie usługi kończy się twardym ubiciem procesu
   z otwartymi połączeniami do bazy.
"""

from __future__ import annotations

import logging
import os
import signal
import sys
from collections.abc import Callable
from types import FrameType

from app import __version__
from app.config import Settings
from app.db import backend_name, safe_database_url

logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(app)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

# Sygnały, na które reagujemy: SIGTERM wysyła systemd i `docker stop`,
# SIGINT to Ctrl+C w terminalu.
HANDLED_SIGNALS = (signal.SIGTERM, signal.SIGINT)


class _AppNameFilter(logging.Filter):
    """Dokłada do każdego wpisu nazwę aplikacji z APP_NAME.

    Dzięki temu, gdy w dzienniku spotkają się logi dwóch instancji,
    widać od razu, która z nich co napisała.
    """

    def __init__(self, app_name: str) -> None:
        super().__init__()
        self._app_name = app_name

    def filter(self, record: logging.LogRecord) -> bool:
        record.app = self._app_name
        return True


def configure_logging(level: str, app_name: str) -> None:
    """Ustawia logowanie całej aplikacji na standardowe wyjście.

    Świadomie NIE piszemy do pliku. Proces uruchomiony jako usługa systemd
    ma swój log w dzienniku systemowym, proces w kontenerze — w logu
    kontenera. Gdyby aplikacja sama pisała do pliku, obie te ścieżki
    byłyby puste i diagnostyka zaczynałaby się od szukania pliku.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    handler.addFilter(_AppNameFilter(app_name))

    root = logging.getLogger()
    # Podmieniamy uchwyty zamiast dokładać kolejny — inaczej przy ponownym
    # utworzeniu aplikacji (np. w testach) każdy wpis pojawiłby się dwa razy.
    for existing in list(root.handlers):
        root.removeHandler(existing)
    root.addHandler(handler)
    root.setLevel(level)


def log_startup_banner(settings: Settings) -> None:
    """Wypisuje przy starcie komplet informacji o konfiguracji.

    To ma być pierwsza rzecz, do której sięga się przy pytaniu
    „dlaczego to nie działa?”. Widać tu wszystko, co aplikacja wzięła
    ze zmiennych środowiskowych — a więc też to, czego NIE wzięła,
    bo zmiennej nie ustawiono.
    """
    logger.info("Uruchamiam aplikację %s w wersji %s", settings.app_name, __version__)
    logger.info(
        "Nasłuchuję na %s:%s (dokumentacja API: http://%s:%s/docs)",
        settings.app_host,
        settings.app_port,
        settings.app_host,
        settings.app_port,
    )
    if settings.app_host in ("127.0.0.1", "localhost", "::1"):
        logger.info(
            "APP_HOST=%s oznacza, że aplikacja przyjmuje połączenia wyłącznie "
            "z tej samej maszyny — z innego komputera będzie niewidoczna",
            settings.app_host,
        )
    logger.info(
        "Baza danych: %s (%s)",
        backend_name(settings.database_url),
        safe_database_url(settings.database_url),
    )
    if settings.cors_enabled:
        logger.info(
            "CORS: WŁĄCZONY dla %d origin-ów: %s",
            len(settings.cors_origins),
            ", ".join(settings.cors_origins),
        )
    else:
        logger.info(
            "CORS: WYŁĄCZONY — zmienna CORS_ORIGINS jest pusta, więc odpowiedzi "
            "nie zawierają nagłówków CORS"
        )
    logger.info("Poziom logowania: %s (zmienna LOG_LEVEL)", settings.log_level)


def install_signal_handlers() -> None:
    """Podpina własną obsługę SIGTERM i SIGINT.

    Sygnał to nie to samo co zabicie procesu. `kill -9` (SIGKILL) jest
    nieprzechwytywalny — proces znika natychmiast, bez szansy na sprzątanie.
    SIGTERM to prośba: „zakończ pracę”, i aplikacja może na nią odpowiedzieć.

    Nie zastępujemy obsługi, którą ustawił serwer — dokładamy własny wpis
    do logu i oddajemy sterowanie poprzedniej procedurze, żeby serwer mógł
    dokończyć swoje zamykanie (dokończyć trwające żądania, wywołać
    procedurę zamknięcia aplikacji).
    """
    for handled_signal in HANDLED_SIGNALS:
        _install_one_handler(handled_signal)


def _install_one_handler(handled_signal: signal.Signals) -> None:
    """Podpina obsługę jednego sygnału, zachowując poprzednią procedurę."""
    try:
        previous = signal.getsignal(handled_signal)
        signal.signal(handled_signal, _make_handler(handled_signal, previous))
    except (ValueError, OSError, RuntimeError):
        # `signal.signal` działa wyłącznie w głównym wątku procesu.
        # W testach aplikacja bywa uruchamiana w wątku pobocznym — wtedy
        # po prostu nie ma czego podpinać i nie jest to błąd.
        logger.debug(
            "Nie udało się podpiąć obsługi sygnału %s (prawdopodobnie wątek poboczny)",
            handled_signal.name,
            exc_info=True,
        )


def _make_handler(
    handled_signal: signal.Signals,
    previous: Callable[[int, FrameType | None], object] | int | None,
) -> Callable[[int, FrameType | None], None]:
    """Buduje procedurę obsługi sygnału opakowującą poprzednią."""

    def handler(signal_number: int, frame: FrameType | None) -> None:
        logger.info(
            "Otrzymano sygnał %s — rozpoczynam zamykanie aplikacji "
            "(dokańczam trwające żądania i zamykam połączenia z bazą)",
            handled_signal.name,
        )
        if callable(previous):
            previous(signal_number, frame)
            return
        if previous == signal.SIG_IGN:
            return
        # Nikt inny nie obsługiwał tego sygnału — przywracamy zachowanie
        # domyślne i wysyłamy sygnał ponownie do siebie, żeby proces
        # faktycznie się zakończył.
        signal.signal(handled_signal, signal.SIG_DFL)
        os.kill(os.getpid(), signal_number)

    return handler
