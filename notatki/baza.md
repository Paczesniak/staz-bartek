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


