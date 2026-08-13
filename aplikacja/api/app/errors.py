"""Jednolita obsługa błędów — każdy błąd API wygląda tak samo.

Kontrakt: odpowiedź błędna to zawsze `{"detail": "komunikat po polsku"}`.
Bez wyjątków, bez dwóch różnych formatów zależnie od tego, kto rzucił błąd.

Druga zasada: komunikat dla klienta ma być konkretny co do TEGO, CO ZROBIŁ
KLIENT, ale nie może zdradzać, jak zbudowana jest baza czy aplikacja.
Szczegóły techniczne idą do logu — tam są potrzebne i tam są bezpieczne.
"""

from __future__ import annotations

import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# Polskie odpowiedniki standardowych komunikatów HTTP. Używane wtedy, gdy
# nikt nie podał własnej treści błędu (np. 404 wygenerowane przez router).
DEFAULT_MESSAGES: dict[int, str] = {
    404: "Nie znaleziono zasobu pod wskazanym adresem.",
    405: "Ta metoda HTTP nie jest obsługiwana pod tym adresem.",
    500: "Wewnętrzny błąd serwera. Szczegóły znajdziesz w logach aplikacji.",
}

# Polskie odpowiedniki najczęstszych błędów walidacji zgłaszanych przez Pydantic.
VALIDATION_MESSAGES: dict[str, str] = {
    "missing": "pole jest wymagane",
    "string_type": "wartość musi być tekstem",
    "int_type": "wartość musi być liczbą całkowitą",
    "json_invalid": "treść żądania nie jest poprawnym dokumentem JSON",
    "model_attributes_type": "treść żądania musi być obiektem JSON",
}

GENERIC_SERVER_ERROR = DEFAULT_MESSAGES[500]


def register_error_handlers(application: FastAPI) -> None:
    """Podpina wszystkie procedury obsługi błędów do aplikacji."""
    application.add_exception_handler(RequestValidationError, handle_validation_error)
    application.add_exception_handler(StarletteHTTPException, handle_http_exception)
    application.add_exception_handler(Exception, handle_unexpected_error)


async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    """Zamienia błąd walidacji treści żądania na odpowiedź 400.

    Domyślnie FastAPI odpowiedziałby kodem 422 i rozbudowaną strukturą
    techniczną. Kontrakt tego API mówi jednak: błędne dane to 400
    i jedno zdanie po polsku.
    """
    assert isinstance(exc, RequestValidationError)
    logger.info("Odrzucono żądanie %s %s — błąd walidacji", request.method, request.url.path)
    return JSONResponse(status_code=400, content={"detail": _describe_validation(exc)})


def _describe_validation(exc: RequestValidationError) -> str:
    """Buduje jedno czytelne zdanie z listy błędów walidacji."""
    problems: list[str] = []
    for error in exc.errors():
        field = _field_name(error.get("loc", ()))
        reason = VALIDATION_MESSAGES.get(str(error.get("type", "")), "wartość jest niepoprawna")
        problems.append(f"{field}: {reason}")

    if not problems:
        return "Treść żądania jest niepoprawna."
    return "Niepoprawna treść żądania — " + "; ".join(problems) + "."


def _field_name(location: tuple[object, ...] | list[object]) -> str:
    """Zamienia ścieżkę błędu Pydantica na nazwę pola zrozumiałą dla człowieka."""
    parts = [str(part) for part in location if part != "body"]
    return f"pole '{'.'.join(parts)}'" if parts else "treść żądania"


async def handle_http_exception(request: Request, exc: Exception) -> JSONResponse:
    """Ujednolica odpowiedzi błędów HTTP i tłumaczy komunikaty domyślne.

    Gdy kod aplikacji podał własną treść (np. „Kod 'abc' jest już zajęty”),
    zostaje ona bez zmian. Gdy treści nie podano, FastAPI wstawia angielską
    frazę standardową („Not Found”) — wtedy podmieniamy ją na polską.
    """
    assert isinstance(exc, StarletteHTTPException)
    detail = exc.detail if isinstance(exc.detail, str) else None
    if not detail or detail == _standard_phrase(exc.status_code):
        detail = DEFAULT_MESSAGES.get(exc.status_code, "Żądanie nie mogło zostać zrealizowane.")

    if exc.status_code >= 500:
        logger.error(
            "Błąd serwera %s przy %s %s", exc.status_code, request.method, request.url.path
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail},
        headers=getattr(exc, "headers", None),
    )


def _standard_phrase(status_code: int) -> str | None:
    """Zwraca angielską frazę standardową dla kodu HTTP (np. 404 → 'Not Found')."""
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return None


async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    """Ostatnia linia obrony: cokolwiek niespodziewanego → 500 i pełny wpis w logu.

    Do klienta idzie zdanie ogólne. Pełny ślad stosu (razem z komunikatem
    bazy danych) trafia do logu — komunikaty błędów bazy potrafią zdradzać
    nazwy tabel i kolumn, a to informacja dla administratora, nie dla świata.
    """
    logger.exception(
        "Nieobsłużony błąd podczas przetwarzania %s %s: %s",
        request.method,
        request.url.path,
        type(exc).__name__,
    )
    return JSONResponse(status_code=500, content={"detail": GENERIC_SERVER_ERROR})
