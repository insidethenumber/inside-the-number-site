#!/usr/bin/env python3
"""
Inside the Number — UFC card page generator.

Produces ufc.html: a STATIC page with every fight on the upcoming UFC card,
the best available price on each corner across ~50 books, the true win
probability once the vig is stripped, and what the house keeps.

Why static generation instead of the client-side rendering the games board
uses: a crawler fetching games.html receives "Loading today's board..." and
nothing else, which is why that page cannot rank. This page is the opposite
bet — the fights are in the HTML itself, so Google can index the one piece of
content ITN owns that no free competitor publishes at all. ESPN carries zero
MMA prices; The Odds API includes MMA on the free tier. That asymmetry is the
entire reason this page exists.

Runs in GitHub Actions (the local sandbox cannot reach api.the-odds-api.com).
One credit per run.

    python3 scripts/build_ufc_page.py --start 2026-08-29 --end 2026-08-30 \
        --title "UFC Fight Night Shanghai" --venue "Shanghai, China"
"""

import argparse, html, json, os, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "https://api.the-odds-api.com/v4"


def api_key():
    k = os.environ.get("ODDS_API_KEY")
    if k:
        return k
    p = os.path.join(ROOT, "itn-secrets.env")
    if os.path.exists(p):
        for line in open(p):
            if line.strip().startswith("ODDS_API_KEY="):
                v = line.split("=", 1)[1].strip()
                if v:
                    return v
    sys.exit("ERROR: no ODDS_API_KEY")


def implied(american):
    v = float(american)
    return 100.0 / (v + 100.0) if v > 0 else abs(v) / (abs(v) + 100.0)


def fetch(start, end):
    q = urllib.parse.urlencode({
        "apiKey": api_key(), "regions": "us", "markets": "h2h",
        "oddsFormat": "american",
        "commenceTimeFrom": start + "T00:00:00Z",
        "commenceTimeTo": end + "T00:00:00Z",
    })
    url = f"{BASE}/sports/mma_mixed_martial_arts/odds?{q}"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            left = r.headers.get("x-requests-remaining")
            print(f"credits remaining: {left}", file=sys.stderr)
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: HTTP {e.code} {e.read().decode()[:200]}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: cannot reach the Odds API ({e.reason}). "
                 "Expected locally; run in GitHub Actions.")


def best_both(ev):
    """Best price per corner across every book quoting the fight."""
    best = {}
    for bk in ev.get("bookmakers", []):
        for mk in bk.get("markets", []):
            if mk.get("key") != "h2h":
                continue
            for oc in mk.get("outcomes", []):
                n, p = oc.get("name"), oc.get("price")
                if p is None:
                    continue
                if n not in best or p > best[n]["price"]:
                    best[n] = {"price": p, "book": bk.get("title")}
    if len(best) != 2:
        return None
    (a, da), (b, db) = best.items()
    ia, ib = implied(da["price"]), implied(db["price"])
    tot = ia + ib
    da["true"], db["true"] = ia / tot * 100, ib / tot * 100
    hold = (tot - 1) * 100
    return {"a": {"name": a, **da}, "b": {"name": b, **db},
            "hold": hold, "books": len(ev.get("bookmakers", []))}


def read_for(f, all_holds):
    """
    One line per fight, derived from the numbers rather than written fresh —
    a generator must not invent opinions it can't verify on regeneration.
    """
    fav = f["a"] if f["a"]["true"] >= f["b"]["true"] else f["b"]
    dog = f["b"] if fav is f["a"] else f["a"]
    gap = abs(f["a"]["true"] - f["b"]["true"])
    if gap < 5:
        return ("A genuine coin flip — the market can't separate them, and at "
                f"{f['hold']:.1f}% margin this is among the cheapest bets on the card.")
    if fav["true"] >= 80:
        return (f"Heavy chalk. {fav['name']} is a true {fav['true']:.0f}% — "
                f"{dog['name']} backers are being paid {dog['price']:+d} to disagree.")
    if f["hold"] < 0:
        return ("The books disagree on this one enough that shopping both corners "
                "flips the margin negative — best of both sides beats the market.")
    if f["hold"] == min(all_holds):
        return (f"The best-priced fight on the card — shopping both corners "
                f"leaves just {f['hold']:.1f}% to the house.")
    return (f"The market makes {fav['name']} {fav['true']:.0f}/{dog['true']:.0f}. "
            f"Break-even on the dog at {dog['price']:+d} is {implied(dog['price'])*100:.0f}%.")


