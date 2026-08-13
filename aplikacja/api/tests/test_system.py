"""Testy warstwy technicznej: /health, /metrics, CORS i format błędów."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app import __version__
from app.db import create_db_engine

CORS_HEADER = "access-control-allow-origin"


def test_health_reports_ok(client: TestClient) -> None:
    """Przy działającej bazie /health zwraca 200 i komplet informacji."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok", "version": __version__}


def test_health_reports_503_when_database_is_down(client: TestClient, tmp_path: Path) -> None:
    """Gdy baza nie odpowiada, /health zwraca 503 — a nie 200 z kłamstwem."""
    unreachable = tmp_path / "nieistniejacy-katalog" / "links.db"
    client.app.state.engine = create_db_engine(f"sqlite:///{unreachable}")

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["status"] == "error"
    assert response.json()["database"] == "error"


def test_metrics_expose_required_series(client: TestClient, sample_url: str) -> None:
    """Endpoint /metrics zawiera wszystkie metryki wymagane przez monitoring."""
    client.post("/api/links", json={"url": sample_url, "code": "metryki"})

    body = client.get("/metrics").text

    for metric in (
        "linkbox_links_total",
        "linkbox_redirects_total",
        "linkbox_http_requests_total",
        "linkbox_request_duration_seconds",
        "linkbox_up",
    ):
        assert f"# HELP {metric}" in body, f"brak opisu HELP dla {metric}"
        assert f"# TYPE {metric}" in body, f"brak typu TYPE dla {metric}"


def test_metrics_use_prometheus_content_type(client: TestClient) -> None:
    """Prometheus oczekuje zwykłego tekstu, nie JSON-a."""
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")


def test_metrics_count_links_from_database(client: TestClient, sample_url: str) -> None:
    """Metryka linkbox_links_total pokazuje faktyczną liczbę linków w bazie."""
    client.post("/api/links", json={"url": sample_url, "code": "jeden"})
    client.post("/api/links", json={"url": sample_url, "code": "dwa"})

    body = client.get("/metrics").text

    assert 'linkbox_links_total{app="linkbox"} 2' in body


def test_redirect_counter_grows(client: TestClient, sample_url: str) -> None:
    """Licznik przekierowań rośnie z każdym wejściem pod /r/{code}."""
    client.post("/api/links", json={"url": sample_url, "code": "klikany"})
    client.get("/r/klikany", follow_redirects=False)
    client.get("/r/klikany", follow_redirects=False)

    body = client.get("/metrics").text

    assert 'linkbox_redirects_total{app="linkbox",code="klikany"} 2' in body


def test_metrics_use_route_template_not_raw_path(client: TestClient, sample_url: str) -> None:
    """Etykieta path to wzorzec trasy — inaczej liczba serii rosłaby bez końca."""
    client.post("/api/links", json={"url": sample_url, "code": "wzorzec"})
    client.get("/api/links/wzorzec")

    body = client.get("/metrics").text

    assert 'path="/api/links/{code}"' in body
    assert 'path="/api/links/wzorzec"' not in body


def test_metrics_label_unmatched_paths_with_one_shared_value(client: TestClient) -> None:
    """Adresy spoza aplikacji (np. skanery) trafiają pod jedną wspólną etykietę."""
    client.get("/wp-admin/setup-config.php")
    client.get("/.env")

    body = client.get("/metrics").text

    assert 'path="<unmatched>",status="404"} 2' in body
    assert "wp-admin" not in body


def test_metrics_histogram_is_cumulative(client: TestClient) -> None:
    """Ostatni kubełek histogramu musi równać się liczbie wszystkich próbek."""
    client.get("/health")

    lines = client.get("/metrics").text.splitlines()
    infinite_bucket = _metric_value(lines, "linkbox_request_duration_seconds_bucket", 'le="+Inf"')
    total_count = _metric_value(lines, "linkbox_request_duration_seconds_count", "")

    assert infinite_bucket == total_count
    assert total_count > 0


def _metric_value(lines: list[str], metric_name: str, label_fragment: str) -> float:
    """Wyciąga wartość jednej próbki z tekstowej odpowiedzi /metrics."""
    for line in lines:
        if line.startswith(metric_name) and label_fragment in line:
            return float(line.rsplit(" ", 1)[1])
    raise AssertionError(f"Nie znaleziono metryki {metric_name} z etykietą {label_fragment!r}")


def test_no_cors_header_when_origins_are_empty(client: TestClient) -> None:
    """Domyślnie CORS jest wyłączony — odpowiedź nie ma nagłówka Access-Control-Allow-Origin."""
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})

    assert CORS_HEADER not in {name.lower() for name in response.headers}


def test_cors_header_present_when_origin_configured(make_client) -> None:
    """Po ustawieniu CORS_ORIGINS ten sam adres dostaje nagłówek CORS."""
    client = make_client(CORS_ORIGINS="http://localhost:3000")

    response = client.get("/health", headers={"Origin": "http://localhost:3000"})

    assert response.headers[CORS_HEADER] == "http://localhost:3000"


def test_cors_header_absent_for_unknown_origin(make_client) -> None:
    """Origin spoza listy nie dostaje nagłówka — lista to lista, nie sugestia."""
    client = make_client(CORS_ORIGINS="http://localhost:3000")

    response = client.get("/health", headers={"Origin": "http://zlosliwy.example.com"})

    assert CORS_HEADER not in {name.lower() for name in response.headers}


def test_cors_accepts_multiple_origins(make_client) -> None:
    """CORS_ORIGINS przyjmuje listę origin-ów rozdzieloną przecinkami."""
    client = make_client(CORS_ORIGINS="http://localhost:3000, http://localhost:5173")

    response = client.get("/health", headers={"Origin": "http://localhost:5173"})

    assert response.headers[CORS_HEADER] == "http://localhost:5173"


def test_unknown_path_returns_polish_error(client: TestClient) -> None:
    """Nieznany adres zwraca 404 w tym samym formacie co pozostałe błędy."""
    response = client.get("/nie-ma-takiego-adresu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Nie znaleziono zasobu pod wskazanym adresem."}


def test_wrong_method_returns_polish_error(client: TestClient) -> None:
    """Niewłaściwa metoda HTTP też zwraca komunikat po polsku."""
    response = client.put("/api/links")

    assert response.status_code == 405
    assert "metoda" in response.json()["detail"].lower()


def test_openapi_documentation_is_available(client: TestClient) -> None:
    """Dokumentacja pod /docs musi działać — to pierwszy dowód, że API żyje."""
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
