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

