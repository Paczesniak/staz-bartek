# CI — niech sprawdza się samo

**To jedyny dokument, który dziś czytasz.** Zadania są w kolejności wykonania, pogrupowane w moduły.

## Cel dnia

Przez cztery dni sprawdzałeś wszystko ręcznie: uruchamiałeś aplikację i patrzyłeś, czy wstała; wchodziłeś na front i patrzyłeś, czy lista się ładuje; czytałeś log i szukałeś linii, która mówi, co poszło nie tak.

To działa dokładnie tak długo, jak długo pamiętasz o sprawdzeniu. W zespole, w którym pracuje pięć osób, nie pamięta nikt — i dlatego sprawdzanie przenosi się na maszynę, która robi to za każdym razem, przy każdej zmianie, bez wyjątków i bez litości.

Dziś budujesz to sprawdzanie. Najpierw **u siebie** — jednym skryptem, który uruchamiasz przed commitem. Potem **na GitHubie** — tym samym skryptem, który uruchamia się sam po każdym `git push`. Na koniec dokładasz to, czego żadne testy jednostkowe nie złapią: budowanie obrazu i sprawdzenie, czy aplikacja w nim w ogóle wstaje.

Trzy rzeczy z tego tygodnia wracają dziś po raz ostatni:

- **Kod wyjścia to nie ozdoba.** W F1 zobaczyłeś, że `$?` mówi, czy polecenie się udało. Dziś ten jeden bajt decyduje o tym, czy pipeline jest zielony, czy czerwony — i czy twoja zmiana w ogóle wejdzie do projektu.
- **To, co masz u siebie, nie jest tym, co ma projekt.** Twoje `.env` z hasłem nie jest w repozytorium (i dobrze). CI dostaje **tylko to, co jest w repozytorium** — i to jest najuczciwszy test, czy projekt da się w ogóle uruchomić komuś innemu.
- **Obraz z konkretnym tagiem, zależności z przypiętą wersją.** Przez cały tydzień powtarzałem to jak zdartą płytę. Dziś zobaczysz, po co: CI buduje wszystko od zera, na czystej maszynie, i to on pierwszy zapłaci za każde „a u mnie działa".

## Zasady

- **Notatki idą do `notatki/ci.md`.** Na starcie: `export NOTATKI=~/staz/notatki/ci.md`.
- **Commituj po każdym module.** Dziś to nie jest tylko dobra praktyka — każdy push uruchamia pipeline, więc commity są częścią ćwiczenia.
- **Ostatni dzień stażu.** Ostatni moduł to retro: co zostaje po tym tygodniu i co robisz dalej. Potraktuj go poważnie, bo to jedyna część, którą zabierzesz ze sobą w całości.

## Zanim zaczniesz

### 1. Materiały

    cd ~/staz
    git pull
    ./zainstaluj.sh

### 2. Sprawdź, że wczorajszy stos stoi

    cd ~/staz/aplikacja
    docker compose ps
    curl -s http://127.0.0.1:8000/health

Dziś nie będziesz go dużo używał, ale w module `obraz` przyda się jako punkt odniesienia.

### 3. Ustaw dzień

    lab dzien ci
    lab moduly

## Jak wygląda dzień

    lab start <moduł>
    lab grade <moduł>
    lab koniec <moduł>

**O czasach.** Suma zadań to **210 minut**. Ostatni dzień jest krótszy — resztę czasu zostawiamy na obronę i rozmowę.

**Czego `lab grade` NIE robi dzisiaj:** nie sprawdza, czy twój pipeline świeci na GitHubie na zielono. Nie ma jak — działa na twojej maszynie, a Actions działa u nich. Sprawdza to, co ma pod ręką: czy skrypt istnieje i naprawdę wyłapuje błędy, czy plik workflow jest poprawny i ma to, co trzeba, czy commit jest wypchnięty. **Zielony pipeline pokazujesz mi na obronie** — wtedy razem zajrzymy w zakładkę Actions.

---

## Moduł: lokalnie — 45 min

    lab start lokalnie

### Z1. Trzy narzędzia, które już masz — 15 min

#### O co tu chodzi

