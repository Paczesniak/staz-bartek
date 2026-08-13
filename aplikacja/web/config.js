/*
 * Konfiguracja adresu API — JEDYNE miejsce w całym froncie, gdzie ten adres występuje.
 *
 * Plik ładuje się PRZED app.js i ustawia globalny obiekt window.APP_CONFIG.
 * Kod aplikacji nigdy nie zawiera adresu API na sztywno — czyta go stąd.
 *
 * Żeby przełączyć front na inne API, podmieniasz tylko ten jeden plik.
 * Przykłady wartości:
 *   "http://localhost:8000"        — API uruchomione natywnie na tej samej maszynie
 *   "http://192.168.56.10:8000"    — API na maszynie wirtualnej, front otwarty z hosta
 *   ""                             — API pod tym samym adresem i portem co front
 *                                    (adresy względne, przydatne za reverse proxy)
 *
 * Adres podajemy BEZ ukośnika na końcu i BEZ ścieżki — sam schemat, host i port.
 */
window.APP_CONFIG = {
  API_BASE_URL: "http://localhost:8000",
};
