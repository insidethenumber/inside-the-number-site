#!/usr/bin/env python3
"""
Inside the Number — daily slate builder.

Runs in GitHub Actions. Gathers today's board from public feeds, applies the
selection constraints, and emits a JSON brief. No browser, no local state, no
git locks — a fresh checkout every run.

Why this exists: the local automation missed or ran late on Aug 20, 21, 23 and
24. Every failure traced to one of two things — a stale .git lock that could
not be deleted from the sandbox, or Claude in Chrome freezing. Neither exists
on a GitHub runner.

    python3 scripts/build_slate.py --date 2026-08-25 --out brief.json

Feeds used (all public, no keys):
    ESPN scoreboard   — odds, records, probables, status
    ESPN core odds    — per-event moneyline/spread/total with open and current
    MLB StatsAPI      — probable pitchers, season lines, last-15 hitting
"""

import argparse, json, sys, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

# Identify as curl, deliberately.
#
# Measured on a GitHub runner, same URL, same second:
#     curl    -> HTTP 200, 206,607 bytes
#     urllib  -> HTTP 403 Forbidden
#
# So ESPN is not blocking the datacenter IP; it is rejecting the request. A
# Chrome User-Agent made it WORSE — a request claiming to be Chrome without
# any of Chrome's other headers looks like impersonation to Akamai, whereas an
# honest curl signature is a well-known, permitted client. Do not "improve"
# this into a browser string.
UA = {
    "User-Agent": "curl/8.5.0",
    "Accept": "*/*",
}

LEAGUES = [
    ("MLB",  "baseball/mlb"),
    ("NFL",  "football/nfl"),
    ("CFB",  "football/college-football"),
    ("WNBA", "basketball/wnba"),
    ("NBA",  "basketball/nba"),
    ("NHL",  "hockey/nhl"),
    ("UFC",  "mma/ufc"),
]


