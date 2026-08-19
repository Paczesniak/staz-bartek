### Z1

## Notatka wstępna

Docker: obraz a kontener
	- Obraz = gotowy, tylko do odczytu szablon aplikacji.
	- Kontener = uruchomiona instancja obrazu z własną zapisywalną warstwą.
	- Obraz składa się z wielu warstw, dzięki czemu Docker może je współdzielić i używać cache.

Kontener a maszyna wirtualna
	- VM ma własny system operacyjny i własne jądro.
	- Kontener korzysta z jądra systemu hosta i izoluje tylko procesy, pliki, sieć itd.
	- Dzięki temu kontenery są mniejsze i uruchamiają się szybciej, bo nie muszą startować całego systemu operacyjnego.

## Zadania

1. docker version - serwer ma wersje 29.1.3 i tak samo klient. 
Sprawidziłem czy działa w tle za pomocą (systemctl status docker). W tle działa część serwerowa Dockera. 

2. docker images -  pokazuje obraz czyli szblony do tworzenia kontenerów
docker ps -a - pokazuje wszystkie kontenery utworzonych obrazów

3. Na maszynie: python3 --version
Python 3.14.4

Na dockerze: Python 3.12.14

(Miałem problem z internetem w VM ale były ustawione 2 domyślne trasy, usunąłem domyślną trase enp0s8 i dziła)

4. Kontener proba jest widoczny tylko w docker ps -a, ponieważ jest zatrzymany. Status Exited (0) oznacza, że zakończył działanie poprawnie.

5. usunąłem docker rm proba 

## Notatka końcowa

1. docker images pokazuje dostępne obrazy, czyli szablony do tworzenia kontenerów, a docker ps -a pokazuje konkretne kontenery utworzone z tych obrazów.

2. Użytkownik należący do grupy docker ma w praktyce uprawnienia zbliżone do root, bo może uruchomić kontener z dostępem do systemu hosta.

## Komendy

- docker version (pokazuje wersję klienta i serwera Dockera)
- systemctl status docker (sprawdza, czy usługa Docker działa) 
- docker images (pokazuje dostępne obrazy Dockera)
- docker ps -a (pokazuje wszystkie kontenery, także zatrzymane)
- python3 --version (pokazuje wersję Pythona na maszynie)
- docker run --name proba python:3.12-slim python --version ( tworzy i uruchamia kontener proba z Pythonem 3.12 i pokazuje jego wersję)
- docker ps (pokazuje tylko działające kontenery)
- docker rm proba (usuwa kontener proba)

### Z2

## Notatka wstępna 

docker build
- FROM → wybiera bazowy obraz, np. Linuxa/Pythona, od którego zaczynasz budowę.
- WORKDIR → ustawia katalog roboczy wewnątrz obrazu, np. /app.
- COPY → kopiuje pliki z Twojego komputera do obrazu.
- RUN → wykonuje polecenie podczas budowania, np. instaluje biblioteki.
- USER → zapisuje, jako jaki użytkownik mają być wykonywane dalsze polecenia i później działać kontener.
- EXPOSE → zapisuje informację, na jakim porcie aplikacja ma nasłuchiwać; sam nie otwiera portu.
- CMD → zapisuje domyślne polecenie, które ma się uruchomić po starcie kontenera.

docker run
- USER → kontener działa jako użytkownik ustawiony wcześniej w Dockerfile.
- WORKDIR → proces startuje w ustawionym katalogu roboczym.
- CMD → Docker faktycznie wykonuje zapisane polecenie i uruchamia aplikację

Konkretnego tagu używa się po to, żeby build był przewidywalny i powtarzalny. slim zmniejsza obraz przez usunięcie zbędnych pakietów, a alpine jest jeszcze mniejszy, ale może mieć więcej problemów ze zgodnością bibliotek.

- pełny → największy, najwięcej rzeczy gotowych
- slim  → mniejszy, nadal dość typowe środowisko Debiana
- alpine → bardzo mały, ale większe ryzyko problemów ze zgodnością

