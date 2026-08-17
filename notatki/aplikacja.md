### Z1

1. Mamy 2 katalogi najwyższego poziomu:
	- api/ -backend/API baza, endpointy, migracje, logi, metryki
	- web/ frontend w HTML/CSS/JS, który komunikuje sie z API
2. Adres API jest w (web/config.js)
3. Aplikacja API bierze konfiguracje ze zmiennych środowiskowych


### Z2

1. which python3 - /usr/bin/python3
which pip - nie dało nic (nie ma zainstalowanego) 


bartek@ubuntu:~/staz$ cd ~/staz/aplikacja/api
bartek@ubuntu:~/staz/aplikacja/api$ which python3
/usr/bin/python3
bartek@ubuntu:~/staz/aplikacja/api$ which pip
bartek@ubuntu:~/staz/aplikacja/api$ type pip
-bash: type: pip: not found

2. Uwtorzyłem środowisko ze zmianą ip na 0.0.0.0

3. which python3 - /home/bartek/staz/aplikacja/api/.venv/bin/python3
which pip - /home/bartek/staz/aplikacja/api/.venv/bin/pip
echo $PATH - /home/bartek/staz/aplikacja/api/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

4. pip list | wc -l - 35
python -c "import fastapi; print(fastapi.__version__)" - 0.141.1

## Dodatkowe info
Zainstalowanie biblioteki oznacza dodanie jej plików do środowiska, a aktywowanie środowiska powoduje, że powłoka zaczyna używać Pythona i pip właśnie z tego środowiska.


### Z3

## Przewidywania
1. Aplikacja uruchomiona bez utworzenia struktury bazy — w ogóle wstanie?
Odp.: Zależy jaka to jest aplikacja. Jesli aplikacja jest stworzona na podstawie bazy czyli wszystkie zmienne/dane są pobierana z bazy zamiast dynamicznie to aplikacja nie wstanie. 
2. curl http://127.0.0.1:8000/health — co odpowie?
Odp.: Prawdopodobnie pokaże, że aplikacja działa i baza jest osiągalna bo połącznie może działac bez utworzenia tabeli.
3. curl http://127.0.0.1:8000/api/links — co odpowie?
Odp.: Powinien wystąpić jakiś błąd braku tabeli bo będzie próba odczytu danych z tabeli, której jeszcze migracja nie była stworzona. 

## Wyniki
1. /health był mylący, bo sprawdzi, czy aplikacja może połączyć sie z bazą ale nie sprawdził czy istnieją wszystkie wymagane tabele i czy da sie wykonać zapytanie aplikacji
2. Szczegóły błędów nie są wyświetlane w aplikacji z powodu bezpeczeństwa (brak pokazywania inforamacji o kodzie, bazie, ścieżkach plików czy konfiguracji) które mogły by pomóc w atatach.

### Z4

1. Po migracji nic sie nie zmiło z powodu że już chyba była migracja zrobiona rozmiar bazy sie nie zminił. 
2. Logi są takie same bo nie było przedtem błędu.
3. curl pokazuje to samo
4. {"code":"VzFuhAx","url":"https://example.com","clicks":0,"created_at":"2026-08-17T08:02:30.478645Z"}
5. (.venv) bartek@ubuntu:~/staz/aplikacja/api$ curl -i http://127.0.0.1:8000/r/VzFuhAx
HTTP/1.1 307 Temporary Redirect
date: Mon, 17 Aug 2026 08:03:59 GMT
server: uvicorn
content-length: 0
location: https://example.com
6. (.venv) bartek@ubuntu:~/staz/aplikacja/api$ curl -i http://127.0.0.1:8000/api/links/VzFuhAx
HTTP/1.1 200 OK
date: Mon, 17 Aug 2026 08:05:38 GMT
server: uvicorn
content-length: 100
content-type: application/json
{"code":"VzFuhAx","url":"https://example.com","clicks":4,"created_at":"2026-08-17T08:02:30.478645Z"}
Odp.: Co się zmieniło w odpowiedzi po wywołaniu przekierowania? Odpowiedź dostałem wraz z częścia body z api czyli "{"code":"VzFuhAx","url":"https://example.com","clicks":4,"created_at":"2026-08-17T08:02:30.478645Z"}"
7. curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/docs
Odpowiedz: 200

## Notatka
Kod 307 jest używany zamiast kodu 301 ponieważ przeglądarka pyta za każdym razem o przekierowanie i zliczać kliknięcia. 

### Z5 

1. Zmieniłem port w zmiennej środowiskowej na 9000 (APP_PORT=9000 python -m app) 
Potwierdziłem curl-em że że odpowiada ({"status":"ok","database":"ok","version":"1.0.0"})

2. Po ustawieu poziomu DEBUG pojawiły się dodatkowe techniczne logi o utworzeniu silnika bazy danych oraz używanym asynico. 

