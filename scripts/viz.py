#!/usr/bin/env python3
"""Formats that are NOT data cards — built Sep 3, 2026 after Chuck said the
franchise cards "all look the same. There are no pictures, memes, videos."

He was right. I scrolled our own Following feed that morning and wrote down
what actually gets views. Highest organic post in our feed: a Thursday-night
TV SCHEDULE GRID from @ProjSports — 938 likes, 27K views — network logos down
the side, kickoff times across the top, team marks filling the grid. Not a
data card. A REFERENCE OBJECT people screenshot and keep. Next: @ParlayScience
at 170K, a product poster — huge white condensed type on black with one green
highlight block. Then @ProFootballTalk, a real action photo with a caption
bar. Then @Bet_Labs posting a raw screenshot of a betslip. Then @Bigbetsbrand
posting a video clip and a text-only "RISE AND SHINE ☀️" at 4.5K.

So the feed is: grids, posters, photos, video, screenshots, jokes. Our cards
were four variations of "dark rectangle, big number". This file is the fix.

Formats here:
  grid     THE BOARD as a tonight's-TV object — times down the side, games as
           team-coloured blocks, the one competitive game highlighted
  poster   Single loud statement, ParlayScience register — condensed white
           type, one saturated highlight block, team marks big
  texts    A phone message thread. The joke format that needs no photography
           and gets screenshotted. FOURTH QUARTER lives here.
  ticker   Animated MP4 + GIF: the number moving from open to now. Motion is
           the cheapest way to stop a thumb and we can do it with ffmpeg.

Usage:
  python3 scripts/viz.py grid   --out x.png --data games.json --sub "..."
  python3 scripts/viz.py poster --out x.png --headline "..." --number "..." ...
  python3 scripts/viz.py texts  --out x.png --data thread.json --sub "..."
  python3 scripts/viz.py ticker --out x.mp4 --left -24.5 --right -18.5 ...
"""
import argparse, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards import BG, PANEL, WHITE, DIM, MUTED, GREEN, LINE, B, D, M, logo, hexcolor
from franchise import ctr, fit, wrap, foot

INK = "#0b0e13"
AMBER = "#ffb020"
HOT = "#00e08a"


def new(W, H, bg=BG):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def paste_c(img, im, cx, cy):
    if im is not None:
        img.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)


