# Baza danych — z pliku na serwer

**To jedyny dokument, który dziś czytasz.** Zadania są w kolejności wykonania, pogrupowane w moduły.

## Cel dnia

Przez trzy dni twoja aplikacja trzymała dane w pliku `links.db`. Wczoraj przeniosłeś ten plik do wolumenu i dzięki temu przeżył usunięcie kontenera. To była właściwa naprawa — ale rozwiązała tylko jeden z problemów, jakie ma plik.

Dziś zamieniasz plik na **serwer bazy danych**: osobny kontener, z własnym procesem, do którego aplikacja łączy się przez sieć. Przy okazji przechodzisz przez trzy rzeczy, które w pracy robi się przy każdej takiej zmianie:

- **sterownik** — aplikacja nie umie rozmawiać z bazą, której nie zna, i powie ci to jednym konkretnym zdaniem w logu,
- **przeniesienie danych** — nowa baza jest pusta, a stare linki nie przeniosą się same,
- **kopia zapasowa** — a właściwie **odtworzenie z niej**, bo kopia, której nikt nigdy nie odtworzył, jest tylko plikiem.

Trzy rzeczy z poprzednich dni wracają dziś w nowej postaci:

- **`localhost` znaczy „ten sam komputer".** W F2 chodziło o Windowsa i VM-kę. Wczoraj — o maszynę i wnętrze kontenera. Dziś ostatni raz: dla kontenera z aplikacją `localhost` to on sam, a baza stoi w **innym kontenerze**. Wróci to do ciebie w awarii na koniec dnia.
- **Log czytasz od pierwszej linii.** Aplikacja przy starcie wypisuje, z jaką bazą się łączy. Dziś ta jedna linia jest twoim głównym narzędziem diagnostycznym.
- **Hierarchia trwałości danych.** W F1 ułożyłeś: zmienna powłoki → `tmpfs` → dysk. Wczoraj dołożyłeś warstwę zapisywalną kontenera i wolumen. Dziś dochodzi ostatnie piętro — jedyne, które chroni przed **twoim własnym błędem**, a nie przed awarią sprzętu.

## Zasady

- **Notatki idą do `notatki/baza.md`.** Na starcie: `export NOTATKI=~/staz/notatki/baza.md`.
- **Pracujesz na dwóch sesjach SSH naraz** — w jednej log, w drugiej polecenia.
- **Commituj po każdym module.**
- **Zapisuj pytania na bieżąco.** „Nie mam pytań" nadal nie jest dopuszczalną odpowiedzią.
- **Hasło do bazy jest hasłem.** Dziś pierwszy raz masz w projekcie prawdziwy sekret. Obowiązuje jedna zasada bez wyjątków: **hasło nie trafia do repozytorium**. Sprawdzimy to na końcu dnia.

## Zanim zaczniesz

### 1. Materiały

Na maszynie wirtualnej:

    cd ~/staz
    git pull
    ./zainstaluj.sh

### 2. Sprawdź, co zostało po wczoraj

    cd ~/staz/aplikacja
    docker compose ps
    docker volume ls

Powinieneś zobaczyć swój wczorajszy stos i wolumen z danymi. **Nie kasuj go** — te dane są dziś materiałem do przeniesienia.

Jeśli stos nie działa, podnieś go (`docker compose up -d`) i sprawdź, że `/health` odpowiada. Reszta dnia zakłada, że wczorajszy stan jest na miejscu.

### 3. Ustaw dzień

    lab dzien baza
    lab moduly

## Jak wygląda dzień

Ten sam schemat co zawsze:

    lab start <moduł>     # przygotowuje środowisko wszystkich zadań modułu
    lab grade <moduł>     # sprawdza, czy zrobiłeś dobrze — możesz powtarzać do skutku
    lab koniec <moduł>    # zamyka moduł i przechodzi do następnego

**O czasach.** Suma zadań to **240 minut**. Czasy są orientacyjne i nie są zakładem. Jeśli któreś zadanie idzie dłużej, zapisujesz po dwudziestu minutach, na czym stoisz, i idziesz dalej.

**Czego `lab grade` nie robi:** nie czyta twoich notatek w poszukiwaniu właściwych słów. Sprawdza **stan maszyny** — czy kontener bazy działa, czy ma healthcheck, ile wierszy jest w tabeli, czy plik kopii zawiera dane. Zrozumienie sprawdzamy na obronie.

**Każde zadanie ma cztery części:** „O co tu chodzi", „Czego potrzebujesz" (prompty do AI — proszą o **wytłumaczenie mechanizmu**, nie o gotowe polecenie), „Zadanie" i „Sprawdź się".

---

## Moduł: postgres — 50 min

    lab start postgres

### Z1. Baza to serwer, nie plik — 10 min

#### O co tu chodzi

