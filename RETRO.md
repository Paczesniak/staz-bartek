# RETRO

## 1. Co potrafię dziś, czego nie potrafiłem w poniedziałek?

1. Dużo swobodniej poruszam się po Linuxie. Przypomniałem sobie podstawowe komendy, pracę na plikach i katalogach, uprawnienia oraz podstawy pracy z terminalem.
   Zadanie: ćwiczenia z Linuxa, SSH i pracy na plikach w repozytorium.

2. Lepiej poruszam się po GitHubie i rozumiem podstawy działania Gita oraz GitHub Actions. Potrafię zrobić commit, push, sprawdzić status repozytorium i zdiagnozować podstawowe problemy z pipeline.
   Zadanie: tworzenie `ci.yml`, uruchamianie pipeline w GitHub Actions i naprawa czerwonego builda.

3. Na początku miałem tylko ogólne pojęcie, czym jest Docker. Teraz potrafię budować obrazy, uruchamiać kontenery, pracować z Docker Compose, wolumenami, siecią i bazą danych. 
   Zadanie: uruchomienie aplikacji w Docker Compose, dodanie PostgreSQL, healthchecka i smoke testu.

4. Rozumiem już, czym jest błąd CORS i wiem, że nie zawsze da się go naprawić po stronie frontendu. Potrafię rozpoznać, że problem leży po stronie serwera i wiem, gdzie szukać konfiguracji CORS.
   Zadanie: diagnozowanie problemu z komunikacją frontend–API i konfiguracją `CORS_ORIGINS`.

5. Nauczyłem się lepiej czytać logi i szukać w nich pierwszej konkretnej przyczyny błędu, zamiast skupiać się tylko na ostatnim komunikacie.
   Zadanie: diagnozowanie błędów PostgreSQL, restartującego się kontenera, błędów CI oraz smoke testu

## 2. Które zadanie było najtrudniejsze i dlaczego?

Najtrudniejsze były dla mnie zadania związane z diagnozowaniem i naprawianiem błędów. Najwięcej czasu zajmowało mi znalezienie miejsca, w którym faktycznie był problem, ponieważ nie miałem jeszcze doświadczenia i nie zawsze wiedziałem, od czego zacząć. Trudne były też niektóre zadania związane z konfiguracją plików, ponieważ nawet mały błąd w ustawieniach potrafił zatrzymać działanie całej aplikacji.

## 3. Gdzie straciłem najwięcej czasu i co zrobiłbym inaczej?

Najwięcej czasu straciłem na diagnozowaniu problemów z Docker Compose i bazą danych.

## 4. Czego nadal nie rozumiem?

1. Nie do końca rozumiem wszystkie opcje w compose.yaml.
2. Podobnie mam z konfiguracją ci.yml
3. Nadal potrzebuje wiecej praktyki, żeby samemu rozumieć, co robią poszczególne linijki bez pomocy AI.

## 5. Jak korzystałem z AI i co bym zmienił?

AI pomagało mi głównie przy analizie logów, formułowaniu dokładniejszych poleceń i konfiguracji. Czasem jednak źle interpretowało sytuację, np. przy rzekomym udostępnieniu hasła w Git, dlatego zacząłem częściej sam sprawdzać, czy problem faktycznie istnieje, zamiast od razu ufać podpowiedzi.

## 6. Co robię dalej?

1. Chcę lepiej rozumieć Dockera i Docker Compose.
   Pierwszy krok: spróbować uruchomić jedną z moich istniejących aplikacji za pomocą Docker Compose

2. Chcę lepiej rozumieć CI/CD i GitHub Actions.
   Pierwszy krok: doadać prosty pipeline CI/CD do jednej z moich isniejących aplikacji

3. Chcę lepiej diagnozować błędy bez ciągłej pomocy AI.
   Pierwszy krok: przy kolejnym błędzie najpierw sam przeczytać logi i zapisze swoją hipotezy zanim poproszę AI o pomoc. (ogranicze jego pomoc)
