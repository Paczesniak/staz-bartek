'use strict';

/* ============================================================================
 * Skracacz linków — logika strony.
 *
 * Czysty JavaScript (ES6+), bez frameworków, bez buildu, bez zależności z sieci.
 * Adres API pochodzi WYŁĄCZNIE z pliku config.js (window.APP_CONFIG) — w tym
 * pliku nie ma i nie może być żadnego adresu zapisanego na sztywno.
 *
 * Najważniejsza część tego kodu to nie skracanie linków, tylko sekcja
 * "Warstwa sieci" — rozróżnianie rodzajów awarii. Zobacz komentarz przy
 * funkcji rozroznijAwarieSieci().
 * ========================================================================== */

// ─────────────────────────── Stałe ───────────────────────────

const DOMYSLNY_ADRES_API = 'http://localhost:8000';
const INTERWAL_HEALTH_MS = 15000;
const WZORZEC_KODU = /^[A-Za-z0-9_-]{1,32}$/;
const CZAS_KOMUNIKATU_OK_MS = 6000;

/** Rodzaje awarii, które ten front potrafi od siebie odróżnić. */
const RODZAJ = Object.freeze({
  CORS: 'cors',                   // serwer odpowiedział, przeglądarka zablokowała odpowiedź
  NIEOSIAGALNE: 'nieosiagalne',   // nikt nie odebrał pod tym adresem i portem
  KLIENT: 'klient',               // HTTP 4xx — serwer świadomie odrzucił żądanie
  SERWER: 'serwer',               // HTTP 5xx — serwer się wywrócił
  ODPOWIEDZ: 'odpowiedz',         // odpowiedź przyszła, ale nie jest tym JSON-em, którego oczekujemy
});

/** Stany zdrowia pokazywane na pasku u góry strony. */
const ZDROWIE = Object.freeze({
  SPRAWDZANIE: 'sprawdzanie',
  OK: 'ok',
  BAZA: 'baza',        // API odpowiada, ale zgłasza problem z bazą danych
  AWARIA: 'awaria',    // API nieosiągalne albo odpowiedź zablokowana przez przeglądarkę
});

// ─────────────────────────── Stan ───────────────────────────

/* Stan trzymamy w jednym zamrożonym obiekcie i podmieniamy w całości —
   nigdy nie modyfikujemy go w miejscu. */
let stan = Object.freeze({
  adresApi: DOMYSLNY_ADRES_API,
  zdrowie: ZDROWIE.SPRAWDZANIE,
  rodzajAwarii: null,
  wysylanie: false,
});

function ustawStan(zmiany) {
  stan = Object.freeze({ ...stan, ...zmiany });
}

/** Uchwyty do elementów strony; wypełniane raz przy starcie. */
const el = {};

// ────────────────────── Konfiguracja ──────────────────────

/**
 * Czyta adres API z config.js. Zwraca też ewentualne ostrzeżenie, żeby
 * literówka w konfiguracji nie objawiła się jako tajemniczy błąd sieci.
 */
function odczytajKonfiguracje() {
  const konfiguracja = window.APP_CONFIG;

  if (!konfiguracja || typeof konfiguracja.API_BASE_URL !== 'string') {
    return {
      adres: DOMYSLNY_ADRES_API,
      ostrzezenie: 'Nie znalazłem poprawnego `window.APP_CONFIG.API_BASE_URL` — '
        + 'sprawdź, czy plik `config.js` istnieje i czy jest wczytany przed `app.js`. '
        + `Używam adresu domyślnego \`${DOMYSLNY_ADRES_API}\`.`,
    };
  }

  const adres = konfiguracja.API_BASE_URL.trim().replace(/\/+$/, '');

  // Pusty adres jest poprawny i oznacza "to samo miejsce, co ta strona".
  if (adres === '') return { adres: '', ostrzezenie: null };

  if (!/^https?:\/\//i.test(adres)) {
    return {
      adres,
      ostrzezenie: `Adres API w \`config.js\` (\`${adres}\`) nie zaczyna się od \`http://\` `
        + 'ani `https://`. Przeglądarka potraktuje go jako ścieżkę względną i żądania pójdą '
        + 'w zupełnie inne miejsce, niż myślisz.',
    };
  }

  return { adres, ostrzezenie: null };
}

/** Adres API w formie czytelnej dla człowieka (pusty = ten sam origin co strona). */
function adresApiDoPokazania() {
  return stan.adresApi === '' ? `${window.location.origin} (ten sam co strona)` : stan.adresApi;
}

// ─────────────────────── Warstwa sieci ───────────────────────

