"""Konfiguracja aplikacji — wyłącznie ze zmiennych środowiskowych.

Zasada: w kodzie nie ma ŻADNEJ wartości konfiguracyjnej wpisanej na sztywno
w miejscu użycia. Wszystko przechodzi przez ten moduł, dzięki czemu jest
jedno miejsce, w którym widać cały kontrakt konfiguracyjny aplikacji.

Wszystkie zmienne mają wartości domyślne, dlatego czytamy je przez
`os.environ.get(nazwa, domyślna)`. Gdyby któraś była WYMAGANA (np. hasło,
dla którego nie wolno wymyślać domyślnej wartości), użylibyśmy
`os.environ["NAZWA"]` — wtedy brak zmiennej zatrzymuje aplikację od razu
przy starcie, z czytelnym `KeyError`, zamiast objawiać się dziwnym błędem
pół godziny później.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Wartości domyślne. Zebrane w jednym miejscu, żeby dokumentacja
# (README, .env.example) miała jedno źródło prawdy.
DEFAULT_APP_NAME = "linkbox"
DEFAULT_APP_HOST = "127.0.0.1"
DEFAULT_APP_PORT = "8000"
DEFAULT_DATABASE_URL = "sqlite:///./links.db"
DEFAULT_LOG_LEVEL = "INFO"

# CELOWO pusty string. Domyślnie aplikacja NIE wysyła nagłówków CORS,
# więc front serwowany z innego portu dostanie błąd w przeglądarce.
# To jest zamierzone ćwiczenie — rozwiązaniem jest ustawienie zmiennej
# środowiskowej CORS_ORIGINS, a nie zmiana kodu.
DEFAULT_CORS_ORIGINS = ""

VALID_LOG_LEVELS = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG")


@dataclass(frozen=True)
class Settings:
    """Niezmienny (frozen) zestaw ustawień aplikacji.

    `frozen=True` oznacza, że po wczytaniu konfiguracji nikt jej już nie
    podmieni w trakcie działania procesu. Konfiguracja zmienia się przez
    restart z innymi zmiennymi środowiskowymi — tak samo jak w usłudze
    systemd czy w kontenerze.
    """

    app_name: str
    app_host: str
    app_port: int
    database_url: str
    cors_origins: tuple[str, ...]
    log_level: str

    @property
    def cors_enabled(self) -> bool:
        """Czy obsługa CORS jest w ogóle włączona (lista origin-ów niepusta)."""
        return len(self.cors_origins) > 0


def load_settings() -> Settings:
    """Wczytuje konfigurację ze zmiennych środowiskowych.

    Funkcja jest czysta w tym sensie, że nie trzyma stanu — każde wywołanie
    czyta środowisko od nowa. Aplikacja woła ją raz, przy starcie.
    """
    return Settings(
        app_name=os.environ.get("APP_NAME", DEFAULT_APP_NAME).strip() or DEFAULT_APP_NAME,
        app_host=os.environ.get("APP_HOST", DEFAULT_APP_HOST).strip() or DEFAULT_APP_HOST,
        app_port=parse_port(os.environ.get("APP_PORT", DEFAULT_APP_PORT)),
        database_url=os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL).strip()
        or DEFAULT_DATABASE_URL,
        cors_origins=parse_cors_origins(os.environ.get("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)),
        log_level=parse_log_level(os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)),
    )


def parse_port(raw: str) -> int:
    """Zamienia tekst na numer portu i sprawdza, czy mieści się w zakresie.

    Błędna wartość zatrzymuje aplikację przy starcie — lepiej nie wstać
    z jasnym komunikatem niż wstać na losowym porcie.
    """
    try:
        port = int(raw.strip())
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"APP_PORT musi być liczbą całkowitą, otrzymano: {raw!r}") from exc

    if not 1 <= port <= 65535:
        raise ValueError(f"APP_PORT musi mieścić się w zakresie 1-65535, otrzymano: {port}")
    return port


def parse_cors_origins(raw: str) -> tuple[str, ...]:
    """Rozbija listę origin-ów rozdzieloną przecinkami na krotkę.

    Przykład: `"http://localhost:3000, http://localhost:5173"` daje dwa wpisy.
    Puste fragmenty i białe znaki są pomijane, więc pusty string oznacza
    „CORS wyłączony”.

    Origin to schemat + host + port (`http://localhost:3000`), bez ścieżki
    na końcu — to ta sama definicja, którą przeglądarka pokazuje w błędzie CORS.
    """
    if not raw:
        return ()
    return tuple(origin.strip() for origin in raw.split(",") if origin.strip())


def parse_log_level(raw: str) -> str:
    """Normalizuje poziom logowania; nieznana wartość to błąd konfiguracji."""
    level = raw.strip().upper()
    if level not in VALID_LOG_LEVELS:
        raise ValueError(
            f"LOG_LEVEL musi być jedną z wartości {', '.join(VALID_LOG_LEVELS)}, "
            f"otrzymano: {raw!r}"
        )
    return level
