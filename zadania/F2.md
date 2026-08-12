# F2 — procesy, pakiety, sieć: dlaczego coś nie działa

**To jedyny dokument, który dziś czytasz.** Zadania są w kolejności wykonania, pogrupowane w moduły.

## Cel dnia

Nauczyć się uruchamiać, znajdować i zatrzymywać to, co działa na maszynie, oraz zrozumieć, dlaczego aplikacja, która „u mnie działa", bywa niewidoczna z zewnątrz. Na końcu dnia dostajesz zepsutą usługę i masz ją doprowadzić do działania — jutro będziesz robił dokładnie to samo, tylko z prawdziwą aplikacją.

## Zasady

Te same co wczoraj:

- **Korzystaj z AI**; warunek jeden — `sudo` czegoś, czego nie umiesz opisać, nie uruchamiasz nigdy.
- **Dowodem jest wynik, nie opis** — wyniki dopisujesz przez `>>` z nagłówkiem zadania.
- **⏱** oznacza zadanie na czas, **🔮** zadanie, w którym najpierw zapisujesz przewidywanie, a dopiero potem sprawdzasz.
- **Zablokowany dłużej niż 20 minut?** Zapisz, na czym, przejdź dalej, wróć później.

Dodatkowo dziś:

- **Notatki idą do `notatki/f2.md`.** Na starcie: `export NOTATKI=~/staz/notatki/f2.md`.
- **Pracujesz na dwóch sesjach SSH naraz** — w jednej uruchamiasz, w drugiej obserwujesz. Dwie zakładki Windows Terminala.

## Jak wygląda dzień

Ten sam schemat co wczoraj, moduł po module:

    lab start <moduł>     # przygotowuje środowisko wszystkich zadań modułu
    lab grade <moduł>     # sprawdza, czy zrobiłeś dobrze — możesz powtarzać do skutku
    lab koniec <moduł>    # zamyka moduł i przechodzi do następnego

Gdyby `lab` zgubił kontekst dnia: `lab dzien F2`. Lista modułów w kolejności: `lab moduly`.

`lab grade` ocenia **cały moduł naraz**. Jeśli uruchomisz je w połowie modułu, zadania jeszcze nierobione wypadną na czerwono — to normalne, nie znaczy, że coś zepsułeś.

**Każde zadanie ma dziś cztery części:**

- **O co tu chodzi** — po co ci to i gdzie się z tym spotkasz naprawdę.
- **Czego potrzebujesz** — czego musisz się dowiedzieć, żeby w ogóle zacząć. Są tu gotowe prompty do AI. Są napisane tak, żeby AI **wytłumaczyło ci mechanizm, a nie rozwiązało zadanie za ciebie**. Jeśli przerobisz je na „napisz mi polecenie, które…", dostaniesz gotowca i stracisz dokładnie to, po co tu jesteś. Nikt tego nie sprawdzi poza tobą.
- **Zadanie** — co masz zrobić.
- **Sprawdź się** — polecenie, które to sprawdza.

---

## Moduł: ssh — 13 min

    lab start ssh

### Z1. Odbierz zadania dnia — 3 min

#### O co tu chodzi

Treść zadań przychodzi do ciebie tak samo jak w pracy przychodzi kod — przez Gita, a nie mailem: `git pull` zaciąga to, co mentor dopisał od wczoraj.

#### Zadanie

    cd ~/staz
    git pull
    cat zadania/F2.md

#### Sprawdź się

    lab grade ssh

Nie zdziw się, że wyjdzie na czerwono — `lab grade ssh` ocenia oba zadania modułu naraz, a Z2 masz jeszcze przed sobą.

### Z2. Połącz się po SSH — 10 min

#### O co tu chodzi

Wczoraj wszystko przepisywałeś ręcznie w oknie VirtualBoksa — bez schowka, bez wklejania, litera po literze. Dziś odzyskujesz normalny terminal, ale musisz się najpierw dostać na maszynę z Windowsa.

W quizie napisałeś o SSH, że „chyba szyfrowało połączenia" — i to prawda, tylko to nie jest powód, dla którego go używasz. Powód jest taki, że ta maszyna nie ma monitora ani klawiatury, a ty i tak będziesz nią sterował. Dokładnie tak wygląda praca z każdym serwerem, którego w życiu nie zobaczysz.

#### Czego potrzebujesz

Dwóch rzeczy: umieć odczytać, jakie adresy ma twoja maszyna, i umieć się na nią połączyć z Windowsa.

> Jestem początkujący w Linuksie. Wytłumacz mi, jak czytać wynik polecenia `ip a`: co to jest interfejs sieciowy, dlaczego maszyna wirtualna ma zwykle więcej niż jeden adres IP i czym różni się w VirtualBoksie karta typu NAT od karty host-only. Pokaż przykładowy wynik i opisz go linijka po linijce.

> Wytłumacz mi jak początkującemu, czym jest SSH i co się dzieje, gdy wpisuję `ssh uzytkownik@adres`. Kto się z kim łączy, co to znaczy, że dostaję „zdalną powłokę", i dlaczego to jest coś innego niż pulpit zdalny. Nie podawaj mi gotowej komendy pod moją maszynę.

**Jednego dziś nie pytaj:** co oznacza `localhost`. Punkt 4 tego zadania to eksperyment, a odpowiedź poznana teraz go zepsuje. Wrócimy do niego na końcu dnia.

#### Zadanie

1. W konsoli VM uruchom `ip a`. Znajdź **dwa** adresy IP poza `127.0.0.1` i zapisz oba w notatkach.
2. W Windows Terminal połącz się: `ssh twoj_uzytkownik@192.168.56.X` (adres z karty host-only).
3. Otwórz **drugą** zakładkę i połącz się ponownie. Od tej chwili pracujesz na dwóch sesjach.
4. Spróbuj jeszcze z Windowsa: `ssh twoj_uzytkownik@localhost`. **Zapisz w notatkach, czym skończyła się próba z `localhost` — i nie tłumacz tego jeszcze.** Wrócimy do tego na końcu dnia.

> Ta maszyna nie ma monitora ani klawiatury i właśnie nią sterujesz. To jest odpowiedź na pytanie, po co komu terminal.

#### Sprawdź się

    lab grade ssh

<!-- -->

    lab grade ssh
    lab koniec ssh

---

## Moduł: dysk — 10 min

    lab start dysk

