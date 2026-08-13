# Aplikacja — uruchom cudzy kod i utrzymaj go w ruchu

**To jedyny dokument, który dziś czytasz.** Zadania są w kolejności wykonania, pogrupowane w moduły.

## Cel dnia

Dostajesz gotową aplikację — API skracacza linków i front do niego. **Nie piszesz jej kodu.** Twoje zadanie to doprowadzić ją do stanu, w którym działa jak na serwerze: uruchamia się sama po restarcie maszyny, konfiguruje się bez dotykania kodu, ma logi, do których da się zajrzeć, i jest widoczna z twojej przeglądarki na Windowsie.

To jest ta granica, o którą chodzi w tym zawodzie: **„u mnie się uruchamia" to nie to samo co „działa"**. Przez cały dzień będziesz po tej drugiej stronie.

Po drodze spotkasz CORS-a — tego samego, przy którym kiedyś utknąłeś. Tym razem masz w rękach serwer, więc pierwszy raz możesz go naprawić naprawdę, a nie obejść.

## Zasady

Te same co w F2:

- **Korzystaj z AI**; warunek jeden — `sudo` czegoś, czego nie umiesz opisać, nie uruchamiasz nigdy.
- **Dowodem jest wynik, nie opis** — wyniki dopisujesz przez `>>` z nagłówkiem zadania.
- **⏱** oznacza zadanie na czas, **🔮** zadanie, w którym najpierw zapisujesz przewidywanie, a dopiero potem sprawdzasz.
- **Zablokowany dłużej niż 20 minut?** Zapisz, na czym, przejdź dalej, wróć później.
- **Notatki idą do `notatki/aplikacja.md`.** Na starcie: `export NOTATKI=~/staz/notatki/aplikacja.md`.
- **Pracujesz na dwóch sesjach SSH naraz** — w jednej trzymasz aplikację albo log, w drugiej sprawdzasz. Od modułu `cors` dojdzie trzecia, na serwer frontu, i zostanie już do końca dnia.

Dodatkowo dziś:

- **Commituj po każdym module.** Pracujemy zdalnie i twoje commity są jedynym miejscem, z którego widzę, gdzie jesteś. Format: `typ: co zrobiłeś`, tak jak `docs: notatki F1`.
- **Zapisuj pytania na bieżąco**, w sekcji `Pytania` w notatkach. Dziś **„nie mam pytań" nie jest dopuszczalną odpowiedzią** — pierwszy raz uruchamiasz cudzą aplikację na serwerze i pytania po prostu są. Dwa zadania proszą wprost o zapisanie pytania, zanim zaczniesz je rozwiązywać.
- **Log aplikacji czytasz od pierwszej linii, nie od ostatniej.** Ta aplikacja wypisuje przy starcie komplet ustawień, z którymi wystartowała. Bardzo często odpowiedź jest właśnie tam — wzięła inną wartość, niż ci się wydawało.

## Zanim zaczniesz — pobierz materiały

Wszystko przyszło do twojego repozytorium: zadania, kod aplikacji i nowa wersja labu. Na maszynie wirtualnej:

    cd ~/staz
    git pull
    unzip -o lab-aplikacja.zip
    sudo bash lab/install.sh $(whoami)

Instalacja **dokłada** zadania obok F1 i F2 — twoje zaliczenia i notatki zostają nietknięte. Gdyby zabrakło `unzip`: `sudo apt install unzip`.

Kod aplikacji jest w `~/staz/aplikacja/` — nie będziesz go pisał, tylko uruchamiał i obudowywał.

## Jak wygląda dzień

Ten sam schemat co w F2, moduł po module:

    lab start <moduł>     # przygotowuje środowisko wszystkich zadań modułu
    lab grade <moduł>     # sprawdza, czy zrobiłeś dobrze — możesz powtarzać do skutku
    lab koniec <moduł>    # zamyka moduł i przechodzi do następnego

Na starcie ustaw dzień: `lab dzien aplikacja`. Lista modułów w kolejności: `lab moduly`.

`lab grade` ocenia **cały moduł naraz**. Jeśli uruchomisz je w połowie modułu, zadania jeszcze nierobione wypadną na czerwono — to normalne, nie znaczy, że coś zepsułeś.

**O czasach przy zadaniach.** Suma zadań to 350 minut, a w planie dnia jest jeszcze **15 minut rezerwy** — bo pierwszy w życiu `venv`, pierwszy unit systemd i pierwszy restart maszyny z całą aplikacją potrafią zająć więcej, niż wygląda na papierze. Czasy są orientacyjne i nie są zakładem: jeśli któreś zadanie idzie dłużej, to nie znaczy, że robisz je źle. Znaczy tylko tyle, że po dwudziestu minutach bez postępu zapisujesz, na czym stoisz, i idziesz dalej.

**Czego `lab grade` nie robi:** nie czyta twoich notatek w poszukiwaniu właściwych słów. Sprawdza **stan maszyny** — czy proces działa, czy port nasłuchuje pod właściwym adresem, czy usługa jest włączona, czy baza ma tabele. Z notatek patrzy najwyżej na to, czy sekcja danego zadania w ogóle istnieje i ma treść. Zrozumienie sprawdzamy na obronie, w rozmowie — bo tego żaden skrypt nie zmierzy.

**Każde zadanie ma cztery części:**

- **O co tu chodzi** — po co ci to i gdzie się z tym spotkasz naprawdę.
- **Czego potrzebujesz** — czego musisz się dowiedzieć, żeby w ogóle zacząć. Są tu gotowe prompty do AI. Są napisane tak, żeby AI **wytłumaczyło ci mechanizm, a nie rozwiązało zadanie za ciebie**. Jeśli przerobisz je na „napisz mi polecenie, które…", dostaniesz gotowca i stracisz dokładnie to, po co tu jesteś. Nikt tego nie sprawdzi poza tobą.
- **Zadanie** — co masz zrobić.
- **Sprawdź się** — polecenie, które to sprawdza.

---

## Moduł: uruchom — 70 min

    lab start uruchom

### Z1. Odbierz kod i rozejrzyj się — 5 min

#### O co tu chodzi

Aplikacja przyszła do ciebie tą samą drogą co zadania — przez Gita. Tak to wygląda w pracy: kod jest w repozytorium, a nie w załączniku do maila.

Zanim cokolwiek uruchomisz, obejrzyj, co dostałeś. Pięć minut czytania struktury oszczędza pół godziny szukania pliku, o którym nie wiedziałeś, że istnieje.

#### Zadanie

    cd ~/staz
    git pull
    ls zadania/
    ls aplikacja/

Przejrzyj oba pliki `README.md` — w `aplikacja/api/` i w `aplikacja/web/`. Nie czytaj ich w całości, przelec wzrokiem sekcje.

Do notatek, trzy linijki:

1. Ile katalogów najwyższego poziomu dostałeś i za co odpowiada każdy.
2. W którym pliku leży adres API używany przez front.
3. Jedno zdanie: skąd ta aplikacja bierze konfigurację. Odpowiedź jest w `README.md` API.

**Sprawdź się:** `lab grade uruchom`

Nie zdziw się, że wyjdzie na czerwono — `lab grade uruchom` ocenia wszystkie zadania modułu naraz, a trzy masz jeszcze przed sobą.

### Z2. Środowisko wirtualne i zależności — 25 min

#### O co tu chodzi

Ta aplikacja potrzebuje pięciu bibliotek w konkretnych wersjach. Gdybyś zainstalował je globalnie, drugi projekt na tej samej maszynie wymagający innej wersji tej samej biblioteki wchodziłby z tym w konflikt — i przegrywałby jeden z nich, losowo.

Rozwiązaniem jest środowisko wirtualne: osobny katalog z własnym Pythonem i własnym kompletem bibliotek, należący do jednego projektu. To jest pierwsza rzecz, którą robisz z **każdym** projektem pythonowym, jaki w życiu dostaniesz.

