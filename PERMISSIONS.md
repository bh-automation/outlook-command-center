# PERMISSIONS

| Berechtigung | Funktion | Warum keine schwächere reicht |
|---|---|---|
| `ReadWriteItem` | `item.categories.addAsync` / `removeAsync` an der geöffneten Nachricht (Mailbox 1.8) | `ReadItem` erlaubt nur Lesen; Microsoft verlangt für addAsync/removeAsync mindestens „read/write item“. |

Abgelehnt:
- `ReadWriteMailbox` – nur nötig, um Master-Kategorien anzulegen (`masterCategories`). Stattdessen werden die fünf Kategorien einmalig nativ in Outlook angelegt.
- `ReadMailbox` / REST / Microsoft Graph / SSO – nicht benötigt, kein Token, keine Anmeldung.

Gelesen (lokal, nur Anzeige): `item.from.displayName`, `item.subject`, `item.categories`.
Nicht gelesen: Nachrichtentext, Empfänger, Anhänge, E-Mail-Adressen.

Aktivierung: nur Nachrichten im Lesemodus (`ItemIs Message Read`).
