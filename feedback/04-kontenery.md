# Feedback po dniu kontenery

## Odczytałem

```
01101011 01101111 01101110 01101001 01100101 01100011 00100000 01000011 01001111 01010010 01010011
```

**koniec CORS.**

Masz rację i masz ją podwójnie: raz dlatego, że moduł `cors` odbił cię trzynaście razy przez mój błąd, a drugi raz dlatego, że temat wrócił potem w Z4 i w awarii. Sprawdziłem materiał na oba pozostałe dni: **słowo „CORS" nie pada w nich ani razu.** Czwartek to baza danych, piątek to CI. Temat jest zamknięty.

Zostawiłeś to na końcu pliku, po ostatnim zadaniu, zapisane tak, żeby trzeba było się zatrzymać. Dobrze zrobiłeś. Notatki są po to, żeby ktoś je czytał, a jeśli coś w programie nie działa, to najlepszy moment na powiedzenie tego jest wtedy, kiedy jeszcze da się to zmienić.

## Co zrobiłeś dobrze

**Z10 jest najlepszą rzeczą, jaką napisałeś przez cały staż.** Trzy problemy, każdy rozpisany jako objaw → hipoteza → sprawdzenie → przyczyna → poprawka. Tak wygląda notatka z prawdziwej awarii i tak wygląda wpis do post-mortemu.

Najważniejsze jest to, że **trzeciego problemu nie było w zadaniu**. Zadanie podłożyło ci dwie wady. Ty zauważyłeś, że `compose.yaml` wygląda poprawnie, a `docker compose config` pokazuje co innego — i zamiast poprawić wartość, poszedłeś o poziom wyżej i znalazłeś mechanizm: `compose.override.yaml` nadpisuje. To jest różnica między naprawianiem objawu a rozumieniem systemu.

Twoje zdanie: *„docker compose ps mówi tylko, że kontenery działają, ale nie że aplikacja w środku działa poprawnie i używa właściwych danych"*. Zapamiętaj je. Wracasz do niego w piątek, kiedy pipeline zaświeci na zielono.

**W Z7 doszedłeś sam do właściwej naprawy.** `RUN mkdir -p /data && chown appuser:appuser /data` — katalog i jego właściciel przygotowane w obrazie, **przed** `USER`. To jest dokładnie to rozwiązanie, do którego zadanie miało cię doprowadzić, i trafiłeś w nie bez podpowiedzi.

Przy okazji zrobiłeś coś, czego nie prosiłem: kod aplikacji w `/app` został własnością roota, a zapisywalny jest wyłącznie `/data`. Znaczy to, że proces twojej aplikacji **nie może nadpisać własnego kodu**. W Kubernetes robi się to samo ustawieniem `readOnlyRootFilesystem` i uchodzi za dobrą praktykę. Wyszło ci przy okazji — ale wyszło.

**`compose.yaml` jest dobry.** Cztery ukośniki w `sqlite:////data/links.db` (ta jedna kreska kosztuje ludzi godziny), `nginx:1.27-alpine` z konkretnym tagiem zamiast `latest`, front podmontowany `:ro`, polityka restartu na obu usługach.

**W `Dockerfile.zle` użyłeś `COPY --chown`**, choć nigdzie o tym nie pisałem. Warto wiedzieć, że to nie tylko krótsze od `chown -R` — `chown -R` na skopiowanym katalogu zmienia metadane wszystkich plików, a w obrazie warstwowym oznacza to **zapisanie ich kopii w nowej warstwie**. Przy dużym projekcie obraz puchnie dwukrotnie. `COPY --chown` załatwia to bez duplikacji.

**Sześć modułów w jeden dzień, bez ogona.**

## Co poprawić

**Z3: drugie przewidywanie jest kopią pierwszego.** Pytanie brzmiało odwrotnie — co, gdy kopiowanie *całego katalogu* stoi **przed** instalacją zależności. Odpowiedź to „tak, zmieni się".

Najważniejsze jest jednak to, że **twoje własne pomiary to obaliły**: 10,2 s kontra 45,7 s. Zmierzyłeś różnicę, zapisałeś ją i nie wróciłeś do przewidywania. Cała metoda „przewiduj → sprawdź → skonfrontuj" zatrzymała się na drugim kroku. W Z4 i Z6 zrobiłeś to poprawnie — w Z6 wprost napisałeś, które przewidywanie się nie potwierdziło. Czyli umiesz; tu po prostu nie zamknąłeś pętli.

