# RETENTION-LOG – Command Center (Champion/Challenger, je eine Variable)

| # | Champion | Challenger | Variable | Ergebnis | Entscheidung |
|---|---|---|---|---|---|
| 1 | Icon „konzentrische Ellipsen + Punkt“ | Icon „perspektivische Gitter-Ebene“ | Icon-Motiv | Ellipsen + Punkt wirken wie ein **Auge** (Überwachungs-Assoziation, widerspricht „kein Tracking“). Gitter-Ebene wirkt technisch, ohne Zahnrad-/Werkzeug-Klischee. | **PROMOTE_CHALLENGER** |
| 2 | Bewegung läuft dauerhaft | Bewegung nur bei Zeiger/Fokus im Bereich | Bewegungsauslöser | „Bewegung belohnt Aufmerksamkeit, fordert sie nie“; spart Rechenzeit, wenn der Bereich nur offen steht | **PROMOTE_CHALLENGER** |
| 3 | Knöpfe während Aktion `disabled` | `aria-disabled` statt `disabled` | Sperrmechanik | `disabled` nimmt Tastaturnutzern den Fokus (E2E-Test „Fokus sichtbar“ schlug fehl) | **PROMOTE_CHALLENGER** |
| 4 | Manifest nur V1_0 (ohne Pinning) | V1_0 + V1_1 mit `SupportsPinning` | Manifest-Struktur | Realtest: Ohne V1_1 kommt kein `ItemChanged`; der Bereich blieb offen und zeigte die alte Nachricht. Mit V1_1 meldet Outlook den Wechsel (sofern der Client es unterstützt). | **PROMOTE_CHALLENGER** – Realtest: auf Outlook.com ohne Wirkung (kein `ItemChanged`), schadet nicht; bleibt für Microsoft-365-Konten |
| 5 | Lattice CSS-2.5D (Tier A) | Canvas 2D (Tier B), gleiche Geometrie | 3D-Stufe | Canvas wirkt flacher (ohne echte Perspektive) und kostet ≈ 150× Task-Zeit (555 ms statt 3,7 ms je 9 s). | **KEEP_CHAMPION** |
| 6 | Neigung `rotateX(62deg)` | `rotateX(55deg)` | Neigung | Ring größer, Ebene wirkt weniger wie eine liegende Präzisionsfläche; Markierung rückt an den oberen Rand. Kein Gewinn. | **KEEP_CHAMPION** |

Zwei finale Challenger (#5, #6) ohne Verbesserung → **DESIGN FREEZE Lattice = Tier A, 62°, 9 s**. Vergleichsbild: `SCREENSHOTS/05-final-challengers.png` (links Champion, Mitte 55°, rechts Canvas).
WebGL (Tier C) nicht umgesetzt: Tier B bringt schon keinen sichtbaren Gewinn bei deutlich höheren Kosten.
