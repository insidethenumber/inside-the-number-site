#!/usr/bin/env python3
"""
Inside the Number — social cards, v2.

Why this exists: through Sep 2, 2026 every X post from @thenumberdesk was
plain text. Chuck pulled seven competitor posts that were working — Novig,
Action Network, Bet Labs, CFB Kings, trendscenter — and every single one had
an image, one or two lines of copy, and the data living in the graphic rather
than the sentence. Ours had none of that and were getting 8-36 views.

So: images by default, on everything. The rules baked in here are the ones
those posts share.

  * The graphic carries the data. The caption carries the take.
  * Team colors, not photos. Novig's best card is colour blocks and type; it
    needs no licensed imagery and no CDN fetch (the sandbox cannot reach
    ESPN's CDN anyway — team colours come down as hex in the scoreboard JSON).
  * One idea per card. A card that needs a paragraph to explain has failed.
  * Branded footer on every one, because reposts carry the mark for free.

Formats:
    board     a whole slate, sorted, with the outlier called out
    matchup   one game: two teams, the number, the projection
    bignumber one figure, huge, with the context under it
    trend     a claim plus the rows that support it

    python3 scripts/cards.py board --data slate.json --out card.png \\
        --eyebrow "COLLEGE FOOTBALL IS BACK" \\
        --headline "AND ONLY ONE GAME IS A GAME" \\
        --sub "Thursday's 11 openers, by how close the market thinks" \\
        --note "Ten of eleven are three touchdowns or worse."

Pure PIL, no network. Fonts fall back to DejaVu so this cannot fail on a
runner that lacks Poppins.
"""

import argparse, json, os, sys
from PIL import Image, ImageDraw, ImageFont

BG     = "#0b0e13"
PANEL  = "#141821"
HILITE = "#182031"
WHITE  = "#f2f4f7"
DIM    = "#c6ccd6"
MUTED  = "#8a93a0"
GREEN  = "#00d084"
BLUE   = "#3ba7ff"
AMBER  = "#ffb020"
LINE   = "#232a36"

FONT_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "assets", "fonts"),
    "/usr/share/fonts/truetype/liberation/",
    "/usr/share/fonts/truetype/google-fonts/",
    "/System/Library/Fonts/Supplemental/",
    "/usr/share/fonts/truetype/dejavu/",
]
BOLD_NAMES = ["Poppins-Bold.ttf", "BarlowCondensed-Bold.ttf", "Arial Bold.ttf",
              "DejaVuSans-Bold.ttf"]
# The loud formats need a CONDENSED display face — the difference between a
# graphic and a spreadsheet. Anton/Barlow Condensed if CI has cached them,
# otherwise Liberation Sans Narrow, which ships on every Linux box and is a
# Helvetica Narrow clone. Poppins is a last resort; it is round and soft and
# reads as a slide deck, not a scoreboard.
DISP_NAMES = ["Anton-Regular.ttf", "BarlowCondensed-Bold.ttf",
              "LiberationSansNarrow-Bold.ttf", "DejaVuSansCondensed-Bold.ttf",
              "Poppins-Bold.ttf"]
MED_NAMES  = ["Poppins-Medium.ttf", "Barlow-Medium.ttf", "Arial.ttf",
              "DejaVuSans.ttf"]


def _font(names, size):
    for n in names:
        for d in FONT_DIRS:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def B(size): return _font(BOLD_NAMES, size)
def D(size): return _font(DISP_NAMES, size)
def M(size): return _font(MED_NAMES, size)


LOGO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "logos")


