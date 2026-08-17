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

## Notatka wstępna

Serwer statyczny podaje gotowe pliki HTML/CSS/JS, a serwer API przetwarza żądania, wykonuje logikę i zwraca dane, np. z bazy.

## Zadania 

Strona się otworzy, ale API będzie dla niej niedostępne. Zapisz do notatek:
- dokładną treść komunikatu na pasku stanu u góry strony,
Odp.: Odpowiedź API zablokowana przez przeglądarkę (CORS)
- dokładną treść komunikatu z listy linków,
Odp.: Nie udało się pobrać listy
- adres API, który strona wypisuje w nagłówku i w stopce.
Odp.: http://localhost:8000


Wciśnij F12, przejdź na zakładkę konsoli, odśwież stronę i przepisz oryginalny komunikat przeglądarki — cały, razem z nazwą nagłówka, który się w nim pojawia:
Odp.: Zablokowano żądanie do zasobu innego pochodzenia: zasady „Same Origin Policy” nie pozwalają wczytywać zdalnych zasobów z „http://localhost:8000/health” (brakujący nagłówek CORS „Access-Control-Allow-Origin”). Kod stanu: 200.
Zablokowano żądanie do zasobu innego pochodzenia: zasady „Same Origin Policy” nie pozwalają wczytywać zdalnych zasobów z „http://localhost:8000/api/links” (brakujący nagłówek CORS „Access-Control-Allow-Origin”). Kod stanu: 200.

## Przewidywania

Przewiduję, że curl http://192.168.56.X:8000/health wykonany na VM-ce nie zadziała, jeśli 192.168.56.X nie jest rzeczywistym adresem przypisanym do tej VM.

### Z9

## Notatka wstępna 

CORS działa tak, że serwer przez Access-Control-Allow-Origin mówi przeglądarce, którym stronom wolno czytać jego odpowiedzi.

CORS nie musi oznaczać, że żądanie nie dotarło do serwera. Często dotarło, serwer odpowiedział 200, tylko przeglądarka nie pozwoliła JavaScriptowi przeczytać odpowiedzi.

## Zadania

## Hipoteza

Spodziewam się, że oba żądania dotrą do API, ale odpowiedź może różnić się nagłówkami, gdy podam Origin

## a) Materiał dowodowy

1. Żądania CURL 
- curl -i http://10.17.216.90:8000/api/links:

HTTP/1.1 200 OK
date: Mon, 17 Aug 2026 11:24:57 GMT
server: uvicorn
content-length: 224
content-type: application/json

[{"code":"UhebSc9","url":"https://example.com/bardzo/dluga/sciezka","clicks":0,"created_at":"2026-08-17T10:43:55.208102Z"},{"code":"VzFuhAx","url":"https://example.com","clicks":6,"created_at":"2026-08-17T08:02:30.478645Z"}]

- curl -i -H 'Origin: http://10.17.216.90:3000' http://10.17.216.90:8000/api/links

HTTP/1.1 200 OK
date: Mon, 17 Aug 2026 11:26:40 GMT
server: uvicorn
content-length: 224
content-type: application/json

[{"code":"UhebSc9","url":"https://example.com/bardzo/dluga/sciezka","clicks":0,"created_at":"2026-08-17T10:43:55.208102Z"},{"code":"VzFuhAx","url":"https://example.com","clicks":6,"created_at":"2026-08-17T08:02:30.478645Z"}]

## Hipoteza 2

Dodanie nagłówka Origin może spowodować, że serwer doda nagłówki CORS do odpowiedzi

## Sprawdzenie 2 

Wykonałem dwa takie same żądania do /api/links, jedno bez Origin

## Wyniki

Oba żądania zwróciły HTTP/1.1 200 OK, a zestaw nagłówków odpowiedzi był taki sam; w odpowiedzi z Origin również nie pojawił się nagłówek Access-Control-Allow-Origin

Serwer odpowiada poprawnie nawet na żądanie zawierające Origin, ale nie dodaje nagłówka CORS pozwalającego przeglądarce udostępnić odpowiedź JavaScriptowi.

2. Zakładka Network w przeglądarce:

Status: 200 OK
HTTP/1.1

content-length: 49
content-type: application/json
date: Mon, 17 Aug 2026 11:37:29 GMT
server: uvicorn

przeglądarka nie pozwoliła JavaScriptowi odczytać odpowiedzi, bo serwer nie odesłał zgody CORS

3. Front po błędzie fetch() wykonuje dodatkową próbę połączenia bez potrzeby odczytywania odpowiedzi i jeśli ona się powiedzie, rozpoznaje, że serwer działa, a pierwszą odpowiedź zablokował CORS.

## Notatka Doadatkowa

1 → API działa + brak nagłówka CORS
2 → najmocniejszy dowód CORS: 200 OK, ale przeglądarka blokuje odpowiedź
3 → API żyje/da się do niego dotrzeć, ale sam CORS-u nie udowadnia

## b) Rozstrzygnij trzy pary

1. Różni sie port 3000 i 8000 - inny
2. Różni sie hot localhost i 193.168.56.X - inny
3. Rózni sie protokół http i https - inny 

## c) Napraw - po stronie serwera

Ustawiłem w .env CORS_ORIGINS=http://localhost:3000. 
Ustawiłem w config.js http://localhost:3000.

## d) Próba kontrolna 

Dla CORS localhost i adres IP to dwa różne originy, nawet jeśli prowadzą do tej samej maszyny, ponieważ host jest częścią originu i musi się dokładnie zgadzać.

## e) Drugi dowód

|                        | przed naprawą | po naprawie                                               |
| curl bez `Origin`      | brak          |  brak                                                     |
| curl z `Origin: …3000` | brak          |  access-control-allow-origin: http://localhost:3000       |

## Notatka Dodatkowa

1. Kiedy serwer dodaje CORS?
Odp.: Gdy dostanie Origin i ten adres jest na liście dozwolonych.
2. Czemu curl bez Origin nic nie mówi o CORS?
Odp.: Bo sprawdza tylko, czy API działa, a nie czy pozwala danemu originowi czytać odpowiedź.
3. Kto blokował odpowiedź?
Odp.: Przeglądarka, bo serwer nie wysyłał wcześniej zgody Access-Control-Allow-Origin.

## f) Utwal konfiguracje

CORS_ORIGINS=http://localhost:3000

w .env

## Notatki końcowe

1. Kto zablokował odpowiedź i na jakiej podstawie?
Odp.: Przeglądarka, bo w odpowiedzi brakowało pasującego Access-Control-Allow-Origin.
2. Dlaczego naprawa była po stronie API?
Odp.: Bo to API musi wysłać zgodę CORS dla originu frontu; front nie może sam sobie tej zgody nadać.
3. Od czego zacząłbym teraz?
Odp.: Najpierw F12 → Network → żądanie → Headers, sprawdziłbym status, Origin i czy odpowiedź zawiera Access-Control-Allow-Origin.


### Z10

## Przewidywania

Usługa najpewniej nie wystartuje, bo ręcznie uruchomiona plikacja już zajmuje ten sam port, więc drugi proces dostanie błąd zajetego adresu.


