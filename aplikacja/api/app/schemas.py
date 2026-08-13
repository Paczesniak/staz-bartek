"""Modele danych wejścia i wyjścia (Pydantic).

Te klasy opisują kontrakt API i zasilają dokumentację pod `/docs`.
Właściwa walidacja treści (poprawność URL-a, dozwolone znaki w kodzie)
siedzi w `validation.py` — dzięki temu błędne dane dostają odpowiedź 400
z jednym, czytelnym komunikatem po polsku, a nie techniczny raport 422.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LinkCreate(BaseModel):
    """Treść żądania POST /api/links."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"url": "https://example.com/bardzo/dluga/sciezka"},
                {"url": "https://example.com", "code": "moj-kod"},
            ]
        }
    )

    url: str = Field(description="Adres docelowy przekierowania (http:// lub https://)")
    code: str | None = Field(
        default=None,
        description=(
            "Opcjonalny własny kod. Gdy pominięty, serwer losuje kod. "
            "Dozwolone znaki: litery, cyfry, '-' i '_'."
        ),
    )


class LinkOut(BaseModel):
    """Reprezentacja linku zwracana przez API."""

    code: str = Field(description="Kod widoczny w adresie /r/{code}")
    url: str = Field(description="Adres docelowy przekierowania")
    clicks: int = Field(description="Liczba wykonanych przekierowań")
    created_at: datetime = Field(description="Data utworzenia (UTC)")


class HealthOut(BaseModel):
    """Odpowiedź endpointu /health."""

    status: str = Field(description="'ok' albo 'error'")
    database: str = Field(description="Stan połączenia z bazą: 'ok' albo 'error'")
    version: str = Field(description="Wersja aplikacji")


class ErrorOut(BaseModel):
    """Jednolity format błędu — każdy błąd API wygląda tak samo."""

    detail: str = Field(description="Komunikat błędu po polsku")