def logo(league, abbr, size):
    """Cached team logo as an RGBA thumbnail, or None.

    Never fetches. scripts/fetch_logos.py populates assets/logos/ from a CI
    runner; here we only read. A missing logo is not an error — the card just
    falls back to the team's colour bar, which is why every layout still works
    on a machine with no assets at all."""
    if not league or not abbr:
        return None
    # ESPN's /teams endpoint (what fetch_logos.py reads) and the scoreboard feed
    # do not always agree on a team's abbreviation — Buffalo is BUF in one and
    # BUFF in the other, UAlbany is UALB vs ALB. Found Sep 3, 2026 when the
    # MARKET MOVERS card for UAlbany @ Buffalo silently drew colour bars instead
    # of logos. Try the exact name, then the obvious near-misses, before giving
    # up. A missing logo is still not an error; it just should be rare.
    league = str(league).lower()
    a = str(abbr).upper()
    cands = [a, a[:-1], a + "F", a + "R", a[:3], a[:4]]
    path = None
    for c in dict.fromkeys(cands):
        if not c:
            continue
        pp = os.path.join(LOGO_DIR, league, f"{c}.png")
        if os.path.exists(pp):
            path = pp
            break
    if path is None:
        return None
    try:
        im = Image.open(path).convert("RGBA")
        im.thumbnail((size, size), Image.LANCZOS)
        return im
    except Exception:
        return None


def paste_logo(img, im, x, y_center):
    """Paste centred vertically on y_center; returns the width consumed."""
    if im is None:
        return 0
    img.paste(im, (x, int(y_center - im.height / 2)), im)
    return im.width


def hexcolor(c, fallback="#444a55"):
    """ESPN gives colours as bare hex, sometimes empty, sometimes near-black."""
    if not c:
        return fallback
    c = str(c).strip().lstrip("#")
    if len(c) != 6:
        return fallback
    try:
        int(c, 16)
    except ValueError:
        return fallback
    # Pure black reads as "no colour" against our background — nudge it.
    if c.lower() in ("000000", "010101", "0b0e13"):
        return "#5a6472"
    return "#" + c


def footer(d, W, H):
    d.line([56, H - 92, W - 56, H - 92], fill=LINE, width=2)
    d.text((56, H - 70), "INSIDE THE NUMBER", font=B(26), fill=WHITE)
    d.text((330, H - 66), "insidethenumber.com", font=M(23), fill=GREEN)
    d.text((W - 150, H - 66), "21+", font=M(23), fill=MUTED)


def head(d, eyebrow, headline, sub, W):
    y = 46
    if eyebrow:
        d.text((56, y), eyebrow.upper(), font=B(30), fill=GREEN); y += 44
    if headline:
        d.text((56, y), headline.upper(), font=B(66), fill=WHITE); y += 86
    if sub:
        d.text((56, y), sub, font=M(28), fill=MUTED); y += 60
    return y


# ------------------------------------------------------------------ board
def card_board(a):
    """A slate, sorted by how close the market thinks each game is.

    rows: [{away, home, away_color, home_color, line, line_label, total}]
    The tightest game gets the highlight treatment — that contrast is the
    whole point of the card, so there is always exactly one hero row.
    """
    rows = json.load(open(a.data))
    rows.sort(key=lambda r: abs(float(r["line"])))
    n = len(rows)
    RH = 88
    W = 1200
    H = 236 + n * RH + 190
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    head(d, a.eyebrow, a.headline, a.sub, W)

    y = 236
    for i, r in enumerate(rows):
        line = float(r["line"])
        hero = (i == 0)
        d.rounded_rectangle([56, y, W - 56, y + RH - 12], 10,
                            fill=HILITE if hero else PANEL)
        d.rounded_rectangle([56, y, 64, y + RH - 12], 4,
                            fill=hexcolor(r.get("home_color")))
        tx = 86
        la = logo(r.get("league"), r.get("away_abbr"), 46)
        lh = logo(r.get("league"), r.get("home_abbr"), 46)
        if la or lh:
            cy = y + (RH - 12) / 2
            tx += paste_logo(img, la, tx, cy) + 8
            tx += paste_logo(img, lh, tx, cy) + 14
        d.text((tx, y + 16), r["away"], font=B(30), fill=WHITE if hero else DIM)
        d.text((tx, y + 50), f"at {r['home']}", font=M(23), fill=MUTED)

        col = GREEN if hero else (AMBER if abs(line) < 25 else "#6b7280")
        d.text((W - 430, y + 26), r["line_label"], font=B(36), fill=col)
        if r.get("total"):
            d.text((W - 150, y + 30), f"O/U {r['total']}", font=M(26), fill=MUTED)
        if hero and a.hero_label:
            d.text((W - 430, y + 2), a.hero_label.upper(), font=B(15), fill=GREEN)
        y += RH

    if a.note:
        d.text((56, y + 18), a.note, font=B(30), fill=WHITE)
    if a.note2:
        d.text((56, y + 60), a.note2, font=M(24), fill=MUTED)
    footer(d, W, H)
    return img


