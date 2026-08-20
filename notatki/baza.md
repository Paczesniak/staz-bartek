----- Baza danych -----

### Z1 

## Notatka startowa

SQLite:
- Nie ma osobnego serwera
- procesem jest głównie aplikacja
- aplikacja przez bibliotekę SQLite otwiera plik np. baza.db
- Połącznie z bazą = otwarcie pliku bazy do pracy

PostgresSQL:
- działa jako osobny proces/serwer
- aplikacja nie otwiera plików bazy bezpośrednio
- pliki otwiea i obsługuje PostgresSQL
- Połącznie z bazą = połącznie aplikacji z serwerem PostgresSQL i utworzenie sesji

Komendy:
psql - służy do zapytań, zmian i administracji
	
Przykład:
	- psql -U bartek -d sklep (w tedy moge wpisywać komendy SQL)

pg_dump - do robienia kopii/eksportu bazy
	
Przykład: 
	- pg_dump -U bartek sklep > backup.sql

## Zadania

1. 2026-08-20 07:22:14.732 UTC [48] LOG:  database system is ready to accept connections

2. docker exec -it proba-pg psql -U postgres

\l - pokazuje listę bazy danych 

\dt - pokazuje tabele w aktualnej bazie

SELECT version; - pokazuje wersję PostgresSQL

\q - wychodze z psql

3. \dt - napisało Did not find any relatrion dlatego że jeszcze nie stworzyliśmy żadnej tabeli w bazie

4. docker rm -f proba-pg - usuwam kontener proba-pg

## Notatka końcowa 

- SQLite - baza to głównie plik otwieralny przez proces aplikacji, PostgresSQL baza jest obsługiwana przez osobny proces serwera PostgresSQL z którym aplikacja się łączy.

- docker rm -f jest goźne przy prawdziwej bazie bo jeśli dane są zapisne tylko w kontenerze, usunięcie kontenera może oznaczać bezpowrotną utratę danych.

### Z2

## Notatka startowa 

W Docker Compose kontenery w jednym stosie zwykle są w tej samej sieci i mogą łączyć się po nazwie usługi.

services:
  app:
    image: my-app
    depends_on:
      - db

  db:
    image: postgres
    expose:
      - "5432"

Natomiast PostgresSQL tak, że db pełni role hosta:

host: dp
port:5432

ports: — wystawia port kontenera na hosta, np. na Twoje Ubuntu/Windows:

ports:
  - "5432:5432"

expose: — informuje, że dany port jest używany wewnątrz sieci kontenerów:

expose:
  - "5432"

W oficjalnym obrazie postgres te zmienne są używane głównie przy pierwszym uruchomieniu pustej bazy:
- POSTGRES_USER — tworzy użytkownika
- POSTGRES_PASSWORD — ustawia mu hasło
- POSTGRES_DB — tworzy bazę o podanej nazwie

Uwaga! - Jeśli wolumen z danymi już istnieje, zmiana tych wartości nie przebuduje istniejącej bazy.

## Zadania

Cała kofiguracja pliku composer.yaml wygląda teraz tak:


services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      APP_HOST: 0.0.0.0
      APP_PORT: 8000
      CORS_ORIGINS: http://localhost:3000
      APP_NAME: linkbox-compose
      DATABASE_URL: sqlite:////data/links.db
    volumes:
      - linkbox-data:/data
    restart: unless-stopped

  web:
    image: nginx:1.27-alpine
    ports:
      - "3000:80"
    volumes:
      - ./web:/usr/share/nginx/html:ro
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: linkbox
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: linkbox
    volumes:
       - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  linkbox-data:
    external: true
    name: linkbox-data

  postgres_data:

## Notatka końcowa

- api widzi bazę pod nazwą db, bo jest to nazwa usługi w compose.yaml.
- Po sklonowaniu repo będzie compose.yaml, ale zabraknie pliku .env z hasłem
- docker compose down zostawia dane w wolumenie, a docker compose down -v usuwa też wolumen i dane
- Usługa db używa obrazu postgres:16, zmiennych POSTGRES_* i wolumenu postgres_data pod /var/lib/postgresql/data

### Z3

## Notatka startowa

depends_on - bez warunków oznacza uruchom tę usuługę wcześniej
condition: service_healthy - oznacza poczekaj aż zależna przejdzie healthcheck i będzie oznaczaona jako healthy