Jest tu też drugie dno, prosto z F2. Aktywacja środowiska nie instaluje niczego nowego — ona **zmienia twój `PATH`**. To dokładnie ten sam mechanizm, przez który rano `df` kłamało: liczy się, który katalog jest pierwszy.

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi, czym jest środowisko wirtualne w Pythonie (`venv`): co fizycznie powstaje w katalogu `.venv`, dlaczego to rozwiązuje konflikt wersji bibliotek między projektami i co dokładnie robi polecenie `source .venv/bin/activate`. Wytłumacz szczególnie, **jak aktywacja zmienia zmienną `PATH`** i dlaczego dzięki temu `pip` instaluje pakiety w innym miejscu niż wcześniej. Nie podawaj gotowej sekwencji poleceń pod mój projekt — chcę zrozumieć mechanizm.

> Wytłumacz mi, czym jest plik `requirements.txt` i co oznacza w nim zapis `fastapi==0.141.1` w porównaniu do samego `fastapi`. Dlaczego w projektach przypina się wersje? Co się psuje, gdy tego nie zrobić, a instalacja odbywa się dwa tygodnie później na innej maszynie?

#### Zadanie

Pracujesz w `~/staz/aplikacja/api` — wszystkie polecenia tego modułu uruchamiasz stamtąd.

1. **Zanim** cokolwiek utworzysz, zapisz wynik `which python3` i `which pip`. To jest punkt odniesienia.
2. Utwórz środowisko wirtualne i aktywuj je. Instrukcja jest w `README.md` API, sekcja „Uruchomienie".
3. Po aktywacji zapisz jeszcze raz wynik obu poleceń z punktu 1 oraz `echo $PATH`. **Porównaj z punktem 1 i napisz jednym zdaniem, co się zmieniło.**
4. Zainstaluj zależności z `requirements.txt`.
5. Sprawdź, że biblioteki są na miejscu: `pip list | wc -l` oraz `python -c "import fastapi; print(fastapi.__version__)"`.

**Do notatek:** czym różni się „zainstalowałem bibliotekę" od „aktywowałem środowisko"? Jedno zdanie, bez zaglądania do AI — masz w punkcie 3 wszystko, czego trzeba.

**Uwaga na później:** aktywacja obowiązuje **w tej sesji powłoki**. Nowa zakładka SSH to nowa sesja i tam środowiska nie ma. To ta sama ulotność, o której pisałeś w F1.

**Sprawdź się:** `lab grade uruchom`

### Z3. 🔮 Uruchomienie bez jednego kroku — 25 min

#### O co tu chodzi

Uruchomisz teraz aplikację **celowo pomijając jeden krok z instrukcji** — ten o strukturze bazy danych. Robimy to specjalnie, bo tak wygląda najczęstsza pomyłka przy pierwszym wdrożeniu: ktoś skopiował kod, uruchomił proces, zobaczył, że wstał, i poszedł do domu.

Stawka jest taka: za chwilę zapiszesz trzy przewidywania i uruchomisz aplikację, której **czegoś brakuje**. Pytanie brzmi, czy to zauważysz, i czy narzędzie, którym się to zwykle sprawdza, w ogóle jest w stanie ci to powiedzieć. Jutro, pojutrze i za rok będziesz stawał przed tym samym pytaniem: **czym właściwie jest dowód, że aplikacja działa** — i ile taki dowód jest wart.

To zadanie jest oznaczone 🔮. W F1 napisałeś przewidywanie o dysku, nie trafiłeś i **nie poprawiłeś go po fakcie** — dokładnie o to chodzi. Zrób tak samo.

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi, czym jest endpoint `/health` w aplikacji webowej: kto go odpytuje, po co i jak taki endpoint jest zwykle zbudowany od środka. Kto decyduje, jak głęboko ma sięgać — samo „proces żyje", połączenie z bazą, czy coś więcej? Jaki jest koszt każdego z tych wariantów? Nie odnoś się do mojej aplikacji — nie znasz jej.

> Wytłumacz mi, czym są migracje bazy danych i po co istnieje narzędzie takie jak Alembic. Co takie narzędzie robi przy pierwszym uruchomieniu i skąd wie, co ma zrobić. Dlaczego struktury tabel nie tworzy się ręcznie na serwerze, tylko trzyma się ją w repozytorium razem z kodem? Chcę zrozumieć sens, nie dostać listy poleceń.

#### Zadanie

**Zapisz przewidywania, zanim cokolwiek uruchomisz** — trzy odpowiedzi tak/nie, każda z jednym zdaniem uzasadnienia:

1. Aplikacja uruchomiona bez utworzenia struktury bazy — w ogóle wstanie?
2. `curl http://127.0.0.1:8000/health` — co odpowie?
3. `curl http://127.0.0.1:8000/api/links` — co odpowie?

Teraz sprawdź:

1. W pierwszej sesji uruchom aplikację: `python -m app`. **Pomiń krok o migracji z README** — do niego wrócisz w następnym zadaniu. Zostaw ją uruchomioną, zajmie ci całe okno.
2. W drugiej sesji odpytaj `/health`. Zapisz **całą** odpowiedź.
3. Tam samą sesją odpytaj `/api/links`. Zapisz **całą** odpowiedź.
4. Wróć do pierwszego okna i **przeczytaj log od pierwszej linii**. Znajdź linię, która mówi, co jest nie tak, i przepisz ją do notatek dosłownie.
5. Znajdź w logu również ślad po żądaniu z punktu 3 i przepisz z niego tę linię, która mówi coś konkretnego o bazie danych.

**Do notatek, dwa zdania:**

- Dlaczego odpowiedź `/health` była myląca — co ten endpoint faktycznie sprawdził, a czego nie sprawdził.
- Odpowiedź dla klienta brzmiała „szczegóły znajdziesz w logach aplikacji". Napisz, dlaczego aplikacja nie odsyła szczegółów błędu do przeglądarki, tylko chowa je w logu.

**Sprawdź się:** `lab grade uruchom`

### Z4. Migracja, `/docs` i pierwszy link — 15 min

#### O co tu chodzi

Naprawiasz to, co znalazłeś w Z3, i pierwszy raz używasz aplikacji zgodnie z przeznaczeniem. Przy okazji zobaczysz `/docs` — interaktywną dokumentację, którą FastAPI generuje sam z kodu. To jest miejsce, do którego zajrzysz zawsze, gdy dostaniesz cudze API i nikt ci nie powie, co ono umie.

#### Czego potrzebujesz

Nic nowego — instrukcja jest w `README.md` API, a przykłady wywołań `curl` masz tam gotowe. Jeśli składnia `curl -X POST` z nagłówkiem i treścią jest dla ciebie nowa:

> Wytłumacz mi, co robią przełączniki `-X`, `-H` i `-d` w poleceniu `curl` i jak wygląda żądanie POST wysyłane w ten sposób „od środka": co idzie w linii żądania, co w nagłówkach, a co w treści. Wytłumacz też, po co przy wysyłaniu JSON-a podaje się nagłówek `Content-Type`. Bez układania polecenia pod moje API.

#### Zadanie

1. Zatrzymaj aplikację (`Ctrl+C`). **Zanim** wykonasz brakujący krok, zapisz wynik `ls -l links.db` — tak, ten plik już tam jest. Wykonaj brakujący krok z README i wypisz `ls -l links.db` jeszcze raz. Zapisz obie wartości i odpowiedz jednym zdaniem: skoro plik istniał już wcześniej, to co właściwie zrobił brakujący krok?
2. Uruchom aplikację ponownie. **Porównaj log startowy z tym z Z3** — jedno ostrzeżenie zniknęło. Które?
3. Powtórz oba wywołania `curl` z Z3. Zapisz, co się zmieniło.
4. Utwórz link do dowolnego adresu i zapisz zwrócony kod.
5. Wywołaj przekierowanie `curl -i http://127.0.0.1:8000/r/<twój-kod>`. Zapisz kod odpowiedzi HTTP i nagłówek `Location`.
6. Odpytaj ten link jeszcze raz przez `/api/links/<twój-kod>`. **Co się zmieniło w odpowiedzi po wywołaniu przekierowania?**
7. Otwórz w przeglądarce **na VM-ce**… i tu jest problem: ta maszyna nie ma przeglądarki. Zamiast tego sprawdź, że `/docs` odpowiada: `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/docs`. Do `/docs` wejdziesz oczami po module `konfiguracja` — wtedy będzie widoczne z Windowsa.

