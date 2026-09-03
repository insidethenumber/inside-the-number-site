#!/usr/bin/env python3
"""Photo-backed X graphics: real imagery under real numbers.

Built Sep 3, 2026. The gap Chuck kept pointing at was photography — every
format we had was type on a flat colour, because nothing in this environment
generates a picture. The fix is a division of labour:

  Gemini (Chuck's Pro account, driven in Chrome) makes the HERO IMAGE.
  This script lays OUR data, brand and typography over it.

That keeps the thing that matters: the imagery is as good as Gemini's, and
every number on the card came off a live feed the same day. Gemini's own
mockups carried invented stats — that is the one thing we do not copy.

Backgrounds live in assets/heroes/. Add new ones by generating in Gemini and
dropping the file in; nothing here is hard-coded to a specific image.

Layouts:
  band    Photo with a bottom scrim: eyebrow, big headline, number, footer.
          The workhorse — reads at thumbnail size, works on any photo.
  left    Photo dimmed, copy stacked on the left third, number huge under it.
          For images with a busy right side.
  stamp   Photo full-bleed, one enormous number centred with a soft shadow,
          caption under. For the single-number posts.
  split   Photo top half, solid brand panel bottom half with the data.
          Most "designed" of the four; good for two numbers side by side.

Usage:
  python3 scripts/hero.py band --bg assets/heroes/x.jpg --out o.jpg \
      --franchise "THE BOARD" --eyebrow "Thursday - CFB Week 1" \
      --headline "One game tonight|is inside a touchdown." \
      --number "GT -6.5" --note "Colorado +195 - total 50.5" --link
"""
import argparse, os, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards import WHITE, DIM, MUTED, GREEN, B, D, M, logo
from franchise import FR, ctr, fit, wrap

W, H = 1600, 900
INK = "#07090d"


def load_bg(path, w=W, h=H):
    """Cover-fit the photo to the canvas."""
    im = Image.open(path).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def scrim(img, frm=0.42, strength=0.94, top=False):
    """Vertical black gradient so type always has contrast. Without this,
    white text over a bright crowd is unreadable — the single most common way
    photo-backed social graphics fail."""
    g = Image.new("L", (1, H))
    px = g.load()
    for y in range(H):
        t = y / H
        if top:
            v = max(0.0, (frm - t) / max(frm, 1e-6))
        else:
            v = max(0.0, (t - frm) / max(1 - frm, 1e-6))
        px[0, y] = int(255 * min(1.0, v ** 1.25 * strength))
    g = g.resize((W, H))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(black, img, g.point(lambda v: 255 - v)) if False else \
        Image.composite(black, img, g)


def veil(img, amount=0.35):
    black = Image.new("RGB", img.size, (0, 0, 0))
    return Image.blend(img, black, amount)


def chip(d, name, x=56, y=52):
    """Franchise tag, same position on every photo card."""
    if not name:
        return
    col = FR.get(name.upper(), GREEN)
    f = D(38)
    w = d.textlength(name.upper(), font=f) + 52
    d.rounded_rectangle([x, y, x + w, y + 62], 12, fill=col)
    ctr(d, (x, y, x + w, y + 62), name.upper(), f, INK)


