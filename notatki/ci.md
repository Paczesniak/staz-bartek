----- CI Pipeline -----

### Z1

## Notatka startowa

Trzzy narzędzia:
- pytest (czy kod robi to co ma robić. Uruchamia aplikacje w pamięci i sprawdza jej zachowanie)
- ruff (czy w kodzie nie ma błędów widocznych bez uruchamiania: nieużytych importów, literówek w nazwach, typowych pułapek)
- black (czy kod jest zapisany w jednolitym stylu. Nie ocenia poprawności tylko wygląd i robi to bezdyskusyjnie żeby nikt nie tracił czasu na spory o wcięcia)

Testy jednostkowe sprawdzają, czy kod działa poprawnie logicznie.
Linter sprawdza, czy kod nie ma podejrzanych błędów, złych praktyk albo problemów stylistycznych.
Formatter tylko układa kod w jednolity sposób.

Środowisko wirtualne w Pythonie to po prostu oddzielne miejsce na pakiety dla konkretnego projektu.

Przykład: projekt A może używać pytest 8, a projekt B starszej wersji. Dzięki środowiskom wirtualnym te pakiety się nie mieszają i nie rozwalają sobie nawzajem zależności.

Dlatego narzędzia typu:
- pytest
- ruff
- black
- flake8

## Zadania

1. cd ~/staz/aplikacja/api
source .venv/bin/activate
pip install -r requirements.txt

Środowisko zostało  przygotowane.

2. Testy:
- python -m pytest (48 passed, 1 worning in 1.70s)
- python -m ruff check . (All chcecks passed!)
- python -m black --check . (All done! 24 files would be left unchanged)

3. Kod wyjścia:  echo $?
- python -m pytest (0)
- python -m ruff check . (0)
- python -m black --check . (0)

4. echo 'import os, sys' >> app/config.py

Błędy: E401 [*] Multiple imports on one line
Found 5 errors.

Po komendzie echp $? = 1. 

5. git checkout -- app/config.py (przywraca plik config.py do wersji z ostatniego commita)

## Notatka Końcowa

1. Trzy wyniki z punktu 2 i trzy kody wyjścia z punktu 3.
- pytest (48 passed, 1 warning in 1.28s. Kod wyjścia 0)
- ruff (All checks passed! Kod wyjścia 0)
- black (24 files would be left unchanged. Kod wyjścia 0)

2. Po celowym zepsuciu app/config.py:
- ruff zgłosił m.in. E401 Multiple imports on one line oraz F401 imported but unused
- kod wyjścia: 1

3. Program wywołujący te narzędzia wie, czy sprawdzenie się powiodło, po kodzie wyjścia procesu: 0 oznacza sukces, a wartość różna od 0 oznacza błąd.

### Z2 

## Notatka startowa

et -Eeuo pipefail (włącza w Bashu kilka zasad, które sprawiają, że skrypt szybciej ujawnia błędy zamist lecieć dalej:
- -E (błędy z ERR są dziedziczone
- -e (przerwie po błędzie)
- -u (błąd przy niezdefiniowanej zmiennej)
- pipedail (wykryj błąd w całym potoku, nie tylko końcu)

Można zrobić licznik błędów i nie używać set -e do tych sprawdzeń, przykład: 

!/usr/bin/env bash

errors=0

python -m pytest || ((errors++))
python -m ruff check . || ((errors++))
python -m black --check . || ((errors++))

if (( errors > 0 )); then
    echo "Nieudane sprawdzenia: $errors"
    exit 1
fi

echo "Wszystkie sprawdzenia przeszły"
exit 0

Jak w skrypcie bash sprawdzić, czy jestem w katalogu, którego się spodziewam, i jak sprawić, żeby skrypt działał niezależnie od tego, z którego katalogu go uruchomiono?
Odp.:

!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

albo jeśli dodatkowo chce sprawdzać czy jestem w oczekiwanym katalogu:

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f "pyproject.toml" ]]; then
    echo "Błąd: zły katalog"
    exit 1
fi

## Zadania

1.   GNU nano 8.7.1                                            sprawdz.sh
!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$ROOT_DIR/aplikacja/api"

cd "$API_DIR"

errors=0

echo "Test pytest: "
if python -m pytest; then
        echo "Ok: pytest"
else
        echo "Zle: pytest"
        ((errors+=1))
