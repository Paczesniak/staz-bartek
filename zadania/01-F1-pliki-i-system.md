# F1 — twoja maszyna i twoje pliki

**To jedyny dokument, który dziś czytasz.** Wszystko jest tutaj, w kolejności wykonania: od pustego laptopa do commita z notatkami. Nie szukaj nigdzie indziej.

## Cel dnia

Nauczyć się poruszać po systemie bez żadnego okienka — samym terminalem. I zrozumieć, co z zapisanych danych przeżywa wyłączenie maszyny, a co znika bezpowrotnie; ta druga rzecz wróci za dwa dni przy kontenerach i to od niej zależy, czy tamten dzień będzie łatwy.

## Zasady

- **Korzystaj z AI.** Część dzisiejszych zadań jest zbudowana tak, że AI poda ci narzędzie, ale odpowiedzi nie zna — bo nie widzi twojej maszyny. Jeden warunek: `sudo` czegoś, czego nie umiesz opisać, nie uruchamiasz nigdy.
- **Dowodem jest wynik, nie opis.** Wyniki poleceń dopisujesz do notatek przez `>>`, z nagłówkiem zadania:

      echo "== Z7 ==" >> $NOTATKI
      whoami >> $NOTATKI

  Jeśli `$NOTATKI` przestało działać po ponownym zalogowaniu — ustaw je jeszcze raz: `export NOTATKI=~/staz/notatki/f1.md`.
- **⏱ oznacza zadanie na czas.** Liczy się sprawność, nie elegancja.
- **🔮 oznacza zadanie, w którym najpierw zapisujesz przewidywanie**, a dopiero potem sprawdzasz. Przewidywanie jest częścią wyniku — nawet (a właściwie zwłaszcza) jeśli okaże się błędne.
- **Zablokowany dłużej niż 20 minut?** Zapisz w notatkach, na czym, przejdź do następnego zadania, wróć później. Rozstrzygniemy na obronie.
- **Dziś pracujesz w oknie VirtualBoksa, bez SSH i bez schowka** — polecenia przepisujesz ręcznie. To celowe; jutro dostaniesz jedno i drugie.
- Na koniec dnia commitujesz i pushujesz notatki. Commity w trakcie dnia są mile widziane.

## Jak wygląda dzień

Dzień jest podzielony na **moduły**. Każdy prowadzisz tym samym schematem:

    lab start <moduł>     # przygotowuje środowisko wszystkich zadań modułu
    lab grade <moduł>     # sprawdza, czy zrobiłeś dobrze — możesz powtarzać do skutku
    lab koniec <moduł>    # zamyka moduł i przechodzi do następnego

Przydaje się jeszcze `lab moduly` (lista modułów w kolejności, z zaznaczonym bieżącym) i `lab dzien F1` (ustawia bieżący dzień, gdyby `lab` zgubił kontekst).

**Kolejność modułów jest ustalona** — rób je po kolei, z góry na dół tego dokumentu. Walidatory nie są ukryte: możesz zajrzeć do `/opt/lab/zadania/F1/*/sprawdz.sh`, nikt tego nie liczy ani nie loguje.

### Jak zbudowane jest zadanie

Każde zadanie ma tę samą budowę i warto ją czytać po kolei, a nie skakać od razu do środka:

1. **O co tu chodzi** — po co ci ta umiejętność i kiedy naprawdę się przydaje. Dwa, trzy zdania.
2. **Czego potrzebujesz** — czego musisz się dowiedzieć, żeby zadanie w ogóle miało sens, plus **gotowe prompty do AI**. Możesz je przepisać dosłownie albo napisać własne.
3. **Zadanie** — co masz zrobić i pod jakimi warunkami.
4. **Sprawdź się** — polecenie, które oceni twoją pracę.

**Prompty są napisane tak, żeby AI wyjaśniło ci mechanizm, a nie podało gotowe polecenie** — i to jest celowe. Rozwiązanie z AI zajmie ci trzydzieści sekund i nie zostanie w głowie na dłużej niż do jutra. Zrozumienie mechanizmu zostaje. Przy okazji uczysz się pisać prompty, które uczą — to osobna umiejętność i będzie ci potrzebna przez cały staż.

Zadania rozgrzewkowe (kilkuminutowe) mają wersję skróconą — nie ma tam czego długo tłumaczyć.

Ostatnie zadanie w module kończy się dwoma poleceniami: `lab grade` (ocena) i `lab koniec` (zamknięcie modułu). Wcześniejsze zadania mają samo `lab grade` — możesz je uruchamiać po każdym zadaniu, żeby wiedzieć, na czym stoisz.

---

## Moduł: start — 120 min

**Twoje pierwsze zadanie brzmi: zdobądź dostęp do pozostałych zadań.** To nie jest formalność przed właściwą pracą — to jest właściwa praca. Po drodze poznasz maszynę wirtualną, klucze SSH i gita, czyli trzy rzeczy, których będziesz używał przez cały staż.

Ten moduł jako jedyny nie ma poleceń `lab` — lab instaluje mentor na twojej maszynie, gdy tylko będzie ona miała adres IP. Dlatego zadania Z1–Z6 sprawdzasz sam, według opisanych kryteriów. Pierwsze polecenie labu wydajesz w module `rozgrzewka`.

Od mentora dostajesz: plik ISO **Ubuntu Server 24.04 LTS** (albo link) oraz jego nazwę na GitHubie. Potrzebujesz własnego konta na GitHubie — jeśli nie masz, załóż teraz.

### Z1. Maszyna wirtualna — 75 min

#### O co tu chodzi

Aplikacje, które piszesz, na końcu lądują na serwerze — a serwer nie ma pulpitu, ikon ani menedżera plików. Zamiast prosić kogoś o taki serwer, zrobisz go sobie sam: maszyna wirtualna to komputer udawany przez program, z własnym systemem, dyskiem i kartami sieciowymi, działający w oknie na twoim Windowsie.

Przez najbliższe dni cały staż dzieje się **w środku tej maszyny**. Dlatego warto ją założyć porządnie i zrobić na koniec snapshot — to jedyny znany przycisk „cofnij" działający na cały system operacyjny naraz.

