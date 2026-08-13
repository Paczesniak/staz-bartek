# linkbox — skracacz linków (API)

Aplikacja bazowa programu stażowego. Zamienia długi adres na krótki kod
i zlicza, ile razy ktoś z tego kodu skorzystał.

```
POST /api/links  {"url": "https://bardzo.dlugi.adres/…"}   →   {"code": "ob7ShX7", …}
GET  /r/ob7ShX7                                             →   przekierowanie pod długi adres
```

Funkcjonalnie to kilkanaście linijek logiki. Cała reszta — konfiguracja ze
zmiennych środowiskowych, migracje bazy, `/health`, `/metrics`, logi, reakcja
na sygnały — jest tu po to, żeby aplikacja dała się utrzymywać w ruchu.
Tym właśnie zajmuje się DevOps.

## Wymagania

- Python 3.11 lub nowszy
- nic więcej — baza domyślna (SQLite) to zwykły plik, nie osobny serwer

Sprawdzenie wersji:

```bash
python3 --version
```

## Uruchomienie

Wszystkie polecenia wykonuje się w katalogu, w którym leży ten plik.

**1. Środowisko wirtualne** — osobny, odizolowany zestaw bibliotek dla tego
projektu. Bez niego biblioteki instalowałyby się globalnie i dwa projekty
wymagające różnych wersji tej samej biblioteki nie mogłyby współistnieć.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Po aktywacji znak zachęty zaczyna się od `(.venv)`. Wyjście: `deactivate`.

**2. Zależności**

```bash
pip install -r requirements.txt
```

**3. Struktura bazy danych** — pusta baza to jeszcze nie działająca baza;
tabele trzeba w niej utworzyć. Robi to migracja:

```bash
alembic upgrade head
```

Powstanie plik `links.db`. Powtórne uruchomienie tego polecenia niczego nie
zepsuje — Alembic pamięta, które migracje już wykonał.

**4. Start aplikacji**

```bash
python -m app
```

W logu na ekranie pojawi się komplet ustawień, z którymi aplikacja wystartowała.
Zatrzymanie: `Ctrl+C`.

**5. Sprawdzenie, że żyje**

```bash
curl http://127.0.0.1:8000/health
```

Powinno odpowiedzieć `{"status":"ok","database":"ok","version":"1.0.0"}`.

W przeglądarce pod adresem <http://127.0.0.1:8000/docs> czeka **Swagger UI** —
interaktywna dokumentacja, w której każdy endpoint da się wywołać przyciskiem
„Try it out”. Warto tam zajrzeć, zanim powstanie jakikolwiek front.

## Konfiguracja

Aplikacja **nie ma pliku konfiguracyjnego**. Wszystko czyta ze zmiennych
środowiskowych — dzięki temu ten sam kod działa w każdym środowisku, a hasła
nigdy nie trafiają do repozytorium.

| Zmienna | Domyślnie | Znaczenie |
|---|---|---|
| `APP_HOST` | `127.0.0.1` | Adres, na którym aplikacja nasłuchuje. `127.0.0.1` oznacza „tylko ta maszyna”. |
| `APP_PORT` | `8000` | Port TCP. Porty poniżej 1024 wymagają uprawnień administratora. |
| `DATABASE_URL` | `sqlite:///./links.db` | Adres bazy danych w formacie SQLAlchemy. |
| `CORS_ORIGINS` | *(puste)* | Lista adresów (origin-ów) rozdzielona przecinkami, którym przeglądarka pozwoli czytać odpowiedzi tego API. Puste = brak nagłówków CORS. |
| `LOG_LEVEL` | `INFO` | `CRITICAL`, `ERROR`, `WARNING`, `INFO` lub `DEBUG`. |
| `APP_NAME` | `linkbox` | Nazwa instancji. Trafia do każdej linii logu i do etykiety w metrykach. |

Opisy z przykładami: [`.env.example`](.env.example).

Przykład uruchomienia z inną konfiguracją:

```bash
APP_PORT=9000 LOG_LEVEL=DEBUG python -m app
```