fi

echo
echo "Test ruff: "
if python -m ruff check .; then
    echo "OK: ruff"
else
    echo "Zle: ruff"
    ((errors+=1))
fi

echo
echo "Test black: "
if python -m black --check .; then
    echo "OK: black"
else
    echo "Zle: black"
    ((errors+=1))
fi

echo

if (( errors > 0 )); then
        echo "Nieudane sprawdzenie: $errors"
        exit 1
fi

echo "Wszystkie sprawdzenia poszły"
exit 0

2. chmod +x sprawdz.sh

3. (.venv) bartek@ubuntu:~/staz$ ./sprawdz.sh
Test pytest:
................................................                                                                    [100%]
==================================================== warnings summary =====================================================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  /home/bartek/staz/aplikacja/api/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
48 passed, 1 warning in 1.19s
Ok: pytest

Test ruff:
All checks passed!
OK: ruff

Test black:
All done! ✨ 🍰 ✨
24 files would be left unchanged.
OK: black

Wszystkie sprawdzenia poszły
(.venv) bartek@ubuntu:~/staz$ echo $?
0

Na lokalizaci /tmp też działa. Po zrobieniu specjalnie błędów znalazło te błędy i wszystko działa tak jak powinno. 

4. sudo apt install shellcheck (bo nie było go)

shellcheck sprawdz.sh (nic nie wyświetlił czyli nie ma problemu)

## Notatka końcowa

1. Skrypt: 

!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$ROOT_DIR/aplikacja/api"

cd "$API_DIR"

errors=0

echo "Test pytest:"
if python -m pytest; then
    echo "OK: pytest"
else
    echo "Zle: pytest"
    ((errors+=1))
fi

echo
echo "Test ruff:"
if python -m ruff check .; then
    echo "OK: ruff"
else
    echo "Zle: ruff"
    ((errors+=1))
fi

echo
echo "Test black:"
if python -m black --check .; then
    echo "OK: black"
else
    echo "Zle: black"
    ((errors+=1))
fi

echo

if (( errors > 0 )); then
    echo "Nieudane sprawdzenia: $errors"
    exit 1
fi

echo "Wszystkie sprawdzenia poszly"
exit 0

2. Kody wejścia: 
- zielony przebieg: 0
- czerwony przebieg: 1

3. Skrypt wykonuje wszystkie trzy sprawdzenia, a nie zatrzymuje się na pierwszym błędzie, bo zlicza błędy i dopiero na końcu zwraca kod 1.

4. ShellCheck nie zgłosił żadnych błędów ani ostrzeżeń

### Z3

## Notatka startowa

1. Plik workflow GitHub Actions to plik YAML, który mówi GitHubowi kiedy coś uruchomić i co dokładnie ma zrobić.
2. actions/checkout (pobiera kod Twojego repozytorium na maszynę GitHub Actions. Bez tego runner nie będzie miał Twoich plików, więc np. pytest nie znajdzie projektu)
actions/setup-python (instaluje/ustawia wybraną wersję Pythona na runnerze)
3. Job kończy się niepowodzeniem, gdy któryś wymagany krok zwróci kod wyjścia różny od 0.

## Zadania

1. Repozytorium:

name: CI

on:
  push:

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - name: Pobranie kodu
        uses: actions/checkout@v4

      - name: Ustawienie Pythona
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"

      - name: Instalacja zależności
        run: pip install -r aplikacja/api/requirements.txt

      - name: Uruchomienie sprawdzen
        run: ./sprawdz.sh

Wytłumaczenie: 
- name: CI (nazwa wordkflow)
- on: push: (kiedy ma sie uruchomić)
- jobs: (lista zadań)
- check: (sprawdzenie projektu)
- runs-on: ununtu-latest (uruchamienie świeżej maszyny z najnowszym ubuntu)
- steps: (kroki zadań i kolejność)
- name: Pobranie kodu
        uses: actions/checkout@v4 
(pobiera repo na maszyne GitHub)
- name: Ustawienie Pythona
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"
(przygotowywuje pythona w wersji 3.14)
- name: Instalacja zależności
        run: pip install -r aplikacja/api/requirements.txt
(wykonuje komende terminalowa i instaluje biblioteki potrzebne do aplikacji)
- name: Uruchomienie sprawdzen
        run: ./sprawdz.sh