#### Czego potrzebujesz

Dwóch pojęć: wirtualizacji (czym maszyna wirtualna różni się od zwykłego programu) i trybów sieci w VirtualBoksie. Dwie karty sieciowe nie są kaprysem — każda robi co innego i za dwa dni okaże się, dlaczego bez tej drugiej nie zobaczysz swojej aplikacji z Windowsa.

> Jestem początkujący. Wytłumacz mi, czym jest maszyna wirtualna i czym różni się od zwykłego programu uruchomionego na moim komputerze — co to znaczy, że ma „własny" dysk i „własną" pamięć. Potem wyjaśnij dwa tryby sieci w VirtualBoksie: NAT i Host-only. Dla każdego powiedz, kto może się z kim połączyć i w którą stronę. Użyj analogii i nie podawaj mi instrukcji klikania — chcę zrozumieć, po co są dwie karty naraz.

Drugi prompt, o punkcie powrotu:

> Wytłumacz mi jak początkującemu, czym jest snapshot maszyny wirtualnej. Co dokładnie zostaje zapisane, czym to się różni od skopiowania pliku z dyskiem, i w jakich sytuacjach snapshot ratuje sytuację, a w jakich nie pomoże. Podaj przykłady, nie definicję ze słownika.

#### Zadanie

1. Zainstaluj VirtualBox. Nowa maszyna: **2 vCPU, 4096 MB RAM, dysk 30 GB** (dynamiczny).
2. Sieć — ustaw **przed** pierwszym uruchomieniem: **Adapter 1 = NAT**, **Adapter 2 = Host-only**.
3. Zainstaluj Ubuntu Server 24.04 LTS. W trakcie instalacji **zaznacz „Install OpenSSH server"**.
4. Zapamiętaj (albo zapisz na kartce) nazwę użytkownika i hasło, które ustawiasz — będziesz ich używał cały staż. Mentor też będzie się na tę maszynę logował.
5. Po pierwszym zalogowaniu: `sudo poweroff`, a potem w VirtualBoksie zrób **snapshot o nazwie `czysta-instalacja`**. To twój punkt powrotu, gdyby coś poszło źle.
6. Uruchom maszynę ponownie, zaloguj się i sprawdź `ip a` — adres z karty host-only (`192.168.56.X`) podaj mentorowi. Na tej podstawie zainstaluje ci lab.

To jest system bez pulpitu, bez ikon i bez menedżera plików. Tak wygląda maszyna, na której naprawdę stoją aplikacje.

#### Sprawdź się

W tym module nie ma jeszcze labu — sprawdzasz sam:

- maszyna startuje do znaku zachęty i pozwala się zalogować,
- `ip a` pokazuje adres z zakresu `192.168.56.X`,
- w VirtualBoksie na liście snapshotów widnieje `czysta-instalacja`.

### Z2. Git i przedstawienie się — 5 min

#### O co tu chodzi

Zanim git zapisze cokolwiek, musi wiedzieć, kto zapisuje — inaczej twoje commity będą anonimowe i nie zwiążą się z twoim kontem na GitHubie.

Przy okazji poznajesz menedżer pakietów: w Linuksie oprogramowania nie ściąga się ze stron przez instalator, tylko pobiera z repozytoriów systemu jednym poleceniem. W quizie napisałeś przy tym pytaniu „komendy nie pamiętam" — dziś użyjesz jej pierwszy raz, a na serio wrócimy do tego jutro.

#### Czego potrzebujesz

Jedno pytanie do AI wystarczy — reszta to przepisanie sześciu linijek:

> Wytłumacz mi jak początkującemu, czym jest menedżer pakietów w Linuksie i czym są repozytoria. Dlaczego `apt update` to co innego niż `apt install` i co się stanie, jeśli pominę pierwsze? Porównaj to z tym, jak instaluje się programy na Windowsie.

#### Zadanie

    sudo apt update
    sudo apt install -y git
    git --version
    git config --global user.name "Imię Nazwisko"
    git config --global user.email "twoj@email"
    git config --global init.defaultBranch main

Adres e-mail podaj ten sam, którym rejestrowałeś się na GitHubie — inaczej twoje commity nie będą się tam wiązać z twoim kontem.

#### Sprawdź się

`git --version` wypisuje numer wersji, a `git config --global --list` pokazuje twoje imię i adres e-mail.

### Z3. Klucz SSH — 15 min

#### O co tu chodzi

Za chwilę będziesz się łączył z GitHubem, a jutro — z maszyną po SSH. Za każdym razem trzeba jakoś udowodnić, że to ty. Hasło da się podejrzeć, przechwycić i podać dalej; klucz nie, bo jego tajna połowa nigdy nie opuszcza twojego dysku.

W quizie napisałeś o SSH: „chyba szyfrowało połączenia, nie jestem pewien" — i to była uczciwa odpowiedź. Po tym zadaniu będziesz wiedział nie tylko, że szyfruje, ale też dlaczego można komuś oddać jeden plik z pary i nic złego się nie stanie.

#### Czego potrzebujesz

Zrozumienia, że klucz to **para** plików, które robią przeciwne rzeczy, i że kierunek ma tu kluczowe znaczenie — pomyłka w tę stronę jest jednym z klasycznych błędów początkujących.

> Jestem początkujący. Wytłumacz mi, czym jest para kluczy (publiczny i prywatny) w kryptografii asymetrycznej. Który z nich komu daję, a którego nie oddaję nigdy i dlaczego? Wyjaśnij na analogii — chcę zrozumieć, dlaczego klucz publiczny może zobaczyć każdy i nic złego się nie stanie.

> Wytłumacz mi, co dzieje się krok po kroku, gdy loguję się kluczem SSH na serwer: skąd serwer wie, że to ja, skoro nie ma mojego klucza prywatnego i nigdy go nie zobaczy? Nie podawaj mi poleceń — interesuje mnie sam mechanizm.

#### Zadanie

