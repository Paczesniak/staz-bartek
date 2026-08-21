#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$ROOT_DIR/aplikacja/api"

cd "$API_DIR"

errors=0

echo "Test pytest: "
if python -m pytest; then
	echo "Ok: pytest"
else
	echo "Zle: pytest"
	((errors+=1))
fi

echo
echo "Test ruff: "
if python -m ruff check .; then
    echo "OK: ruff"
else
    echo "Zle: ruff"
    ((errors+=1))
fi

echo
echo "Test black: "
if python -m black --check .; then
    echo "OK: black"
else
    echo "Zle: black"
    ((errors+=1))
fi

echo

if (( errors > 0 )); then
	echo "Nieudane sprawdzenie: $errors"
	exit 1 
fi

echo "Wszystkie sprawdzenia poszły"
exit 0
