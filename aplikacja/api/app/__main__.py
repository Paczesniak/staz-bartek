"""Uruchamianie aplikacji poleceniem `python -m app`.

Ten wariant czyta APP_HOST i APP_PORT ze zmiennych środowiskowych, więc
adres nasłuchiwania jest częścią konfiguracji, a nie parametrem, który
trzeba pamiętać przy każdym uruchomieniu.

Alternatywa: `uvicorn app.main:app --host 127.0.0.1 --port 8000`. Wtedy
adres podaje się ręcznie, a uvicorn używa własnego formatu logów.
"""

from __future__ import annotations

import uvicorn

from app.config import load_settings
from app.main import app


def main() -> None:
    """Startuje serwer uvicorn z konfiguracją ze zmiennych środowiskowych."""
    settings = load_settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        # `log_config=None` wyłącza własną konfigurację logów uvicorna —
        # dzięki temu WSZYSTKIE logi (aplikacji i serwera) idą przez jeden
        # uchwyt na stdout, w jednym formacie.
        log_config=None,
        access_log=True,
    )


if __name__ == "__main__":
    main()