Pola: 
- interval: 5s (jak często Docker wykonuje test)
- timeout: 3s (ile maksymalnie czeka na wynik jednego testu)
- retries: 5 (ile kolejnych nieudanych testów może być zanim kontener dostanie status unkealthy
- start_period: 10s (czas na spokony start aplikacji)

healthy znaczy, że Docker uruchomił zdefiniowany healthcheck i zakończył się on powodzeniem. Sprawdza to Docker, wykonując polecenie z pola test.

pg_isready - służy do sprawdzenia czy serwer PostgresSQL jest gotowy przyjmować połącznia.

Przykład: 
pg_isready -U linkbox (sprawdza po prostu stan serwera)

Różnica pomiedzy pg_isready a psql:
- pg_isready (to szybki tesst czy PostgresSQL odpowiada i jest gotowy)
- psql (faktycznie logujesz się do konkretnej bazy i możesz wykonać polecenie SQL)

## Przewidywania 

Jeśli api wystaruje przed bazą w logach spodziewam się błędy połączenia z PostgreSQL albo indormacji że nie udało się połączyć z bazą. 

## Zadania 

Do compose.yaml dodałem:

- db:
healthcheck:
      test: ["CMD-SHELL", "pg_isready -U linkbox -d linkbox"]
      interval: 5s
      retries: 5
      start_period: 10s

- api: 
    depends_on:
      db:
        condition: service_healthy

Przebieg:  docker compose up -d -> docker compose ps (tam już zobaczyłem że db ma healthy) -> docker inspect --format '{{.State.Health.Status}}' $(docker compose ps -q db) 

## Notatka końcowa

- healthcheck:
      test: ["CMD-SHELL", "pg_isready -U linkbox -d linkbox"]
      interval: 5s
      retries: 5
      start_period: 10s
- Kontener działa” znaczy, że jego proces jest uruchomiony, a „kontener jest zdrowy” znaczy, że dodatkowo przechodzi zdefiniowany healthcheck; bez healthchecka docker compose ps pokazuje tylko, że kontener jest uruchomiony, np. Up.

### Z4

## Notatka startowa

postgresql://uzytkownik:haslo@host:5432/nazwa_bazy:
- postgresql:// — typ bazy / dialekt; może też wskazywać sterownik, np. postgresql+psycopg://
- uzytkownik — użytkownik bazy
- haslo — hasło
- host — adres maszyny lub nazwa usługi, np. db
- 5432 — port PostgreSQL
- nazwa_bazy — konkretna baza

sterownik wybiera część przed ://, np. postgresql+psycopg
maszynę/usługę wybiera host

## Przewidywania

1. Aplikacja może nie wystartować jeśli brakuje sterowownika PostgresSQL jak jest to wstanie.
2. W logu spodziwam się błędu o braku sterownika albo problem z połączniem z bazą 
3. Wczorajszych linków nie bęzie bo były zapisane w SQLite a teraz aplikacja przełączy sie na PostgreSQL

## Zadania

Błąd:
- ModuleNotFoundError: No module named 'psycopg'

Postgres działa i jest Healthy,
depends_on działa poprawnie,
DATABASE_URL wygląda dobrze,
problem jest już po stronie obrazu api.

### Z5

## Notatka startowa

1. Sterowniki SQLite są już w Pythonie natomiast PostgresSQL ich nie posiada i trzeba doinstalowywać. 
2. psycopg2 — starszy, bardzo popularny sterownik PostgreSQL dla Pythona
psycopg2-binary — gotowa binarna wersja psycopg2, łatwiejsza do instalacji
psycopg — nowsza wersja 3, obecnie zalecana do nowych projektów
3. Zmiana w requirements.txt nie zmienia już istniejącego obrazu. Pakiety są instalowane podczas docker build, więc trzeba zbudować obraz ponownie

## Zadania

1. Dopisałem psycopg2-binary==2.9.11
2. Odpaliłem docker compose up -d --build
3. Baza danych: postgresql (postgresql+psycopg2://linkbox:***@db:5432/linkbox)
4. curl http://localhost:8000/health
{"status":"ok","database":"ok","version":"1.0.0"}
5. storna działa nie ma linków bo nowa baza

## Notaka końcowa

- Baza danych: postgresql (postgresql+psycopg2://linkbox:***@db:5432/linkbox) — zamiast hasła jest ***, bo aplikacja ukrywa hasło w logach, żeby nie ujawniać danych dostępowych.
- Przewidywanie częściowo się zgodziło: aplikacja faktycznie nie wystartowała, ale problemem był brak sterownika psycopg, a nie sama gotowość bazy
- Lista jest pusta, bo aplikacja korzysta teraz z nowej bazy PostgreSQL; wczorajsze linki nadal są w starej bazie SQLite zapisanej w wolumenie

### Z6 

## Notatka startowa

Migracje to wersjonowane zmiany struktury bazy, np. utworzenie tabeli, dodanie kolumny albo zmiana typu pola.

Jednorazowe „utwórz tabele z kodu” mówi tylko, jak ma wyglądać baza teraz. Migracje zapisują kolejne kroki zmian:
- 0001 - utwórz tabelę links
- 0002 - dodaj kolumnę created_at
- 0003 - zmień długość pola code

Narzędzie Alembic:
- alembic upgrade head — wykonuje wszystkie brakujące migracje aż do najnowszej wersji.
- alembic current — pokazuje, na której migracji jest aktualnie baza.
- alembic history — pokazuje historię dostępnych migracji.
- alembic_version — tabela w bazie, w której Alembic zapisuje aktualną wersję migracji.

## Zadania

1. Użyte komendy:
- \dt
             List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+---------
 public | alembic_version | table | linkbox
 public | links           | table | linkbox
(2 rows)

- SELECT * FROM alembic_version;

 version_num
-------------
 0001
(1 row)

- SELECT count(*) FROm links;

 count
-------
     0
(1 row)

2. W bazie są dwie tabele: links i alembic_version.
links przechowuje linki, a alembic_version zapisuje, na której wersji migracji znajduje się baza

3. docker compose exec api alembic current
INFO     [alembic] alembic.env: Łączę się z bazą: postgresql+psycopg2://linkbox:***@db:5432/linkbox
INFO     [alembic] alembic.runtime.migration: Context impl PostgresqlImpl.
INFO     [alembic] alembic.runtime.migration: Will assume transactional DDL.
0001 (head)

4. docker compose exec api alembic history
<base> -> 0001 (head), Migracja początkowa — tworzy tabelę links.

## Notaktka końcowa

- \dt:
public | alembic_version | table | linkbox
public | links           | table | linkbox

- alembic current:
0001

- Alembic wie, że migracja została wykonana, bo zapisuje jej numer w tabeli alembic_version. Gdyby ta tabela zniknęła, Alembic straciłby informację o aktualnej wersji bazy i mógłby próbować wykonywać migracje ponownie albo zgłaszać błędy

- Pliki migracji fizycznie leżą w projekcie aplikacji, zwykle w katalogu alembic/versions/, i trafiają do repozytorium, żeby każdy miał tę samą historię zmian struktury bazy

### Z7

## Notatka wstepna

Ten sam plik migracji działa w SQLite i PostgreSQL, bo Alembic zwykle nie zapisuje „surowego SQL”, tylko używa operacji SQLAlchemy, np. „utwórz tabelę” albo „dodaj kolumnę”.

## Zadania

1. nano ~/staz/aplikacja/api/alembic/versions/20260810_0001_create_links_table.py
- Nazwa tabeli: links
- Kolumny (id, code, url, clicks, created_at)

2. docker compose exec db psql -U linkbox -d linkbox -c '\d links'

                                       Table "public.links"
   Column   |           Type           | Collation | Nullable |              Default
------------+--------------------------+-----------+----------+-----------------------------------
 id         | integer                  |           | not null | nextval('links_id_seq'::regclass)
 code       | character varying(64)    |           | not null |
 url        | character varying(2048)  |           | not null |
 clicks     | integer                  |           | not null | 0
 created_at | timestamp with time zone |           | not null |
Indexes:
    "pk_links" PRIMARY KEY, btree (id)
    "uq_links_code" UNIQUE CONSTRAINT, btree (code)
 
3. docker run --rm -v linkbox-data:/dane python:3.12-slim \
  python -c "import sqlite3; c=sqlite3.connect('/dane/links.db'); print([r[0] for r in c.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')]); print(c.execute('SELECT count(*) FROM links').fetchone())"
Wynik: (2,)

## Notatka końcowa

- Kolumny tabeli links w PostgreSQL: id, code, url, clicks, created_at.
- Stara baza SQLite: 2 linki. Nowa baza PostgreSQL: 0 linków.
- Migracja jest „wersjonowana”, bo każda zmiana struktury ma swój numer, np. 0001; dwie bazy są na tej samej wersji, jeśli mają ten sam numer w alembic_version.

### Z8

## Notatka startowa

1. Python: SQLite → PostgreSQL
- Skrypt czyta rekordy z SQLite i zapisuje je do Postgresa
- Plus: pełna kontrola nad typami i błędami
- Pułapki: daty, NULL, duplikaty, kolejność ID i transakcje

2. SQLite → CSV → PostgreSQL
- Eksportujesz dane do CSV, potem importujesz np. przez COPY
- Plus: proste i czytelne
- Pułapki: przecinki/cudzysłowy w danych, kodowanie, NULL, format dat

3. Generowanie INSERT
- SQLite generuje polecenia typu:
INSERT INTO links (...) VALUES (...);
- Potem wykonujesz je w PostgreSQL
- Pułapki: różnice składni SQL, escapowanie tekstu, typy danych i większe pliki

Ręczne ID i sekwencja to dwie osobne rzeczy, więc po imporcie danych warto je zsynchronizować.

Polecenie docker run --rm -v NAZWA_WOLUMENU:/gdzies OBRAZ uruchamia jednorazowy kontener i podpina do niego istniejący wolumen
- --rm — po zakończeniu kontener zostanie automatycznie usunięty
- -v NAZWA_WOLUMENU:/gdzies — podpina wolumen Dockera do katalogu /gdzies wewnątrz kontenera
- OBRAZ — obraz, z którego ma powstać ten tymczasowy kontener

## Zadania

1. SQLite do PostgreSQL

Polecenia: 
- mkdir -p narzedzia
- nano narzedzia/migracja_sqlite_postgres.py
- import os
import sqlite3
import psycopg2

sqlite_conn = sqlite3.connect("/dane/links.db")
sqlite_cur = sqlite_conn.cursor()

sqlite_cur.execute(
    "SELECT id, code, url, clicks, created_at FROM links"
)
rows = sqlite_cur.fetchall()

pg_conn = psycopg2.connect(
    host="db",
    dbname="linkbox",
    user="linkbox",
    password=os.environ["POSTGRES_PASSWORD"],
)

pg_cur = pg_conn.cursor()

for row in rows:
    pg_cur.execute(
        """
        INSERT INTO links (id, code, url, clicks, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        row,
    )

pg_conn.commit()

pg_cur.close()
pg_conn.close()
sqlite_cur.close()
sqlite_conn.close()

print(f"Przeniesiono rekordów: {len(rows)}")
- ~/staz/aplikacja$ docker network ls
NETWORK ID     NAME                DRIVER    SCOPE
aa3695c799e4   aplikacja_default   bridge    local
a32c3950ba86   bridge              bridge    local
5ea9768dd32c   host                host      local
8a5812a9c045   none                null      local
- docker run --rm \
  --network aplikacja_default \
  -v linkbox-data:/dane \
  -v ~/staz/narzedzia:/narzedzia:ro \
  --env-file ~/staz/aplikacja/.env \
  python:3.12-slim \
  sh -c "pip install psycopg2-binary==2.9.11 && python /narzedzia/migracja_sqlite_postgres.py"
ODP.: Przeniesiono rekordów: 2

2. docker compose exec db psql -U linkbox -d linkbox -c "SELECT count(*) FROM links;"

 count
-------
     2
(1 row)

3. Na stronie pojawiły się 2 linki (działa)

4. Dodał sie 3 link

5. Jest zapisany

## Notaka końcowa 

- Wybrałem skrypt w Pythonie, bo pozwala bezpośrednio odczytać rekordy z SQLite i zapisać je do PostgreSQL, a każdy krok jest łatwy do prześledzenia.
- Przed migracją: SQLite miało 2 linki, PostgreSQL 0. Po migracji: PostgreSQL miało 2 linki i front również pokazywał 2 linki
- Przy dodawaniu nowego linku nic się nie stało, bo po migracji sekwencja została zsynchronizowana z największym id, więc PostgreSQL nadał poprawne kolejne ID
- Gdybym uruchomił migrację drugi raz, dostałbym błąd przez duplikaty id lub unikalnego code

### Z9

## Notatka startowa

pg_dump - robi logiczny backup PostgreSQL: odczytuje strukturę i dane z bazy i zapisuje je do pliku, z którego można bazę odtworzyć
- --clean (dodaje usuwanie istniejących obiektów przed ich ponownym utworzeniem)
- --if-exists (przy usuwaniu używa IF EXISTS, żeby nie wywalać błędów, jeśli czegoś jeszcze nie ma)

Formaty:
- zwykły SQL — czytelny plik tekstowy z CREATE, INSERT itd.; odtwarzasz np. przez psql
- Fc — format własny/custom, binarny dla pg_restore; mniej czytelny ręcznie, ale daje większą kontrolę przy odtwarzaniu

Bo jeśli baza i backup są na tej samej maszynie, to awaria dysku, usunięcie plików albo uszkodzenie systemu może zniszczyć jedno i drugie naraz.
Zasada 3-2-1:
- 3 kopie danych,
- na 2 różnych rodzajach nośników,
- 1 kopia poza główną maszyną/lokalizacją.

## Zadania

1. mkdir -p ~/staz/kopie
docker compose exec -T db pg_dump -U linkbox -d linkbox --clean --if-exists > ~/staz/kopie/linkbox-2026-08-20.sql

2. ls -lh ~/staz/kopie/
head -30 ~/staz/kopie/linkbox-2026-08-20.sql
grep -c "INSERT\|COPY" ~/staz/kopie/linkbox-2026-08-20.sql

3. 
