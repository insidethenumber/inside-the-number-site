#!/usr/bin/env python3
"""
newsletter_assets.py — build every visual for one Morning Board issue AND the
paste-ready HTML, from one JSON spec, in one command.

    python3 scripts/newsletter_assets.py --issue issue.json \
        --date 2026-09-06 --out-dir assets/newsletter/2026-09-06

Writes into --out-dir:
    header.jpg   dark band: THE MORNING BOARD / date / subtitle  (1200x300)
    pick.jpg     THE PRICE IS THE POINT card for the card's picks (parlay_cards.price)
    move.gif     open→now ticker for the biggest overnight move  (viz.py ticker)
                 skipped when spec.move is null (board did not move)
    number.jpg   the big number card for THE NUMBER TO KNOW      (1200x500)
    issue.html   the whole issue as HTML with <img> tags pointing at
                 https://insidethenumber.com/assets/newsletter/<date>/<file>
                 — this is what gets pasted into Beehiiv as text/html.

Why this exists (Sep 5, 2026): the 7:45 issue went out with zero content images
because the body was pasted as text/plain and the images were never built. Now
the images and the HTML come out of the same command, so one cannot ship
without the other.

Spec (issue.json):
{
  "date_line": "Sunday, September 6",
  "subtitle": "One line under the date.",
  "title": "Post title (one number in it)",
  "free": {"pick": "Ole Miss -7 vs Louisville", "price": "-110", "start": "6:30 PM ET, ESPN",
           "body": ["para 1", "para 2"], "beats": "What beats it: ..."},
  "also": [{"pick": "...", "price": "...", "start": "...", "body": "two sentences"}],
  "price_legs": [{"league":"cfb","abbr":"MISS","pick":"Ole Miss -7","price":"-110",
                  "be":"52.4%","fair":"50.8%","note":"one line"}],
  "price_headline": "Two prices, and what the market's own number says about each.",
  "price_tail": "One closing line for the card.",
  "move": {"away":"LOU","home":"MISS","open":"-6.5","now":"-7","headline":"LOUISVILLE AT OLE MISS",
           "sub":"Half a point toward the home side overnight.", "body": "paragraph"},
  "number": {"value": "46", "body": "Of Saturday's 68 games, 46 were priced at 20 or worse."},
  "market": "paragraph for WHAT THE MARKET KNOWS",
  "board": [{"game": "Louisville at Ole Miss", "line": "MISS -7"}, ...],
  "membership": "one line"
}
"""
import argparse, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw          # noqa: E402
from cards import B, D, M, BG, WHITE, MUTED, GREEN, DIM   # noqa: E402

BASE = "https://insidethenumber.com/assets/newsletter"


def _fit(d, text, font_fn, max_w, start, floor):
    size = start
    while size > floor and d.textlength(text, font=font_fn(size)) > max_w:
        size -= 2
    return font_fn(size)


def header(spec, out):
    W, H = 1200, 300
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((56, 52), "THE MORNING BOARD", font=B(26), fill=GREEN)
    f = _fit(d, spec["date_line"], D, W - 112, 76, 44)
    d.text((56, 96), spec["date_line"], font=f, fill=WHITE)
    sub = spec.get("subtitle", "")
    if sub:
        f2 = _fit(d, sub, M, W - 112, 30, 20)
        d.text((56, 196), sub, font=f2, fill=MUTED)
    d.line([56, H - 44, W - 56, H - 44], fill="#232a36", width=2)
    d.text((56, H - 34), "INSIDE THE NUMBER", font=B(18), fill=DIM)
    r = "insidethenumber.com"
    d.text((W - 56 - d.textlength(r, font=M(18)), H - 34), r, font=M(18), fill=GREEN)
    img.save(out, quality=88)


def number_card(spec, out):
    n = spec["number"]
    W, H = 1200, 500
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((56, 48), "THE NUMBER TO KNOW", font=B(26), fill="#ffb020")
    f = _fit(d, n["value"], D, W - 112, 200, 100)
    d.text((56, 96), n["value"], font=f, fill=WHITE)
    by = d.textbbox((56, 96), n["value"], font=f)[3] + 28
    # wrap body
    words, lines, cur = n["body"].split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=M(30)) > W - 112:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    for i, ln in enumerate(lines[:3]):
        d.text((56, by + i * 40), ln, font=M(30), fill=DIM)
    img.save(out, quality=88)


def price_card(spec, out_dir, out):
    legs = spec.get("price_legs") or []
    if not legs:
        return False
    s = {
        "date_line": spec["date_line"],
        "headline": spec.get("price_headline", "What you pay, and what the market's own number says."),
        "tail": spec.get("price_tail", "Break-even is what the price demands. Fair is the market with the book's cut removed."),
        "legs": legs,
    }
    tmp = os.path.join(out_dir, "_price_spec.json")
    json.dump(s, open(tmp, "w"))
    subprocess.run([sys.executable, os.path.join(HERE, "parlay_cards.py"),
                    "--out-dir", os.path.join(out_dir, "_price"), "--spec", tmp,
                    "--only", "price"], check=True, capture_output=True)
    src = os.path.join(out_dir, "_price", "01-price.png")
    im = Image.open(src).convert("RGB")
    im.resize((1200, int(1200 * im.height / im.width))).save(out, quality=86)
    os.remove(tmp)
    import shutil; shutil.rmtree(os.path.join(out_dir, "_price"), ignore_errors=True)
    return True


