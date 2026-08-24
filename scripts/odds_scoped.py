#!/usr/bin/env python3
"""
Inside the Number — scoped Odds API puller.

Pulls ONLY what ESPN cannot give us, because the free tier is 500 credits a
month and a naive full-board pull costs 16 credits a go.

That 16 is measured, not estimated. Odds API check run #1, Aug 24 2026:

    baseball_mlb            22 events   3 credits
    americanfootball_nfl   272 events   3
    americanfootball_ncaaf 111 events   3
    basketball_nba          41 events   3
    icehockey_nhl           32 events   3
    mma_mixed_martial_arts  59 events   1
                                       --
                                       16  -> 480/month once daily, 960 twice

The same run killed the assumption the budget had been resting on. The docs
say an empty response is not charged, so out-of-season sports were supposed to
be free -- but nothing comes back empty. Books post next-season lines months
ahead, so in AUGUST the NBA returned 41 events and the NHL 32. There is no
seasonal discount. Plan for the full price year round.

So this script buys two things only, both of which ESPN genuinely cannot do:

  1. UFC prices. ESPN carries no MMA odds at all. 1 credit, h2h only.
  2. Best price across ~50 books, on the two or three games we actually
     published a pick on. Grouped by sport so overlapping picks share a call.

Roughly 7 credits a day, about 210 a month, run twice daily and still inside
the free tier with room to spare.

    python3 scripts/odds_scoped.py --mode morning   --dry-run
    python3 scripts/odds_scoped.py --mode morning
    python3 scripts/odds_scoped.py --mode afternoon

Morning takes the opening snapshot. Afternoon re-shops the same picks and
diffs against it, which is where the line-movement copy comes from.
"""

import argparse, json, os, re, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
INDEX = os.path.join(ROOT, "index.html")
BASE = "https://api.the-odds-api.com/v4"

# Keep a floor in reserve. Running the quota to zero mid-month means the UFC
# card on the last Saturday goes uncovered, which is the one thing this feed
# is actually here for.
RESERVE = 40

SPORT_KEY = {
    "MLB":  "baseball_mlb",
    "NFL":  "americanfootball_nfl",
    "CFB":  "americanfootball_ncaaf",
    "NBA":  "basketball_nba",
    "NHL":  "icehockey_nhl",
    "UFC":  "mma_mixed_martial_arts",
    "WNBA": "basketball_wnba",
}


# ── credentials ────────────────────────────────────────────────────────────

def api_key():
    k = os.environ.get("ODDS_API_KEY")
    if k:
        return k
    for cand in (os.path.join(ROOT, "itn-secrets.env"),
                 os.path.expanduser("~/Documents/Claude/Projects/itn-secrets.env")):
        if os.path.exists(cand):
            for line in open(cand):
                if line.strip().startswith("ODDS_API_KEY="):
                    v = line.split("=", 1)[1].strip()
                    if v:
                        return v
    sys.exit("ERROR: no ODDS_API_KEY (env var or itn-secrets.env).")


# ── reading today's published picks ────────────────────────────────────────

def parse_picks(path=INDEX):
    """
    Pull today's picks out of the todaysGames array in index.html.

    index.html is deliberately the single source of truth for the slate -- the
    same array renders the ticker and the card, and its comment says so. Adding
    a parallel picks.json for this script to read would create a second thing to
    keep in sync, and every recurring bug in this project so far has been two
    copies of one fact drifting apart. So: read the source of truth, and fail
    loudly if its shape changes.

    Deliberately NOT a JSON parse. That array is JavaScript -- unquoted keys,
    single quotes, curly apostrophes in the prose. Pulling out the four fields
    that matter with targeted regex is more robust here than trying to coerce
    JS into JSON.
    """
    src = open(path, encoding="utf-8").read()
    m = re.search(r"const\s+todaysGames\s*=\s*\[(.*?)\n\s*\];", src, re.S)
    if not m:
        sys.exit("ERROR: could not find the todaysGames array in index.html. "
                 "If its shape changed, update parse_picks().")
    body = m.group(1)

    picks = []
    # Each entry starts at "{ league:" -- split on that rather than trying to
    # balance braces, since the prose fields contain no braces.
    for chunk in re.split(r"\{\s*league\s*:", body)[1:]:
        def grab(field):
            mm = re.search(field + r"\s*:\s*'((?:[^'\\]|\\.)*)'", chunk)
            return mm.group(1) if mm else None

        league = re.match(r"\s*'([^']+)'", chunk)
        league = league.group(1) if league else None
        pick = grab("pick")
        if not league or not pick or pick == "null":
            continue                      # no play on this game

        away_name = grab(r"away\s*:\s*\{[^}]*?name")
        home_name = grab(r"home\s*:\s*\{[^}]*?name")
        picks.append({
            "league": league,
            "away": away_name,
            "home": home_name,
            "pick": pick,
            "free": "free:true" in chunk.replace(" ", ""),
            "market": classify(pick),
        })
    return picks


