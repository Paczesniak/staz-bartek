"""Walidacja danych wchodzących do aplikacji.

Zasada: nie ufamy niczemu, co przyszło z zewnątrz. Sprawdzamy na granicy
systemu (tutaj), a dalej w kodzie zakładamy już, że dane są poprawne.

Funkcje walidujące rzucają `ValidationError` z gotowym komunikatem po polsku.
Warstwa HTTP (`routes/links.py`) zamienia go na odpowiedź 400.
"""

from __future__ import annotations

import re
import secrets
from urllib.parse import urlparse

from app.models import CODE_MAX_LENGTH, CODE_MIN_LENGTH, URL_MAX_LENGTH

# Dozwolone schematy adresu docelowego. Świadomie tylko te dwa: `file://`,
# `javascript:` czy `data:` w przekierowaniu to gotowa dziura bezpieczeństwa.
ALLOWED_URL_SCHEMES = ("http", "https")

# Kod widoczny w adresie: litery, cyfry, myślnik i podkreślnik.
# Bez kropek i ukośników, żeby kod nie mógł udawać ścieżki.
CODE_PATTERN = re.compile(rf"^[A-Za-z0-9_-]{{{CODE_MIN_LENGTH},{CODE_MAX_LENGTH}}}$")

# Alfabet losowanych kodów — bez znaków, które łatwo pomylić przy przepisywaniu
# (0/O, 1/l/I). Skracacz linków ma być czytelny, gdy ktoś przepisuje kod z ekranu.
CODE_ALPHABET = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
GENERATED_CODE_LENGTH = 3


class ValidationError(Exception):
    """Dane wejściowe są niepoprawne. Treść wyjątku trafia wprost do klienta."""


def validate_url(raw_url: str) -> str:
    """Sprawdza adres docelowy i zwraca go w postaci oczyszczonej z białych znaków.

    Wymagania: schemat `http` lub `https`, niepusta nazwa hosta, sensowna długość.
    """
    url = (raw_url or "").strip()

    if not url:
        raise ValidationError("Pole 'url' jest wymagane i nie może być puste.")

    if len(url) > URL_MAX_LENGTH:
        raise ValidationError(
            f"Adres URL jest za długi — maksymalna długość to {URL_MAX_LENGTH} znaków."
        )

    parsed = urlparse(url)

    if parsed.scheme.lower() not in ALLOWED_URL_SCHEMES:
        raise ValidationError(
            "Adres URL musi zaczynać się od 'http://' lub 'https://'. " f"Otrzymano: {url!r}"
        )

    if not parsed.netloc:
        raise ValidationError(
            f"Adres URL nie zawiera nazwy hosta (np. 'https://example.com'). Otrzymano: {url!r}"
        )

    return url


def validate_code(raw_code: str) -> str:
    """Sprawdza własny kod podany przez użytkownika i zwraca go oczyszczonego."""
    code = (raw_code or "").strip()

    if not CODE_PATTERN.match(code):
        raise ValidationError(
            f"Kod może zawierać wyłącznie litery, cyfry, '-' i '_' oraz mieć od "
            f"{CODE_MIN_LENGTH} do {CODE_MAX_LENGTH} znaków. Otrzymano: {raw_code!r}"
        )

    return code


def generate_code() -> str:
    """Losuje kod dla linku, gdy użytkownik nie podał własnego.

    `secrets` zamiast `random` — kody bywają traktowane jak adresy „nie do
    zgadnięcia”, a `random` jest przewidywalny, jeśli ktoś zna wcześniejsze wyniki.
    Kolizję (kod już zajęty) obsługuje warstwa zapisu, ponawiając losowanie.
    """
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(GENERATED_CODE_LENGTH))


def opis_kodu(code: str, prefiks: str = "link") -> str:
    """Zwraca krótki opis kodu do logów."""
    return f"{prefiks}:{code}" if code else f"{prefiks}:(brak)"