W repozytorium, które dostałeś w poniedziałek, są 48 testów, konfiguracja lintera i formatera. Do tej pory ich nie uruchamiałeś — dziś zaczynasz od zobaczenia, co każde z tych narzędzi mówi.

Trzy narzędzia sprawdzają trzy różne rzeczy i **żadne nie zastępuje pozostałych**:

- **pytest** — czy kod robi to, co ma robić. Uruchamia aplikację w pamięci i sprawdza jej zachowanie.
- **ruff** — czy w kodzie nie ma błędów widocznych bez uruchamiania: nieużytych importów, literówek w nazwach, typowych pułapek.
- **black** — czy kod jest zapisany w jednolitym stylu. Nie ocenia poprawności, tylko wygląd — i robi to bezdyskusyjnie, żeby nikt nie tracił czasu na spory o wcięcia.

#### Czego potrzebujesz

> Wytłumacz mi różnicę między **testami jednostkowymi**, **linterem** a **formaterem** kodu. Co wykrywa każde z tych narzędzi, czego żadne z nich nie wykryje, i dlaczego w projektach uruchamia się wszystkie trzy zamiast jednego.

> Wytłumacz mi, co to jest **środowisko wirtualne** w Pythonie i dlaczego narzędzia deweloperskie instaluje się w nim, a nie globalnie w systemie. Jak sprawdzić, czy jestem w aktywnym środowisku wirtualnym?

#### Zadanie

1. Wejdź do katalogu z API i przygotuj sobie środowisko (jeśli twoje `.venv` z poniedziałku jeszcze jest, po prostu je aktywuj):

       cd ~/staz/aplikacja/api
       source .venv/bin/activate     # albo utwórz na nowo: python3 -m venv .venv
       pip install -r requirements.txt

2. Uruchom po kolei i **zapisz ostatnią linię wyniku każdego**:

       python -m pytest
       python -m ruff check .
       python -m black --check .

3. Po każdym z nich sprawdź kod wyjścia i zapisz go:

       echo $?

4. Zepsuj coś na chwilę — dopisz na końcu `app/config.py` linię `import os, sys` (nieużyty import, w jednej linii dwa moduły) i uruchom `ruff` jeszcze raz. Zapisz, co powiedział i **jaki był kod wyjścia**.
5. Cofnij zmianę (`git checkout -- app/config.py`) i sprawdź, że `ruff` znów jest zielony.

**Do notatek:**

- Trzy wyniki z punktu 2 i trzy kody wyjścia z punktu 3.
- Komunikat lintera z punktu 4 i jego kod wyjścia.
- Jedno zdanie: skąd program wywołujący te narzędzia (za chwilę napiszesz taki skrypt) **wie**, czy sprawdzenie się powiodło.

**Sprawdź się:** `lab grade lokalnie`

### Z2. Jeden skrypt zamiast trzech poleceń — 30 min

#### O co tu chodzi

Trzy polecenia, które przed chwilą wpisałeś, to za dużo. Za dużo do zapamiętania, za dużo do wpisania przed każdym commitem, i — co najważniejsze — **za dużo, żeby dwie osoby uruchomiły dokładnie to samo**.

Napiszesz skrypt, który uruchamia wszystkie trzy i kończy się **niezerowym kodem wyjścia, jeśli którekolwiek zawiodło**. Ten sam skrypt uruchomi za chwilę GitHub. To jest sedno dzisiejszego dnia: **CI nie jest osobnym zestawem sprawdzeń — CI to twój skrypt, uruchamiany przez kogoś innego.**

Uwaga na jedną rzecz, o którą łatwo się potknąć: jeśli skrypt ma `set -e`, to **pierwszy** błąd go przerwie i nie zobaczysz pozostałych. Czasem tego właśnie chcesz, a czasem wolisz zobaczyć wszystkie problemy naraz. Zdecyduj świadomie i zapisz w notatkach, którą wersję wybrałeś i dlaczego.

#### Czego potrzebujesz

> Wytłumacz mi, co robią kolejno opcje w `set -Eeuo pipefail` w skrypcie bash: `-E`, `-e`, `-u`, `-o pipefail`. Dla każdej podaj przykład błędu, który dzięki niej wychodzi na jaw.

