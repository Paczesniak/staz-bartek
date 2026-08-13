"""linkbox — skracacz linków.

Aplikacja bazowa programu stażowego DevOps. Świadomie prosta w warstwie
biznesowej (kilka endpointów REST i przekierowanie), za to kompletna
w warstwie operacyjnej: konfiguracja ze zmiennych środowiskowych,
migracje bazy, `/health`, `/metrics`, logi na stdout i reakcja na SIGTERM.

Nazwy w kodzie są po angielsku (konwencja), komentarze i komunikaty
dla użytkownika — po polsku.
"""

__version__ = "1.0.0"