# --------------------------------------------------------------------- grid
def f_grid(a):
    """Tonight's slate as a schedule object. Modelled on the @ProjSports post.

    data: [{"slot":"7:00 ET","games":[{league,away_abbr,home_abbr,away_color,
            home_color,line,hero:bool}, ...]}, ...]
    """
    slots = json.load(open(a.data))
    W = 1200
    ROW = 176
    TOP = 190
    H = TOP + len(slots) * ROW + 120
    img, d = new(W, H)

    d.rectangle([0, 0, W, 8], fill=AMBER)
    d.text((44, 44), "TONIGHT'S BOARD", font=D(78), fill=WHITE)
    if a.sub:
        d.text((46, 132), a.sub.upper(), font=D(36), fill=AMBER)

    LEFT = 190
    y = TOP
    for si, s in enumerate(slots):
        d.rounded_rectangle([40, y, LEFT - 16, y + ROW - 14], 12, fill="#1a1f2b")
        ctr(d, (40, y, LEFT - 16, y + ROW - 14), s["slot"].split()[0], D(54), WHITE)
        ctr(d, (40, y + ROW - 62, LEFT - 16, y + ROW - 24), "ET", D(28), MUTED)

        games = s["games"]
        gw = (W - LEFT - 40 - (len(games) - 1) * 12) // max(len(games), 1)
        x = LEFT
        for g in games:
            hero = g.get("hero")
            box = [x, y, x + gw, y + ROW - 14]
            d.rounded_rectangle(box, 12, fill="#101521")
            if hero:
                d.rounded_rectangle(box, 12, outline=AMBER, width=5)
            # team colour spine
            d.rounded_rectangle([x, y, x + 10, y + ROW - 14], 4,
                                fill=hexcolor(g.get("home_color"), "#39405020"))
            lg = g.get("league", "CFB")
            sz = min(66, gw // 3)
            paste_c(img, logo(lg, g.get("away_abbr"), sz), x + gw * 0.32, y + 58)
            paste_c(img, logo(lg, g.get("home_abbr"), sz), x + gw * 0.68, y + 58)
            ctr(d, (x, y + 34, x + gw, y + 46), "", D(20), MUTED)
            line = str(g.get("line", ""))
            f = fit(d, line, D, gw - 20, 44, 22)
            ctr(d, (x, y + ROW - 76, x + gw, y + ROW - 26), line, f,
                AMBER if hero else DIM)
            x += gw + 12
        y += ROW

    if a.note:
        d.text((44, y + 4), a.note.upper(), font=D(40), fill=HOT)
    d.text((44, H - 62), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((368, H - 58), "insidethenumber.com", font=M(25), fill=GREEN)
    d.text((W - 232, H - 58), "@thenumberdesk", font=M(25), fill=MUTED)
    return img


# ------------------------------------------------------------------- poster
def f_poster(a):
    """One loud statement. Near-black, condensed white type, one highlight
    block, team marks large. The @ParlayScience register."""
    W, H = 1200, 1200
    img, d = new(W, H, "#07090d")
    d.rectangle([0, 0, W, 10], fill=HOT)

    if a.sub:
        d.text((56, 54), a.sub.upper(), font=D(34), fill=HOT)

    lines = [l for l in (a.headline or "").upper().split("|")]
    y = 130
    for i, ln in enumerate(lines):
        ln = ln.strip()
        f = fit(d, ln, D, W - 112, 132, 48)
        if a.highlight and ln == a.highlight.strip().upper():
            wd = d.textlength(ln, font=f)
            d.rectangle([48, y + 6, 68 + wd, y + f.size + 22], fill=HOT)
            d.text((58, y), ln, font=f, fill=INK)
        else:
            d.text((56, y), ln, font=f, fill=WHITE)
        y += f.size + 20

    # team marks, big
    if a.league and (a.away_abbr or a.home_abbr):
        paste_c(img, logo(a.league, a.away_abbr, 240), 330, 780)
        ctr(d, (500, 700, 700, 860), "@", D(96), "#39404f")
        paste_c(img, logo(a.league, a.home_abbr, 240), 870, 780)

    if a.number:
        f = fit(d, a.number, D, W - 112, 190, 90)
        ctr(d, (0, 930, W, 1080), a.number, f, HOT)
    if a.note:
        ctr(d, (0, 1080, W, 1130), a.note.upper(), D(40), DIM)

    d.text((56, H - 60), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((380, H - 56), "insidethenumber.com", font=M(25), fill=GREEN)
    d.text((W - 244, H - 56), "@thenumberdesk", font=M(25), fill=MUTED)
    return img


# -------------------------------------------------------------------- texts
def f_texts(a):
    """A phone message thread. The joke format that needs no photography,
    reads instantly at thumbnail size and gets screenshotted.

    data: [{"who":"them"|"me", "t":"..."}]
    """
    msgs = json.load(open(a.data))
    W = 1000
    PAD, BUB, GAP = 40, 26, 16
    f = M(38)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    laid, y = [], 168
    for m in msgs:
        maxw = W - 2 * PAD - 190
        ls = wrap(d0, m["t"], f, maxw - 2 * BUB)
        wdt = max(d0.textlength(l, font=f) for l in ls) + 2 * BUB
        hgt = len(ls) * (f.size + 12) + 2 * BUB - 12
        laid.append((m["who"], ls, wdt, hgt))
        y += hgt + GAP
    H = y + 130

    img, d = new(W, H, "#000000")
    # phone chrome
    d.rectangle([0, 0, W, 108], fill="#0d0d0f")
    ctr(d, (0, 26, W, 76), a.sub or "Group chat", M(34), "#9aa3b0")
    d.line([0, 108, W, 108], fill="#22252b", width=2)

    y = 168
    for who, ls, wdt, hgt in laid:
        me = who == "me"
        x1 = W - PAD if me else PAD + wdt
        x0 = x1 - wdt
        fill = "#1d9bf0" if me else "#26282d"
        ink = "#ffffff"
        d.rounded_rectangle([x0, y, x1, y + hgt], 28, fill=fill)
        ty = y + BUB - 6
        for l in ls:
            d.text((x0 + BUB, ty), l, font=f, fill=ink)
            ty += f.size + 12
        y += hgt + GAP

    d.line([PAD, H - 96, W - PAD, H - 96], fill="#22252b", width=2)
    d.text((PAD, H - 74), "INSIDE THE NUMBER", font=B(26), fill=WHITE)
    d.text((PAD + 300, H - 70), "insidethenumber.com", font=M(23), fill=GREEN)
    d.text((W - 230, H - 70), "@thenumberdesk", font=M(23), fill=MUTED)
    return img


# ------------------------------------------------------------------- ticker
def ticker_frames(a, tmp):
    """Frames for the line-move animation: the number counts from open to now
    while a bar slides. Motion stops a thumb; a static card does not."""
    W, H = 1200, 676
    lo, hi = float(a.left), float(a.right)
    N, HOLD = 34, 16
    paths = []
    for i in range(N + HOLD * 2):
        if i < HOLD:
            t = 0.0
        elif i >= N + HOLD:
            t = 1.0
        else:
            p = (i - HOLD) / N
            t = p * p * (3 - 2 * p)           # ease in/out
        v = lo + (hi - lo) * t
        img, d = new(W, H)
        d.rectangle([0, 0, W, 8], fill=AMBER)
        d.text((48, 40), "MARKET MOVERS", font=D(46), fill=AMBER)
        if a.sub:
            d.text((48, 96), a.sub.upper(), font=D(34), fill=MUTED)

        if a.league:
            paste_c(img, logo(a.league, a.away_abbr, 92), 110, 250)
            paste_c(img, logo(a.league, a.home_abbr, 92), 220, 250)
        if a.headline:
            d.text((300, 215), a.headline.upper(), font=D(56), fill=WHITE)

        txt = f"{v:+.1f}".replace("+", "") if v < 0 else f"+{v:.1f}"
        f = D(210)
        ctr(d, (0, 300, W, 470), txt, f, AMBER if t > 0 else DIM)

        # slider
        y0 = 500
        d.rounded_rectangle([120, y0, W - 120, y0 + 16], 8, fill="#20252f")
        px = 120 + (W - 240) * t
        d.rounded_rectangle([120, y0, px, y0 + 16], 8, fill=AMBER)
        d.ellipse([px - 20, y0 - 12, px + 20, y0 + 28], fill=WHITE)
        d.text((110, y0 + 36), f"OPEN {lo:g}", font=D(30), fill=MUTED)
        rt = f"NOW {hi:g}"
        d.text((W - 120 - d.textlength(rt, font=D(30)), y0 + 36), rt,
               font=D(30), fill=AMBER if t == 1 else MUTED)

        if a.note and t == 1:
            ctr(d, (0, 585, W, 625), a.note.upper(), D(40), WHITE)
        d.text((48, H - 42), "INSIDE THE NUMBER", font=B(24), fill=WHITE)
        d.text((330, H - 39), "insidethenumber.com", font=M(22), fill=GREEN)
        d.text((W - 210, H - 39), "@thenumberdesk", font=M(22), fill=MUTED)

        p = os.path.join(tmp, f"f{i:04d}.png")
        img.save(p)
        paths.append(p)
    return paths


def f_ticker(a):
    tmp = tempfile.mkdtemp()
    ticker_frames(a, tmp)
    out = a.out
    stem = os.path.splitext(out)[0]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24",
                    "-i", os.path.join(tmp, "f%04d.png"),
                    "-vf", "scale=1200:676:flags=lanczos",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "24",
                    stem + ".mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24",
                    "-i", os.path.join(tmp, "f%04d.png"),
                    "-vf", "fps=20,scale=800:-1:flags=lanczos,split[s0][s1];"
                           "[s0]palettegen[p];[s1][p]paletteuse",
                    "-loop", "0", stem + ".gif"], check=True)
    print(f"wrote {stem}.mp4 and {stem}.gif")
    return None



# -------------------------------------------------------------------- stack
def f_stack(a):
    """Colour-blocked matchup rows. Modelled on @Novig's Chargers "gauntlet"
    post (Sep 3, 2026 reference set): a vertical list where the left half is
    one constant team block and the right half is each opponent in THEIR
    colour, logo alongside. Dead simple, enormously legible at thumbnail size,
    and it turns a schedule into a story ("look what they have to survive").

    Ours carries the number on each row, which is the whole point of the
    account — the same object, but priced.

    data: [{"left":"COLORADO","left_abbr":"COLO","left_color":"CFB4A0",
            "right":"GEORGIA TECH","right_abbr":"GT","right_color":"B3A369",
            "line":"GT -6.5"}, ...]
    A single constant left side reads best; repeat it on every row.
    """
    rows = json.load(open(a.data))
    W = 1200
    RH = 128
    TOP = 210
    H = TOP + len(rows) * RH + 150
    img, d = new(W, H, "#07090d")

    d.text((44, 44), (a.headline or "THE GAUNTLET").upper(), font=D(76), fill=WHITE)
    if a.sub:
        d.text((46, 136), a.sub.upper(), font=D(34), fill=HOT)

    y = TOP
    half = W // 2
    for r in rows:
        lc = hexcolor(r.get("left_color"), "#1b2230")
        rc = hexcolor(r.get("right_color"), "#20283a")
        d.rectangle([40, y, half, y + RH - 6], fill=lc)
        d.rectangle([half, y, W - 40, y + RH - 6], fill=rc)

        lg = r.get("league", "CFB")
        # left: name then mark, hugging the centre seam
        li = logo(lg, r.get("left_abbr"), 66)
        lnf = fit(d, (r.get("left") or "").upper(), D, half - 70 - 110, 46, 24)
        d.text((70, y + 38 + (46 - lnf.size) // 2), (r.get("left") or "").upper(),
               font=lnf, fill=readable(lc))
        # Sep 3: a logo the same colour as its panel disappears (Texas burnt
        # orange on burnt orange, Clemson's paw on orange, Indiana crimson on
        # crimson). Every mark now sits on a white disc so it reads on any
        # team colour — the same trick broadcast score bugs use.
        cy = y + (RH - 6) / 2
        if li is not None:
            plate(d, half - 60, cy, 44)
        paste_c(img, li, half - 60, cy)
        # right: mark then name
        ri = logo(lg, r.get("right_abbr"), 66)
        if ri is not None:
            plate(d, half + 62, cy, 44)
        paste_c(img, ri, half + 62, cy)
        # Reserve the price's width FIRST, then fit the name into what is left.
        # Sep 3: "KENNESAW ST" ran straight into "KENN -22.5" and read as one
        # word. On a card whose whole job is legibility that is fatal.
        ln = str(r.get("line", ""))
        lf = D(44)
        lw = d.textlength(ln, font=lf) if ln else 0
        name_x = half + 118
        name_max = (W - 66 - lw - 28) - name_x
        nf = fit(d, (r.get("right") or "").upper(), D, name_max, 46, 24)
        d.text((name_x, y + 38 + (46 - nf.size) // 2),
               (r.get("right") or "").upper(), font=nf, fill=readable(rc))
        if ln:
            d.text((W - 66 - lw, y + 40), ln, font=lf, fill=readable(rc))
        y += RH

    if a.note:
        d.text((44, y + 14), a.note.upper(), font=D(38), fill=HOT)
    d.text((44, H - 62), "INSIDE THE NUMBER", font=B(28), fill=WHITE)
    d.text((368, H - 58), "insidethenumber.com", font=M(25), fill=GREEN)
    d.text((W - 232, H - 58), "@thenumberdesk", font=M(25), fill=MUTED)
    return img


def plate(d, cx, cy, r, fill="#ffffff"):
    """White disc behind a team mark so it survives any panel colour."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def readable(bg):
    """Black or white ink, whichever survives on this background colour.
    Team colours run from Iowa black to Oregon yellow; hard-coding white text
    makes half the league unreadable."""
    c = bg.lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#07090d" if lum > 0.6 else "#ffffff"

FORMATS = {"grid": f_grid, "poster": f_poster, "texts": f_texts,
           "ticker": f_ticker, "stack": f_stack}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("format", choices=sorted(FORMATS))
    p.add_argument("--out", required=True)
    p.add_argument("--data"); p.add_argument("--sub"); p.add_argument("--headline")
    p.add_argument("--note"); p.add_argument("--number"); p.add_argument("--highlight")
    p.add_argument("--league"); p.add_argument("--away-abbr"); p.add_argument("--home-abbr")
    p.add_argument("--left"); p.add_argument("--right")
    a = p.parse_args()
    img = FORMATS[a.format](a)
    if img is not None:
        img.save(a.out)
        print(f"wrote {a.out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