SQLite jest biblioteką: twoja aplikacja **sama** otwiera plik i sama w nim pisze. Nie ma żadnego procesu bazy — jest kod aplikacji i plik na dysku.

PostgreSQL działa inaczej: to **osobny program**, który cały czas chodzi, pilnuje swoich plików i przyjmuje połączenia przez sieć. Aplikacja nie dotyka plików bazy; wysyła zapytania i dostaje odpowiedzi. Ta jedna różnica pociąga za sobą całą resztę — również to, że baza może stać na innej maszynie niż aplikacja, i że kilka aplikacji naraz może z niej korzystać, nie depcząc sobie po piętach.

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi różnicę między **SQLite** a **PostgreSQL** jako dwoma różnymi rodzajami baz danych: co w każdym przypadku jest procesem, kto otwiera pliki bazy i co właściwie znaczy „połączenie z bazą". Nie porównuj wydajności — chcę zrozumieć budowę.

> Wytłumacz mi, co robi polecenie `psql` i czym różni się od `pg_dump`. Kiedy używa się którego?

#### Zadanie

Uruchom Postgresa **na chwilę, obok wszystkiego innego**, tylko po to, żeby go zobaczyć:

    docker run -d --name proba-pg -e POSTGRES_PASSWORD=chwilowe postgres:16

1. `docker logs proba-pg` — czytaj od pierwszej linii. Znajdź linię, w której baza mówi, że jest gotowa przyjmować połączenia. Zapisz ją.
2. Wejdź do środka i rozejrzyj się:

       docker exec -it proba-pg psql -U postgres

   W `psql` wykonaj kolejno: `\l` (lista baz), `\dt` (tabele w bieżącej bazie), `SELECT version();`, potem `\q`.

3. Zapisz, co pokazało `\dt` i dlaczego akurat to.
4. Posprzątaj: `docker rm -f proba-pg`.

**Do notatek, dwa zdania:**

- Czym różni się „baza danych" w sensie SQLite od „bazy danych" w sensie Postgresa — użyj słowa **proces**.
- Kontener `proba-pg` usunąłeś razem z jego danymi i nic cię to nie kosztowało. Napisz jednym zdaniem, dlaczego przy bazie z prawdziwymi danymi ta sama komenda jest jedną z najgroźniejszych, jakie znasz.

**Sprawdź się:** `lab grade postgres` — wyjdzie na czerwono, masz przed sobą dwa kolejne zadania modułu.

### Z2. Usługa `db` w twoim stosie — 25 min

#### O co tu chodzi

Wczoraj napisałeś `compose.yaml` z dwiema usługami: `api` i `web`. Dziś dochodzi trzecia — `db`. Nie zmieniasz przy tym niczego w aplikacji; dokładasz jej sąsiada.

Dwie rzeczy zrobisz inaczej, niż podpowiada pierwszy przykład z internetu, i obie są celowe.

**Baza nie publikuje portu na zewnątrz.** Usługi `api` i `web` mają `ports:`, bo do nich puka przeglądarka z twojego Windowsa. Do bazy nie puka nikt poza `api` — a kontenery jednego stosu widzą się nawzajem **po nazwie usługi**, bez żadnego przekierowania portów. Dopisanie `ports: "5432:5432"` wystawiłoby twoją bazę na całą sieć, w której stoi VM-ka. Nie rób tego.

**Hasło nie trafia do `compose.yaml`.** `compose.yaml` jest w repozytorium, a repozytorium jest na GitHubie — hasło wpisane wprost do tego pliku jest hasłem opublikowanym. Docker Compose czyta natomiast **automatycznie** plik `.env` z katalogu projektu i podstawia z niego wartości w miejsce `${NAZWA}`. Ten plik zostaje na maszynie i **nigdy** nie idzie do repozytorium.

To nie jest ostrożność na wyrost: skanery przeszukują publiczne repozytoria pod kątem haseł i kluczy w kilka minut od wypchnięcia.

#### Czego potrzebujesz

> Wytłumacz mi, jak w Docker Compose kontenery jednego stosu widzą się nawzajem: co pełni rolę nazwy hosta, czy potrzebne jest do tego `ports:` i czym `ports:` różni się od `expose:`. Podaj przykład dwóch usług, z których jedna łączy się z drugą.

> Wytłumacz mi zmienne `POSTGRES_USER`, `POSTGRES_PASSWORD` i `POSTGRES_DB` w oficjalnym obrazie postgres: kiedy dokładnie są używane i co się stanie, jeśli zmienię ich wartość wtedy, gdy baza ma już swoje dane w wolumenie.

#### Zadanie

Dopisz do `compose.yaml` trzecią usługę — `db`:

1. Obraz `postgres:16` — **konkretny tag**, tak samo jak wczoraj przy swoim obrazie i przy serwerze frontu.
2. Zmienne `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — nazwę użytkownika i bazy wybierz sam (proponuję `linkbox`), hasło też. **Hasło wstaw przez `${...}`**, a jego wartość zapisz w pliku `aplikacja/.env`:

       # aplikacja/.env — zostaje na maszynie, nie idzie do repozytorium
       POSTGRES_PASSWORD=tu-twoje-haslo

   Zanim pójdziesz dalej, dopisz `.env` do `.gitignore` w `~/staz` i sprawdź `git status`. Kolejność jest ważna — plik z hasłem ma być ignorowany, **zanim** zrobisz następny commit.
3. **Nazwany wolumen** podmontowany pod `/var/lib/postgresql/data` — to katalog, w którym Postgres trzyma wszystko. Bez tego twoja baza żyje w warstwie zapisywalnej kontenera; wczoraj widziałeś, ile to jest warte.
4. Polityka restartu, tak samo jak przy pozostałych usługach.
5. **Bez `ports:`** — patrz wyżej.

Potem:

    docker compose up -d
    docker compose ps
    docker compose logs db

Sprawdź, że w logu bazy widzisz tę samą linię o gotowości, co w Z1.

**Do notatek:**

- Wklej fragment `compose.yaml` z usługą `db`.
- Jedno zdanie: pod jaką nazwą kontener `api` będzie widział bazę i skąd ta nazwa się bierze.
- Jedno zdanie: co zobaczy ktoś, kto sklonuje twoje repozytorium — i czego mu zabraknie, żeby uruchomić stos.
- Jedno zdanie: co stanie się z zawartością bazy, gdy jutro zrobisz `docker compose down` bez dodatkowych przełączników, a co — gdy dopiszesz `-v`.

**Sprawdź się:** `lab grade postgres`

### Z3. 🔮 Kto pierwszy: baza czy aplikacja — 15 min

#### O co tu chodzi

Compose podnosi kontenery praktycznie równocześnie. Baza potrzebuje kilku sekund, żeby przygotować pliki i zacząć przyjmować połączenia — aplikacja startuje szybciej i puka do niej, zanim tamta zdąży odpowiedzieć.

Efekt jest podstępny: **na twojej maszynie zwykle działa**, bo obraz jest już pobrany i wszystko idzie szybko. Sypie się dopiero na wolniejszym serwerze albo po restarcie maszyny — czyli tam, gdzie nikt nie patrzy.

`depends_on` w najprostszej postaci mówi tylko „uruchom `db` przed `api`". To za mało, bo **„uruchomiony" nie znaczy „gotowy"**. Dopiero healthcheck pozwala odróżnić jedno od drugiego.

#### Czego potrzebujesz

> Wytłumacz mi w Docker Compose różnicę między `depends_on` bez warunku a `depends_on` z `condition: service_healthy`. Co dokładnie znaczy, że kontener jest „healthy", kto to sprawdza i jak definiuje się `healthcheck`. Wytłumacz też pola `interval`, `timeout`, `retries` i `start_period`.

> Do czego służy polecenie `pg_isready` i czym różni się od zwykłej próby połączenia z bazą?

#### Zadanie

1. **Przewidywanie, do notatek, przed sprawdzeniem:** za chwilę przełączysz aplikację na Postgresa. Napisz jedno zdanie — **po czym poznasz w logu aplikacji**, że wystartowała, zanim baza była gotowa? Jakiego rodzaju komunikatu się spodziewasz?
2. Dodaj do usługi `db` **healthcheck** oparty o `pg_isready` (z właściwym użytkownikiem i bazą), z sensownym `interval`, `retries` i `start_period`.
3. Dodaj do usługi `api` zależność od bazy — z warunkiem `service_healthy`.
4. `docker compose up -d`, a potem `docker compose ps`. W kolumnie statusu przy `db` zobaczysz `(healthy)` — jeśli nie od razu, poczekaj i powtórz.
5. Sprawdź to samo dokładniej:

       docker inspect --format '{{.State.Health.Status}}' $(docker compose ps -q db)

**Do notatek:**

- Wklej definicję healthchecka.
- Jedno zdanie: czym różni się „kontener działa" od „kontener jest zdrowy" i który z tych stanów widzi `docker compose ps`, gdy healthchecka nie ma wcale.

**Sprawdź się:** `lab grade postgres`, potem `lab koniec postgres`

---

## Moduł: sterownik — 40 min

    lab start sterownik

### Z4. 🔮 Przełączenie, które się nie uda — 10 min

#### O co tu chodzi

Masz działającą bazę i działającą aplikację, które o sobie nie wiedzą. Łączy je jedna zmienna: `DATABASE_URL`.

To zadanie jest krótkie i ma jeden cel: **zapisać przewidywanie, zanim zobaczysz wynik**. Za dziesięć minut będziesz wiedział, czy twój model tego, jak aplikacja rozmawia z bazą, jest trafny.

#### Czego potrzebujesz

> Wytłumacz mi budowę adresu połączenia do bazy w formacie SQLAlchemy, na przykładzie `postgresql://uzytkownik:haslo@host:5432/nazwa_bazy`. Co oznacza każdy element, który z nich decyduje o wyborze **sterownika**, a który o tym, z jaką maszyną się łączymy?