.dockerignore ogranicza pliki przekazywane Dockerowi podczas budowania, a .gitignore pliki śledzone przez Git. Strukturę bazy przygotowuje się przy uruchomieniu, bo wtedy znana jest właściwa baza i jej aktualny stan.

Różnica:
- .gitignore mówi Gitowi, czego nie śledzić i nie commitować.
- .dockerignore mówi Dockerowi, czego nie brać do kontekstu budowania.

## Zadania

1. du -sh .venv (rozmiar środowiska wirtualnego) - 113M    .venv
du -sh . (rozmiar środowiska cąłego katalogu) - 113M    .

2. cat .gitignore (sprawdziłem co sie w nim znajduje i tak naprawde przepisałem te rzeczy do nano .dockerignore )

3. do nano Dockerfile wpisałem:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["python", "-m", "app"]

Co oznacza:
- FROM python:3.12-slim → konkretny lekki obraz Pythona, bez latest
- WORKDIR /app → katalog roboczy w kontenerze
- COPY requirements.txt . → kopiuje listę zależności
- RUN pip install ... → instaluje zależności do obrazu
- COPY . . → kopiuje kod aplikacji
- RUN useradd ... → tworzy zwykłego użytkownika
- USER appuser → aplikacja nie działa jako root
- EXPOSE 8000 → deklaruje port aplikacji
- CMD ["python", "-m", "app"] → przy starcie kontenera uruchamia to samo co wcześniej w systemd

4. zmieniłem CMD ["python", "-m", "app"] na CMD ["sh", "-c", "alembic upgrade head && python -m app"] żeby najpierw wykonywać migrację a dopiero potem uruchamiał aplikacje.

5. docker build -t linkbox:1.0 . (buduje obraz i nadaje mu nazwe linkbox:1.0) 
Rozmiar: 78.7MB 

6. docker run --rm linkbox:1.0 ls -a
.
..
.dockerignore
.env.example
.gitignore
Dockerfile
README.md
alembic
alembic.ini
app
pyproject.toml
requirements.txt
tests

docker run --rm linkbox:1.0 whoami
appuser

Obraz zawiera kod aplikacji i wymagane pliki, ale nie zawiera lokalnej konfiguracji .env, środowiska .venv ani bazy danych. Kontener działa jako appuser, a nie root.

## Notatka końcowa

- venv na maszynie izolował biblioteki Pythona od systemu, natomiast w kontenerze jest zbędny, bo sam kontener stanowi odizolowane środowisko i biblioteki są instalowane bezpośrednio w jego obrazie.

- Chcę widzieć appuser, a nie root, ponieważ proces aplikacji powinien działać z ograniczonymi uprawnieniami ze względów bezpieczeństwa.

- Narzędzia deweloperskie (pytest, ruff, black) nie powinny trafiać do obrazu produkcyjnego; na produkcji rozdzieliłbym zależności deweloperskie od produkcyjnych i instalował tylko te potrzebne do działania aplikacji.

### Z3

## Notaka startowa

jej dane wejściowe się nie zmieniły, używa starej warstwy zamiast wykonywać krok ponownie.

Jeśli zmieni się jeden krok, np. kopiowany plik, ta warstwa jest budowana od nowa i wszystkie kolejne też, bo każda następna warstwa bazuje na poprzedniej.

## Przewidywania

1. Nie — jeśli zależności są instalowane przed kopiowaniem kodu, zmiana komentarza unieważni tylko warstwę z kodem i kolejne, a instalacja zależności zostanie z cache.

2. Nie — jeśli zależności są instalowane przed kopiowaniem kodu, zmiana komentarza unieważni tylko warstwę z kodem i kolejne, a instalacja zależności zostanie z cache.

## Zadania

1. time docker build -t linkbox:1.0 . 
- real    0m0.961s
- user    0m0.044s
- sys     0m0.199s

2. time docker build -t linkbox:1.0 . (po dodaniu literki do komentarza)
- real    0m14.208s
- user    0m0.083s
- sys     0m1.211s

3. cp Dockerfile Dockerfile.zle

zminiłem kolejność:

FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home appuser

COPY --chown=appuser:appuser . .

