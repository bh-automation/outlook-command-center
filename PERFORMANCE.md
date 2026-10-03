# PERFORMANCE

## Budget und Umsetzung (v1, CSS-2.5D)
- Animation nur über `transform` (Compositor), keine Layout-/Paint-Animation
- 9-s-Zyklus, 86 % Ruhe, 14 % Bewegung; max. 1,5° / 3 px; keine Skalierung
- läuft nur bei Zeiger/Fokus im Bereich; pausiert bei `document.hidden` und Fensterwechsel
- `prefers-reduced-motion` → keine Animation; Schalter „Bewegung: reduziert“
- kein Canvas, kein WebGL, kein `requestAnimationFrame`, keine Timer-Schleifen

## Messungen lokal (Chromium headless, Office.js-Attrappe, 24.09.2026)
| Messgröße | Wert |
|---|---|
| Bereit (Seite geladen + Kategorien angezeigt), Median aus 5 | 68 ms (64–85 ms) |
| 9 s Animation mit Zeiger im Bereich: Layouts / Style-Neuberechnungen / Skriptzeit | 0 / 0 / 0 ms |
| 9 s Animation: Task-Zeit gesamt | 3,7 ms |
| JS-Heap nach 9 s | ≈ 2 MB |
| Größe `site/` gesamt (inkl. Icons) | 42 137 Byte |
| Vergleich Canvas-Challenger (gleiche Geometrie, `requestAnimationFrame`) | 555 ms Task-Zeit je 9 s (≈ 150×) → verworfen |

## Beobachtung im echten Outlook (neues Outlook für Windows, 24.09.2026)
- 20 Nachrichtenwechsel per Tastatur mit geöffnetem Bereich: Outlook reagierte ohne sichtbare Verzögerung, der Bereich blieb stabil.
- Neue Mail verfassen und senden mit installiertem Add-in: normal.
- Die Bewegung (max. 1,5° / 3 px) liegt unter der Auflösung der Bildschirmfotos; sichtbar belegt ist nur die Ruhelage. Bewegung, Pause und Reduced-Motion sind im Browser-Test belegt.
