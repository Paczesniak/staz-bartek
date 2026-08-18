### Z1

## Notatka wstępna

Docker: obraz a kontener
	- Obraz = gotowy, tylko do odczytu szablon aplikacji.
	- Kontener = uruchomiona instancja obrazu z własną zapisywalną warstwą.
	- Obraz składa się z wielu warstw, dzięki czemu Docker może je współdzielić i używać cache.

Kontener a maszyna wirtualna
	- VM ma własny system operacyjny i własne jądro.
	- Kontener korzysta z jądra systemu hosta i izoluje tylko procesy, pliki, sieć itd.
	- Dzięki temu kontenery są mniejsze i uruchamiają się szybciej, bo nie muszą startować całego systemu operacyjnego.

## Zadania

1. docker version - serwer ma wersje 29.1.3 i tak samo klient. 
Sprawidziłem czy działa w tle za pomocą (systemctl status docker). W tle działa część serwerowa Dockera. 

2. docker images -  pokazuje obraz czyli szblony do tworzenia kontenerów
docker ps -a - pokazuje wszystkie kontenery utworzonych obrazów

3. 