# ---------------------------------------------------------------- matchup
def card_matchup(a):
    """One game. Two colour blocks, the number, and the projection."""
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    head(d, a.eyebrow, None, None, W)

    ac, hc = hexcolor(a.away_color), hexcolor(a.home_color)
    top, bh = 130, 150
    for idx, (name, col, sub, abbr) in enumerate(
            [(a.away, ac, a.away_sub, a.away_abbr),
             (a.home, hc, a.home_sub, a.home_abbr)]):
        yy = top + idx * (bh + 16)
        d.rounded_rectangle([56, yy, W - 56, yy + bh], 12, fill=PANEL)
        d.rounded_rectangle([56, yy, 74, yy + bh], 6, fill=col)
        tx = 104
        lg = logo(a.league, abbr, 108)
        if lg:
            tx += paste_logo(img, lg, tx, yy + bh / 2) + 24
        d.text((tx, yy + 34), name, font=B(52), fill=WHITE)
        if sub:
            d.text((tx, yy + 98), sub, font=M(24), fill=MUTED)

    if a.number:
        d.text((W - 470, top + 44), a.number, font=B(78), fill=GREEN)
    if a.number_sub:
        d.text((W - 470, top + 140), a.number_sub, font=M(26), fill=MUTED)

    yy = top + 2 * (bh + 16) + 24
    if a.note:
        d.text((56, yy), a.note, font=B(30), fill=WHITE)
    if a.note2:
        d.text((56, yy + 44), a.note2, font=M(24), fill=MUTED)
    footer(d, W, H)
    return img


# -------------------------------------------------------------- bignumber
def card_bignumber(a):
    """One figure, as large as it will go, with the context beneath."""
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    if a.eyebrow:
        d.text((56, 56), a.eyebrow.upper(), font=B(30), fill=GREEN)
    d.text((56, 130), a.number, font=B(230), fill=GREEN)
    if a.headline:
        d.text((56, 400), a.headline, font=B(50), fill=WHITE)
    if a.sub:
        d.text((56, 470), a.sub, font=M(28), fill=MUTED)
    if a.note:
        d.text((56, 520), a.note, font=M(28), fill=MUTED)
    footer(d, W, H)
    return img


# ------------------------------------------------------------------ trend
def card_trend(a):
    """A claim, then the rows that back it.  rows: [{label, value}]"""
    rows = json.load(open(a.data))
    W = 1200
    RH = 78
    H = 250 + len(rows) * RH + 160
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    head(d, a.eyebrow, a.headline, a.sub, W)
    y = 250
    for r in rows:
        d.rounded_rectangle([56, y, W - 56, y + RH - 12], 10, fill=PANEL)
        d.text((86, y + 18), r["label"], font=M(30), fill=DIM)
        col = GREEN if r.get("good") else (AMBER if r.get("warn") else WHITE)
        d.text((W - 380, y + 12), str(r["value"]), font=B(40), fill=col)
        y += RH
    if a.note:
        d.text((56, y + 16), a.note, font=B(28), fill=WHITE)
    footer(d, W, H)
    return img