### Z3. ⏱ Znowu — 10 min

#### O co tu chodzi

Dysk zapchał się drugi raz, w innym miejscu niż wczoraj. To nie jest złośliwość — tak to wygląda naprawdę: ta sama awaria wraca w innym katalogu, u innego klienta, w innym miesiącu. Dlatego wczorajsze polecenia mają się zamienić w **rutynę**, którą wykonujesz bez zastanawiania.

Zadanie jest na czas nie po to, żeby cię stresować, tylko żeby sprawdzić, czy to już rutyna, czy wciąż szukanie po omacku.

#### Czego potrzebujesz

Tego samego, co wczoraj. Jeśli metoda ci wyleciała z głowy — odśwież ją, ale nie proś o gotowe polecenie pod ten konkretny przypadek:

> Wytłumacz mi metodę szukania, co zajmuje miejsce na dysku w Linuksie: od czego zacząć, jak schodzić coraz głębiej w katalogi zamiast zgadywać, i czym różni się `df` od `du`. Interesuje mnie kolejność kroków, nie gotowa sekwencja poleceń — mam to znaleźć sam.

#### Zadanie

Dysk na twojej maszynie zapchał się drugi raz, w innym miejscu niż wczoraj. **Masz 10 minut** na znalezienie i usunięcie przyczyny.

Do notatek (pod nagłówkiem `Z3`): ile ci to zajęło i które polecenie z wczoraj okazało się najbardziej przydatne.

#### Sprawdź się

    lab grade dysk

<!-- -->

    lab grade dysk
    lab koniec dysk

---

## Moduł: procesy — 30 min

    lab start procesy

**Uwaga o sprawdzaniu tego modułu:** zadania Z5–Z7 nie zostawiają po sobie żadnego śladu w systemie — po zabiciu procesu nie ma czego oglądać. Dlatego `lab grade procesy` odnotuje, że przez moduł przeszedłeś, ale **nie potwierdzi treści twoich odpowiedzi**. Jeśli wynik będzie wyglądał pusto — tak ma być, nic nie jest zepsute. Te zadania sprawdzamy **na obronie**, ustnie, z twoich notatek. Pisz je więc tak, żebyś umiał je za dwa dni obronić.

### Z5. Uruchom, znajdź, zabij — 10 min

#### O co tu chodzi

W quizie na pytanie o podgląd procesów napisałeś „nie wiem", a zatrzymanie programu opisałeś jako „coś ze zniszczeniem". Dziś to domykamy — i to jest jedna z tych umiejętności, których będziesz używał codziennie.

Sytuacja z życia: aplikacja na serwerze się zawiesiła i zjada procesor. Nie ma Menedżera zadań, nie ma czego kliknąć. Musisz ją **znaleźć po nazwie, rozpoznać po numerze i zatrzymać** — i to wszystko przez terminal.

#### Czego potrzebujesz

Zrozumienia, że każdy uruchomiony program dostaje od systemu numer (PID) — i że to właśnie po tym numerze, a nie po nazwie, mówi się systemowi, co ma zatrzymać.

> Jestem początkujący w Linuksie. Wytłumacz mi, czym jest proces i czym jest PID. Skąd system bierze te numery, czy się powtarzają, i co właściwie oznaczają kolumny w wyniku `ps aux`. Wytłumacz też, czym różni się `ps` od `top`. Pokaż przykładowy wynik i opisz go — nie podawaj gotowej komendy pod moje zadanie.

> Wytłumacz mi, co robi znak `&` na końcu polecenia w Bashu, czym różni się program uruchomiony „w tle" od tego uruchomionego normalnie, i co właściwie robi Ctrl+C. Wspomnij o sygnałach — co to jest sygnał i dlaczego proces można poprosić o zakończenie na kilka sposobów. Chcę zrozumieć mechanizm, nie dostać gotowca.

#### Zadanie

1. Uruchom w tle proces `sleep 600`.
2. Znajdź jego PID — **nie przepisując go z ekranu** przy uruchomieniu.
3. Zatrzymaj go po PID. Potwierdź, że zniknął.
4. Uruchom `sleep 900` **bez** tła i zatrzymaj innym sposobem. Zapisz jedno zdanie: czym te dwa sposoby się różnią.

Przy okazji zapisz do notatek trzy liczby: ile procesów działa w systemie, jaki PID ma twoja powłoka, ile pamięci zajmuje `sshd`.

#### Sprawdź się

    lab grade procesy

To zadanie nie ma automatycznego sprawdzenia — obronisz je ustnie, z notatek.

### Z6. 🔮 Co przeżywa rozłączenie sesji — 12 min

#### O co tu chodzi

Jutro uruchomisz aplikację na tym serwerze i zamkniesz terminal. Pytanie, czy ona to przeżyje, nie jest ciekawostką — to jest **cała różnica między „uruchomiłem" a „wdrożyłem"**. W quizie napisałeś o usłudze w tle, że „działa, jest niewidoczna, ale coś robi" — dobra intuicja, dziś dokładasz do niej narzędzia.

To zadanie jest oznaczone 🔮, bo tu chodzi o twoją intuicję, nie o wynik. Zapisz najpierw, czego się spodziewasz — nawet jeśli nie masz pojęcia. Zwłaszcza wtedy.

#### Czego potrzebujesz

Zrozumienia, że proces jest do czegoś **przywiązany** — i że rozłączenie tego czegoś ma konsekwencje.

> Wytłumacz mi jak początkującemu, co dzieje się z uruchomionymi programami, gdy rozłączam sesję SSH. Co to znaczy, że proces jest „podpięty do terminala"? Czym jest sygnał SIGHUP i kto go wysyła? Użyj analogii i nie podawaj mi gotowego rozwiązania — mam to sprawdzić eksperymentem.

> Wytłumacz mi, czym jest sesja i terminal w Linuksie: co konkretnie ginie, gdy zamykam okno, a co zostaje w systemie. Pokaż to na przykładzie, nie na definicji.

#### Zadanie

**Zapisz przewidywanie dla obu przypadków, zanim sprawdzisz.**

1. `sleep 600 &` → rozłącz sesję SSH → połącz się ponownie → czy proces żyje?
2. `nohup sleep 600 &` → to samo → czy proces żyje?

**Do notatek, dwa zdania:**