> Jak w skrypcie bash uruchomić kilka sprawdzeń tak, żeby **wszystkie** się wykonały, ale skrypt na końcu i tak zwrócił błąd, jeśli choć jedno zawiodło? Pokaż wzorzec ze zliczaniem błędów i wytłumacz, jak działa.

> Jak w skrypcie bash sprawdzić, czy jestem w katalogu, którego się spodziewam, i jak sprawić, żeby skrypt działał niezależnie od tego, z którego katalogu go uruchomiono?

#### Zadanie

1. Napisz skrypt `~/staz/sprawdz.sh`, który:
   - ma `set -Eeuo pipefail`,
   - działa niezależnie od katalogu, z którego go uruchomiono,
   - uruchamia **wszystkie trzy** narzędzia (pytest, ruff, black) na katalogu `aplikacja/api`,
   - wypisuje czytelnie, które sprawdzenie przeszło, a które nie,
   - kończy się kodem `0`, gdy wszystko przeszło, i kodem **różnym od zera**, gdy cokolwiek zawiodło.
2. Nadaj mu prawo wykonywania (`chmod +x`).
3. Sprawdź, że działa **w obie strony**:
   - uruchom na czystym kodzie → ma być zielony, `echo $?` ma dać `0`,
   - zepsuj coś (jak w Z1 punkt 4) → ma być czerwony, `echo $?` ma dać coś innego niż `0`,
   - cofnij zmianę → znów zielony.
4. Uruchom `shellcheck sprawdz.sh` (zainstaluj, jeśli trzeba: `sudo apt install shellcheck`) i napraw, co zgłosi.

**Do notatek:**

- Wklej skrypt.
- Zapisz oba kody wyjścia z punktu 3 (zielony i czerwony przebieg).
- Jedno zdanie: czy twój skrypt zatrzymuje się na pierwszym błędzie, czy wykonuje wszystkie sprawdzenia — i dlaczego tak zdecydowałeś.
- Jedno zdanie: co zgłosił `shellcheck` (jeśli nic — napisz to wprost).

**Sprawdź się:** `lab grade lokalnie`, potem `lab koniec lokalnie`

---

## Moduł: pipeline — 50 min

    lab start pipeline

### Z3. Ten sam skrypt, cudza maszyna — 35 min

#### O co tu chodzi

GitHub Actions działa tak: w repozytorium leży plik opisujący, **co** ma się uruchomić i **kiedy**. Po każdym pushu GitHub czyta ten plik, wstaje mu czysta maszyna wirtualna, klonuje na nią twoje repozytorium i wykonuje kroki, które w tym pliku opisałeś.

Słowo „czysta" jest tu najważniejsze. Ta maszyna nie ma twojego `.venv`, twojego `.env`, twojej bazy ani niczego, czego nie ma w repozytorium. Jeśli twój projekt da się uruchomić **tylko u ciebie**, dowiesz się o tym w ciągu dwóch minut od pierwszego pusha.

#### Czego potrzebujesz

> Wytłumacz mi budowę pliku workflow GitHub Actions: co robią sekcje `on:`, `jobs:`, `runs-on:`, `steps:`. Jaka jest różnica między krokiem `uses:` a `run:`? Gdzie w repozytorium musi leżeć ten plik, żeby GitHub go zauważył?

> Wytłumacz mi, co robią akcje `actions/checkout` i `actions/setup-python`. Co dokładnie się stanie, jeśli pominę pierwszą z nich?

> Wytłumacz mi, co znaczy, że job w GitHub Actions „zakończył się niepowodzeniem". Skąd GitHub wie, że krok się nie udał?

#### Zadanie

1. Utwórz w repozytorium plik `.github/workflows/ci.yml`. Ma:
   - uruchamiać się przy każdym `push`,
   - działać na `ubuntu-latest`,
   - pobrać kod (`actions/checkout`),
   - przygotować Pythona w wersji zgodnej z tą, której używasz (`actions/setup-python`),
   - zainstalować zależności z `aplikacja/api/requirements.txt`,
   - uruchomić **twój skrypt** `sprawdz.sh` — nie trzy osobne polecenia.
