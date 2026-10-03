# WEB-RESEARCH-NOTES

| Thema | Befund | Quelle |
|---|---|---|
| Kategorien setzen | `item.categories.addAsync/removeAsync`, Mailbox 1.8, mindestens „read/write item“; Fehler `InvalidCategory`, wenn die Kategorie nicht in der Kategorienliste existiert | Microsoft Learn: Office.Categories (Outlook) |
| Kategorienliste anlegen | `mailbox.masterCategories` braucht „read/write mailbox“ → bewusst nicht genutzt | Microsoft Learn: Office.MasterCategories |
| Nachrichtenwechsel | `Office.EventType.ItemChanged`, Mailbox 1.5, nur für anheftbare Bereiche | Microsoft Learn: Implement a pinnable task pane in Outlook |
| Pinning im Manifest | `SupportsPinning` in `VersionOverridesV1_1`; V1_0 und V1_1 müssen beide vorhanden sein | ebd. |
| Pinning Outlook.com | als „nicht verfügbar“ genannt → im Realtest geprüft | ebd. |
| Manifest-Schema | Reihenfolgen laut XSD: `ShowTaskpane` = SourceLocation → SupportsPinning; FormFactor = FunctionFile → ExtensionPoint; V1_1 = Requirements → Hosts → Resources; V1_0 erlaubt verschachteltes V1_1 am Ende | Microsoft Learn: [MS-OWEMXML] Schemas mailappversionoverrides und /1.1 |
| Sideload neues Outlook | Apps → Add-Ins abrufen → Meine Add-Ins → Benutzerdefiniertes Add-In hinzufügen | Microsoft Learn: Sideload Outlook add-ins for testing (live bestätigt) |

Maschinelle XSD-Validierung war nicht möglich: Der Microsoft-Validierungsdienst (`office-addin-manifest validate`) antwortete mit 403, die XSD-Dateien waren aus der Build-Umgebung nicht abrufbar. Ersatz: Strukturabgleich mit dem XSD-Text auf Microsoft Learn und die Strukturprüfungen in `tools/validate_repo.py`. Den Ausschlag gibt die Installation in Outlook: Outlook lehnt ungültige Manifeste beim Hinzufügen ab.