- czym różni się program *zainstalowany* od *uruchomionego* (pomoc: `which sleep` pokazuje plik, `ps aux` pokazuje procesy),
- twoja jutrzejsza aplikacja ma działać po zamknięciu terminala **i** wstawać sama po restarcie serwera. `nohup` załatwia połowę tego. Czego brakuje?

#### Sprawdź się

    lab grade procesy

To zadanie nie ma automatycznego sprawdzenia — obronisz je ustnie, z notatek.

### Z7. Zadanie odwrotne: czytanie `ps` — 8 min

#### O co tu chodzi

Do tej pory uruchamiałeś polecenie i patrzyłeś na wynik. Teraz odwrotnie: dostajesz **cudzy wynik** i masz powiedzieć, co z niego wynika. Tak wygląda 90% prawdziwej diagnostyki — ktoś wkleja ci fragment logu albo zrzut z monitoringu i pyta „co tu się dzieje".

#### Czego potrzebujesz

Umiejętności czytania tabeli, którą wypisuje `ps`.

> Wytłumacz mi kolumna po kolumnie, co oznacza wynik polecenia `ps aux` w Linuksie: USER, PID, %CPU, %MEM, VSZ, RSS, TTY, STAT, START, TIME, COMMAND. Wytłumacz szczególnie, co oznacza znak `?` w kolumnie TTY i co oznaczają litery w kolumnie STAT. Użyj **własnego** przykładowego wiersza — nie odpowiadaj na moje pytania, tylko naucz mnie czytać tę tabelę.

#### Zadanie

    bartek    1487  0.0  0.4  17064  8192 ?  Ss  09:14  0:00 /usr/bin/python3 -m http.server 8080

1. Który element jest PID-em, a który zużyciem pamięci?
2. Podaj polecenie, które zatrzyma dokładnie ten proces.
3. Podaj polecenie, które wypisze **tylko** wiersze zawierające `http.server`.
4. Skąd wiadomo, że ten proces nie jest podpięty do żadnego terminala?

#### Sprawdź się

    lab grade procesy

To zadanie nie ma automatycznego sprawdzenia — obronisz je ustnie, z notatek.

<!-- -->

    lab grade procesy
    lab koniec procesy

---

## Moduł: pakiety — 12 min

    lab start pakiety

### Z8. Pakiety — 12 min

#### O co tu chodzi

W quizie przy menedżerze pakietów napisałeś „komendy nie pamiętam". To jest różnica, która zaskakuje wszystkich przychodzących z Windowsa: w Linuksie **nie szukasz instalatora na stronie producenta**. Jest lista zaufanych serwerów wpisana w system i jedno polecenie, które stamtąd bierze pakiet razem ze wszystkim, czego on potrzebuje.

Od jutra każda instalacja czegokolwiek na serwerze idzie tą drogą. Warto wiedzieć, skąd te pliki naprawdę przychodzą — bo pytanie „skąd wziąłeś ten pakiet" pada na każdym audycie bezpieczeństwa.

#### Czego potrzebujesz

Zrozumienia, czym jest repozytorium i co robi menedżer pakietów.

> Jestem początkujący w Linuksie, przychodzę z Windowsa. Wytłumacz mi, czym jest repozytorium pakietów i czym jest menedżer pakietów w Ubuntu. Skąd fizycznie biorą się pliki, które instaluję, i gdzie w systemie zapisana jest lista serwerów, z których się je pobiera? Wytłumacz też, czym różnią się od siebie `apt update`, `apt upgrade` i `apt install`. Porównaj to z pobieraniem pliku `.exe` ze strony w Windowsie — chcę zrozumieć różnicę, nie dostać listy komend.

> Wytłumacz mi, dlaczego zwykły użytkownik w Linuksie nie może zapisywać w katalogach systemowych i jak czytać komunikat, który wtedy dostaje. Co dokładnie próbuje zrobić instalator, że potrzebuje uprawnień administratora?

#### Zadanie

1. Zainstaluj `htop` **bez** `sudo`. Zapisz komunikat i jedno zdanie: dlaczego.
2. Zainstaluj `htop`, `curl`, `jq` i `tree` prawidłowo.
3. Ustal, **skąd fizycznie przyszedł** `htop` — nazwij źródło, nie „z internetu".
4. Odinstaluj `tree` i potwierdź, że polecenie przestało istnieć.

**Do notatek:** dwie różnice między `apt install` a pobraniem instalatora ze strony w Windowsie. Oraz: co robi `sudo apt update`, a czego **nie** robi.

#### Sprawdź się

    lab grade pakiety

<!-- -->

    lab grade pakiety
    lab koniec pakiety

---

## Moduł: sciezka-path — 38 min

    lab start sciezka-path

**Po przygotowaniu tego modułu przeloguj sesję SSH** (wyjdź i połącz się ponownie) — inaczej część stanu się nie uaktywni.

### Z9. `PATH` — 8 min

#### O co tu chodzi

W quizie przy zmiennych środowiskowych i `PATH` napisałeś „nie wiem". To jeden z tematów, które mentor zaznaczył do nadrobienia od razu — i najmniej oczywisty z nich, bo `PATH` działa przez cały czas, tylko go nie widać.

Sytuacja z życia: napiszesz własny skrypt, uruchomisz go po nazwie i dostaniesz `command not found`, mimo że plik leży dwa katalogi dalej i na pewno istnieje. Albo odwrotnie — uruchomisz polecenie i wykona się **coś innego**, niż myślałeś. Za oba przypadki odpowiada ta jedna zmienna.

#### Czego potrzebujesz

Zrozumienia, że powłoka nie „zna" poleceń — ona ich **szuka**, w konkretnych katalogach i w konkretnej kolejności.

> Jestem początkujący w Linuksie. Wytłumacz mi, czym jest zmienna `PATH`: co dokładnie zawiera, jak system jej używa w momencie, gdy wpisuję nazwę polecenia, i w jakiej kolejności przegląda katalogi. Wytłumacz też, co się stanie, jeśli dwa katalogi z `PATH` zawierają program o tej samej nazwie. Na koniec: czym różni się `which` od `type`. Nie podawaj gotowych poleceń pod moje zadanie — chcę zrozumieć mechanizm.

#### Zadanie

Odpowiedzi zapisz w notatkach:

1. Ile katalogów jest w twoim `PATH`?
2. Gdzie fizycznie leży `ls`? A `curl`? (Gdyby `curl` nie było na maszynie — zainstaluj go tak, jak w poprzednim module.)
3. Dlaczego wpisujesz `ls`, a nie `/usr/bin/ls`?

