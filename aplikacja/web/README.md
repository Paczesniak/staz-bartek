# Front skracacza linków

Interfejs przeglądarkowy do API skracacza linków. Czysty HTML, CSS i JavaScript — **bez
frameworków, bez `npm`, bez kroku budowania i bez pobierania czegokolwiek z internetu**.
Wszystko, co jest potrzebne, leży w tym katalogu, więc strona działa również na maszynie
odciętej od sieci.

Front nie ma własnego backendu ani bazy. Cała jego wiedza pochodzi z API, które odpytuje
z poziomu przeglądarki.

## Pliki

| Plik | Za co odpowiada |
|---|---|
| `index.html` | struktura strony: pasek stanu, formularz, lista linków |
| `style.css` | wygląd; motyw jasny i ciemny wybierany automatycznie wg ustawień systemu |
| `app.js` | cała logika: odpytywanie API, walidacja, rysowanie listy, rozpoznawanie awarii |
| `config.js` | **jedyne** miejsce z adresem API |

## Jak uruchomić

Strony **nie otwieraj podwójnym kliknięciem** w pliku `index.html`. Adres wyglądałby wtedy
`file:///...`, a przeglądarka traktuje takie strony inaczej niż zwykłe i część rzeczy nie
zadziała. Front zawsze serwujemy przez serwer statyczny.

Z tego katalogu (`aplikacja/web`):

```bash
python3 -m http.server 3000
```

Potem w przeglądarce: <http://localhost:3000>.

Zatrzymanie serwera: `Ctrl+C` w terminalu, w którym działa.

Jeśli front stoi na maszynie wirtualnej, a przeglądarka jest na hoście, użyj adresu IP tej
maszyny zamiast `localhost`, np. `http://192.168.56.10:3000` — pod warunkiem że serwer
nasłuchuje na wszystkich interfejsach, a nie tylko na `127.0.0.1`.

Sam serwer statyczny nie ma nic wspólnego z API: podaje wyłącznie cztery pliki z tego
katalogu. Wszystkie dane strona pobiera osobno, już z przeglądarki, spod adresu z `config.js`.

## Jak zmienić adres API

W pliku `config.js`:

```js
window.APP_CONFIG = {
  API_BASE_URL: "http://localhost:8000",
};
```

To jest **jedyne miejsce w całym froncie, w którym występuje adres API**. W `app.js` nie ma
go nigdzie na sztywno — jest tam wyłącznie odczyt tej wartości. Zmiana adresu to podmiana
jednej linijki w jednym pliku, bez przeszukiwania kodu i bez przebudowywania czegokolwiek.

Zasady dla wartości:

- podajemy schemat, host i port — bez ukośnika na końcu i bez ścieżki,
  poprawnie: `"http://192.168.56.10:8000"`, niepoprawnie: `"192.168.56.10:8000/api/"`
- pusty łańcuch `""` znaczy „API jest pod tym samym adresem i portem co ta strona"
  i sprawia, że front wysyła żądania względne

Po zmianie odśwież stronę **z pominięciem pamięci podręcznej** (`Ctrl+Shift+R`) — inaczej
przeglądarka może użyć starej wersji `config.js` i będziesz szukał błędu w złym miejscu.
Aktualnie używany adres strona wypisuje w nagłówku i w stopce; to pierwsza rzecz do
sprawdzenia, gdy coś nie działa.

## Pasek stanu API

Pasek u góry strony odpytuje `/health` przy starcie i potem co 15 sekund. Przycisk
„Sprawdź teraz" wymusza sprawdzenie natychmiast. Pasek ma cztery stany:

| Kolor | Stan | Co znaczy |
|---|---|---|
| szary | Sprawdzam stan API | pierwsze zapytanie jeszcze trwa |
| zielony | API działa | `/health` odpowiedziało, baza zgłasza się jako sprawna |
| pomarańczowy | API działa, baza danych nie | proces API żyje i odpowiada, ale sam mówi, że nie ma połączenia z bazą |
| czerwony | API nieosiągalne / odpowiedź zablokowana | brak odpowiedzi albo odpowiedź zatrzymana przez przeglądarkę |

Rozróżnienie zielony/pomarańczowy jest tu najważniejsze: **„serwer odpowiada" i „aplikacja
działa" to dwie różne rzeczy.** Proces może odpowiadać na `/health` i jednocześnie nie
potrafić zapisać ani jednego linku.

## Rodzaje awarii i co znaczą

Strona nie pokazuje jednego uniwersalnego „coś poszło nie tak". Rozpoznaje rodzaj awarii
i przy każdym wypisuje, co dokładnie się stało i od czego zacząć szukanie przyczyny.