(uruchamia skrypt sprawdz.sh który odpala pytest, ruff, black)

2. git add .github/workflows/ci.yml sprawdz.sh
git commit -m "Dodanie CI GitHub Actions"
git push

3. Jest na github

4. Cały przebieg trwał 26 sekund.
Job check trwał 22 sekundy.
Workflow zakończył się statusem Success.
Potrzebne było 1 podejście.
Nie było błędu powodującego zatrzymanie workflow.
GitHub pokazał tylko ostrzeżenie o tym, że Node.js 20 jest deprecated dla jednej z użytych akcji, ale nie wpłynęło to na wynik.

## Notatka końcowa

1. Plik ci.yml

name: CI

on:
  push:

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - name: Pobranie kodu
        uses: actions/checkout@v4

      - name: Ustawienie Pythona
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"

      - name: Instalacja zależności
        run: pip install -r aplikacja/api/requirements.txt

      - name: Uruchomienie sprawdzen
        run: ./sprawdz.sh

2. Czas przebiegu: 26 sekund. Job check: 22 sekundy. Najdłuższy krok wpisz zgodnie z widokiem po rozwinięciu joba check — na pokazanym screenie nie widać czasów poszczególnych kroków.

3. Czerwonych przebiegów nie było — pipeline przeszedł poprawnie za pierwszym podejściem.

4. Maszyna GitHub Actions jest tymczasowym, świeżym runnerem Ubuntu i nie ma mojej konfiguracji VM, moich lokalnych plików spoza repozytorium ani wcześniej zainstalowanych przeze mnie programów i zależności.

### Z4

## Notatka startowa

Sekrety w GitHub Actions to poufne wartości, np. hasła, tokeny API, klucze dostępu albo dane logowania do bazy.

Ustawiasz je w repozytorium na GitHubie w:
Settings → Secrets and variables → Actions → New repository secret

Potem w workflow używasz ich tak:
env:
  DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}

Nie potrzebujesz sekretów, jeśli workflow tylko pobiera publiczny kod, instaluje zależności i uruchamia testy/lintery bez żadnych prywatnych danych.

Testy na bazie w pamięci tworzą sobie tymczasową bazę podczas uruchomienia, więc nie potrzebują osobnego Postgresa, hasła ani DATABASE_URL.
Zaleta: są szybkie, proste i niezależne od środowiska.
Cena: nie sprawdzą, czy aplikacja naprawdę potrafi połączyć się z PostgreSQL, czy konfiguracja bazy jest poprawna ani czy występują różnice między bazą testową a prawdziwą bazą.

## Zadnia

1. Przewidywania:
- czy CI ma dostęp do twojego pliku .env
Odp.: CI nie ma dostępu do mojego lokalnego pliku .env, bo ten plik nie jest w repozytorium.
- czy testy w CI łączą się z twoją bazą Postgresa,
Odp.: Testy w CI nie łączą się z moim PostgreSQL, tylko używają własnej bazy testowej.
- co się stanie, jeśli usuniesz requirements.txt z repozytorium i wypchniesz.
Odp.: Gdybym usunął requirements.txt i zrobił push, workflow wywaliłby się przy instalacji zależności, bo pliku nie byłoby w repozytorium.

2. Run pip install -r aplikacja/api/requirements.txt
Successfully installed

3. IN_MEMORY_DATABASE_URL = "sqlite://"

4. Wywalił by się na kroku Instalacja zależności czyli przy poleceniu pip install -r aplikacja/api/requirements.txt
w logu pojawiło by sie:

ERROR: Could not open requirements file:
[Errno 2] No such file or directory: 'aplikacja/api/requirements.txt'

## Notatka końcowa

1. Przewidywałem, że CI nie ma dostępu do mojego lokalnego pliku .env — potwierdziło się. Przewidywałem, że testy w CI nie łączą się z PostgreSQL, tylko używają bazy testowej — potwierdziło się. Przewidywałem, że bez requirements.txt pipeline wywaliłby się na kroku instalacji zależności z błędem braku pliku — to wynika bezpośrednio z polecenia pip install -r aplikacja/api/requirements.txt.
2. IN_MEMORY_DATABASE_URL = "sqlite://"
3. Pipeline sprawdza pytest, ruff i black. Nie sprawdza prawdziwego Postgresa, .env ani działania całego systemu w Docker Compose.



