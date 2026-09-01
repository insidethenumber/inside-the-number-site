#!/usr/bin/env python3
"""
Inside the Number — per-game static pages.

The single biggest SEO gap: games.html is client-rendered, so Google sees
"Loading today's board" and none of the numbers we compute. This script turns
data/brief-latest.json — already produced daily by the reliable daily-slate
workflow — into one static, indexable page per game under g/.

Pure transform, no network. If the brief exists, this cannot fail for any
reason the slate build didn't already fail for.

    python3 scripts/build_game_pages.py            # today's brief
    python3 scripts/build_game_pages.py --brief data/brief-2026-08-25.json

Pages accumulate: ~16 a day, ~480 a month of long-tail entries like
"Red Sox vs Marlins odds August 25". Each page states the matchup, the
prices, the no-vig win chances and the break-evens — the things we compute
that a bare odds page doesn't carry.
"""

import argparse, glob, html, json, os, re, sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOT, "g")

MONTHS = ["January","February","March","April","May","June","July","August",
          "September","October","November","December"]


def e(s):
    return html.escape(str(s), quote=True)


def pretty_date(iso):                      # "2026-08-25" -> "August 25, 2026"
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m)-1]} {int(d)}, {y}"


def slug(g, date):
    a = re.sub(r"[^a-z0-9]", "", g["away"]["abbr"].lower())
    h = re.sub(r"[^a-z0-9]", "", g["home"]["abbr"].lower())
    return f"{date}-{a}-{h}"


def fmt_odds(v):
    """'-140' / '+131' / None -> display string."""
    if v in (None, "", "None"):
        return "—"
    s = str(v)
    return s if s.startswith(("+", "-")) else f"+{s}"


CSS = """
:root{--bg:#050608;--s1:#0e1116;--s2:#141821;--bd:#1c2129;--green:#00d084;
--blue:#3ba7ff;--white:#f0f2f5;--mid:#9ca3af;--muted:#6b7280}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Barlow',system-ui,sans-serif;background:var(--bg);color:var(--white);line-height:1.6}
nav{border-bottom:1px solid var(--bd);padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between}
nav a{color:var(--white);text-decoration:none;font-weight:800;font-size:18px;letter-spacing:.04em;text-transform:uppercase}
nav a span{color:var(--green)}
nav .r{font-size:12px;letter-spacing:.08em;text-transform:uppercase}
nav .r a{font-size:12px;color:#b6bdc8;font-weight:500;margin-left:18px}
.wrap{max-width:760px;margin:0 auto;padding:36px 20px 56px}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--green);letter-spacing:.18em;text-transform:uppercase;margin-bottom:10px}
h1{font-family:'Barlow Condensed',sans-serif;font-size:clamp(30px,5vw,46px);font-weight:900;text-transform:uppercase;line-height:1.02}
h1 span{color:var(--green)}
.meta{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);margin:10px 0 24px}
h2{font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;text-transform:uppercase;margin:26px 0 10px}
table{width:100%;border-collapse:collapse;background:var(--s1);border:1px solid var(--bd);border-radius:12px;overflow:hidden}
th{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;text-align:left;padding:11px 13px;border-bottom:1px solid var(--bd)}
td{padding:9px 13px;font-size:13.5px;border-bottom:1px solid rgba(255,255,255,.04)}
tr:last-child td{border-bottom:none}
td.n{font-family:'IBM Plex Mono',monospace}
td.g{font-family:'IBM Plex Mono',monospace;color:var(--green)}
th:nth-child(n+2),td:nth-child(n+2){text-align:right}
p.x{font-size:14px;color:var(--mid);font-weight:300;margin:14px 0;max-width:64ch}
p.x b{color:var(--white)}
.foot{border-top:1px solid var(--bd);margin-top:34px;padding-top:16px;font-size:12px;color:var(--muted)}
.foot a{color:var(--green);text-decoration:none}
.cta{margin:28px 0 6px;padding:18px 20px;border:1px solid rgba(0,208,132,.28);border-radius:12px;background:rgba(0,208,132,.05)}
.cta .k{font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:var(--green);letter-spacing:.16em;text-transform:uppercase;margin-bottom:6px}
.cta p{font-size:14px;color:var(--mid);font-weight:300;margin:0 0 12px;max-width:60ch}
.cta p b{color:var(--white);font-weight:600}
.cta a.go{display:inline-block;font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:15px;letter-spacing:.05em;text-transform:uppercase;color:#050608;background:linear-gradient(90deg,var(--green),var(--blue));padding:9px 16px;border-radius:8px;text-decoration:none}
@media(max-width:640px){td,th{padding:8px 9px;font-size:12.5px}}
"""


