# Installation in Outlook (Sideload)

Voraussetzungen:
- `https://bh-automation.github.io/outlook-command-center/taskpane.html` lädt.
- Die Kategorien ACTION, WAITING, PROJECT, DONE, REFERENCE existieren in Outlook (Einstellungen → Konten → Kategorien). Office.js kann nur vorhandene Kategorien setzen.

## Installieren (neues Outlook für Windows, getestet 24.09.2026)
1. `manifest.xml` herunterladen: `https://bh-automation.github.io/outlook-command-center/manifest.xml` (oder `manifest.production.xml` aus dem Repository).
2. Eine Mail markieren → Menüband **Apps** bzw. **Weitere Apps** → **Add-Ins abrufen**.
3. **Meine Add-Ins** → **Benutzerdefinierte Add-Ins** → **Benutzerdefiniertes Add-In hinzufügen** → **Aus Datei hinzufügen…** → `manifest.xml` wählen.
   - Falls der Dateidialog nur minimiert in der Taskleiste erscheint: auf den Eintrag klicken, dann über die Titelleiste **Maximieren**.
   - „Von URL hinzufügen“ war im Test nicht nutzbar; „Aus Datei“ funktioniert.
4. Warnhinweis lesen (Standardhinweis für benutzerdefinierte Add-Ins) → **Installieren**.
5. Eine empfangene Mail öffnen → **Apps** → **Precision Workspace**. Der Bereich öffnet sich rechts.

## Aktualisieren (neue Manifest-Version)
Outlook übernimmt Manifest-Änderungen nicht automatisch: Add-In entfernen (siehe `ROLLBACK.md`) und die neue `manifest.xml` wie oben **aus Datei** installieren. Code-Änderungen in `site/` wirken ohne Neuinstallation, sobald Pages neu veröffentlicht hat.

## Nachrichtenwechsel
Das Manifest fordert einen anheftbaren Bereich an (`SupportsPinning`). Mit Microsoft-365-Konto meldet Outlook dann jeden Nachrichtenwechsel (`ItemChanged`) und der Bereich zeigt die neue Nachricht.
**Outlook.com (Realtest 24.09.2026):** Das Manifest wird angenommen, aber Outlook meldet keinen Wechsel. Der Bereich bleibt offen und zeigt und bearbeitet weiter die Nachricht in seinem Kopf. Für eine andere Nachricht: Bereich schließen → Nachricht wählen → **Weitere Apps → Precision Workspace**.
