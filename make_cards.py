#!/usr/bin/env python3
"""
Inside the Number — social card generator.

Renders 1600x900 cards that match insidethenumber.com rather than merely using
its colours. Everything here is lifted from the live site:

  * the ITN mark beside the wordmark, with THE set in green
  * the green radial glow bleeding from the top left
  * the faint 80px grid over the lower half
  * a rounded, bordered, top-lit panel — the same treatment as the analysis
    cards on a game page
  * a huge Barlow-Condensed-style headline with one accent word in green
  * mono, letter-spaced, uppercase labels
  * insidethenumber.com and 21+ on the footer line

    python3 make_cards.py     # rebuild everything into social/cards/

Fonts ship with the OS — Liberation Sans Narrow Bold stands in for Barlow
Condensed and DejaVu Sans Mono for IBM Plex Mono — so there is nothing to
download and nothing to go stale.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 900

# Straight from the site's CSS custom properties
BLACK    = (5, 6, 8)
SURF1    = (10, 12, 16)
SURF2    = (16, 19, 24)
BORDER   = (28, 33, 41)
WHITE    = (240, 242, 245)
GREEN    = (0, 208, 132)
BLUE     = (59, 167, 255)
RED      = (255, 92, 92)
GOLD     = (240, 180, 41)
MID      = (156, 163, 175)
MUTED    = (107, 114, 128)

HERE   = os.path.dirname(os.path.abspath(__file__))
OUT    = os.path.join(HERE, "social", "cards")
AVATAR = os.path.join(HERE, "social", "itn-avatar.png")

COND = "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

_f = {}
def f(path, size):
    if (path, size) not in _f:
        _f[(path, size)] = ImageFont.truetype(path, size)
    return _f[(path, size)]


def track(d, xy, text, font, fill, spacing=6):
    """Letter-spaced text. PIL has no tracking, so step glyph by glyph."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


def track_w(d, text, font, spacing=6):
    return sum(d.textlength(c, font=font) + spacing for c in text) - spacing


def background():
    """Site background: near-black, green glow off the top left, faint grid."""
    img = Image.new("RGB", (W, H), BLACK)

    # Radial glow, built small and upscaled so the falloff stays smooth
    g = Image.new("L", (200, 113), 0)
    gd = ImageDraw.Draw(g)
    for r in range(90, 0, -2):
        gd.ellipse([28 - r, 8 - r, 28 + r, 8 + r], fill=int(150 * (1 - r / 90) ** 2))
    g = g.resize((W, H), Image.BICUBIC)
    glow = Image.new("RGB", (W, H), (0, 120, 92))
    img = Image.composite(glow, img, g.point(lambda v: min(v, 90)))

    # Grid over the lower half, as on the site
    d = ImageDraw.Draw(img)
    for x in range(0, W, 80):
        d.line([(x, int(H * 0.42)), (x, H)], fill=(19, 24, 32), width=1)
    for y in range(int(H * 0.42), H, 80):
        d.line([(0, y), (W, y)], fill=(19, 24, 32), width=1)
    return img


def panel(img, box, radius=26):
    """Rounded, bordered, top-lit panel — the site's card treatment."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGB", (x1 - x0, y1 - y0))
    ld = ImageDraw.Draw(layer)
    h = y1 - y0
    for i in range(h):                      # vertical gradient, lighter at the top
        t = i / max(h - 1, 1)
        ld.line([(0, i), (x1 - x0, i)],
                fill=tuple(int(SURF2[c] + (SURF1[c] - SURF2[c]) * t) for c in range(3)))
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius, fill=255)
    img.paste(layer, (x0, y0), mask)
    ImageDraw.Draw(img).rounded_rectangle(box, radius, outline=BORDER, width=2)


def wordmark(img, d, x, y):
    """ITN mark + INSIDE THE NUMBER, with THE in green, as in the site header."""
    try:
        av = Image.open(AVATAR).convert("RGBA").resize((58, 58), Image.LANCZOS)
        img.paste(av, (x, y), av)
    except Exception:
        pass
    fw = f(COND, 44)
    cx = x + 78
    for word, col in [("INSIDE ", WHITE), ("THE ", GREEN), ("NUMBER", WHITE)]:
        cx = track(d, (cx, y + 9), word, fw, col, spacing=2)


def card(name, label, headline, lines, accent=GREEN, label_col=None):
    """headline: list of lines; each line is a list of (text, colour) segments."""
    img = background()
    d = ImageDraw.Draw(img)

    panel(img, (60, 60, W - 60, H - 60))
    d = ImageDraw.Draw(img)

    wordmark(img, d, 110, 108)
    d.line([(110, 208), (W - 110, 208)], fill=BORDER, width=2)

    track(d, (110, 250), label.upper(), f(MONO, 26), label_col or accent, spacing=8)

    # Headline — shrink until the widest line fits
    size = 132
    while size > 54:
        fh = f(COND, size)
        widest = max(sum(d.textlength(t, font=fh) for t, _ in ln) for ln in headline)
        if widest <= W - 240:
            break
        size -= 4
    fh = f(COND, size)

    y = 310
    for ln in headline:
        x = 110
        for text, col in ln:
            d.text((x, y), text, font=fh, fill=col)
            x += d.textlength(text, font=fh)
        y += int(size * 1.02)

    y += 22
    for ln in lines:
        d.text((110, y), ln, font=f(SANS, 36), fill=MID)
        y += 52

    fm = f(MONO, 26)
    d.text((110, H - 128), "insidethenumber.com", font=fm, fill=MUTED)
    w21 = d.textlength("21+", font=fm)
    d.text((W - 110 - w21, H - 128), "21+", font=fm, fill=MUTED)

    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    img.save(p, "PNG", optimize=True)
    return p


CARDS = [
    dict(name="01-break-even.png",
         label="Break-even",
         headline=[[("-203 MEANS ", WHITE), ("67%", GREEN)]],
         lines=["A price is a hurdle, not an opinion.",
                "That bet has to win 67% of the time just to break even."]),

    dict(name="02-starter-form.png",
         label="Starter form",
         headline=[[("4.53 SEASON", WHITE)], [("1.45 ", GREEN), ("LAST THREE", WHITE)]],
         lines=["Tyler Mahle. Same pitcher, two different bets.",
                "18.2 innings, 3 earned runs, 19 strikeouts."]),

    dict(name="03-averages-lie.png",
         label="Averages lie",
         headline=[[("8.0 RUNS ", WHITE), ("OR 4.5", RED)]],
         lines=["Milwaukee went 4-1 scoring 8.0 a game.",
                "One of those was 22-0. Take it out and it's 4.5."],
         accent=RED),

    dict(name="04-what-beats-it.png",
         label="What beats it",
         headline=[[("WE PUBLISH", WHITE)], [("THE ", GREEN), ("DOWNSIDE", WHITE)]],
         lines=["Every pick carries the scenario that loses it,",
                "with the probability attached."]),

    dict(name="05-no-record.png",
         label="No record",
         headline=[[("WE DON'T", WHITE)], [("PUBLISH ", WHITE), ("ONE", GREEN)]],
         lines=["Everyone's is winning. None of them are audited.",
                "We publish the price and the math instead."]),
]

if __name__ == "__main__":
    for c in CARDS:
        print("wrote", card(**c))