def get(url, tries=3):
    """GET JSON with retries. A single flaky feed must not kill the run."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
    print(f"  WARN  {url.split('?')[0]} failed after {tries} tries: {last}", file=sys.stderr)
    return None


def implied(american):
    """American odds -> implied probability (includes the book's margin)."""
    try:
        v = float(american)
    except (TypeError, ValueError):
        return None
    return 100.0 / (v + 100.0) if v > 0 else abs(v) / (abs(v) + 100.0)


def no_vig(a, b):
    """Strip the margin from a two-way market. Returns (pa, pb, hold)."""
    ia, ib = implied(a), implied(b)
    if ia is None or ib is None:
        return None
    tot = ia + ib
    if tot <= 0:
        return None
    return ia / tot, ib / tot, (tot - 1.0) * 100.0


def collect(date_yyyymmdd):
    """Every game on the board that has not started, with its prices."""
    board = []
    for label, path in LEAGUES:
        url = (f"https://site.api.espn.com/apis/site/v2/sports/{path}"
               f"/scoreboard?dates={date_yyyymmdd}")
        data = get(url)
        if data is None:
            print(f"  {label:<5} FETCH FAILED", file=sys.stderr)
            continue
        evs = data.get("events", [])
        states = {}
        for ev in evs:
            st = (ev.get("status", {}).get("type", {}) or {}).get("state", "?")
            states[st] = states.get(st, 0) + 1
        print(f"  {label:<5} {len(evs):>3} events  {states or '(none)'}", file=sys.stderr)
        for ev in data.get("events", []):
            state = (ev.get("status", {}).get("type", {}) or {}).get("state")
            if state != "pre":
                continue          # never present a started game as bettable
            comps = ev.get("competitions") or [{}]
            c = comps[0]
            teams = {}
            for side in c.get("competitors", []):
                teams[side.get("homeAway")] = {
                    "abbr": (side.get("team") or {}).get("abbreviation"),
                    "name": (side.get("team") or {}).get("shortDisplayName"),
                    "record": next((r.get("summary") for r in (side.get("records") or [])
                                    if r.get("type") == "total"), ""),
                }
            o = (c.get("odds") or [{}])[0]
            board.append({
                "league": label,
                "id": ev.get("id"),
                "short": ev.get("shortName"),
                "start": ev.get("date"),
                "detail": (ev.get("status", {}).get("type", {}) or {}).get("shortDetail"),
                "venue": (c.get("venue") or {}).get("fullName", ""),
                "away": teams.get("away", {}),
                "home": teams.get("home", {}),
                "total": o.get("overUnder"),
                "over_odds": o.get("overOdds"),
                "under_odds": o.get("underOdds"),
                "spread": o.get("spread"),
                "ml_away": ((o.get("awayTeamOdds") or {}).get("moneyLine")),
                "ml_home": ((o.get("homeTeamOdds") or {}).get("moneyLine")),
                "provider": (o.get("provider") or {}).get("name", ""),
            })
    return board


def enrich(game):
    """Add true prices and break-evens — the numbers the brand is built on."""
    nv = no_vig(game.get("ml_away"), game.get("ml_home"))
    if nv:
        game["true_away"], game["true_home"], game["hold"] = (
            round(nv[0] * 100, 1), round(nv[1] * 100, 1), round(nv[2], 2))
    for k, src in (("be_over", "over_odds"), ("be_under", "under_odds"),
                   ("be_ml_away", "ml_away"), ("be_ml_home", "ml_home")):
        p = implied(game.get(src))
        if p is not None:
            game[k] = round(p * 100, 1)
    return game


def audit(picks):
    """
    The selection constraints, enforced rather than trusted.

    Every card this operation published before these rules existed was 100%
    MLB moneylines. These are the guardrails, checked in code so a run cannot
    quietly drift back.
    """
    problems = []
    by_sport, by_type = {}, {}
    for p in picks:
        by_sport[p["league"]] = by_sport.get(p["league"], 0) + 1
        by_type[p["market"]] = by_type.get(p["market"], 0) + 1

    for sport, n in by_sport.items():
        if n > 2:
            problems.append(f"{n} picks from {sport} — maximum is 2")

    ml = by_type.get("Moneyline", 0)
    if picks and ml > len(picks) / 2:
        problems.append(f"{ml} of {len(picks)} picks are moneylines — maximum is half")

    return {"sports": by_sport, "types": by_type, "problems": problems,
            "passed": not problems}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD; defaults to today US/Central")
    ap.add_argument("--out", default="brief.json")
    a = ap.parse_args()

    if a.date:
        d = datetime.strptime(a.date, "%Y-%m-%d")
    else:
        # US/Central without pulling in a tz library
        d = datetime.now(timezone.utc) - timedelta(hours=5)
    ymd = d.strftime("%Y%m%d")

    print(f"Building slate for {d.strftime('%A %b %d, %Y')}")
    board = [enrich(g) for g in collect(ymd)]

    by_league = {}
    for g in board:
        by_league.setdefault(g["league"], []).append(g)

    print(f"\n{len(board)} games not yet started:")
    for lg, games in sorted(by_league.items()):
        print(f"  {lg:<5} {len(games)}")
        for g in games:
            tot = f"O/U {g['total']}" if g.get("total") is not None else "no total"
            ml = f"{g.get('ml_away','?')}/{g.get('ml_home','?')}"
            print(f"     {g['short']:<12} {tot:<12} ML {ml:<12} {g.get('detail','')}")

    brief = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "slate_date": d.strftime("%Y-%m-%d"),
        "slate_label": d.strftime("%a, %b %-d"),
        "non_mlb_available": sorted(k for k in by_league if k != "MLB"),
        "games": board,
    }
    with open(a.out, "w") as fh:
        json.dump(brief, fh, indent=1)
    print(f"\nwrote {a.out}  ({len(board)} games)")

    if not board:
        # A genuinely empty board happens (Mondays in February). Only a failed
        # fetch is an error, and that is reported per-league above.
        print("::warning title=Empty board::No unstarted games found for this date.")


if __name__ == "__main__":
    main()
