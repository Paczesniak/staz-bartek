# Feedback po dniu aplikacja

## Najpierw sprostowanie — błąd był po mojej stronie

Moduł `cors` odbił cię **trzynaście razy**. Nie dlatego, że robiłeś źle.

Walidator wymagał, żeby w `config.js` stał adres IP maszyny, i odrzucał `localhost`. Napisałem go przy założeniu, że masz sieć host-only — a ty masz NAT z przekierowaniem portów, bo inaczej nie działało ci SSH. Przy takiej sieci `localhost` **jest poprawną odpowiedzią**, i to była twoja odpowiedź.

Walidator jest już poprawiony: sprawdza spójność między `config.js` a `CORS_ORIGINS`, a nie konkretną wartość. Przepraszam za stracony czas — te trzynaście podejść nie obciąża twojego wyniku.

Wniosek na przyszłość dla ciebie, nie dla mnie: **kiedy jesteś pewny swojego rozumowania, a narzędzie mówi „źle" — zgłoś to od razu.** W realnej pracy to samo dotyczy testów CI i cudzych skryptów. Nie zawsze mylisz się ty.

## Co zrobiłeś dobrze

**Z9 zrobiłeś dokładnie tak, jak się diagnozuje.** Dwa żądania `curl` różniące się jedną rzeczą — nagłówkiem `Origin` — i porównanie odpowiedzi. Zapisałeś hipotezę przed sprawdzeniem, potem wynik: oba `200 OK`, oba z tym samym zestawem nagłówków, `Access-Control-Allow-Origin` nie ma w żadnym.

To jest sedno CORS-a, którego nie umiałeś rozwiązać na rozmowie: **serwer odpowiedział poprawnie, blokadę postawiła przeglądarka.** `curl` widzi dane, karta w przeglądarce nie. Masz to teraz nie z definicji, tylko z własnego eksperymentu.

**Moduł `logi` za pierwszym podejściem, oba zadania.** Przy okazji rozpisałeś sobie opcje `journalctl` — `-u`, `-f`, `-n`, `-b`, `--since`, `-p err`, `--no-pager`. To jest notatka, do której naprawdę się wraca.

**Trzymasz strukturę notatek przez cały dzień.** Notatka wstępna → przewidywania → zadania → wyniki, konsekwentnie od Z1 do Z15. Przy zadaniach z 🔮 przewidywanie faktycznie stoi przed sprawdzeniem.

**Zamknąłeś 6 z 6 modułów.** Dzień był rozciągnięty, ale nie zostawiłeś ogona.

## Co poprawić

**`notatki/aplikacja.md.save` wjechał do repozytorium.** To plik, który `nano` zostawia po nieładnym wyjściu z edytora. W F2 był `.swp` po `vimie` — wtedy dopisałeś `*.swp` do `.gitignore` i dobrze. Dołóż tam teraz `*.save`, usuń plik z repozytorium (`git rm --cached`) i temat znika na zawsze.

**Moduł `usluga`: trzy nieudane podejścia, w każdym te same sześć warunków o `linkbox-staging`.** Druga usługa obok pierwszej to jedna z rzeczy, które w pracy robi się co tydzień — warto, żebyś umiał powiedzieć, co dokładnie cię tam zatrzymało. Zapytam o to na obronie, bez podchwytliwości.

**Z14 skwitowałeś „Nie ma problemu".** Formalnie dobrze — naprawiłeś to w Z9. Ale to była **próba kontrolna**: sprawdzian, czy umiesz odróżnić „nic tu nigdy nie było zepsute" od „było zepsute i naprawiłem to wtedy a wtedy". W raporcie z awarii ta różnica jest całą treścią.

## Na dziś — kontenery

Bierzesz tę samą aplikację, którą wczoraj uruchamiałeś ręcznie, i pakujesz ją w obraz Dockera. Potem dwa kontenery naraz przez `docker compose`, wolumen na dane i awaria do rozgryzienia na koniec.

Dwie rzeczy z wczoraj wracają dziś w nowej postaci i będą ci potrzebne:

- **`APP_HOST=127.0.0.1` znaczy w kontenerze coś innego niż na maszynie.** Wczoraj to ustawienie sprawiło, że aplikacja była niewidoczna z Windowsa. Dziś zrobi to samo, tylko granica przebiega w innym miejscu.
- **Log czytasz od pierwszej linii.** Aplikacja wypisuje przy starcie komplet ustawień, z jakimi wystartowała. To zadziała identycznie w kontenerze — zmieni się tylko polecenie, którym ten log oglądasz.

Zaczynasz od instalacji Dockera, **przed pierwszym zadaniem** — jeden krok wymaga wylogowania i zalogowania z powrotem, a w połowie dnia to kosztuje więcej niż na starcie. Wszystko jest w pliku z zadaniami.