**Do notatek:** w punkcie 5 dostałeś kod `307`, a nie `301`. W README API jest wyjaśnione dlaczego. Przepisz ten powód własnymi słowami — w jednym zdaniu, bez cytowania.

**Sprawdź się:** `lab grade uruchom`

<!-- -->

    lab grade uruchom
    lab koniec uruchom
    cd ~/staz && git add notatki/ && git commit -m "docs: modul uruchom" && git push

---

## Moduł: konfiguracja — 60 min

    lab start konfiguracja

### Z5. Ta sama aplikacja, inne ustawienia — 20 min

#### O co tu chodzi

W F2 na pytanie o zmienne środowiskowe napisałeś „nie wiem", a potem sam sprawdziłeś, że `export TRYB=test` znika po rozłączeniu sesji. Dziś zobaczysz, po co to komu.

Ta aplikacja **nie ma pliku konfiguracyjnego**. Cała jej konfiguracja przychodzi ze zmiennych środowiskowych i to nie jest kaprys autora: dzięki temu ten sam, niezmieniony kod działa na twojej maszynie, na serwerze testowym i na produkcji, różniąc się wyłącznie ustawieniami. Gdyby adres bazy siedział w kodzie, każde środowisko wymagałoby innej wersji kodu — a hasło wpisane w kod zostaje w historii repozytorium **na zawsze**, także po jego usunięciu.

Za trzy zadania ta sama wiedza posłuży ci do naprawienia CORS-a. Za pięć — do napisania usługi systemd.

#### Czego potrzebujesz

> Wytłumacz mi, na czym polega przekazywanie konfiguracji do programu przez zmienne środowiskowe. Czym różni się zapis `ZMIENNA=wartosc polecenie` od `export ZMIENNA=wartosc` wykonanego wcześniej? Jak długo żyje każda z tych wartości i który proces ją widzi? Wytłumacz też, co dziedziczy proces potomny po procesie, który go uruchomił. Pokaż przykłady na dowolnym programie, nie na moim.