Klucz to para plików: **publiczny** i **prywatny**.

    ssh-keygen -t ed25519 -C "staz-vm"

Przy pytaniu o hasło do klucza możesz wcisnąć Enter (bez hasła) — na maszynie stażowej to akceptowalne.

    ls -l ~/.ssh
    cat ~/.ssh/id_ed25519.pub

**Zapamiętaj tę zasadę, bo jest ważniejsza niż całe to polecenie:**

- plik **`.pub`** (publiczny) wgrywasz na GitHub — może go zobaczyć każdy, nic się nie stanie,
- plik **bez `.pub`** (prywatny) **nigdy nie opuszcza tej maszyny**. Nie wysyłasz go nigdzie, nie wklejasz do czatu, nie wrzucasz do repozytorium.

Skopiuj zawartość `.pub` i dodaj ją na GitHubie: **Settings → SSH and GPG keys → New SSH key**. Sprawdź, czy działa:

    ssh -T git@github.com

Poprawna odpowiedź zawiera „successfully authenticated" i informację, że powłoki nie dostaniesz — to normalne.

> **Jeśli polecenie się zawiesza albo zwraca „Connection timed out"** — firmowa sieć blokuje port 22. Nie walcz z tym, przejdź do sekcji „Gdy sieć blokuje port 22" na końcu tego modułu.

#### Sprawdź się

`ssh -T git@github.com` odpowiada twoją nazwą użytkownika z GitHuba i słowami „successfully authenticated".

### Z4. Repozytorium — 10 min

#### O co tu chodzi

Repozytorium jest miejscem, w którym oddajesz pracę — mentor nie będzie oglądał twojego ekranu ani czytał wiadomości z opisem, co zrobiłeś. Widzi to, co trafi na GitHuba, i tylko to.

Repozytorium ma być **prywatne**, bo poza notatkami wylądują w nim adresy, nazwy kont i szczegóły twojej maszyny. Prywatne oznacza jednak, że domyślnie nie widzi go nikt — łącznie z mentorem — więc drugi krok jest tak samo obowiązkowy jak pierwszy.

#### Zadanie

1. Na GitHubie utwórz **prywatne** repozytorium o nazwie `staz-<twoje-imię>`. Bez pliku README na start — dodasz go sam.
2. **Settings → Collaborators → Add people** → dodaj mentora. Bez tego on nie zobaczy twojej pracy, a ty nie dostaniesz zadań.
3. Powiadom mentora, że zaproszenie czeka.

#### Sprawdź się

Repozytorium widnieje na twoim koncie z etykietą „Private", a na liście współpracowników jest mentor (na razie ze statusem oczekującego zaproszenia).

### Z5. Klon i struktura — 10 min

#### O co tu chodzi

„Sklonować repozytorium" znaczy: ściągnąć jego kopię na swój dysk razem z całą historią zmian. Od tej chwili masz dwa egzemplarze — jeden lokalnie, drugi na GitHubie — i to ty decydujesz, kiedy się wyrównują.

W quizie napisałeś, że „commit zapisuje lokalnie, a push wysyła", i to była jedna z lepszych odpowiedzi w całym arkuszu. Dziś zobaczysz ten podział w praktyce, na własnym repozytorium.

#### Czego potrzebujesz

Świadomości, że plik przechodzi przez kilka stanów, zanim znajdzie się na GitHubie, i że każde z trzech poleceń przesuwa go tylko o jeden krok.

> Wytłumacz mi jak początkującemu drogę, którą przebywa plik w gicie: zapisany na dysku → `git add` → `git commit` → `git push`. Co dokładnie robi każdy z tych kroków i gdzie fizycznie leżą moje zmiany po każdym z nich? Wyjaśnij też, co pokazuje `git status` na każdym etapie. Bez gotowego zestawu poleceń do przepisania — chcę rozumieć, co się dzieje.

#### Zadanie

    cd ~
    git clone git@github.com:<twoj-login>/staz-<imie>.git staz
    cd ~/staz
    mkdir -p notatki

Utwórz w `nano` plik `README.md` — trzy, cztery zdania własnymi słowami: co to za repozytorium, co leży w `zadania/`, a co w `notatki/`.

    git add .
    git commit -m "chore: struktura repozytorium"
    git push

Wejdź na GitHuba i zobacz swój commit. **To jest cały mechanizm stażu w jednym miejscu:** to, co widzisz na GitHubie, widzi też mentor.

**Dwie zasady, które oszczędzą ci kłopotów:**

- **`zadania/` piszesz tylko ty przez `git pull`** — nie edytujesz tam nic. To katalog mentora.
- **`notatki/` to twój teren** — mentor tam nie pisze.

Gdy każdy pisze w swoim katalogu, konflikty scalania praktycznie nie występują.

#### Sprawdź się

Commit „chore: struktura repozytorium" jest widoczny na GitHubie w przeglądarce, a `git status` na maszynie mówi, że nie ma nic do wysłania.

### Z6. Zadania dnia i miejsce na wyniki — 5 min

#### O co tu chodzi

Odbierasz zadania i przygotowujesz plik, do którego przez resztę dnia będą trafiać wyniki wszystkich poleceń — bo to on jest twoim oddanym zadaniem domowym.

#### Zadanie

Gdy mentor potwierdzi, że wypchnął zadania:

    cd ~/staz
    git pull
    ls zadania/
    cat zadania/F1.md

**To ten sam dokument, który właśnie czytasz** — dostałeś go najpierw jako plik na Windowsie, bo bez repozytorium nie było jak. Od tego momentu wszystkie zadania odbierasz przez `git pull`, a wszystkie wyniki oddajesz przez `git push`.

Jeśli `zadania/` jest puste — mentor jeszcze nie wypchnął. Zawołaj go.

Teraz miejsce na wyniki:

    mkdir -p ~/praca/f1
    touch ~/staz/notatki/f1.md
    export NOTATKI=~/staz/notatki/f1.md
    echo "# Notatki F1" >> $NOTATKI
    cat $NOTATKI

