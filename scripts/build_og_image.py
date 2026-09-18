#!/usr/bin/env python3
"""
Inside the Number — social share card (og-image.png).

Why this exists: og-image.png was a one-off binary committed in Aug 2026 with
no source and no way to regenerate it. When the product repositioned away from
picks, the card still read "One free pick every morning" and contradicted the
site, both bios and the Beehiiv description on every share.

This script is the reproducible source. It takes the pristine card
(assets/og/og-image-base.png, the Aug 2026 artwork) and rewrites ONLY the
subtitle block: background rebuilt from the surrounding gradient, the 84px
scanline grid restored, then one line of copy drawn in the brand face.

Everything else - gradient, ITN badge, wordmark, headline, divider, domain,
league strip - is the untouched original. Run:

    python3 scripts/build_og_image.py            # writes og-image.png
    python3 scripts/build_og_image.py --check    # verify only, no write
"""
import argparse, sys, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "assets", "og", "og-image-base.png")
OUT  = os.path.join(ROOT, "og-image.png")
FONT = os.path.join(ROOT, "assets", "fonts", "Barlow-Medium.ttf")

SIZE       = (1200, 630)
SUBTITLE   = "Line moves, key numbers and fair prices. Not picks."
SUB_COLOR  = (156, 163, 175)      # sampled from the original subtitle ink
LEFT       = 85                   # original subtitle left margin
BASELINE   = 516                  # centred in the block the two old lines held
BAND       = (465, 562)           # rows rebuilt from the gradient
SCANLINES  = range(0, 630, 84)    # grid rows, flat #101319 in the original
SCAN_COLOR = (16, 19, 25)
FONT_SIZE  = 29                   # matches the original subtitle x-height/width

def build():
    if not os.path.exists(BASE):
        sys.exit(f"STOP. Base artwork missing: {BASE}")
    img = Image.open(BASE).convert("RGB")
    if img.size != SIZE:
        sys.exit(f"STOP. Base is {img.size}, expected {SIZE}")
    px = img.load()
    y0, y1 = BAND

    # 1. rebuild the band: vertical linear interpolation of the gradient
    for x in range(SIZE[0]):
        top, bot = px[x, y0 - 1], px[x, y1 + 1]
        span = (y1 + 1) - (y0 - 1)
        for y in range(y0, y1 + 1):
            t = (y - (y0 - 1)) / span
            px[x, y] = tuple(round(top[c] + (bot[c] - top[c]) * t) for c in range(3))

    # 2. restore the scanline grid inside the band
    d = ImageDraw.Draw(img)
    for y in SCANLINES:
        if y0 <= y <= y1:
            d.line([(0, y), (SIZE[0], y)], fill=SCAN_COLOR)

    # 3. one line of copy, brand face, original left margin
    d.text((LEFT, BASELINE), SUBTITLE,
           font=ImageFont.truetype(FONT, FONT_SIZE), fill=SUB_COLOR, anchor="ls")
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    img = build()
    if a.check:
        print(f"OK base->render {img.size}, subtitle: {SUBTITLE!r}")
        return
    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size}")
    print(f"subtitle: {SUBTITLE!r}")

if __name__ == "__main__":
    main()
