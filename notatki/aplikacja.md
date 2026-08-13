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


