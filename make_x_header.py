#!/usr/bin/env python3
"""
X profile banner, 1500x500.

The previous version put the tagline and the URL in the lower left, which is
exactly where X drops the circular avatar. On a 1500x500 source the avatar
covers roughly x 20..352, y 333..500 — so two lines of body copy and the
website line were sitting underneath it.

This version keeps the whole bottom-left quadrant empty. The logo lockup sits
top-left (clear of the avatar), and everything else moves to the right half,
vertically centred. Mobile crops banners harder top and bottom, so nothing
important goes within 60px of either edge either.

    python3 make_x_header.py
"""

import os
from PIL import Image, ImageDraw, ImageFont
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("itn", os.path.join(HERE, "itn_logo.py"))
itn = importlib.util.module_from_spec(spec); spec.loader.exec_module(itn)

W, H = 1500, 500
BLACK = (5, 6, 8)
WHITE = (240, 242, 245)
GREEN = (0, 208, 132)
MID   = (156, 163, 175)
MUTED = (107, 114, 128)

COND = "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# Where X lays the avatar over a 1500x500 banner, plus a little slack.
AVATAR_BOX = (0, 320, 380, 500)


def f(p, s): return ImageFont.truetype(p, s)


def track(d, xy, text, font, fill, sp=6):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + sp
    return x


def build():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    # Horizontal wash: deep green on the left into navy on the right
    for x in range(W):
        t = x / (W - 1)
        r = int(6 + 2 * t)
        g = int(58 * (1 - t) + 20 * t)
        b = int(40 * (1 - t) + 52 * t)
        d.line([(x, 0), (x, H)], fill=(r, g, b))

    # Vignette the far corners back toward black
    for x in range(W):
        t = x / (W - 1)
        fade = max(0.0, (t - 0.72) / 0.28)
        if fade > 0:
            d.line([(x, 0), (x, H)], fill=(int(6 + 6 * (1 - fade)), int(20 * (1 - fade)),
                                           int(52 * (1 - fade) + 14 * fade)))

    # Faint grid, same texture as the site
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(20, 40, 44), width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(20, 40, 44), width=1)

    # ---- Logo lockup, top left. Sits above the avatar overlay. ----
    badge = itn.render_badge(104)
    img.paste(badge, (72, 60))
    d = ImageDraw.Draw(img)
    fw = f(COND, 60)
    cx = 200
    for word, col in [("INSIDE ", WHITE), ("THE ", GREEN), ("NUMBER", WHITE)]:
        cx = track(d, (cx, 68), word, fw, col, sp=2)
    track(d, (202, 134), "SHARP SPORTS ANALYSIS", f(MONO, 22), MUTED, sp=6)

    # ---- Everything else lives right of the avatar ----
    x0 = 620
    fh = f(COND, 76)
    d.text((x0, 150), "THE NUMBER", font=fh, fill=WHITE)
    d.text((x0, 226), "DOESN'T LIE.", font=fh, fill=GREEN)

    fb = f(SANS, 27)
    d.text((x0, 322), "A free pick every morning, with the reasoning shown.", font=fb, fill=MID)
    d.text((x0, 360), "Live odds and the true price on every game.", font=fb, fill=MID)

    track(d, (x0, 412), "insidethenumber.com", f(MONO, 25), GREEN, sp=2)

    return img


def preview(img):
    """Simulate exactly what X covers, so a collision is obvious."""
    p = img.copy()
    d = ImageDraw.Draw(p, "RGBA")
    d.ellipse([20, 333, 352, 665], fill=(255, 60, 60, 110), outline=(255, 60, 60, 255), width=4)
    d.rectangle([0, 0, W, 60], fill=(255, 200, 0, 60))
    d.rectangle([0, H - 60, W, H], fill=(255, 200, 0, 60))
    d.text((370, 300), "avatar overlay", fill=(255, 160, 160, 255), font=f(SANS, 22))
    return p


if __name__ == "__main__":
    img = build()
    img.save(os.path.join(HERE, "social", "itn-x-header.png"), "PNG", optimize=True)
    preview(img).save("/sessions/fervent-compassionate-mayer/mnt/outputs/x_header_preview.png")
    print("wrote social/itn-x-header.png")