def fmt_time(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    # US Central, summer (UTC-5). Card-day only, so a fixed offset is fine.
    from datetime import timedelta
    ct = dt - timedelta(hours=5)
    return ct.strftime("%-I:%M %p CT")


def build(events, title, venue, datestr):
    fights = []
    for ev in sorted(events, key=lambda e: e.get("commence_time", ""), reverse=True):
        f = best_both(ev)
        if not f:
            continue
        f["time"] = fmt_time(ev["commence_time"])
        f["iso"] = ev["commence_time"]
        fights.append(f)
    if not fights:
        sys.exit("ERROR: no priced fights in the window — refusing to write an empty page.")

    holds = [f["hold"] for f in fights]
    for f in fights:
        f["read"] = read_for(f, holds)

    main = fights[0]                    # latest start = main event
    closest = min(fights, key=lambda f: abs(f["a"]["true"] - f["b"]["true"]))
    cheapest = min(fights, key=lambda f: f["hold"])
    heaviest = max(fights, key=lambda f: max(f["a"]["true"], f["b"]["true"]))
    hfav = heaviest["a"] if heaviest["a"]["true"] > heaviest["b"]["true"] else heaviest["b"]

    stamp = datetime.now(timezone.utc).strftime("%b %-d, %Y %H:%M UTC")
    e = html.escape

    def frow(f, feature=False):
        a, b = f["a"], f["b"]
        cls = "fight feature" if feature else "fight"
        return f"""
      <div class="{cls}">
        <div class="f-top"><span class="f-time">{e(f['time'])}</span>
          <span class="f-hold">house edge {f['hold']:.1f}% · {f['books']} books</span></div>
        <div class="f-grid">
          <div class="corner"><div class="f-name">{e(a['name'])}</div>
            <div class="f-price">{a['price']:+d}</div>
            <div class="f-book">best: {e(a['book'])}</div>
            <div class="f-true">{a['true']:.1f}% true</div></div>
          <div class="vs">vs</div>
          <div class="corner"><div class="f-name">{e(b['name'])}</div>
            <div class="f-price">{b['price']:+d}</div>
            <div class="f-book">best: {e(b['book'])}</div>
            <div class="f-true">{b['true']:.1f}% true</div></div>
        </div>
        <div class="f-read">{e(f['read'])}</div>
      </div>"""

    rows = frow(main, True) + "".join(frow(f) for f in fights[1:])

    ld = {
        "@context": "https://schema.org", "@type": "SportsEvent",
        "name": title, "sport": "Mixed Martial Arts",
        "startDate": min(f["iso"] for f in fights),
        "location": {"@type": "Place", "name": venue},
        "description": f"Every fight on the {title} card with the best available "
                       "moneyline across major sportsbooks and each fighter's true "
                       "win probability once the bookmaker's margin is removed.",
        "organizer": {"@type": "Organization", "name": "UFC"},
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": "https://insidethenumber.com/"},
            {"@type": "ListItem", "position": 2, "name": "UFC",
             "item": "https://insidethenumber.com/ufc.html"}]}

    desc = (f"{title} odds — every fight priced across major sportsbooks. Best "
            "moneyline on both corners, true win probability with the vig removed, "
            "and what the house keeps on each fight.")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{e(title)} Odds — Best Price on Every Fight | Inside the Number</title>
