#!/usr/bin/env python3
"""
Cache team logos into assets/logos/ so the card generator can use them.

Why a separate script that runs in CI: the sandbox Claude works in cannot
reach a.espncdn.com at all (every request returns nothing), but a GitHub
Actions runner can — it is already pulling the scoreboard every morning. So
the logos get fetched once on the runner, committed, and from then on the
card generator just reads them off disk with no network at all.

Logos are trademarks of their schools and clubs. They are used here the way
every odds publisher uses them: to identify the team a number belongs to, in
editorial coverage of a real game. No endorsement is implied or claimed.

    python3 scripts/fetch_logos.py            # all covered leagues
    python3 scripts/fetch_logos.py --league CFB
"""

import argparse, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "logos")

# CFB carries every FBS team, so it needs the higher limit.
LEAGUES = {
    "MLB": ("baseball/mlb", 60),
    "NFL": ("football/nfl", 60),
    "CFB": ("football/college-football", 400),
    "NBA": ("basketball/nba", 60),
    "NHL": ("hockey/nhl", 60),
    "CBB": ("basketball/mens-college-basketball", 400),
}
UA = {"User-Agent": "Mozilla/5.0 (compatible; InsideTheNumber/1.0)"}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_league(label, path, limit):
    url = (f"https://site.api.espn.com/apis/site/v2/sports/{path}"
           f"/teams?limit={limit}")
    try:
        data = json.loads(get(url).decode())
    except Exception as e:
        print(f"  {label:<4} teams list FAILED: {e}", file=sys.stderr)
        return 0

    entries = []
    for grp in data.get("sports", [{}])[0].get("leagues", [{}]):
        for t in grp.get("teams", []):
            team = t.get("team", {})
            abbr = (team.get("abbreviation") or "").upper()
            logos = team.get("logos") or []
            href = logos[0].get("href") if logos else None
            if abbr and href:
                entries.append((abbr, href))

    d = os.path.join(OUT, label.lower())
    os.makedirs(d, exist_ok=True)
    got = 0
    for abbr, href in entries:
        dest = os.path.join(d, f"{abbr}.png")
        if os.path.exists(dest) and os.path.getsize(dest) > 500:
            got += 1
            continue                      # already cached, don't re-download
        try:
            blob = get(href, timeout=20)
            if len(blob) < 500:
                raise ValueError(f"suspiciously small ({len(blob)}B)")
            with open(dest, "wb") as fh:
                fh.write(blob)
            got += 1
            time.sleep(0.05)              # be polite, this is their CDN
        except Exception as e:
            print(f"    {label} {abbr}: {e}", file=sys.stderr)
    print(f"  {label:<4} {got}/{len(entries)} logos in assets/logos/{label.lower()}/")
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--league", choices=sorted(LEAGUES),
                    help="just one league (default: all)")
    a = ap.parse_args()
    todo = [a.league] if a.league else list(LEAGUES)
    total = 0
    for lg in todo:
        p, lim = LEAGUES[lg]
        total += fetch_league(lg, p, lim)
    print(f"total {total} logos cached")
    if total == 0:
        sys.exit("no logos fetched — refusing to report success")


if __name__ == "__main__":
    main()