#### Sprawdź się

    lab grade sciezka-path

### Z10. Coś tu kłamie — 30 min

#### O co tu chodzi

Dwa narzędzia patrzą na ten sam dysk i mówią co innego. Jedno z nich kłamie, a ty musisz ustalić które — bo dopóki wierzysz niewłaściwemu, będziesz „naprawiał" coś, co wcale nie jest zepsute.

W quizie, na pytanie o ostatnią sytuację, w której coś nie działało, odpowiedziałeś jednym słowem: „CORS". Tu chcę zobaczyć **drogę, nie wynik**. Zapis ścieżki drążenia jest częścią zadania, nie dodatkiem do niego — i to jest dokładnie ta umiejętność, na której stoją dni 8 i 10 twojego planu.

Zaplanuj to jako 30 minut. Jeśli po dwudziestu stoisz w miejscu — zapisz, na czym, i wróć później.

#### Czego potrzebujesz

Dwóch rzeczy: metody drążenia i wiedzy o tym, skąd naprawdę bierze się program, który uruchamiasz.

> Wytłumacz mi, jak wygląda uporządkowane szukanie przyczyny awarii: hipoteza → czym ją sprawdzam → wynik → następna hipoteza. Pokaż to na krótkim przykładzie z zupełnie innej dziedziny niż informatyka, żebym zrozumiał samą metodę. Wytłumacz też, dlaczego zapisywanie odrzuconych hipotez ma sens.

> Wytłumacz mi, skąd powłoka bierze program, który uruchamiam po nazwie, i jak sprawdzić, **który konkretnie plik** zostanie uruchomiony. Wytłumacz też, gdzie w Ubuntu zapisuje się rzeczy, które mają się wykonać przy każdym zalogowaniu — czym są pliki startowe powłoki i który z nich czyta zwykła sesja SSH. Bez gotowych rozwiązań, chcę zrozumieć mechanizm.

#### Zadanie

`df -h` pokazuje, że `/` jest zajęte w 98%. Ale to, co widać przez `du`, sumuje się do kilku gigabajtów przy dysku 30 GB. Wczoraj zapchany dysk wyglądał zupełnie inaczej.

**Ustal, które z tych dwóch narzędzi kłamie i dlaczego. Napraw.**

Zasady:

- Zapisujesz ścieżkę drążenia: każdą hipotezę i to, czym ją sprawdziłeś.
- Nie usuwasz plików systemowych — rozwiązanie **nie** polega na zwalnianiu miejsca.
- Gdy znajdziesz przyczynę, dopisz jedno zdanie: jak to samo mogłoby wyglądać złośliwie. Co jeszcze dałoby się w ten sposób podmienić?

#### Sprawdź się

    lab grade sciezka-path

<!-- -->

    lab grade sciezka-path
    lab koniec sciezka-path

---

## Moduł: zmienne — 10 min

    lab start zmienne

**Uwaga o sprawdzaniu tego modułu:** tak samo jak przy procesach — `export TRYB=test` nie zostawia po sobie nic, co da się sprawdzić po fakcie. `lab grade zmienne` odnotuje, że przez moduł przeszedłeś, ale **nie potwierdzi treści twoich odpowiedzi**; pusto wyglądający wynik nie znaczy, że coś jest zepsute. Ten moduł sprawdzamy **na obronie**, z twoich notatek.

### Z11. Zmienne środowiskowe — 10 min

#### O co tu chodzi

To druga połowa luki z quizu — przy zmiennych środowiskowych napisałeś „nie wiem". A jutro twoja aplikacja będzie brała hasło do bazy właśnie stamtąd, bo nie ma innego sensownego miejsca, gdzie mogłaby je wziąć.

Punkt 4 tego zadania jest z twojego podwórka i celowo: klucz do API wpisany w plik `.js` na froncie to najczęstszy wyciek w projektach frontendowych. Po tym zadaniu będziesz umiał powiedzieć, dlaczego — i czym to się różni od hasła trzymanego po stronie serwera.

#### Czego potrzebujesz

> Jestem początkujący w Linuksie. Wytłumacz mi, czym jest zmienna środowiskowa, czym różni się od zwykłej zmiennej w powłoce i co dokładnie robi `export`. Dlaczego wartość ustawiona w jednej sesji znika po rozłączeniu, a w drugiej sesji jej nie widać? Pokaż przykłady, nie podawaj gotowca pod moje zadanie.

> Jestem frontendowcem. Wytłumacz mi, dlaczego wszystko, co trafia do kodu JavaScript wykonywanego w przeglądarce, jest publiczne — nawet jeśli siedzi w pliku `.js` o dziwnej nazwie albo jest zminifikowane. Kto i jak może to odczytać? Czym różni się to od sekretu trzymanego po stronie serwera, do którego przeglądarka nigdy nie zagląda?

#### Zadanie

1. `export TRYB=test`, sprawdź. Rozłącz SSH, połącz ponownie, sprawdź jeszcze raz.
2. Jedno zdanie: dlaczego to jest **to samo zjawisko**, które widziałeś wczoraj przy ulotności danych.
3. Aplikacja potrzebuje hasła do bazy danych. Gdzie je wpisujesz i dlaczego nie w kodzie?
4. Pytanie z twojego podwórka: wpisujesz klucz do API prosto w plik `.js` na froncie. Kto go zobaczy i jak? Czym to się różni od hasła trzymanego na serwerze?

#### Sprawdź się

    lab grade zmienne

Ten moduł nie ma automatycznego sprawdzenia — obronisz go ustnie, z notatek.

<!-- -->

    lab grade zmienne
    lab koniec zmienne

---

## Moduł: uprawnienia — 47 min

    lab start uprawnienia

### Z12. Własny skrypt i uprawnienia — 22 min

#### O co tu chodzi

W quizie rozpoznałeś, że chodzi o uprawnienia „do odczytu, zapisu i coś jeszcze". To „coś jeszcze" to prawo do **uruchomienia** i dziś je poznasz od strony praktycznej: napiszesz plik, uruchomisz go i dostaniesz odmowę.

To nie jest ciekawostka — każdy skrypt, który w życiu napiszesz, przechodzi przez ten moment. A punkt 6 zadania jest zapowiedzią jutra: usługa uruchamiana automatycznie startuje z **innego katalogu** niż ten, w którym ty ją testowałeś, i przez to widzi co innego.