Brakuje też dwóch rzeczy z treści zadania: numeru kroku, od którego cache przestał działać (z twojego logu: `Step 5/9`), i notatki końcowej — dwóch zdań o tym, po co `requirements.txt` kopiuje się osobno i ile buildów dziennie musiałbyś robić, żeby ta różnica cię obchodziła.

**Rozmiar obrazu: zapisałeś 78,7 MB.** To niemożliwe — sam `python:3.12-slim` waży 123 MB, a doszły do niego twoje zależności. Sprawdź `docker images linkbox` jeszcze raz i zobacz, którą kolumnę czytałeś. Ta liczba nie jest ozdobnikiem: na niej stoi porównanie z `.venv`, czyli cała pointa tamtej notatki.

**`compose.override.yaml` wjechał do repozytorium** (commit `a20ba65`), a trzy commity później go usunąłeś. Usunąłeś słusznie — ten plik podłożył ci lab i nie należy do twojego projektu. Ciekawi mnie co innego: zacommitowałeś wersję **naprawioną**, a nie podłożoną, czyli poprawiłeś nakładkę zamiast ją skasować. To działa i nie jest błędem. Pytanie brzmi, czy w tamtym momencie wiedziałeś, że ten plik jest ciałem obcym.

**Czwarty raz ta sama rzecz w commitach.** `ed26d4c` i `f042813` — oba „feat: stos compose z API i frontem". `a20ba65` i `d45256c` — oba „docs: modul awaria". `3f3a3d2` i `37ec0e9` — oba „docs: modul dane". Za każdym razem pierwszy niesie pliki, drugi notatki, a komunikat jest przepisany.

Historia commitów jest dokumentacją, którą czyta się wtedy, kiedy coś się zepsuło i trzeba znaleźć moment, w którym przestało działać. Dwa identyczne wpisy obok siebie tej odpowiedzi nie dają. W piątek zobaczysz, że każdy push uruchamia przebieg CI — od tego momentu komunikat commita zaczyna odpowiadać na pytanie „co takiego zrobiłem, że pipeline stanął na czerwono".

**Moduł `uruchomienie`: dwa nieudane podejścia, za każdym razem te same trzy warunki.** To nie były trzy problemy, tylko jeden: nie było działającego kontenera, więc walidator nie miał czego sprawdzić ani pod kątem CORS, ani `/health`. Warto to widzieć — przy trzech czerwonych liniach naraz najczęściej jest jedna przyczyna, a nie trzy.

## Na jutro — baza danych

Dziś twoja aplikacja trzyma dane w pliku SQLite w wolumenie. Jutro dostanie prawdziwą bazę: **PostgreSQL jako trzecia usługa w tym samym stosie** — z własnym wolumenem, healthcheckiem i zależnością od gotowości, a nie od samego startu. Potem przeprowadzka danych ze starej bazy do nowej, kopia zapasowa, odtworzenie po skasowaniu tabeli i awaria na koniec.

Trzy rzeczy z dziś wracają jutro w mocniejszej postaci:

- **`docker compose config`** — dziś dał ci przełom w Z10. Jutro będzie podstawowym narzędziem, bo dojdzie plik `.env`, a wartości zaczną się brać z miejsca, którego nie widać w `compose.yaml`.
- **Wolumen i uprawnienia.** Wiesz już, że pusty wolumen podmontowany pod nieprzygotowaną ścieżkę powstaje jako `root`. Obraz Postgresa rozwiązuje to inaczej niż twoja aplikacja — zobacz jak.
- **`DATABASE_URL`.** Ta sama zmienna, inny adres. Zmienia się nie tylko ścieżka, ale i to, **czym** jest miejsce po drugiej stronie.

Jedna rzecz na wejściu, ważniejsza od reszty: **hasło do bazy nie trafia do `compose.yaml`.** Ten plik jest w repozytorium, a repozytorium jest na GitHubie — hasło wpisane wprost jest hasłem opublikowanym. Zadanie mówi, gdzie ma trafić zamiast tego, a ostatni moduł dnia sprawdzi, czy nie ma go w żadnym śledzonym pliku.

Instalacja jak zawsze:

    cd ~/staz
    git pull
    ./zainstaluj.sh
