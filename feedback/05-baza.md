# Feedback po dniu baza

## Wynik

8 z 8 modułów, wszystkie zadania zaliczone, **ani jeden warunek nie padł dwa razy w tym samym module**. To pierwszy taki dzień w całym stażu — i był to dzień najtrudniejszy z dotychczasowych.

W poniedziałek uruchamiałeś cudzą aplikację według instrukcji. Wczoraj zamknąłeś ją w obrazie. Dziś przeniosłeś jej dane do prawdziwego serwera bazy, zrobiłeś kopię i **odtworzyłeś z niej po skasowaniu tabeli**. To ostatnie jest tym, czego większość ludzi nigdy nie ćwiczy — do momentu, w którym musi.

## Co zrobiłeś dobrze

**Awaria (Z11) — zobaczyłeś to, o co w tym zadaniu chodziło.** W jednej wartości siedziały dwie wady, a pierwsza zasłaniała drugą. Twoja notatka:

> Błąd `Connection refused` wynikał z użycia `localhost` zamiast `db`. Po zmianie hosta błąd **zmienił się** na `password authentication failed`, więc API zaczęło docierać do PostgreSQL.

To jest sedno: komunikat, który się zmienia, jest informacją. Dopóki nie dochodzisz do serwera, o haśle nie dowiesz się nic — bo nikt go jeszcze nie sprawdzał. Twoja notatka startowa pokazuje, że rozumiesz tę różnicę nie z definicji, tylko z tego, co zobaczyłeś.

Zweryfikowałeś naprawę **trzema niezależnymi sposobami**: `/health`, liczba rekordów w tabeli i front. O to prosiłem i nie każdy to robi — zielony `/health` nie mówi nic o danych.

**Sekwencja `id` — najtrudniejsza pułapka tego dnia i wpadłeś w nią świadomie.** Przeniosłeś dane z jawnym `id`, czyli drogą, która zostawia licznik Postgresa w tyle. Zauważyłeś to i naprawiłeś, a w notatkach zapisałeś dlaczego:

> Ręczne ID i sekwencja to dwie osobne rzeczy, więc po imporcie danych warto je zsynchronizować.

Gdybyś wstawiał bez `id`, wszystko zadziałałoby od razu — i nie dowiedziałbyś się, że sekwencja w ogóle istnieje. Twoja droga była trudniejsza i więcej cię nauczyła. Do tego sam odpowiedziałeś na pytanie, które miałem ci zadać: co się stanie przy powtórnym uruchomieniu migracji.

**Skrypt `migracja_sqlite_postgres.py` jest napisany dobrze.** Hasło bierzesz z `os.environ["POSTGRES_PASSWORD"]`, a nie z kodu. Zamykasz kursory i połączenia. Na końcu wypisujesz liczbę przeniesionych rekordów — czyli skrypt mówi, co zrobił, zamiast kończyć w ciszy. To trzy rzeczy, których brakuje w większości skryptów „na raz".

Jedno użyłeś w wersji ostrzejszej, niż musiałeś: `os.environ["KLUCZ"]` wywala się od razu, gdy zmiennej nie ma, zamiast po cichu podstawić `None` i wywrócić się trzy kroki dalej z niezrozumiałym błędem. Tak właśnie należy czytać konfigurację, bez której program i tak nie zadziała.

**`compose.yaml`:** healthcheck z `pg_isready`, `depends_on` z warunkiem `service_healthy`, nazwany wolumen na dane bazy, konkretny tag `postgres:16`, brak `ports:` na bazie i hasło wyłącznie przez `${POSTGRES_PASSWORD}`. Sprawdziłem historię repozytorium — hasło nie pojawiło się w niej ani razu.

**Twoje trzy pytania są lepsze niż połowa moich.** Zwłaszcza pierwsze:

> Dlaczego zmiana `POSTGRES_PASSWORD` w `.env` nie zmienia automatycznie hasła w już istniejącej bazie?

To jest dokładnie to pytanie, które miałem ci zadać na obronie. Odpowiedź: obraz Postgresa używa tych zmiennych **tylko przy inicjalizacji pustego wolumenu**. Wolumen już istnieje, więc hasło w bazie zostaje stare, a zmienia się tylko to, którym puka aplikacja — i przestaje pasować. Ludzie tracą na tym całe popołudnia, bo „przecież zmieniłem hasło w konfiguracji".

