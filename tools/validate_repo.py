#!/usr/bin/env python3
"""Repository-Validator für den Benedict Precision Workspace (Outlook-Add-in).

Harte Prüfungen (Exit-Code 1 bei Fehler):
  Manifest   – wohlgeformt, GUID, nur ReadWriteItem, nur HTTPS, eine Herkunft, Ressourcen vorhanden
  Assets     – Icon-Größen passend zum Manifest
  Web        – CSP vorhanden, einziges externes Skript = Office.js, kein Inline-Skript,
               keine Netzwerk-APIs, kein innerHTML/eval, keine Web-Fonts, keine Analytics
  Workflows  – minimale Rechte, Actions auf Commit-SHA gepinnt
  Geheimnisse – keine Token-/Schlüssel-Muster im Repository

Aufruf:  python tools/validate_repo.py [--allow-placeholder]
"""
from __future__ import annotations

import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MANIFEST = ROOT / "manifest.production.xml"
OFFICE_JS = "https://appsforoffice.microsoft.com/lib/1/hosted/office.js"
PLACEHOLDER = "YOUR_GITHUB_USER"
REPO_NAME = "outlook-command-center"
STATUS = ["ACTION", "WAITING", "PROJECT", "DONE", "REFERENCE"]
NS = {
    "o": "http://schemas.microsoft.com/office/appforoffice/1.1",
    "bt": "http://schemas.microsoft.com/office/officeappbasictypes/1.0",
    "v": "http://schemas.microsoft.com/office/mailappversionoverrides",
    "v11": "http://schemas.microsoft.com/office/mailappversionoverrides/1.1",
}
XSI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"
REQUIRED_FILES = [
    "manifest.production.xml", "README.md", "SECURITY.md", "PERMISSIONS.md", "PERFORMANCE.md",
    "ROLLBACK.md", "CHANGELOG.md", "docs/GITHUB-HARDENING.md", "docs/REDTEAM-GITHUB.md",
    "site/taskpane.html", "site/taskpane.css", "site/taskpane.js", "site/logic.js",
    "site/commands.html", "site/commands.js", "site/support.html", "site/index.html",
    ".github/workflows/pages.yml", ".github/workflows/codeql.yml", ".github/workflows/validate.yml",
    ".github/dependabot.yml",
]

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("kein PNG")
    return struct.unpack(">II", head[16:24])


def check_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"Datei fehlt: {rel}")


