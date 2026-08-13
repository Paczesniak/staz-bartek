"""Migracja początkowa — tworzy tabelę links.

Identyfikator migracji: 0001
Poprzednia migracja: brak (to pierwsza migracja)

Migracja składa się z dwóch funkcji:

* `upgrade()`   — co zrobić, żeby przejść do tej wersji struktury bazy,
* `downgrade()` — jak się z niej wycofać.

Obie muszą do siebie pasować. Migracja bez działającego `downgrade()`
to migracja, z której nie ma odwrotu — a odwrót bywa potrzebny o 2 w nocy.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Tworzy tabelę `links` przechowującą skrócone adresy.

    Definicja jest przenośna — te same typy SQLAlchemy tłumaczy na typy
    właściwe dla konkretnej bazy, więc migracja zadziała zarówno na SQLite,
    jak i na PostgreSQL.
    """
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("clicks", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_links"),
        # Warunek unikalności kodu. To on odpowiada za odpowiedź 409
        # przy próbie zajęcia zajętego kodu — pilnuje tego baza, nie aplikacja.
        sa.UniqueConstraint("code", name="uq_links_code"),
    )


def downgrade() -> None:
    """Usuwa tabelę `links` wraz z całą jej zawartością."""
    op.drop_table("links")