Podwójna strzałka **dopisuje na końcu**. Pojedyncza (`>`) **kasuje plik i zaczyna od zera** — o tym jeszcze się dziś przekonasz. Skrót `$NOTATKI` żyje tylko w tej sesji terminala; po ponownym zalogowaniu trzeba go ustawić od nowa, a dlaczego tak jest — dowiesz się po południu.

#### Sprawdź się

`cat $NOTATKI` wypisuje linijkę `# Notatki F1`, a w `zadania/` leży plik `F1.md`.

### Gdy sieć blokuje port 22 — plan B

Firmowe sieci często zamykają port 22 na zewnątrz. Masz dwa wyjścia — wybierz jedno, drugie zostaw jako zapas.

**A. SSH przez port 443.** W `nano` utwórz plik `~/.ssh/config`:

    Host github.com
      Hostname ssh.github.com
      Port 443
      User git

    chmod 600 ~/.ssh/config
    ssh -T git@github.com

**B. HTTPS z tokenem.** Na GitHubie: **Settings → Developer settings → Personal access tokens → Fine-grained tokens**. Zakres: tylko twoje repozytorium stażowe, uprawnienia: Contents → Read and write. Skopiuj token — zobaczysz go raz.

    cd ~/staz
    git remote set-url origin https://github.com/<twoj-login>/staz-<imie>.git
    git config --global credential.helper store
    git pull        # jako login podaj nazwę użytkownika, jako hasło — token

**Token to hasło.** `credential.helper store` zapisuje go w pliku otwartym tekstem (`~/.git-credentials`). Na maszynie stażowej to akceptowalny kompromis; na produkcyjnej — nie. Jeśli kiedykolwiek wkleisz token gdzieś publicznie, natychmiast go unieważnij na GitHubie.

---

## Moduł: rozgrzewka — 8 min

    lab start rozgrzewka

### Z7. ⏱ Kim jesteś, gdzie jesteś, co masz — 8 min

#### O co tu chodzi

Pierwsza rzecz, którą robi się po zalogowaniu na cudzą albo nieznaną maszynę, to ustalenie, gdzie się właściwie wylądowało — kim jestem, na jakim hoście i czy ta maszyna w ogóle ma zasoby, żeby cokolwiek na niej uruchomić.

To zadanie jest na czas i **nie musisz znać tych poleceń z głowy** — masz obok AI i po to tu jest. Liczy się to, żeby po pięciu minutach mieć w notatkach konkretne liczby z tej maszyny, a nie ogólniki.

#### Zadanie

**Masz 5 minut.** Ustal i dopisz do notatek:

1. swoją nazwę użytkownika, nazwę maszyny, katalog, w którym startujesz, oraz do jakich grup należysz,
2. ile masz wolnego miejsca na `/`, ile RAM-u, ile rdzeni procesora,
3. w Windowsie dyski są osobnymi literami — `C:`, `D:`. Tutaj takich liter nie ma. **Jednym poleceniem** pokaż, co pełni tu ich rolę, a potem dopisz jedno zdanie porównujące oba rozwiązania. Napisz to zdanie tak, żeby padła w nim nazwa **Windows** — porównujesz dwa światy, więc nazwij oba.

Do notatek trafiają **wyniki** poleceń, a nie ich nazwy.

#### Sprawdź się

    lab grade rozgrzewka      # sprawdź, czy zrobiłeś dobrze
    lab koniec rozgrzewka     # zamknij moduł i przejdź do następnego

---

## Moduł: pliki — 57 min

    lab start pliki

### Z9. Struktura jednym poleceniem — 10 min

#### O co tu chodzi

Projekt, wdrożenie albo backup zwykle zaczyna się od katalogu z kilkunastoma podkatalogami o ustalonych nazwach. Klikanie ich po kolei to kilka minut i trzy literówki; napisane jednym poleceniem — kilka sekund i da się wkleić do skryptu, który zrobi to samo na dziesięciu maszynach.

**Sedno tego zadania to właśnie „jednym poleceniem", a nie sama struktura.** Struktura powstanie tak czy inaczej — chodzi o to, żebyś poznał mechanizm, dzięki któremu powstaje za jednym razem.

#### Czego potrzebujesz

Dwóch rzeczy: tego, co powłoka robi z twoim tekstem, **zanim** uruchomi polecenie (potrafi go rozmnożyć), oraz tego, dlaczego tworzenie katalogu wewnątrz nieistniejącego katalogu domyślnie kończy się błędem.

> Jestem początkujący w Linuksie. Wytłumacz mi, jak powłoka bash przetwarza to, co wpiszę, **zanim** uruchomi polecenie — na przykładzie rozwijania nawiasów klamrowych `{a,b,c}`. Pokaż mi 3–4 przykłady z `echo`, od najprostszego, żebym zobaczył sam wynik rozwinięcia. Wyjaśnij też, co się dzieje przy zagnieżdżeniu. Nie podawaj mi gotowego polecenia do mojego zadania.

> Wytłumacz mi, dlaczego przy tworzeniu zagnieżdżonego katalogu dostaję `No such file or directory`, skoro podałem poprawną ścieżkę. Jaka jest ogólna zasada w Uniksie: kiedy narzędzie tworzy brakujące katalogi po drodze, a kiedy odmawia? Nie podawaj mi flagi — powiedz, jak znaleźć ją samodzielnie w `man mkdir`.

#### Zadanie

Zbuduj **jednym poleceniem**:

    ~/praca/f1/
      notatki/
      smieci/
      archiwum/2024/{q1,q2,q3,q4}

**Dowód:** `ls -R ~/praca` dopisane do notatek. Jeśli użyłeś więcej niż jednego polecenia — spróbuj jeszcze raz, o to właśnie chodzi w tym zadaniu.

Lab zobaczy tylko efekt, bo w systemie plików nie zostaje ślad po tym, ile poleceń go zbudowało. O liczbę poleceń zapyta cię mentor na obronie — i to nie jest luka do wykorzystania, tylko powód, żeby zrobić to uczciwie. Umiejętność zostaje twoja, nie labu.

#### Sprawdź się

    lab grade pliki