### 1. API nie odpowiada

Przeglądarka nie dostała żadnej odpowiedzi — nawet błędnej. Pod tym adresem i portem nikt
nie odebrał. Typowe przyczyny: proces nie został uruchomiony, wywrócił się po starcie,
nasłuchuje na innym porcie albo nasłuchuje wyłącznie na `127.0.0.1` i przez to jest
niewidoczny z innej maszyny.

Od czego zacząć: czy proces w ogóle chodzi, `ss -tlnp` na maszynie z API, `curl -i` z tej
samej maszyny, na której API stoi.

### 2. Odpowiedź zablokowana przez przeglądarkę (CORS)

Żądanie wyszło, serwer odpowiedział — ale kod strony tej odpowiedzi nie zobaczył, bo
przeglądarka ją przechwyciła i odrzuciła. **To reguła bezpieczeństwa przeglądarki, a nie
awaria sieci ani błąd serwera.** Dokładnie to samo żądanie wykonane `curl`-em zadziała,
bo `curl` żadnych reguł CORS nie sprawdza.

Strona rozpoznaje ten przypadek i **odróżnia go od zwykłego braku połączenia**, mimo że
`fetch` w obu przypadkach rzuca ten sam wyjątek `TypeError: Failed to fetch`. Jak to robi —
patrz komentarz przy funkcji `rozroznijAwarieSieci()` w `app.js`; to jedna z ciekawszych
rzeczy w tym kodzie.

Od czego zacząć: konsola przeglądarki (`F12`) — jest tam oryginalny komunikat z nazwą
brakującego nagłówka. Potem zakładka `Network`: żądanie ze statusem `200` przy jednoczesnym
błędzie na stronie to podpis CORS-a. Na koniec porównaj origin strony z adresem API i wypisz,
czym dokładnie się różnią.

Reszty dochodzisz sam — komunikat na stronie mówi, co się dzieje, ale świadomie nie podaje
gotowego rozwiązania.

### 3. API działa, baza danych nie

`/health` odpowiedziało (najczęściej statusem `503`), ale API samo zgłasza, że nie ma
połączenia z bazą. Warstwa aplikacji jest sprawna, warstwa danych nie. Debugowanie frontu
nic tu nie da — droga przeglądarka → API jest w porządku, skoro odpowiedź dotarła.

### 4. Błąd `4xx` — serwer odrzucił żądanie

Świadoma decyzja API: żądanie doszło i zostało zrozumiane, ale jest niepoprawne. Strona
pokazuje wtedy treść pola `detail` z odpowiedzi, czyli powód podany przez serwer.
Najczęstsze: `400` — niepoprawny adres, `404` — nie ma takiego kodu, `409` — kod już zajęty.
Poprawka jest po stronie danych, nie serwera.

### 5. Błąd `5xx` — serwer się wywrócił

Żądanie doszło i zostało przyjęte, ale obsługa padła w środku. To nie jest wina frontu ani
danych z formularza. Przyczyna jest w logach procesu API — przy błędzie `5xx` zostaje tam
ślad wyjątku z nazwą pliku i numerem linii.

### 6. Nieczytelna odpowiedź

Odpowiedź przyszła, ale nie jest poprawnym JSON-em. Zwykle znaczy to, że pod tym adresem
odpowiada coś innego niż API — na przykład serwer statyczny albo proxy, które zwróciło
własną stronę błędu.

## Walidacja po stronie przeglądarki

Zanim front wyśle cokolwiek do API, sprawdza dane u siebie:

- adres musi dać się rozebrać jako URL i mieć schemat `http://` albo `https://`
- własny kod, jeśli podany, musi pasować do `[A-Za-z0-9_-]` i mieć najwyżej 32 znaki

To oszczędza jedno żądanie sieciowe, ale **niczego nie gwarantuje**: walidacja w przeglądarce
jest wygodą dla użytkownika, nie zabezpieczeniem. Każdy może ją ominąć, wysyłając żądanie
`curl`-em. Prawdziwe sprawdzanie danych musi być po stronie API — i dlatego strona i tak
obsługuje odpowiedź `400`.

## Znane ograniczenia

- Kopiowanie do schowka wymaga tak zwanego bezpiecznego kontekstu: `https://` albo
  `http://localhost`. Strona otwarta po adresie IP użyje metody zapasowej, a gdy i ta
  zawiedzie — wypisze adres do skopiowania ręcznie.
- Brak stronicowania listy. Przy kilku tysiącach linków strona zacznie zwalniać.
- Front nie ma logowania ani żadnej autoryzacji. Każdy, kto otworzy stronę, może dodawać
  i usuwać linki.
