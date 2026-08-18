# Kontenery — ta sama aplikacja, inne opakowanie

**To jedyny dokument, który dziś czytasz.** Zadania są w kolejności wykonania, pogrupowane w moduły.

## Cel dnia

Wczoraj doprowadziłeś aplikację do stanu, w którym utrzymuje się w ruchu na twojej maszynie: środowisko wirtualne, zależności, migracja, konfiguracja ze zmiennych środowiskowych, usługa systemd, dziennik. Dziś zapiszesz to samo w postaci, którą da się przenieść — i przekonasz się, że przeniesienie **nie jest darmowe**.

Trzy rzeczy z poprzednich dni wracają dziś w nowej postaci i to jest cała konstrukcja tego dnia:

- **ulotność danych.** W F1 sam ułożyłeś hierarchię: zmienna powłoki → `tmpfs` → dysk. Wczoraj dołożyłeś do niej piętro. Dziś dochodzi czwarte i jest najbardziej podchwytliwe ze wszystkich, bo **wygląda jak dysk**. To jest najważniejszy moment dnia.
- **`APP_HOST=127.0.0.1`.** Wczoraj znaczyło „widoczna tylko z tej maszyny". Dziś znaczy dokładnie to samo — tylko że „ta maszyna" to teraz wnętrze kontenera, więc przekierowanie portu nic nie da.
- **konfiguracja przez zmienne środowiskowe.** Ta sama, co wczoraj. Zmienia się wyłącznie kanał, którym wchodzi do procesu.

Kodu aplikacji nadal nie piszesz i nadal go nie dotykasz.

## Zasady

Te same co wczoraj:

- **Korzystaj z AI**; warunek jeden — `sudo` czegoś, czego nie umiesz opisać, nie uruchamiasz nigdy.
- **Dowodem jest wynik, nie opis** — wyniki dopisujesz przez `>>` z nagłówkiem zadania.
- **🔮** oznacza zadanie, w którym najpierw zapisujesz przewidywanie, a dopiero potem sprawdzasz. W F1, F2 i wczoraj robiłeś to rzetelnie i nie poprawiałeś po fakcie — zrób tak samo.
- **Zablokowany dłużej niż 20 minut?** Zapisz, na czym, przejdź dalej, wróć później.
- **Notatki idą do `notatki/kontenery.md`.** Na starcie: `export NOTATKI=~/staz/notatki/kontenery.md`.
- **Pracujesz na dwóch sesjach SSH naraz** — w jednej trzymasz kontener albo jego log, w drugiej sprawdzasz.
- **Commituj po każdym module.** Pracujemy zdalnie i twoje commity są jedynym miejscem, z którego widzę, gdzie jesteś.
- **Zapisuj pytania na bieżąco.** Dziś, tak jak wczoraj, **„nie mam pytań" nie jest dopuszczalną odpowiedzią.**
- **Log czytasz od pierwszej linii, nie od ostatniej.** Ta aplikacja wypisuje przy starcie komplet ustawień, z którymi wystartowała. Dziś ta zasada zadziała dokładnie tak samo — zmieni się tylko polecenie, którym ten log oglądasz.

Dodatkowo dziś jedna rzecz nowa:

- **Adresu twojej maszyny wirtualnej nigdzie w tym dokumencie nie ma** i to jest celowe. Wszędzie, gdzie piszę „**adres, pod którym twój Windows widzi VM-kę**", wstawiasz to, czego używałeś wczoraj w `config.js` i w przeglądarce. Jeśli masz w VirtualBoksie **przekierowanie portów**, tym adresem jest `localhost` — i to nie jest błąd ani uproszczenie, tylko konsekwencja sposobu, w jaki masz ustawioną sieć. Zapisz tę wartość na górze notatek i używaj jej wszędzie, gdzie zobaczysz ten zwrot.

## Zanim zaczniesz — materiały i Docker

### 1. Materiały

Na maszynie wirtualnej:

    cd ~/staz
    git pull
    ./zainstaluj.sh

To ta sama komenda co zawsze — `zainstaluj.sh` sam znajdzie nową paczkę, rozpakuje ją i posprząta po sobie (opis w `JAK-ZACZAC-DZIEN.md`). Instalacja **dokłada** zadania obok F1, F2 i wczorajszych — zaliczenia i notatki zostają nietknięte.

### 2. Docker

Dockera nie ma jeszcze na twojej maszynie. Instalujesz go **teraz, przed pierwszym zadaniem**, bo jeden z kroków wymaga wylogowania się i zalogowania z powrotem — a w połowie dnia to kosztuje więcej niż na starcie.

    sudo apt update
    sudo apt install -y docker.io docker-compose-v2
    sudo systemctl enable --now docker
    sudo usermod -aG docker $(whoami)

Ostatnie polecenie dopisuje twoje konto do grupy `docker`. **Zmiana przynależności do grup obowiązuje od nowego zalogowania**, więc teraz: `exit`, połącz się po SSH jeszcze raz i sprawdź, że działa **bez `sudo`**:

    docker run --rm hello-world
    docker compose version

Jeśli pierwsze polecenie mówi coś o odmowie dostępu do gniazda (`permission denied … docker.sock`), to znaczy, że nowe logowanie nie zadziałało — wyjdź i zaloguj się jeszcze raz. **Nie obchodź tego przez `sudo docker`**; przez resztę dnia zakładam, że `docker` działa na twoim koncie.

Gdyby pakiet `docker-compose-v2` nie istniał w twoim wydaniu Ubuntu, zgłoś to — jest wtedy druga droga, przez oficjalne repozytorium Dockera, i przejdziemy przez nią razem.

### 3. Ustaw dzień

    lab dzien kontenery
    lab moduly

## Jak wygląda dzień

Ten sam schemat co zawsze, moduł po module:

    lab start <moduł>     # przygotowuje środowisko wszystkich zadań modułu
    lab grade <moduł>     # sprawdza, czy zrobiłeś dobrze — możesz powtarzać do skutku
    lab koniec <moduł>    # zamyka moduł i przechodzi do następnego

`lab grade` ocenia **cały moduł naraz**. Uruchomione w połowie modułu pokaże na czerwono zadania, których jeszcze nie robiłeś — to normalne.

**O czasach.** Suma zadań to **230 minut**, plus **10 minut rezerwy** — razem cztery godziny. To jest **krótszy dzień niż wczorajszy** i tak ma być: zostały trzy dni na trzy tematy. Czasy są orientacyjne i nie są zakładem. Jeśli któreś zadanie idzie dłużej, zapisujesz po dwudziestu minutach, na czym stoisz, i idziesz dalej.