> Wytłumacz mi, po co program ma regulowany poziom logowania (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Co się dzieje, gdy zostawi się `DEBUG` na produkcji — wymień konkretne konsekwencje, także te niezwiązane z wydajnością. Kiedy poziom podnosi się do `DEBUG` i na jak długo?

#### Zadanie

Aplikację uruchamiaj w pierwszej sesji, sprawdzaj w drugiej. Po każdym uruchomieniu **czytaj pierwsze linie logu** — jest w nich komplet ustawień, z którymi aplikacja wystartowała.

1. Uruchom aplikację na porcie **9000**, nie zmieniając żadnego pliku. Potwierdź `curl`-em, że odpowiada pod nowym portem, a pod `8000` już nie.
2. Uruchom ją z `LOG_LEVEL=DEBUG`. Odpytaj `/health` i porównaj, ile linii pojawiło się w logu w porównaniu do poprzedniego uruchomienia. Jedno zdanie: co dokładnie doszło.
3. Uruchom **dwie kopie naraz**, na dwóch różnych portach, z różnymi wartościami `APP_NAME`. Sprawdź, że po logu poznajesz, która z nich odpowiedziała.
4. Spróbuj uruchomić aplikację z `LOG_LEVEL=GADATLIWY`. Zapisz **dosłownie**, co się stało, i odpowiedz jednym zdaniem: czy to dobrze, że aplikacja w takiej sytuacji nie wstaje?
5. Zatrzymaj wszystkie kopie. Potwierdź, że żaden port nie został zajęty — tak, jak sprawdzałeś to w F2.

**Do notatek:** punkt 4 to jest wzorzec zwany „fail fast". Napisz w dwóch zdaniach, co byłoby gorsze od niewstania: wypisz konkretny scenariusz, w którym aplikacja startuje z błędną konfiguracją i problem wychodzi dopiero po godzinie.

**Sprawdź się:** `lab grade konfiguracja`

### Z6. `.env` — konfiguracja, która nie trafia do repozytorium — 15 min

#### O co tu chodzi

Wpisywanie sześciu zmiennych przed każdym uruchomieniem jest nie do zniesienia po trzecim razie. Standardowe rozwiązanie to plik `.env` z wartościami dla twojej maszyny — **wczytywany do środowiska powłoki, nie czytany przez aplikację**. Ta różnica jest istotna: aplikacja nadal nie wie nic o żadnym pliku, a więc na serwerze to samo zadziała bez `.env`, z wartościami wstrzykniętymi przez systemd albo kontener.

Drugi powód jest z twojego podwórka. W F2 odpowiadałeś na pytanie, kto zobaczy klucz API wpisany do pliku `.js`. Tu jest siostrzana pułapka po stronie serwera: `.env` z prawdziwym hasłem, przypadkiem dodany do repozytorium. Popełnia się to raz i pamięta latami, bo z historii Gita tego się już porządnie nie usuwa.

#### Czego potrzebujesz

> Wytłumacz mi, czym jest plik `.env` w projekcie i dlaczego mimo istnienia takiego pliku mówi się, że aplikacja czyta konfigurację ze zmiennych środowiskowych. Kto właściwie wczytuje ten plik? Wytłumacz też, co robią polecenia `set -a` i `set +a` w Bashu i dlaczego samo `source .env` bez nich może nie wystarczyć. Bez gotowca pod mój projekt.

> Wytłumacz mi, dlaczego usunięcie pliku z sekretem i zrobienie kolejnego commita **nie usuwa go z repozytorium**. Co dokładnie zostaje i kto to zobaczy? Co się robi, gdy hasło jednak trafiło na zdalne repozytorium — jaka jest pierwsza czynność?

#### Zadanie

1. Przeczytaj `.env.example`. To jest **dokumentacja**, nie konfiguracja — aplikacja tego pliku nie czyta. Zapisz, ile zmiennych opisuje i która z nich jest domyślnie pusta.
2. Zrób z niego kopię roboczą `.env` i ustaw w niej `APP_PORT=8000` oraz `LOG_LEVEL=DEBUG`.
3. Wczytaj `.env` do środowiska sesji i uruchom aplikację **bez** podawania czegokolwiek w linii poleceń. Potwierdź w logu startowym, że ustawienia zostały przyjęte.
4. Sprawdź, czy `.env` trafi do repozytorium: `cd ~/staz && git status`. Zapisz wynik i **wyjaśnij go** — nie wystarczy napisać „nie trafi", napisz dlaczego. Podpowiedź: w katalogu API jest plik, który o tym decyduje.
5. Otwórz drugą sesję SSH i w niej sprawdź `echo $APP_PORT`. Zapisz wynik i jedno zdanie: dlaczego taki.

**Do notatek:** trzy miejsca, z których ta aplikacja może dostać wartość `APP_PORT` — wymień je i uszereguj od najbardziej ulotnego do najtrwalszego. Jedno z nich poznasz dopiero w module `usluga`; zostaw na nie miejsce i wróć tu później.

**Sprawdź się:** `lab grade konfiguracja`

### Z7. 🔮 Działa u ciebie, nie widać z Windowsa — 25 min

#### O co tu chodzi

Aplikacja działa. Odpowiada na `curl` z tej samej maszyny. A z przeglądarki na twoim Windowsie — nie otworzy się. Proces żyje, port jest zajęty, nic nie jest zepsute.

To jest dokładnie ta sama sytuacja, którą rozbierałeś w F2 na serwerze uruchamianym jednym poleceniem. Różnica jest jedna i tylko jedna: **tu nie ma żadnego przełącznika w linii poleceń, który mógłbyś dopisać**. Ta aplikacja adres nasłuchu bierze z konfiguracji — i to jest jej normalne, docelowe zachowanie, a nie ułatwienie na potrzeby ćwiczenia. Tak są zbudowane wszystkie aplikacje, z którymi będziesz pracował.

Nagrodą jest `/docs`: interaktywna dokumentacja API, w której każdy endpoint wywołasz przyciskiem. Zobaczysz ją w chwili, gdy aplikacja stanie się widoczna z twojej przeglądarki.

#### Czego potrzebujesz

Wszystko, czego potrzebujesz merytorycznie, przerabiałeś w F2 — nie proś AI o powtórkę, jeśli pamiętasz. Jeśli nie pamiętasz:

> Wytłumacz mi jeszcze raz różnicę między nasłuchiwaniem serwera na `127.0.0.1` a na `0.0.0.0`. Nie chodzi mi o gotową komendę — chcę móc sam powiedzieć, dlaczego serwer widoczny z tej samej maszyny bywa niewidoczny z innej, mimo że proces działa i port jest otwarty.

Przyda się natomiast rzecz nowa: skąd wiadomo, **co aplikacja faktycznie wzięła**, gdy nie wierzysz już własnym założeniom.

> Wytłumacz mi, dlaczego dobrze napisana aplikacja wypisuje przy starcie komplet swojej konfiguracji do logu. Jakie klasy problemów to rozwiązuje w praktyce i dlaczego to jest pierwsze miejsce, do którego sięga administrator, a nie ostatnie? Wytłumacz też, czego takiego loga NIE wolno wypisywać.

#### Zadanie

**Zapisz trzy przewidywania, zanim cokolwiek sprawdzisz** — przy każdym jedno zdanie, dlaczego tak sądzisz:

1. `curl http://127.0.0.1:8000/health` z drugiej sesji SSH na VM-ce — zadziała?
2. Przeglądarka na Windowsie pod `http://192.168.56.X:8000/docs` — zadziała?
3. Przeglądarka na Windowsie pod `http://localhost:8000/docs` — zadziała?

Teraz:

1. Uruchom aplikację z domyślnymi ustawieniami i sprawdź wszystkie trzy przewidywania.
2. W drugiej sesji wypisz nasłuchujące porty i **przepisz do notatek kolumnę z adresem nasłuchu** dla portu 8000.
3. Znajdź w logu startowym linię, która **mówi ci wprost**, dlaczego aplikacja jest niewidoczna z innej maszyny. Przepisz ją.
4. Doprowadź do tego, żeby `/docs` otworzyło się w przeglądarce na Windowsie. **Nie zmieniasz ani jednego pliku aplikacji** i nie ruszasz sieci w VirtualBoksie — zmieniasz jedną wartość konfiguracji.
5. Ponownie wypisz nasłuchujące porty i przepisz tę samą kolumnę. Porównaj z punktem 2.
6. W `/docs` rozwiń `POST /api/links`, kliknij „Try it out" i utwórz link z przeglądarki. Zapisz, jaki kod odpowiedzi zwróciło.

**Do notatek:** zmień wartość tej zmiennej w `.env` (jest tam już od Z6, przyszła z `.env.example`), żeby nie podawać jej za każdym razem. I odpowiedz na jedno pytanie: przewidywanie numer 3 — dlaczego wynik był taki, a nie inny? Bez sformułowania „sieć lokalna".

**Sprawdź się:** `lab grade konfiguracja`

<!-- -->

    lab grade konfiguracja
    lab koniec konfiguracja
    cd ~/staz && git add notatki/ && git commit -m "docs: modul konfiguracja" && git push

---

## Moduł: cors — 55 min

    lab start cors

### Z8. Front na własnym porcie — 15 min

#### O co tu chodzi

Do tej pory API odpytywałeś `curl`-em i przez `/docs`. Teraz podłączasz do niego prawdziwy front — HTML, CSS i `fetch()`, czyli twoje podwórko. Z jedną różnicą wobec wszystkiego, co robiłeś wcześniej: **to ty stawiasz oba końce naraz** i możesz zajrzeć po obu stronach.

Front nie ma własnego backendu ani bazy. Jest to komplet czterech plików statycznych, które przeglądarka pobiera z jednego serwera, a wszystkie dane dociąga sama, już z przeglądarki, z zupełnie innego miejsca. To rozdzielenie jest sednem dzisiejszego modułu.

Tego zadania nie naprawiasz — masz doprowadzić do stanu, w którym strona się otwiera i czegoś nie umie. Naprawa jest w Z9.

#### Czego potrzebujesz

> Wytłumacz mi, czym różni się serwer statyczny (podający pliki HTML, CSS, JS) od serwera API. Co się dzieje krok po kroku, gdy przeglądarka otwiera stronę z jednego serwera, a ta strona wywołuje `fetch()` pod adres drugiego serwera — kto z kim się łączy i ile jest tych połączeń? Rysuj to słowami, nie podawaj mi konfiguracji.

#### Zadanie

Aplikacja API ma być uruchomiona i widoczna z Windowsa — tak, jak zostawiłeś ją po Z7.

1. W trzeciej sesji SSH (tak, trzeciej — pierwsza to API, druga to twoje sprawdzanie) uruchom serwer statyczny frontu na porcie **3000**, z katalogu `~/staz/aplikacja/web`. Instrukcja jest w `README.md` frontu.
2. Ustaw w `config.js` adres API. Uwaga: przeglądarka jest na **Windowsie**, więc adres musi być taki, pod którym Windows widzi twoją VM-kę. To nie jest ten sam adres, którego używasz w `curl`-u na VM-ce.
3. Otwórz `http://192.168.56.X:3000` w przeglądarce na Windowsie. Jeśli strona w ogóle się nie otwiera, to jeszcze nie jest zadanie z Z9 — sprawdź po kolei najprostsze rzeczy: czy serwer frontu naprawdę wstał i nie wywrócił się z błędem, czy port **3000** nasłuchuje i czy wpisałeś ten adres, o którym mowa w punkcie 2. Adres nasłuchu odpada: `python3 -m http.server` domyślnie przyjmuje połączenia ze wszystkich interfejsów, więc problem z Z7 tu nie wraca.
4. Strona się otworzy, ale **API będzie dla niej niedostępne**. Zapisz do notatek:
   - dokładną treść komunikatu na pasku stanu u góry strony,
   - dokładną treść komunikatu z listy linków,
   - adres API, który strona wypisuje w nagłówku i w stopce.
5. Wciśnij `F12`, przejdź na zakładkę konsoli, odśwież stronę i **przepisz oryginalny komunikat przeglądarki** — cały, razem z nazwą nagłówka, który się w nim pojawia.

**Do notatek, zanim przejdziesz dalej:** jedno zdanie z przewidywaniem — czy `curl http://192.168.56.X:8000/health` wykonany na VM-ce zadziała? Nie sprawdzaj jeszcze.

**Sprawdź się:** `lab grade cors`

### Z9. To jest ten CORS — 40 min

#### O co tu chodzi

To jest **twoje** zadanie tego dnia i punkt kulminacyjny całego fundamentu.

W quizie, zapytany o ostatnią awarię, jaką pamiętasz, odpowiedziałeś jednym słowem: „CORS". Nie rozwiązałeś go wtedy. W F2 zobaczyłeś go z drugiej strony na dwóch serwerach uruchamianych jednym poleceniem — ale tam nie było czego naprawić, bo `python3 -m http.server` nie ma jak wysłać nagłówka.

Dziś masz w rękach prawdziwe API z prawdziwą konfiguracją. Naprawisz to **po stronie serwera i bez dotykania kodu** — ani frontu, ani API. Po tym zadaniu przestaje to być awaria, której nie umiesz rozwiązać, i staje się dwuminutową czynnością.

Dwie rzeczy, które masz z tego wynieść i umieć powiedzieć na obronie:

- **kto podejmuje decyzję o zablokowaniu** — i dlaczego szukanie przyczyny w kodzie frontu potrafi zająć całe popołudnie,
- **co dokładnie musi się zgodzić**, żeby przeglądarka przepuściła odpowiedź.

#### Czego potrzebujesz

**Zanim zaczniesz, zapisz w notatkach jedno pytanie** — takie, na które musisz sobie odpowiedzieć, żeby w ogóle ruszyć z miejsca. Nie „jak naprawić CORS", tylko pytanie o mechanizm. To jest część zadania.

> Jestem frontendowcem i widziałem błąd CORS, ale nigdy go nie naprawiałem. Wytłumacz mi mechanizm od strony serwera: co konkretnie serwer musi odesłać w odpowiedzi, żeby przeglądarka przepuściła ją do kodu strony? Jak nazywa się ten nagłówek i co dokładnie w nim jest? Wytłumacz też, dlaczego to sam serwer decyduje, komu ufa — i czemu ustawienie tam gwiazdki jest uznawane za zły pomysł. Nie podawaj mi konfiguracji żadnego konkretnego frameworka, chcę zrozumieć kontrakt.

> Wytłumacz mi, jak czytać zakładkę „Network" w narzędziach deweloperskich przeglądarki przy diagnozowaniu takiego problemu: jak rozpoznać, że żądanie **wyszło i wróciło z serwera**, a mimo to kod strony go nie zobaczył. Co widać wtedy w kolumnie statusu, a co w zakładce z nagłówkami odpowiedzi?

#### Zadanie

Pracujesz metodą, którą ćwiczyłeś w F2: hipoteza → czym ją sprawdzam → wynik → następna hipoteza. **Ścieżkę drążenia zapisujesz na bieżąco, nie po fakcie** — to jest oceniane tak samo jak sam wynik.

Front sam wypisał ci już komunikat z nazwą brakującego nagłówka i z listą wskazówek — masz to przepisane w notatkach z Z8. **To jest punkt wyjścia, nie wynik pracy.** Wszystko poniżej wymaga rzeczy, których na ekranie nie było.

**a) Zbierz materiał dowodowy — zanim cokolwiek naprawisz.** Trzy pomiary, każdy zapisany w całości:

