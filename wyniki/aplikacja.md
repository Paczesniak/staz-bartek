# Raport dnia aplikacja — 2026-08-18 09:52:52

| Moduł | Zaliczony | Zadania | Warunki | Udane | Nieudane | Pierwsze podejście | Czas realizacji |
|---|---|---|---|---|---|---|---|
| uruchom | TAK | 3/3 | 10/10 | 1 | 3 | 2026-08-13T13:09:39+0000 | 91godz. 47min. |
| konfiguracja | TAK | 2/2 | 8/8 | 1 | 2 | 2026-08-17T09:12:25+0000 | 2godz. 0min. |
| cors | TAK | 2/2 | 6/6 | 1 | 13 | 2026-08-17T11:12:35+0000 | — |
| usluga | TAK | 3/3 | 16/16 | 1 | 3 | 2026-08-18T07:16:17+0000 | 19godz. 53min. |
| logi | TAK | 2/2 | 10/10 | 2 | 0 | 2026-08-18T09:42:11+0000 | — |
| zamkniecie | TAK | 1/1 | 4/4 | 1 | 0 | 2026-08-18T09:52:28+0000 | 0godz. 0min. |

„Czas realizacji" to odstęp od pierwszego `lab start <moduł>` do pierwszego kompletnego zaliczenia — nie ostatnie sprawdzenie, które myli, gdy stażysta wraca do już zrobionego modułu.

## Zadania niezaliczone

Brak.

## Często niespełniane warunki

Tylko warunki, które nie przeszły więcej niż raz w tym samym module — pojedyncza awaria to szum, nie sygnał.

### uruchom — 1 udane / 3 nieudane

- ✗ 3× „w tabeli links nie ma żadnego zapisanego linku"

### konfiguracja — 1 udane / 2 nieudane

- ✗ 2× „usługa na porcie 8000 faktycznie działa"
- ✗ 2× „port 8000 nasłuchuje na wszystkich interfejsach, nie tylko na loopbacku"
- ✗ 2× „plik .env ma APP_HOST ustawiony na 0.0.0.0"
- ✗ 2× „endpoint /health nie odpowiada 200 pod adresem innym niż loopback"

### cors — 1 udane / 13 nieudane

- ✗ 13× „plik .env ma CORS_ORIGINS ustawiony na adres frontu"
- ✗ 13× „API nie odsyła poprawnego nagłówka access-control-allow-origin dla origin frontu"
- ✗ 12× „config.js wskazuje API pod adresem IP (http://<IP>:8000)"
- ✗ 11× „config.js nie wskazuje API przez localhost"
- ✗ 4× „kod aplikacji (api/app, web/app.js) ma niezacommitowane zmiany"

### usluga — 1 udane / 3 nieudane

- ✗ 3× „usługa linkbox-staging jest active"
- ✗ 3× „port stagingu nie nasłuchuje"
- ✗ 3× „linkbox-staging nadal ma APP_PORT=8000 — kolizja z portem usługi produkcyjnej"
- ✗ 3× „katalog roboczy stagingu nie istnieje"
- ✗ 3× „ExecStart stagingu wskazuje Pythona ze środowiska wirtualnego (.venv)"
- ✗ 3× „/health usługi stagingowej NIE odpowiada"
- ✗ 2× „usługa linkbox jest włączona do automatycznego startu (enabled)"


## Aktywność

Łączny czas między pierwszym a ostatnim wywołaniem `lab` dnia aplikacja: 117godz. 8min. (2026-08-13T12:44:12+0000 -> 2026-08-18T09:52:28+0000).

## Podsumowanie

6 z 6 modułów z automatycznym sprawdzeniem zaliczonych.