#### Czego potrzebujesz

Umiejętności czytania uprawnień z `ls -l` i zapisywania ich z powrotem przez `chmod`.

> Jestem początkujący w Linuksie. Wytłumacz mi wynik polecenia `ls -l` znak po znaku: co oznacza pierwszy znak, a potem trzy grupy po trzy litery. Kto to jest „właściciel", kto „grupa", a kto „pozostali" i skąd system wie, kim ja jestem. Wytłumacz też zapis liczbowy w `chmod`: skąd biorą się te cyfry i jak przeliczyć w obie strony. Pokaż przykłady, ale nie rozwiązuj mojego zadania.

> Wytłumacz mi, jak długo żyje zmienna środowiskowa i kto ją dziedziczy: co widzi program uruchomiony z mojej powłoki, a czego nie widzi. Wytłumacz też, czym różni się „katalog, w którym leży skrypt" od „katalogu, w którym skrypt został uruchomiony" i co w związku z tym pokazuje `pwd` wywołane w środku skryptu.

#### Zadanie

W `nano` utwórz `~/praca/f2/start.sh`:

```bash
#!/bin/bash
echo "Uruchamiam w trybie: $TRYB"
echo "Katalog roboczy: $(pwd)"
```

1. Uruchom `./start.sh`. Zapisz **dosłownie**, co odpowiedział system.
2. Spróbuj obejść problem przez `sudo ./start.sh`. Zapisz wynik i jedno zdanie: dlaczego `sudo` tu nie pomogło.
3. `ls -l start.sh` — przepisz uprawnienia i **rozbij je na trzy grupy**, opisując każdą literę.
4. Napraw i uruchom.
5. Uruchom tak, żeby wypisał tryb `produkcja` — **nie zmieniając pliku i nie robiąc `export`**.
6. Uruchom z innego katalogu: `cd ~ && ~/praca/f2/start.sh`. Co zmieniło się w drugiej linii wyniku i dlaczego to będzie ważne przy usłudze uruchamianej automatycznie?
7. **Zadanie odwrotne:** chcę uprawnienia `-rwxr-x---`. Podaj `chmod` w zapisie liczbowym i powiedz, kto po tej zmianie może plik uruchomić, a kto nawet go nie przeczyta.

#### Sprawdź się

    lab grade uprawnienia

### Z13. Dwa problemy naraz — 25 min

#### O co tu chodzi

Zgłoszenie brzmi „nic nie działa" i wygląda na jedną awarię. Są dwie, z dwóch różnych powodów, i naprawienie jednej nie ruszy drugiej. Umiejętność, o którą tu chodzi, to **rozdzielenie objawów**: nazwać każdy problem osobno, zanim zaczniesz cokolwiek zmieniać.

Zakaz `chmod 777` nie jest kaprysem. To najczęstszy „szybki fix" w internecie — działa zawsze i zawsze zostawia po sobie dziurę, bo daje pełne prawa wszystkim użytkownikom maszyny. Jutro będziesz to widział w cudzych instrukcjach; dziś masz się nauczyć robić **najmniejszą wystarczającą zmianę**.

#### Czego potrzebujesz

Kluczowa jest tu rzecz, która myli praktycznie wszystkich: uprawnienia na **katalogu** znaczą co innego niż te same litery na **pliku**.

> Jestem początkujący w Linuksie. Wytłumacz mi różnicę między uprawnieniami do pliku a uprawnieniami do katalogu: co dokładnie oznaczają `r`, `w` i `x` postawione na katalogu — bo to nie to samo, co na pliku. Pokaż konkretne sytuacje: mogę wejść do katalogu, ale nie widzę listy plików; widzę listę, ale nie mogę nic utworzyć; widzę plik, ale nie mogę go otworzyć. Wytłumacz też, jak sprawdzić, kto jest właścicielem pliku i do jakich grup należę.

> Wytłumacz mi, dlaczego `chmod 777` jest uznawane za zły nawyk. Co konkretnie się psuje pod względem bezpieczeństwa i kto po takiej zmianie może zrobić co. Podaj przykład realnej konsekwencji, nie samą definicję.

#### Zadanie

W `~/praca/f2/` przestało działać wszystko:

1. Utwórz w tym katalogu nowy plik. Nie da się.
2. Przeczytaj leżący tam `konfiguracja.txt`. Też nie da się.

**To są dwa różne problemy z dwóch różnych powodów.** Nazwij oba osobno i napraw oba.

**Zabronione:** `chmod 777`, `chown -R` na całym katalogu, kasowanie i tworzenie katalogu od nowa. Ma być najmniejsza zmiana, która wystarczy.

**Dowód:** `ls -ld` katalogu i `ls -l` pliku przed i po, plus jedno zdanie na każdy problem: co dokładnie było nie tak.

Na koniec, dla kontrastu: spróbuj `cat /etc/shadow`, potem `sudo cat /etc/shadow`. Dwa zdania: dlaczego ten plik jest zamknięty i dlaczego aplikacja webowa nie powinna działać jako root.

#### Sprawdź się

    lab grade uprawnienia

<!-- -->

    lab grade uprawnienia
    lab koniec uprawnienia

---

## Moduł: logi — 26 min

    lab start logi

### Z14. Pipe i logi na żywo — 14 min

#### O co tu chodzi

W quizie przy pytaniach o `grep`, `tail -f` i o potok (`|`) padło „nie wiem" — za każdym razem. To są trzy rzeczy, których na serwerze używa się **codziennie** — bo pierwszą reakcją na „nie działa" nie jest zgadywanie, tylko otwarcie logu i patrzenie, co się w nim pojawia w momencie awarii.

Podgląd na żywo to jest ten moment, w którym przestajesz zgadywać: robisz coś w jednym oknie i **widzisz** w drugim, co system o tym sądzi.

#### Czego potrzebujesz

Dwóch rzeczy: łączenia poleceń w łańcuch i oglądania pliku, który wciąż rośnie.

> Jestem początkujący w Linuksie. Wytłumacz mi, co robi znak `|` między dwoma poleceniami: w którą stronę płyną dane, co to jest standardowe wejście i standardowe wyjście, i dlaczego to się nazywa „potok". Pokaż trzy przykłady od najprostszego i opisz każdy. Nie podawaj polecenia pod moje zadanie.

