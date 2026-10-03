# INSTALLATION-LOG

| Wo | Was | Warum | Entfernen |
|---|---|---|---|
| PC (Windows) | nichts installiert außer dem Outlook-Add-in „Precision Workspace“ (Sideload, nur Manifest) | Aufgabenbereich | `ROLLBACK.md` |
| PC (Windows) | keine Entwicklerzertifikate, kein localhost-Server, keine Node-/Python-Pakete | – | – |
| Outlook | Kategorien ACTION, WAITING, PROJECT, DONE, REFERENCE (nativ angelegt) | Office.js kann nur vorhandene Kategorien setzen | Einstellungen → Konten → Kategorien |
| GitHub | Repository, Pages, CodeQL, Dependabot | Hosting und Prüfungen | `ROLLBACK.md` |
| Build-Container (Claude) | Playwright/Chromium (vorinstalliert), `office-addin-manifest` (npm, temporär) | E2E-Tests; Manifest-Prüfung (Online-Dienst nicht erreichbar) | Container wird verworfen |
