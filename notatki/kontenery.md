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