RUN pip install --no-cache-dir -r requirements.txt

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python -m app"]

4. Dockerfile
- real    0m10.258s
- user    0m0.043s
- sys     0m0.182s

Dockerfile.zle
- real    0m45.760s
- user    0m0.097s
- sys     0m1.109s

### Z4

## Notatka startowa

EXPOSE → informacja/dokumentacja o porcie kontenera
-p → realnie udostępnia port kontenera przez port hosta

Czyli to -p otwiera drogę z zewnątrz, a EXPOSE tylko mówi, którego portu aplikacja używa.


127.0.0.1 w kontenerze to localhost kontenera, nie hosta; jeśli aplikacja słucha tylko tam, -p nie wystarczy, żeby udostępnić ją z zewnątrz.

## Przewidywania

1. Twoja wczorajsza usługa linkbox jest włączona do automatycznego startu i trzyma port 8000. Co się stanie, gdy uruchomisz kontener z -p 8000:8000?
Odp.: Nie uruchomi się poprawnie.

2. Kontener uruchomiony bez -p: curl http://127.0.0.1:8000/health z VM-ki — zadziała?
Odp.: Zadziała

3. Kontener uruchomiony z -p 8000:8000, aplikacja w środku z domyślną konfiguracją — curl z VM-ki zadziała?
Odp.: Nie zadziała

4. Ten sam kontener uruchomiony z -p 8080:8000 — curl z VM-ki na port 8080 zadziała? A przeglądarka na Windowsie pod tym portem?
Odp.: Nie zadziała

## Zadania

1. sudo systemctl stop linkbox (zatrzymałem usługe)
systemctl is-active linkbox (jest na inactive)
sudo ss -tlnp | grep ':8000' (nie ma komunikatu czyli jest wolny)

2. Bez -p kontener działał, ale curl z VM na 127.0.0.1:8000 nie zadziałał (Could not connect to server), ponieważ port kontenera nie był wystawiony na hosta.

3. Przy -p 8000:8000 połączenie dochodziło do kontenera, ale aplikacja słuchała tylko na 127.0.0.1 wewnątrz kontenera, więc curl zakończył się Connection reset by peer.

4. APP_HOST=127.0.0.1 oznacza, że aplikacja przyjmuje połączenia wyłącznie z tej samej maszyny — z innego komputera będzie niewidoczna
Wczoraj 127.0.0.1 oznaczał localhost całej VM, a dziś oznacza localhost wewnątrz kontenera, więc host nie może dostać się do aplikacji przez ten adres.

5. curl http://127.0.0.1:8000/health
{"status":"ok","database":"ok","version":"1.0.0"}

6. Could not connect to server

## Notatki końcowe

127.0.0.1 nadal oznacza localhost, ale teraz jest to localhost kontenera, a nie VM.

-p nie pomagało, bo po stronie kontenera łączył się ruch z interfejsu sieciowego, a aplikacja słuchała tylko na 127.0.0.1.

Są 2 przekierowania: Windows → VM i VM → kontener; 8000 działał, bo oba istniały, a dla 8080 brakowało przekierowania w VirtualBox.

### Z5 

## Notatki początkowe 

ENV ustawia domyślną wartość w obrazie, a -e ustawia ją przy uruchomieniu kontenera i ma wyższy priorytet. Wartości zależnych od środowiska nie zapisuje się w obrazie, żeby ten sam obraz działał w różnych środowiskach i nie przechowywał sekretów.

docker logs -f → śledzi na żywo stdout/stderr jednego kontenera.
journalctl -f → śledzi na żywo journal systemu/systemd, czyli logi usług i systemu hosta.

## Zadania

1. Kontenter linbox-main uruchomił sie w tle i przyją konfiguracje.

Logi: 
Uruchamiam aplikację linkbox-main w wersji 1.0.0
Nasłuchuję na 0.0.0.0:8000
CORS: WŁĄCZONY dla 1 origin-ów: http://localhost:3000

2. 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp

3. 2026-08-19T10:13:07+0000 INFO     [linkbox-main] uvicorn.access: 172.17.0.1:47836 - "POST /api/links HTTP/1.1" 201
curl wygenerował POST /api/links ze statusem 201, czyli link został utworzony poprawnie.

4. Mam 1 obraz linkbox:1.0 i 2 działające konteney. 1 obraz 2 kontenery

5. Kontener zakończył się błędem przez nieprawidłową wartość LOG_LEVEL=GADATLIWY znalazłem go przez docker ps -a, a przyczynę sprawdziałem poleceniem docker logs linkbox-zly-log

6. Posprzątałem poleceniami docker stop linkbox-drugi i rm linkbox-drugi

## Notatki końcowe

APP_PORT:
- docker run -e → zmienna w shellu / .env → systemd Environment= / EnvironmentFile= → ENV w obrazie.

Zatrzymany kontener nadal isnieje i ma logi, a usuniety znika razem ze swoim stanem i logami. 

### Z6

## Notatka początkow
docker stop - kontener przestaje działać, ale jego wartwa zapisywalna zostaje
docker start - uruchamiasz ten sam kontener, wiec jego wcześniejsze pliki nadal są
docker rm - kontener znika razem ze swoją wartą zapisywalną

Dwa kontenery mają wlasną osobną wartę zapisywalną !!!

## Przewidywania

1. Pod jaką ścieżką w kontenerze wyląduje plik links.db? Odpowiedz konkretną ścieżką, nie opisem.
Odp.: /tmp/links.db

2. Tworzysz link, zatrzymujesz kontener (docker stop) i uruchamiasz go z powrotem (docker start). Link będzie?
Odpl.: Tak link będzie

3. Tworzysz link, usuwasz kontener (docker rm) i uruchamiasz nowy z tego samego obrazu. Link będzie?
Odp.: Nie linku nie będzie 

4. Plik links.db, który leży od wczoraj na maszynie w ~/staz/aplikacja/api — ma z tym wszystkim cokolwiek wspólnego?
Odp.: Nie

## Zadania

1. [{"code":"7ZXdHj6","url":"https://example.com/2","clicks":0,"created_at":"2026-08-19T10:39:41.588811Z"},{"code":"5hZ2qEM","url":"https://example.com/1","clicks":0,"created_at":"2026-08-19T10:39:34.668145Z"},{"code":"a4gw93k","url":"https://example.com","clicks":0,"created_at":"2026-08-19T10:13:07.783591Z"}] - curl curl http://127.0.0.1:8000/api/links

2. docker exec linkbox-main ls -lh /tmp/links.db (-rw-r--r-- 1 appuser appuser 20K Aug 19 10:39 /tmp/links.db)

3. A /tmp/links.db

4. [{"code":"7ZXdHj6","url":"https://example.com/2","clicks":0,"created_at":"2026-08-19T10:39:41.588811Z"},{"code":"5hZ2qEM","url":"https://example.com/1","clicks":0,"created_at":"2026-08-19T10:39:34.668145Z"},{"code":"a4gw93k","url":"https://example.com","clicks":0,"created_at":"2026-08-19T10:13:07.783591Z"}]

5. Nowy kontener nowa warstwa zapisywania curl http://127.0.0.1:8000/api/links oddaje [] puste

6. Na VM ma date modyfikacji z 17 sierpnia wiec dzisiejsze operacje kontenerze go nie zmieniły

## Notatki końcowe

Trwałość: zmienna powłoki → tmpfs → warstwa kontenera → dysk.

Warstwa kontenera wygląda jak normalny dysk, ale znika po usunięciu kontenera.

docker rm -f usunął kontener razem z jego warstwą i danymi.

### Z7 

## Notatka startowa

Named volume → zwykle dane bazy i dane trwałe.
Bind mount → zwykle kod i pliki, które chcesz bezpośrednio współdzielić z hostem.

Problem wynika z uprawnień: wolumen może być widoczny jako katalog należący do root, a proces działa jako zwykły użytkownik. Rozwiązuje się to przez przygotowanie katalogu i jego właściciela w obrazie przed przejściem na USER.

## Zadania