<meta name="description" content="{e(desc)}"/>
<link rel="canonical" href="https://insidethenumber.com/ufc.html"/>
<meta name="theme-color" content="#050608"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"/>
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Inside the Number"/>
<meta property="og:url" content="https://insidethenumber.com/ufc.html"/>
<meta property="og:title" content="{e(title)} — every fight at its true price"/>
<meta property="og:description" content="{e(desc)}"/>
<meta property="og:image" content="https://insidethenumber.com/og-image.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="https://insidethenumber.com/og-image.png"/>
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(crumbs)}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=Barlow:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
  :root {{
    --black:#050608; --border:#1c2129; --border-lit:#2a2f3a;
    --surface-1:#0e1116; --surface-2:#141821;
    --green:#00d084; --green-deep:#007a4d; --green-dim:rgba(0,208,132,0.12);
    --blue:#3ba7ff; --red:#ff5c5c; --gold:#f0b429;
    --white:#f0f2f5; --muted:#6b7280; --mid:#9ca3af;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Barlow',sans-serif; background:var(--black); color:var(--white); line-height:1.6; }}
  body::before {{ content:''; position:fixed; inset:0; z-index:-1; pointer-events:none;
    background:
      linear-gradient(rgba(255,255,255,0.11) 1px, transparent 1px) 0 0 / 100% 64px,
      linear-gradient(90deg, rgba(255,255,255,0.11) 1px, transparent 1px) 0 0 / 64px 100%,
      radial-gradient(ellipse 65% 28% at 8% 10%, rgba(0,208,132,0.38) 0%, transparent 62%),
      radial-gradient(ellipse 58% 24% at 94% 32%, rgba(59,167,255,0.34) 0%, transparent 60%); }}
  nav {{ background:rgba(5,6,8,0.9); backdrop-filter:blur(14px); border-bottom:1px solid var(--border);
    padding:0 48px; display:flex; align-items:center; justify-content:space-between; height:60px;
    position:sticky; top:0; z-index:100; }}
  .nav-brand {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
  .nav-name {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:20px;
    letter-spacing:0.04em; text-transform:uppercase; color:var(--white); }}
  .nav-name span {{ color:var(--green); }}
  .nav-links {{ display:flex; gap:26px; list-style:none; }}
  .nav-links a {{ color:#b6bdc8; text-decoration:none; font-size:13px; font-weight:500;
    letter-spacing:0.06em; text-transform:uppercase; }}
  .nav-links a:hover {{ color:var(--green); }}
  .wrap {{ max-width:860px; margin:0 auto; padding:44px 24px 60px; }}
  .eyebrow {{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--green);
    letter-spacing:0.18em; text-transform:uppercase; margin-bottom:10px; }}
  h1 {{ font-family:'Barlow Condensed',sans-serif; font-size:clamp(34px,5vw,56px); font-weight:900;
    text-transform:uppercase; line-height:0.98; }}
  h1 span {{ background:linear-gradient(100deg,var(--green),var(--blue));
    -webkit-background-clip:text; background-clip:text; color:transparent; }}
  .sub {{ color:var(--mid); font-weight:300; margin:14px 0 6px; max-width:640px; }}
  .stamp {{ font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:var(--muted); margin-bottom:26px; }}
  .strip {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:22px 0 30px; }}
  .chip {{ background:var(--surface-1); border:1px solid var(--border); border-radius:12px; padding:13px 15px; }}
  .chip .l {{ font-family:'IBM Plex Mono',monospace; font-size:8.5px; color:var(--muted);
    letter-spacing:0.13em; text-transform:uppercase; margin-bottom:5px; }}
  .chip .v {{ font-family:'Barlow Condensed',sans-serif; font-size:17px; font-weight:800; }}
  .chip .s {{ font-size:11.5px; color:var(--mid); }}
  .fight {{ background:var(--surface-1); border:1px solid var(--border); border-radius:14px;
    padding:18px 20px; margin-bottom:14px; }}
  .fight.feature {{ border-top:3px solid var(--green); background:var(--surface-2); }}
  .f-top {{ display:flex; justify-content:space-between; margin-bottom:12px; }}
  .f-time {{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--blue); letter-spacing:0.1em; }}
  .f-hold {{ font-family:'IBM Plex Mono',monospace; font-size:9.5px; color:var(--muted);
    letter-spacing:0.06em; text-transform:uppercase; }}
  .f-grid {{ display:grid; grid-template-columns:1fr auto 1fr; gap:14px; align-items:center; }}
  .corner {{ text-align:center; }}
  .f-name {{ font-family:'Barlow Condensed',sans-serif; font-size:19px; font-weight:800;
    text-transform:uppercase; letter-spacing:0.02em; }}
  .f-price {{ font-family:'IBM Plex Mono',monospace; font-size:22px; font-weight:600;
    color:var(--green); margin:2px 0; }}
  .f-book {{ font-size:11px; color:var(--muted); }}
  .f-true {{ font-family:'IBM Plex Mono',monospace; font-size:11.5px; color:var(--mid); margin-top:3px; }}
  .vs {{ font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--muted); }}
  .f-read {{ border-top:1px solid var(--border); margin-top:13px; padding-top:11px;
    font-size:13px; color:var(--mid); font-weight:300; }}
  .expl {{ border-top:1px solid var(--border); margin-top:26px; padding-top:18px;
    font-size:13px; color:var(--mid); font-weight:300; }}
  .cta {{ background:var(--green-dim); border:1px solid var(--green); border-radius:14px;
    padding:20px 22px; margin-top:26px; }}
  .cta a {{ color:var(--green); font-weight:600; text-decoration:none; }}
  footer {{ border-top:1px solid var(--border); padding:26px 24px 34px; text-align:center; }}
  .foot-d {{ font-size:11px; color:var(--muted); max-width:640px; margin:0 auto 8px; }}
  .foot-c {{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--muted); }}
  @media (max-width:640px) {{
    nav {{ padding:0 18px; }} .nav-links {{ display:none; }}
    .strip {{ grid-template-columns:1fr; }}
    .f-grid {{ gap:8px; }} .f-name {{ font-size:16px; }} .f-price {{ font-size:18px; }}
  }}