#### Zadanie

1. **Najpierw, do notatek — przewidywanie.** Zmienisz `DATABASE_URL` z adresu SQLite na adres Postgresa. Napisz **przed** zrobieniem czegokolwiek:
   - czy aplikacja wstanie,
   - jeśli nie, to co konkretnie zobaczysz w logu,
   - czy twoje wczorajsze linki będą widoczne po przełączeniu.

   Trzy zdania. Nie sprawdzaj przed zapisaniem — to jest cała wartość tego zadania.

2. Zmień w `compose.yaml` zmienną `DATABASE_URL` usługi `api` tak, żeby wskazywała twoją bazę: użytkownik, hasło, **host równy nazwie usługi bazy**, port `5432`, nazwa bazy.
3. `docker compose up -d`
4. `docker compose logs api` — **od pierwszej linii**.

**Do notatek:** wklej komunikat, na którym aplikacja się zatrzymała. Cały, razem z ostatnią linią.

**Sprawdź się:** `lab grade sterownik` — na tym etapie ma być na czerwono.

### Z5. Aplikacja nie zna tej bazy — 30 min

#### O co tu chodzi

Komunikat, który przed chwilą zobaczyłeś, kończy się linią w rodzaju:

    ModuleNotFoundError: No module named 'psycopg2'

To jest jeden z najuczciwszych błędów, jakie spotkasz. Mówi wprost: brakuje **modułu** o konkretnej nazwie.

SQLAlchemy jest warstwą pośrednią — potrafi rozmawiać z wieloma bazami, ale samo nie umie mówić w żadnym z ich języków sieciowych. Do każdej bazy potrzebuje **sterownika**: osobnej biblioteki, która wie, jak wygląda protokół danej bazy. Dla SQLite sterownik jest wbudowany w Pythona, więc przez trzy dni nie musiałeś o nim myśleć. Dla Postgresa trzeba go zainstalować.

I tu wchodzi wczorajsza lekcja: **twoja aplikacja mieszka teraz w obrazie**. Instalowanie czegokolwiek w działającym kontenerze nie ma sensu — zniknie przy pierwszym `docker compose up`. Zmiana musi trafić do `requirements.txt`, a obraz trzeba **zbudować od nowa**.

#### Czego potrzebujesz

> Wytłumacz mi, czym jest **sterownik bazy danych (DBAPI)** w Pythonie i dlaczego SQLAlchemy go potrzebuje. Dlaczego dla SQLite nic nie trzeba instalować, a dla PostgreSQL już tak?

> Czym różnią się pakiety `psycopg2`, `psycopg2-binary` i `psycopg` (wersja 3)? Który wybrać w projekcie na naukę i dlaczego? Czy wybór wpływa na to, jak wygląda adres połączenia?

> Wytłumacz mi, dlaczego zmiana w `requirements.txt` nie działa, dopóki nie zbuduję obrazu od nowa. Jak w Docker Compose zbudować obraz ponownie i czym różni się `docker compose up -d --build` od `docker compose build`?

#### Zadanie

1. Dopisz sterownik do `aplikacja/api/requirements.txt` — **z przypiętą wersją** (`==`), tak jak wszystkie pozostałe zależności w tym pliku. Sprawdzona i działająca: `psycopg2-binary==2.9.11`.
2. Zbuduj obraz od nowa i podnieś stos.
3. `docker compose logs api` — od pierwszej linii. Znajdź linię zaczynającą się od **`Baza danych:`** i zapisz ją w całości.
4. Sprawdź, że aplikacja odpowiada: `/health` ma zwrócić `"database": "ok"`.
5. Otwórz front w przeglądarce (ten sam adres co wczoraj) i zobacz listę linków.

**Do notatek, trzy rzeczy:**

- Linia `Baza danych:` z logu. Zwróć uwagę, **co stoi w miejscu hasła** — i napisz jedno zdanie, dlaczego aplikacja tak to wypisuje.
- Porównanie z twoim przewidywaniem z Z4: co się zgodziło, co nie.
- Lista linków w przeglądarce wygląda inaczej niż wczoraj. Jedno zdanie: **dlaczego** — i gdzie w takim razie są twoje wczorajsze linki.

**Sprawdź się:** `lab grade sterownik`, potem `lab koniec sterownik`

---

## Moduł: migracja — 30 min

    lab start migracja

### Z6. Skąd w nowej bazie wzięły się tabele — 15 min

#### O co tu chodzi