def classify(pick):
    """
    Which market a pick string names.

    We only pay for the market we actually took a position in. Asking for
    h2h,spreads,totals when the pick is a total costs three credits instead of
    one, and gets us two markets nobody will read.
    """
    p = pick.lower()
    if re.search(r"\b(over|under)\b|\bo\d|\bu\d", p):
        return "totals"
    if re.search(r"[+-]\d+\.5\b", p):     # -1.5, +4.5 -- a handicap
        return "spreads"
    return "h2h"


# ── the API ────────────────────────────────────────────────────────────────

def call(path, **params):
    params["apiKey"] = api_key()
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            return (json.loads(r.read().decode()),
                    int(r.headers.get("x-requests-last") or 0),
                    int(r.headers.get("x-requests-remaining") or -1))
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        if e.code == 401:
            sys.exit("ERROR: key rejected (401). Check ODDS_API_KEY.")
        if e.code == 429:
            sys.exit("ERROR: out of credits (429). Free tier is 500/month.")
        print(f"  WARN HTTP {e.code} on {path}: {body}", file=sys.stderr)
        return None, 0, -1
    except urllib.error.URLError as e:
        # The Claude sandbox cannot reach this host at all (tunnel 403); a
        # GitHub runner can. That is a different problem from a bad key.
        sys.exit(f"ERROR: could not reach {BASE} ({e.reason}).\n"
                 "  Expected in the local sandbox -- run this in GitHub Actions.")


def implied(american):
    v = float(american)
    return 100.0 / (v + 100.0) if v > 0 else abs(v) / (abs(v) + 100.0)


def best_across_books(event, market, line_hint=None):
    """
    Best available price per outcome across every book quoting this event.

    Shopping both sides is the highest-return habit in betting and it is
    invisible if you only ever look at one book -- which is exactly the ESPN
    limitation this whole feed exists to fix.
    """
    best = {}
    for bk in event.get("bookmakers", []):
        for mk in bk.get("markets", []):
            if mk.get("key") != market:
                continue
            for oc in mk.get("outcomes", []):
                name, price = oc.get("name"), oc.get("price")
                if price is None:
                    continue
                # For spreads and totals the price is only comparable at the
                # same number. -1.5 at +108 and -0.5 at -140 are not two
                # quotes on one bet.
                point = oc.get("point")
                if line_hint is not None and point is not None:
                    if abs(float(point)) != abs(float(line_hint)):
                        continue
                key = name if point is None else f"{name} {point:+g}"
                cur = best.get(key)
                if cur is None or price > cur["price"]:
                    best[key] = {"price": price, "book": bk.get("title"),
                                 "point": point}
    if len(best) == 2:
        (ka, da), (kb, db) = best.items()
        tot = implied(da["price"]) + implied(db["price"])
        if tot > 0:
            da["true"] = round(implied(da["price"]) / tot * 100, 1)
            db["true"] = round(implied(db["price"]) / tot * 100, 1)
            for d in (da, db):
                d["hold"] = round((tot - 1) * 100, 2)
    return best


def match_event(events, pick):
    """
    Find our game in the Odds API's list.

    They use full club names ("Seattle Mariners"); index.html stores the short
    nickname ("Mariners"). Substring both directions and require BOTH sides to
    agree, so "Giants" cannot match the wrong league's Giants.

    UFC has no home or away, and index.html keys fights on last names, so fall
    back to matching either name against either corner.
    """
    def norm(s):
        return re.sub(r"[^a-z ]", "", (s or "").lower())

    a, h = norm(pick["away"]), norm(pick["home"])
    for ev in events:
        ea, eh = norm(ev.get("away_team")), norm(ev.get("home_team"))
        if not a or not h:
            continue
        if (a in ea or ea in a) and (h in eh or eh in h):
            return ev
        if (a in eh or eh in a) and (h in ea or ea in h):   # UFC / side flip
            return ev
    return None


