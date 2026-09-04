#!/usr/bin/env python3
"""
Parlay of the Day — ten formats, one file.

Built Fri Sep 4, 2026 after Chuck killed the first attempt ("that is garbage").
He was right: it was the same dark rectangle with a big amber number that every
other card is, and a parlay is the one product that has a NATIVE visual object
— the slip. People screenshot slips. Nobody screenshots a title card.

So the ten here are ten different KINDS of object, not ten colourways:

  slip      a betslip. Legs, prices, payout. The thing itself.
  stub      a torn ticket stub, perforation and all.
  math      the multiplication shown: 1.87 x 1.84 x 1.96 = 6.75.
  dots      100 dots, 15 lit. What 14.8% actually looks like.
  bars      needed-to-break-even vs three coin flips, as two bars.
  trip      a triptych: one colour panel per leg.
  bug       a broadcast lower-third, the way a score bug looks.
  square    1080x1080 for the square crop, three marks and a price.
  texts     the joke: a message thread about parlays.
  poster    the loud one — huge price, team marks, one line.

Every number is passed in. Nothing is computed from memory, nothing is
hard-coded to a date. --demo renders all ten with the day's parlay.

  python3 scripts/parlay_cards.py --out-dir /tmp/parlay --spec parlay.json
  python3 scripts/parlay_cards.py --out-dir /tmp/parlay --demo
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards import BG, PANEL, WHITE, DIM, MUTED, GREEN, AMBER, LINE, B, D, M, logo
from franchise import ctr, fit, wrap

INK   = "#07090d"
CARD  = "#12161f"
RED   = "#ff4d4d"
PAPER = "#f4f1ea"


# ---------------------------------------------------------------- utilities
def new(W, H, bg=INK):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def grain(img, amount=6):
    """Film grain. Flat black reads as a slide; noise reads as print."""
    import random
    px = img.load()
    W, H = img.size
    rnd = random.Random(7)
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            n = rnd.randint(-amount, amount)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)),
                        max(0, min(255, b + n)))
    return img


def paste_c(img, im, cx, cy):
    if im is not None:
        img.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)


def plate(d, cx, cy, r, fill="#ffffff"):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def mark(img, d, leg, cx, cy, size=96, disc=True):
    """Team logo on a white disc so dark marks survive a dark card."""
    im = logo(leg.get("league", "cfb"), leg["abbr"], size)
    if disc:
        plate(d, cx, cy, int(size * 0.62))
    if im is not None:
        paste_c(img, im, cx, cy)
    else:
        ctr(d, (cx - size, cy - size, cx + size, cy + size), leg["abbr"],
            D(int(size * 0.5)), INK if disc else WHITE)


def foot(d, W, H, right="@thenumberdesk"):
    d.line([56, H - 92, W - 56, H - 92], fill=LINE, width=2)
    d.text((56, H - 72), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((360, H - 68), "insidethenumber.com", font=M(24), fill=GREEN)
    w = d.textlength(right, font=M(24))
    d.text((W - 56 - w, H - 68), right, font=M(24), fill=MUTED)


def eyebrow(d, x, y, txt, col=AMBER, size=30):
    d.text((x, y), txt, font=B(size), fill=col)


# ------------------------------------------------------------------- 1 slip
def f_slip(s, out):
    """The object itself. Legs stacked like a slip, payout at the bottom."""
    W, H = 1600, 900
    img, d = new(W, H)
    d.rounded_rectangle([70, 60, W - 70, H - 60], 26, fill=CARD, outline=LINE,
                        width=2)

    eyebrow(d, 110, 104, "PARLAY OF THE DAY", AMBER, 30)
    d.text((110, 146), s["date_line"].upper(), font=M(26), fill=MUTED)
    d.text((W - 110 - d.textlength(str(len(s["legs"])) + " LEGS", font=B(30)),
            108), f"{len(s['legs'])} LEGS", font=B(30), fill=DIM)

    y = 206
    for leg in s["legs"]:
        d.rounded_rectangle([110, y, W - 110, y + 132], 16, fill="#171c27")
        mark(img, d, leg, 186, y + 66, 80)
        d.text((262, y + 26), leg["pick"], font=D(54), fill=WHITE)
        d.text((264, y + 88), leg["note"], font=M(24), fill=MUTED)
        pr = leg["price"]
        pw = d.textlength(pr, font=D(54))
        d.text((W - 150 - pw, y + 26), pr, font=D(54), fill=DIM)
        be = leg["be"] + " to break even"
        d.text((W - 150 - d.textlength(be, font=M(23)), y + 92), be,
               font=M(23), fill=MUTED)
        y += 148

    d.line([110, y + 4, W - 110, y + 4], fill=LINE, width=2)
    d.text((110, y + 44), "PAYOUT", font=B(34), fill=MUTED)
    d.text((110, y + 90), f"{s['be']} to break even  ·  three coin flips hit "
                          f"{s['coin']}", font=M(24), fill=MUTED)
    pw = d.textlength(s["price"], font=D(92))
    d.text((W - 110 - pw, y + 24), s["price"], font=D(92), fill=GREEN)
    foot(d, W, H)
    grain(img)
    img.save(out)


# ------------------------------------------------------------------- 2 stub
def f_stub(s, out):
    """A torn ticket. Paper stock, perforation, everything off-black."""
    W, H = 1600, 900
    img, d = new(W, H, "#0a0c11")
    x0, y0, x1, y1 = 120, 130, W - 120, H - 130
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=PAPER)

    # perforation: a dotted seam two-thirds across, plus two bite marks
    seam = x0 + int((x1 - x0) * 0.66)
    for yy in range(y0 + 26, y1 - 26, 26):
        d.line([seam, yy, seam, yy + 13], fill="#c9c3b6", width=3)
    d.ellipse([seam - 22, y0 - 22, seam + 22, y0 + 22], fill="#0a0c11")
    d.ellipse([seam - 22, y1 - 22, seam + 22, y1 + 22], fill="#0a0c11")

    d.text((x0 + 46, y0 + 40), "INSIDE THE NUMBER", font=B(28), fill="#8b8578")
    d.text((x0 + 46, y0 + 82), "PARLAY OF THE DAY", font=D(72), fill=INK)
    d.text((x0 + 48, y0 + 168), s["date_line"].upper(), font=M(26),
           fill="#8b8578")

    y = y0 + 230
    for leg in s["legs"]:
        d.text((x0 + 46, y), leg["pick"], font=D(50), fill=INK)
        pw = d.textlength(leg["price"], font=D(50))
        d.text((seam - 60 - pw, y), leg["price"], font=D(50), fill="#5c5648")
        y += 78
    d.line([x0 + 46, y + 6, seam - 60, y + 6], fill="#c9c3b6", width=2)
    for k, line in enumerate(wrap(d, s["hook"], M(26), seam - x0 - 110)[:2]):
        d.text((x0 + 46, y + 26 + k * 36), line, font=M(26), fill="#5c5648")

    # stub side
    cx = (seam + x1) // 2
    ctr(d, (seam, y0 + 120, x1, y0 + 190), "PAYS", B(32), "#8b8578")
    f = fit(d, s["price"], D, (x1 - seam) - 60, 150, 80)
    ctr(d, (seam, y0 + 170, x1, y0 + 330), s["price"], f, INK)
    ctr(d, (seam, y0 + 350, x1, y0 + 400), s["be"] + " TO BREAK EVEN", B(26),
        "#8b8578")
    n = len(s["legs"])
    for i, leg in enumerate(s["legs"]):
        mark(img, d, leg, seam + (x1 - seam) * (i + 0.5) / n, y1 - 130, 84,
             disc=False)
    ctr(d, (seam, y1 - 74, x1, y1 - 40), "insidethenumber.com", M(24),
        "#8b8578")
    img.save(out)


# ------------------------------------------------------------------- 3 math
def f_math(s, out):
    """Show the multiplication. Nobody else posts the actual arithmetic."""
    W, H = 1600, 900
    img, d = new(W, H)
    eyebrow(d, 70, 70, "PARLAY OF THE DAY  ·  THE ARITHMETIC")

    n = len(s["legs"])
    span = W - 260
    slot = span / n
    y = 300
    for i, leg in enumerate(s["legs"]):
        cx = 130 + slot * (i + 0.5)
        mark(img, d, leg, cx, y - 88, 92)
        ctr(d, (cx - slot / 2, y, cx + slot / 2, y + 90), leg["decimal"],
            D(104), WHITE)
        ctr(d, (cx - slot / 2, y + 100, cx + slot / 2, y + 140), leg["pick"],
            M(26), MUTED)
        if i < n - 1:
            d.text((130 + slot * (i + 1) - 20, y + 10), "x", font=D(78),
                   fill=AMBER)

    d.line([130, y + 200, W - 130, y + 200], fill=LINE, width=2)
    d.text((130, y + 230), "=", font=D(96), fill=AMBER)
    d.text((240, y + 226), s["decimal"], font=D(104), fill=WHITE)
    tail = f"{s['price']}  ·  hits {s['be']} of the time or you lose money"
    d.text((240, y + 348), tail, font=M(30), fill=GREEN)
    foot(d, W, H)
    grain(img)
    img.save(out)


# ------------------------------------------------------------------- 4 dots
def f_dots(s, out):
    """100 dots, N lit. The only honest picture of a long price."""
    W, H = 1600, 900
    img, d = new(W, H)
    eyebrow(d, 70, 70, "PARLAY OF THE DAY")
    d.text((70, 118), f"{s['price']} pays like a longshot because it is one",
           font=D(64), fill=WHITE)

    lit = int(round(float(s["be"].rstrip("%"))))
    x0, y0, gap, r = 70, 250, 62, 20
    for i in range(100):
        cx = x0 + (i % 20) * gap + r
        cy = y0 + (i // 20) * gap + r
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=GREEN if i < lit else "#1b2130")

    d.text((70, y0 + 5 * gap + 40),
           f"{s['be']} of the time this cashes. That is what has to happen "
           f"just to break even.", font=M(32), fill=DIM)
    d.text((70, y0 + 5 * gap + 92),
           f"Three coin flips land {s['coin']} of the time. The gap is the "
           f"price of stapling them together.", font=M(32), fill=MUTED)
    foot(d, W, H)
    img.save(out)


# ------------------------------------------------------------------- 5 bars
def f_bars(s, out):
    """Two bars: what it needs, what three coin flips give you."""
    W, H = 1600, 900
    img, d = new(W, H)
    eyebrow(d, 70, 70, "PARLAY OF THE DAY  ·  PRICED HONESTLY")

    need = float(s["be"].rstrip("%"))
    coin = float(s["coin"].rstrip("%"))
    top, full = 236, W - 560
    for i, (lab, val, col) in enumerate(
            [("NEEDS TO HIT", need, AMBER), ("THREE COIN FLIPS", coin, "#38455c")]):
        y = top + i * 180
        w = int(full * val / max(need, coin))
        d.rounded_rectangle([300, y, 300 + w, y + 112], 10, fill=col)
        d.text((70, y + 32), lab, font=B(30), fill=MUTED)
        d.text((320 + w, y + 18), f"{val:g}%", font=D(76),
               fill=WHITE if i == 0 else DIM)

    y = top + 400
    f = fit(d, s["hook"], D, W - 140, 56, 34)
    for k, line in enumerate(wrap(d, s["hook"], f, W - 140)[:2]):
        d.text((70, y + k * 66), line, font=f, fill=WHITE)
        y_end = y + k * 66
    d.text((70, y_end + 84), s["legs_line"] + f"   {s['price']}", font=M(32),
           fill=GREEN)
    foot(d, W, H)
    grain(img)
    img.save(out)


# ------------------------------------------------------------------- 6 trip
def f_trip(s, out):
    """One colour panel per leg. Team colour does the design work."""
    W, H = 1600, 900
    img, d = new(W, H)
    n = len(s["legs"])
    pw = W / n
    for i, leg in enumerate(s["legs"]):
        x0 = int(pw * i)
        x1 = int(pw * (i + 1))
        d.rectangle([x0, 0, x1, H - 150], fill=leg.get("color", PANEL))
        d.rectangle([x0, 0, x0 + 3, H - 150], fill=INK)
        mark(img, d, leg, (x0 + x1) / 2, 210, 128)
        f = fit(d, leg["pick"], D, (x1 - x0) - 70, 76, 40)
        ctr(d, (x0, 330, x1, 410), leg["pick"], f, "#ffffff")
        ctr(d, (x0, 420, x1, 470), leg["price"], B(40), "#ffffff")
        for k, line in enumerate(wrap(d, leg["note"], M(24), (x1 - x0) - 90)[:3]):
            ctr(d, (x0, 500 + k * 34, x1, 534 + k * 34), line, M(24), "#e8ecf3")
        ctr(d, (x0, 640, x1, 686), leg["be"] + " to break even", M(24),
            "#dbe2ec")

    d.rectangle([0, H - 150, W, H], fill=INK)
    d.text((56, H - 120), "ALL THREE", font=B(34), fill=MUTED)
    d.text((56, H - 78), s["price"], font=D(64), fill=GREEN)
    tail = f"{s['be']} to break even  ·  three coin flips hit {s['coin']}"
    d.text((W - 56 - d.textlength(tail, font=M(28)), H - 96), tail, font=M(28),
           fill=DIM)
    img.save(out)


# -------------------------------------------------------------------- 7 bug
def f_bug(s, out):
    """Broadcast lower-third. Reads as television, not as an infographic."""
    W, H = 1600, 900
    img, d = new(W, H)
    for y in range(H):                     # subtle vertical falloff
        v = int(7 + 10 * (y / H))
        d.line([0, y, W, y], fill=(v, v + 2, v + 6))

    d.text((56, 70), s["hook"], font=D(54), fill=WHITE)
    d.text((58, 146), f"{s['be']} to break even  ·  three coin flips hit "
                      f"{s['coin']}", font=M(30), fill=MUTED)

    bar_y = 230
    d.rectangle([0, bar_y, W, bar_y + 96], fill="#101623")
    d.rectangle([0, bar_y, 16, bar_y + 96], fill=AMBER)
    d.text((52, bar_y + 24), "PARLAY OF THE DAY", font=B(44), fill=WHITE)
    d.text((W - 300, bar_y + 28), s["date_line"].upper(), font=M(26),
           fill=MUTED)

    y = bar_y + 128
    for i, leg in enumerate(s["legs"]):
        d.rectangle([0, y, W, y + 96], fill="#161c29" if i % 2 == 0 else "#131926")
        d.rectangle([0, y, 16, y + 96], fill=leg.get("color", PANEL))
        mark(img, d, leg, 78, y + 48, 62)
        d.text((136, y + 24), leg["pick"], font=D(50), fill=WHITE)
        d.text((640, y + 32), leg["note"], font=M(24), fill=MUTED)
        pw = d.textlength(leg["price"], font=D(50))
        d.text((W - 60 - pw, y + 24), leg["price"], font=D(50), fill=DIM)
        y += 100

    d.rectangle([0, y, W, y + 104], fill=GREEN)
    d.text((52, y + 26), "PAYS", font=B(44), fill=INK)
    pw = d.textlength(s["price"], font=D(72))
    d.text((W - 60 - pw, y + 16), s["price"], font=D(72), fill=INK)
    d.text((52, H - 80), "insidethenumber.com  ·  @thenumberdesk", font=M(26),
           fill=MUTED)
    img.save(out)


# ----------------------------------------------------------------- 8 square
def f_square(s, out):
    """1080 square for the crop that phones actually show."""
    W = H = 1080
    img, d = new(W, H)
    d.rounded_rectangle([40, 40, W - 40, H - 40], 28, outline=LINE, width=2)
    ctr(d, (0, 96, W, 140), "PARLAY OF THE DAY", B(32), AMBER)

    n = len(s["legs"])
    for i, leg in enumerate(s["legs"]):
        cx = W * (i + 0.5) / n
        mark(img, d, leg, cx, 250, 118)
        ctr(d, (cx - W / (2 * n), 336, cx + W / (2 * n), 380), leg["pick"],
            B(30), WHITE)

    f = fit(d, s["price"], D, W - 200, 300, 140)
    ctr(d, (0, 420, W, 660), s["price"], f, GREEN)
    ctr(d, (0, 690, W, 736), f"{s['be']} TO BREAK EVEN", B(34), DIM)
    ctr(d, (0, 744, W, 786), f"THREE COIN FLIPS HIT {s['coin']}", B(30), MUTED)
    for k, line in enumerate(wrap(d, s["hook"], M(30), W - 200)[:2]):
        ctr(d, (0, 850 + k * 44, W, 894 + k * 44), line, M(30), DIM)
    ctr(d, (0, H - 110, W, H - 70), "insidethenumber.com", B(30), WHITE)
    grain(img)
    img.save(out)


# ------------------------------------------------------------------ 9 texts
def f_texts(s, out):
    """The joke format. Screenshotted more than any card we make."""
    W, H = 1600, 900
    img, d = new(W, H, "#0d1117")
    px0, px1, pbot = 380, W - 380, H - 120
    d.rounded_rectangle([px0, 24, px1, pbot], 38, fill="#000000",
                        outline="#232a36", width=3)
    d.rounded_rectangle([px0 + 150, 50, px1 - 150, 80], 15, fill="#0d1117")
    ctr(d, (px0, 94, px1, 138), s["thread_title"], B(30), MUTED)

    y = 172
    for who, txt in s["thread"]:
        me = who == "me"
        f = M(31)
        lines = wrap(d, txt, f, 470)
        bw = max(d.textlength(l, font=f) for l in lines) + 60
        bh = len(lines) * 44 + 42
        x1 = px1 - 40 if me else px0 + 40 + bw
        x0 = x1 - bw
        d.rounded_rectangle([x0, y, x1, y + bh], 22,
                            fill="#1d6fe8" if me else "#20262f")
        for k, l in enumerate(lines):
            d.text((x0 + 30, y + 20 + k * 44), l, font=f,
                   fill="#ffffff" if me else DIM)
        y += bh + 20

    d.text((px0, pbot + 26), s["price"], font=D(48), fill=GREEN)
    lw = d.textlength(s["price"], font=D(48))
    d.text((px0 + lw + 24, pbot + 40), s["legs_line"], font=M(26), fill=MUTED)
    d.text((56, pbot + 26), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((58, pbot + 64), "insidethenumber.com", font=M(24), fill=GREEN)
    img.save(out)


# ---------------------------------------------------------------- 10 poster
def f_poster(s, out):
    """The loud one. Type to the edges, marks as furniture, one line of copy."""
    W, H = 1600, 900
    img, d = new(W, H)
    d.rectangle([0, 0, W, 12], fill=AMBER)

    n = len(s["legs"])
    for i, leg in enumerate(s["legs"]):
        mark(img, d, leg, W - 140 - (n - 1 - i) * 150, 140, 112)

    f = fit(d, s["price"], D, W - 120, 400, 240)
    bb = f.getbbox(s["price"])
    top = 226
    d.text((56, top - bb[1]), s["price"], font=f, fill=WHITE)
    y = top + (bb[3] - bb[1])

    fl = fit(d, s["legs_line"].upper(), D, W - 120, 62, 36)
    d.text((62, y + 30), s["legs_line"].upper(), font=fl, fill=AMBER)
    d.text((66, y + 106), f"{s['be']} to break even. Three coin flips hit "
                          f"{s['coin']}.", font=M(30), fill=DIM)
    foot(d, W, H)
    grain(img, 8)
    img.save(out)


FORMATS = {
    "slip": f_slip, "stub": f_stub, "math": f_math, "dots": f_dots,
    "bars": f_bars, "trip": f_trip, "bug": f_bug, "square": f_square,
    "texts": f_texts, "poster": f_poster,
}


def contact_sheet(paths, out, cols=3, cell=760):
    ims = []
    for p in paths:
        im = Image.open(p)
        r = min(cell / im.width, cell / im.height)
        ims.append(im.resize((int(im.width * r), int(im.height * r))))
    rows = (len(ims) + cols - 1) // cols
    pad = 24
    W = cols * cell + pad * (cols + 1)
    H = rows * cell + pad * (rows + 1)
    sheet = Image.new("RGB", (W, H), "#05070a")
    for i, im in enumerate(ims):
        cx = pad + (i % cols) * (cell + pad) + (cell - im.width) // 2
        cy = pad + (i // cols) * (cell + pad) + (cell - im.height) // 2
        sheet.paste(im, (cx, cy))
    sheet.save(out, quality=92)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--spec", help="JSON spec; omit with --demo")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--only", help="comma list of formats")
    a = ap.parse_args()

    if a.spec:
        s = json.load(open(a.spec))
    elif a.demo:
        s = DEMO
    else:
        ap.error("need --spec or --demo")

    os.makedirs(a.out_dir, exist_ok=True)
    names = (a.only.split(",") if a.only else list(FORMATS))
    made = []
    for i, name in enumerate(names, 1):
        out = os.path.join(a.out_dir, f"{i:02d}-{name}.png")
        FORMATS[name](s, out)
        made.append(out)
        print("wrote", out)
    sheet = os.path.join(a.out_dir, "00-CONTACT-SHEET.jpg")
    contact_sheet(made, sheet)
    print("wrote", sheet)


DEMO = {
    "date_line": "Friday, September 4",
    "price": "+575",
    "decimal": "6.75",
    "be": "14.8%",
    "coin": "12.5%",
    "hook": "Three bets you would make on their own, priced as one you would not.",
    "legs_line": "San Jose State / Yankees / Rays",
    "thread_title": "the group chat, every Friday",
    "thread": [
        ("them", "put all three on one ticket"),
        ("me", "that ticket needs to hit 14.8% of the time to break even"),
        ("them", "so like a coin flip"),
        ("me", "three coin flips. 12.5%."),
        ("them", "so yes"),
    ],
    "legs": [
        {"league": "cfb", "abbr": "SJSU", "pick": "San Jose State +3",
         "price": "-115", "be": "53.5%", "color": "#0055a2",
         "note": "EMU opened -3.5 and -162. It is -3 and -148 now."},
        {"league": "mlb", "abbr": "NYY", "pick": "Yankees ML",
         "price": "-119", "be": "54.3%", "color": "#132448",
         "note": "Fried 2.80 against Buehler 4.66 in San Diego."},
        {"league": "mlb", "abbr": "TB", "pick": "Rays ML",
         "price": "-104", "be": "51.0%", "color": "#092c5c",
         "note": "Opened -126. Texas is the home favourite now."},
    ],
}
DEMO["legs"][0]["decimal"] = "1.87"
DEMO["legs"][1]["decimal"] = "1.84"
DEMO["legs"][2]["decimal"] = "1.96"


if __name__ == "__main__":
    main()
