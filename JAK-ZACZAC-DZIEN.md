# Jak zacząć nowy dzień

Za każdym razem, gdy dostaniesz materiały na kolejny dzień, robisz to samo.
Wszystko **na maszynie wirtualnej**, nie na Windowsie.

## 1. Pobierz i zainstaluj

```bash
cd ~/staz
git pull
./zainstaluj.sh
```

`zainstaluj.sh` sam znajdzie nową paczkę, rozpakuje ją, zainstaluje lab
i posprząta po sobie. Twoje zaliczenia i notatki z poprzednich dni zostają
nietknięte — instalacja tylko **dokłada** nowy dzień obok starych.

Gdyby zabrakło `unzip`:

```bash
sudo apt install unzip
```

## 2. Sprawdź, że działa

```bash
lab dzien aplikacja     # nazwa dnia jest w pliku z zadaniami
lab moduly              # lista modułów w kolejności
```

Jeśli `lab` nie działa zaraz po instalacji — wyloguj się i zaloguj ponownie.

## 3. Pracuj modułami

```bash
lab start <moduł>       # przygotowuje środowisko wszystkich zadań modułu
                        # ← ZAWSZE zacznij od tego, inaczej zadania nie będą miały stanu

lab grade <moduł>       # sprawdza, co już masz zrobione; możesz powtarzać do skutku

lab koniec <moduł>      # zamyka moduł i przechodzi do następnego
```

Przydatne:

```bash
lab status              # gdzie jesteś
lab sprawdz Z07         # sprawdź pojedyncze zadanie
lab reset Z07           # zacznij jedno zadanie od zera
lab pomoc
```

## 4. Zamknij dzień

```bash
lab koniec aplikacja    # generuje raport dnia
```

Raport trafia do `wyniki/` w tym repozytorium. Potem commit i push — **bez
tego dzień nie jest oddany**:

```bash
git add notatki/ wyniki/
git commit -m "docs: notatki i raport dnia"
git push
```

## Zasady, które ułatwiają życie

**Commituj po każdym module**, nie raz na koniec dnia. Pracujemy zdalnie, więc
Twoje commity są jedynym sposobem, żebym widział, gdzie jesteś. Jak utkniesz na
trzy godziny, chcę o tym wiedzieć tego samego dnia.

**Notatki pisz na bieżąco**, nie po fakcie. Przy zadaniach oznaczonych 🔮
przewidywanie zapisujesz **przed** sprawdzeniem — o to w nich chodzi.

**Zablokowany dłużej niż 30 minut?** Zapisz, na czym, przejdź dalej, wróć
później. Rozstrzygniemy na obronie.

**AI wolno.** Jedyny warunek: zanim wciśniesz Enter, umiej powiedzieć, co dane
polecenie zrobi. `sudo` czegoś, czego nie umiesz opisać, nie uruchamiasz.
