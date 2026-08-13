"""Testy warstwy procesu: obsługa sygnałów i wczytywanie konfiguracji."""

from __future__ import annotations

import logging
import signal

import pytest

from app.config import parse_cors_origins, parse_log_level, parse_port
from app.runtime import install_signal_handlers


def test_sigterm_is_logged_and_passed_further(caplog: pytest.LogCaptureFixture) -> None:
    """Aplikacja reaguje na SIGTERM: zapisuje to w logu i oddaje sterowanie dalej.

    Podstawiamy własną procedurę obsługi jako „poprzednią”, żeby sprawdzić,
    że nasza obsługa jej nie gubi. W prawdziwym uruchomieniu tą poprzednią
    procedurą jest zamykanie serwera — gdyby została pominięta, aplikacja
    zapisałaby w logu, że się zamyka, i działała dalej.
    """
    delivered: list[int] = []
    original_term = signal.getsignal(signal.SIGTERM)
    original_int = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGTERM, lambda number, frame: delivered.append(number))

    try:
        install_signal_handlers()
        with caplog.at_level(logging.INFO, logger="app.runtime"):
            signal.raise_signal(signal.SIGTERM)
    finally:
        signal.signal(signal.SIGTERM, original_term)
        signal.signal(signal.SIGINT, original_int)

    assert delivered == [int(signal.SIGTERM)], "poprzednia procedura obsługi nie została wywołana"
    assert any("SIGTERM" in record.message for record in caplog.records)


def test_parse_cors_origins_splits_and_trims() -> None:
    """Lista origin-ów jest rozdzielana przecinkami, z pominięciem spacji."""
    assert parse_cors_origins("http://a:3000, http://b:5173") == (
        "http://a:3000",
        "http://b:5173",
    )


@pytest.mark.parametrize("raw", ["", "   ", ",", " , "])
def test_parse_cors_origins_treats_blank_as_disabled(raw: str) -> None:
    """Pusta wartość CORS_ORIGINS oznacza CORS wyłączony."""
    assert parse_cors_origins(raw) == ()


@pytest.mark.parametrize("raw", ["abc", "", "0", "70000", "-1"])
def test_parse_port_rejects_invalid_values(raw: str) -> None:
    """Błędny APP_PORT zatrzymuje aplikację przy starcie, zamiast działać losowo."""
    with pytest.raises(ValueError):
        parse_port(raw)


def test_parse_log_level_normalizes_case() -> None:
    """Poziom logowania można podać małymi literami."""
    assert parse_log_level("debug") == "DEBUG"


def test_parse_log_level_rejects_unknown_value() -> None:
    """Literówka w LOG_LEVEL to błąd konfiguracji, a nie cicho przyjęta wartość."""
    with pytest.raises(ValueError):
        parse_log_level("VERBOSE")