def check_manifest(allow_placeholder: bool) -> None:
    raw = MANIFEST.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(raw.encode("utf-8"))
    except ET.ParseError as e:
        fail(f"Manifest nicht wohlgeformt: {e}")
        return
    if PLACEHOLDER in raw and not allow_placeholder:
        fail(f"Manifest enthält noch den Platzhalter {PLACEHOLDER}")

    gid = root.findtext("o:Id", namespaces=NS) or ""
    if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", gid):
        fail(f"Ungültige Add-in-Id: {gid!r}")
    ver = root.findtext("o:Version", namespaces=NS) or ""
    if not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", ver):
        fail(f"Ungültige Version: {ver!r}")

    perms = [p.text.strip() for p in root.iter(f"{{{NS['o']}}}Permissions") if p.text]
    if perms != ["ReadWriteItem"]:
        fail(f"Berechtigung muss genau ReadWriteItem sein, gefunden: {perms}")

    urls = re.findall(r'(?:DefaultValue|>)\s*"?(https?://[^"<\s]+)', raw)
    urls += [u for u in re.findall(r"(https?://[^\"<\s]+)", raw) if u not in urls]
    urls = [u for u in urls if not u.startswith("http://schemas.microsoft.com") and "w3.org" not in u]
    origins = set()
    for u in urls:
        p = urlparse(u)
        if p.scheme != "https":
            fail(f"Nicht-HTTPS-URL im Manifest: {u}")
        origins.add(p.netloc)
    if len(origins) != 1:
        fail(f"Manifest nutzt mehr als eine Herkunft: {sorted(origins)}")

    # Ressourcen-URLs → Dateien unter site/
    for u in urls:
        p = urlparse(u)
        if p.path.rstrip("/") == "":
            continue  # AppDomain
        prefix = f"/{REPO_NAME}/"
        if not p.path.startswith(prefix):
            fail(f"URL liegt nicht unter /{REPO_NAME}/: {u}")
            continue
        local = SITE / p.path[len(prefix):]
        if not local.is_file():
            fail(f"Manifest verweist auf fehlende Datei: site/{p.path[len(prefix):]}")

    # Icon-Größen
    expect = {"icon-16.png": 16, "icon-32.png": 32, "icon-64.png": 64, "icon-80.png": 80, "icon-128.png": 128}
    for name, size in expect.items():
        f = SITE / "assets" / name
        if f.is_file():
            w, h = png_size(f)
            if (w, h) != (size, size):
                fail(f"{name}: {w}×{h} statt {size}×{size}")
        else:
            fail(f"Icon fehlt: assets/{name}")

    # VersionOverrides: V1_0 außen, V1_1 innen (Pflicht für SupportsPinning), Pinning aktiv
    outer = root.find("v:VersionOverrides", NS)
    if outer is None or outer.attrib.get(XSI_TYPE) != "VersionOverridesV1_0":
        fail("VersionOverridesV1_0 fehlt als äußeres Element")
    else:
        inner = outer.find("v11:VersionOverrides", NS)
        if inner is None or inner.attrib.get(XSI_TYPE) != "VersionOverridesV1_1":
            fail("VersionOverridesV1_1 fehlt (innerhalb von V1_0)")
        else:
            pins = [e.text for e in inner.iter(f"{{{NS['v11']}}}SupportsPinning")]
            if pins != ["true"]:
                fail(f"SupportsPinning muss genau einmal true sein, gefunden: {pins}")
            sets = inner.find("v11:Requirements/bt:Sets", NS)
            if sets is None or sets.attrib.get("DefaultMinVersion") != "1.5":
                fail("V1_1 Requirements: Mailbox DefaultMinVersion 1.5 erwartet (ItemChanged)")
            # Jede resid muss in Resources definiert sein
            ids = {e.attrib["id"] for e in inner.iter() if "id" in e.attrib and e.tag.startswith("{" + NS["bt"])}
            for e in inner.iter():
                rid = e.attrib.get("resid")
                if rid and rid not in ids:
                    fail(f"resid ohne Ressource: {rid}")
            # Aufgabenbereich-URL (Menüband) == SourceLocation (FormSettings)
            tp = [e.attrib.get("DefaultValue") for e in inner.iter(f"{{{NS['bt']}}}Url") if e.attrib.get("id") == "Taskpane.Url"]
            src = root.find("o:FormSettings/o:Form/o:DesktopSettings/o:SourceLocation", NS)
            if not tp or src is None or tp[0] != src.attrib.get("DefaultValue"):
                fail("Taskpane.Url und FormSettings/SourceLocation weichen voneinander ab")
            ctx = [e.attrib.get(XSI_TYPE) for e in inner.iter(f"{{{NS['v11']}}}ExtensionPoint")]
            if ctx != ["MessageReadCommandSurface"]:
                fail(f"Nur MessageReadCommandSurface erlaubt, gefunden: {ctx}")

    # Regel: nur Nachrichten im Lesemodus
    rules = [r.attrib for r in root.iter(f"{{{NS['o']}}}Rule") if r.attrib.get("ItemType")]
    if rules != [{"{http://www.w3.org/2001/XMLSchema-instance}type": "ItemIs", "ItemType": "Message", "FormType": "Read"}]:
        fail(f"Aktivierungsregel unerwartet: {rules}")


SCRIPT_SRC = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
LINK_HREF = re.compile(r"<link\b[^>]*href=\"([^\"]+)\"", re.I)
NET_API = re.compile(r"\b(fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket|EventSource|importScripts)")
DANGEROUS = re.compile(r"\b(innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval\s*\(|new\s+Function)\b")
ANALYTICS = re.compile(r"(google-analytics|googletagmanager|gtag\(|mixpanel|segment\.io|hotjar|clarity\.ms|plausible|matomo|sentry)", re.I)
FONTS = re.compile(r"(fonts\.googleapis|fonts\.gstatic|@font-face|@import)", re.I)


