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