### Z10. Cztery operacje bez `cd` — 15 min

#### O co tu chodzi

Utworzyć, skopiować, zmienić nazwę, wyświetlić, usunąć — to jest komplet codziennych operacji na plikach i będziesz je robił po kilkadziesiąt razy dziennie przez resztę kariery. W quizie z tej piątki padło tylko kopiowanie (i to pod windowsową nazwą), więc zaczynamy od zera i to jest normalne.

Zakaz `cd` nie jest złośliwością. Chodzi o to, żebyś nauczył się **wskazywać miejsca względem tego, gdzie stoisz** — bo dokładnie tak pisze się ścieżki w skryptach, w konfiguracjach i w plikach Dockera, gdzie nikt nie wie z góry, w którym katalogu wszystko wystartuje.

#### Czego potrzebujesz

Ścieżek względnych: co znaczy `.`, co znaczy `..`, jak złożyć z nich drogę do katalogu obok, a nie pod spodem.

> Jestem początkujący w Linuksie. Wytłumacz mi różnicę między ścieżką bezwzględną a względną. Co dokładnie oznaczają `.` i `..` i jak zbudować ścieżkę do katalogu, który jest „obok" mojego, a nie w środku? Narysuj przykładowe drzewo katalogów i pokaż na nim 4 ścieżki względne z tego samego punktu startowego. Nie rozwiązuj mojego zadania — chcę sam ułożyć ścieżki.

> Wytłumacz mi, dlaczego polecenie usuwające pliki odmawia usunięcia katalogu i co znaczy „rekurencyjnie" przy operacjach na katalogach. Wyjaśnij też, dlaczego to akurat tutaj jest niebezpieczne. Nie podawaj mi gotowej komendy.

**Zanim uruchomisz cokolwiek, co usuwa:** w Linuksie **nie ma kosza**. Usunięty plik jest usunięty — nie ma okna z pytaniem, nie ma „przywróć". Nawyk, który warto sobie wyrobić od dziś: najpierw ta sama ścieżka w `ls`, dopiero potem w poleceniu, które kasuje.

#### Zadanie

Stoisz w `~/praca/f1/notatki` i **nie wolno ci stamtąd wyjść**. Zakazane: `cd`, `~`, `$HOME` oraz każda ścieżka zaczynająca się od `/`. Zostają wyłącznie ścieżki liczone od miejsca, w którym stoisz.

1. Utwórz plik `plan.md` w `archiwum/2024/q3` (treść dowolna, `nano`).
2. Skopiuj go do `smieci/` pod nazwą `plan-kopia.md`.
3. Zmień nazwę `plan-kopia.md` na `plan-stary.md`.
4. Wypisz zawartość `plan-stary.md` na ekran.
5. Usuń katalog `smieci` razem z zawartością — jednym poleceniem.

**Dowód:** pięć użytych ścieżek + `ls -R ~/praca/f1`, dopisane do notatek.

**Uwaga, żeby nie było nieporozumienia:** zakaz `cd`, `~`, `$HOME` i ścieżek od `/` dotyczy **wyłącznie pięciu kroków powyżej**. Dowód wpisujesz normalnie — w `ls -R ~/praca/f1` tylda jest jak najbardziej w porządku, bo to już nie jest część ćwiczenia, tylko sposób na pokazanie wyniku.

#### Sprawdź się

    lab grade pliki

### Z11. Pliki, których nie da się usunąć po imieniu — 12 min

#### O co tu chodzi

Prędzej czy później trafisz na plik, który wygląda zwyczajnie, a nie daje się ruszyć: nazwa ze spacją, nazwa zaczynająca się od myślnika, nazwa ze znakiem zapytania. Takie pliki powstają same — z uploadu, z eksportu z Windowsa, ze źle napisanego skryptu.

To nie jest ciekawostka. To jest pierwszy moment, w którym zobaczysz, że **powłoka czyta to, co wpisujesz, zanim polecenie w ogóle wystartuje** — i że część twojego tekstu zdąży zmienić znaczenie po drodze. Ta jedna obserwacja tłumaczy potem połowę dziwnych błędów w skryptach.

#### Czego potrzebujesz

Zrozumienia, co powłoka robi z argumentami: gdzie widzi granicę między jednym a drugim, które znaki mają dla niej specjalne znaczenie i dlaczego myślnik na początku nazwy jest osobnym problemem.

> Jestem początkujący. Wytłumacz mi, co robi powłoka bash z tekstem, który wpisuję, zanim uruchomi polecenie: jak dzieli go na argumenty, po czym poznaje granicę między nimi i które znaki traktuje specjalnie (np. `*`, `?`, spacja). Pokaż na przykładach z `echo`, żebym zobaczył, ile argumentów naprawdę dostaje polecenie. Nie podawaj mi gotowych komend do usuwania plików.

> Wytłumacz mi, dlaczego polecenia uniksowe traktują argument zaczynający się od myślnika inaczej niż pozostałe, i jaka jest ogólna, przyjęta w Uniksie konwencja radzenia sobie z tym problemem. Interesuje mnie zasada i to, gdzie jej szukać w `man`, a nie gotowe polecenie.

#### Zadanie

W `~/warsztat/przychodzace/` leżą cztery pliki. Usuń trzy z nich. **Zostaw `wyniki-pomiarow.txt`** — będzie potrzebny w Z13.

Oczywiste polecenie zawiedzie przy każdym z trzech i za każdym razem z innego powodu.

**Dowód:** dla każdego z trzech plików — komunikat błędu, który zobaczyłeś, i polecenie, które w końcu zadziałało. Plus jedno zdanie: dlaczego pierwsza próba nie wyszła.

#### Sprawdź się

    lab grade pliki

### Z12. Sprzątanie po kimś — 20 min

#### O co tu chodzi

Ktoś przed tobą zrzucił do jednego katalogu trzysta plików: logi, obrazki, dane, teksty, wszystko razem. Taka sytuacja zdarza się naprawdę — po nieudanym wdrożeniu, po skrypcie, który zapisał wyniki „tymczasowo", albo po koledze, który już nie pracuje. Nikt tego nie posprząta ręcznie, plik po pliku.