2. Zacommituj i wypchnij.
3. Wejdź na GitHuba, w zakładkę **Actions** twojego repozytorium. Obserwuj przebieg **na żywo** — rozwiń kroki i czytaj log tak samo, jak czytałeś log aplikacji: od góry.
4. Zapisz, ile trwał cały przebieg i który krok zajął najwięcej czasu.
5. Jeśli jest czerwony — czytaj log, popraw, commituj, pushuj. **To jest normalna część tego zadania**, nie porażka. Zapisz, ile podejść potrzebowałeś i na czym się wywalało.

**Do notatek:**

- Wklej plik `ci.yml`.
- Czas przebiegu i najdłuższy krok.
- Jeśli były czerwone przebiegi: co je powodowało, po kolei.
- Jedno zdanie: czym różni się maszyna, na której zadziałał twój pipeline, od twojej VM-ki — wymień trzy rzeczy, których tam nie ma.

**Sprawdź się:** `lab grade pipeline`

### Z4. 🔮 Czego CI nie widzi — 15 min

#### O co tu chodzi

Wczoraj schowałeś hasło do bazy w pliku `.env`, którego nie ma w repozytorium. Dziś twój pipeline uruchamia testy — i przechodzą. Warto zrozumieć, dlaczego, bo to samo pytanie wróci przy każdym projekcie: **skąd CI ma wziąć hasła, klucze i adresy, skoro nie ma ich w repo?**

#### Czego potrzebujesz

> Wytłumacz mi, czym są **sekrety** w GitHub Actions: gdzie się je ustawia, jak używa w workflow i dlaczego nie da się ich odczytać z logu przebiegu. Kiedy projekt ich potrzebuje, a kiedy nie?

> Dlaczego testy, które działają na bazie w pamięci, nie potrzebują żadnej konfiguracji ani działającej bazy danych? Jaka jest w tym zaleta i jaka jest cena — czego takie testy NIE sprawdzą?

#### Zadanie

1. **Przewidywanie, do notatek, przed sprawdzeniem.** Odpowiedz z głowy, bez zaglądania:
   - czy CI ma dostęp do twojego pliku `.env`,
   - czy testy w CI łączą się z twoją bazą Postgresa,
   - co się stanie, jeśli usuniesz `requirements.txt` z repozytorium i wypchniesz.
2. Sprawdź pierwsze dwa punkty w logu przebiegu — poszukaj kroku instalacji zależności i kroku z testami.
3. Zajrzyj do `aplikacja/api/tests/conftest.py` i znajdź linię mówiącą, jakiej bazy używają testy. Zapisz ją.
4. **Nie sprawdzaj punktu trzeciego przez usunięcie pliku.** Zamiast tego napisz, jak wyglądałby log przebiegu — na którym kroku i z jakim komunikatem by się wywalił.

**Do notatek:**

- Twoje trzy przewidywania i to, co się z nich potwierdziło.
- Linia z `conftest.py`.
- Dwa zdania: co twój pipeline sprawdza **naprawdę**, a czego nie sprawdza wcale — mimo że świeci na zielono.

**Sprawdź się:** `lab grade pipeline`, potem `lab koniec pipeline`

---

## Moduł: czerwony — 40 min

    lab start czerwony

### Z5. Zepsuty build — 40 min

#### O co tu chodzi

Pipeline, który zawsze świeci na zielono, jest bezużyteczny — nie wiadomo, czy cokolwiek sprawdza. Wartość ma dopiero taki, który **czerwieni się wtedy, kiedy trzeba**, i mówi wprost, co jest nie tak.

`lab start czerwony` zmienił coś w kodzie aplikacji. Nie mówię ci, co ani ile rzeczy. Twoje zadanie: doprowadzić do zielonego przebiegu — **z sensowną poprawką, nie przez wyłączenie sprawdzenia**.

To ostatnia awaria w tym stażu i jedyna, która dotyczy kodu, a nie konfiguracji.

#### Czego potrzebujesz

> Jak czytać log nieudanego przebiegu w GitHub Actions: gdzie szukać pierwszego błędu, dlaczego ostatnie linie logu bywają mylące i czym różni się błąd narzędzia od błędu samego workflow?