</style>
</head>
<body>
<nav>
  <a class="nav-brand" href="index.html"><span class="nav-name">Inside <span>the</span> Number</span></a>
  <ul class="nav-links">
    <li><a href="index.html">Home</a></li>
    <li><a href="games.html">Games</a></li>
    <li><a href="dfs.html">DFS</a></li>
    <li><a href="tools.html">Tools</a></li>
    <li><a href="learn.html">Learn</a></li>
  </ul>
</nav>
<div class="wrap">
  <div class="eyebrow">// UFC · {e(datestr)} · {e(venue)}</div>
  <h1>{e(title)}<br/><span>every fight at its true price.</span></h1>
  <p class="sub">The best available moneyline on both corners across major sportsbooks,
    and what each fighter's price really says once the bookmaker's margin comes out.
    ESPN doesn't carry MMA odds. We do.</p>
  <div class="stamp">Prices updated {stamp} · best of {max(f['books'] for f in fights)} books</div>

  <div class="strip">
    <div class="chip"><div class="l">Closest fight</div>
      <div class="v">{e(closest['a']['name'].split()[-1])} / {e(closest['b']['name'].split()[-1])}</div>
      <div class="s">{closest['a']['true']:.0f} / {closest['b']['true']:.0f} — a real coin flip</div></div>
    <div class="chip"><div class="l">Cheapest to bet</div>
      <div class="v">{cheapest['hold']:.1f}% house edge</div>
      <div class="s">{e(cheapest['a']['name'].split()[-1])} vs {e(cheapest['b']['name'].split()[-1])} after shopping</div></div>
    <div class="chip"><div class="l">Heaviest favorite</div>
      <div class="v">{e(hfav['name'])}</div>
      <div class="s">a true {hfav['true']:.0f}% — priced {hfav['price']:+d}</div></div>
  </div>
{rows}
  <p class="expl"><b>How to read this.</b> Both corners of any fight add up to more than
    100% at the posted prices — the surplus is the bookmaker's margin, and it's what you're
    charged to bet. Strip it out and what's left is the true probability: what the market
    actually thinks. "Best" is the strongest price any major book is offering on that corner
    right now; taking the best number on your side is the single highest-return habit in
    betting.</p>
  <div class="cta"><b>One free pick every morning, with the reasoning shown.</b><br/>
    <a href="https://insidethenumber.beehiiv.com/subscribe" target="_blank" rel="noopener">
    Get it in your inbox →</a></div>
</div>
<footer>
  <div class="foot-d">For entertainment purposes only. Inside the Number does not facilitate
    gambling. Odds shown are from licensed data feeds and may differ from your book.
    Please gamble responsibly.</div>
  <div class="foot-c">© 2026 ITN · Nashville, TN</div>
</footer>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--title", default="UFC Fight Night Shanghai")
    ap.add_argument("--venue", default="Shanghai, China")
    ap.add_argument("--datestr", default="Sat, Aug 29")
    ap.add_argument("--out", default=os.path.join(ROOT, "ufc.html"))
    a = ap.parse_args()

    events = fetch(a.start, a.end)
    print(f"{len(events)} events in window", file=sys.stderr)
    page = build(events, a.title, a.venue, a.datestr)
    with open(a.out, "w") as fh:
        fh.write(page)
    print(f"wrote {a.out} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
