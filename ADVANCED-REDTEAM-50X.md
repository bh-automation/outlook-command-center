# ADVANCED-REDTEAM-50X – Immersive (50 × 0/1/2 = 100, Freigabe ≥ 94, 0 kritische Fehler)

Stand: 24.09.2026, 19:25 – Endwertung nach Realtest.

| Bereich | # | Prüfung | Punkte | Beleg |
|---|---|---|---|---|
| Plattform | 1 | Client exakt bestimmt | 2 | neues Outlook für Windows + Outlook im Web |
| Plattform | 2 | Kontotyp bestimmt | 2 | Outlook.com, privates Microsoft-Konto |
| Plattform | 3 | Add-in-Unterstützung belegt | 2 | Sideload + Aufgabenbereich im echten Outlook |
| Plattform | 4 | Sideload-Richtlinie belegt | 2 | „Benutzerdefinierte Add-Ins“ verfügbar, keine Admin-Vorgabe |
| Plattform | 5 | Pinning-Unterstützung belegt | 2 | Realtest 24.09. 19:20: Manifest mit SupportsPinning angenommen, aber kein `ItemChanged` (Outlook.com) → Plattformgrenze belegt |
| Design | 6 | keine Host-Hacks | 2 | nur native Einstellungen + Add-in; kein DOM/CSS am Host |
| Design | 7 | Copilot-Design nur wenn verfügbar | 2 | geprüft; nur 3 Auswahllisten, passt nicht → nicht genutzt |
| Design | 8 | Kontrast exzellent | 2 | Primärtext 15,7:1 / 13,5:1; Sekundärtext ≥ 6,2:1; Akzent-Blau-Text 5,6:1; Linien 3,0:1 |
| Design | 9 | keine zusätzliche Unruhe | 2 | ein Eintrag unter „Apps“, Host-Oberfläche unverändert |
| Design | 10 | bisheriger Ablauf bleibt | 2 | Kategorien sind normale Outlook-Kategorien, Add-in optional |
| Architektur | 11 | unterstützter Erweiterungspunkt | 2 | `MessageReadCommandSurface`, `ShowTaskpane` |
| Architektur | 12 | Menüband-Integration gültig | 2 | „Weitere Apps → Precision Workspace“ mit V1_1-Manifest |
| Architektur | 13 | Manifest gültig | 2 | V1_0 + V1_1 von Outlook bei „Aus Datei hinzufügen“ angenommen |
| Architektur | 14 | minimale Rechte | 2 | nur `ReadWriteItem` |
| Architektur | 15 | HTTPS/Sicherheitsmodell | 2 | GitHub Pages HTTPS, CSP, eine Herkunft |
| 3D | 16 | abstrakt/professionell | 2 | Präzisions-Gitter, Ringe, kein Gegenstand |
| 3D | 17 | keine Gaming-Ästhetik | 2 | kein Neon, kein Glühen, keine Partikel |
| 3D | 18 | überwiegend ruhig | 2 | 86 % Ruhe je 9 s; max. 1,5° / 3 px |
| 3D | 19 | Fallback vorhanden | 2 | Reduced-Motion + Schalter; ohne Animation statisch vollständig |
| 3D | 20 | kein unnötiges Bibliotheksgewicht | 2 | 0 Bibliotheken, `site/` 42 KB |
| Performance | 21 | keine sichtbare Outlook-Verzögerung | 2 | 20 Nachrichtenwechsel mit offenem Bereich |
| Performance | 22 | Pause wenn verborgen | 2 | E2E: `document.hidden`, ohne Aufmerksamkeit |
| Performance | 23 | Speicherverhalten | 2 | JS-Heap ≈ 2 MB |
| Performance | 24 | keine großen Medien | 2 | nur SVG inline + 5 kleine PNG-Icons |
| Performance | 25 | kein dauerhafter GPU-Effekt | 2 | nur `transform`, 0 Layouts/0 Skriptzeit in 9 s, läuft nur bei Aufmerksamkeit |
| Datenschutz | 26 | kein Tracking | 2 | Validator |
| Datenschutz | 27 | keine Analytics | 2 | Validator |
| Datenschutz | 28 | keine Web-Fonts | 2 | Systemschriften; CSP `font-src 'none'` |
| Datenschutz | 29 | kein Abfluss von Nachrichteninhalt | 2 | Nachrichtentext wird nicht gelesen; keine Netzwerk-APIs; CSP `connect-src` |
| Datenschutz | 30 | Abhängigkeiten geprüft | 2 | keine Laufzeit-Abhängigkeit außer Office.js; Actions gepinnt, Dependabot |
| UX | 31 | Bereich bringt mehr als Deko | 1 | Ein-Klick-Status funktioniert; ohne Pinning je Nachricht neu öffnen |
| UX | 32 | Aktionen verständlich | 2 | Name + Kurzhinweis je Knopf, Status im Kopf |
| UX | 33 | max. fünf Hauptaktionen | 2 | genau fünf |
| UX | 34 | schmaler Bereich funktioniert | 2 | 280–480 px ohne Abschneiden (E2E) |
| UX | 35 | Tastatur/Fokus | 2 | Enter löst aus, Fokus sichtbar, Fokus bleibt nach Aktion |
| Signatur | 36 | bestehende Signatur erhalten | 2 | Testmail an eigenes Postfach: Text, Farben, Links identisch zur Referenz |
| Signatur | 37 | GIF bleibt animiert | 2 | GIF byte-identisch zur Referenz (gleiche Datei, gleiche Frames) |
| Signatur | 38 | erstes Bild funktioniert | 2 | gleiche Datei wie Referenz |
| Signatur | 39 | keine Größenänderung | 2 | Bildmaße und Dateigrößen identisch |
| Signatur | 40 | Empfängeransicht unverändert | 2 | empfangenes HTML entspricht der Referenz |
| Stabilität | 41 | übersteht Outlook-Neustart | 2 | nach Neustart vorhanden, lädt, zeigt Nachricht |
| Stabilität | 42 | übersteht Nachrichtenwechsel | 1 | stabil, keine falschen Schreibzugriffe; Bereich folgt der Auswahl aber nicht (Outlook.com) |
| Stabilität | 43 | kein defekter Bereich | 2 | lädt im echten Outlook |
| Stabilität | 44 | Fehler werden sauber gemeldet | 2 | fehlende Kategorie, alte Outlook-Version, keine Auswahl |
| Stabilität | 45 | Deinstallation/Rollback vorhanden | 2 | `ROLLBACK.md` |
| Nutzen | 46 | Outlook wirkt eigenständiger | 2 | Blaupause + Dunkel + eigener Bereich |
| Nutzen | 47 | bleibt professionell | 2 | ruhige Farben, eine Akzentfarbe |
| Nutzen | 48 | System schnell erklärbar | 2 | 5 Knöpfe = 5 Status, ein Status pro Mail |
| Nutzen | 49 | Nutzen größer als Wartung | 1 | Wartung minimal; Nutzen durch fehlendes Pinning begrenzt |
| Nutzen | 50 | zwei finale Challenger ohne Verbesserung | 2 | Canvas (Tier B) und 55°-Neigung verworfen (RETENTION-LOG #5/#6) |

Ergebnis: **97/100**, 0 kritische Fehler → **PASS** (Freigabe ≥ 94).

Kritische Fehler (Richtlinie umgangen · Host-DOM/CSS · Signatur beschädigt · Postfachdaten nach außen · Outlook spürbar langsamer · Oberfläche lenkt ab): **keiner gefunden**.