1. **Dwa razy to samo żądanie, raz z nagłówkiem `Origin`, raz bez.** Z VM-ki:

       curl -i http://192.168.56.X:8000/api/links
       curl -i -H 'Origin: http://192.168.56.X:3000' http://192.168.56.X:8000/api/links

   Przepisz **komplet nagłówków odpowiedzi** z obu wywołań i zaznacz różnice. Wynik może cię zdziwić — zapisz go takim, jaki jest, bez interpretowania.
2. **Zakładka `Network` w przeglądarce**, żądanie do `/health` przy jednoczesnym błędzie na stronie. Zapisz status i **komplet nagłówków odpowiedzi z zakładki `Headers`**. Uwaga: kolumna statusu zależy od przeglądarki — Chrome potrafi napisać `CORS error` albo `(failed)`, Firefox pokaże `200`. Jeśli kodu w kolumnie nie widzisz, dowodem jest zakładka `Headers` (albo pomiar z punktu 1) — nie sama nazwa w tabeli.
3. **Front twierdzi, że serwer najprawdopodobniej odpowiedział.** Skąd on to wie, skoro `fetch()` rzuca ten sam błąd przy braku serwera i przy zablokowanej odpowiedzi? Znajdź w `app.js` miejsce, które to rozstrzyga, i opisz **jednym zdaniem, na czym polega ta sztuczka**. Kodu nie zmieniasz — czytasz go.

**Do notatek, po tych trzech pomiarach i przed naprawą:** które z nich w ogóle **cokolwiek dowodzą w sprawie CORS-a**, a które potwierdzają wyłącznie, że API żyje? Wskaż i uzasadnij — to jest ta sama różnica, przez którą ludzie „naprawiają" CORS-a przez pół dnia w kodzie frontu.

**b) Rozstrzygnij trzy pary.** Definicję origin masz w komunikacie frontu; tu chodzi o jej użycie. Przy każdej parze napisz „ten sam / inny" i jedno zdanie, **która składowa** decyduje:

1. `http://192.168.56.X:3000` i `http://192.168.56.X:8000`
2. `http://localhost:3000` i `http://192.168.56.X:3000` — pytane z maszyny, na której oba adresy prowadzą do tego samego komputera
3. `http://192.168.56.X:3000` i `https://192.168.56.X:3000`

Para numer 2 wróci do ciebie w punkcie d) i na obronie. Odpowiedz na nią teraz, na piśmie, zanim poznasz wynik.

**c) Napraw — po stronie serwera, bez zmiany kodu.** Zatrzymaj API, ustaw właściwą konfigurację, uruchom ponownie. W logu startowym musi być widać, że mechanizm jest włączony i dla jakiego adresu. Odśwież stronę z pominięciem pamięci podręcznej (`Ctrl+Shift+R`) i potwierdź: pasek stanu zielony, formularz działa, lista linków się wypełnia.

**d) Próba kontrolna — obowiązkowa.** Zatrzymaj API i uruchom je ponownie, tym razem podając jako dozwolony origin `http://localhost:3000`. Odśwież stronę. Zapisz, co się stało, i wyjaśnij dlaczego — **to jest najważniejsze zdanie w całym module**. Potem przywróć poprawną wartość.

**e) Drugi dowód — tabelka na cztery pola.** Powtórz **oba** wywołania z punktu a1 przy naprawionym API i zestaw wyniki w notatkach w takiej tabelce:

    |                        | przed naprawą | po naprawie |
    | curl bez `Origin`      |               |             |
    | curl z `Origin: …3000` |               |             |

W każdej komórce wpisz jedno: czy w odpowiedzi jest nagłówek `access-control-allow-origin` i jaką ma wartość. Jedna z tych czterech komórek różni się od pozostałych — i to jest cały mechanizm w jednym obrazku.

Trzy zdania do notatek:

- W którym momencie serwer w ogóle podejmuje decyzję o wysłaniu tego nagłówka i skąd wie, komu odpowiada.
- Dlaczego `curl` **bez** nagłówka `Origin` nie jest w stanie ani potwierdzić, ani obalić naprawy CORS-a — mimo że to dokładnie ten sam adres i ten sam zasób.
- I wynikające z tego: kto blokował, skoro serwer przez cały czas odpowiadał tak samo.

**f) Utrwal konfigurację.** Zmień wartość tej zmiennej w `.env` (jest tam pusta od Z6), żeby nie podawać jej ręcznie. Za chwilę przeniesiesz to ustawienie jeszcze raz — do usługi systemd — i wtedy się okaże, czy rozumiesz, skąd aplikacja bierze zmienne.

**Do notatek, trzy zdania na koniec:**

- Kto zablokował odpowiedź i na jakiej podstawie.
- Dlaczego naprawa musiała być po stronie API, mimo że błąd zobaczyłeś w kodzie frontu.
- Wróć do swojej historii z quizu: gdybyś wtedy wiedział to, co teraz, od czego byś zaczął? Konkretnie — jakie pierwsze polecenie albo jaka pierwsza zakładka.

**Sprawdź się:** `lab grade cors`

<!-- -->

    lab grade cors
    lab koniec cors
    cd ~/staz && git add notatki/ aplikacja/web/config.js
    git commit -m "chore: adres API frontu i notatki modulu cors" && git push

W tym module jako jedynym commitujesz **coś poza notatkami**: `config.js` to plik śledzony przez Gita i zmieniłeś go w Z8. Jeśli go zostawisz niezacommitowanego, zablokuje ci zaliczenie ostatniego modułu dnia — walidator wymaga tam czystego `git status`.

---

## Moduł: usluga — 95 min

    lab start usluga

### Z10. Aplikacja jako usługa systemu — 40 min

#### O co tu chodzi

Do tej pory twoja aplikacja żyła w oknie terminala. Zamkniesz sesję SSH — zniknie. To jest cała różnica między „uruchomiłem" a „wdrożyłem", którą nazwałeś sam pod koniec F2: `nohup` załatwiał połowę, a brakowało startu po restarcie maszyny.

Brakująca połowa nazywa się **systemd** i jest tym, co na każdym serwerze linuksowym pilnuje uruchomionych rzeczy. W quizie napisałeś o usłudze w tle, że „działa, jest niewidoczna, ale coś robi" — dobra intuicja. Dziś dostajesz do niej narzędzia.