Zmienna podana przed poleceniem obowiązuje tylko dla tego jednego
uruchomienia. Sprawdzenie, co aplikacja faktycznie zobaczyła: pierwsze linie
jej logu przy starcie.

### Uwaga o CORS

Domyślnie `CORS_ORIGINS` jest **puste**, więc odpowiedzi nie zawierają
nagłówków CORS. Konsekwencja: strona serwowana z innego adresu niż to API
(np. front na porcie 3000) dostanie w przeglądarce błąd o zablokowanym
żądaniu — mimo że `curl` na ten sam adres działa bez zarzutu.

To nie jest usterka. CORS jest regułą **przeglądarki**: serwer nie blokuje
niczego, to przeglądarka odmawia skryptowi dostępu do odpowiedzi, dopóki
serwer nie potwierdzi wprost, że zna dany origin. `curl` przeglądarką nie jest,
więc żadnych reguł nie stosuje.

Origin to **schemat + host + port** — `http://localhost:3000` i
`http://localhost:8000` to dwa różne origin-y, mimo tego samego hosta.

## Endpointy

| Metoda | Adres | Odpowiedź | Opis |
|---|---|---|---|
| `GET` | `/health` | `200` / `503` | Stan aplikacji i połączenia z bazą |
| `GET` | `/metrics` | `200` | Metryki w formacie Prometheusa (zwykły tekst) |
| `GET` | `/api/links` | `200` | Lista wszystkich linków, od najnowszego |
| `POST` | `/api/links` | `201` / `400` / `409` | Utworzenie linku |
| `GET` | `/api/links/{code}` | `200` / `404` | Szczegóły jednego linku |
| `DELETE` | `/api/links/{code}` | `204` / `404` | Usunięcie linku |
| `GET` | `/r/{code}` | `307` / `404` | Przekierowanie pod adres docelowy + zliczenie kliknięcia |

Reprezentacja linku:

```json
{
  "code": "ob7ShX7",
  "url": "https://example.com/bardzo/dluga/sciezka",
  "clicks": 3,
  "created_at": "2026-08-10T14:02:10.407900Z"
}
```

### Przykłady

Utworzenie linku z losowym kodem:

```bash
curl -X POST http://127.0.0.1:8000/api/links \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://docs.python.org/3/"}'
```

Utworzenie linku z własnym kodem (litery, cyfry, `-` i `_`, od 3 do 64 znaków):

```bash
curl -X POST http://127.0.0.1:8000/api/links \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://docs.python.org/3/", "code": "python"}'
```

Przekierowanie. `curl` domyślnie przekierowań nie wykonuje — pokaże samą
odpowiedź z nagłówkiem `Location`. Przełącznik `-i` wypisuje nagłówki,
a `-L` każe iść za przekierowaniem:

```bash
curl -i http://127.0.0.1:8000/r/python
```

Pozostałe operacje:

```bash
curl http://127.0.0.1:8000/api/links
curl http://127.0.0.1:8000/api/links/python
curl -X DELETE -i http://127.0.0.1:8000/api/links/python
```

### Kody odpowiedzi i format błędów

| Kod | Kiedy |
|---|---|
| `200` | Gotowe, odpowiedź w treści |
| `201` | Utworzono nowy link |
| `204` | Gotowe, brak treści (po usunięciu) |
| `307` | Przekierowanie tymczasowe pod adres docelowy |
| `400` | Błędne dane wejściowe (np. adres inny niż `http://` lub `https://`) |
| `404` | Nie ma linku o takim kodzie |
| `409` | Podany kod jest już zajęty |
| `503` | Aplikacja działa, ale nie widzi bazy danych |

Każdy błąd ma tę samą postać:

```json
{"detail": "Kod 'python' jest już zajęty. Wybierz inny albo pomiń pole 'code'."}
```

Dlaczego przekierowanie to `307`, a nie `301`: kod `301` („przeniesiono na
stałe”) przeglądarka zapamiętuje i przy kolejnym wejściu nie pyta już serwera —
licznik kliknięć przestałby rosnąć. `307` wymusza pytanie za każdym razem.