1. docker volume create linkbox-data + -v linkbox-data:/data + DATABASE_URL=sqlite:////data/links.db.
2. Błąd: sqlite3.OperationalError: unable to open database file; naprawa: RUN mkdir -p /data && chown appuser:appuser /data.
3. Czas buildu: 1m31.988s, cache: 0 kroków.
4. Po docker rm -f i uruchomieniu nowego kontenera z tym samym wolumenem oba linki nadal były na liście.
5. docker volume inspect linkbox-data pokazuje Mountpoint; dane należą do Dockera i nie edytuje się ich ręcznie.
6. Kontener bez wolumenu ma własną bazę, więc lista linków jest pusta; po teście kontener usuwamy.

## Notatka końcowa

Montując wolumen, deklaruję, że dana ścieżka przestaje być częścią warstwy zapisywalnej kontenera.

Trwałość: zmienna powłoki → tmpfs → warstwa kontenera → wolumen → dysk hosta.

Po docker rm znika kontener i jego warstwa zapisywalna, ale wolumen zostaje; wiem to, bo po uruchomieniu nowego kontenera z tym samym wolumenem linki nadal były dostępne.

### Z8

## Notatka startowa

Compose.yaml - plik w którym opisuje cały zestaw kontenerów i ich konfiguracje
usługa - to opis jednego typu kontenera
image: - oznacza użyj gotowego obrazu
build: - oznacza zbuduj obraz z Dozkerfile z podanej lokazlizacji
Compose przenosi parametry uruchomienia do pliku 

docker compose up -d:
- czyta compose.yaml,
- w razie potrzeby buduje obrazy,
- tworzy sieci/wolumeny,
- tworzy i uruchamia kontenery,
- -d oznacza działanie w tle.

docker compose stop - zatrzymuje kontener

docker compose down - zatrzymuje kontener, usuwa kontenery, usuwa sieć utworzoną przez compose

Wytłumacz mi, skąd Docker Compose bierze nazwę projektu, gdy jej nie podam, i co ta nazwa zmienia w nazwach kontenerów, sieci i wolumenów. Co się dzieje, gdy odwołam się w pliku compose do wolumenu, który już istnieje na maszynie — czy Compose go użyje, czy utworzy własny? Jak się wskazuje ten istniejący? Odpowiadaj ogólnie.

## Zadania

1. stworzyłem compose.yaml
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

volumes:
  linkbox-data:
    external: true
    name: linkbox-data

2. docker compose up -d
docker compose ps
docker compose logs

3. docker volume ls
DRIVER    VOLUME NAME
local     linkbox-data

4. curl działa

5. Po docker compose down i ponownym docker compose up -d linki nadal były dostępne, ponieważ Compose usunął kontener i sieć, ale nie usunął wolumenu z bazą danych.

## Notatki końcowe

-p 8000:8000 - ports: "8000:8000"
-e APP_HOST=0.0.0.0 - environment: APP_HOST: 0.0.0.0
-e APP_PORT=8000 - environment: APP_PORT: 8000
-e CORS_ORIGINS=http://localhost:3000 - environment: CORS_ORIGINS: http://localhost:3000
-e APP_NAME=linkbox-compose - environment: APP_NAME: linkbox-compose
-e DATABASE_URL=sqlite:////data/links.db - environment: DATABASE_URL: sqlite:////data/links.db
-v linkbox-data:/data - volumes: linkbox-data:/data
--name - Compose nadał nazwę automatycznie: aplikacja-api-1
linkbox:1.0 - build: ./api
restart - restart: unless-stopped

docker compose down usuwa kontener i sieć, ale zostawia wolumen; docker compose down -v usuwa również wolumen i znajdujące się w nim dane. 

### Z9

## Notatki startowe

nginx: pliki /usr/share/nginx/html, port 80; bind mount udostępnia katalog hosta w kontenerze, a :ro blokuje zapis z kontenera.

systemd uruchamia Dockera, a Docker (dockerd) na podstawie zapisanej polityki restartu wznawia kontenery.

## Zadania

