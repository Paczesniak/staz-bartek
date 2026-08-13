"""Zależności FastAPI — wspólne obiekty wstrzykiwane do funkcji obsługi tras.

Aplikacja trzyma swoje obiekty współdzielone (konfigurację, silnik bazy,
rejestr metryk) w `app.state`. Trasy nie sięgają po nie przez zmienne
globalne, tylko dostają je przez `Depends(...)` — dzięki temu w testach
da się podstawić inną bazę bez dotykania kodu tras.
"""

from __future__ import annotations

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.engine import Connection, Engine

from app.config import Settings
from app.metrics import MetricsRegistry


def get_settings(request: Request) -> Settings:
    """Zwraca konfigurację aplikacji wczytaną przy starcie."""
    return request.app.state.settings


def get_engine(request: Request) -> Engine:
    """Zwraca silnik bazy danych (pulę połączeń)."""
    return request.app.state.engine


def get_metrics(request: Request) -> MetricsRegistry:
    """Zwraca rejestr metryk aplikacji."""
    return request.app.state.metrics


def get_connection(request: Request) -> Iterator[Connection]:
    """Wypożycza połączenie z bazą na czas jednego żądania.

    Połączenie wraca do puli automatycznie po zakończeniu żądania, również
    gdy obsługa zakończy się błędem. Zmiany trzeba zatwierdzić jawnym
    `connection.commit()` w funkcji trasy — bez tego zamknięcie połączenia
    wycofuje transakcję. Wygląda to na dodatkową pracę, ale jest tu celowe:
    widać dokładnie, w którym miejscu dane naprawdę trafiają do bazy.
    """
    engine: Engine = request.app.state.engine
    with engine.connect() as connection:
        yield connection
