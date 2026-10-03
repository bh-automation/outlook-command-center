"""Lokaler End-to-End-Test des Aufgabenbereichs mit Office-Attrappe (Playwright/Chromium).
Aufruf: python3 tests/e2e/run_e2e.py [--shots DIR]"""
import http.server, json, socketserver, sys, threading, time
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
MOCK = (Path(__file__).parent / "office-mock.js").read_text(encoding="utf-8")
OFFICE = "https://appsforoffice.microsoft.com/lib/1/hosted/office.js"
shots = Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
results = []

def check(name, ok, info=""):
    results.append((name, bool(ok), info))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

srv = socketserver.TCPServer(("127.0.0.1", 0), partial(Quiet, directory=str(SITE)))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{port}/taskpane.html"

def open_page(browser, mock=None, width=360, height=720, reduced=False):
    ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=2,
                              reduced_motion="reduce" if reduced else "no-preference")
    page = ctx.new_page()
    requests = []
    page.on("request", lambda r: requests.append(r.url))
    pre = f"window.__PW_MOCK__ = {json.dumps(mock or {})};"
    page.route(OFFICE, lambda route: route.fulfill(status=200, content_type="application/javascript", body=pre + MOCK))
    page.goto(URL)
    wait_js(page, "document.getElementById('ctx-from').textContent !== '–'")
    page.wait_for_timeout(60)
    return ctx, page, requests

def wait_js(page, expr, timeout=5.0):
    """Wartet per CDP-Auswertung (unabhängig von der CSP der Seite)."""
    end = time.time() + timeout
    while time.time() < end:
        if page.evaluate(expr):
            return True
        time.sleep(0.03)
    raise TimeoutError(expr)

def cats(page):
    return page.eval_on_selector_all("#ctx-categories li", "els => els.map(e => e.textContent)")