class BladApi extends Error {
  constructor(rodzaj, szczegoly = {}) {
    super(szczegoly.detail || rodzaj);
    this.name = 'BladApi';
    this.rodzaj = rodzaj;
    this.status = szczegoly.status ?? null;
    this.detail = szczegoly.detail ?? null;
    this.sciezka = szczegoly.sciezka ?? null;
  }
}

/**
 * Odróżnia błąd CORS od nieosiągalnego serwera.
 *
 * Problem: `fetch` w OBU przypadkach rzuca identyczne `TypeError: Failed to fetch`.
 * Z samego wyjątku nie da się poznać, czy serwer nie odpowiedział, czy odpowiedział,
 * a przeglądarka schowała odpowiedź przed kodem strony.
 *
 * Sztuczka: powtarzamy żądanie w trybie `no-cors`. W tym trybie przeglądarka nie
 * sprawdza nagłówków CORS — zwraca "nieprzezroczystą" odpowiedź, której nie da się
 * odczytać, ale która ROZWIĄZUJE SIĘ POMYŚLNIE, jeżeli serwer w ogóle odpowiedział.
 * Czyli:
 *   próba no-cors przechodzi  → serwer żyje, odpowiedź zablokowała przeglądarka  → CORS
 *   próba no-cors też pada    → pod tym adresem naprawdę nikt nie odpowiada       → nieosiągalne
 *
 * Działa tylko dla prostych żądań (GET bez własnych nagłówków), dlatego zawsze
 * sondujemy `/health`, niezależnie od tego, które żądanie się wywróciło.
 */
async function rozroznijAwarieSieci() {
  try {
    await fetch(`${stan.adresApi}/health`, { method: 'GET', mode: 'no-cors', cache: 'no-store' });
    return RODZAJ.CORS;
  } catch {
    return RODZAJ.NIEOSIAGALNE;
  }
}

/** Bezpiecznie wyciąga pole `detail` z odpowiedzi błędu; null, gdy się nie da. */
async function odczytajDetail(odpowiedz) {
  try {
    const dane = await odpowiedz.json();
    return dane && typeof dane.detail === 'string' ? dane.detail : null;
  } catch {
    return null;
  }
}

/** Zamienia odpowiedź HTTP na dane albo na BladApi z właściwym rodzajem. */
async function przetworzOdpowiedz(odpowiedz, sciezka) {
  if (odpowiedz.status === 204) return null;

  if (!odpowiedz.ok) {
    const rodzaj = odpowiedz.status >= 500 ? RODZAJ.SERWER : RODZAJ.KLIENT;
    throw new BladApi(rodzaj, {
      status: odpowiedz.status,
      detail: await odczytajDetail(odpowiedz),
      sciezka,
    });
  }

  try {
    return await odpowiedz.json();
  } catch {
    throw new BladApi(RODZAJ.ODPOWIEDZ, { status: odpowiedz.status, sciezka });
  }
}

/**
 * Jedyne wejście do API. Każdy błąd wychodzi stąd jako BladApi z rozpoznanym
 * rodzajem — dzięki temu warstwa widoku nigdy nie ogląda surowego `TypeError`.
 */
async function zapytajApi(sciezka, opcje = {}) {
  let odpowiedz;

  try {
    odpowiedz = await fetch(`${stan.adresApi}${sciezka}`, { cache: 'no-store', ...opcje });
  } catch (przyczyna) {
    // Tu ląduje "Failed to fetch" — czyli CORS albo brak serwera. Trzeba rozstrzygnąć.
    const rodzaj = await rozroznijAwarieSieci();
    ustawStan({ zdrowie: ZDROWIE.AWARIA, rodzajAwarii: rodzaj });
    odswiezPasekStanu();
    throw new BladApi(rodzaj, { sciezka });
  }

  return przetworzOdpowiedz(odpowiedz, sciezka);
}

// ─────────────────── Operacje na zasobach ───────────────────

const api = {
  pobierzLinki: () => zapytajApi('/api/links'),

  dodajLink: (url, kod) => zapytajApi('/api/links', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(kod ? { url, code: kod } : { url }),
  }),

  usunLink: (kod) => zapytajApi(`/api/links/${encodeURIComponent(kod)}`, { method: 'DELETE' }),
};

// ──────────────── Komunikaty o błędach ────────────────

/**
 * Zamienia BladApi na komunikat dla człowieka: tytuł, wyjaśnienie i wskazówki
 * diagnostyczne. Wskazówki mają prowadzić do przyczyny, nie podawać gotowca.
 * Fragmenty w `odwrotnych apostrofach` renderują się jako <code>.
 */