def check_web() -> None:
    for html in sorted(SITE.glob("*.html")):
        text = html.read_text(encoding="utf-8")
        if "Content-Security-Policy" not in text or "default-src 'none'" not in text:
            fail(f"{html.name}: CSP mit default-src 'none' fehlt")
        for attrs, body in SCRIPT_SRC.findall(text):
            m = re.search(r'src="([^"]+)"', attrs)
            if not m:
                if body.strip():
                    fail(f"{html.name}: Inline-Skript gefunden")
                continue
            src = m.group(1)
            if src.startswith("http") and src != OFFICE_JS:
                fail(f"{html.name}: externes Skript nicht erlaubt: {src}")
            if not src.startswith("http") and not (SITE / src).is_file():
                fail(f"{html.name}: Skript fehlt: {src}")
        for href in LINK_HREF.findall(text):
            if href.startswith("http"):
                fail(f"{html.name}: externe Ressource: {href}")
        if "http://" in text.replace("http://www.w3.org", ""):
            fail(f"{html.name}: http:// gefunden")
        if ANALYTICS.search(text):
            fail(f"{html.name}: Analytics-Muster gefunden")
    for f in list(SITE.glob("*.js")) + list(SITE.glob("*.css")):
        text = f.read_text(encoding="utf-8")
        if f.suffix == ".js":
            if NET_API.search(text):
                fail(f"{f.name}: Netzwerk-API gefunden ({NET_API.search(text).group(0)})")
            if DANGEROUS.search(text):
                fail(f"{f.name}: unsicheres DOM/eval-Muster ({DANGEROUS.search(text).group(0)})")
        if ANALYTICS.search(text):
            fail(f"{f.name}: Analytics-Muster gefunden")
        if FONTS.search(text):
            fail(f"{f.name}: Web-Font/Import gefunden")
        if re.search(r"url\(\s*['\"]?https?:", text):
            fail(f"{f.name}: externe url() gefunden")
    # Buttons ↔ Logik
    html = (SITE / "taskpane.html").read_text(encoding="utf-8")
    buttons = re.findall(r'data-status="([A-Z]+)"', html)
    if buttons != STATUS:
        fail(f"Aktionsknöpfe {buttons} ≠ {STATUS}")
    if len(buttons) > 5:
        fail("Mehr als 5 Primäraktionen")
    logic = (SITE / "logic.js").read_text(encoding="utf-8")
    if 'var STATUS = ["ACTION", "WAITING", "PROJECT", "DONE", "REFERENCE"]' not in logic:
        fail("logic.js: Statusliste weicht ab")
    js = (SITE / "taskpane.js").read_text(encoding="utf-8")
    for forbidden in ("item.move", "displayReplyForm", "sendAsync", "deleteAsync", "masterCategories"):
        if forbidden in js:
            fail(f"taskpane.js: nicht erlaubte API {forbidden}")
    # Private Daten dürfen nicht veröffentlicht werden
    for f in SITE.rglob("*"):
        if f.is_file() and f.suffix in {".html", ".js", ".css"}:
            if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", f.read_text(encoding="utf-8")):
                fail(f"{f.relative_to(ROOT)}: E-Mail-Adresse gefunden")
    allowed_ext = {".html", ".js", ".css", ".png"}
    for f in SITE.rglob("*"):
        if f.is_file() and f.suffix not in allowed_ext:
            fail(f"Unerwartete Datei im veröffentlichten Ordner: {f.relative_to(ROOT)}")


def check_workflows() -> None:
    wf_dir = ROOT / ".github" / "workflows"
    for wf in sorted(wf_dir.glob("*.yml")):
        text = wf.read_text(encoding="utf-8")
        if "permissions:" not in text:
            fail(f"{wf.name}: keine explizite permissions-Angabe")
        if "write-all" in text or "contents: write" in text:
            fail(f"{wf.name}: zu weitreichende Schreibrechte")
        for use in re.findall(r"uses:\s*([^\s#]+)", text):
            if use.startswith("./"):
                continue
            ref = use.split("@", 1)[1] if "@" in use else ""
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                fail(f"{wf.name}: Action nicht auf Commit-SHA gepinnt: {use}")
            owner = use.split("/", 1)[0]
            if owner not in {"actions", "github"}:
                fail(f"{wf.name}: Action außerhalb von actions/ bzw. github/: {use}")


SECRET = re.compile(
    r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35})"
)


def check_secrets() -> None:
    for f in ROOT.rglob("*"):
        if ".git" in f.parts or not f.is_file() or f.suffix in {".png"}:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if f.name == "validate_repo.py":
            continue
        if SECRET.search(text):
            fail(f"Geheimnis-Muster in {f.relative_to(ROOT)}")


def main() -> int:
    allow_placeholder = "--allow-placeholder" in sys.argv
    check_files()
    if MANIFEST.is_file():
        check_manifest(allow_placeholder)
    check_web()
    check_workflows()
    check_secrets()
    for w in warnings:
        print("WARNUNG:", w)
    if errors:
        for e in errors:
            print("FEHLER:", e)
        print(f"VALIDATION FAIL ({len(errors)} Fehler)")
        return 1
    print("VALIDATION PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