def build_page(g, date):
    a, h = g["away"], g["home"]
    title = f"{a['name']} vs {h['name']} Odds & True Price — {pretty_date(date)}"
    desc = (f"{a['name']} at {h['name']} on {pretty_date(date)}: moneyline "
            f"{fmt_odds(g.get('ml_away'))}/{fmt_odds(g.get('ml_home'))}, total "
            f"{g.get('total','—')}, and the no-vig win chance on both sides — "
            f"what the market really thinks, before the book's cut.")
    fn = slug(g, date) + ".html"
    # Cloudflare serves /g/slug and 301s /g/slug.html, so the .html form can
    # never be indexed. Advertise the URL that returns 200.
    canon = f"https://insidethenumber.com/g/{fn[:-5]}"

    ta, th_ = g.get("true_away"), g.get("true_home")
    hold = g.get("hold")

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "SportsEvent",
        "name": f"{a['name']} at {h['name']}",
        "sport": "Baseball" if g["league"] == "MLB" else g["league"],
        "startDate": g.get("start", date),
        "location": {"@type": "Place", "name": g.get("venue", "")},
        "competitor": [
            {"@type": "SportsTeam", "name": a["name"]},
            {"@type": "SportsTeam", "name": h["name"]},
        ]})

    rows = []
    rows.append(f"<tr><td>Moneyline</td><td class='g'>{fmt_odds(g.get('ml_away'))}"
                f"</td><td class='g'>{fmt_odds(g.get('ml_home'))}</td></tr>")
    if g.get("spread") not in (None, "", "None"):
        rows.append(f"<tr><td>Run line</td><td class='n' colspan='2'>"
                    f"{e(g['spread'])}</td></tr>")
    if g.get("total") not in (None, "", "None"):
        tot = str(g["total"]).lstrip("ou")
        rows.append(f"<tr><td>Total {e(tot)}</td><td class='n'>Over "
                    f"{fmt_odds(g.get('over_odds'))}</td><td class='n'>Under "
                    f"{fmt_odds(g.get('under_odds'))}</td></tr>")

    true_block = ""
    if ta is not None and th_ is not None:
        true_block = f"""
  <h2>What the market really thinks</h2>
  <table>
    <tr><th></th><th>{e(a['abbr'])}</th><th>{e(h['abbr'])}</th></tr>
    <tr><td>Win chance (no-vig)</td><td class='g'>{ta:.1f}%</td><td class='g'>{th_:.1f}%</td></tr>
    <tr><td>Break-even at the price</td><td class='n'>{g.get('be_ml_away','—')}%</td><td class='n'>{g.get('be_ml_home','—')}%</td></tr>
  </table>
  <p class="x">Both posted prices together imply more than 100% — that surplus
  ({hold:.1f}% here) is what the book keeps. Strip it out and the market makes
  this <b>{e(a['abbr'])} {ta:.1f}%</b>, <b>{e(h['abbr'])} {th_:.1f}%</b>. The
  break-even row is the win rate you'd need at the posted price just to tread
  water — the gap between the two rows is the cost of the bet.</p>"""

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{e(title)} | Inside the Number</title>
<meta name="description" content="{e(desc)}"/>
<link rel="canonical" href="{canon}"/>
<meta property="og:title" content="{e(title)}"/>
<meta property="og:description" content="{e(desc)}"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:site_name" content="Inside the Number"/>
<meta property="og:image" content="https://insidethenumber.com/og-image.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<script type="application/ld+json">{ld}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800;900&family=Barlow:wght@300;400;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>{CSS}</style>
</head>
<body>
<nav><a href="/">Inside <span>the</span> Number</a>
  <div class="r"><a href="/games">Today's board</a><a href="/learn">Learn</a></div></nav>
<div class="wrap">
  <div class="eyebrow">// {e(g['league'])} · {e(pretty_date(date))}</div>
  <h1>{e(a['name'])} <span>at</span> {e(h['name'])}</h1>
  <div class="meta">{e(g.get('detail',''))} · {e(g.get('venue',''))} ·
    {e(a['abbr'])} {e(a.get('record',''))} — {e(h['abbr'])} {e(h.get('record',''))}
    · lines via {e(g.get('provider','the market'))}</div>

  <h2>The prices</h2>
  <table>
    <tr><th>Market</th><th>{e(a['abbr'])}</th><th>{e(h['abbr'])}</th></tr>
    {''.join(rows)}
  </table>
{true_block}
  <div class="cta">
    <div class="k">Every pick, in your inbox</div>
    <p>We take a side on three or four games a day and send every one to
    subscribers with the reasoning, before anything starts. <b>One is free on
    the homepage. The rest only go out by email.</b> No card, no spam.</p>
    <a class="go" href="/#signup">Get every pick free →</a>
  </div>
  <p class="x">Prices move all day. The live version of this game — score,
  line movement and the rest of the board — is on
  <a style="color:var(--green)" href="/games">today's board</a>.</p>

  <div class="foot">Inside the Number · every game priced at what the market
  really thinks · <a href="/">insidethenumber.com</a> · 21+ only. If gambling
  stops being fun, call 1-800-GAMBLER.</div>
</div>
</body>
</html>"""
    return fn, page


def rebuild_sitemap():
    """Every page under g/, newest first, into g/sitemap-games.xml."""
    urls = []
    for p in sorted(glob.glob(os.path.join(OUTDIR, "*.html")), reverse=True):
        fn = os.path.basename(p)
        m = re.match(r"(\d{4}-\d{2}-\d{2})-", fn)
        lastmod = m.group(1) if m else datetime.now(timezone.utc).date().isoformat()
        urls.append(f"  <url><loc>https://insidethenumber.com/g/{fn[:-5]}</loc>"
                    f"<lastmod>{lastmod}</lastmod></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(OUTDIR, "sitemap-games.xml"), "w") as fh:
        fh.write(xml)
    return len(urls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", default=os.path.join(ROOT, "data", "brief-latest.json"))
    a = ap.parse_args()

    brief = json.load(open(a.brief))
    date = brief["slate_date"]
    games = [g for g in brief.get("games", [])
             if g.get("away") and g.get("home")]
    if not games:
        sys.exit("brief has no games — refusing to write an empty day")

    os.makedirs(OUTDIR, exist_ok=True)
    written = 0
    for g in games:
        fn, page = build_page(g, date)
        with open(os.path.join(OUTDIR, fn), "w") as fh:
            fh.write(page)
        written += 1
    n = rebuild_sitemap()
    print(f"wrote {written} game pages for {date}; sitemap-games.xml now lists {n}")


if __name__ == "__main__":
    main()
