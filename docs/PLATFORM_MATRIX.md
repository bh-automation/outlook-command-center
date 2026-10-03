# PLATFORM_MATRIX – Benedict Outlook Immersive (Loop v1, Abschnitt 3)

Stand: 24.09.2026, 14:40–14:50. Nur gelesen, nichts verändert.

## PLATFORM_MATRIX
| Punkt | Befund | Beleg |
|---|---|---|
| Outlook-Oberflächen | Neues Outlook für Windows + Outlook im Web (outlook.live.com) | live, Baseline |
| Kontotyp | **Outlook.com, privates Microsoft-Konto** – kein Arbeits- oder Schulkonto | Baseline |
| Administratorvorgaben | keine (kein Firmenkonto) | Baseline |
| Add-ins aktiviert | ja – „Meine Vorlagen“ und „Bing Maps“ aktiv (von Microsoft bereitgestellt) | live 24.09.2026 |
| Sideloading | **AVAILABLE** – neues Outlook: Mail markieren → „Weitere Apps“ → „Add-ins abrufen“ → „Meine Add-Ins“ → „Benutzerdefinierte Add-Ins“: Installation **aus Datei oder von URL**; aktuell keine benutzerdefinierten Add-Ins | live 24.09.2026 16:41 |
| Anheftbarer Aufgabenbereich (Pinning) | **NICHT VERFÜGBAR.** Microsoft Learn: „Pinnable task panes aren't available for … Outlook.com“. Nur für Microsoft-365-Abonnenten mit Arbeitskonto. | learn.microsoft.com/office/dev/add-ins/outlook/pinnable-taskpane |
| Copilot-Design | vorhanden, nur 3 Auswahllisten, **kein Aktualisierungsrhythmus** | live, Retention-Log |
| Eigene Menüband-Registerkarte | nicht möglich im neuen Outlook / Web (nur klassisches Outlook) | Pack, Microsoft-Doku |
| HTTPS-Hosting für ein Add-in | GitHub Pages (Konto `bh-automation`) | 24.09.2026 |

## Gate Phase 4
`ADVANCED_ADDIN = TECHNISCH MÖGLICH, ABER NICHT EMPFOHLEN`

Gründe:
1. Ohne Pinning schließt sich der Bereich bei jedem Wechsel zur nächsten Mail. Ein „Command Center“ müsste bei jeder Mail neu geöffnet werden.
2. Die Aktionen ACTION/WAITING/PROJECT/DONE liefern native QuickSteps mit einem Klick und ohne Wartungsaufwand.
3. Das Add-in braucht dauerhaftes HTTPS-Hosting (Konto nötig), eine Sideload-Freigabe und Pflege bei Änderungen des Manifests.
4. Red-Team-Punkte 31 („Bereich bringt mehr als Deko“) und 49 („Nutzen größer als Wartungsaufwand“) würden voraussichtlich scheitern.

Empfehlung: native Phase 2 fertigstellen (Kategorien, Favoriten, QuickSteps, bedingte Formatierung). Das Add-in erst neu bewerten, wenn ein Firmen- bzw. Microsoft-365-Arbeitskonto mit Pinning zur Verfügung steht.

## Hard Start (Loop v1, Abschnitt 0) – 24.09.2026, 14:50
```text
PRECISION SKILL      = PASS  (outlook-precision-workspace installiert)
IMMERSIVE SKILL      = FAIL  (nur als ZIP im Pack vorhanden, nicht installiert)
CLAUDE DESKTOP       = PASS  (Sitzung mit dem PC verbunden, Bildschirmsteuerung zuletzt 14:30 erfolgreich)
OUTLOOK ACCESS       = PASS  (neues Outlook für Windows per Bildschirmsteuerung, Web per Chrome)
ADVANCED PACK ACCESS = PASS  (alle Dateien gelesen)
→ STOP laut Loop: Outlook wird nicht angefasst, bis der Immersive-Skill installiert ist.
```

## Vorab-Einordnung der Route (Abschnitt 8)
- Route A (angehefteter Bereich): **ausgeschlossen**, weil Outlook.com kein Pinning unterstützt.
- Route B (normaler Aufgabenbereich, 1 Menüband-Befehl): möglich, **wenn** Sideloading im Konto funktioniert. Wird live geprüft.
- Route C: falls Sideloading nicht angeboten wird.

## Offene Voraussetzungen für Route B
1. Sideloading live prüfen (Outlook → Apps/Add-Ins → Meine Add-Ins → „Benutzerdefiniertes Add-In hinzufügen“).
2. Native Ebene zuerst fertigstellen (Abschnitt 6): Die Kategorien ACTION/WAITING/PROJECT/DONE/REFERENCE müssen in der Kategorienliste existieren. Office.js kann nur vorhandene Kategorien setzen. Neue Kategorien anlegen würde die Berechtigung ReadWriteMailbox erfordern, und die ist nicht minimal.
3. HTTPS-Hosting: Empfohlen ist GitHub Pages (statisch, kostenlos, ohne Nachrichtendaten). Benötigt ein GitHub-Konto des Nutzers und seine Freigabe für die Veröffentlichung.
   Nicht empfohlen: localhost mit Entwicklerzertifikat. Das installiert ein Stammzertifikat in Windows (Sicherheitseinstellung) und erfordert einen dauerhaft laufenden Server.
4. API-Grenzen (Office.js): Kategorien setzen und entfernen geht (Mailbox 1.8, Berechtigung ReadWriteItem). Kennzeichnen und Archivieren gibt es in Office.js nicht direkt. DONE ist deshalb nur als „Status-Kategorien entfernen“ realisierbar. Ein echtes Archivieren bliebe beim QuickStep.

## Nachtrag 24.09.2026, 16:36–16:41 (live)
- Kategorien angelegt: ACTION (Rot), WAITING (Orange), PROJECT (Blau), DONE (Grün), REFERENCE (Blaugrün), CAREER (Lila), FINANCE (Gelb), PRIVATE (Grau). ACTION und WAITING sind als Favoriten im Ordnerbereich.
- Sideloading verfügbar (aus Datei oder URL) → **Route B** (normaler Aufgabenbereich, 1 Menüband-Befehl).

## Nachtrag 24.09.2026, 19:07–19:25 (Realtest v1.0.0)
- Manifest V1_0 + V1_1 mit `SupportsPinning` „Aus Datei“ installiert: angenommen („Von URL“ ausgegraut).
- Nachrichtenwechsel mit offenem Bereich: **kein `ItemChanged`** → Pinning auf Outlook.com bestätigt nicht verfügbar. Bereich zeigt weiter die Ausgangsnachricht; Aktionen treffen nur diese.
- Neu öffnen auf anderer Nachricht: zeigt die neue Nachricht. Nach Outlook-Neustart: Add-in vorhanden und funktionsfähig.