Piszesz plik z opisem: co uruchomić, z jakiego katalogu, na czyich prawach, z jaką konfiguracją i co zrobić, gdy proces padnie. Systemd bierze ten opis i realizuje go bez ciebie — także o trzeciej w nocy, gdy śpisz.

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi, czym jest systemd i czym jest „unit" typu `service`. Opisz sekcje `[Unit]`, `[Service]` i `[Install]` — co się w każdej z nich umieszcza i dlaczego akurat tam. Wytłumacz znaczenie pól `ExecStart`, `WorkingDirectory`, `User`, `Environment`, `EnvironmentFile` i `Restart`. Wytłumacz też, dlaczego w `ExecStart` podaje się ścieżkę bezwzględną i co się stanie, gdy poda się samą nazwę programu. Nie pisz mi gotowego unitu — chcę umieć go napisać sam.

> Wytłumacz mi, po co po zmianie pliku unitu wykonuje się `systemctl daemon-reload` i co dokładnie robi to polecenie. Wytłumacz też różnicę między `systemctl restart`, `systemctl reload` i ponownym `start` po `stop`. Czym różni się `systemctl status` od `systemctl is-active`?

> Wytłumacz mi, jakie środowisko dostaje proces uruchomiony przez systemd. Czy widzi zmienne, które wyeksportowałem w swojej sesji SSH? Czy czyta mój `~/.bashrc`? Z jakiego katalogu startuje, jeśli nic nie ustawię? Odpowiedz ogólnie — nie znasz mojej maszyny.

#### Zadanie

Trzeci prompt wyżej zawiera ostrzeżenie, które zaraz cię dotknie. Potraktuj je poważnie.

**Zanim cokolwiek uruchomisz, zapisz przewidywanie:** twoja aplikacja jest w tej chwili uruchomiona ręcznie w pierwszej sesji. Co się stanie, gdy w drugiej sesji wystartujesz tę samą aplikację jako usługę, nie zatrzymawszy tamtej? Jedno zdanie i **dlaczego**.

1. Napisz unit `linkbox.service`. Zapisujesz go jako **`/etc/systemd/system/linkbox.service`** — to jest katalog, w którym systemd szuka usług dodanych przez administratora, i zapis w nim wymaga `sudo`. Unit ma spełniać wszystkie poniższe warunki:
   - aplikacja działa **na twoim koncie**, nie jako `root`,
   - startuje z właściwego katalogu i właściwym Pythonem — tym ze środowiska wirtualnego,
   - dostaje **tę samą konfigurację**, którą doprowadziłeś do działania w modułach `konfiguracja` i `cors`,
   - pracuje na **codziennym** poziomie logowania, nie diagnostycznym — jeśli w `.env` został ci `DEBUG` z Z6, to jest moment, żeby to poprawić (dlaczego, wiesz z Z5),
   - po nieoczekiwanym padzie procesu wstaje sama,
   - jej log trafia do dziennika systemowego (nie musisz nic robić, żeby tak było — ale w Z13 sprawdzisz dlaczego).
2. Przeładuj konfigurację systemd i uruchom usługę. Zweryfikuj przewidywanie z góry.
3. `systemctl status linkbox` — przepisz do notatek trzy rzeczy: stan usługi, PID głównego procesu i ostatnie linie logu, które status pokazuje.
4. Potwierdź trzema niezależnymi dowodami, że to działa: `curl` na `/health` z VM-ki, `ss -tlnp` z właściwym adresem nasłuchu i **odświeżony front na Windowsie z zielonym paskiem stanu**.
5. Ubij proces aplikacji **twardo**, po PID: `kill -9 <PID>` — tak, jakby się wywrócił. Odczekaj kilka sekund i sprawdź `systemctl status` jeszcze raz. Zapisz, co się stało i **jaki PID ma teraz proces**.
6. Powtórz to samo **zwykłym** `kill <PID>`, bez `-9`. Zapisz, czy tym razem też wstała.
7. Zatrzymaj usługę przez `systemctl stop`. Zapisz, czy wstała.

**Do notatek:** trzy powyższe punkty dały (albo nie dały) trzy różne wyniki, mimo że za każdym razem proces przestał istnieć. Wyjaśnij różnicę — pomoc jest w wartości, którą wpisałeś w polu `Restart`, i w tym, czym różni się `kill -9` od `kill`. To ta sama różnica, którą opisywałeś w F2 przy sygnałach.

**Do notatek:** wróć do Z6 i uzupełnij listę miejsc, z których aplikacja może dostać `APP_PORT`. Trzecie miejsce już znasz. Napisz też, **które z tych miejsc mogą się ze sobą spotkać w jednym uruchomieniu**, a które nigdy — i dlaczego. Podpowiedź, żebyś nie szukał tam, gdzie nie ma: to pytanie o **procesy**, nie o pliki. Dla pary, która faktycznie może się spotkać, napisz, która wartość wygrywa.

**Sprawdź się:** `lab grade usluga`

### Z11. 🔮 `enable` kontra `start` — 20 min

#### O co tu chodzi

To są dwa różne polecenia, które robią dwie różne rzeczy, i mylenie ich jest jednym z najczęstszych błędów przy pierwszym wdrożeniu. Objaw jest zawsze ten sam i zawsze przychodzi w najgorszym momencie: wszystko działało tygodniami, serwer się zrestartował po aktualizacji i aplikacja nie wróciła.

Sprawdzisz to jedynym uczciwym sposobem: restartem maszyny. Dwa razy — najpierw w stanie, w jakim maszyna jest teraz, potem po jednej zmianie.

#### Czego potrzebujesz

> Wytłumacz mi różnicę między `systemctl start` a `systemctl enable` — co dokładnie robi każde z nich i w którym momencie. Co robi `enable --now`? Jak sprawdzić, czy dana usługa jest włączona do automatycznego startu, jeśli akurat nie jest uruchomiona? Wytłumacz też, co znaczy `WantedBy=multi-user.target` w sekcji `[Install]` i dlaczego bez sekcji `[Install]` polecenie `enable` nie ma czego zaczepić. Bez gotowca pod mój unit.

#### Zadanie

**Zapisz przewidywania, zanim zrestartujesz maszynę** — cztery odpowiedzi, każda z jednym zdaniem uzasadnienia:

1. Usługa `linkbox` po restarcie maszyny — będzie działać?
2. Serwer statyczny frontu na porcie 3000 — będzie działać?
3. Linki, które utworzyłeś przez `/docs` i przez front — przetrwają restart?
4. Zmienne, które wczytałeś z `.env` do swojej sesji — przetrwają?

Teraz:

1. Sprawdź i **tylko zapisz**, czy usługa jest włączona do automatycznego startu. Niczego jeszcze nie zmieniaj — chcesz zobaczyć, co się stanie przy stanie, który masz teraz.
2. Zrestartuj maszynę wirtualną.
3. Połącz się ponownie po SSH i sprawdź wszystkie cztery przewidywania. **Nie poprawiaj przewidywań** — dopisz wyniki obok.
4. Punkt 2 przewidywań to jest lekcja, nie usterka. Napisz jednym zdaniem, czego brakuje frontowi, żeby zachowywał się jak API. Nie rób tego jeszcze — samo nazwanie wystarczy.
5. Dopiero teraz włącz usługę do automatycznego startu i **zrestartuj maszynę drugi raz**. Zapisz, czym ten restart różnił się od poprzedniego — jednym zdaniem, o usłudze `linkbox`.
6. Przywróć front do działania, żeby móc pracować dalej.

**Do notatek, dwa zdania:**

- Czym różni się `start` od `enable` — własnymi słowami, bez cytowania dokumentacji.
- Dane, które utworzyłeś dzisiaj, przetrwały restart maszyny. W F1 ułożyłeś hierarchię trwałości: zmienna powłoki, `tmpfs`, dysk. Dopisz do niej dzisiejsze piętro i powiedz, gdzie w tej hierarchii leży plik `links.db`.

**Sprawdź się:** `lab grade usluga`

### Z12. Cudza usługa, która nie wstaje — 35 min

#### O co tu chodzi

