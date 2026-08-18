#!/bin/bash
# ==============================================================================
# zainstaluj.sh — instalacja labu na maszynie stażysty
# ==============================================================================
#
# Ten plik leży w twoim repozytorium. Używasz go za każdym razem, gdy dostaniesz
# materiały na nowy dzień:
#
#     git pull && ./zainstaluj.sh
#
# Skrypt sam znajdzie najnowszą paczkę, rozpakuje ją, zainstaluje lab
# i posprząta po sobie. Nie musisz pamiętać nazwy pliku ani kolejności kroków.
#
# Gdyby kiedyś wziął nie ten dzień co trzeba, możesz wskazać go wprost:
#
#     ./zainstaluj.sh kontenery
# ==============================================================================

set -Eeuo pipefail

KATALOG_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$KATALOG_REPO"

# ------------------------------------------------------------------------------
# Znajdź paczkę
# ------------------------------------------------------------------------------

shopt -s nullglob
PACZKI=(lab-*.zip)
shopt -u nullglob

if ((${#PACZKI[@]} == 0)); then
  printf 'Nie widzę żadnej paczki lab-*.zip w %s\n' "$KATALOG_REPO" >&2
  printf 'Zrobiłeś „git pull"? Jeśli tak, a paczki nadal nie ma — napisz do mentora.\n' >&2
  exit 1
fi

# Wskazany dzień ma pierwszeństwo. Bez argumentu bierzemy najnowszą paczkę
# według czasu modyfikacji — po „git pull" to zawsze ta, która właśnie
# przyszła. Jest jednak przypadek, w którym ten czas nic nie mówi: po świeżym
# „git clone" wszystkie pliki dostają ten sam znacznik i wybór robi się
# przypadkowy. Dlatego przy kilku paczkach mówimy głośno, którą wzięliśmy.
if [[ -n "${1:-}" ]]; then
  PACZKA="lab-${1}.zip"
  if [[ ! -f "$PACZKA" ]]; then
    printf 'Nie widzę paczki %s w %s\n\n' "$PACZKA" "$KATALOG_REPO" >&2
    printf 'Paczki, które tu są:\n' >&2
    printf '  %s\n' "${PACZKI[@]}" >&2
    exit 1
  fi
else
  PACZKA="$(ls -t -- "${PACZKI[@]}" | head -n 1)"
fi

printf '\n== Instalacja labu ==\n\n'
printf '  paczka: %s\n' "$PACZKA"
if ((${#PACZKI[@]} > 1)) && [[ -z "${1:-}" ]]; then
  printf '          (najnowsza z %d w repozytorium — inny dzień: ./zainstaluj.sh <nazwa-dnia>)\n' "${#PACZKI[@]}"
fi

# ------------------------------------------------------------------------------
# Rozpakuj
# ------------------------------------------------------------------------------

if ! command -v unzip > /dev/null 2>&1; then
  printf '\nBrakuje polecenia „unzip". Zainstaluj je i uruchom ponownie:\n' >&2
  printf '  sudo apt install unzip\n\n' >&2
  exit 1
fi

printf '  → rozpakowuję\n'
unzip -qo -- "$PACZKA"

if [[ ! -f lab/install.sh ]]; then
  printf '\nW paczce nie ma lab/install.sh — coś jest nie tak z archiwum.\n' >&2
  printf 'Napisz do mentora i nie kasuj pliku %s.\n\n' "$PACZKA" >&2
  exit 1
fi

# ------------------------------------------------------------------------------
# Zainstaluj (install.sh sam poprosi o sudo)
# ------------------------------------------------------------------------------

printf '  → instaluję (poprosi o hasło do sudo)\n\n'
bash lab/install.sh "$(id -un)"

# ------------------------------------------------------------------------------
# Posprzątaj
# ------------------------------------------------------------------------------
#
# Rozpakowany katalog jest już niepotrzebny — lab żyje w /opt/lab. Archiwum
# ZOSTAJE: przyszło przez repozytorium, więc git je śledzi, a skasowanie
# zrobiłoby bałagan w „git status". Waży kilkadziesiąt kilobajtów i jest
# zapisem tego, którą wersję labu dostałeś którego dnia.

if [[ -d lab ]]; then
  rm -rf -- lab
  printf '\n  → posprzątałem rozpakowany katalog\n'
fi

printf '\n== Gotowe ==\n\n'
printf 'Lab jest zainstalowany. Zacznij od:\n\n'
printf '  lab moduly        # co jest dzisiaj do zrobienia\n\n'
printf 'Jeśli „lab" nie działa, wyloguj się i zaloguj ponownie.\n\n'
