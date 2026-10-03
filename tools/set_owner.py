#!/usr/bin/env python3
"""Setzt den GitHub-Benutzernamen im Produktionsmanifest ein.
Aufruf: python tools/set_owner.py <github-benutzername>"""
import re
import sys
from pathlib import Path

if len(sys.argv) != 2 or not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", sys.argv[1]):
    sys.exit("Aufruf: python tools/set_owner.py <github-benutzername>")
user = sys.argv[1].lower()  # github.io-Hostnamen sind klein geschrieben
p = Path(__file__).resolve().parent.parent / "manifest.production.xml"
s = p.read_text(encoding="utf-8")
if "YOUR_GITHUB_USER" not in s:
    sys.exit("Platzhalter bereits ersetzt.")
p.write_text(s.replace("YOUR_GITHUB_USER", user), encoding="utf-8")
print(f"Manifest gesetzt auf https://{user}.github.io/outlook-command-center/")