> Wytłumacz mi różnicę między wypisaniem końcówki pliku a śledzeniem go na żywo. Czym jest dziennik systemowy w Ubuntu, czym różni się `journalctl` od zwykłych plików w `/var/log` i jak się z takiego podglądu wychodzi. Chcę zrozumieć mechanizm, nie dostać gotowej komendy.

#### Zadanie

1. Wypisz wyłącznie te procesy, które mają w nazwie `ssh`. Jedno zdanie: w którą stronę płyną dane przez `|`.
2. W **pierwszej** sesji uruchom podgląd logu systemowego na żywo. W **drugiej** rozłącz się i zaloguj ponownie. Opisz, co zobaczyłeś w pierwszym oknie — i czym ten podgląd różni się od zwykłego wypisania końcówki pliku.
3. To samo, ale przefiltrowane tak, żeby widać było tylko linie dotyczące SSH.

#### Sprawdź się

    lab grade logi

### Z15. ⏱ Ile było nieudanych logowań — 12 min

#### O co tu chodzi

Każda maszyna wystawiona do sieci jest skanowana — automaty próbują logować się na typowe konta, non stop. Pytanie „ile razy ktoś próbował" nie jest pytaniem o wrażenie, tylko o **liczbę, którą wyciąga się z logu**. Tak wygląda pierwszy krok każdego zgłoszenia bezpieczeństwa.

To zadanie ma jeszcze jedno dno: **AI nie zna tej liczby**, bo nie ma dostępu do twojej maszyny. Może ci podać narzędzie i metodę, ale jeśli poda konkretną liczbę — właśnie ją zmyśliło. Sam opisałeś w quizie, że błędy AI wyłapujesz tam, gdzie masz wiedzę. Tu ją będziesz miał.

#### Czego potrzebujesz

Umiejętności filtrowania logu i liczenia trafień zamiast oglądania ich na oko.

> Jestem początkujący w Linuksie. Wytłumacz mi, gdzie Ubuntu zapisuje informacje o próbach logowania po SSH i jakie są dwa różne sposoby dostania się do tych zapisów. Wytłumacz, jak zawęzić dziennik do jednej usługi i do dzisiejszej daty oraz jak **policzyć** pasujące linie zamiast je wypisywać. Nie licz niczego za mnie — nie masz dostępu do mojej maszyny i konkretna liczba może wyjść tylko z niej.

**Uwaga na pułapkę obserwatora.** Jeśli będziesz przeszukiwał plik dziennika przez `sudo`, twoje własne polecenie może trafić do tego samego dziennika — razem ze wzorcem, którego szukasz — i zawyżyć wynik. Objaw: przy drugim uruchomieniu tego samego polecenia liczba rośnie o jeden. Uruchom je dwa razy i sprawdź, czy wynik jest stabilny; jeśli nie jest, zmień sposób liczenia.

#### Zadanie

**Masz 5 minut.** Dziś ktoś kilkanaście razy próbował zalogować się na tę maszynę po SSH na nieistniejące konta. **Podaj dokładną liczbę prób.**

AI nie zna tej liczby — poda ci narzędzie, resztę musisz zrobić sam. Dopisz też polecenie, którym ją policzyłeś.

#### Sprawdź się

    lab grade logi

<!-- -->

    lab grade logi
    lab koniec logi

---

## Moduł: siec — 55 min

    lab start siec

### Z16. Co nasłuchuje na tej maszynie — 10 min

#### O co tu chodzi

W quizie IP opisałeś poprawnie, ale porty „mgliście". Ten moduł domyka lukę, którą mentor zaznaczył jako **priorytetową na cały tydzień** — bez niej stanie ci dzień z Dockerem i dzień z proxy.

Zaczynasz od tabeli, do której będziesz wracał do końca stażu. Odpowiada na dwa najczęstsze pytania świata: „dlaczego port jest zajęty" i „dlaczego nie mogę się połączyć". Za chwilę dopiszesz do niej własny wpis, a jutro Docker dopisze kilka.

#### Czego potrzebujesz

Zrozumienia, co właściwie znaczy, że program „nasłuchuje na porcie".

> Jestem początkujący. Wytłumacz mi jak człowiekowi, co to znaczy, że program „nasłuchuje na porcie". Czym jest port, dlaczego jeden port w danej chwili może zająć tylko jeden program i skąd przeglądarka wie, na który port ma się połączyć, skoro ja go nie wpisuję. Użyj analogii i nie podawaj mi gotowej komendy.

> Wytłumacz mi, jak w Linuksie sprawdzić, które programy nasłuchują i pod jakim adresem. Co oznaczają poszczególne opcje w `ss -tlnp` (`-t`, `-l`, `-n`, `-p`) i dlaczego bez uprawnień administratora kolumna z nazwą procesu bywa pusta? Wytłumacz opcje, nie układaj polecenia pod moje zadanie.

#### Zadanie

1. Wypisz porty, które nasłuchują, razem z nazwami procesów, które je zajmują. **Uruchom to przez `sudo`** — bez uprawnień administratora kolumna z nazwami procesów będzie pusta, a to właśnie ona jest tu potrzebna.
2. Znajdź wśród nich SSH. Zgadza się z tym, co zapisałeś w Z2?
3. Zapisz całą listę — za chwilę dojdzie do niej twój własny wpis.

#### Sprawdź się

    lab grade siec

### Z17. Twoja strona na twoim serwerze — 20 min

#### O co tu chodzi

Pierwszy raz **twój** kod — HTML i `fetch()`, czyli twoje podwórko — pojedzie na Linuksie, którym sam zarządzasz. Do tej pory pisałeś stronę, którą ktoś inny gdzieś podawał; dziś jesteś po obu stronach naraz.

To jest też domknięcie tego, czego uczyłeś się sam: podłączania projektu do API. Znasz to od strony klienta. Za chwilę zobaczysz to samo od strony serwera — i to ten sam mechanizm, który jutro postawisz w Dockerze.

#### Czego potrzebujesz

Wiedzy, czym właściwie jest ten „serwer", który uruchamiasz jednym poleceniem.

> Wytłumacz mi, co się dzieje, gdy uruchamiam `python3 -m http.server` w jakimś katalogu. Co to znaczy, że coś „jest serwerem HTTP", co on robi z plikami z tego katalogu i jak wygląda pojedyncze zapytanie i odpowiedź. Wytłumacz też, dlaczego strona otwarta z pliku (`file://`) zachowuje się inaczej niż ta sama strona podana przez serwer — szczególnie przy `fetch()`. Jestem frontendowcem, więc możesz odwołać się do przeglądarki.