def line_of(pick):
    """
    The handicap or total in the pick, so we compare like with like.

    "Reds -1.5 (+108)" -> 1.5. Note this must not pick up the PRICE in the
    parentheses: -1.5 is the bet, +108 is what it pays. Matching only on a
    half-point keeps the two apart, since American prices are whole numbers.
    """
    m = re.search(r"[+-]?\d+\.5\b", pick)
    return abs(float(m.group(0))) if m else None


# ── usage ledger ───────────────────────────────────────────────────────────

def ledger_path():
    return os.path.join(DATA, "odds-usage.json")


def load_ledger():
    p = ledger_path()
    if os.path.exists(p):
        return json.load(open(p))
    return {"runs": []}


def save_ledger(led):
    os.makedirs(DATA, exist_ok=True)
    led["runs"] = led["runs"][-120:]     # keep it from growing without bound
    json.dump(led, open(ledger_path(), "w"), indent=1)


# ── main ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["morning", "afternoon"], default="morning")
    ap.add_argument("--dry-run", action="store_true",
                    help="plan the calls and print the cost, spend nothing")
    a = ap.parse_args()

    picks = parse_picks()
    if not picks:
        print("No published picks in index.html. Nothing to shop.")

    print(f"Today's published picks ({len(picks)}):")
    for p in picks:
        tag = "FREE" if p["free"] else "pro"
        print(f"  {p['league']:<5} {p['away']} @ {p['home']:<14} "
              f"{p['pick']:<24} -> {p['market']:<8} [{tag}]")

    # Group picks by sport, union the markets. Two MLB picks in different
    # markets cost 2 credits total, not 2 calls of 3.
    plan = {}
    for p in picks:
        key = SPORT_KEY.get(p["league"])
        if not key:
            print(f"  WARN no Odds API sport key for {p['league']}", file=sys.stderr)
            continue
        plan.setdefault(key, set()).add(p["market"])

    # UFC every morning regardless of whether we picked it -- ESPN has zero MMA
    # prices, so this is the only place Saturday's card can come from.
    if a.mode == "morning":
        plan.setdefault(SPORT_KEY["UFC"], set()).add("h2h")

    cost = sum(len(v) for v in plan.values())     # 1 credit per market, 1 region
    print(f"\nPlanned calls ({cost} credits, mode={a.mode}):")
    for sport, markets in sorted(plan.items()):
        print(f"  {sport:<28} {','.join(sorted(markets))}")

    if a.dry_run:
        print("\nDRY RUN — nothing called, no credits spent.")
        return

    if not plan:
        print("Nothing to call.")
        return

    out, spent, remaining = [], 0, None
    for sport, markets in sorted(plan.items()):
        if remaining is not None and remaining - len(markets) < RESERVE:
            print(f"::warning title=Odds credits low::Stopping before {sport}. "
                  f"{remaining} left, reserve is {RESERVE}.")
            break
        events, last, rem = call(f"/sports/{sport}/odds", regions="us",
                                 markets=",".join(sorted(markets)),
                                 oddsFormat="american")
        spent += last
        if rem >= 0:
            remaining = rem
        if events is None:
            continue

        if sport == SPORT_KEY["UFC"] and a.mode == "morning":
            out.append({"kind": "ufc_board", "sport": sport,
                        "events": summarize_ufc(events)})

        for p in picks:
            if SPORT_KEY.get(p["league"]) != sport:
                continue
            ev = match_event(events, p)
            if not ev:
                print(f"  no match on the board for {p['away']} @ {p['home']}",
                      file=sys.stderr)
                continue
            best = best_across_books(ev, p["market"], line_of(p["pick"]))
            out.append({
                "kind": "pick_shop", "league": p["league"], "pick": p["pick"],
                "free": p["free"], "market": p["market"],
                "away": ev.get("away_team"), "home": ev.get("home_team"),
                "commence": ev.get("commence_time"),
                "books": len(ev.get("bookmakers", [])),
                "best": best,
            })

    stamp = datetime.now(timezone.utc).isoformat()
    os.makedirs(DATA, exist_ok=True)
    snap = {"generated_utc": stamp, "mode": a.mode,
            "credits_spent": spent, "credits_remaining": remaining,
            "results": out}

    path = os.path.join(DATA, f"odds-{a.mode}.json")
    json.dump(snap, open(path, "w"), indent=1)

    # Afternoon run: diff against this morning to get the movement copy.
    if a.mode == "afternoon":
        movement(snap)

    led = load_ledger()
    led["runs"].append({"at": stamp, "mode": a.mode, "spent": spent,
                        "remaining": remaining})
    save_ledger(led)

    print(f"\nwrote {os.path.relpath(path, ROOT)}")
    print(f"credits: spent {spent} this run, {remaining} remaining this month")
    month = sum(r["spent"] for r in led["runs"]
                if r["at"][:7] == stamp[:7])
    print(f"spent so far in {stamp[:7]}: {month}")

    # The upgrade trigger, enforced rather than remembered.
    #
    # Chuck's decision on Aug 24 was to stay on the free tier until there is
    # traffic, and to be REMINDED rather than left to notice. A note in
    # BACKLOG.md is not a reminder -- nobody reads a backlog on the day it
    # matters. So the run itself raises it, in the place he will actually be
    # looking when something breaks.
    if month > 400:
        print(f"::warning title=Odds upgrade trigger::{month} credits used this "
              "month, over the 400 threshold on a 500 cap. Time to revisit the "
              "$30/mo plan -- see BACKLOG.md 'Odds API'.")
    if remaining is not None and remaining < RESERVE * 2:
        print(f"::warning title=Odds credits low::{remaining} credits left. "
              "Free tier resets monthly; consider the $30 plan if traffic justifies it.")