function opiszBlad(blad) {
  const budowniczy = BUDOWNICZOWIE_KOMUNIKATOW[blad.rodzaj] || komunikatNieznany;
  return budowniczy(blad, adresApiDoPokazania());
}

function komunikatCors(blad, adres) {
  return {
    typ: 'blad',
    tytul: 'Przeglądarka zablokowała odpowiedź serwera (CORS)',
    tresc: `Żądanie do \`${adres}\` wyszło z przeglądarki i serwer najprawdopodobniej `
      + 'na nie odpowiedział — sprawdziłem to dodatkową próbą, która nie podlega regułom CORS, '
      + 'i ta próba przeszła. Odpowiedzi nie widzi jednak kod tej strony: przeglądarka '
      + 'przechwyciła ją i odrzuciła, bo serwer nie odesłał nagłówka '
      + `\`Access-Control-Allow-Origin\` pasującego do origin tej strony (\`${window.location.origin}\`). `
      + 'To reguła bezpieczeństwa samej przeglądarki, a nie awaria sieci ani błąd serwera — '
      + 'dokładnie to samo żądanie wykonane `curl`-em zadziała, bo `curl` żadnego CORS-a nie sprawdza.',
    wskazowki: [
      'Otwórz konsolę (`F12`) — jest tam oryginalny komunikat przeglądarki z nazwą nagłówka, którego zabrakło.',
      'Zakładka `Network`: znajdź to żądanie i sprawdź, czy w ogóle wyszło i z jakim statusem wróciło. '
        + 'Status `200` przy jednoczesnym błędzie na stronie to podpis CORS-a.',
      `Porównaj origin tej strony (\`${window.location.origin}\`) z adresem API (\`${adres}\`). `
        + 'Wypisz, czym dokładnie się różnią: schemat, host, port.',
      `Sprawdź to samo poza przeglądarką: \`curl -i ${adres}/health\`. Jeśli tam działa, `
        + 'masz potwierdzenie, że ani sieć, ani API nie są tu winne.',
      'Pytanie do rozstrzygnięcia: skoro serwer odpowiedział, to kto i na jakiej podstawie zdecydował, '
        + 'że ta odpowiedź nie może trafić do kodu strony?',
    ],
  };
}

function komunikatNieosiagalne(blad, adres) {
  return {
    typ: 'blad',
    tytul: 'API nie odpowiada',
    tresc: `Przeglądarka nie dostała z \`${adres}\` żadnej odpowiedzi — nawet błędnej. `
      + 'Nic nie zostało tu zablokowane: pod tym adresem i portem po prostu nikt nie odebrał. '
      + 'Typowe przyczyny: proces API nie został uruchomiony, wywrócił się zaraz po starcie, '
      + 'nasłuchuje na innym porcie, albo nasłuchuje wyłącznie na `127.0.0.1` i przez to jest '
      + 'niewidoczny z innej maszyny.',
    wskazowki: [
      'Sprawdź, czy proces API w ogóle chodzi na maszynie, na której miał wstać.',
      'Zobacz, kto nasłuchuje na porcie: `ss -tlnp`. Jeśli tego portu nie ma na liście, aplikacja nie wstała.',
      `Spróbuj z maszyny, na której stoi API: \`curl -i ${adres}/health\`.`,
      'Jeśli `curl` z tamtej maszyny działa, a stąd nie — przyczyna leży w adresie, porcie albo w tym, '
        + 'na jakim interfejsie aplikacja nasłuchuje. Nie w kodzie tej strony.',
      'Sprawdź też literówkę w `config.js`: zły port wygląda dokładnie tak samo jak wyłączony serwer.',
    ],
  };
}

function komunikatSerwer(blad) {
  return {
    typ: 'blad',
    tytul: `Błąd po stronie serwera (HTTP ${blad.status})`,
    tresc: (blad.detail ? `Powód podany przez serwer: ${blad.detail} ` : '')
      + 'Żądanie doszło do API i zostało przyjęte, ale obsługa wywróciła się w środku. '
      + 'To nie jest wina tej strony ani danych, które wpisałeś w formularz — front wysłał żądanie '
      + `i dostał odpowiedź ze statusem \`${blad.status}\`.`,
    wskazowki: [
      'Zajrzyj w logi procesu API — przy błędzie `5xx` jest tam ślad wyjątku z nazwą pliku i numerem linii.',
      'Spójrz na pasek stanu u góry: jeśli `/health` też zgłasza problem z bazą, przyczyny szukaj '
        + 'najpierw w bazie, a dopiero potem w kodzie API.',
      'Powtórz żądanie `curl`-em z flagą `-i` — zobaczysz surowy status i nagłówki bez pośrednictwa strony.',
    ],
  };
}