Serwer zajmie ci całe okno terminala i nie odda go, dopóki działa — to normalne i dlatego pracujesz dziś na dwóch sesjach. Uruchamiasz w jednej, patrzysz i sprawdzasz w drugiej.

#### Zadanie

W `~/praca/f2/www/` utwórz dwa pliki. `dane.json`:

```json
{"komunikat": "dziala"}
```

oraz `index.html` — zwykła strona, która przez `fetch()` pobiera `dane.json` i wypisuje wynik na ekranie. To twoje podwórko, napisz ją po swojemu.

Uruchom serwer:

    cd ~/praca/f2/www && python3 -m http.server 8080 --bind 127.0.0.1

**Zostaw go uruchomiony** — musi działać w chwili sprawdzania i będzie ci potrzebny w kolejnym zadaniu.

#### Sprawdź się

    lab grade siec

### Z18. 🔮 Jedno słowo, które zmienia wszystko — 25 min

#### O co tu chodzi

Przed chwilą uruchomiłeś serwer i sprawdziłeś go **na tej samej maszynie**. Teraz spróbujesz wejść na niego **z innego komputera** — ze swojego Windowsa. I okaże się, że nie działa, mimo że serwer chodzi, proces żyje, a port jest zajęty.

To jest jedna z najczęstszych rzeczy, na których ludzie tracą godziny — łącznie z takimi, którzy pracują w tym zawodzie od lat. W quizie napisałeś, że `localhost` to „sieć lokalna". Po tym zadaniu będziesz wiedział, dlaczego to nie to samo, i **dlaczego ta różnica zablokuje ci dzień z Dockerem**, jeśli jej nie zrozumiesz.

#### Czego potrzebujesz

Zrozumienia, że aplikacja nie „nasłuchuje na porcie" — ona nasłuchuje **na konkretnym adresie i porcie**. Adres decyduje, kto może się połączyć.

> Wytłumacz mi jak początkującemu różnicę między nasłuchiwaniem serwera na `127.0.0.1` a na `0.0.0.0`. Co oznacza każdy z tych adresów? Dlaczego serwer na `127.0.0.1` jest niewidoczny z innego komputera, mimo że proces działa i port jest otwarty? Użyj analogii i nie podawaj mi gotowej komendy — chcę zrozumieć mechanizm, bo mam to sam rozwiązać.

Przyda ci się też umiejętność odczytania, co i **pod jakim adresem** nasłuchuje na twojej maszynie:

> Wytłumacz mi, jak odczytać wynik polecenia `ss -tlnp` w Linuksie. Co oznacza każda kolumna? Jak rozpoznać, czy dana usługa przyjmie połączenie z innego komputera, czy tylko z tej samej maszyny?

#### Zadanie

Serwer z Z17 działa. **Zanim cokolwiek sprawdzisz, zapisz trzy przewidywania** — i przy każdym jedno zdanie, dlaczego tak sądzisz:

1. `curl -i http://localhost:8080/` z drugiej sesji SSH na VM-ce — zadziała?
2. Przeglądarka na Windowsie pod `http://192.168.56.X:8080` — zadziała?
3. Przeglądarka na Windowsie pod `http://localhost:8080` — zadziała?

Sprawdź wszystkie trzy. W drugiej sesji wypisz nasłuchujące porty i **przepisz kolumnę z adresem nasłuchu**.

Teraz zatrzymaj serwer i uruchom go **bez** `--bind`. Powtórz te same trzy sprawdzenia i ponownie przepisz kolumnę z adresem nasłuchu.

**Do notatek:** zmieniło się jedno słowo i zmieniło wszystko. Napisz dokładnie, co ono robi — bez używania sformułowania „sieć lokalna".

#### Sprawdź się

    lab grade siec

<!-- -->

    lab grade siec
    lab koniec siec

---

## Moduł: cors — 30 min

    lab start cors

### Z19. CORS od drugiej strony + kody odpowiedzi — 30 min

#### O co tu chodzi

To jest **twoje** zadanie dnia. W quizie, zapytany o ostatnią awarię, jaką pamiętasz, odpowiedziałeś jednym słowem: „CORS" — i wtedy nie umiałeś go rozwiązać. Dziś jesteś po drugiej stronie: to ty stawiasz oba serwery, więc pierwszy raz możesz zobaczyć **jednocześnie** to, co widzi przeglądarka, i to, co widzi `curl`.

Najważniejsze, co masz z tego wynieść: CORS **nie jest błędem w twoim kodzie**. Dlatego szukanie przyczyny w kodzie potrafi zająć całe popołudnie — wtedy właśnie nie wiedziałeś, gdzie patrzeć. Dziś ustalisz, kto konkretnie podejmuje tę decyzję i na jakiej podstawie.

Druga część to kody odpowiedzi HTTP — w quizie GET i POST opisałeś dobrze, kodów nie znałeś wcale. Bez nich każda diagnoza aplikacji webowej kończy się na „nie działa".

#### Czego potrzebujesz

> Jestem początkujący. Wytłumacz mi, czym jest kod odpowiedzi HTTP i co znaczą grupy 2xx, 3xx, 4xx i 5xx. Omów szczególnie 200, 301 i 404 — kiedy serwer zwraca każdy z nich i co powinien z tym zrobić klient. Wytłumacz też, co dokładnie pokazuje `curl` z opcją `-i` w porównaniu do zwykłego wywołania. Nie układaj poleceń pod moje zadanie.

> Jestem frontendowcem i widziałem kiedyś błąd CORS, ale go nie rozumiem. Wytłumacz mi mechanizm od strony przeglądarki: co to jest *origin* i z jakich trzech części się składa, dlaczego przeglądarka blokuje odpowiedź, mimo że serwer ją wysłał, i dlaczego `curl` nie ma z tym żadnego problemu. Wytłumacz też, **po której stronie** — przeglądarki czy serwera — leży decyzja o przepuszczeniu odpowiedzi. Chcę zrozumieć mechanizm, nie dostać gotowej konfiguracji.

#### Zadanie

**a) Kody.** Przy działającym serwerze wywołaj `curl -i` tak, żeby dostać **200**, **404** i **301**. Trzeci wymaga pomysłu — podpowiedź: katalog. Zapisz trzy kody i po jednym zdaniu, co znaczą. Do notatek wklej **całą linię statusu** z każdej odpowiedzi (tę zaczynającą się od `HTTP/`), nie sam numer.