**Czego `lab grade` nie robi:** nie czyta twoich notatek w poszukiwaniu właściwych słów. Sprawdza **stan maszyny** — czy obraz istnieje, czy kontener działa, czy port jest przekierowany, czy wolumen ma dane, co odpowiada API. Z notatek patrzy najwyżej na to, czy sekcja danego zadania w ogóle istnieje i ma treść. Zrozumienie sprawdzamy na obronie.

**Każde zadanie ma cztery części:** „O co tu chodzi" (po co ci to), „Czego potrzebujesz" (gotowe prompty do AI — proszą o **wytłumaczenie mechanizmu**, nie o rozwiązanie; jeśli przerobisz je na „napisz mi polecenie, które…", stracisz dokładnie to, po co tu jesteś), „Zadanie" i „Sprawdź się".

---

## Moduł: obraz — 60 min

    lab start obraz

### Z1. Obraz, kontener, warstwa — 10 min

#### O co tu chodzi

W quizie na pytanie o różnicę między kontenerem a maszyną wirtualną napisałeś: „maszyna wirtualna ma system". To jest połowa odpowiedzi i to ta łatwiejsza. Druga połowa — co w takim razie ma kontener i skąd bierze resztę — jest tym, czego dziś użyjesz sto razy.

Zanim cokolwiek zbudujesz, potrzebujesz trzech słów: **obraz**, **kontener**, **warstwa**. Dziesięć minut teraz oszczędza godzinę zgadywania po południu.

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi różnicę między **obrazem** a **kontenerem** w Dockerze: co jest czym, co jest tylko do odczytu, a co powstaje dopiero przy uruchomieniu. Wytłumacz też, czym jest **warstwa** obrazu i dlaczego obraz składa się z wielu warstw zamiast być jednym plikiem. Nie odnoś się do żadnego konkretnego projektu.

> Wytłumacz mi, czym kontener różni się od maszyny wirtualnej: co każde z nich uruchamia u siebie, a co bierze z zewnątrz. Dlaczego kontener nie ma własnego jądra systemu i skąd bierze się z tego różnica w czasie startu i w rozmiarze? Bez porównań marketingowych — chcę wiedzieć, co się dzieje technicznie.

#### Zadanie

1. `docker version` — zapisz wersję klienta i wersję serwera. Jedno zdanie: która z tych dwóch części jest procesem działającym w tle i **sprawdź to tym samym poleceniem, którym wczoraj sprawdzałeś `linkbox`**.
2. `docker images` oraz `docker ps -a` — wypisz oba. Jedno zdanie: czym różni się to, co pokazuje pierwsze polecenie, od tego, co pokazuje drugie.
3. Uruchom Pythona w kontenerze i porównaj go z Pythonem na maszynie:

       python3 --version
       docker run --name proba python:3.12-slim python --version

   Zapisz obie wersje. Kontener celowo uruchamiasz **bez** `--rm`.
4. `docker ps` i `docker ps -a` jeszcze raz. Kontener `proba` jest tylko na jednej z tych list — zapisz na której i co pokazuje kolumna ze statusem.
5. Usuń go: `docker rm proba`.

**Do notatek, dwa zdania:**

- Czym obraz różni się od kontenera — użyj do tego dwóch list z punktu 2.
- Dodanie twojego konta do grupy `docker` sprawiło, że możesz uruchamiać kontenery bez `sudo`. Zastanów się (i zapytaj AI, jeśli trzeba), **dlaczego mówi się, że to jest w praktyce równoważne daniu temu kontu uprawnień administratora na całej maszynie**. Jedno zdanie.

**Sprawdź się:** `lab grade obraz`

Wyjdzie na czerwono — dwa zadania modułu masz jeszcze przed sobą.

### Z2. Dockerfile dla `linkbox` — 30 min

#### O co tu chodzi

Wczoraj doprowadziłeś tę aplikację do działania, wykonując po kolei kroki z `README.md`: środowisko wirtualne, zależności, migracja, start. Zajęło ci to godzinę i istnieje wyłącznie na twojej maszynie. Jutro ktoś inny — albo ty za pół roku, albo serwer, którego jeszcze nie ma — musiałby przejść tę samą drogę i pomylić się w tym samym miejscu.

`Dockerfile` to ta sama instrukcja, tylko zapisana w postaci, którą **da się wykonać**. Nie opisuje, jak uruchomić aplikację; opisuje, **jak zbudować maszynę, na której ta aplikacja już jest uruchomiona**.

Jest w tym jeden krok, o którym wczoraj nie musiałeś myśleć, a dziś musisz — zobaczysz go w zadaniu.

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi, co robi każda z instrukcji `FROM`, `WORKDIR`, `COPY`, `RUN`, `USER`, `EXPOSE` i `CMD` w pliku `Dockerfile`. Przy każdej powiedz, czy jej efekt powstaje w czasie **budowania** obrazu, czy dopiero przy **uruchomieniu** kontenera — to rozróżnienie jest dla mnie najważniejsze. Nie pisz mi gotowego Dockerfile'a pod mój projekt.

> Wytłumacz mi, dlaczego obraz bazowy podaje się z konkretnym tagiem wersji, a nie jako `latest`. Co dokładnie się psuje, gdy zbuduję obraz z `latest` dzisiaj, a ktoś inny zbuduje go z tego samego pliku za trzy miesiące? Wytłumacz też, czym różnią się warianty obrazów oznaczane `slim` i `alpine` od pełnych i co się traci, wybierając mniejszy.

> Wytłumacz mi, co robi plik `.dockerignore` i czym różni się od `.gitignore`. Co konkretnie dzieje się z plikami, których nie wykluczę — gdzie one lądują i co powiększają? Wytłumacz też, dlaczego kroku przygotowania **struktury bazy danych** nie wykonuje się w czasie budowania obrazu, tylko przy starcie kontenera. Bez pisania mi gotowego pliku.

#### Zadanie

Pracujesz w `~/staz/aplikacja/api`.

1. **Zanim zaczniesz pisać**, zmierz i zapisz dwie rzeczy: `du -sh .venv` oraz `du -sh .` — ile waży środowisko wirtualne i ile waży cały katalog.
2. Napisz `.dockerignore`. Ma wykluczyć wszystko, co nie należy do obrazu: środowisko wirtualne, bazę danych, twoją lokalną konfigurację i pliki pośrednie Pythona. Podpowiedź, gdzie szukać listy: leżący obok `.gitignore` wyklucza prawie dokładnie to samo i z prawie dokładnie tych samych powodów.
3. Napisz `Dockerfile` w tym samym katalogu. Ma spełniać wszystkie poniższe warunki:
   - obraz bazowy **z konkretną wersją Pythona** (aplikacja wymaga 3.11 lub nowszego), w wariancie lekkim — nie `latest`,
   - ustalony katalog roboczy w środku obrazu,
   - zainstalowane zależności z `requirements.txt`,
   - wniesiony kod aplikacji,
   - zadeklarowany port, na którym aplikacja nasłuchuje,
   - aplikacja uruchamiana tym samym poleceniem co wczoraj (`python -m app`),
   - **proces nie działa jako `root`.** Wczoraj w unicie systemd wpisałeś `User=` i wiesz dlaczego. Tu obowiązuje dokładnie ta sama zasada i dokładnie z tego samego powodu.
4. **Jeszcze jedna rzecz, o której wczoraj nie musiałeś myśleć.** Migrację (`alembic upgrade head`) uruchomiłeś raz, ręcznie, i temat się skończył. Kontener startuje od zera przy **każdym** uruchomieniu — a za dwa moduły zobaczysz, że jego baza też potrafi startować od zera. Zadbaj o to, żeby przy starcie kontenera struktura bazy była na miejscu, **zanim** ruszy aplikacja. Jedno polecenie ma poprzedzić drugie; trzeci prompt wyżej mówi ci, dlaczego nie robi się tego przy budowaniu.
5. Zbuduj obraz i nadaj mu nazwę oraz tag:

       docker build -t linkbox:1.0 .

   Zapisz, ile trwało budowanie i ile waży gotowy obraz (`docker images linkbox`).
6. Sprawdź, że w obrazie jest to, co miało być, i nie ma tego, czego być nie miało:

       docker run --rm linkbox:1.0 ls -a
       docker run --rm linkbox:1.0 whoami

   Zapisz oba wyniki.

**Do notatek, trzy zdania:**

- Porównaj rozmiar `.venv` z punktu 1 z rozmiarem obrazu. W obrazie nie ma środowiska wirtualnego, a aplikacja i tak ma swoje biblioteki. Napisz, **po co był `venv` na maszynie i dlaczego w kontenerze jest zbędny.**
- Punkt 6, drugie polecenie: kontener wypisał nazwę konta, na którym uruchamia się proces. Jedno zdanie, dlaczego chcesz tam widzieć to, co widzisz.
- `requirements.txt` zawiera również narzędzia deweloperskie — `pytest`, `ruff`, `black`. Trafiły do twojego obrazu. Jedno zdanie: czy powinny i co byś z tym zrobił, gdyby ten obraz miał iść na produkcję.

**Sprawdź się:** `lab grade obraz`

### Z3. 🔮 Kolejność `COPY` — 20 min

#### O co tu chodzi

Obraz zbudowałeś raz. W pracy budujesz go kilkadziesiąt razy dziennie — po każdej zmianie w kodzie, przy każdym uruchomieniu potoku CI — i wtedy zaczyna być ważne, ile to trwa.

Docker nie buduje wszystkiego od nowa: pamięta wynik każdego kroku i pomija te, które się nie zmieniły. Wystarczy jednak przestawić dwie linijki, żeby przestał — i wtedy każda poprawka literówki w komentarzu kosztuje ponowną instalację wszystkich zależności. To jest najczęstszy błąd w pierwszym Dockerfile w życiu i jednocześnie najłatwiejszy do pokazania.

#### Czego potrzebujesz

> Wytłumacz mi, na czym polega pamięć podręczna warstw (cache) przy budowaniu obrazu Dockera: skąd Docker wie, że dany krok można pominąć, i co się dzieje ze wszystkimi krokami **po** tym, który się zmienił. Wytłumacz szczególnie, dlaczego zmiana pliku kopiowanego w jednym kroku unieważnia warstwy powstałe w krokach następnych. Bez odnoszenia się do mojego pliku.

#### Zadanie

**Zapisz przewidywania, zanim cokolwiek uruchomisz** — dwie odpowiedzi, każda z jednym zdaniem uzasadnienia:

1. Zmieniasz jedną literę w komentarzu w pliku kodu aplikacji i budujesz obraz ponownie. Czy instalacja zależności wykona się jeszcze raz?
2. To samo, ale w Dockerfile'u kopiowanie **całego** katalogu stoi **przed** instalacją zależności. Czy odpowiedź się zmieni?

Teraz sprawdź:

1. Zbuduj obraz drugi raz, **bez żadnej zmiany**. Zapisz czas i policz, ile kroków miało w wyniku `CACHED`.
2. Zmień jedną literę w komentarzu w `app/main.py` — w komentarzu, nie w kodzie. Zbuduj ponownie. Zapisz czas i **numer kroku, od którego cache przestał działać**.
3. Zrób kopię swojego Dockerfile'a i w kopii **przestaw kolejność**: najpierw kopiowanie całego katalogu, potem instalacja zależności.

       cp Dockerfile Dockerfile.zle
       # popraw Dockerfile.zle
       docker build -f Dockerfile.zle -t linkbox:zle .

4. Zmień jeszcze raz literę w tym samym komentarzu i zbuduj **obie** wersje. Zapisz oba czasy obok siebie.
5. Posprzątaj: `rm Dockerfile.zle` i `docker rmi linkbox:zle`.

**Do notatek, dwa zdania:**

- Dlaczego `requirements.txt` kopiuje się osobno i **przed** kodem. Nie „bo tak się robi" — napisz, co konkretnie dzięki temu zostaje pominięte.
- Ile razy dziennie musiałbyś zbudować ten obraz, żeby różnica z punktu 4 zaczęła cię obchodzić. Policz to na swoich dwóch pomiarach, nie na wyczuciu.

**Sprawdź się:** `lab grade obraz`

<!-- -->

    lab grade obraz
    lab koniec obraz
    cd ~/staz && git add notatki/ aplikacja/api/Dockerfile aplikacja/api/.dockerignore
    git commit -m "feat: Dockerfile dla linkbox" && git push

**Uwaga na commit.** Dziś, inaczej niż wczoraj, **tworzysz nowe pliki w repozytorium** — `Dockerfile`, `.dockerignore`, a później `compose.yaml`. Samo `git add notatki/` ich nie obejmie, a niezacommitowane zablokują ci zaliczenie ostatniego modułu dnia. Po każdym commicie sprawdź `git status`.

---

## Moduł: uruchomienie — 50 min

    lab start uruchomienie

### Z4. 🔮 Kontener wstał, a strony nie ma — 30 min

#### O co tu chodzi

To jest wczorajsze Z7 o jedno piętro wyżej.

Obraz jest zbudowany. Kontener wstaje, `docker ps` mówi `Up`, log wygląda znajomo i nie ma w nim ani jednego błędu. A strona się nie otwiera. Nic nie jest zepsute — po prostu jedna wartość konfiguracji znaczy dziś coś innego niż wczoraj, mimo że jest identyczna.

Przy okazji zobaczysz rzecz, której zwykle nikt nie rozumie za pierwszym razem: **przekierowanie portów, które masz ustawione w VirtualBoksie, i przełącznik `-p` w `docker run` to jest dokładnie ten sam mechanizm.** Dwie warstwy tego samego, jedna nad drugą. Po tym zadaniu będziesz umiał policzyć, ile ich stoi między twoją przeglądarką a procesem.

#### Czego potrzebujesz

> Wytłumacz mi, co robi przełącznik `-p` w `docker run`: po której stronie dwukropka jest port maszyny, a po której port w kontenerze, i co dokładnie dzieje się z połączeniem przychodzącym na port maszyny. Wytłumacz też, czym różni się instrukcja `EXPOSE` w Dockerfile od `-p` przy uruchomieniu — która z nich naprawdę otwiera drogę z zewnątrz, a która jest wyłącznie opisem. Nie układaj polecenia pod mój projekt.

> Wytłumacz mi, czym jest `127.0.0.1` **wewnątrz** kontenera. Czy to ten sam `127.0.0.1`, co na maszynie, na której ten kontener działa? Jeśli serwer w kontenerze nasłuchuje wyłącznie na tym adresie, to kto może się z nim połączyć, a kto nie — i czy przekierowanie portu przy uruchomieniu cokolwiek tu zmieni? Chcę zrozumieć mechanizm, mam to rozwiązać sam.

#### Zadanie

**Zapisz cztery przewidywania, zanim uruchomisz cokolwiek** — każde z jednym zdaniem uzasadnienia:

1. Twoja wczorajsza usługa `linkbox` jest włączona do automatycznego startu i trzyma port 8000. Co się stanie, gdy uruchomisz kontener z `-p 8000:8000`?
2. Kontener uruchomiony **bez** `-p`: `curl http://127.0.0.1:8000/health` z VM-ki — zadziała?
3. Kontener uruchomiony z `-p 8000:8000`, aplikacja w środku z domyślną konfiguracją — `curl` z VM-ki zadziała?
4. Ten sam kontener uruchomiony z `-p 8080:8000` — `curl` z VM-ki na port 8080 zadziała? A przeglądarka na Windowsie pod tym portem?

Teraz sprawdź, po kolei:

1. Uruchom kontener na pierwszym planie:

       docker run --rm -p 8000:8000 linkbox:1.0

   Zweryfikuj przewidywanie 1 i **przepisz komunikat dosłownie**. Doprowadź port do stanu, w którym da się go zająć. Wczorajszej usługi **nie usuwaj** — na razie tylko ją zatrzymaj, wrócimy do niej w module `compose`.
2. Uruchom kontener bez `-p` i sprawdź przewidywanie 2.
3. Uruchom kontener z `-p 8000:8000` i sprawdź przewidywanie 3. Kontener wstaje, log wygląda znajomo — **przeczytaj go od pierwszej linii**, jak wczoraj.
4. Znajdź w logu linię, która mówi wprost, dlaczego aplikacja jest nieosiągalna, i przepisz ją. **To jest ta sama linia co wczoraj** — napisz obok, dlaczego znaczy dziś co innego.
5. Napraw to. **Bez zmiany kodu i bez przebudowywania obrazu** — ma wystarczyć sposób uruchomienia. Potwierdź `curl`-em z VM-ki, a potem otwórz `/docs` w przeglądarce na Windowsie, pod adresem, pod którym twój Windows widzi VM-kę.
6. Sprawdź przewidywanie 4: uruchom ten sam obraz z `-p 8080:8000`. Najpierw `curl` z VM-ki na porcie 8080, potem przeglądarka na Windowsie pod tym samym portem. Zapisz **oba** wyniki. Jeśli z Windowsa nie działa — **nie naprawiaj tego**, tylko nazwij, czego brakuje. Potem wróć do `-p 8000:8000`.

**Do notatek, trzy zdania:**

- `APP_HOST=127.0.0.1` znaczy dokładnie to samo co wczoraj. Napisz, **co się zmieniło**, żeby ta sama wartość dała inny skutek.
- Dlaczego `-p` nie pomogło, dopóki aplikacja nasłuchiwała na `127.0.0.1`. Użyj w tym zdaniu słowa „kto" — kto właściwie próbuje się połączyć po stronie kontenera.
- Punkt 6: wypisz po kolei **wszystkie przekierowania, które muszą zadziałać**, żeby pakiet z twojej przeglądarki na Windowsie dotarł do procesu w kontenerze. Policz je. Potem napisz jednym zdaniem, dlaczego port 8000 działa, a 8080 zachował się tak, jak się zachował.

**Sprawdź się:** `lab grade uruchomienie`

### Z5. Konfiguracja i log kontenera — 20 min

#### O co tu chodzi

Wczoraj konfiguracja wchodziła do aplikacji przez `Environment=` w pliku usługi. Dziś wejdzie przez `-e` w linii poleceń. Aplikacja nie została zmieniona ani o jeden znak — i o to właśnie chodzi w konfiguracji przez zmienne środowiskowe: program nie wie i nie ma prawa wiedzieć, co go uruchomiło.

Druga rzecz: dziś nie ma `journalctl`. Aplikacja nadal pisze na standardowe wyjście i nadal **świadomie nie decyduje, gdzie to trafi** — decyduje o tym to, co ją uruchomiło. Wczoraj był to dziennik systemowy, dziś jest to log kontenera. To jest ta sama reguła, którą opisywałeś wczoraj w module `logi`, trzeci raz z rzędu potwierdzona.

#### Czego potrzebujesz

> Wytłumacz mi, jak przekazuje się konfigurację do kontenera: co robi przełącznik `-e` przy `docker run`, czym różni się od instrukcji `ENV` w Dockerfile i **która z tych wartości wygrywa**, gdy obie ustawiają tę samą zmienną. Wytłumacz też, dlaczego wartości specyficznych dla środowiska nie zapisuje się w obrazie. Bez gotowca pod mój projekt.

> Wytłumacz mi, skąd biorą się logi, które pokazuje `docker logs`: co dokładnie jest zbierane, gdzie to leży i co się z tym dzieje, gdy kontener zostanie usunięty. Wytłumacz też, czym `docker logs -f` różni się od `journalctl -f` i dlaczego aplikacja w kontenerze tym bardziej nie powinna pisać do własnego pliku z logiem.

#### Zadanie

**Najpierw jedna rzecz z wczoraj.** Front na porcie 3000 dziś nie działa i nie jest to awaria — maszyna od wczoraj się restartowała, a serwer frontu **nie jest usługą**, tylko zwykłym procesem sesji. Sam to nazwałeś wczoraj w Z11. Uruchom go tak jak wczoraj, w trzeciej sesji SSH:

    cd ~/staz/aplikacja/web && python3 -m http.server 3000

W module `compose` przestanie być procesem sesji na dobre.

1. Uruchom kontener **w tle** (`-d`), z własną nazwą (`--name`), podając przez `-e` komplet konfiguracji: adres nasłuchu, port, listę dozwolonych origin-ów (ta sama wartość co wczoraj) i nazwę instancji inną niż domyślna. Potwierdź **w logu startowym**, że aplikacja przyjęła wszystkie te wartości.
2. `docker ps` — przepisz kolumnę `PORTS` i wyjaśnij jednym zdaniem, co dokładnie w niej widać.
3. W drugiej sesji włącz podgląd logu na żywo. W pierwszej utwórz link `curl`-em i odśwież front na Windowsie. Zapisz, co pojawiło się w logu i **czym te wpisy różnią się od siebie**.
4. Uruchom **drugi** kontener z **tego samego obrazu**, na innym porcie maszyny i z inną nazwą instancji. Sprawdź, że po logu poznajesz, który z nich odpowiedział. Zapisz, ile masz teraz obrazów i ile kontenerów — i jedno zdanie, dlaczego te dwie liczby się różnią.
5. Spróbuj uruchomić kontener z `LOG_LEVEL=GADATLIWY`. Zapisz, co się stało — **i którym poleceniem to zobaczyłeś**, skoro `docker ps` tego kontenera nie pokazuje.
6. Posprzątaj: zatrzymaj i usuń drugi kontener oraz ten z punktu 5. Zostaje jeden, działający.

**Do notatek, dwa zdania:**

- Wczoraj w module `konfiguracja` zacząłeś listę miejsc, z których ta aplikacja może dostać `APP_PORT`, a w module `usluga` ją uzupełniłeś. **Dopisz do niej dzisiejsze piętra** i uszereguj całość od najbardziej ulotnego do najtrwalszego.
- Punkt 5: kontener, który się nie uruchomił, nadal jest na liście i nadal ma log. Jedno zdanie: czym różni się „kontener zatrzymany" od „kontener usunięty". Odpowiedź na to pytanie jest całym następnym modułem.

**Sprawdź się:** `lab grade uruchomienie`

<!-- -->

    lab grade uruchomienie
    lab koniec uruchomienie
    cd ~/staz && git add notatki/ && git commit -m "docs: modul uruchomienie" && git push

---

## Moduł: dane — 40 min

    lab start dane

**To jest najważniejszy moduł dnia.** Jeśli coś z dzisiaj masz pamiętać za rok, to właśnie te dwa zadania.

### Z6. 🔮 Gdzie znikają dane — 15 min

#### O co tu chodzi

W F1 ułożyłeś hierarchię trwałości: zmienna powłoki → `tmpfs` → dysk. W quizie na pytanie „kontener i dane" napisałeś „nie wiem" — i to była szczera odpowiedź, bo bez tej hierarchii nie ma jak na nie odpowiedzieć.

Teraz ją masz. Dochodzi czwarty poziom i jest najbardziej podchwytliwy ze wszystkich, bo **z wnętrza kontenera wygląda dokładnie jak dysk**: jest ścieżka, jest plik, `ls -l` pokazuje rozmiar, aplikacja normalnie zapisuje i odczytuje. Wszystko się zgadza aż do momentu, w którym coś sprząta kontenery.

To zadanie jest o **zobaczeniu** problemu. Naprawy tu nie ma — jest w Z7.

#### Czego potrzebujesz

> Wytłumacz mi, gdzie fizycznie ląduje plik zapisany przez proces działający w kontenerze. Czym jest **warstwa zapisywalna** kontenera, jak długo żyje i co się z nią dzieje przy `docker stop`, przy `docker start`, a co przy `docker rm`. Wytłumacz też, dlaczego dwa kontenery uruchomione z tego samego obrazu nie widzą nawzajem swoich zmian. Nie odnoś się do mojej aplikacji.

#### Zadanie

**Zapisz cztery przewidywania, zanim cokolwiek sprawdzisz** — każde z jednym zdaniem uzasadnienia:

1. Pod jaką ścieżką **w kontenerze** wyląduje plik `links.db`? Odpowiedz konkretną ścieżką, nie opisem.
2. Tworzysz link, zatrzymujesz kontener (`docker stop`) i uruchamiasz go z powrotem (`docker start`). Link będzie?
3. Tworzysz link, usuwasz kontener (`docker rm`) i uruchamiasz nowy z tego samego obrazu. Link będzie?
4. Plik `links.db`, który leży od wczoraj na maszynie w `~/staz/aplikacja/api` — ma z tym wszystkim cokolwiek wspólnego?

Teraz sprawdź. Przy każdym punkcie zapisz polecenie i wynik:

1. W działającym kontenerze utwórz przez API **dwa** linki i wypisz listę.
2. Zajrzyj do środka kontenera i znajdź plik bazy — ścieżka i rozmiar. Do wykonania polecenia w działającym kontenerze służy `docker exec`.
3. Wypisz, co w tym kontenerze zmieniło się względem obrazu: `docker diff <nazwa>`. Znajdź na tej liście swój plik bazy i przepisz linijkę. **To jest ta warstwa zapisywalna, o którą pytał prompt** — widzisz ją na własne oczy.
4. `docker stop`, potem `docker start`, potem znowu lista linków. Sprawdź przewidywanie 2.
5. `docker rm -f` i nowy kontener z tego samego obrazu, z takimi samymi przełącznikami. Znowu lista linków. Sprawdź przewidywanie 3.
6. Na maszynie: `ls -l ~/staz/aplikacja/api/links.db`. Porównaj datę modyfikacji z tym, co robiłeś dziś. Sprawdź przewidywanie 4.

**Do notatek, trzy zdania:**

- **Dopisz czwarty poziom do hierarchii trwałości z F1**: zmienna powłoki → `tmpfs` → dysk → … Powiedz, gdzie w tym szeregu leży warstwa zapisywalna kontenera.
- Dlaczego ten poziom jest podchwytliwy — czym wygląda, a czym jest. Jedno zdanie, własnymi słowami.
- Punkt 5 usunął dane, których nikt nie kasował. Napisz, **co dokładnie je skasowało** i w którym momencie.

**Sprawdź się:** `lab grade dane`

### Z7. Wolumen — 25 min

#### O co tu chodzi

Naprawiasz to, co zobaczyłeś w Z6. Naprawa nie polega na kopiowaniu pliku w bezpieczne miejsce — polega na **zadeklarowaniu przy starcie, że jedna konkretna ścieżka nie należy do kontenera.** Wszystko, co pod nią wyląduje, przestaje być częścią tego, co ginie razem z kontenerem.

To jest ta sama decyzja, którą podejmuje się na każdym wdrożeniu z bazą danych, i pierwsza rzecz, o którą pyta się przy przeglądzie cudzego `compose.yaml`.

Uprzedzam od razu, żebyś nie szukał usterki tam, gdzie jej nie ma: **w tym zadaniu najprawdopodobniej zobaczysz błąd o braku dostępu do pliku.** To nie jest pomyłka w treści — to jest właśnie ta rzecz, której to zadanie uczy.

#### Czego potrzebujesz

> Wytłumacz mi, czym jest **wolumen** w Dockerze i czym różni się od zwykłego katalogu w kontenerze: gdzie fizycznie leżą jego dane, kto nimi zarządza i co się z nimi dzieje po usunięciu kontenera. Wytłumacz też różnicę między **wolumenem nazwanym** a **podmontowaniem katalogu z maszyny** (`bind mount`) — co się do czego lepiej nadaje i który z nich zwykle wybiera się na dane bazy, a który na kod. Bez gotowca pod mój projekt.

> Wytłumacz mi, do kogo należy katalog, który powstaje jako punkt podmontowania **pustego nazwanego wolumenu**, i co się dzieje, gdy proces w kontenerze działa na koncie innym niż `root` i próbuje w tym katalogu utworzyć plik. Jak się ten problem rozwiązuje **po stronie obrazu**? Odpowiadaj ogólnie, nie znasz mojego Dockerfile'a.

#### Zadanie

1. Utwórz nazwany wolumen i uruchom kontener tak, żeby baza aplikacji wylądowała **w nim**, a nie w kontenerze.

   Dwie rzeczy, o które się tu potykają wszyscy:
   - wolumen podmontowuje się pod **katalog**, nie pod pojedynczy plik — więc baza musi trafić do jakiegoś katalogu, a nie leżeć tam, gdzie leży teraz;
   - żeby to osiągnąć, musisz zmienić **jedną zmienną konfiguracji aplikacji**. Który zapis oznacza ścieżkę bezwzględną, a który względną — masz opisane w `.env.example`, przy tej właśnie zmiennej. Przeczytaj ten komentarz uważnie, bo różnica to jeden znak.
2. Jeśli kontener się nie uruchomi i w logu zobaczysz błąd o niemożności otwarcia pliku bazy — **przepisz go dosłownie do notatek** i dopiero potem szukaj przyczyny. Naprawa jest w Dockerfile: brakuje w nim jednej rzeczy, o której mówi drugi prompt wyżej. Popraw i przebuduj obraz.
3. Przy przebudowie zapisz, **ile kroków miało `CACHED`** i ile trwało budowanie. Porównaj z Z3 i dopisz jedno zdanie: czy kolejność, którą tam ustaliłeś, właśnie się przydała.
4. Potwierdź, że działa. Utwórz przez API **dwa nowe linki**, a potem:

       docker rm -f <nazwa>
       # uruchom nowy kontener z tym samym wolumenem
       curl ... /api/links

   Linki mają być na miejscu. Zapisz wynik.
5. `docker volume ls` i `docker volume inspect <wolumen>` — zapisz **ścieżkę na maszynie**, pod którą Docker trzyma dane tego wolumenu. Zajrzyj tam (`sudo ls -l …`). Jedno zdanie: do kogo ten katalog należy i dlaczego nie edytuje się go ręcznie.
6. **Próba kontrolna — obowiązkowa.** Uruchom jeszcze jeden kontener z tego samego obrazu, na innym porcie maszyny, **bez** wolumenu. Odpytaj jego listę linków. Zapisz wynik i wyjaśnij go jednym zdaniem. Potem go usuń.

**Do notatek, trzy zdania:**

- Co dokładnie deklarujesz, montując wolumen — napisz, **czego ta ścieżka przestaje być częścią**.
- Wróć do hierarchii z Z6 i dopisz do niej wolumen. Gdzie w niej leży?
- Wczoraj na obronie padło pytanie: „co zniknie, gdy skasuję katalog roboczy usługi". Odpowiedz na nie jeszcze raz, teraz o kontenerze: **co zniknie, gdy skasuję kontener, a co zostanie** — i skąd to wiesz, a nie zgadujesz.

**Sprawdź się:** `lab grade dane`

<!-- -->

    lab grade dane
    lab koniec dane
    cd ~/staz && git add notatki/ aplikacja/api/Dockerfile
    git commit -m "docs: modul dane" && git push

---

## Moduł: compose — 40 min

    lab start compose

### Z8. Jeden plik zamiast długiego polecenia — 25 min

#### O co tu chodzi

Twoje `docker run` ma już nazwę, przekierowanie portu, sześć zmiennych środowiskowych i wolumen. Zmieści się jeszcze w jednej linii, ale nikt — włącznie z tobą za tydzień — nie odtworzy go z pamięci bez pomyłki. A pomyłka w tym poleceniu nie jest widoczna od razu: kontener wstanie, tylko dane pójdą w złe miejsce.

To jest dokładnie ten sam problem, który wczoraj rozwiązał plik unitu: **opis stanu docelowego zapisany w pliku zamiast polecenia wpisywanego z pamięci.** `compose.yaml` jest tym, czym wczoraj był `linkbox.service` — z tą różnicą, że opisuje nie jeden proces, a cały zestaw.

#### Czego potrzebujesz

> Wytłumacz mi, czym jest plik `compose.yaml` i co opisuje: czym jest w nim „usługa", czym różni się `image:` od `build:` i jak zapisuje się w nim to, co w `docker run` podawało się przez `-p`, `-e` i `-v`. Wytłumacz też, co robi `docker compose up -d`, co robi `docker compose down` i czym `down` różni się od `stop`. Nie pisz mi gotowego pliku pod mój projekt.

> Wytłumacz mi, skąd Docker Compose bierze **nazwę projektu**, gdy jej nie podam, i co ta nazwa zmienia w nazwach kontenerów, sieci i **wolumenów**. Co się dzieje, gdy odwołam się w pliku compose do wolumenu, który już istnieje na maszynie — czy Compose go użyje, czy utworzy własny? Jak się wskazuje ten istniejący? Odpowiadaj ogólnie.

#### Zadanie

Pracujesz w `~/staz/aplikacja` — katalogu **nadrzędnym** nad `api/` i `web/`.

1. Napisz plik `compose.yaml` (dokładnie ta nazwa) z **jedną** usługą, nazwaną dokładnie **`api`**. Ma odtwarzać to samo, co robi twoje `docker run` z Z7:
   - obraz budowany z katalogu `api/`, nie pobierany gotowy,
   - przekierowanie portu,
   - komplet zmiennych środowiskowych,
   - wolumen z bazą,
   - **polityka restartu** — kontener ma wstawać sam po padzie i po włączeniu maszyny. To jest odpowiednik `Restart=` z wczorajszego unitu.
2. Zatrzymaj i usuń kontener uruchomiony ręcznie w Z7, a potem wystartuj stos:

       docker compose up -d
       docker compose ps
       docker compose logs

3. **Sprawdź, czy dane przeżyły przejście z `docker run` na compose.** Jeśli lista linków jest pusta — to nie jest usterka aplikacji ani twojego pliku. Zajrzyj do `docker volume ls` i porównaj z tym, co widziałeś w Z7. Zapisz, co znalazłeś, i doprowadź do stanu, w którym compose używa **tego samego wolumenu**, w którym leżą twoje dzisiejsze linki.
4. Potwierdź, że aplikacja jest widoczna z Windowsa: `/docs` w przeglądarce i zielony pasek stanu na froncie.
5. `docker compose down`, a potem `docker compose up -d` jeszcze raz. Zapisz, czy linki przetrwały, i jedno zdanie dlaczego.

**Do notatek, dwa zdania:**

- Wypisz obok siebie swoje `docker run` z Z7 i odpowiadające mu linijki `compose.yaml` — po jednej parze na każdy przełącznik. To jest tabelka, do której będziesz wracał.
- Jedno zdanie: co `docker compose down` robi z kontenerem, czego **nie** robi z wolumenem i jakim przełącznikiem robi też to drugie. To jest polecenie, którym najłatwiej dziś skasować sobie dane — chcesz wiedzieć o tym wcześniej niż przez przypadek.

**Sprawdź się:** `lab grade compose`

### Z9. Front dołącza do stosu — 15 min

#### O co tu chodzi

Wczoraj w Z11 zrestartowałeś maszynę i front nie wrócił. Nazwałeś wtedy, czego mu brakuje: **nie jest usługą, nikt go nie wznawia.** Dziś to naprawiasz — front przestaje być procesem, który trzymasz w trzeciej sesji SSH, i staje się częścią stosu, tak samo jak API.

Przy okazji ostatnia rzecz do posprzątania: wczorajsza usługa systemd nadal startuje sama i nadal chce ten sam port co twój kontener. Jedna aplikacja, dwóch zarządców — to się nie może udać.

#### Czego potrzebujesz

> Wytłumacz mi, jak w kontenerze uruchamia się serwer plików statycznych na obrazie `nginx`: w którym katalogu **wewnątrz** obrazu ten serwer szuka plików do podania i na którym porcie domyślnie nasłuchuje. Wytłumacz też, na czym polega podmontowanie katalogu z maszyny do kontenera i co daje dopisanie do niego trybu tylko do odczytu. Bez układania mi gotowej usługi.

> Wytłumacz mi, co właściwie wznawia kontenery po restarcie maszyny, gdy w pliku compose jest ustawiona polityka restartu. Który proces to robi i co ma z tym wspólnego usługa `docker` w systemd? Odpowiadaj ogólnie.

#### Zadanie

1. Dopisz do `compose.yaml` drugą usługę, nazwaną dokładnie **`web`**:
   - obraz `nginx` w wariancie `alpine`, z **konkretnym** tagiem — nie `latest`,
   - katalog `web/` z maszyny podmontowany tam, gdzie nginx szuka plików, **tylko do odczytu**,
   - port 3000 na maszynie, tak jak dotąd,
   - ta sama polityka restartu co przy `api`.

   Obrazu dla frontu **nie budujesz** — bierzesz gotowy. Jedno zdanie do notatek: dlaczego tu wystarczy `image:`, a przy API musiało być `build:`.
2. Zatrzymaj `python3 -m http.server` w trzeciej sesji. Podnieś stos i sprawdź front na Windowsie — ma działać tak jak przed chwilą.
3. **Wyłącz wczorajsze usługi systemd**: `linkbox` oraz `linkbox-staging`. Nie wystarczy je zatrzymać — mają nie wracać po restarcie maszyny (wiesz z wczorajszego Z11, którym poleceniem się to robi i czym różni się od zatrzymania). Zapisz, co zrobiłeś i dlaczego to było konieczne.
4. **Krótki eksperyment, dwie minuty.** Usuń z usługi `api` zmienną z listą dozwolonych origin-ów, podnieś stos ponownie i odśwież front. Zapisz, co zobaczył użytkownik i co zobaczyłeś w konsoli przeglądarki. Potem przywróć zmienną. To jest wczorajsza awaria, przeniesiona o jedno piętro — chcesz ją rozpoznać w pół sekundy, a nie w pół godziny.

**Do notatek, dwa zdania:**

- Wczoraj rolę „to ma wstawać samo po włączeniu maszyny" pełniło `systemctl enable`. Napisz, **co pełni tę rolę dzisiaj** — wymień oba elementy, bo to nie jest jedna rzecz.
- **Zapisz przewidywanie na jutro** (sprawdzisz je rano, przy pierwszym uruchomieniu maszyny): po włączeniu VM-ki, bez logowania się przez SSH i bez wpisywania czegokolwiek, front na Windowsie zadziała? Jedno zdanie uzasadnienia. Nie sprawdzaj tego dziś.

**Sprawdź się:** `lab grade compose`

<!-- -->

    lab grade compose
    lab koniec compose
    cd ~/staz && git add notatki/ aplikacja/compose.yaml
    git commit -m "feat: stos compose z API i frontem" && git push

---

## Moduł: awaria — 30 min

    lab start awaria

### Z10. Kumulacja: `Up`, a nie działa — 30 min

#### O co tu chodzi

To jest końcówka dnia i jego sens naraz.

Przedwczoraj `/health` mówiło, że wszystko gra, a aplikacja nie działała. Wczoraj `systemctl is-active` mówiło `active`, a użytkownik widział zepsutą stronę. Dziś `docker compose ps` mówi `Up` — i nadal nie działa.

To jest ta sama lekcja trzeci raz z rzędu, za każdym razem o piętro wyżej: **stan zgłaszany przez narzędzie potwierdza wyłącznie to, co to narzędzie umie sprawdzić.** Nikt ci nie powie, co jest zepsute ani ile tego jest.

Nowego materiału tu nie ma. Wszystko, czego potrzebujesz, robiłeś dziś — w każdym module po kolei. Jedyne, co jest nowe, to że nikt nie mówi, w którym.

#### Czego potrzebujesz

Niczego nowego. Jeśli poczujesz, że kręcisz się w kółko, wróć do metody z F2: **„podejrzewam X, sprawdzę to przez Y"** — jedno zdanie zapisane **przed** każdym poleceniem diagnostycznym.

Jeden prompt, jeśli utkniesz na **czytaniu** stanu, a nie na jego naprawianiu:

> Wytłumacz mi, jak sprawdzić, jaka konfiguracja **naprawdę** obowiązuje uruchomiony stos Docker Compose — nie ta, którą widzę w pliku, który sam napisałem, tylko ta, którą Compose faktycznie złożył i zastosował. Czy do jednego projektu może się dokładać więcej niż jeden plik i skąd Compose bierze te pliki, jeśli nie wskażę ich jawnie? Jak zobaczyć wynik złożenia w całości i jak rozpoznać, skąd pochodzi która wartość? Odpowiadaj ogólnie, nie znasz mojego projektu.

To jest **to samo pytanie**, które wczoraj zadawałeś o usługę systemd. Warto zauważyć, że jest to samo.

#### Zadanie

Twój stos jest podniesiony, `docker compose ps` pokazuje obie usługi jako działające. Front na Windowsie mimo to nie działa.

**Zanim cokolwiek zmienisz**, zapisz w notatkach:

- co widzisz na stronie — dosłownie, oba komunikaty,
- co widzisz w konsoli przeglądarki,
- jedno przewidywanie: gdzie leży problem i **dlaczego akurat tam**.

**Zasady:**

- Nie zmieniasz **ani jednego pliku aplikacji ani frontu**. `config.js` jest poprawny — to API ma wrócić tam, gdzie było, a nie front pójść za nim.
- Nie kasujesz i nie przepisujesz swojego `compose.yaml` od zera.
- Poprawka ma być **trwała**: po `docker compose down` i `docker compose up -d`, **bez żadnych dodatkowych przełączników**, stan ma się utrzymać. Rozwiązanie, które działa tylko przy jednym konkretnym uruchomieniu, nie liczy się jako naprawa.
- Dla **każdej** napotkanej przeszkody zapisujesz osobno: objaw, hipotezę, czym ją sprawdziłeś, przyczynę, poprawkę.

**Stan docelowy.** Opisuję go tak, jak zobaczyłby go użytkownik — nie listą objawów, bo ich lista jest właśnie tym, co masz sam ustalić:

1. **Front na Windowsie działa w całości**: pasek stanu zielony, a na liście są **te same linki, które dodałeś dzisiaj** — te z modułu `dane`. Formularz tworzy nowe i widać je po odświeżeniu.
2. **Stan przeżywa `docker compose down` i ponowne `docker compose up -d`.** Sprawdź to naprawdę, nie na słowo.

Uwaga do punktu 1: **pusta lista linków nie jest stanem docelowym**, nawet jeśli strona świeci na zielono. To znaczyłoby, że aplikacja działa — tylko nie tam, gdzie leży twoja dzisiejsza praca. Dokładnie tę różnicę ćwiczyłeś w module `dane`.

**Do notatek na koniec, trzy rzeczy:**

- Ile było problemów, jaki był każdy z nich i **z którego modułu dnia** pochodził.
- Które polecenie dało ci przełom i dlaczego wcześniej patrzyłeś w złe miejsce.
- Jedno zdanie o `docker compose ps`: przez cały czas pokazywał, że kontenery działają. **Co ten stan potwierdza, a czego nie potwierdza?** To jest to samo pytanie, co wczoraj o `systemctl is-active` i przedwczoraj o `/health` — odpowiedz na nie trzeci raz, teraz o piętro wyżej, i napisz, co się w twojej odpowiedzi zmieniło przez te trzy dni.

**Sprawdź się:** `lab grade awaria`

<!-- -->

    lab grade awaria
    lab koniec awaria
    cd ~/staz && git add notatki/ && git commit -m "docs: modul awaria" && git push

---

## Moduł: zamkniecie — 10 min

    lab start zamkniecie

### Z11. Zamknięcie dnia — 10 min

#### O co tu chodzi

Notatki są produktem tego dnia. Jedna sekcja szczególnie: **hierarchia trwałości**. Zacząłeś ją w F1 z trzema poziomami, wczoraj dopisałeś czwarty, dziś dwa kolejne. Za miesiąc, gdy ktoś zapyta cię „a gdzie właściwie mieszkają dane tej aplikacji", odpowiesz z tej jednej strony.

#### Zadanie

1. Uporządkuj `notatki/kontenery.md` — cztery sekcje:
   - **Eksperymenty** — Z3, Z4, Z6: przewidywania kontra wyniki. Bez poprawiania przewidywań po fakcie.
   - **Diagnozy** — Z7, Z8, Z10: co było zepsute, **jak** to znalazłeś i w jakiej kolejności.
   - **Hierarchia trwałości** — pełna wersja, od najbardziej ulotnego do najtrwalszego, wszystkie poziomy z F1, z wczoraj i z dziś. Przy każdym jedno zdanie: co go kasuje.
   - **Trzy pytania** — konkretne. Mogą dotyczyć czegoś, co dziś zadziałało, a nie rozumiesz dlaczego.

2. Oddaj pracę. **Sprawdź najpierw `git status` — ma być czysto.** Dziś powstały trzy nowe pliki śledzone przez Gita: `aplikacja/api/Dockerfile`, `aplikacja/api/.dockerignore` i `aplikacja/compose.yaml`. Jeśli któregoś nie zacommitowałeś przy swoim module, zrób to teraz:

       cd ~/staz
       git status
       git add notatki/ aplikacja/
       git commit -m "docs: notatki kontenery"
       git push

3. Zalicz i zamknij moduł, a potem cały dzień:

       lab grade zamkniecie
       lab koniec zamkniecie
       lab koniec kontenery       # raport całego dnia — pokaż go mentorowi

4. **To jeszcze nie koniec.** `lab koniec kontenery` zapisał raport dnia w twoim repozytorium (`wyniki/kontenery.md`), więc `git status` znowu nie jest czysty. Tak ma być — zaliczenie modułu już masz. Wypchnij raport osobnym commitem:

       git add wyniki/kontenery.md
       git commit -m "docs: raport dnia kontenery"
       git push

5. **Zostaw stos podniesiony.** Nie zatrzymuj kontenerów na koniec dnia — jutro rano sprawdzisz przewidywanie zapisane w Z9, a do tego maszyna musi wstać w takim stanie, w jakim ją zostawiasz.

6. Wyłącz maszynę i zrób snapshot **`po-kontenerach`**.

**Sprawdź się:** `lab grade zamkniecie`