function komunikatKlient(blad) {
  return {
    typ: 'ostrzezenie',
    tytul: `Serwer odrzucił żądanie (HTTP ${blad.status})`,
    tresc: blad.detail
      ? `Powód podany przez serwer: ${blad.detail}`
      : 'Serwer nie podał powodu w polu `detail`. Kod `4xx` oznacza, że to żądanie było '
        + 'niepoprawne z punktu widzenia API — poprawka jest po stronie danych, nie serwera.',
    wskazowki: wskazowkiDlaStatusu(blad.status),
  };
}

function komunikatOdpowiedz(blad, adres) {
  return {
    typ: 'blad',
    tytul: 'Nieczytelna odpowiedź serwera',
    tresc: `Odpowiedź przyszła ze statusem \`${blad.status}\`, ale jej treść nie jest poprawnym `
      + 'JSON-em, którego oczekuje ten front. Zwykle znaczy to, że pod tym adresem odpowiada coś '
      + 'innego niż API — na przykład serwer statyczny albo proxy, które zwróciło własną stronę błędu.',
    wskazowki: [
      'Zakładka `Network`, podgląd `Response` — zobacz, co faktycznie przyszło zamiast JSON-a.',
      `Sprawdź w terminalu: \`curl -i ${adres}${blad.sciezka || ''}\` — zwróć uwagę na nagłówek \`Content-Type\`.`,
    ],
  };
}

function komunikatNieznany() {
  return {
    typ: 'blad',
    tytul: 'Nieoczekiwany błąd',
    tresc: 'Coś poszło nie tak w kodzie tej strony. Szczegóły są w konsoli przeglądarki (`F12`).',
    wskazowki: [],
  };
}

const BUDOWNICZOWIE_KOMUNIKATOW = {
  [RODZAJ.CORS]: komunikatCors,
  [RODZAJ.NIEOSIAGALNE]: komunikatNieosiagalne,
  [RODZAJ.SERWER]: komunikatSerwer,
  [RODZAJ.KLIENT]: komunikatKlient,
  [RODZAJ.ODPOWIEDZ]: komunikatOdpowiedz,
};

function wskazowkiDlaStatusu(status) {
  if (status === 400) {
    return [
      'Sprawdź, czy adres ma pełny schemat (`http://` albo `https://`) — API waliduje go po swojemu '
        + 'i ostrzej niż przeglądarka.',
    ];
  }
  if (status === 404) {
    return [
      'Tego kodu nie ma w bazie. Mógł zostać usunięty w międzyczasie — odśwież listę i sprawdź ponownie.',
    ];
  }
  if (status === 409) {
    return [
      'Taki kod już istnieje. Podaj inny albo zostaw pole puste, żeby API wygenerowało kod samo.',
    ];
  }
  return [];
}

// ──────────────────── Rysowanie komunikatów ────────────────────

/** Wstawia tekst, zamieniając fragmenty w `odwrotnych apostrofach` na <code>. */
function wstawTekstZKodem(element, tekst) {
  String(tekst).split('`').forEach((czesc, indeks) => {
    if (czesc === '') return;
    if (indeks % 2 === 1) {
      const kod = document.createElement('code');
      kod.textContent = czesc;
      element.appendChild(kod);
    } else {
      element.appendChild(document.createTextNode(czesc));
    }
  });
}

let uchwytUkrywaniaKomunikatu = null;

function pokazKomunikat({ typ, tytul, tresc, wskazowki = [], zrodlo = 'operacja' }) {
  window.clearTimeout(uchwytUkrywaniaKomunikatu);

  el.komunikat.className = `komunikat komunikat--${typ}`;
  // Skąd wziął się ten komunikat — patrz opiszZmianeZdrowia(): powrót API do zdrowia
  // ma prawo sprzątnąć tylko własny komunikat, a nie błąd innej operacji.
  el.komunikat.dataset.zrodlo = zrodlo;
  el.komunikat.replaceChildren();

  const naglowek = document.createElement('p');
  naglowek.className = 'komunikat__tytul';
  naglowek.textContent = tytul;
  el.komunikat.appendChild(naglowek);

  if (tresc) {
    const akapit = document.createElement('p');
    akapit.className = 'komunikat__tresc';
    wstawTekstZKodem(akapit, tresc);
    el.komunikat.appendChild(akapit);
  }

  if (wskazowki.length > 0) {
    const lista = document.createElement('ul');
    lista.className = 'komunikat__wskazowki';
    wskazowki.forEach((wskazowka) => {
      const pozycja = document.createElement('li');
      wstawTekstZKodem(pozycja, wskazowka);
      lista.appendChild(pozycja);
    });
    el.komunikat.appendChild(lista);
  }

  el.komunikat.hidden = false;

  // Potwierdzenia znikają same; błędy zostają, dopóki nie zastąpi ich nowy komunikat.
  if (typ === 'ok') {
    uchwytUkrywaniaKomunikatu = window.setTimeout(ukryjKomunikat, CZAS_KOMUNIKATU_OK_MS);
  }
}

