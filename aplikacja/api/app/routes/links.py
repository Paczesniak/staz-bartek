"""Operacje na linkach — REST pod `/api/links`.

Konwencja REST użyta tutaj: adres wskazuje ZASÓB (`/api/links/{code}`),
a metoda HTTP mówi, co z nim zrobić (GET czytaj, POST utwórz, DELETE usuń).
Kod odpowiedzi też niesie informację: 201 to „utworzono”, 204 „zrobione,
nie mam nic do powiedzenia”, 409 „konflikt z tym, co już istnieje”.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response

from app.dependencies import get_connection
from app.repository import delete_link, get_link, insert_link, list_links
from app.schemas import ErrorOut, LinkCreate, LinkOut
from app.validation import ValidationError, generate_code, validate_code, validate_url

logger = logging.getLogger(__name__)

# Ile razy losujemy kod, zanim uznamy, że coś jest nie tak. Przy siedmioznakowym
# kodzie z 56-znakowego alfabetu kolizja jest bardzo mało prawdopodobna,
# ale „mało prawdopodobne” to nie to samo co „niemożliwe”.
MAX_CODE_ATTEMPTS = 5

router = APIRouter(prefix="/api/links", tags=["links"])

NOT_FOUND_RESPONSE = {404: {"model": ErrorOut, "description": "Nie ma linku o takim kodzie"}}


@router.get("", response_model=list[LinkOut], summary="Lista wszystkich linków")
def read_links(connection: Connection = Depends(get_connection)) -> list[dict[str, object]]:
    """Zwraca wszystkie linki, od najnowszego."""
    return list_links(connection)


@router.get(
    "/{code}",
    response_model=LinkOut,
    summary="Szczegóły jednego linku",
    responses=NOT_FOUND_RESPONSE,
)
def read_link(code: str, connection: Connection = Depends(get_connection)) -> dict[str, object]:
    """Zwraca jeden link po jego kodzie. Nie zwiększa licznika kliknięć."""
    link = get_link(connection, code)
    if link is None:
        raise HTTPException(status_code=404, detail=_not_found_message(code))
    return link


@router.post(
    "",
    response_model=LinkOut,
    status_code=status.HTTP_201_CREATED,
    summary="Utworzenie nowego linku",
    responses={
        400: {"model": ErrorOut, "description": "Niepoprawny adres URL lub kod"},
        409: {"model": ErrorOut, "description": "Podany kod jest już zajęty"},
    },
)
def create_link(
    payload: LinkCreate, connection: Connection = Depends(get_connection)
) -> dict[str, object]:
    """Tworzy nowy skrócony link.

    Gdy pole `code` jest puste, serwer losuje kod. Gdy podano własny kod,
    a jest już zajęty — odpowiedź 409, bo dwa różne adresy nie mogą siedzieć
    pod jednym kodem.
    """
    try:
        url = validate_url(payload.url)
        custom_code = validate_code(payload.code) if payload.code is not None else None
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if custom_code is None:
        return _create_with_generated_code(connection, url)
    return _create_with_custom_code(connection, custom_code, url)


def _create_with_custom_code(connection: Connection, code: str, url: str) -> dict[str, object]:
    """Zapisuje link z kodem podanym przez użytkownika."""
    try:
        link = insert_link(connection, code, url)
        connection.commit()
    except IntegrityError as exc:
        # Wycofujemy nieudaną transakcję, zanim odpowiemy — bez tego
        # połączenie wróciłoby do puli w stanie „transakcja przerwana”.
        connection.rollback()
        logger.info("Odrzucono próbę zajęcia kodu %r — kod jest już w bazie", code)
        raise HTTPException(
            status_code=409,
            detail=f"Kod '{code}' jest już zajęty. Wybierz inny albo pomiń pole 'code'.",
        ) from exc

    logger.info("Utworzono link %s -> %s (kod własny)", code, url)
    return link


def _create_with_generated_code(connection: Connection, url: str) -> dict[str, object]:
    """Zapisuje link, losując wolny kod.

    Nie sprawdzamy najpierw, czy kod jest wolny — przy dwóch instancjach
    aplikacji między sprawdzeniem a zapisem i tak mogłaby wcisnąć się druga
    instancja. Zamiast tego próbujemy zapisać i reagujemy na odmowę bazy.
    """
    for attempt in range(1, MAX_CODE_ATTEMPTS + 1):
        code = generate_code()
        try:
            link = insert_link(connection, code, url)
            connection.commit()
        except IntegrityError:
            connection.rollback()
            logger.warning(
                "Wylosowany kod %r jest już zajęty — losuję ponownie (próba %d z %d)",
                code,
                attempt,
                MAX_CODE_ATTEMPTS,
            )
            continue

        logger.info("Utworzono link %s -> %s (kod wylosowany)", code, url)
        return link

    logger.error("Nie udało się wylosować wolnego kodu w %d próbach", MAX_CODE_ATTEMPTS)
    raise HTTPException(
        status_code=500,
        detail="Nie udało się wygenerować wolnego kodu. Spróbuj ponownie lub podaj własny kod.",
    )


@router.delete(
    "/{code}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Usunięcie linku",
    responses=NOT_FOUND_RESPONSE,
)
def remove_link(code: str, connection: Connection = Depends(get_connection)) -> Response:
    """Usuwa link. Odpowiedź 204 nie ma treści — nie ma już czego zwracać."""
    if not delete_link(connection, code):
        raise HTTPException(status_code=404, detail=_not_found_message(code))

    connection.commit()
    logger.info("Usunięto link o kodzie %s", code)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _not_found_message(code: str) -> str:
    """Jeden komunikat 404 dla wszystkich operacji na pojedynczym linku."""
    return f"Nie ma linku o kodzie '{code}'."
