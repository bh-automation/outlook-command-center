"""Erzeugt die Add-in-Icons (16/32/64/80/128 px) – abstraktes Präzisionsgitter, keine Zahnräder."""
from pathlib import Path
from PIL import Image, ImageDraw

GRAPHITE = (17, 24, 32, 255)
NAVY_LINE = (36, 57, 74, 255)
BLUE = (0, 113, 187, 255)
FROST = (234, 241, 245, 255)
OUT = Path(__file__).resolve().parent.parent / "site" / "assets"
SS = 8  # Supersampling


def icon(size: int) -> Image.Image:
    S = size * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.18), fill=GRAPHITE)
    cx = cy = S / 2
    small = size <= 16
    lw = max(SS, int(S * (0.07 if small else 0.03)))
    # Perspektivische Ebene: Raute (Quadrat in Aufsicht, geneigt) in Precision Blue
    w, h = S * (0.34 if small else 0.33), S * (0.34 if small else 0.19)
    rh = [(cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)]
    d.line(rh + [rh[0]], fill=BLUE, width=int(lw * (1.3 if small else 1.6)), joint="curve")
    if not small:
        # Gitterlinien der Ebene (Frost, dünn)
        for t in (1/3, 2/3):
            a = (rh[3][0] + (rh[0][0]-rh[3][0])*t, rh[3][1] + (rh[0][1]-rh[3][1])*t)
            b = (rh[2][0] + (rh[1][0]-rh[2][0])*t, rh[2][1] + (rh[1][1]-rh[2][1])*t)
            d.line([a, b], fill=FROST, width=max(SS, lw // 2))
            a = (rh[0][0] + (rh[1][0]-rh[0][0])*t, rh[0][1] + (rh[1][1]-rh[0][1])*t)
            b = (rh[3][0] + (rh[2][0]-rh[3][0])*t, rh[3][1] + (rh[2][1]-rh[3][1])*t)
            d.line([a, b], fill=FROST, width=max(SS, lw // 2))
        # Vertikale Achse über der Ebene
        d.line([cx, cy - S * 0.36, cx, cy - h - S * 0.02], fill=FROST, width=lw)
        d.line([cx, cy + h + S * 0.02, cx, cy + S * 0.36], fill=NAVY_LINE, width=lw)
    return im.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for s in (16, 32, 64, 80, 128):
        icon(s).save(OUT / f"icon-{s}.png", optimize=True)
        print("icon", s, (OUT / f"icon-{s}.png").stat().st_size, "B")
