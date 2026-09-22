#!/usr/bin/env python3
"""Build one crawlable weekly NFL and college-football hub from ESPN's public feed.

The live board is intentionally interactive. This page is the small, stable
search doorway: current NFL games and ranked college-football matchups in HTML,
with links into the live board for the complete slate. It is not a picks page.
"""

import argparse
import html
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from build_slate import get, enrich

ROOT = Path(__file__).resolve().parent.parent
CENTRAL = ZoneInfo("America/Chicago")
LEAGUES = (("NFL", "football/nfl"), ("CFB", "football/college-football"))


def market(block, side, field="odds", when="close"):
    value = (((block or {}).get(side) or {}).get(when) or {}).get(field)
    return value if value not in (None, "") else None


def fetch_day(day):
    games = []
    ymd = day.strftime("%Y%m%d")
    for league, path in LEAGUES:
        data = get(f"https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard?dates={ymd}")
        if not data:
            continue
        for event in data.get("events", []):
            if ((event.get("status", {}).get("type", {}) or {}).get("state")) != "pre":
                continue
            competition = (event.get("competitions") or [{}])[0]
            sides = {side.get("homeAway"): side for side in competition.get("competitors", [])}
            away, home = sides.get("away", {}), sides.get("home", {})
            odds = (competition.get("odds") or [{}])[0]
            away_team, home_team = away.get("team") or {}, home.get("team") or {}
            game = {
                "league": league,
                "start": event.get("date"),
                "away": {"abbr": away_team.get("abbreviation", "Away"), "name": away_team.get("shortDisplayName", "Away")},
                "home": {"abbr": home_team.get("abbreviation", "Home"), "name": home_team.get("shortDisplayName", "Home")},
                "rank_away": ((away.get("curatedRank") or {}).get("current")),
                "rank_home": ((home.get("curatedRank") or {}).get("current")),
                "spread": market(odds.get("pointSpread"), "away", "line"),
                "total": market(odds.get("total"), "over", "line") or odds.get("overUnder"),
                "ml_away": market(odds.get("moneyline"), "away") or (odds.get("awayTeamOdds") or {}).get("moneyLine"),
                "ml_home": market(odds.get("moneyline"), "home") or (odds.get("homeTeamOdds") or {}).get("moneyLine"),
            }
            games.append(enrich(game))
    return games


def kickoff(iso):
    if not iso:
        return "Kickoff TBA"
    value = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(CENTRAL)
    return value.strftime("%a, %b %-d · %-I:%M %p CT")


def team_name(team, rank):
    label = html.escape(team["name"])
    return f"#{rank} {label}" if rank and rank <= 25 else label


def game_row(game):
    away = team_name(game["away"], game.get("rank_away"))
    home = team_name(game["home"], game.get("rank_home"))
    spread = html.escape(str(game["spread"])) if game.get("spread") is not None else "Line pending"
    total = html.escape(str(game["total"])) if game.get("total") is not None else "Total pending"
    fair = ""
    if game.get("true_away") is not None and game.get("true_home") is not None:
        fair = f"<span>Fair win chance: {game['true_away']}% / {game['true_home']}%</span>"
    return f'''<article class="game">
  <div class="kickoff">{kickoff(game.get("start"))}</div>
  <h3>{away} <b>at</b> {home}</h3>
  <div class="numbers"><span>Spread: {spread}</span><span>Total: {total}</span>{fair}</div>
</article>'''


def build(games, stamp):
    nfl = sorted((g for g in games if g["league"] == "NFL"), key=lambda g: g.get("start") or "")
    ranked_cfb = sorted(
        (g for g in games if g["league"] == "CFB" and any(r and r <= 25 for r in (g.get("rank_away"), g.get("rank_home")))),
        key=lambda g: g.get("start") or "",
    )
    cfb_rows = "".join(game_row(g) for g in ranked_cfb) or "<p class=\"empty\">No ranked college-football games are currently posted for this window.</p>"
    nfl_rows = "".join(game_row(g) for g in nfl) or "<p class=\"empty\">No upcoming NFL games are currently posted for this window.</p>"
    date_label = stamp.strftime("%B %-d, %Y")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>This Week's NFL & College Football Odds | Inside the Number</title>
