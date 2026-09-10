#!/usr/bin/env python3
"""
Cache NFL player headshots into assets/headshots/ for the card generator.

Why a separate CI script, same reason as fetch_logos.py: the sandbox Claude
works in cannot reach a.espncdn.com at all, but a GitHub Actions runner can.
Fetch once on the runner, commit, and every downstream build reads off disk
with no network.

WHAT THESE ARE, precisely, because it matters:

These are team-issued roster portraits — the standard posed headshot every
club publishes on its own roster page, the one that appears on ESPN, on
fantasy apps, and on every betting graphic in the category. They are NOT
wire game action. A wire photographer's game frame is somebody's copyrighted
work that costs $50-$100 to license; a roster portrait is a publicity photo
the league distributes to be used when identifying the player.

That distinction is real but it is not a licence. Copyright sits with the
league or the club, ESPN's CDN is a delivery host and not a grant, and the
player holds a right of publicity on top of that. We use them the way every
odds publisher uses a team logo: to identify the human a number belongs to,
inside editorial commentary about a real game.

The hard line, from docs/EDITORIAL-DOCTRINE.md, which no file size or
resolution changes:

    A player's face never appears on a graphic carrying a price, a promo
    code, an affiliate link, or the word "premium."

Odds are fine — "+425 via DraftKings" is a fact about the market, and
reporting it is commentary. Our subscription price next to the same face is
his likeness selling our product. Different thing entirely.

    python3 scripts/fetch_headshots.py
    python3 scripts/fetch_headshots.py --force
"""

import argparse, json, os, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "headshot_manifest.json")
OUT = os.path.join(ROOT, "assets", "headshots")

# Same UA fetch_logos.py settled on: ESPN/Akamai 403s a "compatible; bot"
# string from a GitHub runner but accepts an honest curl UA.
UA = {"User-Agent": "curl/8.5.0", "Accept": "*/*"}

URL = "https://a.espncdn.com/i/headshots/{league}/players/full/{pid}.png"

# A 1x1 or otherwise tiny response means ESPN has no portrait for that id and
# served a placeholder. Better to have no file than a grey silhouette we then
# paste onto a card at 300px.
MIN_BYTES = 4000


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download players we already have")
    ap.add_argument("--league", default=None, help="only this league key")
    a = ap.parse_args()

    with open(MANIFEST) as f:
        man = json.load(f)

    got = skipped = failed = 0
    credits = {}

    for league, players in man.items():
        if league.startswith("_"):
            continue
        if a.league and league != a.league:
            continue
        d = os.path.join(OUT, league)
        os.makedirs(d, exist_ok=True)

        for p in players:
            pid = str(p["id"])
            dest = os.path.join(d, f"{pid}.png")
            if os.path.exists(dest) and not a.force:
                skipped += 1
                credits[f"{league}/{pid}"] = p
                continue
            url = URL.format(league=league, pid=pid)
            try:
                blob = get(url)
            except urllib.error.HTTPError as e:
                print(f"  MISS {p['name']:24s} HTTP {e.code}", file=sys.stderr)
                failed += 1
                continue
            except Exception as e:
                print(f"  MISS {p['name']:24s} {e}", file=sys.stderr)
                failed += 1
                continue
            if len(blob) < MIN_BYTES:
                print(f"  TINY {p['name']:24s} {len(blob)}b - no portrait, skipping",
                      file=sys.stderr)
                failed += 1
                continue
            with open(dest, "wb") as f:
                f.write(blob)
            print(f"  ok   {p['name']:24s} {len(blob):>7,}b  {p['team']} {p['pos']}")
            credits[f"{league}/{pid}"] = p
            got += 1
            time.sleep(0.2)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "CREDITS.json"), "w") as f:
        json.dump({
            "source": "ESPN CDN roster portraits (a.espncdn.com/i/headshots)",
            "what": "Team-issued roster publicity portraits, not wire game action.",
            "use": ("Editorial identification of the player a number belongs to. "
                    "Never on a graphic carrying a price, promo code, affiliate "
                    "link or the word premium."),
            "players": credits,
        }, f, indent=2)

    print(f"\nheadshots: {got} new, {skipped} cached, {failed} failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