Nowa baza wstała pusta. Mimo to aplikacja działa, `/health` mówi `ok`, a dodawanie linków przechodzi. Ktoś więc utworzył w niej tabele — i warto wiedzieć kto, bo za tydzień to samo ma się wydarzyć na serwerze, którego jeszcze nie ma.

Wczoraj zbudowałeś obraz tak, żeby migracja wykonywała się **przy starcie kontenera**, a nie przy budowaniu. Dziś widzisz, po co: ten sam obraz, uruchomiony przy nowej, pustej bazie, sam doprowadził ją do stanu, jakiego oczekuje kod.

#### Czego potrzebujesz

> Wytłumacz mi, czym są **migracje bazy danych** i po co istnieją, skoro strukturę tabel można utworzyć jednym poleceniem z kodu. Co daje trzymanie historii zmian struktury w plikach w repozytorium?

> W narzędziu Alembic: co robi `alembic upgrade head`, co pokazuje `alembic current`, a co `alembic history`? Do czego służy tabela `alembic_version` w bazie?

#### Zadanie

1. Wejdź do bazy i rozejrzyj się — tym razem to **twoja** baza, nie próbna:

       docker compose exec db psql -U <użytkownik> -d <baza>

   W `psql`: `\dt` (tabele), potem `SELECT * FROM alembic_version;`, potem `SELECT count(*) FROM links;`, na koniec `\q`.

2. Zapisz, jakie tabele są w bazie. Jedna z nich nie przechowuje żadnych linków — napisz, do czego służy.
3. Zapytaj Alembica, co sądzi o stanie bazy:

       docker compose exec api alembic current

4. Porównaj z historią:

       docker compose exec api alembic history

**Do notatek:**

- Wynik `\dt` i wynik `alembic current`.
- Dwa zdania: skąd Alembic **wie**, że migracja została już wykonana, i co by się stało, gdyby ta wiedza zginęła (np. gdyby ktoś usunął tabelę `alembic_version`).
- Jedno zdanie: gdzie fizycznie leżą pliki migracji i dlaczego trafiają do repozytorium razem z kodem.

**Sprawdź się:** `lab grade migracja`

### Z7. Ta sama migracja, druga baza — 15 min

#### O co tu chodzi

Masz teraz dwie bazy o **identycznej strukturze** i różnej zawartości: wczorajszy SQLite w wolumenie i dzisiejszy Postgres. Struktura jest identyczna nie przez przypadek — obie przeszły tę samą migrację, opisaną tym samym plikiem w repozytorium.

To jest cała obietnica migracji: opis struktury jest **w kodzie**, jeden dla wszystkich środowisk, i wykonuje się tak samo na laptopie, w testach i na produkcji.

#### Czego potrzebujesz

> Wytłumacz mi, dlaczego ten sam plik migracji potrafi utworzyć tabele w SQLite i w PostgreSQL, choć te bazy różnią się typami danych i składnią SQL. Co robi tu warstwa pośrednia (SQLAlchemy) i gdzie leżą granice tej przenośności?

#### Zadanie

1. Znajdź plik migracji w repozytorium (`aplikacja/api/alembic/versions/`) i przeczytaj go. Nie musisz rozumieć każdej linii — znajdź nazwę tabeli i nazwy kolumn.
2. Porównaj strukturę tabeli `links` w obu bazach.

   W Postgresie:

       docker compose exec db psql -U <użytkownik> -d <baza> -c '\d links'

   W starym SQLite — plik leży w wolumenie z wczoraj. Podejrzyj go bez kopiowania, uruchamiając jednorazowy kontener z podmontowanym wolumenem:

       docker run --rm -v <nazwa-wolumenu>:/dane python:3.12-slim \
         python -c "import sqlite3,sys; c=sqlite3.connect('/dane/links.db'); \
         print([r[0] for r in c.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')]); \
         print(c.execute('SELECT count(*) FROM links').fetchone())"

   Nazwę wolumenu i ścieżkę do pliku bazy weź ze swojego wczorajszego `compose.yaml` — muszą się zgadzać z tym, co tam ustawiłeś.

3. Zapisz liczbę linków w starej bazie. **Będzie ci potrzebna w następnym module.**

**Do notatek:**

- Lista kolumn tabeli `links` z Postgresa.
- Liczba linków w starej bazie SQLite i w nowej bazie Postgres.
- Jedno zdanie: co to znaczy, że migracja jest „wersjonowana", i po czym poznasz, że dwie bazy są na tej samej wersji.

**Sprawdź się:** `lab grade migracja`, potem `lab koniec migracja`

---

## Moduł: dane — 40 min

    lab start dane

### Z8. Przeprowadzka — 40 min

#### O co tu chodzi

Nowa baza działa i jest pusta. Stare linki leżą w pliku SQLite w wolumenie. Nikt ich nie przeniesie za ciebie — a w prawdziwej migracji to właśnie ten krok robi się w nocy, z wyłączonym ruchem, i to on decyduje o powodzeniu całej operacji.

