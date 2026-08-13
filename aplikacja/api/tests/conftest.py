"""Wspólne przygotowanie testów.

Testy działają na bazie SQLite trzymanej w PAMIĘCI (`sqlite://`), więc:

* nie potrzebują uruchomionego serwera ani działającej bazy,
* nie zostawiają po sobie żadnych plików,
* każdy test dostaje pustą bazę, więc kolejność testów nie ma znaczenia.

To jest dokładnie to, czego potrzeba w potoku CI: `pytest` i tyle.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models import metadata

# Adres bazy w pamięci. Baza znika razem z procesem testowym.
IN_MEMORY_DATABASE_URL = "sqlite://"

ClientFactory = Callable[..., TestClient]


@pytest.fixture
def make_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[ClientFactory]:
    """Fabryka klientów testowych z możliwością nadpisania zmiennych środowiskowych.

    Konfiguracja aplikacji pochodzi wyłącznie ze zmiennych środowiskowych,
    więc test konfiguracji to po prostu test z innymi zmiennymi.
    """
    created: list[TestClient] = []

    def _build(**environment: str) -> TestClient:
        defaults = {
            "APP_NAME": "linkbox",
            "DATABASE_URL": IN_MEMORY_DATABASE_URL,
            "CORS_ORIGINS": "",
            "LOG_LEVEL": "WARNING",
        }
        for name, value in {**defaults, **environment}.items():
            monkeypatch.setenv(name, value)

        application = create_app()
        # Tworzymy strukturę bazy bezpośrednio z opisu w `models.py`.
        # W testach nie uruchamiamy Alembica — sprawdzamy zachowanie
        # aplikacji, a nie samą procedurę migracji.
        metadata.create_all(application.state.engine)

        client = TestClient(application)
        client.__enter__()  # uruchamia procedurę startową aplikacji (lifespan)
        created.append(client)
        return client

    yield _build

    for client in created:
        client.__exit__(None, None, None)


@pytest.fixture
def client(make_client: ClientFactory) -> TestClient:
    """Domyślny klient testowy: pusta baza w pamięci, CORS wyłączony."""
    return make_client()


@pytest.fixture
def sample_url() -> str:
    """Przykładowy poprawny adres docelowy używany w wielu testach."""
    return "https://example.com/bardzo/dluga/sciezka?parametr=1"