function ukryjKomunikat() {
  el.komunikat.hidden = true;
  el.komunikat.replaceChildren();
}

function pokazBlad(blad) {
  if (blad instanceof BladApi) {
    pokazKomunikat(opiszBlad(blad));
    return;
  }
  console.error('Nieoczekiwany błąd w kodzie strony:', blad);
  pokazKomunikat(opiszBlad({ rodzaj: 'nieznany' }));
}

// ─────────────────── Pasek stanu API (/health) ───────────────────

const OPISY_ZDROWIA = {
  [ZDROWIE.SPRAWDZANIE]: { klasa: 'sprawdzanie', etykieta: 'Sprawdzam stan API…', opis: '' },
  [ZDROWIE.OK]: { klasa: 'ok', etykieta: 'API działa', opis: '' },
  [ZDROWIE.BAZA]: {
    klasa: 'baza',
    etykieta: 'API działa, baza danych nie',
    opis: 'Proces API odpowiada, ale zgłasza brak połączenia z bazą — operacje na linkach mogą się nie udać.',
  },
  [ZDROWIE.AWARIA]: { klasa: 'awaria', etykieta: 'API nieosiągalne', opis: '' },
};

function odswiezPasekStanu(dodatki = {}) {
  const opis = OPISY_ZDROWIA[stan.zdrowie];
  const cors = stan.zdrowie === ZDROWIE.AWARIA && stan.rodzajAwarii === RODZAJ.CORS;

  el.pasekStanu.className = `pasek-stanu pasek-stanu--${opis.klasa}`;
  el.stanEtykieta.textContent = cors
    ? 'Odpowiedź API zablokowana przez przeglądarkę (CORS)'
    : opis.etykieta;

  if (cors) {
    el.stanOpis.textContent = 'Serwer odpowiada, ale przeglądarka nie wpuszcza odpowiedzi do kodu strony.';
  } else if (stan.zdrowie === ZDROWIE.AWARIA) {
    el.stanOpis.textContent = `Pod adresem ${adresApiDoPokazania()} nikt nie odpowiada.`;
  } else {
    el.stanOpis.textContent = dodatki.opis ?? opis.opis;
  }

  if (stan.zdrowie !== ZDROWIE.SPRAWDZANIE) {
    el.stanCzas.textContent = `sprawdzono ${new Date().toLocaleTimeString('pl-PL')}`;
  }
}

/** Odpytuje /health i tłumaczy wynik na jeden z trzech stanów paska. */
async function sprawdzZdrowie({ pokazZmiane = true } = {}) {
  const poprzednie = stan.zdrowie;
  el.stanOdswiez.disabled = true;

  try {
    const dane = await zapytajApi('/health');
    const bazaDziala = !dane || dane.database === 'ok';
    ustawStan({ zdrowie: bazaDziala ? ZDROWIE.OK : ZDROWIE.BAZA, rodzajAwarii: null });
    odswiezPasekStanu({ opis: opisWersji(dane) });
  } catch (blad) {
    obsluzBladZdrowia(blad);
  } finally {
    el.stanOdswiez.disabled = false;
  }

  if (pokazZmiane && stan.zdrowie !== poprzednie) opiszZmianeZdrowia();
}

function opisWersji(dane) {
  if (!dane) return '';
  const czesci = [];
  if (typeof dane.version === 'string') czesci.push(`wersja ${dane.version}`);
  if (typeof dane.database === 'string') czesci.push(`baza: ${dane.database}`);
  return czesci.join(' · ');
}

function obsluzBladZdrowia(blad) {
  // 503 na /health to nie awaria połączenia, tylko świadoma odpowiedź API:
  // proces żyje i sam zgłasza, że baza mu nie odpowiada.
  if (blad instanceof BladApi && blad.status === 503) {
    ustawStan({ zdrowie: ZDROWIE.BAZA, rodzajAwarii: null });
    odswiezPasekStanu({ opis: blad.detail || OPISY_ZDROWIA[ZDROWIE.BAZA].opis });
    return;
  }

  if (blad instanceof BladApi && (blad.rodzaj === RODZAJ.CORS || blad.rodzaj === RODZAJ.NIEOSIAGALNE)) {
    ustawStan({ zdrowie: ZDROWIE.AWARIA, rodzajAwarii: blad.rodzaj });
    odswiezPasekStanu();
    return;
  }

  ustawStan({ zdrowie: ZDROWIE.AWARIA, rodzajAwarii: null });
  odswiezPasekStanu();
}