Zadanie jest otwarte: **masz przenieść dane, sposób wybierasz sam**. Poniżej masz trzy drogi, z których każda jest w porządku. Wybierz jedną, ale **umiej wytłumaczyć, dlaczego akurat tę**.

**Uwaga na jedną rzecz.** Kolumna `code` ma w bazie ograniczenie unikalności. Jeśli uruchomisz przenoszenie dwa razy, za drugim razem dostaniesz błąd o naruszeniu tego ograniczenia — i to jest zachowanie **poprawne**. Zastanów się, zanim zaczniesz, jak chcesz to obsłużyć.

#### Czego potrzebujesz

> Mam dane w bazie SQLite (plik) i chcę je przenieść do PostgreSQL, do tabeli o identycznej strukturze. Wytłumacz mi trzy możliwe podejścia: (1) skrypt w Pythonie czytający z jednej bazy i piszący do drugiej, (2) eksport do pliku CSV i import po stronie Postgresa, (3) wygenerowanie poleceń INSERT ze SQLite. Dla każdego podejścia powiedz, gdzie są pułapki. Nie pisz mi jeszcze kodu.

> Wytłumacz mi, czym w PostgreSQL jest **sekwencja** dla kolumny `id` typu `serial`/`identity` i co się dzieje, gdy wstawię wiersze z jawnie podanym `id` — czy kolejny automatyczny `id` będzie poprawny? Jak to sprawdzić i naprawić?

> Wytłumacz mi polecenie `docker run --rm -v NAZWA_WOLUMENU:/gdzies OBRAZ` — co dokładnie robi `--rm`, jak działa podmontowanie wolumenu i dlaczego to jest wygodny sposób na dostanie się do danych bez uruchamiania całego stosu.

#### Zadanie

1. Przenieś linki ze starej bazy SQLite do Postgresa. Wybraną drogą, z pomocą AI — **ale kod, który uruchamiasz, masz rozumieć na tyle, żeby powiedzieć, co robi każda jego linia**. Zapytam o to na obronie.
2. Sprawdź wynik po stronie bazy, nie po stronie aplikacji:

       docker compose exec db psql -U <użytkownik> -d <baza> -c "SELECT count(*) FROM links;"

   Liczba ma się zgadzać z tą, którą zapisałeś w Z7.

3. Sprawdź wynik po stronie aplikacji: odśwież front w przeglądarce. Twoje wczorajsze linki mają tam być.
4. **Sprawdź sekwencję** — dodaj przez front albo przez API jeden nowy link. Jeśli dostaniesz błąd o duplikacie klucza, to znaczy, że licznik `id` w Postgresie nie wie o wierszach, które wstawiłeś ręcznie. Napraw to (patrz drugi prompt) i dodaj link jeszcze raz.
5. Skrypt albo polecenia, których użyłeś, zapisz w repozytorium — w katalogu `narzedzia/` w `~/staz`. To jest dokument z operacji, nie śmieć.

**Do notatek:**

- Którą drogę wybrałeś i dlaczego.
- Liczba linków przed i po, z obu stron (baza i front).
- Co się stało przy dodawaniu nowego linku w punkcie 4 i jak to rozwiązałeś. Jeśli nic się nie stało — napisz, dlaczego twoja metoda przenoszenia nie zepsuła sekwencji.
- Jedno zdanie: co poszłoby nie tak, gdybyś uruchomił przenoszenie drugi raz.

**Sprawdź się:** `lab grade dane`, potem `lab koniec dane`

---

## Moduł: kopia — 20 min

    lab start kopia

### Z9. Kopia zapasowa — 20 min

#### O co tu chodzi

Wolumen chroni dane przed usunięciem kontenera. Nie chroni przed niczym innym: ani przed `docker compose down -v`, ani przed `DROP TABLE`, ani przed awarią dysku, ani przed tobą o siedemnastej w piątek.

Kopia zapasowa to **osobny plik, poza bazą**, z którego da się odtworzyć stan. Postgres ma do tego własne narzędzie — `pg_dump` — które nie kopiuje plików bazy, tylko wypisuje polecenia SQL odtwarzające jej zawartość. Dzięki temu taką kopię da się wczytać również do bazy w innej wersji albo na innej maszynie.

**To zadanie i następne są parą.** Plik, który za chwilę zrobisz, będzie ci potrzebny w następnym module — tam twoje dane znikną. Nie zaczynaj modułu `odtworzenie`, dopóki `lab grade kopia` nie jest na zielono.

#### Czego potrzebujesz

> Wytłumacz mi, co robi `pg_dump` i czym różni się od skopiowania katalogu z plikami bazy. Co oznaczają przełączniki `--clean` i `--if-exists` i dlaczego zwykle warto ich użyć? Czym różni się dump w formacie zwykłego SQL od formatu własnego (`-Fc`)?