**b) CORS.** W drugiej sesji, w **innym katalogu**, uruchom drugi serwer na porcie 8081 z własnym `dane.json`. Zmień `index.html` tak, żeby `fetch()` szedł na `http://192.168.56.X:8081/dane.json`. Otwórz stronę z portu 8080 w przeglądarce na Windowsie, F12 → konsola. Zapisz komunikat.

**c) Próba kontrolna.** Na VM-ce: `curl http://192.168.56.X:8081/dane.json`. Zadziałało?

**Trzy pytania do notatek:**

- dlaczego `curl` pobiera ten plik bez problemu, a przeglądarka odmawia,
- co to jest *origin* i z czego się składa,
- `http://IP:8080` i `http://IP:8081` — ta sama maszyna? ten sam origin?

**d) Powrót do Z2.** Odpowiedz teraz na pytanie z rana: dlaczego `ssh uzytkownik@192.168.56.X` z Windowsa zadziałało, a `ssh uzytkownik@localhost` nie. Jedno zdanie, bez sformułowania „sieć lokalna".

#### Sprawdź się

    lab grade cors

<!-- -->

    lab grade cors
    lab koniec cors

---

## Moduł: sklep — 35 min

    lab start sklep

### Z20. 🔮 Uruchom sklep — 35 min

#### O co tu chodzi

To jest końcówka dnia i jego sens naraz. Dostajesz **cudzą** usługę, która nie startuje, i nikt ci nie mówi, co jest w niej nie tak. Nie ma tu nowego materiału — wszystko, czego potrzebujesz, robiłeś dziś już co najmniej raz. Pytanie brzmi, czy potrafisz **wybrać właściwe narzędzie, gdy nikt nie mówi którego użyć**. Dokładnie tak wygląda pierwszy dzień na prawdziwym projekcie.

Poprzeczka jest ustawiona wyżej niż „u mnie działa": usługa ma się otworzyć **w przeglądarce mentora, na jego komputerze**. To znaczy, że sprawdzenie „mnie się otwiera" niczego nie dowodzi.

Jutro zrobisz to samo z prawdziwą aplikacją, tylko wtedy nikt już nie napisze ci, że coś jest zepsute.

#### Czego potrzebujesz

Dwóch rzeczy, i obie są umiejętnościami, nie poleceniami: umieć przeczytać cudzy skrypt i mieć metodę na „uruchamiam i nie działa".

> Jestem początkujący. Wytłumacz mi, jak czytać cudzy skrypt w Bashu, żeby zrozumieć, co robi, **zanim** go uruchomię: co oznacza pierwsza linia pliku, jak rozpoznać zmienne i skąd biorą się ich wartości, w jakiej kolejności wykonują się polecenia i na co zwrócić uwagę przy ścieżkach. Nie pisz mi żadnego skryptu — chcę umieć przeczytać istniejący.

> Wytłumacz mi metodę pracy z sytuacją „uruchamiam i nie działa": jak czytać komunikat błędu, dlaczego czytam go w całości, a nie tylko pierwszą linię, co sprawdzić najpierw, jak po każdej poprawce sprawdzić, czy coś się zmieniło, i po czym poznać, że problem był więcej niż jeden. Odpowiadaj ogólnie — nie znasz mojego przypadku i nie chcę, żebyś go zgadywał.

**Czego nie rób:** nie wklejaj AI całej zawartości skryptu z prośbą „napraw to". Dostaniesz gotowca i stracisz jedyne zadanie w tym dniu, które sprawdza, czy potrafisz sam.

#### Zadanie

W `/opt/sklep/` leży usługa, która ma się otworzyć **w przeglądarce mentora, na jego Windowsie, pod portem 9000**. Nie działa.

**Zanim cokolwiek uruchomisz:** obejrzyj pliki i zapisz, co według ciebie zawiedzie. Dopiero potem sprawdzaj.

**Zasady:**

- Nie kopiujesz plików poza `/opt/sklep`.
- Nie przepisujesz skryptu od zera — naprawiasz to, co jest.
- Dla **każdej** napotkanej przeszkody zapisujesz osobno: komunikat, przyczynę, poprawkę.
- Na koniec pokazujesz, że port 9000 nasłuchuje pod właściwym adresem.

Wszystko, czego tu potrzebujesz, robiłeś dziś już co najmniej raz.

#### Sprawdź się

    lab grade sklep

<!-- -->

    lab grade sklep
    lab koniec sklep

---

## Moduł: zamkniecie — 15 min

    lab start zamkniecie

### Z21. Zamknięcie dnia — 15 min

#### O co tu chodzi

Notatki są produktem tego dnia — nie zadania, nie polecenia, tylko one. Za dwa dni na obronie będziesz odpowiadał z nich, a za miesiąc, gdy ta sama awaria wróci, będą jedyną rzeczą, która ci zostanie. W pracy nazywa się to post-mortem i pisze się je dokładnie z tego samego powodu.

Snapshot na końcu to twój punkt powrotu — od jutra będziesz psuł tę maszynę na poważnie.

#### Czego potrzebujesz

> Wytłumacz mi, jak zapisywać notatki z rozwiązanej awarii, żeby były przydatne za miesiąc, kiedy nie będę pamiętał kontekstu. Co powinno się w nich znaleźć poza samą komendą — objaw, hipotezy, sposób sprawdzenia, wynik? Pokaż krótki przykład na dowolnej wymyślonej awarii, nie na mojej.

#### Zadanie

1. Uporządkuj `notatki/f2.md` — trzy sekcje:
   - **Eksperymenty** — Z6, Z18, Z20: przewidywania kontra wyniki.
   - **Diagnozy** — Z3, Z10, Z13, Z20: co było zepsute i **jak** to znalazłeś.
   - **Trzy pytania na jutro.**

2. Oddaj pracę:

       cd ~/staz
       git add notatki/
       git commit -m "docs: notatki F2"
       git push

#### Sprawdź się

    lab grade zamkniecie

<!-- -->

    lab grade zamkniecie
    lab koniec zamkniecie
    lab koniec F2             # raport całego dnia — pokaż go mentorowi

3. Wyłącz maszynę i zrób snapshot **`po-fundamencie`**. To będzie punkt powrotu na najbliższe dni.
