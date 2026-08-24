#!/usr/bin/env python3
"""
Inside the Number — reply ammunition.

Pre-computes the numbers that make a good X reply, so writing five of them is
fifteen minutes instead of an evening.

WHY THIS EXISTS
---------------
As of Aug 24 2026 the account had 0 followers and its three posts had drawn
3, 6 and 3 views. The scheduled queue works perfectly and reaches nobody,
because X gives a new account with no followers essentially no distribution on
standalone posts. Replies are the only lever that borrows someone else's
audience, and the account is already paying for Premium, whose one real
feature is reply prioritisation.

A good reply needs one exact number the original post left out. Digging that
number out by hand per post is the slow part -- so this does it in advance for
every game on the board.

WHAT IT PRODUCES
----------------
  1. Per-game house edge, so "this parlay leg costs you X%" is instant.
  2. The compounding table -- the single most useful stat this operation owns.
     Nobody publishes "stack ten legs and the book keeps 16.5%".
  3. Break-even for every posted price on the board, plus a reference ladder
     for the round numbers that show up in other people's posts.
  4. Probable starters with their real outs-recorded distribution, which is
     what every "over X.5 outs" prop turns on. Sourced from MLB's own game
     logs rather than a season average, because the average hides the shape.

Runs in GitHub Actions: the Claude sandbox cannot reach ESPN or statsapi.mlb.com
(tunnel 403), a runner can.

    python3 scripts/reply_ammo.py                 # today, US/Central
    python3 scripts/reply_ammo.py --date 2026-08-25
"""

import argparse, json, sys, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

# ESPN answers curl and refuses urllib's default UA. Measured, not guessed --
# see scripts/build_slate.py for the full note. Do not "improve" this into a
# browser string; a Chrome UA without Chrome's other headers does worse.
UA = {"User-Agent": "curl/8.5.0", "Accept": "*/*"}


def get(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=UA), timeout=25) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
    print(f"  WARN {url.split('?')[0]} failed: {last}", file=sys.stderr)
    return None


def implied(a):
    """American odds -> implied probability INCLUDING the book's margin."""
    a = float(a)
    return 100.0 / (a + 100.0) if a > 0 else abs(a) / (abs(a) + 100.0)


def american(dec):
    return (dec - 1) * 100 if dec >= 2 else -100 / (dec - 1)


def outs_from_ip(ip):
    """
    Innings pitched -> outs.

    Baseball writes thirds as decimals: 6.2 is six and TWO THIRDS, not six point
    two. Treating it as a float is the classic way to get this wrong, and every
    "over 16.5 outs" prop turns on exactly this conversion.
    """
    whole, _, frac = str(ip or "0").partition(".")
    return int(whole or 0) * 3 + int(frac or 0)


def board(ymd):
    """Tonight's MLB moneylines with the hold on each game."""
    d = get("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb"
            f"/scoreboard?dates={ymd}")
    games = []
    for ev in (d or {}).get("events", []):
        if (ev.get("status", {}).get("type", {}) or {}).get("state") != "pre":
            continue
        c = (ev.get("competitions") or [{}])[0]
        o = (c.get("odds") or [{}])[0]

        def leg(side):
            blk = (o.get("moneyline") or {}).get(side) or {}
            for when in ("close", "open"):
                v = (blk.get(when) or {}).get("odds")
                if v not in (None, ""):
                    return v
            return (o.get(f"{side}TeamOdds") or {}).get("moneyLine")

        a = next((x for x in c.get("competitors", []) if x.get("homeAway") == "away"), {})
        h = next((x for x in c.get("competitors", []) if x.get("homeAway") == "home"), {})
        ml_a, ml_h = leg("away"), leg("home")
        if ml_a in (None, "") or ml_h in (None, ""):
            continue
        ia, ih = implied(ml_a), implied(ml_h)
        tot = ia + ih
        games.append({
            "away": (a.get("team") or {}).get("abbreviation"),
            "home": (h.get("team") or {}).get("abbreviation"),
            "ml_away": int(ml_a), "ml_home": int(ml_h),
            "hold": (tot - 1) * 100,
            "true_away": ia / tot * 100, "true_home": ih / tot * 100,
        })
    return games