Chodzi o to, żebyś nauczył się **operować na grupach plików naraz**, zamiast klikać po jednym. To jedna z tych umiejętności, która w pierwszym tygodniu oszczędza godzinę, a przez rok — kilka dni.

#### Czego potrzebujesz

Trzech rzeczy: rozpoznawania plików po nazwie (tzw. globbing, czyli `*.log`), przenoszenia wielu plików jednym poleceniem oraz sposobu na policzenie, ile ich właściwie jest.

Jeśli któraś z tych rzeczy jest dla ciebie nowa — **zapytaj AI, ale o wyjaśnienie, nie o gotowca**:

> Jestem początkujący w Linuksie. Wytłumacz mi, czym jest globbing (`*.log`, `plik?.txt`, `[abc]*`) i czym różni się od wyrażeń regularnych. Pokaż 4 przykłady od najprostszego, wyjaśnij każdy znak. Powiedz też, co się stanie, jeśli żaden plik nie pasuje do wzorca — i dlaczego to bywa niebezpieczne przy poleceniach, które usuwają.

Drugi prompt, jeśli nie wiesz, jak policzyć pliki:

> Wytłumacz mi, jak w Linuksie policzyć pliki pasujące do wzorca. Pokaż dwa różne sposoby i wyjaśnij, czym się różnią oraz który jest bezpieczniejszy przy dziwnych nazwach plików (ze spacjami, z myślnikiem na początku).

**Zanim uruchomisz cokolwiek, co usuwa** — sprawdź ten sam wzorzec poleceniem `ls`. Ten jeden nawyk uratuje ci kiedyś dzień pracy.

#### Zadanie

W `~/warsztat/` leży 300 plików wrzuconych bez ładu. Doprowadź do porządku:

- pliki `.log` → `logi/`, `.jpg` → `obrazy/`, `.csv` → `dane/`, `.txt` → `teksty/`
- wszystkie `.tmp` → usunięte
- katalog `przychodzace/` zostaje nietknięty

**Ograniczenie: maksymalnie 8 poleceń łącznie.** Przenoszenie plik po pliku odpada — jeśli robisz to pojedynczo, to znaczy, że nie używasz mechanizmu, o który chodzi w tym zadaniu.

**Dowód:** liczba plików w każdym z czterech katalogów (cztery liczby) + potwierdzenie, że nie został żaden `.tmp`.

#### Sprawdź się

    lab grade pliki
    lab koniec pliki

---

## Moduł: przekierowania — 10 min

    lab start przekierowania

### Z13. 🔮 Plik, którego nie wolno stracić — 10 min

#### O co tu chodzi

Jeden znak różnicy w poleceniu decyduje o tym, czy dopiszesz coś do pliku, czy skasujesz jego całą dotychczasową zawartość. Bez ostrzeżenia, bez pytania, bez kosza. To jest chyba najczęstszy sposób, w jaki początkujący traci dane na serwerze — i praktycznie jedyny, którego da się uniknąć czystą wiedzą.

W quizie na pytanie o `>` i `>>` napisałeś: „coś było kiedyś, ale nie przypomnę sobie". Po tym zadaniu przypomnisz sobie na zawsze, bo zrobisz to na pliku, którego naprawdę nie wolno zepsuć.

#### Czego potrzebujesz

Zrozumienia, co dokładnie dzieje się z plikiem w momencie przekierowania — i w którym momencie, bo to nie jest to samo co „na końcu polecenia".

> Jestem początkujący w Linuksie. Wytłumacz mi różnicę między `>` a `>>` przy przekierowaniu wyniku polecenia do pliku. Co dokładnie dzieje się z istniejącym plikiem w każdym z tych dwóch przypadków i w którym momencie — przed uruchomieniem polecenia czy po? Podaj przykład sytuacji, w której pomyłka kosztuje utratę danych. Nie podawaj mi gotowego polecenia do mojego zadania.

Przyda ci się też sposób na zmierzenie pliku przed zmianą i po — bez tego nie będziesz miał czego porównać z przewidywaniem:

> Wytłumacz mi, jak w Linuksie sprawdzić, ile plik tekstowy ma linii, słów i znaków. Wyjaśnij, co dokładnie liczy to narzędzie i jak zachowuje się, gdy ostatnia linia nie kończy się znakiem nowej linii. Chcę zrozumieć wynik, nie tylko go zobaczyć.

#### Zadanie

`~/warsztat/przychodzace/wyniki-pomiarow.txt` zawiera dane, których nie da się odtworzyć.

1. **Zanim cokolwiek zrobisz:** policz i zapisz, ile plik ma linii.
2. **Zapisz przewidywanie:** dopiszesz do niego trzy razy aktualną datę — ile linii będzie miał potem?
3. Wykonaj.
4. Policz linie ponownie i porównaj z przewidywaniem.
5. Jeśli liczba spadła — nie panikuj, tylko zawołaj mentora i powiedz, co się stało i jak zamierzasz to naprawić.

#### Sprawdź się

    lab grade przekierowania
    lab koniec przekierowania

---

## Moduł: ulotnosc — 35 min

    lab start ulotnosc

### Z14. 🔮 Co przeżywa wyłączenie maszyny — 25 min

#### O co tu chodzi

Najważniejsze zadanie dnia. Nie dlatego, że najtrudniejsze — dlatego, że wszystko, co robisz od pojutrza, opiera się na jednej intuicji: **niektóre dane przeżywają wyłączenie maszyny, a inne znikają, i to widać z góry, jeśli się wie, gdzie patrzeć.**

W quizie na pytanie o różnicę między RAM-em a dyskiem napisałeś, że dysk trzyma „twarde dane", a RAM „szybkie". Nie padło ani słowo o tym, że jedno z nich znika po wyłączeniu. Przy pytaniu o dane w kontenerze napisałeś „nie wiem" — to ta sama luka, tylko dwa dni później. Dziś zamykasz obie naraz, na własnych oczach, na własnej maszynie.