> Wytłumacz mi, dlaczego kopia zapasowa trzymana na tej samej maszynie co baza jest „lepsza niż nic, ale to nie jest backup". Jaka jest zasada 3-2-1?

#### Zadanie

1. Zrób zrzut swojej bazy do pliku **poza kontenerem** — do katalogu `~/staz/kopie/` na maszynie. Nazwa pliku ma zawierać datę.

   Wskazówka co do konstrukcji: `docker compose exec` uruchamia polecenie w kontenerze, a jego wyjście możesz przekierować do pliku na maszynie. Uważaj na to, żeby polecenie nie próbowało otworzyć terminala — przy przekierowaniu do pliku przydaje się `-T`.

   Użyj `--clean --if-exists` (patrz prompt wyżej).

2. Obejrzyj, co powstało — to zwykły tekst:

       ls -lh ~/staz/kopie/
       head -30 ~/staz/kopie/<twój-plik>.sql
       grep -c "INSERT\|COPY" ~/staz/kopie/<twój-plik>.sql

3. Znajdź w pliku miejsce, w którym są twoje linki. Zapisz, jak wygląda (jedna linia wystarczy).
4. **Ten katalog leży w repozytorium, ale jego zawartość nie może do niego trafić.** Zrzut bazy to plik generowany — waży swoje, zmienia się przy każdym wykonaniu i nie ma czego wersjonować. Dopisz `kopie/` do `.gitignore` w `~/staz` i sprawdź `git status`.

**Do notatek:**

- Polecenie, którym zrobiłeś kopię — dokładnie takie, jakiego użyłeś.
- Rozmiar pliku i liczba linii z danymi.
- Dwa zdania: dlaczego ten plik nie może trafić do repozytorium, mimo że nie ma w nim hasła. Zastanów się przy okazji, czy **na pewno** nie ma — sprawdź to, zamiast zakładać.

**Sprawdź się:** `lab grade kopia`, potem `lab koniec kopia`

---

## Moduł: odtworzenie — 25 min

    lab start odtworzenie

### Z10. Odtworzenie — 25 min

#### O co tu chodzi

Kopia, której nikt nigdy nie odtworzył, nie jest kopią zapasową. Jest plikiem, o którym wszyscy zakładają, że zadziała — i który sprawdza się pierwszy raz w dniu awarii, kiedy nie ma już czasu na naukę.

`lab start odtworzenie` **usunął zawartość twojej tabeli `links`**. Baza działa, aplikacja działa, front się otwiera — tylko lista jest pusta. Dokładnie tak wygląda pomyłka o siedemnastej w piątek.

Masz to odtworzyć z pliku, który zrobiłeś w Z9.

#### Czego potrzebujesz

> Jak wczytać plik SQL zrobiony przez `pg_dump` z powrotem do bazy PostgreSQL działającej w kontenerze Docker Compose? Wytłumacz mi rolę przełącznika `-T` w `docker compose exec` i po co przy wczytywaniu ustawia się `ON_ERROR_STOP=1`.

> Czym różni się odtworzenie na bazę, w której tabele jeszcze istnieją, od odtworzenia na bazę pustą? Co w tym kontekście robi dump zrobiony z `--clean --if-exists`?

#### Zadanie

1. Zanim cokolwiek zrobisz — sprawdź i **zapisz stan**: ile wierszy jest teraz w tabeli `links` i co pokazuje front.
2. Odtwórz dane z kopii z Z9.
3. Sprawdź trzy rzeczy, w tej kolejności:
   - liczba wierszy w bazie (`SELECT count(*) FROM links;`),
   - odpowiedź API (`/api/links`),
   - lista w przeglądarce.
4. Dodaj przez front nowy link i sprawdź, że się zapisał. Jeśli nie — patrz Z8 punkt 4, to ten sam mechanizm.

**Do notatek — to jest mini-raport z awarii i chcę go w tej formie:**

- **Objaw:** co dokładnie było widać (baza, API, przeglądarka).
- **Przyczyna:** co się stało z danymi.
- **Naprawa:** polecenie, którym odtworzyłeś, i ile to zajęło.
- **Weryfikacja:** czym potwierdziłeś, że dane wróciły — wymień wszystkie trzy sprawdzenia.
- **Wniosek:** jedno zdanie o tym, czego dowiedziałeś się o swojej kopii zapasowej, czego nie wiedziałeś przed Z10.

**Sprawdź się:** `lab grade odtworzenie`, potem `lab koniec odtworzenie`

---

## Moduł: awaria — 25 min

    lab start awaria

### Z11. Kumulacja: stos wstaje, aplikacja nie — 25 min

#### O co tu chodzi

