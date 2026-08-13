"""Metryki w formacie tekstowym Prometheusa.

Napisane ręcznie, bez biblioteki `prometheus_client` — format jest na tyle
prosty, że warto go raz zobaczyć od środka. To zwykły tekst: dla każdej
metryki linia `# HELP`, linia `# TYPE` i jedna linia na każdą kombinację
etykiet.

Opisy `# HELP` są po angielsku — to konwencja Prometheusa i wszystkie
narzędzia (Grafana, alerty) zakładają ten język.

Liczniki żyją w pamięci procesu i zerują się przy restarcie. Tak ma być:
Prometheus zbiera dane osobno z każdej instancji i sam wykrywa restart
(licznik nagle maleje). Dlatego aplikacja może działać w dwóch kopiach,
a stan trwały trzyma wyłącznie baza.
"""

from __future__ import annotations

import threading
from collections.abc import Iterable

CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"

# Granice kubełków histogramu w sekundach. Ostatni kubełek (+Inf) dokładany
# automatycznie. Wartości dobrane pod API, które powinno odpowiadać w milisekundach.
DURATION_BUCKETS: tuple[float, ...] = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    10.0,
)


def escape_label_value(value: str) -> str:
    """Przygotowuje wartość etykiety do formatu tekstowego Prometheusa.

    Format wymaga zabezpieczenia backslasha, cudzysłowu i znaku nowej linii —
    inaczej wartość z takim znakiem rozwaliłaby parsowanie po stronie Prometheusa.
    """
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def format_labels(labels: dict[str, str]) -> str:
    """Buduje fragment `{klucz="wartość",...}`; dla pustego słownika zwraca ''."""
    if not labels:
        return ""
    pairs = ",".join(f'{name}="{escape_label_value(value)}"' for name, value in labels.items())
    return "{" + pairs + "}"


