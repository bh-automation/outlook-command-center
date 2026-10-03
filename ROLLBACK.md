# ROLLBACK

## Add-in entfernen (sofort, vollständig)
1. Outlook (neu oder Web) → **Apps** → **Add-Ins abrufen** → **Meine Add-Ins**.
2. Unter „Benutzerdefinierte Add-Ins“ bei **Precision Workspace** auf **…** → **Entfernen**.
3. Der Eintrag „Precision Workspace“ unter **Apps** ist weg. Nachrichten, Ordner und Signatur bleiben unverändert.

Getestet 24.09.2026: Entfernen ohne Rückfrage; danach „Keine Add-Ins gefunden“; Neuinstallation aus Datei funktioniert.

## Auf einen früheren Stand zurück
- **Nur Code (`site/`):** im Repository den früheren Commit bzw. Tag wiederherstellen (Datei-Stand hochladen oder Revert) → Pages veröffentlicht automatisch neu.
- **Manifest:** frühere `manifest.production.xml` aus dem Tag/Commit laden → Add-in entfernen → aus Datei neu installieren.

## Kategorien
- Gesetzte Kategorien bleiben an den Nachrichten; es sind normale Outlook-Kategorien.
- Entfernen: Nachricht markieren → Kategorisieren → Häkchen entfernen. Die Kategorie selbst unter Einstellungen → Konten → Kategorien löschen/umbenennen.

## Veröffentlichung zurücknehmen
- GitHub → Repository → Settings → Pages → Veröffentlichung abschalten, oder das Repository archivieren.

## Signatur
Das Add-in liest und schreibt keine Signaturen und ist beim Verfassen nicht aktiv (Regel: nur Nachrichten im Lesemodus). Prüfung: neue Mail → Standardsignatur erscheint unverändert, Icon animiert.

## Lokaler Entwicklungs-Host
Nicht verwendet (kein localhost, kein Entwicklerzertifikat) – nichts zu entfernen.
