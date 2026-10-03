# GitHub-Härtung

Reihenfolge so gewählt, dass der Besitzer sich nicht aussperrt.

| # | Maßnahme | Stand 24.09.2026 |
|---|---|---|
| 1 | **Pages:** Settings → Pages → Source = **GitHub Actions** | aktiv |
| 2 | Deployment nur nach Validierung (`deploy` braucht `build`, `build` braucht `validate`) | aktiv |
| 3 | **Code security:** Dependabot alerts, Dependabot security updates, Secret scanning, Push protection | aktiv |
| 4 | **Actions:** nur Actions von GitHub (`actions/*`, `github/*`), SHA-Pinning Pflicht; Workflow permissions = Read | aktiv |
| 5 | **Ruleset `main`** – siehe unten | durch Besitzer anzulegen |
| 6 | **Konto:** Zwei-Faktor-Authentifizierung | Besitzer |

## Ruleset `main` (Settings → Rules → Rulesets → New ruleset → New branch ruleset)
- Name: `main-protection`, Enforcement: **Active**, Target branches: **Include default branch**
- ✔ Restrict deletions
- ✔ Require linear history
- ✔ Block force pushes
- **Nicht** aktivieren: „Require status checks“ und „Require a pull request“. Beide würden das direkte Hochladen über die Weboberfläche (Ein-Personen-Repo) blockieren. Die Veröffentlichung ist stattdessen über den Pages-Workflow abgesichert: Ohne `VALIDATION PASS` und grüne Tests wird nichts deployt.
- Keine Bypass-Liste nötig (die drei Regeln blockieren normale Commits nicht).