def move_gif(spec, out):
    m = spec.get("move")
    if not m:
        return False
    subprocess.run([sys.executable, os.path.join(HERE, "viz.py"), "ticker", "--out", out,
                    "--left", str(m["open"]), "--right", str(m["now"]),
                    "--headline", m["headline"], "--sub", m.get("sub", "")],
                   check=True, capture_output=True)
    mp4 = out[:-4] + ".mp4"
    if os.path.exists(mp4):
        os.remove(mp4)
    return os.path.exists(out) and os.path.getsize(out) < 1_000_000


def issue_html(spec, date, have):
    e = html.escape
    u = lambda f: f"{BASE}/{date}/{f}"
    P = []
    P.append(f'<p><img src="{u("header.jpg")}" alt="The Morning Board — {e(spec["date_line"])}. {e(spec.get("subtitle",""))}"></p>')

    fr = spec["free"]
    P.append("<p><strong>1 · THE FREE PICK</strong></p>")
    P.append(f'<p><strong>{e(fr["pick"])} ({e(fr["price"])})</strong>, {e(fr["start"])}.</p>')
    for para in fr["body"]:
        P.append(f"<p>{e(para)}</p>")
    if fr.get("beats"):
        P.append(f"<p><em>{e(fr['beats'])}</em></p>")
    if have.get("pick.jpg"):
        legs = spec["price_legs"]
        alt = "; ".join(f'{l["pick"]} is {l["price"]}, break-even {l["be"]}, fair {l["fair"]}' for l in legs)
        P.append(f'<p><img src="{u("pick.jpg")}" alt="{e(alt)}"></p>')
    if spec.get("also"):
        P.append("<p><strong>Also on the card</strong></p>")
        for a in spec["also"]:
            P.append(f'<p><strong>{e(a["pick"])} ({e(a["price"])})</strong>, {e(a["start"])}. {e(a["body"])}</p>')

    P.append("<p><strong>2 · BIGGEST OVERNIGHT MOVE</strong></p>")
    m = spec.get("move")
    if m:
        P.append(f"<p>{e(m['body'])}</p>")
        if have.get("move.gif"):
            P.append(f'<p><img src="{u("move.gif")}" alt="{e(m["headline"].title())} opened {e(str(m["open"]))} and is {e(str(m["now"]))} now."></p>')
    else:
        P.append(f"<p>{e(spec.get('no_move', 'The board barely moved overnight.'))}</p>")

    n = spec["number"]
    P.append("<p><strong>3 · THE NUMBER TO KNOW</strong></p>")
    if have.get("number.jpg"):
        P.append(f'<p><img src="{u("number.jpg")}" alt="{e(n["value"])} — {e(n["body"])}"></p>')
    P.append(f"<p><strong>{e(n['value'])}</strong> — {e(n['body'])}</p>")

    P.append("<p><strong>4 · WHAT THE MARKET KNOWS</strong></p>")
    P.append(f"<p>{e(spec['market'])}</p>")

    P.append("<p><strong>5 · TODAY'S BOARD</strong></p>")
    for g in spec["board"]:
        P.append(f'<p>{e(g["game"])} — <strong>{e(g["line"])}</strong></p>')
    P.append('<p><a href="https://insidethenumber.com/games">Every game on today\'s board, priced at what the market really thinks, at insidethenumber.com/games</a></p>')

    if spec.get("membership"):
        P.append(f"<p>{e(spec['membership'])}</p>")
    P.append('<p>Follow Inside the Number on X — <a href="https://x.com/thenumberdesk">@thenumberdesk</a></p>')
    P.append("<p>21+. If gambling stops being fun, stop. 1-800-GAMBLER.</p>")
    return "\n".join(P)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", required=True)
    ap.add_argument("--date", required=True, help="YYYY-MM-DD, used in URLs")
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    spec = json.load(open(a.issue))
    os.makedirs(a.out_dir, exist_ok=True)
    have = {}
    header(spec, os.path.join(a.out_dir, "header.jpg")); have["header.jpg"] = True
    have["pick.jpg"] = price_card(spec, a.out_dir, os.path.join(a.out_dir, "pick.jpg"))
    have["move.gif"] = move_gif(spec, os.path.join(a.out_dir, "move.gif"))
    number_card(spec, os.path.join(a.out_dir, "number.jpg")); have["number.jpg"] = True
    h = issue_html(spec, a.date, have)
    open(os.path.join(a.out_dir, "issue.html"), "w").write(h)
    for f, ok in have.items():
        p = os.path.join(a.out_dir, f)
        print(f"{'OK  ' if ok else 'SKIP'} {f}" + (f"  {os.path.getsize(p)//1024} KB" if ok else ""))
    print("OK   issue.html  images:", h.count("<img"))


if __name__ == "__main__":
    main()