## Metryki

`GET /metrics` zwraca zwykły tekst w formacie Prometheusa — po jednej linii
na metrykę, z opisem `# HELP` i typem `# TYPE`.

| Metryka | Typ | Znaczenie |
|---|---|---|
| `linkbox_up` | gauge | `1`, gdy baza odpowiada; `0`, gdy nie |
| `linkbox_links_total` | gauge | Liczba linków w bazie |
| `linkbox_redirects_total` | counter | Liczba przekierowań, z etykietą `code` |
| `linkbox_http_requests_total` | counter | Liczba żądań, z etykietami `method`, `path`, `status` |
| `linkbox_request_duration_seconds` | histogram | Czas obsługi żądań |

Różnica między typami: **gauge** to wartość chwilowa, która może rosnąć
i maleć (jak wskazówka na liczniku prądu); **counter** tylko rośnie i zeruje
się przy restarcie procesu; **histogram** zlicza próbki w przedziałach
(„ile żądań zmieściło się poniżej 0,1 s”).

Etykieta `path` zawiera **wzorzec** trasy (`/api/links/{code}`), a nie
konkretny adres. Gdyby trafiał tam prawdziwy kod linku, każdy nowy link
tworzyłby osobną serię danych i po tygodniu byłoby ich kilkadziesiąt tysięcy
zamiast kilkunastu.

Podgląd:

```bash
curl http://127.0.0.1:8000/metrics
```

## Testy i jakość kodu

```bash
pytest                  # testy
ruff check .            # linter — szuka błędów i niezgodności ze stylem
black --check .         # sprawdzenie formatowania (bez --check: formatuje)
```

Testy działają na bazie trzymanej w pamięci i **nie wymagają uruchomionego
serwera ani pliku `links.db`** — samo `pytest` wystarczy.

## Struktura projektu

```
api/
├── app/                    kod aplikacji
│   ├── __main__.py         uruchomienie przez `python -m app`
│   ├── main.py             złożenie aplikacji w całość
│   ├── config.py           odczyt zmiennych środowiskowych
│   ├── db.py               połączenie z bazą danych
│   ├── models.py           definicja tabeli `links`
│   ├── repository.py       zapytania SQL
│   ├── validation.py       sprawdzanie danych wejściowych
│   ├── schemas.py          opis danych wejścia i wyjścia
│   ├── metrics.py          metryki w formacie Prometheusa
│   ├── middleware.py       zliczanie żądań
│   ├── errors.py           jednolity format błędów
│   ├── dependencies.py     obiekty wstrzykiwane do tras
│   ├── runtime.py          logowanie i obsługa sygnałów
│   └── routes/             endpointy HTTP
├── alembic/                migracje bazy danych
├── tests/                  testy
├── requirements.txt        lista zależności z przypiętymi wersjami
├── .env.example            opis zmiennych środowiskowych
└── pyproject.toml          ustawienia pytest, ruff i black
```

## Gdy coś nie działa

1. **Przeczytaj log aplikacji od początku.** Pierwsze linie po starcie
   wypisują komplet ustawień: adres, port, bazę, stan CORS. Bardzo często
   odpowiedź jest właśnie tam — aplikacja wzięła inną wartość, niż się wydawało.
2. **Sprawdź `/health`.** Odpowiedź `503` oznacza, że aplikacja żyje, ale nie
   widzi bazy. Brak jakiejkolwiek odpowiedzi to zupełnie inny problem — pod tym
   adresem i portem nic nie nasłuchuje.
3. **`Address already in use`** — port jest zajęty przez inny proces.
   Użyj innego portu (`APP_PORT`) albo znajdź i zatrzymaj tamten proces.
4. **Błąd o braku tabeli `links`** — nie wykonano migracji.
   Uruchom `alembic upgrade head`.
5. **Błąd CORS w konsoli przeglądarki, a `curl` działa** — to nie usterka
   sieci ani serwera. Patrz „Uwaga o CORS” wyżej.