def pressed(page):
    return page.eval_on_selector_all(".act[aria-pressed=true]", "els => els.map(e => e.dataset.status)")

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx, page, reqs = open_page(b)
    check("Absender/Betreff angezeigt", page.text_content("#ctx-from") == "Muster, Max" and "Wartungsvertrag" in page.text_content("#ctx-subject"))
    check("Start: Kategorie CAREER, kein Status", cats(page) == ["CAREER"] and page.text_content("#ctx-status") == "kein Status")
    check("Knöpfe aktiv bei Mailbox ≥1.8", page.eval_on_selector_all(".act", "els => els.every(e => !e.disabled)"))
    if shots: page.screenshot(path=str(shots / "01-pane-start.png"), full_page=True)

    page.click("[data-status=ACTION]"); wait_js(page, "document.getElementById('status').textContent.includes('ACTION')")
    check("ACTION setzt ACTION", sorted(cats(page)) == ["ACTION", "CAREER"] and pressed(page) == ["ACTION"], str(cats(page)))
    page.click("[data-status=WAITING]"); wait_js(page, "document.getElementById('status').textContent.includes('WAITING')")
    check("WAITING ersetzt ACTION, CAREER bleibt", sorted(cats(page)) == ["CAREER", "WAITING"] and pressed(page) == ["WAITING"], str(cats(page)))
    calls = page.evaluate("window.__calls.filter(c => c[0] !== 'get')")
    check("Reihenfolge: erst hinzufügen, dann entfernen", [c[:2] for c in calls[-2:]] == [["add", ["WAITING"]], ["remove", ["ACTION"]]], str(calls[-2:]))
    if shots: page.screenshot(path=str(shots / "02-pane-waiting.png"), full_page=True)
    page.click("[data-status=WAITING]"); wait_js(page, "document.getElementById('status').textContent.includes('entfernt')")
    check("Zweiter Klick entfernt WAITING", cats(page) == ["CAREER"] and pressed(page) == [])
    for s in ("PROJECT", "DONE", "REFERENCE"):
        page.click(f"[data-status={s}]"); wait_js(page, f"document.getElementById('status').textContent.includes('{s} gesetzt')")
    check("PROJECT/DONE/REFERENCE setzen nur Kategorien", sorted(cats(page)) == ["CAREER", "REFERENCE"], str(cats(page)))
    ops = {c[0] for c in page.evaluate("window.__calls")}
    check("Nur get/add/remove verwendet", ops <= {"get", "add", "remove"}, str(ops))

    # Tastatur
    page.focus("[data-status=ACTION]"); page.keyboard.press("Enter")
    wait_js(page, "document.getElementById('status').textContent.includes('ACTION gesetzt')")
    check("Tastatur: Enter auf ACTION", pressed(page) == ["ACTION"])
    outline = page.eval_on_selector("[data-status=ACTION]", "e => getComputedStyle(e).outlineStyle")
    check("Fokus sichtbar", outline != "none", outline)

    # Bewegung
    page.mouse.move(5, 5); page.hover(".lattice"); page.wait_for_timeout(50)
    st = page.eval_on_selector("#lattice", "e => getComputedStyle(e).animationPlayState")
    check("Gitter läuft bei Zeiger im Bereich", st == "running", st)
    page.evaluate("document.activeElement && document.activeElement.blur()")
    page.evaluate("document.getElementById('pane').dispatchEvent(new PointerEvent('pointerleave'))"); page.wait_for_timeout(50)
    st2 = page.eval_on_selector("#lattice", "e => getComputedStyle(e).animationPlayState")
    check("Gitter pausiert ohne Aufmerksamkeit", st2 == "paused", st2)
    page.evaluate("Object.defineProperty(document,'hidden',{get:()=>true,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))")
    check("Pause bei document.hidden", page.eval_on_selector("#pane", "e => e.classList.contains('is-hidden')"))
    page.evaluate("Object.defineProperty(document,'hidden',{get:()=>false,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))")
    page.click("#motion-toggle")
    an = page.eval_on_selector("#lattice", "e => getComputedStyle(e).animationName")
    check("Schalter 'Bewegung: reduziert' stoppt Animation", an == "none" and "reduziert" in page.text_content("#motion-toggle"), an)
    page.click("#motion-toggle")
    kf = page.evaluate("""() => { for (const s of document.styleSheets) for (const r of s.cssRules) if (r.name === 'lattice-drift') return [...r.cssRules].map(k => k.keyText + ' ' + k.style.transform); }""")
    check("Keyframes: 86 % Ruhe, max 1,5°/3 px", kf is not None and kf[0].startswith("0%, 86%") and "1.5deg" in kf[1] and "-3px" in kf[1], str(kf))
    dur = page.eval_on_selector("#lattice", "e => getComputedStyle(e).animationDuration")
    check("Zyklus 9 s", dur == "9s", dur)

    ext = sorted({r for r in reqs if not r.startswith(f"http://127.0.0.1:{port}")})
    check("Einzige externe Anfrage = Office.js", ext == [OFFICE], str(ext))
    if shots:
        page.hover(".lattice"); page.wait_for_timeout(100)
    ctx.close()

    # Reduced motion (System)
    ctx, page, _ = open_page(b, reduced=True)
    an = page.eval_on_selector("#lattice", "e => getComputedStyle(e).animationName")
    check("prefers-reduced-motion → keine Animation", an == "none", an)
    ctx.close()

    # Fehlende Kategorie
    ctx, page, _ = open_page(b, mock={"master": ["ACTION", "WAITING", "PROJECT", "DONE", "CAREER"], "initial": ["ACTION", "CAREER"]})
    page.click("[data-status=REFERENCE]"); wait_js(page, "document.getElementById('status').classList.contains('is-error')")
    check("Fehlende Kategorie: klare Meldung", "fehlt in Outlook" in page.text_content("#status"))
    check("Fehlende Kategorie: nichts verändert", sorted(cats(page)) == ["ACTION", "CAREER"], str(cats(page)))
    if shots: page.screenshot(path=str(shots / "03-pane-missing-category.png"), full_page=True)
    ctx.close()

    # Angehefteter Bereich: Nachrichtenwechsel (ItemChanged)
    ctx, page, _ = open_page(b)
    page.click("[data-status=ACTION]"); wait_js(page, "document.getElementById('status').textContent.includes('ACTION gesetzt')")
    page.evaluate("window.__switchItem('Zweite Testnachricht', 'Beispiel, Erika', ['DONE'])")
    wait_js(page, "document.getElementById('ctx-subject').textContent === 'Zweite Testnachricht'")
    check("ItemChanged: Kopf zeigt neue Nachricht", page.text_content("#ctx-from") == "Beispiel, Erika")
    wait_js(page, "document.querySelectorAll('#ctx-categories li').length === 1")
    check("ItemChanged: Kategorien/Status der neuen Nachricht", cats(page) == ["DONE"] and pressed(page) == ["DONE"], str(cats(page)))
    check("ItemChanged: alte Statusmeldung gelöscht", page.text_content("#status") == "")
    page.click("[data-status=PROJECT]"); wait_js(page, "document.getElementById('status').textContent.includes('PROJECT gesetzt')")
    items = page.evaluate("window.__items.map(i => i.__cats().slice().sort())")
    check("ItemChanged: Aktion trifft nur die neue Nachricht", items == [["ACTION", "CAREER"], ["PROJECT"]], str(items))
    page.evaluate("window.__switchItem(null)")
    wait_js(page, "document.getElementById('ctx-from').textContent === 'Keine Nachricht ausgewählt'")
    check("Keine Auswahl: Knöpfe gesperrt", page.eval_on_selector_all(".act", "els => els.every(e => e.disabled)"))
    page.evaluate("window.__switchItem('Dritte Testnachricht', 'Muster, Max', [])")
    wait_js(page, "document.getElementById('ctx-subject').textContent === 'Dritte Testnachricht'")
    wait_js(page, "[...document.querySelectorAll('.act')].every(e => e.getAttribute('aria-disabled') === 'false')")
    check("Neue Auswahl: Knöpfe wieder aktiv", page.eval_on_selector_all(".act", "els => els.every(e => !e.disabled)"))
    ctx.close()

    # Wechsel mitten in der Aktion (langsamer Host): add und remove bleiben an derselben Nachricht
    ctx, page, _ = open_page(b, mock={"delay": 250, "initial": ["WAITING"]})
    wait_js(page, "document.querySelectorAll('#ctx-categories li').length === 1")
    page.click("[data-status=ACTION]")
    page.wait_for_timeout(60)
    page.evaluate("window.__switchItem('Zweite Testnachricht', 'Beispiel, Erika', ['WAITING', 'CAREER'])")
    wait_js(page, "document.getElementById('status').textContent.includes('ACTION gesetzt')", timeout=6)
    items = page.evaluate("window.__items.map(i => i.__cats().slice().sort())")
    targets = {c[2] for c in page.evaluate("window.__calls") if c[0] in ("add", "remove")}
    check("Wechsel während Aktion: nur erste Nachricht verändert", items == [["ACTION"], ["CAREER", "WAITING"]] and len(targets) == 1, f"{items} {targets}")
    check("Wechsel während Aktion: Hinweis 'zuvor geöffneten Nachricht'", "zuvor geöffneten" in page.text_content("#status"), page.text_content("#status"))
    wait_js(page, "document.getElementById('ctx-subject').textContent === 'Zweite Testnachricht'")
    check("Wechsel während Aktion: Anzeige zeigt neue Nachricht", sorted(cats(page)) == ["CAREER", "WAITING"], str(cats(page)))
    ctx.close()

    # Schneller Doppelwechsel: späte Antwort der alten Nachricht darf die Anzeige nicht überschreiben
    ctx, page, _ = open_page(b, mock={"delays": {"B": 400, "C": 20}})
    page.evaluate("window.__switchItem('B', 'Beispiel, Erika', ['PROJECT'])")
    page.wait_for_timeout(30)
    check("Beim Laden: alter Status ausgeblendet + Aktionen gesperrt", pressed(page) == [] and page.eval_on_selector_all(".act", "els => els.every(e => e.getAttribute('aria-disabled') === 'true')"))
    # Echter Klick per DOM (Playwright würde bei aria-disabled bis zur Freigabe warten)
    page.evaluate("document.querySelector('[data-status=ACTION]').click()")
    page.evaluate("window.__switchItem('C', 'Muster, Max', ['DONE'])")
    page.wait_for_timeout(700)
    check("Schneller Wechsel: späte Antwort verworfen, Anzeige = letzte Nachricht", page.text_content("#ctx-subject") == "C" and cats(page) == ["DONE"], f"{page.text_content('#ctx-subject')} {cats(page)}")
    writes = [c for c in page.evaluate("window.__calls") if c[0] != "get"]
    check("Klick während Laden: keine Schreibaktion", writes == [], str(writes))
    ctx.close()

    # Alte Outlook-Version
    ctx, page, _ = open_page(b, mock={"maxMinor": 7})
    check("Mailbox < 1.8: Knöpfe gesperrt + Hinweis", page.eval_on_selector_all(".act", "els => els.every(e => e.disabled)") and "1.8" in page.text_content("#status"))
    ctx.close()

    # Breiten
    for w in (280, 320, 360, 480):
        ctx, page, _ = open_page(b, width=w, height=760)
        sw = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        clipped = page.evaluate("""() => [...document.querySelectorAll('.act, .ctx-from, .ctx-subject, .foot')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 0.5).length""")
        check(f"Breite {w}px: kein horizontales Scrollen/Abschneiden", sw[0] <= sw[1] and clipped == 0, f"{sw}, clipped={clipped}")
        if shots and w in (280, 480): page.screenshot(path=str(shots / f"04-pane-{w}px.png"), full_page=True)
        ctx.close()

    # Größe der veröffentlichten Dateien
    total = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    check("site/ < 60 KB", total < 60_000, f"{total} B")
    b.close()

srv.shutdown()
fails = [r for r in results if not r[1]]
print(f"\nE2E: {len(results) - len(fails)}/{len(results)} PASS")
sys.exit(1 if fails else 0)