# ------------------------------------------------------------------ split
def card_split(a):
    """The loud one. Two saturated blocks, one number each, read in a glance.

    Modelled directly on what actually works in our own timeline — Bracco's
    green/red "did your team go undefeated" card, Big Bet Co's single glowing
    price. The lesson from scrolling the feed on Sep 2 2026: at thumbnail size
    nobody reads a table. Five words of huge type beat sixty words of small
    type every time. So this format refuses to carry more than a headline, two
    numbers and a kicker.
    """
    W, H = 1200, 1004
    BLUE_BANNER = "#1d9bf0"
    L, R = "#00c46a", "#e0263c"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    def ctr(box, txt, font, fill):
        if not txt:
            return
        x0, y0, x1, y1 = box
        w = d.textlength(txt, font=font)
        bb = font.getbbox(txt)
        d.text(((x0 + x1 - w) / 2, (y0 + y1 - (bb[3] - bb[1])) / 2 - bb[1]),
               txt, font=font, fill=fill)

    d.rounded_rectangle([48, 44, W - 48, 168], 16, fill=BLUE_BANNER)
    ctr((48, 44, W - 48, 168), (a.headline or "").upper(), D(54), "#ffffff")

    gap, top, bh = 24, 196, 560
    bw = (W - 96 - gap) // 2
    d.rounded_rectangle([48, top, 48 + bw, top + bh], 18, fill=L)
    d.rounded_rectangle([48 + bw + gap, top, W - 48, top + bh], 18, fill=R)

    for x0, x1, big, lab, l1, l2, l3, ink in [
        (48, 48 + bw, a.left_number, a.left_label, a.left_line1,
         a.left_line2, a.left_line3, BG),
        (48 + bw + gap, W - 48, a.right_number, a.right_label, a.right_line1,
         a.right_line2, a.right_line3, "#ffffff"),
    ]:
        ctr((x0, top + 40, x1, top + 300), big or "", D(300), ink)
        ctr((x0, top + 300, x1, top + 372), (lab or "").upper(), D(68), ink)
        ctr((x0, top + 380, x1, top + 430), (l1 or "").upper(), D(38), ink)
        ctr((x0, top + 430, x1, top + 486), (l2 or "").upper(), D(64), ink)
        ctr((x0, top + 486, x1, top + 536), (l3 or "").upper(), D(32), ink)

    y = top + bh + 28
    d.rounded_rectangle([48, y, W - 48, y + 120], 16, fill=PANEL)
    ctr((48, y, W - 48, y + 64), (a.note or "").upper(), D(60), WHITE)
    ctr((48, y + 60, W - 48, y + 112), a.note2 or "", M(26), "#9aa3b0")

    d.text((52, H - 58), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((372, H - 54), "insidethenumber.com", font=M(25), fill=GREEN)
    d.text((W - 108, H - 54), "21+", font=M(25), fill=MUTED)
    return img


FORMATS = {"split": card_split, "board": card_board, "matchup": card_matchup,
           "bignumber": card_bignumber, "trend": card_trend}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("format", choices=sorted(FORMATS))
    p.add_argument("--out", required=True)
    p.add_argument("--data", help="JSON rows for board/trend")
    p.add_argument("--eyebrow"); p.add_argument("--headline")
    p.add_argument("--sub"); p.add_argument("--note"); p.add_argument("--note2")
    p.add_argument("--hero-label", default="")
    p.add_argument("--away"); p.add_argument("--home")
    p.add_argument("--away-color"); p.add_argument("--home-color")
    p.add_argument("--away-sub"); p.add_argument("--home-sub")
    p.add_argument("--number"); p.add_argument("--number-sub")
    p.add_argument("--league", help="MLB/NFL/CFB/NBA/NHL/CBB — enables logos")
    for side in ("left", "right"):
        p.add_argument(f"--{side}-number"); p.add_argument(f"--{side}-label")
        p.add_argument(f"--{side}-line1"); p.add_argument(f"--{side}-line2")
        p.add_argument(f"--{side}-line3")
    p.add_argument("--away-abbr"); p.add_argument("--home-abbr")
    a = p.parse_args()

    if a.format in ("board", "trend") and not a.data:
        sys.exit(f"{a.format} needs --data")
    img = FORMATS[a.format](a)
    img.save(a.out)
    print(f"wrote {a.out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
