"""Endpointy techniczne: `/health` i `/metrics`.

Nie należą do funkcjonalności skracacza linków — służą temu, co aplikację
uruchamia i pilnuje. `/health` odpowiada na pytanie „czy działa?”,
`/metrics` na pytanie „jak działa i ile tego zrobiła?”.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse, PlainTextResponse, Response

from app import __version__
from app.db import check_database
from app.dependencies import get_engine, get_metrics
from app.metrics import CONTENT_TYPE, MetricsRegistry
from app.repository import count_links
from app.schemas import HealthOut

logger = logging.getLogger(__name__)

router = APIRouter(tags=["system"])


@router.get(
    "/health",
    response_model=HealthOut,
    summary="Stan aplikacji",
    responses={
        200: {"description": "Aplikacja działa i widzi bazę danych"},
        503: {"model": HealthOut, "description": "Baza danych nie odpowiada"},
    },
)
def read_health(engine: Engine = Depends(get_engine)) -> Response:
    """Sprawdza, czy aplikacja odpowiada i czy widzi bazę danych.

    Zwraca 200 tylko wtedy, gdy baza faktycznie odpowiedziała na zapytanie
    kontrolne. Endpoint, który zwraca 200 zawsze, jest bezużyteczny —
    potwierdza jedynie, że proces żyje, a to widać też po tym, że w ogóle
    coś odpowiedziało.
    """
    database_ok = check_database(engine)
    payload = {
        "status": "ok" if database_ok else "error",
        "database": "ok" if database_ok else "error",
        "version": __version__,
    }
    return JSONResponse(status_code=200 if database_ok else 503, content=payload)


@router.get(
    "/metrics",
    summary="Metryki w formacie Prometheusa",
    response_class=PlainTextResponse,
    responses={200: {"content": {"text/plain": {}}, "description": "Metryki aplikacji"}},
)
def read_metrics(
    engine: Engine = Depends(get_engine),
    registry: MetricsRegistry = Depends(get_metrics),
) -> Response:
    """Zwraca metryki aplikacji jako zwykły tekst.

    Prometheus odpytuje ten adres cyklicznie (domyślnie co kilkanaście
    sekund) i zapisuje u siebie kolejne odczyty. Aplikacja niczego nie
    wysyła sama — to Prometheus przychodzi po dane.
    """
    links_total, database_up = _read_database_gauges(engine)
    body = registry.render(links_total=links_total, database_up=database_up)
    return PlainTextResponse(content=body, media_type=CONTENT_TYPE)


def _read_database_gauges(engine: Engine) -> tuple[int | None, bool]:
    """Pobiera z bazy wartości metryk `linkbox_links_total` i `linkbox_up`.

    Gdy baza nie odpowiada, endpoint metryk MUSI mimo to zwrócić odpowiedź —
    inaczej monitoring straciłby jedyną informację, która jest wtedy
    najważniejsza: `linkbox_up 0`.
    """
    try:
        with engine.connect() as connection:
            return count_links(connection), True
    except SQLAlchemyError:
        logger.error("Nie udało się odczytać metryk z bazy danych", exc_info=True)
        return None, False
