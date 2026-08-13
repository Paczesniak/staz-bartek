"""${message}

Identyfikator migracji: ${up_revision}
Poprzednia migracja: ${down_revision | comma,n}
Data utworzenia: ${create_date}
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """Zmiany wprowadzane przez tę migrację."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Wycofanie zmian z funkcji upgrade()."""
    ${downgrades if downgrades else "pass"}
