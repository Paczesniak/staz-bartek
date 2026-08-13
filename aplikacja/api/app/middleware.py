"""Middleware zbierające metryki każdego żądania HTTP.

Middleware to warstwa, przez którą przechodzi KAŻDE żądanie — również te
zakończone błędem i te, które nie trafiły w żadną trasę. Dlatego to tutaj,
a nie w poszczególnych trasach, liczymy żądania i mierzymy czas odpowiedzi.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

# Etykieta dla żądań, które nie trafiły w żadną trasę (np. skanery szukające
# `/wp-admin`). Gdyby trafiał tu prawdziwy adres, każde takie żądanie
# tworzyłoby nową serię czasową w Prometheusie.
UNMATCHED_PATH = "<unmatched>"

CallNext = Callable[[Request], Awaitable[Response]]


def register_metrics_middleware(application: FastAPI) -> None:
    """Podpina middleware zliczające żądania do aplikacji."""

    @application.middleware("http")
    async def collect_request_metrics(request: Request, call_next: CallNext) -> Response:
        started_at = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            # Nieobsłużony wyjątek to dla klienta odpowiedź 500 — i tak musi
            # być policzony. Wyjątek podajemy dalej, żeby zajęła się nim
            # warstwa obsługi błędów; nie połykamy go tutaj.
            _record(request, status_code=500, started_at=started_at)
            raise
        _record(request, status_code=response.status_code, started_at=started_at)
        return response


def _record(request: Request, status_code: int, started_at: float) -> None:
    """Zapisuje w rejestrze metryk jedno obsłużone żądanie."""
    duration = time.perf_counter() - started_at
    registry = request.app.state.metrics
    registry.record_request(
        method=request.method,
        path=resolve_route_template(request),
        status=status_code,
        duration=duration,
    )


def resolve_route_template(request: Request) -> str:
    """Zwraca WZORZEC trasy, w którą trafiło żądanie (np. `/api/links/{code}`).

    Dlaczego nie zwykły `request.url.path`? Bo w metryce Prometheusa każda
    inna wartość etykiety to osobna seria czasowa. Adres `/r/abc123` z
    prawdziwym kodem oznaczałby tyle serii, ile linków w bazie — i po kilku
    dniach Prometheus miałby ich dziesiątki tysięcy zamiast kilkunastu.

    Wzorzec bierzemy z informacji, którą router zostawia w opisie żądania
    (`scope`) po dopasowaniu trasy. Gdy żaden wzorzec nie pasował, klucza
    tam nie ma i zwracamy jedną wspólną etykietę zamiast prawdziwego adresu.
    """
    route = request.scope.get("route")
    template = getattr(route, "path_format", None) or getattr(route, "path", None)
    if isinstance(template, str) and template:
        return template

    # Trasy wbudowane w FastAPI (`/docs`, `/openapi.json`) nie zostawiają wpisu
    # `route`, ale zostawiają `endpoint` — czyli funkcję, która je obsłużyła.
    # Skoro do tego doszło i adres nie zawiera żadnego parametru
    # (`path_params` jest puste), to sam adres JEST wzorcem trasy.
    if request.scope.get("endpoint") is not None and not request.scope.get("path_params"):
        return request.url.path

    return UNMATCHED_PATH