#### Czego potrzebujesz

Trzech pojęć: gdzie „mieszka" zmienna powłoki, czym jest system plików trzymany w pamięci i co to znaczy, że dane są trwałe.

> Jestem początkujący w Linuksie. Wytłumacz mi, czym jest zmienna powłoki: gdzie ona fizycznie istnieje, jak długo żyje i dlaczego nowe okno terminala albo nowe logowanie jej nie widzi. Wyjaśnij przy okazji, co to znaczy, że proces ma własne środowisko. Bez gotowych poleceń — chcę zrozumieć mechanizm.

> Wytłumacz mi, czym jest system plików typu `tmpfs` i czym różni się od zwykłego systemu plików na dysku. Dlaczego coś, co wygląda w terminalu jak zwykły katalog z plikami, może w rzeczywistości leżeć w pamięci? Podaj przykłady, do czego się tego używa i dlaczego to jest przydatne, a nie tylko dziwne.

#### Zadanie

    free -h
    ZMIENNA=alfa
    echo $ZMIENNA
    exit                      # wyloguj się i zaloguj ponownie
    echo $ZMIENNA

Dopisz do notatek, co się stało ze zmienną. (Tak, to jest to samo, co dzieje się z `$NOTATKI`.) Potem trzy zapisy:

    echo "jestem w pamieci" > /dev/shm/ulotne.txt
    echo "jestem na dysku"  > ~/praca/f1/trwale.txt
    ZMIENNA2=beta

Sprawdź, że wszystkie trzy istnieją. Uruchom `df -h` i znajdź wiersz z `/dev/shm` — jakiego jest typu?

**Zanim zrestartujesz maszynę, zapisz przewidywanie dla każdego z trzech zapisów: przeżyje czy nie i dlaczego tak sądzisz.** Potem `sudo reboot` i sprawdź wszystkie trzy.

**Do notatek:** trzy przewidywania, trzy wyniki oraz **trzy poziomy trwałości** — od najkrócej żyjącego do najdłużej, z przykładem każdego.

#### Sprawdź się

    lab grade ulotnosc

### Z15. Metoda, nie lista — 10 min

#### O co tu chodzi

Poprzednie zadanie pokazało ci trzy konkretne miejsca. Problem w tym, że katalogów na serwerze są tysiące i nikt nie pamięta listy tych ulotnych — a pomyłka kosztuje utratę danych, które ktoś uznał za zapisane.

Dlatego zamiast listy do wykucia potrzebujesz **jednego pytania, które możesz zadać systemowi o dowolny katalog** i dostać odpowiedź w dziesięć sekund. Tytuł zadania mówi dokładnie to: metoda, nie lista.

#### Czego potrzebujesz

Zrozumienia, że katalogi, które widzisz jako jedno drzewo, w rzeczywistości należą do różnych systemów plików — i że system potrafi ci powiedzieć, do którego należy dany katalog.

> Jestem początkujący w Linuksie. Wytłumacz mi, co to znaczy, że system plików jest „zamontowany" w jakimś punkcie drzewa katalogów. Dlaczego `/` i `/dev/shm` mogą być zupełnie różnymi systemami plików, choć wyglądają jak jedno drzewo? Wyjaśnij, jak w ogóle sprawdza się, do którego systemu plików należy konkretny katalog, i co oznaczają typy w rodzaju `ext4` czy `tmpfs`. Nie podawaj mi gotowego polecenia — chcę je znaleźć sam.

#### Zadanie

Podaj **jedno polecenie**, którym w dziesięć sekund rozstrzygniesz, czy dowolny katalog leży w pamięci, czy na dysku.

Zastosuj je do: `/dev/shm`, `/run`, `/tmp`, `~`, `/var/log`. Dla każdego dopisz jedno słowo: RAM albo dysk.

**Jeden z wyników prawdopodobnie cię zaskoczy.** Napisz który i sprawdź, dlaczego akurat tak jest na tej maszynie.

#### Sprawdź się

    lab grade ulotnosc
    lab koniec ulotnosc

---

## Moduł: sciezki — 20 min

    lab start sciezki

### Z16. Labirynt ścieżek — 20 min

#### O co tu chodzi

To jest egzamin z tego, co ćwiczyłeś w Z10, tylko bez podpowiedzi: siedem plików o identycznej nazwie, rozrzuconych po drzewie katalogów, i jeden punkt, z którego nie wolno się ruszyć.

W quizie na pytanie o ścieżki odpowiedziałeś „nie pamiętam", a ścieżkę zdefiniowałeś jako „zbiór danych" — czyli opisałeś plik. Po tym zadaniu ścieżka przestanie być abstrakcją, bo przez dwadzieścia minut będzie jedynym narzędziem, jakie masz.

#### Czego potrzebujesz

Sprawności w składaniu ścieżek względnych — w górę przez `..`, w dół przez nazwy — oraz umiejętności rozpoznania wpisu w katalogu, który tylko udaje katalog.

> Jestem początkujący w Linuksie. Wytłumacz mi, jak czytać wynik polecenia `ls -l`: co oznacza każda kolumna i — przede wszystkim — co oznacza pierwszy znak w linii. Jakie rodzaje wpisów mogą wystąpić w katalogu poza zwykłym plikiem i katalogiem? Pokaż, po czym poznać każdy z nich w wyniku `ls -l`.

> Wytłumacz mi, czym jest dowiązanie symboliczne w Linuksie: co fizycznie zawiera, czym różni się od kopii pliku i co się stanie, jeśli cel zniknie. Wyjaśnij też, dlaczego ten sam plik może być dostępny pod dwiema różnymi ścieżkami. Użyj przykładu z drzewem katalogów, bez gotowych poleceń dla mnie.

#### Zadanie

W `~/labirynt/` jest siedem plików o nazwie `dane.txt`, każdy z innym słowem w środku. Stoisz w `~/labirynt/start` i **nie wolno ci stamtąd wyjść**. Zakazane: `cd`, `~`, `$HOME`, ścieżki od `/` oraz `find`.

