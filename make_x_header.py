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

    # ---- Everything in one centred band, measured off Chuck's iPhone
    # screenshot (Sep 5 2026). On iOS the profile view scales the 1500x500
    # banner to ~0.73 and crops ~118px off each side, then lays these over it
    # (source-pixel coordinates):
    #   status bar + "Messages" back-label   y 0..150   full width
    #   back button circle                    x 180..303, y 212..336
    #   search button circle                  x 1200..1323, y 212..336
    #   avatar                                x 145..420, y 465+
    # Desktop adds the avatar at x 20..352, y 333..500. The intersection of
    # what survives everywhere is x 360..1180, y 165..455 -- so that is the
    # only place anything is drawn. The old top-left lockup sat under the
    # status bar and the old headline ran into the search button.
    L, R = 360, 1180
    band_w = R - L

    # Row 1: small lockup
    badge = itn.render_badge(52)
    img.paste(badge, (L, 172))
    d = ImageDraw.Draw(img)
    fw = f(COND, 40)
    cx = L + 66
    for word, col in [("INSIDE ", WHITE), ("THE ", GREEN), ("NUMBER", WHITE)]:
        cx = track(d, (cx, 178), word, fw, col, sp=1)

    # Row 2: headline on one line
    fh = f(COND, 70)
    x = L
    for word, col in [("THE NUMBER ", WHITE), ("DOESN'T LIE.", GREEN)]:
        d.text((x, 236), word, font=fh, fill=col)
        x += d.textlength(word, font=fh)

    # Rows 3-4: the line, and what it means
    fb = f(SANS, 27)
    d.text((L, 330), "Every line, explained \u2014 what the market actually thinks.", font=fb, fill=MID)
    d.text((L, 366), "Live odds and the true price on every game, free.", font=fb, fill=MID)

    # Row 5
    track(d, (L, 412), "insidethenumber.com", f(MONO, 24), GREEN, sp=2)

    return img


def preview(img):
    """Simulate what X covers on iPhone AND desktop, so a collision is obvious."""
    p = img.copy()
    d = ImageDraw.Draw(p, "RGBA")
    red = (255, 60, 60, 110)
    # iPhone side crop
    d.rectangle([0, 0, 118, H], fill=(255, 200, 0, 90))
    d.rectangle([W - 118, 0, W, H], fill=(255, 200, 0, 90))
    # iPhone status bar / back label
    d.rectangle([0, 0, W, 150], fill=(255, 200, 0, 70))
    # iPhone back + search buttons
    d.ellipse([180, 212, 303, 336], fill=red)
    d.ellipse([1200, 212, 1323, 336], fill=red)
    # iPhone avatar
    d.ellipse([145, 465, 420, 740], fill=red)
    # desktop avatar
    d.ellipse([20, 333, 352, 665], fill=(60, 120, 255, 90), outline=(60, 120, 255, 255), width=3)
    d.text((400, 470), "red = iPhone overlays, blue = desktop avatar, yellow = iPhone crop/status bar",
           fill=(255, 220, 220, 255), font=f(SANS, 18))
    return p


if __name__ == "__main__":
    img = build()
    img.save(os.path.join(HERE, "social", "itn-x-header.png"), "PNG", optimize=True)
    preview(img).save("/sessions/fervent-compassionate-mayer/mnt/outputs/x_header_preview.png")
    print("wrote social/itn-x-header.png")
