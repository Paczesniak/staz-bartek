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