def summarize_ufc(events):
    """Trim the UFC board to what a reader can use. 59 events is not a card."""
    rows = []
    for ev in events[:40]:
        best = best_across_books(ev, "h2h")
        if len(best) != 2:
            continue
        (ka, da), (kb, db) = best.items()
        rows.append({
            "commence": ev.get("commence_time"),
            "a": {"name": ka, "price": da["price"], "book": da["book"],
                  "true": da.get("true")},
            "b": {"name": kb, "price": db["price"], "book": db["book"],
                  "true": db.get("true")},
            "hold": da.get("hold"),
            "books": len(ev.get("bookmakers", [])),
        })
    rows.sort(key=lambda r: r["commence"] or "")
    return rows


def movement(pm):
    """
    Compare the afternoon shop against the morning one.

    This is the whole reason for a second pull. One snapshot is a price; two is
    a story -- "this went from -118 to -105 since breakfast" is something no
    free site publishes well, and it costs us three credits.
    """
    am_path = os.path.join(DATA, "odds-morning.json")
    if not os.path.exists(am_path):
        print("no morning snapshot to compare against", file=sys.stderr)
        return
    am = json.load(open(am_path))
    if am.get("generated_utc", "")[:10] != pm.get("generated_utc", "")[:10]:
        print("morning snapshot is from another day — skipping movement",
              file=sys.stderr)
        return

    def index(snap):
        return {r["pick"]: r for r in snap["results"] if r["kind"] == "pick_shop"}

    a_i, p_i = index(am), index(pm)
    moves = []
    for pick, now in p_i.items():
        then = a_i.get(pick)
        if not then:
            continue
        for side, nb in (now.get("best") or {}).items():
            ob = (then.get("best") or {}).get(side)
            if not ob:
                continue
            d = nb["price"] - ob["price"]
            if d:
                moves.append({"pick": pick, "side": side,
                              "open": ob["price"], "now": nb["price"],
                              "delta": d, "book_now": nb["book"]})
    pm["movement"] = moves
    json.dump(pm, open(os.path.join(DATA, "odds-afternoon.json"), "w"), indent=1)

    if not moves:
        print("\nNo price movement on our picks since this morning.")
        return
    print("\nMovement since this morning:")
    for m in sorted(moves, key=lambda x: -abs(x["delta"])):
        print(f"  {m['pick']:<26} {m['side']:<22} "
              f"{m['open']:+} -> {m['now']:+}  ({m['delta']:+}) @ {m['book_now']}")


if __name__ == "__main__":
    main()
