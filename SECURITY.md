# SECURITY

## Bedrohungsmodell (Kurzfassung)
| Risiko | Maßnahme |
|---|---|
| Datenabfluss von Maildaten | keine Netzwerk-APIs im Code (Validator prüft `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`); CSP `connect-src` nur 'self' + Office.js-Herkunft |
| Script-Injection (XSS) über Betreff/Absender | Ausgabe nur per `textContent`; `innerHTML`/`eval` im Validator verboten; CSP ohne Inline-Skripte |
| Kompromittierte Drittanbieter-Bibliothek | keine Bibliotheken; einziges externes Skript ist Office.js von Microsoft |
| Manipulierte GitHub Actions | nur `actions/*` und `github/*`, auf Commit-SHA gepinnt; Dependabot meldet Updates |
| Unbefugte Änderung am Code | Ruleset auf `main` (siehe docs/GITHUB-HARDENING.md), Pflicht-Statuscheck |
| Zu weite Rechte | nur `ReadWriteItem`; Workflows mit minimalen `permissions` |
| Geheimnisse im Repo | keine vorhanden/benötigt; Validator sucht Token-Muster |
| Öffentliche Pages-Seite | enthält nur statischen Code, keine Maildaten, keine Adressen |

## Grenzen
- GitHub Pages erlaubt keine eigenen HTTP-Header; die CSP wird per `<meta>` gesetzt (`frame-ancestors` ist per Meta nicht möglich – Outlook muss die Seite ohnehin einbetten).
- Office.js wird zur Laufzeit von Microsoft geladen (von Microsoft vorgeschrieben, kein SRI möglich, da die Datei sich ändert).

## Meldung
Probleme bitte als Issue im Repository melden.