1. Wypisz zawartość **wszystkich siedmiu** plików. Podaj siedem słów i siedem ścieżek, których użyłeś.
2. Podaj **dwie różne ścieżki wskazujące ten sam plik** i wyjaśnij jednym zdaniem, dlaczego to ten sam plik.
3. W `start/` jest coś, co nie jest zwykłym katalogiem. Znajdź to, sprawdź `ls -l` i napisz, dokąd prowadzi.

#### Sprawdź się

    lab grade sciezki
    lab koniec sciezki

---

## Moduł: dysk — 30 min

    lab start dysk

### Z17. 🔮 Dysk się zapełnił — 30 min

#### O co tu chodzi

„Brak miejsca na dysku" to jedna z tych awarii, które wyglądają jak dziesięć innych awarii naraz: aplikacja przestaje zapisywać, baza się nie uruchamia, logi się urywają, a komunikaty nie mówią wprost, co jest przyczyną. Zdarza się to regularnie i zwykle nie ma nikogo, kto by ci powiedział, gdzie szukać.

To zadanie nie jest o znalezieniu pliku. **Jest o tym, jak się szuka**, gdy nie wiadomo, gdzie szukać — i to jedyne takie zadanie w całym dniu.

W quizie, zapytany o ostatnią sytuację, w której coś nie działało, odpowiedziałeś jednym słowem: „CORS". Dziś chodzi o dokładne przeciwieństwo: interesuje mnie każdy krok, także ten, który okazał się ślepy.

#### Czego potrzebujesz

Dwóch narzędzi, które brzmią podobnie, a odpowiadają na zupełnie inne pytania — i jednej metody przeszukiwania, która działa niezależnie od tego, czego szukasz.

> Jestem początkujący w Linuksie. Wytłumacz mi różnicę między `df` a `du`: na jakie pytanie odpowiada każde z nich i dlaczego potrafią pokazać różne liczby dla tego samego miejsca. Wyjaśnij, jak czytać ich wynik kolumna po kolumnie. Nie rozwiązuj mojego zadania — chcę zrozumieć narzędzia.

> Wytłumacz mi metodę szukania, gdy wiem tylko, że „coś zajmuje dużo miejsca", ale nie wiem gdzie. Jak zawężać obszar poszukiwań krok po kroku, zamiast przeglądać wszystko po kolei? Opisz to jako sposób myślenia (od korzenia w dół, sprawdzam największą gałąź), a nie jako gotowy zestaw poleceń. Powiedz też, jak nie zgubić się po drodze i jak zapisywać, co już sprawdziłem.

#### Zadanie

`df -h` pokazuje, że `/` jest zajęte niemal w całości. Znajdź przyczynę i zwolnij miejsce.

**Zasady:**

- Nie usuwasz niczego, czego nie umiesz nazwać.
- Zanim cokolwiek usuniesz, mówisz mentorowi, co to jest i dlaczego uważasz, że można.
- Przed usunięciem zapisz przewidywanie: ile miejsca się zwolni i jaki procent pokaże `df -h` potem.
- **Zapisujesz ścieżkę drążenia:** każdy katalog, do którego wszedłeś, i jedno zdanie, dlaczego akurat tam.

Ten ostatni punkt jest właściwym wynikiem zadania — ważniejszym niż samo znalezienie pliku. Sam plik znajdzie ci AI w trzy sekundy; twojej ścieżki myślenia nie napisze nikt.

#### Sprawdź się

    lab grade dysk
    lab koniec dysk

---

## Moduł: zamkniecie — 15 min

    lab start zamkniecie

### Z18. Zamknięcie dnia — 15 min

#### O co tu chodzi

Notatki są jedyną rzeczą, która z dzisiejszego dnia zostanie na dłużej — i jedyną, którą zobaczy mentor. Chronologiczna lista `== Z9 ==`, `== Z10 ==` była dobra w trakcie pracy; teraz zamieniasz ją w coś, co da się przeczytać po tygodniu i zrozumieć, czego się nauczyłeś.

Porządkowanie notatek na koniec to nie biurokracja. To moment, w którym z dziesięciu osobnych zadań robi się jeden spójny obraz — i przy okazji ostatnia szansa, żeby zauważyć, w którym miejscu twoje przewidywanie rozminęło się z rzeczywistością.

#### Czego potrzebujesz

Pewności co do jednej rzeczy w gicie, którą łatwo pomylić — i którą mentor i tak cię zapyta na obronie.

> Wytłumacz mi, czym różni się `git commit` od `git push`. Gdzie fizycznie są moje zmiany po commicie, a gdzie po pushu? Co zobaczy współpracownik, jeśli zrobię commit i wyłączę komputer bez pusha? Jak sprawdzić, czy mam lokalnie coś, czego nie ma jeszcze na serwerze? Wytłumacz mechanizm, nie dawaj mi listy poleceń do przepisania.

#### Zadanie

1. Uporządkuj `notatki/f1.md`. Ma zawierać **trzy sekcje i nic poza nimi** (stare nagłówki `== Zxx ==` mają zniknąć — scal je w sekcje):
   - **Eksperymenty** — Z13, Z14, Z17: co przewidziałeś, co wyszło, gdzie się pomyliłeś.
   - **Diagnozy** — Z16 i Z17: co było nie tak i **jak** to znalazłeś. Ścieżka drążenia, nie rozwiązanie.
   - **Trzy pytania na jutro.**

   Nie opisuj, co robi każde polecenie — od tego jest `man` i AI, a ty i tak będziesz to tłumaczył ustnie.

2. Oddaj pracę:

       cd ~/staz
       git add notatki/
       git commit -m "docs: notatki F1"
       git push

3. Sprawdź na GitHubie, że commit tam jest. Jeśli go nie widać — mentor go nie zobaczy i dzień formalnie nie został oddany.

#### Sprawdź się

    lab grade zamkniecie
    lab koniec zamkniecie
    lab koniec F1             # raport całego dnia — pokaż go mentorowi

4. Na sam koniec, już po raporcie dnia: wyłącz maszynę i zrób snapshot **`po-F1`**.