<meta name="description" content="This week's NFL games and ranked college-football matchups with current spreads, totals and no-vig fair win chances. Updated from the live feed.">
<link rel="canonical" href="https://insidethenumber.com/weekly-football-odds">
<meta property="og:type" content="website">
<meta property="og:title" content="This Week's NFL & College Football Odds">
<meta property="og:description" content="Current spreads, totals and fair win chances from the live board.">
<meta property="og:url" content="https://insidethenumber.com/weekly-football-odds">
<meta property="og:site_name" content="Inside the Number">
<meta property="og:image" content="https://insidethenumber.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"This Week's NFL and College Football Odds","url":"https://insidethenumber.com/weekly-football-odds","description":"A current weekly collection of NFL games and ranked college-football matchups with spreads, totals and no-vig fair win chances.","isPartOf":{{"@type":"WebSite","name":"Inside the Number","url":"https://insidethenumber.com/"}}}}</script>
<style>
  :root{{--bg:#050608;--panel:#0d1218;--line:#23303b;--text:#f0f2f5;--muted:#97a1ad;--green:#00d084;--blue:#3ba7ff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:Arial,sans-serif}}nav{{padding:18px max(22px,calc((100vw - 1120px)/2));border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;align-items:center}}nav a{{color:var(--muted);text-decoration:none;font-size:14px}}.brand{{font-weight:800;color:var(--text)}}.brand span{{color:var(--green)}}main{{max-width:1120px;margin:auto;padding:60px 22px 80px}}.eyebrow{{color:var(--green);font:12px monospace;letter-spacing:.12em;text-transform:uppercase}}h1{{font-size:clamp(40px,7vw,76px);line-height:.94;margin:16px 0}}h1 span{{color:var(--green)}}.intro{{max-width:720px;color:var(--muted);line-height:1.65;font-size:17px}}.stamp{{font:12px monospace;color:var(--muted);margin:24px 0 46px}}section{{margin-top:52px}}h2{{font-size:27px;margin:0 0 10px}}.section-copy{{color:var(--muted);margin:0 0 18px;line-height:1.6}}.games{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}.game{{border:1px solid var(--line);background:var(--panel);padding:18px;border-radius:8px}}.kickoff{{font:11px monospace;color:var(--green);margin-bottom:10px}}h3{{margin:0;font-size:20px;line-height:1.2}}h3 b{{color:var(--muted);font-size:13px;margin:0 5px}}.numbers{{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px}}.numbers span{{font:12px monospace;color:#c9d0d8;border-left:2px solid var(--blue);padding-left:7px}}.cta{{display:inline-block;margin-top:28px;padding:14px 18px;background:var(--green);color:#04100b;font-weight:800;text-decoration:none;border-radius:6px}}.fine{{margin-top:18px;color:var(--muted);font-size:13px;line-height:1.6}}.empty{{color:var(--muted)}}@media(max-width:700px){{.games{{grid-template-columns:1fr}}main{{padding-top:42px}}nav{{align-items:flex-start;flex-direction:column;gap:10px}}}}
</style>
</head>
<body>
<nav><a class="brand" href="/">Inside <span>the</span> Number</a><div><a href="/games?sport=NFL&scope=week">NFL board</a> &nbsp; <a href="/games?sport=CFB&scope=week">CFB board</a> &nbsp; <a href="/learn">Learn</a></div></nav>
<main>
  <div class="eyebrow">Football odds · current weekly window</div>
  <h1>Every week.<br><span>Every number.</span></h1>
  <p class="intro">A crawlable view of this week's NFL slate and ranked college-football matchups. The live board carries every game; this page explains the price the market is posting without pretending it is a pick.</p>
  <p class="stamp">Updated from the public feed: {date_label} · Times shown in Central</p>
  <section><h2>NFL this week</h2><p class="section-copy">Spread, total and the fair win chance after the sportsbook margin is removed.</p><div class="games">{nfl_rows}</div><a class="cta" href="/games?sport=NFL&scope=week">Open the full NFL board</a></section>
  <section><h2>Ranked college football</h2><p class="section-copy">Every upcoming game in the weekly window involving an AP Top 25 team.</p><div class="games">{cfb_rows}</div><a class="cta" href="/games?sport=CFB&scope=week">Open the full college-football board</a></section>
  <p class="fine">Lines move. This page is a market-reading reference, not betting advice. Check the live board for the current number before relying on any price.</p>
</main>
</body>
</html>'''


def update_sitemap():
    path = ROOT / "sitemap.xml"
    text = path.read_text()
    today = datetime.now(CENTRAL).strftime("%Y-%m-%d")
    block = f'''  <url>\n    <loc>https://insidethenumber.com/weekly-football-odds</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n'''
    if "https://insidethenumber.com/weekly-football-odds" in text:
        text = re.sub(r"  <url>\s*<loc>https://insidethenumber\.com/weekly-football-odds</loc>.*?  </url>\s*", block, text, flags=re.S)
    else:
        text = text.replace("</urlset>", block + "</urlset>")
    path.write_text(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="weekly-football-odds.html")
    args = parser.parse_args()
    now = datetime.now(CENTRAL)
    games = []
    for offset in range(7):
        games.extend(fetch_day(now.date() + timedelta(days=offset)))
    Path(args.out).write_text(build(games, now))
    update_sitemap()
    print(f"wrote {args.out}: {sum(g['league'] == 'NFL' for g in games)} NFL, {sum(g['league'] == 'CFB' for g in games)} CFB games")


if __name__ == "__main__":
    main()