1. dopisałem nową usługę 

  web:
    image: nginx:1.27-alpine
    ports:
      - "3000:80"
    volumes:
      - ./web:/usr/share/nginx/html:ro
    restart: unless-stopped

2. docker compose up -d && docker compose ps

web i api są 

3. już były wyłączone

4. Po usunięciu CORS_ORIGINS użytkownik zobaczył komunikat Odpowiedź API zablokowana przez przeglądarkę (CORS) oraz brak listy linków. W konsoli przeglądarki pojawił się błąd braku pasującego nagłówka Access-Control-Allow-Origin.

## Notatka końcowa

zisiaj: systemd uruchamia Dockera, a restart: unless-stopped uruchamia kontenery.
Jutro: tak, front powinien wstać sam po uruchomieniu VM.

### Z10 

## Notatka startowa

docker compose config - ono pokazuje wynikową konfigurację, którą Compose faktycznie złożył: łączy pliki, podstawia zmienne i rozwija skrócone zapisy do pełniejszej postaci.

docker compose config pokazuje wynikową konfigurację po połączeniu plików i podstawieniu zmiennych; kilka plików Compose może się nakładać, a późniejsze ustawienia mogą nadpisywać wcześniejsze.

Na stronie: „Odpowiedź API zablokowana przez przeglądarkę (CORS)” oraz „Nie udało się pobrać listy — szczegóły w komunikacie powyżej.”

W konsoli: błąd CORS związany z brakiem pasującego nagłówka Access-Control-Allow-Origin.

## Przewidywanie

Przewidywanie: problem jest w ustawieniach CORS w API, bo API działa, ale przeglądarka blokuje odpowiedź dla strony z localhost:3000.

## Zadania

Problem 1
- Objaw: Front pokazuje „API nieosiągalne”, a curl zwraca Connection reset by peer.
- Hipoteza: API nasłuchuje na złym adresie.
- Sprawdzenie: docker compose logs api oraz docker compose config.
- Przyczyna: APP_HOST=127.0.0.1, więc API było dostępne tylko wewnątrz kontenera.
- Poprawka: zmiana na APP_HOST=0.0.0.0.

Problem 2
- Objaw: Po naprawieniu API działało, ale miało złą bazę danych i nie korzystało z wcześniejszych linków.
- Hipoteza: API korzysta z niewłaściwej ścieżki do bazy.
- Sprawdzenie: docker compose logs api oraz docker compose config.
- Przyczyna: DATABASE_URL=sqlite:////tmp/links.db zamiast bazy z wolumenu.
- Poprawka: zmiana na DATABASE_URL=sqlite:////data/links.db.

Problem 3
- Objaw: compose.yaml wyglądał poprawnie, ale docker compose config pokazywał inne wartości.
- Hipoteza: konfigurację nadpisuje drugi plik Compose.
- Sprawdzenie: ls -la compose* oraz sprawdzenie com.docker.compose.project.config_files.
- Przyczyna: compose.override.yaml nadpisywał APP_HOST i DATABASE_URL.
- Poprawka: poprawiłem wartości w compose.override.yaml.

Test końcowy
	Wykonałem:
		- docker compose down
		- docker compose up -d

	Po ponownym uruchomieniu front działał, API było zielone i wcześniejsze linki z wolumenu nadal były dostępne.

## Notatka końcowa

- Były 2 problemy: zły adres API (APP_HOST) z modułu sieć/porty i zła baza (DATABASE_URL) z modułu dane/wolumeny.
- Przełom dało docker compose config, bo pokazało, że compose.override.yaml nadpisuje mój compose.yaml.
- docker compose ps mówi tylko, że kontenery działają, ale nie że aplikacja w środku działa poprawnie i używa właściwych danych. 

## Trzy pytania

1. Dlaczego compose.override.yaml automatycznie nadpisuje compose.yaml?
2. Dlaczego 127.0.0.1 w kontenerze może być problemem?
3. Przy kolejnych zadaniach warto ograniczyć powtarzanie tematów związanych z CORS.


01101011 01101111 01101110 01101001 01100101 01100011 00100000 01000011 01001111 01010010 01010011