/**
 * Pełny opis awarii pokazujemy tylko przy ZMIANIE stanu, a nie co 15 sekund —
 * inaczej ten sam komunikat mrugałby w kółko i przestałby cokolwiek znaczyć.
 */
function opiszZmianeZdrowia() {
  if (stan.zdrowie === ZDROWIE.OK) {
    // Sprzątamy wyłącznie własny komunikat. Błąd zapisu albo nieudanego pobrania listy
    // musi zostać na ekranie, nawet jeśli /health właśnie odpowiedziało poprawnie.
    if (el.komunikat.dataset.zrodlo === 'zdrowie') ukryjKomunikat();
    return;
  }

  if (stan.zdrowie === ZDROWIE.BAZA) {
    pokazKomunikat({
      zrodlo: 'zdrowie',
      typ: 'ostrzezenie',
      tytul: 'API odpowiada, ale baza danych nie',
      tresc: 'Endpoint `/health` odpowiedział, więc proces API żyje i przyjmuje żądania. '
        + 'Sam zgłasza jednak, że nie ma połączenia z bazą (`database` inne niż `ok`, zwykle razem ze '
        + 'statusem `503`). To ważne rozróżnienie: warstwa aplikacji jest sprawna, warstwa danych nie. '
        + 'Lista linków i dodawanie mogą się nie udać, mimo że serwer z zewnątrz wygląda zdrowo.',
      wskazowki: [
        'Sprawdź, czy proces bazy danych działa i czy przyjmuje połączenia.',
        'Zajrzyj w logi API z momentu startu — nieudane połączenie z bazą zwykle zostawia tam wyraźny ślad.',
        'Zwróć uwagę, że tu nie ma sensu debugować frontu: `/health` odpowiedział, więc droga '
          + 'przeglądarka → API jest w porządku.',
      ],
    });
    return;
  }

  if (stan.zdrowie === ZDROWIE.AWARIA && stan.rodzajAwarii) {
    pokazKomunikat({
      ...opiszBlad(new BladApi(stan.rodzajAwarii, { sciezka: '/health' })),
      zrodlo: 'zdrowie',
    });
  }
}

// ─────────────────────── Lista linków ───────────────────────

function sformatujDate(wartosc) {
  if (!wartosc) return 'brak daty';
  const data = new Date(wartosc);
  if (Number.isNaN(data.getTime())) return String(wartosc);
  return data.toLocaleString('pl-PL', { dateStyle: 'short', timeStyle: 'short' });
}

function adresSkrotu(kod) {
  return `${stan.adresApi}/r/${encodeURIComponent(kod)}`;
}

function zbudujWierszLinku(link) {
  const pozycja = document.createElement('li');
  pozycja.className = 'link';

  const glowna = document.createElement('div');
  glowna.className = 'link__glowna';

  const skrot = document.createElement('a');
  skrot.className = 'link__skrot';
  skrot.href = adresSkrotu(link.code);
  skrot.textContent = adresSkrotu(link.code);
  skrot.target = '_blank';
  skrot.rel = 'noopener noreferrer';

  const cel = document.createElement('div');
  cel.className = 'link__cel';
  cel.textContent = link.url || '(brak adresu docelowego)';
  cel.title = link.url || '';

  const meta = document.createElement('div');
  meta.className = 'link__meta';
  meta.appendChild(zbudujMeta('kliknięcia', String(link.clicks ?? 0)));
  meta.appendChild(zbudujMeta('utworzono', sformatujDate(link.created_at)));

  glowna.append(skrot, cel, meta);
  pozycja.append(glowna, zbudujAkcje(link));
  return pozycja;
}

function zbudujMeta(etykieta, wartosc) {
  const span = document.createElement('span');
  span.appendChild(document.createTextNode(`${etykieta}: `));
  const mocny = document.createElement('strong');
  mocny.textContent = wartosc;
  span.appendChild(mocny);
  return span;
}