> Wytłumacz mi, czym różni się naprawienie błędu zgłoszonego przez lintera od **wyciszenia** go (np. przez `# noqa`). Kiedy wyciszenie jest uzasadnione, a kiedy jest oszustwem wobec samego siebie?

#### Zadanie

1. Uruchom **najpierw lokalnie** swój skrypt: `./sprawdz.sh`. Zapisz, co zgłosił i jaki był kod wyjścia.
2. Zdiagnozuj i napraw. Uwaga: sprawdzenia są trzy i wada niekoniecznie dotyczy tylko jednego z nich.
3. Uruchom skrypt lokalnie jeszcze raz — ma być zielony, zanim cokolwiek wypchniesz. **Tak się z tego korzysta**: lokalny skrypt istnieje po to, żeby czerwony pipeline był rzadkością, a nie codziennością.
4. Zacommituj, wypchnij, obejrzyj przebieg w Actions.
5. Porównaj: ile czasu zajęło ci znalezienie problemu lokalnie, a ile zajęłoby czekanie na wynik z CI przy każdej próbie.

**Do notatek — raport w tym samym formacie, co wczoraj:**

- **Objaw:** co dokładnie zgłosiło które narzędzie (wklej fragment).
- **Przyczyna:** co było zmienione w kodzie.
- **Naprawa:** co zrobiłeś — i dlaczego akurat tak, a nie przez wyciszenie.
- **Weryfikacja:** lokalnie i w CI.
- Jedno zdanie: co byś stracił, gdybyś nie miał lokalnego skryptu i musiał czekać na CI po każdej próbie.

**Sprawdź się:** `lab grade czerwony`, potem `lab koniec czerwony`

---

## Moduł: obraz — 40 min

    lab start obraz

### Z6. CI buduje obraz — 40 min

#### O co tu chodzi

Testy jednostkowe sprawdzają kod. Nie sprawdzają, czy **da się z niego zbudować obraz**, czy ten obraz **wstaje**, i czy aplikacja w nim odpowiada. A to są dokładnie te rzeczy, które psują się między środą a piątkiem: ktoś dopisze zależność i zapomni o `requirements.txt`, ktoś zmieni ścieżkę i `Dockerfile` przestaje trafiać w kod.

Dokładasz do pipeline'u drugi job, który buduje obraz — ten sam `Dockerfile`, który napisałeś w środę — uruchamia go i puka do `/health`. To jest **smoke test**: nie sprawdza, czy aplikacja działa dobrze, tylko czy w ogóle wstaje.

#### Czego potrzebujesz

> Wytłumacz mi, jak w GitHub Actions zdefiniować drugi job i jak sprawić, żeby uruchomił się dopiero po pierwszym (`needs:`). Kiedy warto puścić joby równolegle, a kiedy szeregowo?

> Czy na maszynie `ubuntu-latest` w GitHub Actions jest dostępny Docker? Czy trzeba go instalować? Jak zbudować obraz z `Dockerfile` leżącego w podkatalogu repozytorium?

> Wytłumacz mi, czym jest **smoke test** i czym różni się od testu jednostkowego i od testu end-to-end. Jak w skrypcie poczekać, aż uruchomiona w tle usługa zacznie odpowiadać, zamiast po prostu spać 30 sekund?

#### Zadanie

1. Dodaj do `ci.yml` drugi job, który:
   - uruchamia się **po** jobie z testami (`needs:`),
   - buduje obraz z twojego `Dockerfile` (`aplikacja/api`), nadając mu jakiś tag,
   - uruchamia kontener z tego obrazu w tle, z portem wystawionym na maszynę,
   - **czeka**, aż `/health` zacznie odpowiadać (pętla z ograniczeniem liczby prób, nie `sleep 30`),
   - sprawdza, że `/health` zwraca kod 200, i kończy się błędem, jeśli nie,
   - na koniec zatrzymuje kontener.
2. Uwaga na jedną rzecz, którą już znasz: aplikacja domyślnie nasłuchuje na `127.0.0.1`, a to wewnątrz kontenera oznacza jego samego. Przypomnij sobie, jak rozwiązałeś to w środę.
3. Druga uwaga: kontener wystartuje z pustą, domyślną bazą (SQLite w środku kontenera) — i tak ma być. To smoke test, nie test danych.
4. Wypchnij i obejrzyj oba joby w Actions.

