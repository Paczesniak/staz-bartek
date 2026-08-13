"""Testy operacji na linkach: tworzenie, odczyt, usuwanie, przekierowanie."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def test_creates_link_with_generated_code(client: TestClient, sample_url: str) -> None:
    """POST bez własnego kodu tworzy link i losuje dla niego kod."""
    response = client.post("/api/links", json={"url": sample_url})

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"code", "url", "clicks", "created_at"}
    assert body["url"] == sample_url
    assert body["clicks"] == 0
    assert len(body["code"]) >= 3


def test_creates_link_with_custom_code(client: TestClient, sample_url: str) -> None:
    """POST z własnym kodem zapisuje dokładnie ten kod."""
    response = client.post("/api/links", json={"url": sample_url, "code": "moj-kod_1"})

    assert response.status_code == 201
    assert response.json()["code"] == "moj-kod_1"


def test_rejects_duplicate_code_with_conflict(client: TestClient, sample_url: str) -> None:
    """Drugie użycie tego samego kodu kończy się kodem 409 i komunikatem po polsku."""
    client.post("/api/links", json={"url": sample_url, "code": "zajety"})

    response = client.post("/api/links", json={"url": "https://inny.example.com", "code": "zajety"})

    assert response.status_code == 409
    assert "zajęty" in response.json()["detail"]


@pytest.mark.parametrize(
    "bad_url",
    [
        "ftp://example.com/plik.txt",  # niedozwolony schemat
        "javascript:alert(1)",  # próba wstrzyknięcia skryptu
        "example.com",  # brak schematu
        "https://",  # brak hosta
        "",  # pusta wartość
    ],
)
def test_rejects_invalid_url(client: TestClient, bad_url: str) -> None:
    """Adres spoza http/https jest odrzucany kodem 400."""
    response = client.post("/api/links", json={"url": bad_url})

    assert response.status_code == 400
    assert isinstance(response.json()["detail"], str)


def test_rejects_invalid_custom_code(client: TestClient, sample_url: str) -> None:
    """Kod ze znakami spoza dozwolonego zbioru jest odrzucany kodem 400."""
    response = client.post("/api/links", json={"url": sample_url, "code": "zły/kod"})

    assert response.status_code == 400


def test_rejects_missing_url_field(client: TestClient) -> None:
    """Brak pola 'url' to również błąd 400, a nie techniczne 422."""
    response = client.post("/api/links", json={})

    assert response.status_code == 400
    assert "url" in response.json()["detail"]


def test_lists_created_links(client: TestClient, sample_url: str) -> None:
    """GET /api/links zwraca listę wszystkich zapisanych linków."""
    client.post("/api/links", json={"url": sample_url, "code": "pierwszy"})
    client.post("/api/links", json={"url": sample_url, "code": "drugi"})

    response = client.get("/api/links")

    assert response.status_code == 200
    codes = [link["code"] for link in response.json()]
    assert set(codes) == {"pierwszy", "drugi"}


def test_reads_single_link(client: TestClient, sample_url: str) -> None:
    """GET /api/links/{code} zwraca szczegóły jednego linku."""
    client.post("/api/links", json={"url": sample_url, "code": "jeden"})

    response = client.get("/api/links/jeden")

    assert response.status_code == 200
    assert response.json()["url"] == sample_url


def test_returns_404_for_unknown_code(client: TestClient) -> None:
    """Nieznany kod to 404 z komunikatem po polsku."""
    response = client.get("/api/links/nie-ma-takiego")

    assert response.status_code == 404
    assert "Nie ma linku" in response.json()["detail"]


def test_redirect_returns_307_to_target(client: TestClient, sample_url: str) -> None:
    """GET /r/{code} przekierowuje pod adres docelowy kodem 307."""
    client.post("/api/links", json={"url": sample_url, "code": "przekieruj"})

    response = client.get("/r/przekieruj", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == sample_url


def test_redirect_increments_click_counter(client: TestClient, sample_url: str) -> None:
    """Każde przekierowanie zwiększa licznik kliknięć zapisany w bazie."""
    client.post("/api/links", json={"url": sample_url, "code": "licznik"})

    for _ in range(3):
        client.get("/r/licznik", follow_redirects=False)

    assert client.get("/api/links/licznik").json()["clicks"] == 3


def test_reading_link_does_not_increment_clicks(client: TestClient, sample_url: str) -> None:
    """Podgląd linku przez API nie jest kliknięciem i nie zmienia licznika."""
    client.post("/api/links", json={"url": sample_url, "code": "podglad"})

    client.get("/api/links/podglad")

    assert client.get("/api/links/podglad").json()["clicks"] == 0


def test_redirect_returns_404_for_unknown_code(client: TestClient) -> None:
    """Przekierowanie na nieistniejący kod to 404, a nie pusta odpowiedź."""
    response = client.get("/r/nie-ma-takiego", follow_redirects=False)

    assert response.status_code == 404
    assert "Nie ma linku" in response.json()["detail"]


def test_deletes_link(client: TestClient, sample_url: str) -> None:
    """DELETE usuwa link i zwraca 204 bez treści; kolejny odczyt daje 404."""
    client.post("/api/links", json={"url": sample_url, "code": "do-usuniecia"})

    response = client.delete("/api/links/do-usuniecia")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/api/links/do-usuniecia").status_code == 404


def test_delete_unknown_code_returns_404(client: TestClient) -> None:
    """Usunięcie nieistniejącego linku to 404."""
    response = client.delete("/api/links/nie-ma-takiego")

    assert response.status_code == 404