def foot(img, d, link=False):
    d.text((56, H - 66), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((380, H - 62), "insidethenumber.com", font=M(26), fill=GREEN)
    t = "@thenumberdesk"
    d.text((W - 56 - d.textlength(t, font=M(26)), H - 62), t, font=M(26), fill="#c6ccd6")
    if link:
        d.text((56, H - 108), "FULL BOARD AND THE LIVE NUMBER →", font=D(30), fill=GREEN)


def marks(img, league, away, home, x, y, size=118):
    for abbr in (away, home):
        im = logo(league, abbr, size) if league else None
        if im is not None:
            img.paste(im, (int(x), int(y - im.height / 2)), im)
            x += im.width + 18
    return x


def headline(d, text, y, maxsize=104, color=WHITE, x=56, maxw=None):
    maxw = maxw or (W - 112)
    for ln in (text or "").split("|"):
        ln = ln.strip()
        if not ln:
            continue
        f = fit(d, ln.upper(), D, maxw, maxsize, 40)
        d.text((x, y), ln.upper(), font=f, fill=color)
        y += f.size + 10
    return y


# ------------------------------------------------------------------- layouts
def l_band(a):
    img = scrim(load_bg(a.bg), frm=0.34, strength=0.96)
    img = scrim(img, frm=0.30, strength=0.55, top=True)
    d = ImageDraw.Draw(img)
    chip(d, a.franchise)
    if a.eyebrow:
        d.text((56, 132), a.eyebrow.upper(), font=D(34), fill="#c6ccd6")
    y = 356
    y = headline(d, a.headline, y, 96)
    if a.number:
        f = fit(d, a.number, D, W - 112, 150, 70)
        d.text((56, y + 12), a.number, font=f, fill=FR.get((a.franchise or "").upper(), GREEN))
        y += f.size + 16
    if a.note:
        d.text((58, y + 4), a.note.upper(), font=D(36), fill="#c6ccd6")
    if a.league:
        marks(img, a.league, a.away_abbr, a.home_abbr, W - 320, 116, 118)
    foot(img, d, a.link)
    return img


def l_left(a):
    img = veil(load_bg(a.bg), 0.32)
    img = scrim(img, frm=0.0, strength=0.72, top=True)
    d = ImageDraw.Draw(img)
    chip(d, a.franchise)
    if a.eyebrow:
        d.text((56, 132), a.eyebrow.upper(), font=D(34), fill="#c6ccd6")
    y = headline(d, a.headline, 214, 78, maxw=760)
    note_lines = wrap(d, a.note, M(30), 700)[:3] if a.note else []
    BOT = H - 130
    note_block = len(note_lines) * 40
    if a.number:
        # Reserve the note's space FIRST, then give the number whatever is left.
        avail = BOT - note_block - y - 40
        f = fit(d, a.number, D, 760, max(64, min(170, int(avail))), 56)
        d.text((52, y + 16), a.number, font=f,
               fill=FR.get((a.franchise or "").upper(), GREEN))
        y += f.size + 30
    y = max(y, BOT - note_block)
    for ln in note_lines:
        d.text((58, y), ln, font=M(30), fill="#c6ccd6")
        y += 40
    if a.league:
        marks(img, a.league, a.away_abbr, a.home_abbr, W - 300, H - 220, 130)
    foot(img, d, a.link)
    return img


def l_stamp(a):
    img = veil(load_bg(a.bg), 0.46)
    d = ImageDraw.Draw(img)
    chip(d, a.franchise)
    if a.eyebrow:
        d.text((56, 132), a.eyebrow.upper(), font=D(34), fill="#c6ccd6")
    # soft shadow behind the number so it survives any background
    n = a.number or ""
    f = fit(d, n, D, W - 160, 400, 120)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    bb = f.getbbox(n)
    tw = ds.textlength(n, font=f)
    x = (W - tw) / 2
    y = (H - (bb[3] - bb[1])) / 2 - bb[1] - 40
    ds.text((x, y), n, font=f, fill=(0, 0, 0, 210))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((x, y), n, font=f, fill=FR.get((a.franchise or "").upper(), GREEN))
    if a.headline:
        headline(d, a.headline, y + f.size + 24, 62, WHITE, 56)
    if a.note:
        d.text((56, H - 150), a.note.upper(), font=D(34), fill="#c6ccd6")
    foot(img, d, a.link)
    return img


def l_split(a):
    top = load_bg(a.bg, W, 470)
    img = Image.new("RGB", (W, H), INK)
    img.paste(top, (0, 0))
    g = Image.new("L", (1, 120), 0)
    px = g.load()
    for i in range(120):
        px[0, i] = int(255 * (i / 120))
    g = g.resize((W, 120))
    img.paste(Image.new("RGB", (W, 120), INK), (0, 350), g)
    d = ImageDraw.Draw(img)
    chip(d, a.franchise)
    if a.eyebrow:
        d.text((56, 132), a.eyebrow.upper(), font=D(34), fill="#f2f4f7")
    col = FR.get((a.franchise or "").upper(), GREEN)

    # Budget the panel. The panel runs 500 -> H-120 (the footer's zone). Fit the
    # headline, the number and the note INTO that box rather than assuming they
    # fit — Sep 3: a two-line headline plus a 180pt number ran straight off the
    # bottom of the canvas and over the footer.
    TOP, BOT = 496, H - 122
    lines = [l.strip() for l in (a.headline or "").split("|") if l.strip()]
    note_h = 44 if a.note else 0
    hsize = 74
    while hsize > 34:
        nsize = min(150, int((BOT - TOP - len(lines) * (hsize + 10) - note_h) * 0.92))
        if nsize >= 78 or not a.number:
            break
        hsize -= 4
    y = TOP
    for ln in lines:
        f = fit(d, ln.upper(), D, W - 112, hsize, 32)
        d.text((56, y), ln.upper(), font=f, fill=WHITE)
        y += f.size + 10
    if a.number:
        avail = BOT - note_h - y - 8
        f = fit(d, a.number, D, W - 112, max(70, min(150, int(avail))), 60)
        d.text((56, y + 6), a.number, font=f, fill=col)
        y += f.size + 12
    if a.note:
        d.text((58, min(y, BOT - 40)), a.note.upper(), font=D(32), fill="#c6ccd6")
    if a.league:
        marks(img, a.league, a.away_abbr, a.home_abbr, W - 320, 560, 130)
    foot(img, d, a.link)
    return img


LAYOUTS = {"band": l_band, "left": l_left, "stamp": l_stamp, "split": l_split}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("layout", choices=sorted(LAYOUTS))
    p.add_argument("--bg", required=True, help="hero photo (assets/heroes/...)")
    p.add_argument("--out", required=True)
    p.add_argument("--franchise"); p.add_argument("--eyebrow")
    p.add_argument("--headline"); p.add_argument("--number"); p.add_argument("--note")
    p.add_argument("--league"); p.add_argument("--away-abbr"); p.add_argument("--home-abbr")
    p.add_argument("--link", action="store_true",
                   help="add the 'full board' call to action (about 1 post in 4)")
    a = p.parse_args()
    img = LAYOUTS[a.layout](a)
    img.save(a.out, quality=93)
    print(f"wrote {a.out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