**Do notatek:**

- Wklej job budujący obraz.
- Jedno zdanie: dlaczego czekanie w pętli jest lepsze niż `sleep 30` — podaj oba powody (jeden dotyczy czasu, drugi niezawodności).
- Jedno zdanie: co ten job wyłapie, czego nie wyłapią testy jednostkowe. Podaj konkretny przykład błędu.
- Jedno zdanie: dlaczego drugi job ma `needs:` na pierwszym, zamiast lecieć równolegle.

**Sprawdź się:** `lab grade obraz`, potem `lab koniec obraz`

---

## Moduł: zamkniecie — 35 min

    lab start zamkniecie

### Z7. Retro i zamknięcie stażu — 35 min

#### O co tu chodzi

Ostatnie zadanie. Nie ma w nim nic do naprawienia — jest do napisania.

Za tydzień pamięta się z takiego tygodnia trzy rzeczy i wszystkie trzy są przypadkowe. Za to notatka napisana teraz, na świeżo, zostaje w całości i jest tym, co realnie zabierasz ze sobą.

#### Zadanie

1. Uporządkuj `notatki/ci.md` — zwykłe sekcje z dnia, tak jak w poprzednie dni.

2. Załóż w repozytorium plik `RETRO.md` i odpowiedz w nim na sześć pytań. Pisz konkretnie — „było ciekawie" nie jest odpowiedzią:

   **1. Co potrafisz dziś, czego nie potrafiłeś w poniedziałek?** Wymień pięć rzeczy. Przy każdej dopisz zadanie, po którym to poczułeś.

   **2. Które zadanie było najtrudniejsze i dlaczego?** Nie chodzi o najdłuższe — o takie, przy którym najdłużej nie wiedziałeś, co się dzieje.

   **3. Gdzie straciłeś najwięcej czasu i co byś zrobił inaczej?** Miałeś w tym tygodniu przynajmniej jedno miejsce, w którym siedziałeś godzinami. Nazwij je i napisz, co dziś zrobiłbyś od razu.

   **4. Czego nadal nie rozumiesz?** Minimum trzy rzeczy. To jest najważniejsze pytanie w całym retro i jedyne, na które nie ma złej odpowiedzi poza „wszystko rozumiem".

   **5. Jak korzystałeś z AI i co byś zmienił?** Konkretnie: kiedy pomogło, kiedy zaprowadziło cię w ślepą uliczkę, i po czym poznawałeś różnicę.

   **6. Co robisz dalej?** Trzy rzeczy, które chcesz umieć za trzy miesiące, i pierwszy krok do każdej z nich. Ten pierwszy krok ma być tak mały, żebyś mógł go zrobić w najbliższy weekend.

3. Zajrzyj do katalogu `dodatkowe/` w repozytorium — są tam trzy tematy, których nie zdążyliśmy zrobić: **reverse proxy**, **monitoring** i **awarie**. Są napisane tak, żeby dało się je zrobić samemu, w swoim tempie, na tym samym labie. Nie musisz — ale są twoje.

4. Sprawdź, że repozytorium jest w porządku: `git status` czysty, `.env` i `kopie/` nadal ignorowane, pipeline zielony.

5. Commit i push:

       git add .
       git commit -m "docs: retro i zamknięcie stażu"
       git push

6. `lab koniec ci` — raport dnia. Potem ostatni commit z raportem.

**Sprawdź się:** `lab grade zamkniecie`, potem `lab koniec zamkniecie`

---

## Na koniec

Pięć dni temu nie wiedziałeś, dlaczego przeglądarka blokuje odpowiedź, której `curl` nie blokuje.

Dziś masz aplikację, która chodzi w kontenerach, trzyma dane w prawdziwej bazie, ma kopię zapasową sprawdzoną w boju i pipeline, który po każdym pushu sprawdza ją za ciebie. Wszystko to jest w twoim repozytorium, razem z notatkami z każdego dnia — i to jest coś, co **da się pokazać** przy kolejnej rozmowie.

Do zobaczenia na obronie.