function zbudujAkcje(link) {
  const akcje = document.createElement('div');
  akcje.className = 'link__akcje';

  const kopiuj = document.createElement('button');
  kopiuj.type = 'button';
  kopiuj.className = 'przycisk przycisk--cichy przycisk--maly';
  kopiuj.textContent = 'Kopiuj';
  kopiuj.addEventListener('click', () => obsluzKopiowanie(link.code, kopiuj));

  const usun = document.createElement('button');
  usun.type = 'button';
  usun.className = 'przycisk przycisk--grozny przycisk--maly';
  usun.textContent = 'Usuń';
  usun.addEventListener('click', () => obsluzUsuwanie(link.code));

  akcje.append(kopiuj, usun);
  return akcje;
}

function pokazStanListy(tekst) {
  el.stanListy.textContent = tekst;
  el.stanListy.hidden = false;
  el.listaLinkow.hidden = true;
  el.licznikLinkow.hidden = true;
}

function narysujListe(linki) {
  if (!Array.isArray(linki) || linki.length === 0) {
    pokazStanListy('Nie ma jeszcze żadnych linków. Dodaj pierwszy formularzem powyżej.');
    return;
  }

  // Kopia przed sortowaniem — nie zmieniamy tablicy, którą dostaliśmy z API.
  const posortowane = [...linki].sort(
    (a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0),
  );

  el.listaLinkow.replaceChildren(...posortowane.map(zbudujWierszLinku));
  el.listaLinkow.hidden = false;
  el.stanListy.hidden = true;
  el.licznikLinkow.textContent = `(${posortowane.length})`;
  el.licznikLinkow.hidden = false;
}

async function wczytajListe({ cicho = false } = {}) {
  el.przyciskOdswiez.disabled = true;
  if (!cicho) pokazStanListy('Wczytuję listę…');

  try {
    narysujListe(await api.pobierzLinki());
  } catch (blad) {
    pokazStanListy('Nie udało się pobrać listy — szczegóły w komunikacie powyżej.');
    pokazBlad(blad);
  } finally {
    el.przyciskOdswiez.disabled = false;
  }
}

// ───────────────────── Walidacja formularza ─────────────────────

function ustawBladPola(wejscie, elementBledu, tekst) {
  elementBledu.textContent = tekst || '';
  elementBledu.hidden = !tekst;
  wejscie.setAttribute('aria-invalid', tekst ? 'true' : 'false');
}

/** Sprawdza dane PRZED wysłaniem — żeby nie wysyłać żądania, które i tak wróci z 400. */
function sprawdzFormularz(url, kod) {
  ustawBladPola(el.poleUrl, el.bladUrl, '');
  ustawBladPola(el.poleKod, el.bladKod, '');
  let poprawny = true;

  if (url === '') {
    ustawBladPola(el.poleUrl, el.bladUrl, 'Podaj adres do skrócenia.');
    poprawny = false;
  } else {
    const rozebrany = rozbierzUrl(url);
    if (!rozebrany) {
      ustawBladPola(el.poleUrl, el.bladUrl,
        'To nie wygląda na poprawny adres. Pamiętaj o pełnym początku, np. https://przyklad.pl');
      poprawny = false;
    } else if (rozebrany.protocol !== 'http:' && rozebrany.protocol !== 'https:') {
      ustawBladPola(el.poleUrl, el.bladUrl,
        `Obsługiwane są tylko adresy http:// i https:// (podałeś ${rozebrany.protocol}//).`);
      poprawny = false;
    }
  }

  if (kod !== '' && !WZORZEC_KODU.test(kod)) {
    ustawBladPola(el.poleKod, el.bladKod,
      'Kod może zawierać wyłącznie litery bez ogonków, cyfry, myślnik i podkreślenie (do 32 znaków).');
    poprawny = false;
  }

  return poprawny;
}

function rozbierzUrl(wartosc) {
  try {
    return new URL(wartosc);
  } catch {
    return null;
  }
}

// ─────────────────────── Obsługa akcji ───────────────────────

async function obsluzWyslanie(zdarzenie) {
  zdarzenie.preventDefault();
  if (stan.wysylanie) return;

  const url = el.poleUrl.value.trim();
  const kod = el.poleKod.value.trim();
  if (!sprawdzFormularz(url, kod)) return;

  ustawStan({ wysylanie: true });
  el.przyciskDodaj.disabled = true;
  el.przyciskDodaj.textContent = 'Wysyłam…';

  try {
    const utworzony = await api.dodajLink(url, kod);
    el.formularz.reset();
    pokazKomunikat({
      typ: 'ok',
      tytul: 'Link został utworzony',
      tresc: `Skrócony adres: \`${adresSkrotu(utworzony.code)}\` → ${utworzony.url}`,
      wskazowki: [],
    });
    await wczytajListe({ cicho: true });
  } catch (blad) {
    pokazBlad(blad);
  } finally {
    ustawStan({ wysylanie: false });
    el.przyciskDodaj.disabled = false;
    el.przyciskDodaj.textContent = 'Skróć link';
  }
}