3. APP_PORT=9000 APP_NAME=linkbox-b python -m app, APP_PORT=8000 APP_NAME=linkbox-a python -m app

4. ValueError: LOG_LEVEL musi być jedną z wartości CRITICAL, ERROR, WARNING, INFO, DEBUG, otrzymano: 'GADATLIWY'
Dobrze że aplikacja nie wstaje bo od razu wykrywa błędną konfiguracje zamist uruchamiać się z nieprawidłowym poziomem logowania. 

5. sudo ss -tlnp | grep -E ':8000|:9000' 

## Notatka

Gorsze byłoby, gdyby aplikacja wystartowała z błędną konfiguracją i przez godzinę pozornie działała, ale np. zapisywała dane do złej bazy albo logowała za mało informacji. Problem wyszedłby dopiero później, gdy użytkownik zgłosi błąd albo okaże się, że dane trafiły w niewłaściwe miejsce

### Z6 

## Notatka wstępna 
.env to plik z wartościami, source wczytuje je do Basha, a set -a sprawia, że stają się zmiennymi środowiskowymi widocznymi dla uruchamianych programów.

Sekret, który raz trafił do historii repozytorium, należy traktować jak ujawniony; najpierw go zmieniasz, a dopiero potem usuwasz jego ślady z historii.

1. env opisuje:
- Adres na którym nasłuchuje: 127.0.0.1
- Port TCP: APP_PORT=8000
- Adres bazy danych: DATABASE_URL=sqlite:///./links.db
- Lista dozwolonych originów: CORS_ORIGINS=
- Poziom logowania: LOG_LEVEL=INFO
- Nazwa instancji aplikacji: APP_NAME=linkbox

2. Zrobiłem z niego kopie roboczą (cp .env.example .env). Przez nano .env zmieniłem APP_PORT=8000 oraz LOG_LEVEL=DEBUG.

3. (.venv) bartek@ubuntu:~/staz/aplikacja/api$ set -a
(.venv) bartek@ubuntu:~/staz/aplikacja/api$ source .env
(.venv) bartek@ubuntu:~/staz/aplikacja/api$ set +a

4. (.venv) bartek@ubuntu:~/staz/aplikacja/api$ cd ~/staz
(.venv) bartek@ubuntu:~/staz$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   aplikacja/api/app/config.py
        modified:   notatki/aplikacja.md

no changes added to commit (use "git add" and/or "git commit -a")

## Wyjasnienie
Plik .env nie pojawia się w git status ponieważ w aplikacja/api/.gitignore znajduje sie wpis .env. 

5. APP_PORT jest pusty w drugiej sesji, ponieważ zmienne środowiskowe ustawione w jednej sesji Bash nie są automatycznie przekazywane do innej, osobnej sesji SSH.


## Dodatkowa notatka
Trzy miejsca z których ta aplikacja może dostać wartość APP_PORT:
1. APP_PORT=9000 python -m app — tylko dla jednego uruchomienia procesu.
2. export APP_PORT=9000 albo wczytanie z .env — działa w tej sesji powłoki i dla procesów potomnych; po zamknięciu sesji znika.
3. ...

### Z7

## Notatka wstępna 

127.0.0.1 oznacza: nasłuchuj tylko na połączenia przychodzące z tej samej maszyny.
0.0.0.0 oznacza: nasłuchuj na wszystkich interfejsach sieciowych tej maszyny.

Log startowy pokazuje, z jaką konfiguracją aplikacja naprawdę działa, ale powinien pokazywać tylko bezpieczne ustawienia, nigdy sekrety.

## Przewidywania

1. curl http://127.0.0.1:8000/health z drugiej sesji SSH na VM-ce — zadziała?
Odp.: Tak druga sesja SSH powinna działac na tej samej VM.
2. Przeglądarka na Windowsie pod http://192.168.56.X:8000/docs — zadziała?
Odp.: Nie jeśli aplikacja nasłuchuje tylko na 127.0.0.1
3. Przeglądarka na Windowsie pod http://localhost:8000/docs — zadziała?
Odp.: Tak bo mam ustawione przekierowania portu

## Zadania

1. Tak zadziałał (curl http://127.0.0.1:8000/health), (http://localhost:8000/docs) zadzaiałał bo mamy przekierowania
2. LISTEN 0      2048         0.0.0.0:8000      0.0.0.0:*    users:(("python",pid=4626,fd=7))
3. Nasłuchuję na 0.0.0.0:8000
4. APP_HOST=0.0.0.0 python -m app
5. ss -tlnp | grep 8000
6. POST /api/links zwrócił kod 201, czyli nowy link został poprawnie utworzony.

## Notatka końcowa
http://localhost:8000/docs na Windowsie zadziałało, ponieważ VirtualBox miał ustawione przekierowanie portu 8000 z hosta do maszyny wirtualnej, więc żądanie wysłane na localhost:8000 zostało przekazane do aplikacji na VM.

### Z8