Dostajesz gotowy unit, którego ktoś nie dokończył: opis środowiska testowego, drugiej instancji tej samej aplikacji. Nie wstaje i nikt ci nie mówi dlaczego.

Nie ma tu ani jednej nowej rzeczy — wszystko, czego potrzebujesz, robiłeś dziś już co najmniej raz. Pytanie brzmi, czy potrafisz **wybrać właściwe narzędzie, gdy nikt nie mówi którego użyć**, i czy zaczynasz od czytania komunikatu, a nie od zgadywania. To jest umiejętność, na której stoi cała reszta stażu.

Uwaga na najczęstszą pułapkę: to nie jest jedna usterka. Naprawienie pierwszej odsłoni następną, a komunikat po drodze się **zmieni**. Jeśli po poprawce dostajesz inny błąd niż wcześniej — to jest postęp, nie porażka.

#### Czego potrzebujesz

**Zanim zaczniesz, zapisz w notatkach jedno pytanie**, które zadałbyś autorowi tego unitu, gdyby siedział obok. Konkretne, nie „co jest nie tak".

> Wytłumacz mi metodę pracy z usługą systemd, która nie chce wstać: od którego polecenia zaczynam, jak odczytać z niego, czy problem jest w konfiguracji unitu, czy w samej aplikacji, i gdzie szukać pełnej treści błędu, gdy `systemctl status` pokazuje tylko kilka ostatnich linii. Wytłumacz też, jak podejrzeć **finalną, obowiązującą** treść unitu, którą widzi systemd — bo nie zawsze jest identyczna z plikiem, który otwieram edytorem. Odpowiadaj ogólnie, nie znasz mojego przypadku.

> Wytłumacz mi, jak czytać stan usługi w `systemctl status`: co oznaczają `active (running)`, `failed`, `activating`, `inactive (dead)`, co to jest kod wyjścia procesu i jak rozpoznać, że usługa uruchamia się w kółko, zamiast po prostu nie wstać. Bez odnoszenia się do mojej usługi.

**Czego nie rób:** nie wklejaj AI całej zawartości unitu z prośbą „napraw to". Dostaniesz gotowca i stracisz jedyne zadanie w tym module, które sprawdza, czy potrafisz sam.

#### Zadanie

W `/etc/systemd/system/` leży `linkbox-staging.service` — opis drugiej instancji tej samej aplikacji, środowiska testowego. Usługa nie wstaje.

**Zanim cokolwiek uruchomisz:** przeczytaj unit i zapisz, co według ciebie zawiedzie. Dopiero potem sprawdzaj.

**Zasady:**

- **Nie zatrzymujesz `linkbox.service`.** Obie instancje mają na koniec działać jednocześnie.
- Nie kopiujesz kodu aplikacji w nowe miejsce i nie tworzysz drugiego środowiska wirtualnego — poprawiasz to, co jest.
- Nie przepisujesz unitu od zera.
- Dla **każdej** napotkanej przeszkody zapisujesz osobno: komunikat (dosłownie), przyczynę, poprawkę.

**Stan docelowy:** obie usługi działają naraz, każda na własnym porcie, obie odpowiadają na `/health` z VM-ki, a `systemctl is-active` dla obu zwraca `active`.

**Do notatek na koniec, trzy rzeczy:**

- Ile było usterek i jaka była każda z nich — osobno, po kolei.
- Które polecenie dało ci najwięcej informacji i w którym momencie.
- Obie instancje pracują na tej samej bazie danych. Utwórz link przez jedną z nich i odczytaj go przez drugą. Jedno zdanie: dlaczego to działa i co by się stało, gdyby każda instancja trzymała dane w swojej pamięci.

**Sprawdź się:** `lab grade usluga`

<!-- -->

    lab grade usluga
    lab koniec usluga
    cd ~/staz && git add notatki/ && git commit -m "docs: modul usluga" && git push

---

## Moduł: logi — 55 min

**Ten jeden moduł ma `lab start` w środku, nie na początku.** Z13 pracuje na tym, co już masz na maszynie, i niczego nie potrzebuje; polecenie `lab start logi` uruchamiasz dopiero przed Z14, w miejscu, w którym jest wypisane. Nie wyprzedzaj go — kolejność jest tu częścią zadania.

### Z13. Dziennik jednej usługi — 20 min

#### O co tu chodzi

Twoja aplikacja nie pisze do żadnego pliku z logiem. Wypisuje wszystko na standardowe wyjście i **świadomie nie decyduje, gdzie to trafi** — decyduje o tym to, co ją uruchomiło. Uruchomiona z terminala pisze na ekran; uruchomiona przez systemd trafia do dziennika systemowego; uruchomiona w kontenerze — do logu kontenera. To jest reguła, nie właściwość tej jednej aplikacji, i dzięki niej ta sama aplikacja daje się utrzymywać wszędzie.

W F2 poznałeś `journalctl` i `tail -f` na dzienniku całego systemu. Dziś zawężasz go do jednej usługi — bo na prawdziwym serwerze dziennik ma tysiące linii na minutę i oglądanie całości nie jest żadną metodą.

#### Czego potrzebujesz

> Wytłumacz mi, dlaczego dobrze napisana aplikacja serwerowa pisze logi na standardowe wyjście, zamiast sama zakładać plik z logiem. Kto wtedy odbiera te logi i co się dzięki temu upraszcza przy usłudze systemd i przy kontenerze? Wytłumacz też, co by się popsuło, gdyby aplikacja pisała do własnego pliku.

> Wytłumacz mi opcje `journalctl`, których używa się najczęściej przy jednej usłudze: `-u`, `-f`, `-n`, `-b`, `--since`, `-p` i `--no-pager`. Co robi każda z nich i jak się je łączy? Wytłumacz osobno, czym różni się ograniczenie wyniku do **ostatnich N linii** od ograniczenia go **do bieżącego uruchomienia systemu** — i kiedy które z nich jest tym właściwym. Wytłumacz też, czym różni się `journalctl -f` od `tail -f` na pliku i dlaczego dziennik systemowy przeżywa restart maszyny, a proces piszący na ekran nie. Nie układaj polecenia pod moją usługę.

#### Zadanie

Pracujesz na dwóch sesjach: w jednej patrzysz, w drugiej robisz.

1. Wypisz dziennik swojej usługi **od startu maszyny** (`journalctl` ma na to osobny przełącznik — szukaj go w promptach wyżej) i przeczytaj **pierwsze** linie, nie ostatnie. Znajdź linie startowe z kompletem konfiguracji i przepisz do notatek tę, która mówi o mechanizmie CORS.

   Zwróć uwagę, dlaczego to **nie może** być „ostatnie 30 linii": twój front odpytuje `/health` co piętnaście sekund i każde takie odpytanie zostawia wpis. Policz sam, ile wpisów uzbierało się od restartu maszyny w Z11, i zapisz tę liczbę — to jest odpowiedź na pytanie, czemu na serwerze nie ogląda się dziennika „od końca".
2. Włącz podgląd na żywo dziennika tej usługi. W drugiej sesji utwórz link `curl`-em i odśwież front na Windowsie. Opisz, co pojawiło się w pierwszym oknie i **czym te wpisy różnią się od siebie**.
3. Zawęź dziennik do wpisów **z dzisiaj** i policz je. Potem zawęź do samych błędów i porównaj liczby. Pusty wynik też jest wynikiem — jeśli błędów nie ma ani jednego, zapisz jedno zdanie, gdzie w takim razie wylądował błąd `500`, który widziałeś rano w Z3.
4. Znajdź w dzienniku ślad po Z12 — moment, w którym druga usługa nie chciała wstać. Zapisz polecenie, którym go znalazłeś.
5. Złóż jedno polecenie, które pokazuje **na żywo** wyłącznie te linie dziennika twojej usługi, w których pada słowo `health`. To jest to samo składanie, które ćwiczyłeś w F2.
6. Podnieś usłudze poziom logowania do `DEBUG` — **trwale, przez konfigurację usługi**, a nie na jedno uruchomienie. Przeładuj konfigurację, zrestartuj usługę, wykonaj jedno żądanie i zapisz, o ile więcej linii pojawiło się w dzienniku.
7. **Wróć do poprzedniego poziomu logowania**, ponownie przeładuj i zrestartuj usługę, a na koniec potwierdź `systemctl is-active linkbox`. Jedno zdanie do notatek: dlaczego `DEBUG` nie zostaje na stałe.