class MetricsRegistry:
    """Zbiera liczniki aplikacji i renderuje je w formacie Prometheusa.

    Instancja jest tworzona raz na aplikację i trzymana w `app.state.metrics`.
    Wszystkie modyfikacje idą pod blokadą, bo FastAPI obsługuje żądania
    w wielu wątkach i bez tego liczniki potrafiłyby gubić zliczenia.
    """

    def __init__(self, app_name: str) -> None:
        # Etykieta wspólna dla wszystkich metryk. Pozwala odróżnić od siebie
        # dwie instancje tej samej aplikacji, gdy stoją za load balancerem.
        self._base_labels: dict[str, str] = {"app": app_name}
        self._lock = threading.Lock()
        self._redirects: dict[str, int] = {}
        self._requests: dict[tuple[str, str, str], int] = {}
        self._duration_counts: list[int] = [0] * (len(DURATION_BUCKETS) + 1)
        self._duration_sum: float = 0.0

    def record_redirect(self, code: str) -> None:
        """Zlicza jedno wykonane przekierowanie dla danego kodu."""
        with self._lock:
            self._redirects[code] = self._redirects.get(code, 0) + 1

    def record_request(self, method: str, path: str, status: int, duration: float) -> None:
        """Zlicza jedno żądanie HTTP i zapisuje czas jego obsługi.

        `path` to WZORZEC trasy (`/api/links/{code}`), a nie konkretny adres.
        Gdyby trafiał tu adres z prawdziwym kodem, każdy nowy link tworzyłby
        osobną serię czasową i Prometheus po tygodniu miałby ich miliony.
        """
        key = (method, path, str(status))
        with self._lock:
            self._requests[key] = self._requests.get(key, 0) + 1
            self._duration_sum += duration
            self._duration_counts[self._bucket_index(duration)] += 1

    @staticmethod
    def _bucket_index(duration: float) -> int:
        """Zwraca numer kubełka histogramu dla podanego czasu trwania."""
        for index, upper_bound in enumerate(DURATION_BUCKETS):
            if duration <= upper_bound:
                return index
        return len(DURATION_BUCKETS)

    def _snapshot(self) -> tuple[dict[str, int], dict[tuple[str, str, str], int], list[int], float]:
        """Zwraca spójną kopię liczników — render nie blokuje obsługi żądań."""
        with self._lock:
            return (
                dict(self._redirects),
                dict(self._requests),
                list(self._duration_counts),
                self._duration_sum,
            )

    def render(self, links_total: int | None, database_up: bool) -> str:
        """Składa pełną odpowiedź endpointu /metrics.

        `links_total` przychodzi z bazy (None, gdy baza nie odpowiada —
        wtedy metryki po prostu nie ma, bo zgadywanie zera byłoby kłamstwem).
        """
        redirects, requests, bucket_counts, duration_sum = self._snapshot()

        lines: list[str] = []
        lines.extend(self._render_up(database_up))
        lines.extend(self._render_links_total(links_total))
        lines.extend(self._render_redirects(redirects))
        lines.extend(self._render_requests(requests))
        lines.extend(self._render_duration(bucket_counts, duration_sum))
        return "\n".join(lines) + "\n"

    def _sample(self, name: str, value: float, extra_labels: dict[str, str] | None = None) -> str:
        """Buduje pojedynczą linię próbki wraz z etykietami wspólnymi."""
        labels = {**self._base_labels, **(extra_labels or {})}
        rendered = value if isinstance(value, int) else f"{value:.6f}"
        return f"{name}{format_labels(labels)} {rendered}"

    def _render_up(self, database_up: bool) -> Iterable[str]:
        return (
            "# HELP linkbox_up Whether the application can reach its database (1 = yes, 0 = no).",
            "# TYPE linkbox_up gauge",
            self._sample("linkbox_up", 1 if database_up else 0),
        )

    def _render_links_total(self, links_total: int | None) -> Iterable[str]:
        header = (
            "# HELP linkbox_links_total Number of links currently stored in the database.",
            "# TYPE linkbox_links_total gauge",
        )
        if links_total is None:
            return header
        return (*header, self._sample("linkbox_links_total", links_total))

    def _render_redirects(self, redirects: dict[str, int]) -> Iterable[str]:
        lines = [
            "# HELP linkbox_redirects_total Total number of redirects served, by link code.",
            "# TYPE linkbox_redirects_total counter",
        ]
        for code in sorted(redirects):
            lines.append(self._sample("linkbox_redirects_total", redirects[code], {"code": code}))
        return lines

    def _render_requests(self, requests: dict[tuple[str, str, str], int]) -> Iterable[str]:
        lines = [
            "# HELP linkbox_http_requests_total Total number of HTTP requests handled.",
            "# TYPE linkbox_http_requests_total counter",
        ]
        for method, path, status in sorted(requests):
            labels = {"method": method, "path": path, "status": status}
            lines.append(
                self._sample(
                    "linkbox_http_requests_total", requests[(method, path, status)], labels
                )
            )
        return lines

    def _render_duration(self, bucket_counts: list[int], duration_sum: float) -> Iterable[str]:
        """Renderuje histogram: kubełki narastająco, potem suma i liczba próbek.

        W histogramie Prometheusa kubełki są KUMULATYWNE: `le="0.1"` oznacza
        „ile żądań trwało nie dłużej niż 0,1 s”, więc zawiera też wszystkie
        szybsze. Ostatni kubełek `le="+Inf"` musi równać się `_count`.
        """
        lines = [
            "# HELP linkbox_request_duration_seconds Duration of HTTP requests in seconds.",
            "# TYPE linkbox_request_duration_seconds histogram",
        ]
        cumulative = 0
        for index, upper_bound in enumerate(DURATION_BUCKETS):
            cumulative += bucket_counts[index]
            lines.append(
                self._sample(
                    "linkbox_request_duration_seconds_bucket",
                    cumulative,
                    {"le": _format_bound(upper_bound)},
                )
            )
        cumulative += bucket_counts[-1]
        lines.append(
            self._sample("linkbox_request_duration_seconds_bucket", cumulative, {"le": "+Inf"})
        )
        lines.append(self._sample("linkbox_request_duration_seconds_sum", duration_sum))
        lines.append(self._sample("linkbox_request_duration_seconds_count", cumulative))
        return lines


def _format_bound(value: float) -> str:
    """Zapisuje granicę kubełka bez zbędnych zer (0.005 zamiast 0.005000)."""
    return f"{value:g}"
