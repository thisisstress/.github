from __future__ import annotations

from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "profile" / "assets"
OUT = ROOT / "artifacts" / "profile-preview"
OUT.mkdir(parents=True, exist_ok=True)

FILES = [
    "hero-premium.svg",
    "overview-snapshot.svg",
    "final-architecture.svg",
    "model-journey.svg",
    "validation-evidence.svg",
    "footer-endcap.svg",
]

RENDER_WIDTH = 1200
GAP = 28
LABEL_H = 34
MARGIN = 28
BG = (13, 17, 23)
FG = (222, 228, 234)

rendered = []
for filename in FILES:
    src = ASSETS / filename
    png = OUT / filename.replace(".svg", ".png")
    cairosvg.svg2png(
        bytestring=src.read_bytes(),
        write_to=str(png),
        output_width=RENDER_WIDTH,
    )
    with Image.open(png) as im:
        rendered.append((filename, im.convert("RGB").copy()))

sheet_w = RENDER_WIDTH + MARGIN * 2
sheet_h = MARGIN + sum(LABEL_H + im.height + GAP for _, im in rendered)
sheet = Image.new("RGB", (sheet_w, sheet_h), BG)
draw = ImageDraw.Draw(sheet)

y = MARGIN
for filename, im in rendered:
    draw.text((MARGIN, y + 8), filename, fill=FG)
    y += LABEL_H
    sheet.paste(im, (MARGIN, y))
    y += im.height + GAP

contact = OUT / "profile-contact-sheet.png"
sheet.save(contact, optimize=True)

# Also produce a compact "GitHub-like" width to catch small-text / density issues.
MOBILE_W = 760
compact = []
for filename, im in rendered:
    h = round(im.height * MOBILE_W / im.width)
    compact.append((filename, im.resize((MOBILE_W, h), Image.Resampling.LANCZOS)))

compact_w = MOBILE_W + MARGIN * 2
compact_h = MARGIN + sum(LABEL_H + im.height + GAP for _, im in compact)
compact_sheet = Image.new("RGB", (compact_w, compact_h), BG)
draw = ImageDraw.Draw(compact_sheet)
y = MARGIN
for filename, im in compact:
    draw.text((MARGIN, y + 8), filename, fill=FG)
    y += LABEL_H
    compact_sheet.paste(im, (MARGIN, y))
    y += im.height + GAP

compact_sheet.save(OUT / "profile-contact-sheet-760.png", optimize=True)

print(f"Rendered {len(FILES)} profile panels")
print(contact)