async function obsluzUsuwanie(kod) {
  const potwierdzone = window.confirm(
    `Usunąć link o kodzie „${kod}”?\n\n`
    + 'Skrócony adres przestanie działać, a licznik kliknięć zniknie razem z nim. '
    + 'Tej operacji nie da się cofnąć.',
  );
  if (!potwierdzone) return;

  try {
    await api.usunLink(kod);
    pokazKomunikat({ typ: 'ok', tytul: 'Link usunięty', tresc: `Kod \`${kod}\` jest znowu wolny.` });
    await wczytajListe({ cicho: true });
  } catch (blad) {
    pokazBlad(blad);
  }
}

async function obsluzKopiowanie(kod, przycisk) {
  const adres = adresSkrotu(kod);

  try {
    await skopiujDoSchowka(adres);
    const pierwotny = przycisk.textContent;
    przycisk.textContent = 'Skopiowano';
    window.setTimeout(() => { przycisk.textContent = pierwotny; }, 1500);
  } catch (blad) {
    console.warn('Kopiowanie do schowka nie powiodło się:', blad);
    pokazKomunikat({
      typ: 'ostrzezenie',
      tytul: 'Nie udało się skopiować do schowka',
      tresc: `Przeglądarka nie dała dostępu do schowka. Skopiuj adres ręcznie: \`${adres}\``,
      wskazowki: [
        'Dostęp do schowka przeglądarki mają tylko strony w tak zwanym bezpiecznym kontekście: '
          + '`https://` albo `http://localhost`. Strona otwarta po adresie IP go nie dostanie.',
      ],
    });
  }
}

async function skopiujDoSchowka(tekst) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(tekst);
    return;
  }

  // Zapasowa droga dla stron spoza bezpiecznego kontekstu (np. otwartych po adresie IP).
  const pole = document.createElement('textarea');
  pole.value = tekst;
  pole.setAttribute('readonly', '');
  pole.style.position = 'fixed';
  pole.style.opacity = '0';
  document.body.appendChild(pole);
  pole.select();

  try {
    if (!document.execCommand('copy')) throw new Error('execCommand("copy") zwrócił false');
  } finally {
    pole.remove();
  }
}

// ─────────────────────────── Start ───────────────────────────

function podepnijElementy() {
  const identyfikatory = {
    pasekStanu: 'pasek-stanu',
    stanEtykieta: 'stan-etykieta',
    stanOpis: 'stan-opis',
    stanCzas: 'stan-czas',
    stanOdswiez: 'stan-odswiez',
    komunikat: 'komunikat',
    formularz: 'formularz',
    poleUrl: 'pole-url',
    poleKod: 'pole-kod',
    bladUrl: 'blad-url',
    bladKod: 'blad-kod',
    przyciskDodaj: 'przycisk-dodaj',
    przyciskOdswiez: 'przycisk-odswiez',
    listaLinkow: 'lista-linkow',
    stanListy: 'stan-listy',
    licznikLinkow: 'licznik-linkow',
    naglowekAdresApi: 'naglowek-adres-api',
    stopkaAdresApi: 'stopka-adres-api',
  };

  Object.entries(identyfikatory).forEach(([nazwa, id]) => {
    el[nazwa] = document.getElementById(id);
  });
}

function start() {
  podepnijElementy();

  const konfiguracja = odczytajKonfiguracje();
  ustawStan({ adresApi: konfiguracja.adres });

  el.naglowekAdresApi.textContent = adresApiDoPokazania();
  el.stopkaAdresApi.textContent = adresApiDoPokazania();

  el.formularz.addEventListener('submit', obsluzWyslanie);
  el.przyciskOdswiez.addEventListener('click', () => wczytajListe());
  el.stanOdswiez.addEventListener('click', () => sprawdzZdrowie());

  if (konfiguracja.ostrzezenie) {
    pokazKomunikat({
      typ: 'ostrzezenie',
      tytul: 'Problem z konfiguracją adresu API',
      tresc: konfiguracja.ostrzezenie,
      wskazowki: ['Adres API ustawia się w pliku `config.js` — to jedyne miejsce, gdzie on występuje.'],
    });
  }

  sprawdzZdrowie();
  wczytajListe();
  window.setInterval(() => sprawdzZdrowie(), INTERWAL_HEALTH_MS);
}

document.addEventListener('DOMContentLoaded', start);
