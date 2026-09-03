#!/usr/bin/env python3
"""Franchise card templates for @thenumberdesk — the six formats, name baked in.

Built Sep 2, 2026 against docs/MARKETING_PLAN.md §3 and FRANCHISES.md. Every
original X post is one of these. The franchise name sits in the same place, in
the same colour, on every card, so the format becomes recognisable before the
handle is read. Rules that shaped every layout, learned the hard way on Sep 2:

  - five words of huge type beat sixty words of small type
  - one saturated colour per card, on a dark ground
  - the number is the hero; copy is a caption
  - logo when we have it, colour bar when we do not; never a fetch

Usage:
  python3 scripts/franchise.py <template> --out file.png [fields...]
  python3 scripts/franchise.py --demo out_dir/      # renders every template
                                                    # with real Sep 2/3 data

Templates (12):
  board          THE BOARD — the slate, tightest game highlighted
  board-one      THE BOARD — one hero game, two logos, the price
  number         THE NUMBER — one huge figure (green)
  number-red     THE NUMBER — one huge figure, ugly-price variant (red)
  movers         MARKET MOVERS — open → now, one game
  movers-list    MARKET MOVERS — several moves, ranked
  price          THE PRICE IS THE POINT — both sides' implied %, the cut
  breakeven      THE PRICE IS THE POINT — "you need to win X% at this price"
  knows          WHAT THE MARKET KNOWS — a lesson, statement + explanation
  q4             FOURTH QUARTER — the joke, text only, huge
  q4-split       FOURTH QUARTER — two-panel joke (green/red)
  sunday         SUNDAY — what the numbers taught us this week (3 rows)
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards import (BG, PANEL, HILITE, WHITE, DIM, MUTED, GREEN, BLUE, AMBER,
                   LINE, B, D, M, logo, hexcolor)

RED = "#e0263c"
FR = {  # franchise → chip colour. One colour each, forever.
    "THE BOARD": "#1d9bf0",
    "THE NUMBER": "#00d084",
    "MARKET MOVERS": "#ffb020",
    "THE PRICE IS THE POINT": "#b388ff",
    "WHAT THE MARKET KNOWS": "#3ba7ff",
    "FOURTH QUARTER": "#ff5c8a",
    "SUNDAY": "#f2f4f7",
}


# ----------------------------------------------------------------- helpers
def ctr(d, box, txt, font, fill):
    if not txt:
        return
    x0, y0, x1, y1 = box
    w = d.textlength(txt, font=font)
    bb = font.getbbox(txt)
    d.text(((x0 + x1 - w) / 2, (y0 + y1 - (bb[3] - bb[1])) / 2 - bb[1]),
           txt, font=font, fill=fill)


def fit(d, txt, font_fn, max_w, start, floor=28):
    """Largest size at which txt fits in max_w."""
    s = start
    while s > floor:
        f = font_fn(s)
        if d.textlength(txt, font=f) <= max_w:
            return f
        s -= 4
    return font_fn(floor)


def wrap(d, txt, font, max_w):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, name, W, sub=None):
    """The franchise tag. Same place, same size, every card."""
    col = FR.get(name, WHITE)
    f = D(40)
    w = d.textlength(name, font=f) + 56
    d.rounded_rectangle([48, 44, 48 + w, 112], 14, fill=col)
    ink = BG if name != "SUNDAY" else BG
    ctr(d, (48, 44, 48 + w, 112), name, f, ink)
    if sub:
        d.text((48 + w + 24, 62), sub.upper(), font=D(34), fill=MUTED)
    return 140


def foot(d, W, H):
    d.line([48, H - 84, W - 48, H - 84], fill=LINE, width=2)
    d.text((48, H - 64), "INSIDE THE NUMBER", font=B(26), fill=WHITE)
    d.text((326, H - 60), "insidethenumber.com", font=M(23), fill=GREEN)
    d.text((W - 220, H - 60), "@thenumberdesk", font=M(23), fill=MUTED)


def new(W, H):
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def team_block(img, d, league, abbr, color, name, x0, x1, y, size=150):
    """Logo (or colour disc) centred in [x0,x1] at y, name under it."""
    im = logo(league, abbr, size)
    cx = (x0 + x1) // 2
    if im is not None:
        img.paste(im, (int(cx - im.width / 2), int(y)), im)
    else:
        d.ellipse([cx - size / 2, y, cx + size / 2, y + size], fill=hexcolor(color))
        ctr(d, (cx - size / 2, y, cx + size / 2, y + size), (abbr or "")[:4], D(64), WHITE)
    ctr(d, (x0, y + size + 14, x1, y + size + 70), (name or abbr or "").upper(), D(44), WHITE)


# --------------------------------------------------------------- templates
def t_board(a):
    rows = json.load(open(a.data))
    W, RH = 1200, 92
    H = 190 + len(rows) * RH + 120
    img, d = new(W, H)
    chip(d, "THE BOARD", W, a.sub)
    y = 150
    for i, r in enumerate(rows):
        hero = i == 0
        d.rounded_rectangle([48, y, W - 48, y + RH - 12], 12, fill=HILITE if hero else PANEL)
        x = 72
        for side in ("away", "home"):
            im = logo(r.get("league"), r.get(side + "_abbr"), 56)
            if im is not None:
                img.paste(im, (x, int(y + (RH - 12) / 2 - im.height / 2)), im)
            else:
                d.rounded_rectangle([x, y + 14, x + 12, y + RH - 26], 3,
                                    fill=hexcolor(r.get(side + "_color")))
            x += 70
        d.text((x + 8, y + 18), f"{r['away']}  @  {r['home']}".upper(),
               font=D(44 if hero else 40), fill=WHITE if hero else DIM)
        line = str(r.get("line", ""))
        f = D(56 if hero else 44)
        d.text((W - 72 - d.textlength(line, font=f), y + 10), line, font=f,
               fill=FR["THE BOARD"] if hero else WHITE)
        if r.get("total"):
            t = str(r["total"]); ft = D(30)
            d.text((W - 300 - d.textlength(t, font=ft), y + 26), t, font=ft, fill=MUTED)
        y += RH
    if a.note:
        d.text((48, y + 10), a.note.upper(), font=D(40), fill=FR["THE BOARD"])
    foot(d, W, H)
    return img


def t_board_one(a):
    W, H = 1200, 900
    img, d = new(W, H)
    chip(d, "THE BOARD", W, a.sub)
    team_block(img, d, a.league, a.away_abbr, a.away_color, a.away, 48, 560, 200, 220)
    team_block(img, d, a.league, a.home_abbr, a.home_color, a.home, 640, W - 48, 200, 220)
    ctr(d, (500, 250, 700, 380), "@", D(90), MUTED)
    d.rounded_rectangle([48, 540, W - 48, 720], 18, fill=PANEL)
    ctr(d, (48, 540, W - 48, 660), a.number or "", D(130), FR["THE BOARD"])
    ctr(d, (48, 650, W - 48, 720), (a.headline or "").upper(), D(40), DIM)
    if a.note:
        ctr(d, (48, 740, W - 48, 800), a.note.upper(), D(44), WHITE)
    foot(d, W, H)
    return img


def _number(a, col):
    W, H = 1200, 800
    img, d = new(W, H)
    chip(d, "THE NUMBER", W, a.sub)
    f = fit(d, a.number or "", D, W - 96, 340, 120)
    ctr(d, (48, 150, W - 48, 520), a.number or "", f, col)
    if a.headline:
        f2 = fit(d, a.headline.upper(), D, W - 96, 72, 40)
        ctr(d, (48, 520, W - 48, 610), a.headline.upper(), f2, WHITE)
    if a.note:
        for i, ln in enumerate(wrap(d, a.note, M(30), W - 96)[:2]):
            ctr(d, (48, 620 + i * 40, W - 48, 660 + i * 40), ln, M(30), MUTED)
    if a.league and a.away_abbr:
        im = logo(a.league, a.away_abbr, 110)
        if im is not None:
            img.paste(im, (W - 48 - im.width, 40), im)
    foot(d, W, H)
    return img


def t_number(a): return _number(a, FR["THE NUMBER"])
def t_number_red(a): return _number(a, RED)


def t_movers(a):
    W, H = 1200, 820
    img, d = new(W, H)
    chip(d, "MARKET MOVERS", W, a.sub)
    x = 48
    for abbr, col in ((a.away_abbr, a.away_color), (a.home_abbr, a.home_color)):
        im = logo(a.league, abbr, 96)
        if im is not None:
            img.paste(im, (x, 160), im); x += im.width + 16
    d.text((x + 8, 178), (a.headline or f"{a.away} @ {a.home}").upper(), font=D(60), fill=WHITE)
    # open → now
    y0, y1 = 320, 600
    d.rounded_rectangle([48, y0, 540, y1], 18, fill=PANEL)
    d.rounded_rectangle([660, y0, W - 48, y1], 18, fill=FR["MARKET MOVERS"])
    # Fit both figures to the SAME size — the smaller of the two that fit —
    # so the eye compares the numbers, not the type sizes. Sep 3: hardcoding
    # 170 let "BUF -24.5" run straight out of its panel.
    lw, rw = 540 - 48 - 56, (W - 48) - 660 - 56
    fL = fit(d, a.left_number or "", D, lw, 170, 40)
    fR = fit(d, a.right_number or "", D, rw, 170, 40)
    fN = D(min(fL.size, fR.size))
    ctr(d, (48, y0 + 20, 540, y0 + 78), "OPENED", D(36), MUTED)
    ctr(d, (48, y0 + 78, 540, y1 - 24), a.left_number or "", fN, DIM)
    ctr(d, (660, y0 + 20, W - 48, y0 + 78), "NOW", D(36), BG)
    ctr(d, (660, y0 + 78, W - 48, y1 - 24), a.right_number or "", fN, BG)
    ctr(d, (548, y0, 652, y1), "\u2192", D(96), FR["MARKET MOVERS"])
    if a.note:
        f = fit(d, a.note.upper(), D, W - 96, 52, 32)
        ctr(d, (48, 630, W - 48, 700), a.note.upper(), f, WHITE)
    foot(d, W, H)
    return img


def t_movers_list(a):
    rows = json.load(open(a.data))
    W, RH = 1200, 104
    H = 190 + len(rows) * RH + 120
    img, d = new(W, H)
    chip(d, "MARKET MOVERS", W, a.sub)
    y = 150
    for i, r in enumerate(rows):
        d.rounded_rectangle([48, y, W - 48, y + RH - 14], 12, fill=HILITE if i == 0 else PANEL)
        x = 72
        for side in ("away", "home"):
            im = logo(r.get("league"), r.get(side + "_abbr"), 60)
            if im is not None:
                img.paste(im, (x, int(y + (RH - 14) / 2 - im.height / 2)), im); x += 68
        d.text((x + 8, y + 22), r["game"].upper(), font=D(42), fill=WHITE)
        s = f"{r['open']}  →  {r['now']}"
        f = D(52)
        d.text((W - 80 - d.textlength(s, font=f), y + 16), s, font=f,
               fill=FR["MARKET MOVERS"] if i == 0 else DIM)
        y += RH
    if a.note:
        d.text((48, y + 8), a.note.upper(), font=D(40), fill=WHITE)
    foot(d, W, H)
    return img


def t_price(a):
    """left = favourite (price, implied %), right = dog. note = the cut."""
    W, H = 1200, 900
    img, d = new(W, H)
    chip(d, "THE PRICE IS THE POINT", W, a.sub)
    if a.headline:
        d.text((48, 150), a.headline.upper(), font=D(50), fill=WHITE)
    top, bh, gap = 240, 420, 24
    bw = (W - 96 - gap) // 2
    for i, (x0, num, lab, l1, col) in enumerate([
            (48, a.left_number, a.left_label, a.left_line1, PANEL),
            (48 + bw + gap, a.right_number, a.right_label, a.right_line1, PANEL)]):
        d.rounded_rectangle([x0, top, x0 + bw, top + bh], 18, fill=col)
        ctr(d, (x0, top + 24, x0 + bw, top + 80), (lab or "").upper(), D(40), MUTED)
        ctr(d, (x0, top + 80, x0 + bw, top + 250), num or "", D(140), WHITE)
        ctr(d, (x0, top + 250, x0 + bw, top + 330), (l1 or "").upper(), D(64), FR["THE PRICE IS THE POINT"])
        ctr(d, (x0, top + 330, x0 + bw, top + 390), "WHAT THE MARKET REALLY THINKS", D(26), MUTED)
    y = top + bh + 24
    d.rounded_rectangle([48, y, W - 48, y + 120], 16, fill=FR["THE PRICE IS THE POINT"])
    ctr(d, (48, y, W - 48, y + 70), (a.note or "").upper(), D(56), BG)
    ctr(d, (48, y + 66, W - 48, y + 116), a.note2 or "", M(26), BG)
    foot(d, W, H)
    return img


def t_breakeven(a):
    W, H = 1200, 760
    img, d = new(W, H)
    chip(d, "THE PRICE IS THE POINT", W, a.sub)
    d.text((48, 150), "AT", font=D(60), fill=MUTED)
    d.text((120, 120), a.number or "", font=D(140), fill=WHITE)
    d.text((48, 290), "YOU NEED TO WIN", font=D(60), fill=MUTED)
    ctr(d, (48, 340, W - 48, 560), a.headline or "", D(230), FR["THE PRICE IS THE POINT"])
    if a.note:
        f = fit(d, a.note.upper(), D, W - 96, 46, 30)
        ctr(d, (48, 570, W - 48, 640), a.note.upper(), f, WHITE)
    foot(d, W, H)
    return img


def t_knows(a):
    W, H = 1200, 860
    img, d = new(W, H)
    chip(d, "WHAT THE MARKET KNOWS", W, a.sub)
    y = 160
    f = D(76)
    for ln in wrap(d, (a.headline or "").upper(), f, W - 96)[:3]:
        d.text((48, y), ln, font=f, fill=WHITE); y += 88
    y += 20
    d.rounded_rectangle([48, y, 60, y + 260], 4, fill=FR["WHAT THE MARKET KNOWS"])
    f2 = M(34)
    for ln in wrap(d, a.note or "", f2, W - 140)[:6]:
        d.text((88, y + 6), ln, font=f2, fill=DIM); y += 44
    foot(d, W, H)
    return img


def t_q4(a):
    W, H = 1200, 675
    img, d = new(W, H)
    chip(d, "FOURTH QUARTER", W, a.sub)
    f = D(84)
    lines = wrap(d, a.headline or "", f, W - 96)
    while len(lines) > 4 and f.size > 48:
        f = D(f.size - 8); lines = wrap(d, a.headline or "", f, W - 96)
    total = len(lines) * (f.size + 12)
    y = 150 + (H - 84 - 150 - total) / 2
    for ln in lines:
        d.text((48, y), ln, font=f, fill=WHITE); y += f.size + 12
    foot(d, W, H)
    return img


def t_q4_split(a):
    W, H = 1200, 820
    img, d = new(W, H)
    chip(d, "FOURTH QUARTER", W, a.sub)
    if a.headline:
        d.text((48, 150), a.headline.upper(), font=D(50), fill=WHITE)
    top, bh, gap = 230, 440, 24
    bw = (W - 96 - gap) // 2
    for x0, col, big, lab, ink in [(48, "#00c46a", a.left_number, a.left_label, BG),
                                   (48 + bw + gap, RED, a.right_number, a.right_label, WHITE)]:
        d.rounded_rectangle([x0, top, x0 + bw, top + bh], 18, fill=col)
        ctr(d, (x0, top + 30, x0 + bw, top + 260), big or "", fit(d, big or "", D, bw - 40, 200, 80), ink)
        for i, ln in enumerate(wrap(d, (lab or "").upper(), D(44), bw - 40)[:3]):
            ctr(d, (x0, top + 260 + i * 52, x0 + bw, top + 312 + i * 52), ln, D(44), ink)
    foot(d, W, H)
    return img


def t_sunday(a):
    rows = json.load(open(a.data))
    W, RH = 1200, 150
    H = 210 + len(rows) * RH + 110
    img, d = new(W, H)
    chip(d, "SUNDAY", W, "WHAT THE NUMBERS TAUGHT US THIS WEEK")
    y = 160
    for r in rows:
        d.rounded_rectangle([48, y, W - 48, y + RH - 16], 14, fill=PANEL)
        d.text((80, y + 18), r["label"].upper(), font=D(30), fill=MUTED)
        d.text((80, y + 52), r["value"], font=D(60), fill=WHITE)
        y += RH
    foot(d, W, H)
    return img


TEMPLATES = {
    "board": t_board, "board-one": t_board_one, "number": t_number,
    "number-red": t_number_red, "movers": t_movers, "movers-list": t_movers_list,
    "price": t_price, "breakeven": t_breakeven, "knows": t_knows,
    "q4": t_q4, "q4-split": t_q4_split, "sunday": t_sunday,
}


# -------------------------------------------------------------------- demo
def demo(out_dir):
    """Every template, real numbers from Sep 2-3, 2026 (checked that day)."""
    os.makedirs(out_dir, exist_ok=True)
    N = argparse.Namespace
    base = dict(sub=None, note=None, note2=None, headline=None, number=None,
                league=None, away=None, home=None, away_abbr=None, home_abbr=None,
                away_color=None, home_color=None, data=None, left_number=None,
                left_label=None, left_line1=None, right_number=None,
                right_label=None, right_line1=None)
    def A(**k):
        d = dict(base); d.update(k); return N(**d)

    tmps = []
    def J(rows):
        p = os.path.join(out_dir, f"_tmp{len(tmps)}.json")
        json.dump(rows, open(p, "w")); tmps.append(p); return p

    jobs = {
        "board": A(sub="THURSDAY · CFB WEEK 1", note="One football game. Ten scrimmages.",
                   data=J([
            {"league": "CFB", "away": "Colorado", "home": "Georgia Tech", "away_abbr": "COLO", "home_abbr": "GT", "line": "GT -6.5", "total": "o50.5"},
            {"league": "CFB", "away": "UAlbany", "home": "Buffalo", "away_abbr": "ALB", "home_abbr": "BUFF", "line": "BUFF -1200"},
            {"league": "CFB", "away": "Akron", "home": "Wake Forest", "away_abbr": "AKR", "home_abbr": "WAKE", "line": "WAKE -3200"},
            {"league": "CFB", "away": "UAB", "home": "Illinois", "away_abbr": "UAB", "home_abbr": "ILL", "line": "ILL -4500"},
            {"league": "CFB", "away": "UMass", "home": "Rutgers", "away_abbr": "MASS", "home_abbr": "RUTG", "line": "RUTG -6500"},
            {"league": "CFB", "away": "Idaho", "home": "Utah", "away_abbr": "IDHO", "home_abbr": "UTAH", "line": "UTAH -100000"},
        ])),
        "board-one": A(sub="THURSDAY NIGHT", league="CFB", away="Colorado", home="Georgia Tech",
                       away_abbr="COLO", home_abbr="GT", number="GT -6.5",
                       headline="Total 50.5 · Colorado +195", note="The only Thursday game the market can't call"),
        "number": A(sub="THURSDAY", number="-100000", headline="Utah's moneyline against Idaho",
                    note="A hundred thousand dollars to win one. The market is not asking for your opinion.",
                    league="CFB", away_abbr="UTAH"),
        "number-red": A(sub="WEDNESDAY", number="-299", headline="Dodgers, at home, vs the Giants",
                        note="Strip the book's cut and the market says 72%. You are paying for 75%.",
                        league="MLB", away_abbr="LAD"),
        "movers": A(sub="THURSDAY", league="CFB", away="Colorado", home="Georgia Tech",
                    away_abbr="COLO", home_abbr="GT", headline="Colorado @ Georgia Tech",
                    left_number="GT -7", right_number="GT -6.5",
                    note="Half a point toward the dog on a game nobody is talking about"),
        "movers-list": A(sub="OVERNIGHT · MLB", note="Three totals moved. Zero sides did.", data=J([
            {"league": "MLB", "game": "MIL @ CHC", "away_abbr": "MIL", "home_abbr": "CHC", "open": "o9", "now": "o8.5"},
            {"league": "MLB", "game": "PHI @ ARI", "away_abbr": "PHI", "home_abbr": "ARI", "open": "o8", "now": "o8.5"},
            {"league": "MLB", "game": "STL @ LAD", "away_abbr": "STL", "home_abbr": "LAD", "open": "u8.5", "now": "u8"},
        ])),
        "price": A(sub="DODGERS · GIANTS", headline="-299 and +238 together add up to 104.5%",
                   left_number="-299", left_label="Dodgers", left_line1="72%",
                   right_number="+238", right_label="Giants", right_line1="28%",
                   note="The 4.5% is the house", note2="Strip it out and that is what you are actually buying."),
        "breakeven": A(sub="THE MATH", number="-299", headline="75%",
                       note="just to break even. The market thinks 72%."),
        "knows": A(sub="READING A NUMBER",
                   headline="A total that opens 9.5 and closes 9.5 while the over goes +100 to -110 is not unsure.",
                   note="It is a market defending the number. The book would rather move the price than move the line, which tells you it likes 9.5 exactly where it is. An unsure market moves the line. A confident one charges you more to bet against it. Those are different things and they pay differently."),
        "q4": A(sub="THURSDAY", headline="college football is back tomorrow, which means it is time to remember you're bad at this and do it anyway"),
        "q4-split": A(sub="WEEK 1", headline="Every bettor on Thursday night",
                      left_number="-6.5", left_label="What I bet",
                      right_number="+195", right_label="What I'll be screaming about at 10:47 PM"),
        "sunday": A(data=J([
            {"label": "Biggest move of the week", "value": "GT -7 → -6.5 vs Colorado"},
            {"label": "Ugliest price that still got bet", "value": "Utah -100000"},
            {"label": "The number that meant the most", "value": "Dodgers -299 = 75% just to break even"},
        ])),
    }
    for name, a in jobs.items():
        img = TEMPLATES[name](a)
        p = os.path.join(out_dir, f"{name}.png")
        img.save(p)
        print(f"{name:<12} {img.size[0]}x{img.size[1]}  {p}")
    for t in tmps:
        os.remove(t)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("template", nargs="?", choices=sorted(TEMPLATES))
    p.add_argument("--out"); p.add_argument("--demo", metavar="DIR")
    p.add_argument("--data"); p.add_argument("--sub"); p.add_argument("--headline")
    p.add_argument("--note"); p.add_argument("--note2"); p.add_argument("--number")
    p.add_argument("--league"); p.add_argument("--away"); p.add_argument("--home")
    p.add_argument("--away-abbr"); p.add_argument("--home-abbr")
    p.add_argument("--away-color"); p.add_argument("--home-color")
    for s in ("left", "right"):
        p.add_argument(f"--{s}-number"); p.add_argument(f"--{s}-label"); p.add_argument(f"--{s}-line1")
    a = p.parse_args()
    if a.demo:
        return demo(a.demo)
    if not a.template or not a.out:
        sys.exit("need <template> --out, or --demo DIR")
    img = TEMPLATES[a.template](a)
    img.save(a.out)
    print(f"wrote {a.out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
