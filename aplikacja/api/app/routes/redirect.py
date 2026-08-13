"""Przekierowanie `/r/{code}` — właściwe działanie skracacza linków.

To jedyny endpoint, z którego korzysta zwykły człowiek w przeglądarce;
reszta API służy do zarządzania linkami.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Connection
from starlette.responses import RedirectResponse

from app.dependencies import get_connection, get_metrics
from app.metrics import MetricsRegistry
from app.repository import register_click
from app.schemas import ErrorOut

logger = logging.getLogger(__name__)

router = APIRouter(tags=["redirect"])


@router.get(
    "/r/{code}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
    summary="Przekierowanie pod adres docelowy",
    responses={
        307: {"description": "Przekierowanie pod zapisany adres"},
        404: {"model": ErrorOut, "description": "Nie ma linku o takim kodzie"},
    },
)
def follow_link(
    code: str,
    connection: Connection = Depends(get_connection),
    registry: MetricsRegistry = Depends(get_metrics),
) -> RedirectResponse:
    """Przekierowuje pod zapisany adres i zwiększa licznik kliknięć.

    Kod 307 (a nie 301) jest tu wybrany świadomie:

    * 301 „przeniesiono na stałe” przeglądarka zapamiętuje i przy kolejnym
      wejściu w ogóle nie pyta serwera — licznik kliknięć przestałby rosnąć,
      a zmiana adresu docelowego nie działałaby dla osób, które raz weszły.
    * 307 „przekierowanie tymczasowe” zmusza przeglądarkę do zapytania
      za każdym razem i zachowuje metodę oraz treść oryginalnego żądania.
    """
    target_url = register_click(connection, code)
    if target_url is None:
        raise HTTPException(status_code=404, detail=f"Nie ma linku o kodzie '{code}'.")

    # Zatwierdzamy zwiększenie licznika PRZED odesłaniem odpowiedzi —
    # inaczej zamknięcie połączenia wycofałoby zmianę i kliknięcia
    # nigdy by się nie policzyły.
    connection.commit()
    registry.record_redirect(code)
    logger.info("Przekierowanie %s -> %s", code, target_url)

    return RedirectResponse(url=target_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
