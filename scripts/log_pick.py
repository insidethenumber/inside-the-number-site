#!/usr/bin/env python3
"""
Record every published pick, then grade it once the game is final.

Why this exists
---------------
The site publishes a free pick most days and has done for weeks. Nothing ever
wrote it down. The pick appears on the homepage, goes out in the newsletter,
and is gone the next morning -- so after three weeks of picking there is no
answer to "are these any good", either for a reader or for us.

That is the whole problem. Not a design decision, just a missing file.

This keeps data/picks.json: one row per pick, graded against the final score
when it lands. It deliberately does NOT touch the daily automation -- that runs
unattended at 6am and breaking it is worse than having no log. Call this
alongside, not inside.

Grading is intentionally conservative. A pick is only marked win or loss when
the result is unambiguous; anything odd is left pending for a human. A record
that quietly mis-grades itself is worse than no record at all, because it looks
authoritative.

Usage
-----
    # record a pick (run when it is published, before kickoff)
    python3 scripts/log_pick.py add \\
        --sport MLB --game "DET @ MIN" --side "under 8.5" \\
        --price -110 --event-id 401816770

    # grade anything finished (safe to run repeatedly)
    python3 scripts/log_pick.py grade

    # see where we stand
    python3 scripts/log_pick.py record
"""

import argparse
import json
import pathlib
import sys
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "picks.json"

ESPN = ("https://site.api.espn.com/apis/site/v2/sports/"
        "{path}/scoreboard/{eid}")

# ESPN's path segment per league we pick in.
PATHS = {
    "MLB": "baseball/mlb",
    "NFL": "football/nfl",
    "CFB": "football/college-football",
    "NBA": "basketball/nba",
    "NHL": "hockey/nhl",
}


# --------------------------------------------------------------- storage
def load():
    if not LOG.exists():
        return {"picks": []}
    try:
        return json.loads(LOG.read_text())
    except json.JSONDecodeError:
        sys.exit(f"ERROR: {LOG} is not valid JSON. Refusing to overwrite it.")


def save(data):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(data, indent=1) + "\n")


# ------------------------------------------------------------------ add
def cmd_add(a):
    data = load()
    today = a.date or datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")

    # One pick per sport per day. Re-running the morning task should update
    # the row, not silently create a second one and inflate the sample.
    for p in data["picks"]:
        if p["date"] == today and p["sport"] == a.sport:
            p.update(game=a.game, side=a.side, price=a.price,
                     event_id=a.event_id, note=a.note)
            save(data)
            print(f"updated {today} {a.sport}: {a.side}")
            return

    data["picks"].append({
        "date": today,
        "sport": a.sport,
        "game": a.game,
        "side": a.side,
        "price": a.price,
        "event_id": a.event_id,
        "note": a.note,
        "result": "pending",   # pending | win | loss | push | void
        "final": None,
    })
    save(data)
    print(f"logged {today} {a.sport}: {a.side} at {a.price:+d}")


# ---------------------------------------------------------------- grade
def fetch_final(sport, eid):
    """Return (home_score, away_score, completed) or None if unavailable."""
    path = PATHS.get(sport)
    if not path or not eid:
        return None
    try:
        with urllib.request.urlopen(ESPN.format(path=path, eid=eid),
                                    timeout=15) as r:
            d = json.loads(r.read())
    except Exception:
        return None
    try:
        comp = d["header"]["competitions"][0]
        if not comp.get("status", {}).get("type", {}).get("completed"):
            return None
        home = away = None
        for c in comp["competitors"]:
            if c["homeAway"] == "home":
                home = int(c["score"])
            else:
                away = int(c["score"])
        if home is None or away is None:
            return None
        return home, away, True
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def grade_total(side, home, away):
    """'under 8.5' / 'over 8.5' -> win|loss|push, or None if unparseable."""
    parts = side.lower().split()
    if len(parts) < 2 or parts[0] not in ("over", "under"):
        return None
    try:
        line = float(parts[1])
    except ValueError:
        return None
    total = home + away
    if total == line:
        return "push"
    if parts[0] == "over":
        return "win" if total > line else "loss"
    return "win" if total < line else "loss"


def cmd_grade(a):
    data = load()
    changed = 0
    skipped = []
    for p in data["picks"]:
        if p["result"] != "pending":
            continue
        got = fetch_final(p["sport"], p.get("event_id"))
        if not got:
            continue
        home, away, _ = got
        p["final"] = {"home": home, "away": away}

        res = grade_total(p["side"], home, away)
        if res is None:
            # Sides and spreads need to know which team is home, and the
            # abbreviations in "game" are not reliable enough to bet a record
            # on. Leave it for a human rather than guess.
            skipped.append(f'{p["date"]} {p["sport"]} "{p["side"]}"')
            continue
        p["result"] = res
        changed += 1
        print(f'{p["date"]} {p["sport"]} {p["side"]}: {res.upper()} '
              f'({away}-{home}, total {home+away})')

    save(data)
    print(f"\ngraded {changed}")
    if skipped:
        print("needs manual grading (not a total):")
        for s in skipped:
            print("  ", s)


# --------------------------------------------------------------- record
def cmd_record(a):
    data = load()
    picks = data["picks"]
    done = [p for p in picks if p["result"] in ("win", "loss")]
    pending = [p for p in picks if p["result"] == "pending"]
    pushes = [p for p in picks if p["result"] == "push"]

    if not done:
        print(f"{len(picks)} logged, none graded yet "
              f"({len(pending)} pending).")
        return

    w = sum(1 for p in done if p["result"] == "win")
    l = len(done) - w

    # Units at the actual price taken, not assumed -110.
    units = 0.0
    for p in done:
        price = p["price"]
        if p["result"] == "win":
            units += (price / 100) if price > 0 else (100 / -price)
        else:
            units -= 1
    roi = units / len(done) * 100

    print(f"{w}-{l}" + (f"-{len(pushes)}" if pushes else ""))
    print(f"{units:+.2f} units over {len(done)} graded picks ({roi:+.1f}% ROI)")
    if len(done) < 30:
        print(f"\nSample is {len(done)}. That is far too small to mean "
              f"anything yet -- do not publish this as a claim.")
    if pending:
        print(f"{len(pending)} still pending.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="record a published pick")
    p.add_argument("--sport", required=True, choices=sorted(PATHS))
    p.add_argument("--game", required=True, help='e.g. "DET @ MIN"')
    p.add_argument("--side", required=True, help='e.g. "under 8.5"')
    p.add_argument("--price", required=True, type=int, help="American odds")
    p.add_argument("--event-id", help="ESPN event id, enables auto-grading")
    p.add_argument("--date", help="YYYY-MM-DD, defaults to today")
    p.add_argument("--note", default="", help="one line of reasoning")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("grade", help="grade finished picks")
    p.set_defaults(func=cmd_grade)

    p = sub.add_parser("record", help="print the running record")
    p.set_defaults(func=cmd_record)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
