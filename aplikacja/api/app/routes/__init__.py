"""Trasy (endpointy) HTTP aplikacji, podzielone według przeznaczenia.

* `system`   — `/health` i `/metrics`, czyli to, o co pyta monitoring
* `links`    — `/api/links`, czyli operacje na linkach (REST)
* `redirect` — `/r/{code}`, czyli to, po co ta aplikacja w ogóle istnieje
"""

from app.routes import links, redirect, system

__all__ = ["links", "redirect", "system"]