def starters(ymd):
    """
    Probable starters and the SHAPE of their workload, not the average.

    An "over 16.5 outs" line is a question about the middle of a distribution.
    A 5.4 IP season average tells you nothing about how often he actually gets
    the 17th out; the hit rate and the median do.
    """
    # hydrate=team as well: without it the schedule's team object carries only
    # id/name/link and abbreviation comes back None.
    d = get("https://statsapi.mlb.com/api/v1/schedule?sportId=1&date="
            f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}&hydrate=probablePitcher,team")
    out = []
    for day in (d or {}).get("dates", []):
        for gm in day.get("games", []):
            for side in ("away", "home"):
                p = (gm.get("teams", {}).get(side, {}) or {}).get("probablePitcher")
                if not p:
                    continue
                log = get(f"https://statsapi.mlb.com/api/v1/people/{p['id']}"
                          f"/stats?stats=gameLog&group=pitching&season={ymd[:4]}")
                splits = ((log or {}).get("stats") or [{}])[0].get("splits") or []
                outs = [outs_from_ip(s["stat"].get("inningsPitched"))
                        for s in splits if str(s["stat"].get("gamesStarted")) == "1"]
                if not outs:
                    continue
                srt = sorted(outs)
                out.append({
                    "name": p.get("fullName"),
                    "team": (lambda t: t.get("abbreviation") or t.get("teamName")
                             or t.get("name") or "?")(
                                 gm.get("teams", {}).get(side, {}).get("team") or {}),
                    "starts": len(outs),
                    "median": srt[len(srt) // 2],
                    "last8": outs[-8:],
                    # The lines books actually hang on starters.
                    "rates": {n: sum(1 for o in outs if o >= n) / len(outs) * 100
                              for n in (15, 16, 17, 18, 19, 21)},
                })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    a = ap.parse_args()
    d = (datetime.strptime(a.date, "%Y-%m-%d") if a.date
         else datetime.now(timezone.utc) - timedelta(hours=5))
    ymd = d.strftime("%Y%m%d")

    print(f"# Reply ammunition — {d.strftime('%a, %b %d %Y')}\n")

    g = board(ymd)
    if not g:
        print("No priced MLB games on the board.")
        return

    print("## What each moneyline costs you\n")
    print(f"{'game':<12}{'price':<16}{'house edge':>11}   true")
    for x in g:
        px = f"{x['ml_away']:+}/{x['ml_home']:+}"
        print(f"{x['away']+' @ '+x['home']:<12}{px:<16}{x['hold']:>10.2f}%   "
              f"{x['true_away']:.1f}/{x['true_home']:.1f}")

    holds = [x["hold"] for x in g]
    avg = sum(holds) / len(holds)
    print(f"\n  low {min(holds):.2f}%   high {max(holds):.2f}%   average {avg:.2f}%")

    print("\n## The compounding table — the stat nobody else publishes\n")
    print("  Stack n of tonight's moneylines into a parlay and the book keeps:\n")
    for n in (2, 3, 4, 5, 6, 8, 10, 12):
        print(f"    {n:>2} legs   {(1-(1-avg/100)**n)*100:5.1f}%")
    print("\n  The margin compounds. The payout doesn't.")

    print("\n## Break-even ladder\n")
    print("  For the round numbers that turn up in other people's posts:\n")
    for o in (-300, -200, -150, -130, -110, 100, 130, 150, 200, 300, 616, 1000):
        print(f"    {o:>+6}   {implied(o)*100:>5.1f}%")

    print("\n## Starters — outs recorded, by hit rate\n")
    print("  Every 'over X.5 outs' prop is a question about the middle of this\n"
          "  distribution, which a season IP average hides.\n")
    s = starters(ymd)
    if not s:
        print("  (no probable starters posted yet)")
    for p in sorted(s, key=lambda x: x["team"] or ""):
        r = p["rates"]
        print(f"  {p['name']} ({p['team']}) — {p['starts']} starts, median {p['median']} outs")
        print(f"     15+ {r[15]:4.0f}%   16+ {r[16]:4.0f}%   17+ {r[17]:4.0f}%   "
              f"18+ {r[18]:4.0f}%   19+ {r[19]:4.0f}%   21+ {r[21]:4.0f}%")
        print(f"     last 8: {p['last8']}")

    print("\n---\nAt -110 a prop needs 52.4%. Any hit rate below that is a fade,\n"
          "and any line set at a starter's median is a line the book likes.")


if __name__ == "__main__":
    main()
