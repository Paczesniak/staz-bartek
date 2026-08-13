"""Dostęp do danych — wszystkie zapytania do bazy w jednym miejscu.

SQLAlchemy Core, czyli budowanie zapytań bliskie SQL-owi. Odpowiednik SQL
każdej funkcji jest podany w jej opisie — to ten sam SQL, który da się wkleić
do konsoli bazy.

Funkcje przyjmują otwarte połączenie (`Connection`) i nie decydują
o transakcji. Transakcją steruje warstwa wyżej (zależność `get_connection`),
dzięki czemu jedno żądanie HTTP to jedna transakcja.
"""

from __future__ import annotations

from typing import Any

import sqlalchemy as sa
from sqlalchemy.engine import Connection, Row

from app.models import as_utc, links, utc_now


def _row_to_link(row: Row[Any]) -> dict[str, Any]:
    """Zamienia wiersz z bazy na słownik zgodny z kontraktem API.

    Kolumna `id` celowo nie trafia do odpowiedzi — jest szczegółem
    implementacyjnym bazy, a nie częścią publicznego API.
    """
    return {
        "code": row.code,
        "url": row.url,
        "clicks": row.clicks,
        "created_at": as_utc(row.created_at),
    }


def list_links(connection: Connection) -> list[dict[str, Any]]:
    """Zwraca wszystkie linki, od najnowszego.

    SQL: SELECT code, url, clicks, created_at FROM links ORDER BY id DESC
    """
    statement = sa.select(links.c.code, links.c.url, links.c.clicks, links.c.created_at).order_by(
        links.c.id.desc()
    )
    return [_row_to_link(row) for row in connection.execute(statement)]


def get_link(connection: Connection, code: str) -> dict[str, Any] | None:
    """Zwraca jeden link albo None, gdy kodu nie ma w bazie.

    SQL: SELECT code, url, clicks, created_at FROM links WHERE code = :code
    """
    statement = sa.select(links.c.code, links.c.url, links.c.clicks, links.c.created_at).where(
        links.c.code == code
    )
    row = connection.execute(statement).first()
    return _row_to_link(row) if row is not None else None


def insert_link(connection: Connection, code: str, url: str) -> dict[str, Any]:
    """Zapisuje nowy link i zwraca go w postaci zgodnej z API.

    SQL: INSERT INTO links (code, url, clicks, created_at) VALUES (...)

    Przy zajętym kodzie baza rzuci `IntegrityError` (naruszenie unikalności
    kolumny `code`) — obsługuje to warstwa HTTP, zamieniając go na 409.
    Świadomie polegamy na bazie, a nie na wcześniejszym SELECT-cie: przy dwóch
    instancjach aplikacji sprawdzenie „czy wolne” i zapis to dwie różne chwile,
    a ograniczenie unikalności działa zawsze.
    """
    created_at = utc_now()
    statement = sa.insert(links).values(code=code, url=url, clicks=0, created_at=created_at)
    connection.execute(statement)
    return {"code": code, "url": url, "clicks": 0, "created_at": created_at}


def delete_link(connection: Connection, code: str) -> bool:
    """Usuwa link. Zwraca True, gdy faktycznie coś usunięto.

    SQL: DELETE FROM links WHERE code = :code
    """
    result = connection.execute(sa.delete(links).where(links.c.code == code))
    return result.rowcount > 0


def register_click(connection: Connection, code: str) -> str | None:
    """Zwiększa licznik kliknięć i zwraca adres docelowy (None, gdy brak kodu).

    SQL: SELECT url FROM links WHERE code = :code
         UPDATE links SET clicks = clicks + 1 WHERE code = :code

    Licznik zwiększa BAZA (`clicks = clicks + 1`), a nie Python. Gdyby
    aplikacja odczytała wartość, dodała jedynkę i zapisała z powrotem,
    dwa równoległe kliknięcia — albo dwie instancje aplikacji — zgubiłyby
    część zliczeń.
    """
    target = connection.execute(
        sa.select(links.c.url).where(links.c.code == code)
    ).scalar_one_or_none()
    if target is None:
        return None

    connection.execute(
        sa.update(links).where(links.c.code == code).values(clicks=links.c.clicks + 1)
    )
    return target


def count_links(connection: Connection) -> int:
    """Zwraca liczbę linków w bazie — źródło metryki `linkbox_links_total`.

    SQL: SELECT count(*) FROM links
    """
    return connection.execute(sa.select(sa.func.count()).select_from(links)).scalar_one()