**Sprawdź się:** `lab grade logi`

Z14 wypadnie tu na czerwono — jeszcze go nie zacząłeś. Tak ma być.

<!-- -->

    lab start logi

### Z14. Kumulacja: usługa działa, aplikacja nie — 35 min

#### O co tu chodzi

To jest końcówka dnia i jego sens naraz.

Rano zobaczyłeś aplikację, która twierdziła, że jest zdrowa, i nie działała. Teraz masz to samo, tylko o piętro wyżej i bez żadnej podpowiedzi, czego dotyczy problem: **systemd mówi, że wszystko jest w porządku, a użytkownik widzi zepsutą stronę.** Nikt ci nie powie, co jest zepsute ani ile tego jest.

Nie ma tu nowego materiału. Wszystko, czego potrzebujesz, robiłeś dziś — w każdym module po kolei. Jedyne, co jest nowe, to że nikt nie mówi, w którym.

Jutro będziesz robił dokładnie to samo, tylko w kontenerze — i wtedy warstw do sprawdzenia będzie o jedną więcej.

#### Czego potrzebujesz

Niczego nowego. Jeśli w połowie poczujesz, że kręcisz się w kółko, wróć do metody z F2 i zapisuj hipotezy: **„podejrzewam X, sprawdzę to przez Y"**. Jedno zdanie przed każdym poleceniem diagnostycznym.

Jeden prompt, jeśli utkniesz na **czytaniu** stanu — nie na jego naprawianiu:

> Wytłumacz mi, jak sprawdzić, jaka konfiguracja **naprawdę** obowiązuje uruchomioną usługę systemd — nie ta, którą widzę w pliku, który sam napisałem, tylko ta, którą systemd faktycznie złożył i zastosował. Czy do jednej usługi może się dokładać konfiguracja z więcej niż jednego pliku? Jak zobaczyć ją całą i jak rozpoznać, skąd pochodzi która linia? Odpowiadaj ogólnie, nie znasz mojej usługi.

#### Zadanie

Twoja usługa `linkbox` jest uruchomiona i `systemctl is-active` mówi `active`. Front na Windowsie mimo to przestał działać.

**Zanim cokolwiek zmienisz**, zapisz w notatkach:

- co widzisz na stronie — dosłownie, oba komunikaty,
- co widzisz w konsoli przeglądarki,
- jedno przewidywanie: gdzie leży problem i dlaczego akurat tam.

**Zasady:**

- Nie zmieniasz **ani jednego pliku aplikacji ani frontu**. Adres API w `config.js` jest poprawny — to API ma wrócić tam, gdzie było, a nie front pójść za nim.
- Nie usuwasz i nie przepisujesz `linkbox.service` od zera.
- Poprawka ma być **trwała**: po `systemctl restart linkbox` stan ma się utrzymać. Zmiana, która znika po restarcie usługi, nie liczy się jako naprawa.
- Dla każdej napotkanej przeszkody zapisujesz osobno: objaw, hipotezę, czym ją sprawdziłeś, przyczynę, poprawkę.

**Stan docelowy.** Opisuję go tak, jak zobaczyłby go użytkownik — nie listą objawów, bo ich lista jest właśnie tym, co masz sam ustalić:

1. **Front na Windowsie działa w całości**: pasek stanu zielony, na liście są **te same linki, które dodałeś dzisiaj rano**, a formularz tworzy nowe i widać je po odświeżeniu.
2. **Stan przeżywa `systemctl restart linkbox`** — odśwież front jeszcze raz po restarcie usługi i sprawdź to naprawdę, nie na słowo.

Uwaga do punktu 1: pusta lista linków **nie jest** stanem docelowym, nawet jeśli strona świeci na zielono. To znaczyłoby, że aplikacja działa — tylko nie tam, gdzie leży twoja dzisiejsza praca.

**Do notatek na koniec:**

- Ile było problemów, jaki był każdy z nich i **z którego modułu dnia** pochodził.
- Które polecenie dało ci przełom i dlaczego wcześniej patrzyłeś w złe miejsce.
- Jedno zdanie o `systemctl is-active`: usługa mówiła `active` przez cały czas. Co ten stan właściwie potwierdza, a czego nie potwierdza? To jest to samo pytanie co przy `/health` rano — odpowiedz na nie jeszcze raz, teraz o piętro wyżej.

**Sprawdź się:** `lab grade logi`

<!-- -->

    lab grade logi
    lab koniec logi
    cd ~/staz && git add notatki/ && git commit -m "docs: modul logi" && git push

---

## Moduł: zamkniecie — 15 min

    lab start zamkniecie

### Z15. Zamknięcie dnia — 15 min

#### O co tu chodzi

Notatki są produktem tego dnia — nie zadania, nie polecenia, tylko one. Na obronie będziesz odpowiadał z nich, a za miesiąc, gdy ta sama awaria wróci, będą jedyną rzeczą, która ci zostanie.

Jedna rzecz szczególnie: **dzisiejsze pytania.** W F1 dwa razy na trzy napisałeś „nie mam pytań". Po dniu, w którym pierwszy raz uruchamiałeś cudzą aplikację, pisałeś unit systemd i naprawiałeś CORS-a po stronie serwera, to jest po prostu nieprawda. Pytanie nie jest przyznaniem się do niewiedzy — jest najszybszą drogą do odpowiedzi, a zdalnie to jedyny sposób, żebym wiedział, czego ci brakuje. Dziś **„nie mam pytań" nie jest dopuszczalną odpowiedzią.**

#### Czego potrzebujesz

> Wytłumacz mi, jak zapisywać notatki z rozwiązanej awarii, żeby były przydatne za miesiąc, kiedy nie będę pamiętał kontekstu. Co powinno się w nich znaleźć poza samą komendą — objaw, hipotezy, sposób sprawdzenia, wynik? Pokaż krótki przykład na dowolnej wymyślonej awarii, nie na mojej.

#### Zadanie

1. Uporządkuj `notatki/aplikacja.md` — cztery sekcje:
   - **Eksperymenty** — Z3, Z7, Z11: przewidywania kontra wyniki. Bez poprawiania przewidywań po fakcie.
   - **Diagnozy** — Z9, Z12, Z14: co było zepsute, **jak** to znalazłeś i w jakiej kolejności.
   - **Konfiguracja tej aplikacji** — jedna tabelka: zmienna, co robi, jaką wartość ustawiłeś u siebie i dlaczego. To jest strona, do której będziesz wracał przez cały staż.
   - **Trzy pytania** — konkretne, nie „wszystko jasne". Mogą dotyczyć czegoś, co dziś zadziałało, a nie rozumiesz dlaczego.

2. Oddaj pracę. Sprawdź najpierw `git status` — ma być **czysto**, łącznie z `config.js` z modułu `cors`; walidator tego modułu tego wymaga:

       cd ~/staz
       git status
       git add notatki/
       git commit -m "docs: notatki aplikacja"
       git push

3. Zalicz i zamknij moduł, a potem cały dzień:

       lab grade zamkniecie
       lab koniec zamkniecie
       lab koniec aplikacja       # raport całego dnia — pokaż go mentorowi

4. **To jeszcze nie koniec — punkty poniżej są obowiązkowe.** `lab koniec aplikacja` zapisał raport dnia w twoim repozytorium (`wyniki/aplikacja.md`), więc `git status` znowu **nie jest** czysty. Tak ma być, zaliczenie modułu już masz. Wypchnij raport osobnym commitem:

       git add wyniki/aplikacja.md
       git commit -m "docs: raport dnia aplikacja"
       git push

5. Wyłącz maszynę i zrób snapshot **`po-aplikacji`** — to punkt powrotu przed dniem z Dockerem.

**Sprawdź się:** `lab grade zamkniecie`
