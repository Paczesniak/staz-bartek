"""Definicja schematu bazy danych — SQLAlchemy Core (bez ORM).

Świadomie NIE używamy ORM-a. Tabela jest opisana wprost, a zapytania
w `repository.py` są bliskie SQL-owi, który dałoby się wkleić do konsoli
bazy. Dzięki temu widać, co naprawdę leci do bazy.

Wszystkie typy są przenośne: te same definicje działają na SQLite
i na PostgreSQL bez zmiany jednej linijki kodu — zmienia się wyłącznie
zmienna środowiskowa DATABASE_URL.
"""

from __future__ import annotations

from datetime import UTC, datetime

import sqlalchemy as sa

# MetaData to katalog wszystkich tabel aplikacji. Alembic używa go jako
# wzorca („tak ma wyglądać baza”) przy generowaniu migracji.
metadata = sa.MetaData()

# Ograniczenia długości — trzymane jako stałe, bo te same wartości
# sprawdza walidacja wejścia w `validation.py`.
CODE_MAX_LENGTH = 64
CODE_MIN_LENGTH = 3
URL_MAX_LENGTH = 2048

links = sa.Table(
    "links",
    metadata,
    # Klucz główny techniczny. Integer + primary_key SQLAlchemy tłumaczy
    # na autoinkrementację właściwą dla danej bazy (INTEGER PRIMARY KEY
    # w SQLite, SERIAL/IDENTITY w PostgreSQL) — dlatego nie ma tu nic,
    # co byłoby przywiązane do jednego silnika.
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    # Krótki kod widoczny w adresie /r/{code}. Unikalny — to on decyduje
    # o konflikcie 409 przy próbie zajęcia zajętego kodu. Warunek unikalności
    # pilnuje BAZA, a nie aplikacja; przy dwóch instancjach aplikacji tylko
    # baza wie na pewno, czy kod jest jeszcze wolny.
    # Przy okazji powstaje indeks, z którego korzysta wyszukiwanie po kodzie.
    sa.Column("code", sa.String(CODE_MAX_LENGTH), nullable=False, unique=True),
    # Adres docelowy przekierowania.
    sa.Column("url", sa.String(URL_MAX_LENGTH), nullable=False),
    # Licznik kliknięć. Inkrementowany zapytaniem UPDATE ... SET clicks = clicks + 1,
    # czyli po stronie bazy — dzięki temu dwie instancje aplikacji nie gubią zliczeń.
    sa.Column("clicks", sa.Integer, nullable=False, server_default=sa.text("0")),
    # Znacznik czasu zapisywany zawsze w UTC. Wartość wyliczamy w Pythonie,
    # a nie funkcją bazodanową, bo `now()` w każdej bazie nazywa się inaczej.
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)


def utc_now() -> datetime:
    """Zwraca aktualny czas w UTC, ze świadomą strefą czasową.

    Czas zapisujemy zawsze w UTC. Strefę użytkownika ma sobie doliczyć
    warstwa prezentacji — serwer nie zgaduje, gdzie siedzi klient.
    """
    return datetime.now(UTC)


def as_utc(value: datetime) -> datetime:
    """Dokłada strefę UTC do znacznika czasu odczytanego z bazy.

    SQLite nie przechowuje informacji o strefie i oddaje datę „naiwną”
    (bez tzinfo), PostgreSQL z kolumną `timestamptz` oddaje datę ze strefą.
    Ta funkcja sprowadza oba przypadki do jednej postaci, żeby API zwracało
    identyczny format niezależnie od bazy pod spodem.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