To zadanie działa tak samo jak wczorajsza awaria i jak „sklep" z F2: **nie mówię ci, ile jest wad ani jakie**. `lab start awaria` podłożył coś w konfiguracji twojego stosu. Twoje zadanie: doprowadzić aplikację z powrotem do działania, **bez zmian w kodzie aplikacji** i bez usuwania danych.

Wszystko, czego potrzebujesz, było już dziś na ekranie.

#### Czego potrzebujesz

> Wytłumacz mi, jak w PostgreSQL wygląda komunikat o błędnym haśle, a jak o braku połączenia z serwerem — i co każdy z nich mówi o tym, na którym etapie połączenie się urwało. Chcę umieć odróżnić „nie dobiłem się do serwera" od „dobiłem się, ale mnie nie wpuścił".

> Przypomnij mi, w jaki sposób plik `compose.override.yaml` łączy się ze zwykłym `compose.yaml` i która wartość wygrywa przy konflikcie.

#### Zadanie

1. `docker compose ps` — zobacz, co stoi, a co się przewraca.
2. `docker compose logs api` — **od pierwszej linii**. Znajdź linię `Baza danych:` i porównaj ją z tą, którą zapisałeś w Z5. Różnica jest tam, gdzie leży problem.
3. Diagnozuj i naprawiaj **po jednej rzeczy naraz**, zapisując po każdej próbie, co się zmieniło w komunikacie. Komunikat, który się zmienia, jest dowodem, że idziesz w dobrą stronę.
4. Zakończ, gdy: `/health` mówi `"database": "ok"`, front pokazuje listę linków, a liczba linków jest **taka sama jak przed awarią**.

**Do notatek — ten sam format co Z10:**

- **Objaw:** dosłownie, co zobaczyłeś.
- **Ile wad znalazłeś** i w jakiej kolejności je odkrywałeś.
- Dla każdej: **jak się objawiała, po czym ją poznałeś, czym naprawiłeś**.
- **Weryfikacja:** czym potwierdziłeś, że wszystko wróciło — łącznie z liczbą linków.
- Jedno zdanie: która z tych wad była trudniejsza do znalezienia i dlaczego.

**Sprawdź się:** `lab grade awaria`, potem `lab koniec awaria`

---

## Moduł: zamkniecie — 10 min

    lab start zamkniecie

### Z12. Zamknięcie dnia — 10 min

#### Zadanie

1. Uporządkuj `notatki/baza.md` — cztery sekcje na końcu:

   **Eksperymenty** — co sprawdziłeś dziś sam, poza tym, o co prosiłem.

   **Diagnozy** — dwa raporty z awarii (Z10 i Z11) w jednym miejscu, w formacie objaw → przyczyna → naprawa → weryfikacja.

   **Hierarchia trwałości** — pełna lista pięter, jakie poznałeś przez cały staż, od najbardziej ulotnego do najtrwalszego. Zacząłeś ją w F1, dokładałeś we wtorek i środę, dziś dokładasz ostatnie. Przy każdym piętrze jedno zdanie: **przed czym chroni, a przed czym nie**.

   **Trzy pytania** — trzy rzeczy, których dziś nie rozumiesz albo które cię zaskoczyły. „Nie mam pytań" nie jest odpowiedzią.

2. **Sprawdź, czy hasło do bazy nie trafiło do repozytorium.** To nie jest formalność:

       cd ~/staz
       git status --ignored | grep -A2 "Ignored files"
       git log --all -p -S "$(grep POSTGRES_PASSWORD aplikacja/.env | cut -d= -f2-)" | head -5

   Drugie polecenie przeszukuje **całą historię** repozytorium za twoim hasłem — nie tylko bieżący stan plików. Ma nie zwrócić niczego.

   Jeśli hasło gdzieś jest — zatrzymaj się i napisz do mnie **przed** commitem. Sekret raz wypchnięty zostaje w historii nawet po usunięciu go z pliku; usuwa się go zupełnie inaczej i chcę, żebyś zobaczył, jak.

3. Sprawdź, że w `.gitignore` są **oba** wpisy: `.env` (hasło) i `kopie/` (zrzuty bazy), i że `git status` jest czysty.
4. Commit i push:

       git add notatki/ wyniki/ aplikacja/ narzedzia/ .gitignore
       git commit -m "docs: notatki i konfiguracja dnia baza"
       git push

5. `lab koniec baza` — raport dnia. Potem jeszcze jeden commit z raportem.

**Sprawdź się:** `lab grade zamkniecie`, potem `lab koniec zamkniecie`

---

## Na koniec

Zrobiłeś dziś to, co w ogłoszeniach o pracę nazywa się „migracją bazy danych": postawiłeś serwer bazy, przełączyłeś na niego aplikację, przeniosłeś dane, zrobiłeś kopię i — co ważniejsze — **odtworzyłeś z niej**.

Jutro ostatni dzień: sprawiasz, że to wszystko sprawdza się samo, bez ciebie.