**Komunikaty commitów się poprawiły.** Masz dziś dwa zaczynające się od „Zadanie 9 zrobione", ale **z różnymi opisami** — jeden o kopii zapasowej, drugi o poprawionej notatce. Wcześniej były identyczne. Widać, że wziąłeś to pod uwagę.

## Co poprawić

**Z12 miało cztery sekcje. Zrobiłeś jedną.**

Są „Trzy pytania" — i są dobre. Nie ma **Eksperymentów**, nie ma **Diagnoz** (dwa raporty z Z10 i Z11 zebrane w jednym miejscu) i nie ma **Hierarchii trwałości**.

Ta ostatnia boli najbardziej, bo to jedyna rzecz w całym stażu, która spina wszystkie dni w jedno. Zacząłeś ją w F1 przy `tmpfs`. We wtorek dopisałeś dysk. W środę rozszerzyłeś o warstwę zapisywalną kontenera i wolumen — i zrobiłeś to dobrze, mam to w twoich notatkach:

> Trwałość: zmienna powłoki → tmpfs → warstwa kontenera → wolumen → dysk hosta.

Dziś doszły dwa ostatnie piętra: **wolumen bazy danych** i **kopia zapasowa poza maszyną**. Prosiłem o jedno zdanie przy każdym piętrze — przed czym chroni, a przed czym nie — bo dopiero to zamienia listę w narzędzie do myślenia. Wolumen chroni przed `docker rm`, ale nie przed skasowaniem tabeli. Kopia chroni przed skasowaniem tabeli, ale nie przed utratą maszyny, jeśli leży na tej samej maszynie.

Domknij to jutro, przy retro. To dziesięć minut, a zostanie ci na dłużej niż ten staż.

**Nie zamykałeś modułów na bieżąco.** Twój commit mówi wprost: *„Poprawiłem błędy z modułami bo chyba zapomniałem ich zakończyc"*. Efekt widać w raporcie — moduł `kopia` ma wpisane 3 godziny 6 minut „czasu realizacji", choć tyle nad nim nie siedziałeś. Ta liczba to odstęp od `lab start` do momentu, w którym pierwszy raz uruchomiłeś `lab grade`, a zrobiłeś to dopiero przy porządkach na koniec dnia.

Nic ci to nie odbiera — wszystko jest zaliczone. Ale raport jest dokumentem, który zostaje, a `lab grade` po każdym module kosztuje pięć sekund i daje ci informację wtedy, kiedy jeszcze możesz z niej skorzystać.

## Jutro — ostatni dzień

**CI: automat, który sprawdza twój kod przy każdym pushu.**

Zaczniesz od tego, co już umiesz — uruchomienia testów, lintera i formatera na własnej maszynie. Potem zamkniesz te trzy komendy w jednym skrypcie, a skrypt oddasz GitHubowi, żeby uruchamiał go za ciebie. Na koniec pipeline zbuduje twój obraz i sprawdzi, czy aplikacja z niego wstaje.

Będzie też awaria — ostatnia w tym stażu i inna niż dotychczasowe: nie w konfiguracji, tylko **w kodzie**, i trzy wady naraz, każdą wykrywa inne narzędzie.

Trzy rzeczy z tego tygodnia wracają jutro:

- **Log czyta się od góry.** W środę straciłeś godzinę, bo `pip` napisał na końcu „nie znajduję wersji fastapi", a prawdziwa przyczyna stała pięć linii wyżej. Jutro to samo zjawisko wróci w logu przebiegu CI, tylko log będzie dłuższy.
- **„U mnie działa" przestaje być argumentem.** Twój skrypt uruchomi się na cudzej maszynie, na której nie ma nic z twojego środowiska. To jest moment, w którym okazuje się, co tak naprawdę jest w repozytorium, a co tylko u ciebie.
- **Zielony status nie znaczy „działa".** Twoje własne zdanie ze środy: *„docker compose ps mówi tylko, że kontenery działają, ale nie że aplikacja w środku działa poprawnie i używa właściwych danych"*. Jutro dopiszesz do tego wersję o zielonym pipelinie.

Ostatni moduł to retro — pół godziny na sześć pytań o cały staż. Potraktuj je serio, bo to jedyna część, której nie sprawdza żaden automat, a która zostaje z tobą najdłużej.

Instalacja jak zawsze:

    cd ~/staz
    git pull
    ./zainstaluj.sh
